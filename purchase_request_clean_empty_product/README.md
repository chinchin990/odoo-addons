# Purchase Request - Clean Empty Product Lines

[English] | [中文](README.zh.md)

Prevent or clean empty product lines in Purchase Requests to keep data consistent and avoid downstream errors.

## Features
- Blocks/cleans PR lines with missing `product_id` or zero/invalid quantity (implementation‑specific).
- Safer create/edit flows for PR lines.
- Optional tweaks to display names to avoid errors when product is absent.

## Installation
- Odoo 17; depends on `purchase_request`.

## Notes
- Works alongside other PR modules; no price or approval logic is changed.

