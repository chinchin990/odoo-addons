# -*- coding: utf-8 -*-
{
    'name': "Web Disable Import Function",
    'version': '17.0.2.0.0', # 更新版本号
    'summary': "Disables the import functionality for non-authorized users.",
    'description': """
        This module provides a server-side restriction to prevent data import.
        
        The 'load' method is overridden globally. Only users belonging to:
        - System / Administrator
        - Purchase / Manager
        are allowed to import records. Other users will receive an access error.
    """,
    'author': "Your Name / Company",
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    
    # Python 代码的依赖关系
    'depends': ['base', 'purchase'],
    
    # 我们已经删除了 XML 文件，所以 'data' 列表应该为空
    'data': [],
    
    'installable': True,
    'application': True,
    'auto_install': False,
}