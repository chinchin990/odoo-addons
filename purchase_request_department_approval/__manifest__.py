# -*- coding: utf-8 -*-
{
    "name": "Purchase Request Department Approval",
    "summary": """
        Adds a department-level approval step to the Purchase Request workflow
        based on the user's PR prefix.
    """,
    "version": "17.0.1.0.0",
    "category": "Purchases",
    "author": "Gemini",
    "license": "AGPL-3",
    "depends": [
        "purchase_request",
        "user_pr_prefix",
    ],
    "data": [
        "security/security.xml",
        "views/purchase_request_views.xml",
    ],
    "installable": True,
    "application": False,
}
