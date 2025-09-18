# 采购申请 - Supplier 列

[中文] | [English](README.md)

在采购申请明细（内嵌树）中新增自由文本列“Supplier”，用于记录计划采购的供应商，默认放置在总价之前，仅经理可见。

## 功能
- 字段：`x_supplier`（字符），仅经理可见。
- 位置：位于 `estimated_cost`（总价）之前。

## 安装
- Odoo 17；依赖 `purchase_request`。

## 说明
- 不影响后续采购逻辑，仅用于信息记录。

