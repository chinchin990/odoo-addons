"""Department approval extensions for Purchase Request."""

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    # Redefine selection to enforce order including new states
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("to_be_dept_approved", "To be Dept. Approved"),
            ("to_purchasing_verify", "To be Purchasing Verify"),
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

    approved_date = fields.Datetime(
        string="Approved Date",
        readonly=True,
        copy=False,
        help="Last date/time when the request was approved.",
        tracking=True,
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
        """Department approval moves to Purchasing Verify stage.

        No line validation at this step; purchasing verification will validate
        before sending to main approval.
        """
        return self.write({"state": "to_purchasing_verify"})

    def button_purchasing_verify(self):
        """Purchasing verification completed, move to main approval stage.

        Validate that there is at least one valid line before moving on.
        """
        self.to_approve_allowed_check()
        return self.write({"state": "to_approve"})

    @api.depends("state", "line_ids.product_qty", "line_ids.cancelled", "line_ids.product_id")
    def _compute_to_approve_allowed(self):
        for rec in self:
            # Allow validation check in Draft, Dept Approved, and Purchasing Verify
            is_in_valid_state = rec.state in ("draft", "to_be_dept_approved", "to_purchasing_verify")
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
            if rec.state in ("to_be_dept_approved", "to_purchasing_verify"):
                rec.is_editable = False

    def write(self, vals):
        """Block writes for PR User and Dept Manager in terminal/approval states.

        Applies to users in either Purchase Request User or Department Purchase
        Manager groups, unless they are Purchase Request Manager. Disallows
        modifications when the request is in any of these states:
        to_purchasing_verify, to_approve, approved, in_progress, done, rejected.
        """
        user = self.env.user
        is_pr_user = user.has_group("purchase_request.group_purchase_request_user")
        is_dept_mgr = user.has_group(
            "purchase_request_department_approval.group_purchase_request_department_manager"
        )
        is_pr_mgr = user.has_group("purchase_request.group_purchase_request_manager")
        if (is_pr_user or is_dept_mgr) and not is_pr_mgr:
            # Disallow PR Number change via server-side guard
            if "name" in vals:
                raise UserError(_("You are not allowed to modify PR Number."))
            blocked = {
                "to_purchasing_verify",
                "to_approve",
                "approved",
                "in_progress",
                "done",
                "rejected",
            }
            if any(rec.state in blocked for rec in self):
                raise UserError(
                    _("You cannot modify this Purchase Request in its current state.")
                )
        res = super().write(vals)
        # Update the Approved Date whenever state is set to approved
        if vals.get("state") == "approved":
            now = fields.Datetime.now()
            for rec in self:
                if rec.state == "approved":
                    rec.approved_date = now
        return res


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    unit_price = fields.Monetary(
        string="Unit Price",
        currency_field="currency_id",
        default=0.0,
        tracking=True,
        help="Unit price used to compute Total Price.",
    )

    # Override: make Total Price computed from quantity and unit price
    estimated_cost = fields.Monetary(
        string="Total Price",
        currency_field="currency_id",
        compute="_compute_estimated_cost_total",
        store=True,
        help="Total Price = Quantity * Unit Price.",
        readonly=True,
    )

    reason = fields.Text(string="Reason", help="Purpose of purchasing this product.")

    @api.depends("product_qty", "unit_price")
    def _compute_estimated_cost_total(self):
        for line in self:
            qty = line.product_qty or 0.0
            price = line.unit_price or 0.0
            line.estimated_cost = qty * price

    def write(self, vals):
        # Capture changes to qty or unit price for audit log
        track_qty = "product_qty" in vals
        track_price = "unit_price" in vals
        before = {}
        if track_qty or track_price:
            for rec in self:
                before[rec.id] = {
                    "qty": rec.product_qty,
                    "price": rec.unit_price,
                }

        res = super().write(vals)

        if track_qty or track_price:
            user_name = self.env.user.name
            for rec in self:
                prev = before.get(rec.id, {})
                changes = []
                if track_qty and prev.get("qty") != rec.product_qty:
                    changes.append(
                        _("Qty: %(old)s -> %(new)s",
                          old=prev.get("qty"), new=rec.product_qty)
                    )
                if track_price and prev.get("price") != rec.unit_price:
                    changes.append(
                        _("Unit Price: %(old)s -> %(new)s",
                          old=prev.get("price"), new=rec.unit_price)
                    )
                if changes:
                    body = _(
                        "%(user)s updated line %(line)s: %(changes)s",
                        user=user_name,
                        line=(rec.display_name or rec.name or (rec.product_id and rec.product_id.display_name) or rec.id),
                        changes="; ".join(changes),
                    )
                    if rec.request_id:
                        rec.request_id.message_post(body=body, subtype_xmlid="mail.mt_note")
                    else:
                        rec.message_post(body=body, subtype_xmlid="mail.mt_note")
        return res
