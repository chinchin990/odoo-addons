# Purchase Request - Supplier Column

[English] | [中文](README.zh.md)

Add a free-text Supplier column to PR lines (embedded tree), positioned before Total Price, visible to managers only.

## Features
- Field: `x_supplier` (Char), manager-only.
- Position: before `estimated_cost` in the embedded lines tree.

## Installation
- Odoo 17; depends on `purchase_request`.

## Notes
- No impact on procurement logic; purely informational.

