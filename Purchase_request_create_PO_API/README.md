# Purchase Request - Create PO API / Wizard

[English] | [中文](README.zh.md)

Create Purchase Orders from Purchase Request lines via an API/wizard, streamlining the handoff to purchasing.

## Features
- Action or endpoint to create RFQs/POs from selected PR lines.
- Respects product, quantity, company/vendor context.
- Integrates with standard PR → PO flow.

## Installation
- Odoo 17; depends on `purchase_request` and `purchase`.

## Notes
- Does not alter approval rules; triggers creation only when allowed by your process.

