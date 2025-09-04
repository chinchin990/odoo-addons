# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    def _clean_empty_product_lines(self, vals):
        """
        Removes lines where product_id is empty.
        Supports all Odoo One2many command formats:
        - (0, 0, vals): Create new record
        - (1, id, vals): Update existing record
        - (2, id, 0): Delete record
        - (3, id, 0): Unlink record (do not delete)
        - (4, id, 0): Link an existing record
        - (5, 0, 0): Unlink all records
        - (6, 0, [ids]): Replace the list of linked records
        """
        if "line_ids" not in vals:
            return vals
            
        cleaned_lines = []
        removed_count = 0
        
        for command in vals["line_ids"]:
            if not isinstance(command, (list, tuple)) or len(command) < 1:
                # Keep incorrectly formatted commands (let Odoo handle them)
                cleaned_lines.append(command)
                continue
                
            operation = command[0]
            
            if operation == 0:  # Create new record (0, 0, vals)
                if len(command) >= 3 and isinstance(command[2], dict):
                    vals_dict = command[2]
                    # If product_id is missing or False/empty, skip this command
                    if not vals_dict.get("product_id"):
                        removed_count += 1
                        _logger.debug("Removed empty product line during create: %s", vals_dict)
                        continue
                cleaned_lines.append(command)
                
            elif operation == 1:  # Update existing record (1, id, vals)
                if len(command) >= 3 and isinstance(command[2], dict):
                    vals_dict = command[2]
                    # If the update operation explicitly sets product_id to False/empty, skip it
                    if "product_id" in vals_dict and not vals_dict["product_id"]:
                        removed_count += 1
                        _logger.debug("Removed empty product line during update: ID %s, vals %s", command[1], vals_dict)
                        continue
                cleaned_lines.append(command)
                
            else:
                # Other operations (2:delete, 3:unlink, 4:link, 5:unlink all, 6:replace list) remain unchanged
                cleaned_lines.append(command)
        
        vals["line_ids"] = cleaned_lines
        
        if removed_count > 0:
            _logger.info("Cleaned %d empty product lines from purchase request", removed_count)
            
        return vals

    @api.model
    def create(self, vals_list):
        """Override the create method to clean empty product lines before creation"""
        if isinstance(vals_list, dict):
            # Single record
            vals_list = self._clean_empty_product_lines(vals_list)
        elif isinstance(vals_list, list):
            # Multiple records
            vals_list = [self._clean_empty_product_lines(vals) for vals in vals_list]
        
        return super(PurchaseRequest, self).create(vals_list)

    def write(self, vals):
        """Override the write method to clean empty product lines before updating"""
        vals = self._clean_empty_product_lines(vals)
        return super(PurchaseRequest, self).write(vals)

    @api.model
    def _validate_line_data(self, line_vals):
        """
        Validates the line data.
        This method can be overridden in child classes to add extra validation logic.
        """
        if not line_vals:
            return False
        
        # Basic validation: product_id is required
        if not line_vals.get("product_id"):
            return False
            
        # Other validation logic can be added
        # Example: check if quantity is greater than 0
        # if line_vals.get("product_qty", 0) <= 0:
        #     return False
        
        return True

    def _get_line_summary(self):
        """Gets a summary of the current purchase request's lines (for logging purposes)"""
        summary = []
        for line in self.line_ids:
            if line.product_id:
                summary.append(f"Product: {line.product_id.name} (Qty: {line.product_qty})")
            else:
                summary.append(f"Empty product line (ID: {line.id})")
        return summary