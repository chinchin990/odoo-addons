# Purchase Request Create PO API

[English] | [中文说明](README.zh.md)

Integrates remote Purchase Order creation into the standard Purchase Request “Create RFQ” workflow using per-user API credentials.

## Features
- Seamless with the native “Create RFQ” wizard
- Per-user remote API settings (URL, DB, Username, Password/API Key)
- Create a new remote PO or update an existing one
- Product and vendor matching helpers
- Real-time feedback and robust error handling

## How It Works
1. User clicks “Create RFQ” on a Purchase Request
2. Wizard shows an option to create on a remote server and an optional “update existing PO” input
3. System uses current user’s saved API credentials to create/update a remote PO via XML-RPC
4. Local PR lines are marked accordingly

## Configuration
Settings → Users & Companies → Users → Remote API Settings:
- Remote API URL (e.g., https://your-odoo.example.com)
- Remote API Database
- Remote API Username
- Remote API Password/API Key

## Installation
- Dependencies: `base`, `purchase_request`
- Install via Apps; then configure user credentials

## Security
- User-specific, encrypted credential fields
- Errors do not expose secrets; all calls are logged for audit

