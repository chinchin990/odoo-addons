# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'  # Inherit the purchase.request model

    @api.model
    def create(self, vals):
        """Override create to auto-generate a sequence number when creating a PR."""
        # If the user has not manually entered a name, or if the name is the default 'New'
        if not vals.get('name') or vals.get('name') == 'New':
            user = self.env.user
            prefix = user.pr_prefix or 'PR-'  # Get the user's prefix, or use a default value if not set
            year = fields.Date.today().year

            # Build the search pattern: Prefix + Year + Hyphen
            search_pattern = f"{prefix}{year}-"
            
            # Get the latest sequence number for the current year and user prefix
            last_records = self.search(
                [('name', 'like', search_pattern)],
                order='name desc',
                limit=1
            )

            if last_records:
                try:
                    # Extract the last sequence number
                    last_name = last_records[0].name
                    # Split the string and take the last part as the sequence number
                    parts = last_name.split('-')
                    if len(parts) >= 3:  # Ensure there are enough parts
                        last_sequence = int(parts[-1])
                        next_sequence = last_sequence + 1
                    else:
                        next_sequence = 1
                except (ValueError, IndexError) as e:
                    _logger.warning(f"Failed to parse sequence from {last_name}: {e}")
                    next_sequence = 1
            else:
                next_sequence = 1

            # Format the number: Prefix + Year + Sequence (padded to 4 digits)
            vals['name'] = f"{prefix}{year}-{next_sequence:04d}"
            
            _logger.info(f"Generated PR number: {vals['name']} for user {user.name}")

        return super().create(vals)

    @api.model
    def _get_next_sequence_number(self, prefix, year):
        """
        Gets the next sequence number for a given prefix and year.
        This method can be called externally to preview the next number.
        """
        search_pattern = f"{prefix}{year}-"
        last_records = self.search(
            [('name', 'like', search_pattern)],
            order='name desc',
            limit=1
        )
        
        if last_records:
            try:
                last_name = last_records[0].name
                parts = last_name.split('-')
                if len(parts) >= 3:
                    return int(parts[-1]) + 1
            except (ValueError, IndexError):
                pass
        
        return 1

    def preview_next_pr_number(self):
        """
        Previews the next PR number (can be used for display in the UI).
        """
        user = self.env.user
        prefix = user.pr_prefix or 'PR-'
        year = fields.Date.today().year
        next_seq = self._get_next_sequence_number(prefix, year)
        return f"{prefix}{year}-{next_seq:04d}"