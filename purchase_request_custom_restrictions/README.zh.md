# 采购申请 - 自定义限制

[中文] | [English](README.md)

通过只读规则、隐藏字段和必填校验，强化采购申请的数据质量与合规性。

## 功能
- 只读：`requested_by`、`date_start`（创建时自动设置）。
- 可编辑：`approve_date` 保持可编辑。
- 隐藏字段（表单/列表）：`assigned_to`、`company_id`、`origin`。
- 描述：重命名为“Purpose / Category of Purchase”，从草稿提交审核时为必填（服务端校验覆盖状态变更与按钮）。

## 安装
- Odoo 17；依赖 `purchase_request`。

## 说明
- 服务端强制为主；前端隐藏为辅。

