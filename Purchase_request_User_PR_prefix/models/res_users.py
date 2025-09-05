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

    def write(self, vals):
        res = super().write(vals)
        # If PR Prefix changed for any user, clear server-side caches so
        # record rules immediately reflect the new prefix without restarting.
        if 'pr_prefix' in vals:
            try:
                # Invalidate this model field cache
                self.invalidate_cache(['pr_prefix'])
                # Clear registry/model/rule caches for this worker
                self.env.registry.clear_caches()
            except Exception:
                # Be defensive: cache clearing should not block the write
                pass
        return res
