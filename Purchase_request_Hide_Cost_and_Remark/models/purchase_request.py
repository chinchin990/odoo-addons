# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    # Use @api.constrains to declare this as a validation constraint
    # It triggers automatically when the line_ids field changes
    @api.constrains('line_ids')
    def _check_has_lines(self):
        """
        This function is automatically called by Odoo when creating or editing
        a purchase.request record where the line_ids field is part of the transaction.
        """
        # Looping over self is necessary because the constraint might process multiple records at once
        for request in self:
            # If line_ids is empty (i.e., there are no product lines)
            if not request.line_ids:
                # Raise a validation error with a user-friendly message
                raise ValidationError(_(
                    "You must add at least one product to the purchase request.\n"
                ))

    # You no longer need to override the create and write methods!
    # @api.constrains handles both scenarios automatically.