{
    "name": "Hide Chatter Send Message",
    "version": "17.0.1.0.0",
    "category": "Customization",
    "summary": "Hide or rename Send Message button in chatter (Odoo 17)",
    "author": "Your Company",
    "depends": ["mail"],
    "data": [
        "views/chatter_button.xml",
    ],
    "assets": {
        "web.assets_qweb": [
            "hide_chatter_send_message/views/chatter_button.xml",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}