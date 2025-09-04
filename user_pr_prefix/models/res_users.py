# -*- coding: utf-8 -*-

from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    # New Field: User's PR Prefix
    pr_prefix = fields.Char(
        string="PR Prefix",
        default="K1-WH-PR-",
        help="Prefix for Purchase Request numbers for this user. Example: K1-WH-PR- will generate K1-WH-PR-2025-0001",
        size=20
    )