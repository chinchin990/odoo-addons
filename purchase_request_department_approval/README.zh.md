# 采购申请 - 部门审批

[中文] | [English](README.md)

在 OCA 采购申请基础上增加“部门审批”流，并基于用户前缀（pr_prefix）做权限隔离，提供状态门控、按钮可见性以及行价格与理由等易用性增强。

## 主要功能
- 审批流程
  - 新增中间状态：`to_be_dept_approved`（部门审批）、`to_purchasing_verify`（采购核验）。
  - 重排 `state` 选项，保留原有状态；在进入 Approved 时记录 `approved_date`。

- 按钮与状态门控
  - 草稿 → 部门审批：`button_to_approve` 校验通过后进入 `to_be_dept_approved`。
  - 部门审批：`button_dept_approve`（部门采购经理）进入 `to_purchasing_verify`。
  - 采购核验：`button_purchasing_verify`（PR 经理）复核后进入 `to_approve`。
  - 页眉按钮按状态与用户组控制显示。
  - 创建询价单（Create RFQ）：仅在 `approved`/`in_progress` 时可见，且限系统管理员+PR 经理。

- 校验逻辑
  - 禁止含“数量>0 且无产品”的行进入审批。
  - 要求至少存在“未取消、且有产品与数量>0”的有效行（复用 OCA 校验）。
  - 在 `to_be_dept_approved` 与 `to_purchasing_verify` 阶段将单据只读（`is_editable=False`）。

- 前缀（pr_prefix）权限隔离
  - 新增组：Department Purchase Manager（隐含 PR User）。
  - 记录规则基于 `requested_by.pr_prefix`：
    - 部门采购经理：本前缀内（或本人为申请人）可读写删增。
    - PR User：本前缀内仅可读。
    - 关注者（followers）规则：在 PR 与 PR 行上均收紧到相同前缀。

- 非经理编辑限制
  - 对 PR User 与 Dept Manager（非 PR Manager）在以下状态禁止修改：
    `to_purchasing_verify`、`to_approve`、`approved`、`in_progress`、`done`、`rejected`。
  - 服务器端禁止修改 PR 编号（`name`）。

- 明细价格与理由增强
  - 增加 `unit_price` 字段；`estimated_cost` 改为“总价（Total Price）= 数量 × 单价”。
  - 产品变更与创建时自动带入 `standard_price` 作为 `unit_price`（若未填写）。
  - 增加 `reason`（文本）字段；在表单/树视图展示。
  - 视图中将 `unit_price` 放在 `estimated_cost` 之前，并将标签改为“Total Price”。

## 视图概览
- 表单：扩展状态条；增加核准日期；强制 `requested_by` 只读。
- 页眉：按状态/角色显示“重置/部门审批/采购核验”；RFQ 按钮限权且按状态可见。
- 明细（内嵌树）：插入“单价（Unit Price）”“理由（Reason）”，重命名/重排总价列。
- 明细表单：显示 Reason；Unit Price 在 Total Price 之前；标签同步。
- PR 编号：对 PR User 与 Dept Manager 只读。

## 安装
- Odoo 17；依赖：
  - `purchase_request`
  - `purchase_request_user_pr_prefix`（提供用户的 pr_prefix 用于记录规则）

## 说明与兼容
- 可与其它 PR 扩展（价格可见性、列可选、Supplier 列等）配合使用。
- 如全局隐藏非经理价格，请确保各模块的 `groups` 与字段权限一致。

