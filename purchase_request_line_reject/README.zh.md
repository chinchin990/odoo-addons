# 采购申请明细拒绝（Reject）

[中文] | [English](README.md)

为采购申请行增加拒绝/恢复操作，并记录日志，提升流程清晰度。

## 功能
- 行状态（`line_state`）：`normal` / `rejected`。
- 按钮（PR 表单内嵌树与独立列表）
  - 拒绝（fa-ban）：设为 rejected，并在主单记录日志。
  - 恢复（fa-refresh）：恢复为 normal，并在主单记录日志。
- 可见性：仅采购申请经理与系统管理员可见。

## 安装
- Odoo 17；依赖 `purchase_request`。

## 说明
- 不涉及价格或采购逻辑，仅 UI 行为与日志。

