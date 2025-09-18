# Odoo 17 采购申请扩展集

本仓库包含一组围绕采购申请（PR）的 Odoo 17 扩展模块，覆盖流程、可见性与安全。

## 模块一览
- `pr_chatter_hide_send`：在 PR 的 Chatter 中隐藏“发送消息”，仅保留“记录备注”。
- `purchase_request_department_approval`：增加部门审批阶段，优化页眉按钮可见性；将 `unit_price` 放在 `estimated_cost` 前。
- `Purchase_request_Hide_Cost_and_Remark`：对非经理隐藏 PR 成本；增加经理备注；在全系统保护产品价格（销售价/成本）。
- `purchase_request_line_reject`：为 PR 行提供拒绝/恢复按钮，带状态徽章与日志。
- `purchase_request_supplier_column`：在总价前新增自由文本“Supplier”列（仅经理可见）。
- `purchase_request_custom_checkbox`：为 PR 相关列设置 `optional="show"`，允许用户自行隐藏/排序。
- `purchase_request_custom_restrictions`：只读规则、隐藏字段与提交前描述必填校验。
- `purchase_request_line_tree_custom_checkbox`（已替代）：被 `purchase_request_custom_checkbox` 统一替代。
- `purchase_request_clean_empty_product`：防止/清理空白产品行，保证数据一致。
- `Purchase_request_create_PO_API`：从 PR 明细创建询价单/采购单的 API/向导。
- `purchase_request_user_pr_prefix`：按用户/公司为 PR 编号添加前缀。

## 兼容性
- Odoo 17.0（社区版），OCA `purchase_request` 17.0。

## 安装
- 将模块置于 addons 路径下，更新应用列表后按需安装。
- 某些模块依赖 `purchase_request`、`purchase` 及其它自定义 PR 模块。

## 安全说明
- 价格可见性：主要限制在 `purchase.group_purchase_manager` 与 `base.group_system`。
- 全局产品价格安全：由 `Purchase_request_Hide_Cost_and_Remark` 中对 `fields_get` 的覆盖实现（隐藏 `standard_price`/`lst_price`）。
