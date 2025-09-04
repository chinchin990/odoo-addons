# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    state = fields.Selection(
        selection_add=[
            ("to_be_dept_approved", "To be Dept. Approved"),
        ],
        ondelete={"to_be_dept_approved": "cascade"},
    )

    def button_to_approve(self):
        """
        Override the original button to move the request to
        the 'To be Dept. Approved' state first.
        """
        for rec in self:
            rec.write({"state": "to_be_dept_approved"})
        return True

    def button_dept_approve(self):
        """
        Action for the 'Department Approve' button.
        Moves the request to the 'To be Approved' state for the main
        purchase manager.
        """
        self.to_approve_allowed_check()
        return self.write({"state": "to_approve"})

    @api.depends("state", "line_ids.product_qty", "line_ids.cancelled")
    def _compute_to_approve_allowed(self):
        for rec in self:
            _logger.info(
                f"Checking approval for PR {rec.name} in state {rec.state}"
            )
            line_details = []
            if not rec.line_ids:
                _logger.info("PR has no lines (rec.line_ids is empty).")
            else:
                for line in rec.line_ids:
                    line_details.append(
                        f"[Line ID: {line.id}, Qty: {line.product_qty}, Cancelled: {line.cancelled}]"
                    )
                _logger.info("Line details: %s", '\n'.join(line_details))

            is_in_valid_state = rec.state in ("draft", "to_be_dept_approved")
            has_valid_lines = any(
                not line.cancelled and line.product_qty for line in rec.line_ids
            )
            rec.to_approve_allowed = is_in_valid_state and has_valid_lines
            _logger.info(
                f"Final check for PR {rec.name}: valid_state={is_in_valid_state}, valid_lines={has_valid_lines}, result={rec.to_approve_allowed}"
            )

