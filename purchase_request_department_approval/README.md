# Purchase Request Department Approval

Department-level approval workflow for Odoo 17 Purchase Requests, based on each user's PR Prefix.

## Overview
This module adds an intermediate department approval step to OCA's Purchase Request. It introduces a new state, a new security group, and a record rule that isolates visibility by department using the PR Prefix field provided by the companion module `purchase_request_user_pr_prefix`.

## Key Features
- New state: `To be Dept. Approved` inserted between `Draft` and `To be Approved`.
- New group: "Department Purchase Manager" for users who can perform department approval.
- New button: "Department Approve" visible only to the above group when the request is in `To be Dept. Approved`.
- Record rule: Department managers only see requests where the requester's PR Prefix equals their own, ensuring department data isolation.

## Workflow
1. Draft → To be Dept. Approved → To be Approved → Approved.
2. Regular users submit requests; they first require department approval.
3. A Department Purchase Manager with the same PR Prefix approves at the department step.
4. The standard Purchase Request approval follows afterwards.

## Installation
Dependencies: `purchase_request`, `purchase_request_user_pr_prefix`.

- Install from Apps: enable Developer Mode → Update Apps List → search "Purchase Request Department Approval".
- Or via command line: `-i purchase_request,purchase_request_user_pr_prefix,purchase_request_department_approval`.

## Configuration
1. Set PR Prefix per user: Settings > Users & Companies > Users → select a user → set "PR Prefix" (e.g., `SALE`, `TECH`).
2. Assign department managers: Settings > Users & Companies > Groups → open "Department Purchase Manager" → add the appropriate users.

## Usage Example
1. A user with PR Prefix `SALE` creates and submits a purchase request; the state becomes "To be Dept. Approved".
2. A manager in "Department Purchase Manager" who also has PR Prefix `SALE` opens the request and clicks "Department Approve"; the state moves to "To be Approved".
3. The usual purchase manager approval proceeds next, ultimately leading to "Approved".

## Security and Access
- Group: "Department Purchase Manager" grants access to the department approval action.
- Record Rule: limits visibility to requests where `requested_by.pr_prefix == user.pr_prefix`.

## Notes
- If your organization does not use PR Prefix for department partitioning, you can adapt the record rule and visibility logic to match your own department field.
- Tested with Odoo 17 and OCA `purchase_request` 17.0.

## License
AGPL-3

