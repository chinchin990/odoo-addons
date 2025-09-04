# -*- coding: utf-8 -*-
{
    'name': 'Purchase Request Create PO API',
    'version': '17.0.1.0.0',
    'depends': ['base', 'purchase_request'],
    'author': 'Your Name',
    'category': 'Purchases',
    'summary': 'Create Purchase Orders remotely via API integrated with standard Create RFQ workflow',
    'description': '''
        Purchase Request Create PO API
        =============================
        
        This module seamlessly integrates remote PO creation into the standard 
        Purchase Request "Create RFQ" workflow using user-specific API credentials.
        
        Features:
        * Seamless integration with existing "Create RFQ" button workflow
        * User-specific API configuration (URL, Database, Username, Password)
        * Option to create new remote PO or update existing one
        * Automatic product and supplier mapping between systems
        * Real-time feedback and error handling
        * No UI disruption - works within existing Purchase Request interface
        
        How it works:
        1. User clicks standard "Create RFQ" button in Purchase Request
        2. Standard wizard appears with new "Create on Remote Server?" option
        3. When checked, additional field appears for optional existing PO update
        4. System uses current user's API credentials to create/update remote PO
        5. Local purchase request lines are marked as completed
        
        Configuration:
        1. Go to Settings → Users & Companies → Users
        2. In user preferences, configure Remote API Settings:
           - Remote API URL (e.g., https://your-odoo-instance.com)
           - Remote API Database name
           - Remote API Username
           - Remote API Password/API Key
        3. Use standard Purchase Request workflow - new options appear automatically
        
        Technical Details:
        * Inherits purchase.request.line.make.purchase.order wizard model
        * Extends res.users model with API configuration fields
        * XML-RPC integration with comprehensive error handling
        * Product matching via default_code or name
        * Supplier matching via name and supplier_rank
        * Compatible with OCA purchase_request module
        
        Security:
        * Password fields are encrypted and not visible in forms
        * API credentials are user-specific and not shared
        * Comprehensive error handling prevents credential exposure
        * All API calls are logged for audit purposes
    ''',
    'data': [
        'views/res_users_views.xml',
        'views/purchase_request_line_make_purchase_order_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}