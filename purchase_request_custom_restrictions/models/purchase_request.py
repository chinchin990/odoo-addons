# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    # 🔹 把 date_start 改成 Datetime
    date_start = fields.Datetime(
        string="Requisition Date",
        required=True,
        default=fields.Datetime.now,
        tracking=True,
    )

    @api.model
    def create(self, vals):
        # 如果没有传 date_start，就自动带当前时间
        if not vals.get("date_start"):
            vals["date_start"] = fields.Datetime.now()
        return super().create(vals)

    def write(self, vals):
        # Enforce readonly for requested_by and date_start
        blocked = []
        if "requested_by" in vals:
            blocked.append("requested_by")
        if "date_start" in vals:
            blocked.append("date_start")
        if blocked:
            raise UserError(
                _("You cannot modify the following fields: %s") % ", ".join(blocked)
            )

        # Validation: description 必须 >= 10 个字
        if "state" in vals:
            target = vals.get("state")
            for rec in self:
                if rec.state == "draft" and target in {"to_be_dept_approved", "to_approve"}:
                    desc = vals.get("description") if "description" in vals else rec.description
                    if not desc or len(desc.strip()) < 10:
                        raise UserError(
                            _("Purpose / Category of Purchase must be at least 10 characters long.")
                        )
        return super().write(vals)

    def button_to_approve(self):
        # description 必须 >= 10 个字
        for rec in self:
            if not rec.description or len(rec.description.strip()) < 10:
                raise UserError(
                    _("Purpose / Category of Purchase must be at least 10 characters long.")
                )
        return super().button_to_approve()
