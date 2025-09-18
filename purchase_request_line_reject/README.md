# Purchase Request Line Reject

[English] | [中文](README.zh.md)

Add a reject/restore workflow to Purchase Request lines with clear status and audit logging.

## Features
- Line status (`line_state`): `normal` / `rejected`.
- Buttons in PR form embedded tree and standalone list:
  - Reject (fa-ban): sets line to rejected; logs to the parent request.
  - Restore (fa-refresh): returns line to normal; logs to the parent request.
- Visibility: buttons restricted to Purchase Request Managers and System Admins.

## Installation
- Odoo 17; depends on `purchase_request`.

## Notes
- No change to price or procurement logic; only UI actions + logging.

