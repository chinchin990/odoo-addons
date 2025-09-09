# Purchase Request Hide Cost and Remark

[English] | [中文说明](README.zh.md)

Hide price-related information from regular users on Purchase Request views and provide an optional internal remark field for managers.

## Features
- Hide cost fields for non-managers:
  - Hide the Total Price (formerly “Estimated Cost”) column on Purchase Request Lines
  - Hide the total amount and its label in the PR form footer
  - Hide the “Show Details” button on lines
- Remark field:
  - Adds internal remark field (`x_remark`) to purchase request lines
  - Visible/editable for Purchase Request Manager; hidden for regular users
- Group-based visibility:
  - Uses view attributes with groups to control what each role sees

## Compatibility
- Odoo 17, OCA `purchase_request` 17.0
- Compatible with label change “Estimated Cost” → “Total Price”

## Installation
- Dependencies: `purchase_request`
- Install via Apps or CLI; no extra configuration required

## Notes
- This module changes visibility only; it does not alter price computations
- Combine with department approval if multi-step reviews are needed

