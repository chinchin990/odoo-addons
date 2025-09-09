# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    # Line-level status (normal / rejected)
    line_state = fields.Selection(
        [
            ("normal", "Normal"),
            ("rejected", "Rejected"),
        ],
        default="normal",
        string="Line Status",
        tracking=True,
    )

    def action_reject_line(self):
        """Set the line as rejected and log on the parent request."""
        for rec in self:
            if rec.line_state == "rejected":
                continue
            rec.line_state = "rejected"
            if rec.request_id:
                rec.request_id.message_post(
                    body=(
                        _("Line rejected by %s  Product: %s, Qty: %s")
                        % (
                            self.env.user.display_name,
                            rec.product_id.display_name or "-",
                            rec.product_qty,
                        )
                    )
                )
        return True

    def action_reset_line(self):
        """Restore a rejected line to normal and log on the parent request."""
        for rec in self:
            if rec.line_state != "rejected":
                continue
            rec.line_state = "normal"
            if rec.request_id:
                rec.request_id.message_post(
                    body=(
                        _("Line restored to Normal by %s  Product: %s, Qty: %s")
                        % (
                            self.env.user.display_name,
                            rec.product_id.display_name or "-",
                            rec.product_qty,
                        )
                    )
                )
        return True
