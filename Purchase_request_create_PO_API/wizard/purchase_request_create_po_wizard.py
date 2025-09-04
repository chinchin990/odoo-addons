# -*- coding: utf-8 -*-

import xmlrpc.client
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class PurchaseRequestCreatePOWizard(models.TransientModel):
    _name = 'purchase.request.create.po.wizard'
    _description = 'Create Purchase Order Remotely via API'

    # Wizard Fields
    is_remote_creation = fields.Boolean(
        string="Create Remote PO",
        default=False,
        help="Check this to create PO on remote Odoo instance via API"
    )
    remote_po_name = fields.Char(
        string="Remote PO Name",
        help="Custom name for the remote Purchase Order (optional)"
    )
    purchase_request_ids = fields.Many2many(
        'purchase.request',
        string="Purchase Requests",
        help="Selected purchase requests to create PO from"
    )

    @api.model
    def default_get(self, fields_list):
        """Get default values, including the selected purchase requests"""
        res = super().default_get(fields_list)
        
        # Get the selected purchase requests from the context
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['purchase_request_ids'] = [(6, 0, active_ids)]
            
        return res

    def action_create_purchase_order(self):
        """Execute the PO creation action"""
        if not self.is_remote_creation:
            # If not creating remotely, use the standard process
            return self._create_local_purchase_order()
        else:
            # Create PO remotely
            return self._create_remote_purchase_order()

    def _create_local_purchase_order(self):
        """Create a local PO (standard process)"""
        # Standard PO creation logic can be called here
        # Or return the user to the standard flow
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Local PO Creation'),
                'message': _('Please use standard Purchase Request workflow for local PO creation.'),
                'type': 'warning',
            }
        }

    def _create_remote_purchase_order(self):
        """Create a remote PO (via API)"""
        # [CORE CHANGE]: Get API configuration from the current user
        current_user = self.env.user
        url = current_user.x_api_url
        db = current_user.x_api_db
        username = current_user.x_api_username
        api_key = current_user.x_api_password

        # Check if the current user has configured API information
        if not all([url, db, username, api_key]):
            raise UserError(_(
                "Your user profile is missing remote API configuration. "
                "Please contact your administrator to set it up in your user preferences."
            ))

        try:
            # Connect to the remote Odoo server
            _logger.info(f"Connecting to remote Odoo at {url}")
            common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
            
            # Validate the API connection
            uid = common.authenticate(db, username, api_key, {})
            if not uid:
                raise UserError(_("Authentication failed. Please check your API credentials."))
            
            _logger.info(f"Successfully authenticated with remote server. UID: {uid}")
            
            # Create a models proxy
            models_proxy = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
            
            # Process each purchase request
            created_po_names = []
            
            for purchase_request in self.purchase_request_ids:
                po_name = self._create_single_remote_po(
                    models_proxy, db, uid, api_key, purchase_request
                )
                if po_name:
                    created_po_names.append(po_name)
            
            # Return a success message
            if created_po_names:
                message = _(f"Successfully created {len(created_po_names)} remote Purchase Orders: {', '.join(created_po_names)}")
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Remote PO Creation Successful'),
                        'message': message,
                        'type': 'success',
                    }
                }
            else:
                raise UserError(_("No Purchase Orders were created."))

        except xmlrpc.client.Fault as e:
            _logger.error(f"XML-RPC Fault: {e}")
            raise UserError(_(f"Remote API Error: {e.faultString}"))
        except Exception as e:
            _logger.error(f"Unexpected error during remote PO creation: {str(e)}")
            raise UserError(_(f"Failed to create remote PO: {str(e)}"))

    def _create_single_remote_po(self, models_proxy, db, uid, api_key, purchase_request):
        """Create a remote PO for a single purchase request"""
        try:
            # Prepare PO data
            po_vals = self._prepare_po_values(purchase_request)
            
            # Create the PO in the remote system
            po_id = models_proxy.execute_kw(
                db, uid, api_key,
                'purchase.order', 'create',
                [po_vals]
            )
            
            # Get the name of the created PO
            po_data = models_proxy.execute_kw(
                db, uid, api_key,
                'purchase.order', 'read',
                [po_id], {'fields': ['name']}
            )
            
            po_name = po_data[0]['name'] if po_data else f"PO-{po_id}"
            
            _logger.info(f"Successfully created remote PO {po_name} for PR {purchase_request.name}")
            return po_name
            
        except Exception as e:
            _logger.error(f"Failed to create remote PO for PR {purchase_request.name}: {str(e)}")
            raise UserError(_(f"Failed to create remote PO for {purchase_request.name}: {str(e)}"))

    def _prepare_po_values(self, purchase_request):
        """Prepare PO creation data"""
        # Basic PO information
        po_vals = {
            'origin': purchase_request.name,
            'date_order': fields.Datetime.now(),
            'notes': f"Created from Purchase Request: {purchase_request.name}",
        }
        
        # If a custom name is specified, use it
        if self.remote_po_name:
            po_vals['name'] = self.remote_po_name
        
        # Prepare PO line data
        po_lines = []
        for line in purchase_request.line_ids:
            if line.product_id:
                line_vals = {
                    'product_id': line.product_id.id,
                    'name': line.name or line.product_id.name,
                    'product_qty': line.product_qty,
                    'product_uom': line.product_uom_id.id if line.product_uom_id else False,
                    'price_unit': 0.0,  # Price needs to be determined based on supplier information
                    'date_planned': fields.Datetime.now(),
                }
                po_lines.append((0, 0, line_vals))
        
        if po_lines:
            po_vals['order_line'] = po_lines
        else:
            raise UserError(_(f"No valid product lines found in Purchase Request {purchase_request.name}"))
        
        return po_vals

    def _get_default_supplier(self, product_id, models_proxy, db, uid, api_key):
        """Get the default supplier for a product"""
        try:
            # Find supplier information for the product
            supplierinfo_ids = models_proxy.execute_kw(
                db, uid, api_key,
                'product.supplierinfo', 'search',
                [['product_tmpl_id.product_variant_ids', 'in', product_id]],
                {'limit': 1}
            )
            
            if supplierinfo_ids:
                supplierinfo = models_proxy.execute_kw(
                    db, uid, api_key,
                    'product.supplierinfo', 'read',
                    [supplierinfo_ids[0]],
                    {'fields': ['partner_id']}
                )
                return supplierinfo[0]['partner_id'][0] if supplierinfo else False
            
            return False
            
        except Exception as e:
            _logger.warning(f"Failed to get supplier for product {product_id}: {str(e)}")
            return False