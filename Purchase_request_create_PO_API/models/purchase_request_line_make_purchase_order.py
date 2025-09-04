# -*- coding: utf-8 -*-

import xmlrpc.client
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = 'purchase.request.line.make.purchase.order'

    # Add a new field to allow the user to choose between local and remote creation on the UI
    is_remote_creation = fields.Boolean(
        string="Create on Remote Server?",
        default=False,
        help="If checked, this Purchase Order will be created on the configured remote Odoo server via API."
    )
    
    # (Optional) Add a field to allow the user to update an existing PO
    remote_po_name = fields.Char(
        string="Update Existing Remote PO",
        help="Optional. To add items to an existing remote PO, enter its reference number here."
    )

    def make_purchase_order(self):
        """
        Override the core creation method. This is our "hijack" point.
        """
        # If the user does not check "Create on Remote Server", execute the original, local Odoo logic
        if not self.is_remote_creation:
            return super(PurchaseRequestLineMakePurchaseOrder, self).make_purchase_order()

        # --- If checked, execute our remote API logic ---
        
        # 1. Get API configuration from the current user's record
        current_user = self.env.user
        url = current_user.x_api_url
        db = current_user.x_api_db
        username = current_user.x_api_username
        api_key = current_user.x_api_password

        if not all([url, db, username, api_key]):
            raise UserError(_(
                "Your user profile is missing remote API configuration. "
                "Please contact your administrator to set it up in your user preferences."
            ))

        try:
            _logger.info(f"Starting remote PO creation for user {current_user.name}")
            
            # 2. Connect to the remote Odoo server
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            uid = common.authenticate(db, username, api_key, {})
            models_proxy = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            
            if not uid:
                raise UserError(_("Authentication with the remote server failed. Please check your API credentials."))

            _logger.info(f"Successfully authenticated with remote server. UID: {uid}")

            # 3. Prepare the data to be sent (based on the wizard's content)
            
            # a. Find the remote vendor ID
            vendor = self.supplier_id
            if not vendor:
                raise UserError(_("Please select a supplier first."))
                
            remote_partner_ids = models_proxy.execute_kw(
                db, uid, api_key, 
                'res.partner', 'search', 
                [[['name', '=', vendor.name], ['supplier_rank', '>', 0]]], 
                {'limit': 1}
            )
            
            if not remote_partner_ids:
                raise UserError(_("Vendor '%s' not found on the remote server.") % vendor.name)

            remote_partner_id = remote_partner_ids[0]
            _logger.info(f"Found remote supplier: {vendor.name} (ID: {remote_partner_id})")

            # b. Prepare the product line data
            order_lines_vals = []
            processed_requests = []
            
            for item in self.item_ids:
                line = item.line_id
                
                if not line.product_id:
                    _logger.warning(f"Skipping line without product: {line.name}")
                    continue
                    
                # Find the remote product by its internal reference (default_code)
                search_domain = []
                if line.product_id.default_code:
                    search_domain = [['default_code', '=', line.product_id.default_code]]
                else:
                    search_domain = [['name', '=', line.product_id.name]]
                    
                remote_product_ids = models_proxy.execute_kw(
                    db, uid, api_key,
                    'product.product', 'search',
                    [search_domain],
                    {'limit': 1}
                )
                
                if not remote_product_ids:
                    raise UserError(_(
                        "Product '%s' (Code: %s) not found on the remote server."
                    ) % (line.product_id.name, line.product_id.default_code or 'N/A'))
                
                # Add to the order lines
                order_lines_vals.append((0, 0, {
                    'product_id': remote_product_ids[0],
                    'product_qty': item.product_qty,
                    'price_unit': line.estimated_cost or 0.0,
                    'name': line.name or line.product_id.name,
                    'date_planned': fields.Datetime.now(),
                }))
                
                # Record the processed requests
                if line.request_id.name not in processed_requests:
                    processed_requests.append(line.request_id.name)
                
                _logger.info(f"Prepared line for product: {line.product_id.name} (Qty: {item.product_qty})")
            
            if not order_lines_vals:
                raise UserError(_("No valid product lines found to create Purchase Order."))

            # c. (Smart logic) Check if an existing PO should be updated
            remote_po_id_to_update = None
            if self.remote_po_name:
                found_pos = models_proxy.execute_kw(
                    db, uid, api_key,
                    'purchase.order', 'search_read',
                    [[['name', '=', self.remote_po_name]]],
                    {'fields': ['id', 'state'], 'limit': 1}
                )
                
                if found_pos:
                    if found_pos[0]['state'] not in ('draft', 'sent'):
                        raise UserError(_("Remote PO %s is already confirmed/locked and cannot be updated.") % self.remote_po_name)
                    remote_po_id_to_update = found_pos[0]['id']
                    _logger.info(f"Found existing PO to update: {self.remote_po_name} (ID: {remote_po_id_to_update})")
                else:
                    raise UserError(_("Remote PO %s not found.") % self.remote_po_name)

            # 4. Execute the remote operation (create or update)
            if remote_po_id_to_update:
                # Update existing PO - add new order lines
                models_proxy.execute_kw(
                    db, uid, api_key,
                    'purchase.order', 'write',
                    [[remote_po_id_to_update], {'order_line': order_lines_vals}]
                )
                final_message = _('Items successfully added to remote PO %s.') % self.remote_po_name
                _logger.info(f"Updated existing remote PO: {self.remote_po_name}")
                
            else:
                # Create a new PO
                po_vals = {
                    'partner_id': remote_partner_id,
                    'order_line': order_lines_vals,
                    'origin': ', '.join(processed_requests),
                    'date_order': fields.Datetime.now(),
                    'notes': f"Created via API from Purchase Requests: {', '.join(processed_requests)}",
                }
                
                new_po_id = models_proxy.execute_kw(
                    db, uid, api_key,
                    'purchase.order', 'create',
                    [po_vals]
                )
                
                # Get the name of the newly created PO
                new_po_data = models_proxy.execute_kw(
                    db, uid, api_key,
                    'purchase.order', 'read',
                    [new_po_id],
                    {'fields': ['name']}
                )
                
                po_name = new_po_data[0]['name'] if new_po_data else f"PO-{new_po_id}"
                final_message = _('Remote PO created successfully: %s (ID: %s)') % (po_name, new_po_id)
                _logger.info(f"Created new remote PO: {po_name} (ID: {new_po_id})")

            # 5. (Important) Update the status of the local purchase request lines
            request_lines = self.item_ids.mapped('line_id')
            request_lines.write({'purchase_state': 'done'})
            
            _logger.info(f"Updated {len(request_lines)} purchase request lines to 'done' state")
            
            # 6. Return a success notification
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Remote PO Creation Successful'),
                    'message': final_message,
                    'type': 'success',
                    'sticky': False
                }
            }

        except xmlrpc.client.Fault as e:
            error_msg = f"XML-RPC Fault: {e.faultString}"
            _logger.error(error_msg)
            raise UserError(_(f"Remote API Error: {e.faultString}"))
            
        except Exception as e:
            error_msg = f"Unexpected error during remote PO creation: {str(e)}"
            _logger.error(error_msg)
            raise UserError(_(f"Failed to create remote PO: {str(e)}"))

    @api.onchange('is_remote_creation')
    def _onchange_is_remote_creation(self):
        """When the remote creation option changes, clear the remote PO name."""
        if not self.is_remote_creation:
            self.remote_po_name = False