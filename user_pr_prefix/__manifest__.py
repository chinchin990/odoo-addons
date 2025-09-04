# -*- coding: utf-8 -*-
{
    'name': 'User PR Prefix & Auto Number',
    'version': '17.0.1.0.0',
    'depends': ['base', 'purchase_request'],  # Depends on the purchase_request module
    'author': 'Your Name',
    'category': 'Customization',
    'summary': 'Add PR Prefix to Users and auto-generate PR number with user prefix',
    'description': '''
        User PR Prefix & Auto Number System
        ==================================
        
        This module extends the Purchase Request system with:
        * User-specific PR prefixes (configurable per user)
        * Automatic PR number generation with format: [PREFIX][YEAR]-[SEQUENCE]
        * Year-based sequence numbering (resets each year)
        * Per-user prefix management
        
        Features:
        * Configurable PR prefix per user (default: K1-WH-PR-)
        * Automatic number generation: K1-WH-PR-2025-0001
        * Year-based sequence management
        * User-specific numbering (different users, different sequences)
        
        Usage:
        1. Go to Settings → Users & Companies → Users
        2. Set PR Prefix for each user
        3. When creating Purchase Requests, numbers are auto-generated
    ''',
    'data': [
        'views/res_users_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}