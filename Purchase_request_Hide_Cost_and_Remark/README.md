# Purchase Request Hide Cost and Remark

[English] | [中文](README.zh.md)

Hide price information for regular users on Purchase Requests, add a manager‑only remark, and secure product prices globally.

## Features
- Purchase Request visibility
  - Hide Total Price (estimated_cost) for non‑managers in PR form and lines.
  - Hide the PR form footer total and its label for non‑managers.
  - Add internal remark field (`x_remark`) on PR lines (visible to PR Managers).
- Product price security (global)
  - In product forms, restrict Cost (`standard_price`) and Sales Price (`list_price`/`lst_price`) to Purchase Managers.
  - Server‑side hardening: product.product `fields_get` hides `standard_price` and `lst_price` for non‑managers across views.

## Roles & Security
- Price visibility limited to: `purchase.group_purchase_manager` and `base.group_system`.
- Regular users cannot see costs or sales prices in products or PR totals.

## Compatibility
- Odoo 17; OCA `purchase_request` 17.0.

## Installation
- Dependencies: `purchase`, `purchase_request`.
- Install via Apps or CLI; no extra configuration required.

## Notes
- No change to pricing computations; this module focuses on visibility.
- Combine with department approval for multi‑step review workflows.

