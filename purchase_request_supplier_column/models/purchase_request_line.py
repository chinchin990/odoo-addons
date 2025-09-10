# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    # Manager-only free text to note intended supplier on PR line
    x_supplier = fields.Char(string="Supplier", help="Intended supplier for this line")

