# 采购申请隐藏成本与备注

[中文] | [English](README.md)

在采购申请中为普通用户隐藏价格信息，为经理提供仅内部可见的备注字段，并在全系统范围内保护产品价格字段。

## 功能
- 采购申请可见性
  - 对非经理隐藏总价（estimated_cost），包括表单与明细行。
  - 对非经理隐藏表单页脚的总计及其标签。
  - 在明细行新增内部备注字段 `x_remark`（仅采购申请经理可见）。
- 产品价格安全（全局）
  - 在产品表单中，仅采购经理可见成本（`standard_price`）与销售价（`list_price`/`lst_price`）。
  - 服务器侧加强：覆盖 product.product 的 `fields_get`，对非经理隐藏 `standard_price` 与 `lst_price` 的字段元数据，在表单/列表/看板等视图生效。

## 角色与权限
- 价格可见角色：`purchase.group_purchase_manager`、`base.group_system`。
- 普通用户无法在产品与采购申请中看到价格。

## 兼容性
- Odoo 17；OCA `purchase_request` 17.0。

## 安装
- 依赖：`purchase`、`purchase_request`。
- 通过应用界面或命令行安装，无需额外配置。

## 说明
- 不改变任何价格计算逻辑，仅控制可见性。
- 建议配合部门审批流程模块使用，以实现多步骤审核。

