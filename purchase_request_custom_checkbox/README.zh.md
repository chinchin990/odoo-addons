# 采购申请 - 自定义列复选框

[中文] | [English](README.md)

为采购申请相关列表统一设置 `optional="show"`，便于用户自行隐藏/显示列并调整顺序——包括 PR 表单内嵌明细与顶层菜单“采购申请明细（Purchase Request Lines）”。

## 功能
- PR 表单内嵌明细树：为常用列添加 `optional="show"`。
- 采购申请明细列表：同样为重要字段添加可选显示。
- 兼容扩展字段（unit_price、x_supplier、line_state），通过继承视图精确覆盖。

## 安装
- Odoo 17；依赖 `purchase_request` 及相关扩展以获得完整覆盖。

## 说明
- 不修改业务逻辑和标签，仅启用列的用户控制。
