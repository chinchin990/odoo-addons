# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import UserError

class BaseModel(models.AbstractModel):
    # 我们继承 'base' 模型，这是 Odoo 所有模型的父模型，
    # 这样我们的修改就能全局生效。
    _inherit = 'base'

    @api.model
    def load(self, fields, data):
        """
        覆盖 Odoo 核心的 'load' 方法，这是所有导入功能最终都会调用的方法。
        我们在这里进行权限检查。
        """
        # 检查当前用户是否属于允许导入的组
        is_authorized = self.env.user.has_group('purchase.group_purchase_manager') or \
                        self.env.user.has_group('base.group_system')

        # 如果用户没有权限，则直接抛出错误，中断导入操作
        if not is_authorized:
            raise UserError("You do not have permission to import data. Please contact your administrator.")
        
        # 如果用户有权限，则正常执行原始的导入功能
        return super(BaseModel, self).load(fields, data)