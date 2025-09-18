# Purchase Request - Custom Column Checkboxes

[English] | [中文](README.zh.md)

Unify Purchase Request column options with `optional="show"` so users can toggle/hide columns and reorder them — both in the embedded PR form lines and in the top‑level menu “Purchase Request Lines”.

## Features
- Embedded PR lines tree: sets `optional="show"` on common columns.
- Standalone PR lines list: same optional toggles across important fields.
- Compatible with extensions (unit_price, x_supplier, line_state) via targeted inherits.

## Installation
- Odoo 17; depends on `purchase_request` and related PR extensions for full coverage.

## Notes
- Does not change logic or labels; only enables user column toggling.
