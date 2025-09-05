"""Department approval extensions for Purchase Request."""

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    # Reinstate state selection to insert the department approval step explicitly
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("to_be_dept_approved", "To be Dept. Approved"),
            ("to_approve", "To be approved"),
            ("approved", "Approved"),
            ("in_progress", "In progress"),
            ("done", "Done"),
            ("rejected", "Rejected"),
        ],
        string="Status",
        index=True,
        tracking=True,
        required=True,
        copy=False,
        default="draft",
    )

    def button_to_approve(self):
        """Send to department approval after validating lines.

        - Forbid lines that have quantity but missing product
        - Require at least one non-cancelled line with product and qty>0
        - Move to 'to_be_dept_approved'
        """
        for rec in self:
            invalid_lines = rec.line_ids.filtered(
                lambda l: not l.cancelled and (l.product_qty or 0.0) > 0 and not l.product_id
            )
            if invalid_lines:
                raise UserError(
                    _(
                        "You can't request an approval because some lines have "
                        "quantity but no product selected."
                    )
                )
        # Reuse OCA validation (non-cancelled lines with qty > 0)
        self.to_approve_allowed_check()
        return self.write({"state": "to_be_dept_approved"})

    def button_dept_approve(self):
        """Department approval moves to main approval stage."""
        self.to_approve_allowed_check()
        return self.write({"state": "to_approve"})

    @api.depends("state", "line_ids.product_qty", "line_ids.cancelled", "line_ids.product_id")
    def _compute_to_approve_allowed(self):
        for rec in self:
            is_in_valid_state = rec.state in ("draft", "to_be_dept_approved")
            has_valid_lines = any(
                not line.cancelled and line.product_id and (line.product_qty or 0.0) > 0
                for line in rec.line_ids
            )
            rec.to_approve_allowed = is_in_valid_state and has_valid_lines

    @api.depends("state")
    def _compute_is_editable(self):
        """Make PR read-only during department approval."""
        super()._compute_is_editable()
        for rec in self:
            if rec.state == "to_be_dept_approved":
                rec.is_editable = False

    def write(self, vals):
        """Block writes for PR User and Dept Manager in terminal/approval states.

        Applies to users in either Purchase Request User or Department Purchase
        Manager groups, unless they are Purchase Request Manager. Disallows
        modifications when the request is in any of these states:
        to_approve, approved, in_progress, done, rejected.
        """
        user = self.env.user
        is_pr_user = user.has_group("purchase_request.group_purchase_request_user")
        is_dept_mgr = user.has_group(
            "purchase_request_department_approval.group_purchase_request_department_manager"
        )
        is_pr_mgr = user.has_group("purchase_request.group_purchase_request_manager")
        if (is_pr_user or is_dept_mgr) and not is_pr_mgr:
            blocked = {"to_approve", "approved", "in_progress", "done", "rejected"}
            if any(rec.state in blocked for rec in self):
                raise UserError(
                    _("You cannot modify this Purchase Request in its current state.")
                )
        return super().write(vals)
