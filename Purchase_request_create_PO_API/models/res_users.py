# -*- coding: utf-8 -*-

from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    # Using the 'x_' prefix is a good practice in the Odoo community to denote custom fields
    x_api_url = fields.Char(
        string="Remote API URL",
        help="URL of the remote Odoo instance (e.g., https://your-odoo.com)"
    )
    x_api_db = fields.Char(
        string="Remote API Database",
        help="Database name of the remote Odoo instance"
    )
    x_api_username = fields.Char(
        string="Remote API Username",
        help="Username for remote API authentication"
    )
    x_api_password = fields.Char(
        string="Remote API Password",
        password=True,
        help="Password or API key for remote authentication"
    )