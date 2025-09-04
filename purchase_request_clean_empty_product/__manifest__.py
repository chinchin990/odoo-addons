# -*- coding: utf-8 -*-
{
    "name": "Purchase Request Clean Empty Product",
    "version": "17.0.1.0.0",  # 更新为Odoo 17版本
    "author": "Your Name",
    "category": "Purchases",
    "summary": "Automatically clean empty product lines in purchase requests",
    "description": """
        Purchase Request Clean Empty Product
        ===================================
        
        This module automatically removes purchase request lines that have no product selected
        when saving purchase requests. This helps maintain data integrity and clean records.
        
        Features:
        * Automatically removes lines with empty product_id during create/write operations
        * Works silently in the background without user intervention
        * Maintains data consistency and prevents empty product lines
        * Compatible with OCA purchase_request module
        
        Technical Details:
        * Overrides create() and write() methods of purchase.request model
        * Filters out line commands with empty product_id before saving
        * Supports all Odoo One2many command formats (0, 1, 2, 3, 4, 5, 6)
        * Preserves other valid operations while removing empty product lines
    """,
    "depends": ["purchase_request"],  # Depends on the OCA module
    "data": [],
    "demo": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}