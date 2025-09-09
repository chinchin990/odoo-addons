# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    # Override original fields, disable tracking to avoid errors with empty product_id
    name = fields.Char(string="Description", tracking=False)
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="UoM",
        tracking=False,
        domain="[('category_id', '=', product_uom_category_id)]",
    )
    product_qty = fields.Float(
        string="Quantity", tracking=False, digits="Product Unit of Measure"
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        domain=[("purchase_ok", "=", True)],
        tracking=False,
    )

    # Add a remark field - visible only to Purchase Managers
    x_remark = fields.Char(
        string="Remark",
        help="Internal remark for purchase managers only",
        store=True,
        copy=True,
        tracking=False  # Disable field tracking to avoid mail tracking errors
    )

    # Field-level group restrictions (hide from non-managers universally)
    unit_price = fields.Monetary(
        string="Unit Price",
        groups="purchase_request.group_purchase_request_manager,base.group_system",
    )

    # Total Price (estimated_cost): keep compute from upstream, but restrict visibility
    estimated_cost = fields.Monetary(
        groups="purchase_request.group_purchase_request_manager,base.group_system",
        readonly=True,
    )

    @api.onchange('product_id')
    def onchange_product_id(self):
        """Override onchange_product_id to handle cases with an empty product_id"""
        if self.product_id:
            # Only execute original logic if the product exists
            name = self.product_id.name
            if self.product_id.code:
                name = f"[{self.product_id.code}] {name}"
            if self.product_id.description_purchase:
                name += "\n" + self.product_id.description_purchase
            self.product_uom_id = self.product_id.uom_id.id
            self.product_qty = 1
            self.name = name
        else:
            # Do not perform any calculations if the product is empty, to avoid errors
            pass

    def _compute_estimated_cost(self):
        """Override estimated cost calculation to handle empty product_id"""
        for line in self:
            if line.product_id and line.product_qty:
                try:
                    # Only calculate cost if both product and quantity exist
                    line.estimated_cost = line.product_qty * (
                        line.product_id.standard_price or 0.0
                    )
                except:
                    # If calculation fails, set to 0.0
                    line.estimated_cost = 0.0
            else:
                # If there is no product or quantity, cost is 0.0
                line.estimated_cost = 0.0

    def name_get(self):
        """Override name_get to handle empty product_id"""
        result = []
        for line in self:
            if line.product_id:
                # Use normal logic when a product exists
                name = line.product_id.name or line.name or ''
                if line.product_id.code:
                    name = f"[{line.product_id.code}] {name}"
            else:
                # Use the remark or a default name when no product is present
                name = line.x_remark or line.name or _('Empty Line')
            
            result.append((line.id, name))
        return result

    def _compute_display_name(self):
        """Override display_name computation to handle empty product_id"""
        for line in self:
            if line.product_id:
                name = line.product_id.name or ''
                if line.product_id.code:
                    name = f"[{line.product_id.code}] {name}"
                line.display_name = name
            else:
                line.display_name = line.x_remark or line.name or _('Empty Line')

    def write(self, vals):
        """Override the write method to ensure tracking does not fail on empty product_id"""
        # Completely disable tracking to avoid errors
        context = dict(self.env.context)
        context.update({
            'mail_notrack': True,
            'tracking_disable': True,
            'mail_create_nolog': True,
            'mail_create_nosubscribe': True,
        })
        
        return super(PurchaseRequestLine, self.with_context(context)).write(vals)

    @api.model
    def create(self, vals):
        """Override the create method to handle creation with an empty product_id"""
        # If there is no product but there is a remark or quantity, allow creation
        if not vals.get('product_id') and (vals.get('x_remark') or vals.get('product_qty', 0) > 0):
            # Set a default name
            if not vals.get('name'):
                vals['name'] = vals.get('x_remark', _('Empty Line'))
        
        return super(PurchaseRequestLine, self).create(vals)
