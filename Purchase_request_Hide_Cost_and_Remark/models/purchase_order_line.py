# -*- coding: utf-8 -*-

from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # Hide PO line subtotal from non-purchase-managers and non-admins
    price_subtotal = fields.Monetary(
        string="Subtotal",
        groups="purchase.group_purchase_manager,base.group_system",
        readonly=True,
    )

