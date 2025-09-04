# -*- coding: utf-8 -*-
{
    'name': 'Purchase Request Hide Cost and Remark',
    'version': '17.0.1.0.0',
    'depends': ['purchase_request'],
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
        
        Features:
        * Remark field positioned after RFQ/PO qty (manager only)
        * Hidden estimated cost columns (manager only)
        * Hidden total amount (manager only)
        * Hidden show details button (manager only)
        * Role-based field visibility
        * Mail tracking disabled to prevent errors with empty product lines
        
        Access Control:
        * Regular users: Can only see basic product and quantity information
        * Purchase managers: Can see all fields including cost and remark
        
        Technical Implementation:
        * Model inheritance with proper empty product_id handling
        * XML view inheritance with xpath expressions
        * Security group-based field visibility control
        * Action context configuration
    ''',
    'data': [
        'views/purchase_request_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}