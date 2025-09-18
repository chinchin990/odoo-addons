# -*- coding: utf-8 -*-
{
    "name": "Purchase Request - Custom Column Checkboxes",
    "version": "17.0.1.0.0",
    "summary": "Unify PR columns with optional=show for user toggling",
    "license": "LGPL-3",
    "author": "YourCompany",
    "depends": [
        "purchase_request",
        "purchase_request_department_approval",
        "Purchase_request_Hide_Cost_and_Remark",
        "purchase_request_line_reject",
        "purchase_request_supplier_column",
    ],
    "data": [
        "views/purchase_request_embedded_tree_optional.xml",
        "views/purchase_request_line_tree_optional.xml",
        "views/pr_form_embedded_unit_price_optional.xml",
        "views/pr_form_embedded_supplier_optional.xml",
        "views/pr_form_embedded_line_state_optional.xml",
        "views/pr_line_tree_unit_price_optional.xml",
    ],
    "installable": True,
}
