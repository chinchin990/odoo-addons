# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    # ========================== 关键修改开始 ==========================
    # 我们不再使用 selection_add，而是完整地重写整个 state 字段的定义，
    # 并把我们的新状态插入到正确的位置。
    # 这是为了解决 Odoo 在这个特殊情况下可能存在的、
    # 错误地依赖 Selection 顺序来渲染状态栏的 bug。

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('to_be_dept_approved', 'To be Dept. Approved'),  # <-- 你的新状态被强制放在了第二位
            ('to_approve', 'To be approved'),
            ('approved', 'Approved'),
            ('in_progress', 'In progress'),
            ('done', 'Done'),
            ('rejected', 'Rejected'),  # <-- 确保所有原始状态都被包含
        ],
        string='Status',
        index=True,
        tracking=True,
        required=True,
        copy=False,
        default='draft',
    )
    # ========================== 关键修改结束 ==========================

    def button_to_approve(self):
        """
        Override the original button to move the request to
        the 'To be Dept. Approved' state first.
        """
        # 这部分逻辑保持不变
        for rec in self:
            rec.write({"state": "to_be_dept_approved"})
        return True

    def button_dept_approve(self):
        """
        Action for the 'Department Approve' button.
        Moves the request to the 'To be Approved' state for the main
        purchase manager.
        """
        # 这部分逻辑保持不变
        self.to_approve_allowed_check()
        return self.write({"state": "to_approve"})

    @api.depends("state", "line_ids.product_qty", "line_ids.cancelled")
    def _compute_to_approve_allowed(self):
        # 这部分逻辑保持不变
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

            # 这里的逻辑也保持不变，因为它是正确的
            is_in_valid_state = rec.state in ("draft", "to_be_dept_approved")
            has_valid_lines = any(
                not line.cancelled and line.product_qty for line in rec.line_ids
            )
            rec.to_approve_allowed = is_in_valid_state and has_valid_lines
            _logger.info(
                f"Final check for PR {rec.name}: valid_state={is_in_valid_state}, valid_lines={has_valid_lines}, result={rec.to_approve_allowed}"
            )