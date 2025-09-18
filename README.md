# Odoo 17 Purchase Request Extensions

This repository contains a set of Odoo 17 modules that enhance Purchase Request (PR) workflows and data security.

## Modules
- `pr_chatter_hide_send`: Hide "Send message" in PR chatter; keep "Log note" only.
- `purchase_request_department_approval`: Add department approval stages and refine header button visibility; place `unit_price` before `estimated_cost`.
- `Purchase_request_Hide_Cost_and_Remark`: Hide PR costs from non‑managers; add manager remark; secure product prices (Sales/Cost) for non‑managers.
- `purchase_request_line_reject`: Add Reject/Restore actions for PR lines, with status badges and logging.
- `purchase_request_supplier_column`: Add a free‑text Supplier column before Total Price (manager‑only).
- `purchase_request_custom_checkbox`: Apply `optional="show"` to PR columns so users can toggle/hide/reorder.
- `purchase_request_custom_restrictions`: Enforce readonly rules, hide selected fields, and require description on submit.
- `purchase_request_line_tree_custom_checkbox` (deprecated): superseded by `purchase_request_custom_checkbox`.
- `purchase_request_clean_empty_product`: Prevent/clean empty product lines to keep data consistent.
- `Purchase_request_create_PO_API`: API/Wizard to create RFQs/POs from PR lines.
- `purchase_request_user_pr_prefix`: Add user/company-specific PR number prefix.

## Compatibility
- Odoo 17.0 (community) and OCA `purchase_request` 17.0.

## Installation
- Place modules under your addons path; update Apps list and install as needed.
- Some modules depend on `purchase_request`, `purchase`, and other custom PR modules listed above.

## Security Overview
- Price visibility restricted to `purchase.group_purchase_manager` and `base.group_system` where applicable.
- Global product price security via `fields_get` override in `Purchase_request_Hide_Cost_and_Remark`.
