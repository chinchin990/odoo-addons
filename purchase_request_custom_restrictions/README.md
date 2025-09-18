# Purchase Request - Custom Restrictions

[English] | [中文](README.zh.md)

Harden PR data entry with readonly rules, hidden fields, and description validation.

## Features
- Readonly: `requested_by`, `date_start` (auto-set on create).
- Editable: `approve_date` remains editable.
- Hidden fields (form/list): `assigned_to`, `company_id`, `origin`.
- Description: relabeled to "Purpose / Category of Purchase" and required when leaving Draft (server-side checks on state change and button).

## Installation
- Odoo 17; depends on `purchase_request`.

## Notes
- Server-side enforcement; UI hides are supplemental.

