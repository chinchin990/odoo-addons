# PR Chatter: Hide Send Message

[English] | [中文](README.zh.md)

Hide the "Send message" tab/button in the Purchase Request chatter, keeping only "Log note" to reduce mis-sent emails.

## Features
- Scope limited to purchase.request forms.
- CSS-only solution; no JS/Python overrides.
- Injected into both `web.assets_backend` and `mail.assets_messaging` to ensure precedence in Odoo 17.

## Installation
- Odoo 17.
- Install the module and hard refresh the browser (or use `?debug=assets`).

## Notes
- Non-destructive: uninstall to restore original behavior.

