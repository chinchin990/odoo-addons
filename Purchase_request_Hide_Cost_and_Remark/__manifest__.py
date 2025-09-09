# -*- coding: utf-8 -*-
{
    'name': 'Purchase Request Hide Cost and Remark',
    'version': '17.0.1.0.0',
    # 关键改动：添加了对 purchase_request_department_approval 模块的依赖，确保加载顺序正确
    'depends': [
        'purchase',
        'purchase_request',
        'purchase_request_department_approval',
    ],
    'author': 'Your Name',
    'category': 'Purchases',
    'summary': 'Add remark field and hide cost information for regular users',
    'description': '''
        Purchase Request Cost & Remark Control
        =====================================
        
        This module provides:
        * Add remark field to purchase request lines
        * Hide estimated cost fields from regular users
        * Hide remark field from regular users
        * Only purchase managers can see cost and remark information
    ''',
    'data': [
        'views/purchase_request_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
