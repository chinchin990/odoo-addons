# Purchase Request Department Approval

[English] | [中文说明](README.zh.md)

Department-level approval workflow and line pricing extensions for Odoo 17 Purchase Requests.

## Overview
This module adds an intermediate department approval step and extends Purchase Request Lines with Unit Price, computed Total Price, and a Reason field. It also introduces a purchasing verification state and stricter editing rules.

## Key Features
- New states and flow:
  - `To be Dept. Approved` (department approval step)
  - `To be Purchasing Verify` (purchasing verification step)
  - Flow: Draft → To be Dept. Approved → To be Purchasing Verify → To be Approved → Approved → In progress → Done/Rejected
- New button actions:
  - Department Approve: moves to `To be Purchasing Verify` (no line validation; visible to Department Purchase Manager on dept step)
  - Purchasing Verify: validates lines and moves to `To be Approved` (visible to Purchase Request Manager on verify step)
- Line pricing fields:
  - Unit Price (new): editable monetary field on `purchase.request.line`
  - Total Price: renamed from Estimated Cost and now computed = Quantity × Unit Price; read-only, stored
  - Reason (new): free-text purpose for the line
- Edit restrictions:
  - PR User and Department Purchase Manager cannot edit records in `To be Purchasing Verify`
  - PR Number (name) cannot be modified by PR User and Department Purchase Manager (enforced by view and server-side)
- Chatter logging:
  - When Quantity or Unit Price changes on lines, a note is posted indicating the user and the before → after values
- Visibility by department:
  - Existing group and record rules keep visibility restricted by PR Prefix

## UI Changes
- PR form (lines tree):
  - Shows Unit Price next to Quantity
  - Estimated Cost column label changed to “Total Price”
  - Optional Reason column (can be toggled via list view columns)
  - Footer subtotal label changed to “Total Price”
- PR Line form:
  - Adds Unit Price and Reason; Total Price label shown and read-only
- Status bar on PR:
  - Displays the new `To be Purchasing Verify` step

## Security and Access
- Groups:
  - Department Purchase Manager: department approval
  - Purchase Request Manager: purchasing verification and subsequent approvals
- Restrictions:
  - PR User and Department Purchase Manager cannot modify PR Number
  - Server-side write guard blocks edits for those groups in `to_purchasing_verify`, `to_approve`, `approved`, `in_progress`, `done`, `rejected`

## Installation
Dependencies: `purchase_request`, `purchase_request_user_pr_prefix`.

Install from Apps (Developer Mode) or via command: `-i purchase_request,purchase_request_user_pr_prefix,purchase_request_department_approval`.

## Configuration
1. Set each user’s PR Prefix: Settings → Users & Companies → Users → PR Prefix
2. Assign department managers to group: “Department Purchase Manager”

## Notes
- If using the companion customization to hide costs, the Total Price label change is respected; visibility still depends on that module’s group rules.
- Tested with Odoo 17 and OCA `purchase_request` 17.0.

## License
AGPL-3
