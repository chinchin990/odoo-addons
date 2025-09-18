# -*- coding: utf-8 -*-
from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Globally hide product prices for non Purchase Managers.

        For users not in 'purchase.group_purchase_manager', mark
        'standard_price' and 'lst_price' as invisible in field metadata.
        This influences how clients render fields across views.
        """
        res = super(ProductProduct, self).fields_get(allfields=allfields, attributes=attributes)

        # Only Purchase Managers (or higher) can see product prices
        is_purchase_manager = self.env.user.has_group('purchase.group_purchase_manager')
        if not is_purchase_manager:
            for fname in ('standard_price', 'lst_price'):
                if fname in res:
                    # ensure a dict to mutate safely
                    meta = res[fname] or {}
                    meta['invisible'] = True
                    res[fname] = meta

        return res

