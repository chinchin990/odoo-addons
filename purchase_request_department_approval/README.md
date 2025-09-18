# Purchase Request - Department Approval

[English] | [中文](README.zh.md)

Adds a department-level review flow on top of OCA Purchase Request, with prefix‑based access control, state gating, button visibility, and line price conveniences.

## Key Features
- Workflow states
  - Adds `to_be_dept_approved` and `to_purchasing_verify` between Draft → Approval → Approved.
  - Enforces order by redefining the `state` selection (keeps original states).
  - `approved_date` timestamp is stored (readonly) when a request becomes Approved.

- Buttons & state gating
  - Draft → Dept Approve: `button_to_approve` moves to `to_be_dept_approved` after validations.
  - Dept Approve: `button_dept_approve` (Department Purchase Manager) moves to `to_purchasing_verify`.
  - Purchasing Verify: `button_purchasing_verify` (PR Manager) validates again and moves to `to_approve`.
  - Header buttons are shown only in the relevant state and for the proper groups.
  - Create RFQ: visible only in `approved`/`in_progress`; restricted to System Admin + PR Manager.

- Validations
  - Forbid lines with qty > 0 and no product when sending to approval.
  - Require at least one valid non‑cancelled line with product and qty > 0 (reuses OCA checks).
  - During `to_be_dept_approved` and `to_purchasing_verify`, the request becomes readonly (`is_editable = False`).

- Access control (prefix‑based)
  - New group: Department Purchase Manager, implied by PR User.
  - Record rules by `requested_by.pr_prefix`:
    - Dept Managers: full access within their prefix; also if requester is self.
    - PR Users: read‑only within their prefix.
    - Follower rules tightened to same prefix for both PR and PR Line.

- Edit locks for non‑managers
  - For PR Users and Dept Managers (not PR Managers), block edits in states: `to_purchasing_verify`, `to_approve`, `approved`, `in_progress`, `done`, `rejected`.
  - Prevent PR number (`name`) changes via server‑side guard.

- Line price & reason enhancements
  - Adds `unit_price` to PR lines; `estimated_cost` becomes a computed "Total Price" = qty × unit_price.
  - Auto‑fill `unit_price` from product cost on product change and at create if missing.
  - Adds `reason` (text) on PR line; exposed in form/tree.
  - In views, `unit_price` is placed before `estimated_cost` for readability; labels adjusted to "Total Price".

## Views Overview
- Form: extended statusbar; added Approved Date; `requested_by` forced readonly.
- Header: state‑aware buttons for Reset/Dept Approve/Purchasing Verify; RFQ button restricted.
- Lines (embedded tree): inserts Unit Price (before Total Price), Reason, relabels Estimated Cost.
- Line form: shows Reason; Unit Price before Total Price; relabel applies.
- PR number readonly for PR Users and Dept Managers.

## Installation
- Odoo 17; depends on:
  - `purchase_request`
  - `purchase_request_user_pr_prefix` (provides `pr_prefix` on users used by record rules)

## Notes & Compatibility
- Designed to work alongside other PR extensions (price visibility, custom checkboxes, supplier column, etc.).
- If you also hide prices for non‑managers globally, ensure view groups/field groups are consistent across modules.

