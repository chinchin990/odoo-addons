{
    "name": "PR Chatter - Hide Send Message",
    "summary": "Hide 'Send message' only on Purchase Request chatter; keep 'Log note'.",
    "version": "17.0.1.0.1",
    "category": "Purchases",
    "author": "Your Name",
    "website": "",
    "license": "LGPL-3",
    "depends": ["purchase_request", "mail"],
    "data": [
        "views/purchase_request_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "pr_chatter_hide_send/static/src/css/chatter_styles.css",
        ],
        "mail.assets_messaging": [
            "pr_chatter_hide_send/static/src/css/chatter_styles.css",
        ],
    },
    "installable": True,
    "application": False,
}
