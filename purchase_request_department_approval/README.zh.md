# 采购申请部门审批

[英文版](README.md) | 中文说明

## 概述
本模块在标准采购申请流程中新增“部门审批”和“采购核验”两个关键环节，并扩展行项目价格字段：新增单价（Unit Price），将总价（Total Price）改为按“数量 × 单价”自动计算。同时新增“Reason（采购目的）”字段，并在特定状态下限制编辑权限与 PR 编号修改权限。

## 主要功能
- 流程与状态：
  - 新增状态：`To be Dept. Approved（待部门审批）`、`To be Purchasing Verify（待采购核验）`
  - 流程：Draft → To be Dept. Approved → To be Purchasing Verify → To be Approved → Approved → In progress → Done/Rejected
- 按钮：
  - Department Approve：在“待部门审批”由部门采购经理点击，流转至“待采购核验”
  - Purchasing Verify：在“待采购核验”由采购申请管理员点击，流转至“待审批”
- 行价格：
  - 新增 `Unit Price` 单价（可编辑）
  - `Total Price`（原 Estimated Cost）：只读、存储字段，自动计算 = 数量 × 单价
  - 新增 `Reason`（采购目的）文本字段
- 编辑限制：
  - 在 `To be Purchasing Verify` 状态，采购申请用户与部门采购经理不可修改记录
  - 限制两类用户修改 PR 编号（界面只读 + 服务器端拦截）
- 日志增强：
  - 修改行的数量或单价时，会在 Chatter 中记录修改人以及变更前后值

## 界面改动
- PR 表单（明细树）：
  - 在“数量”后显示“单价（Unit Price）”
  - 将“Estimated Cost”列名改为“Total Price”
  - 可选显示“Reason（采购目的）”列
  - 页脚合计标签由“Estimated Cost”改为“Total Price”
- PR 行表单：
  - 新增“Unit Price”“Reason”，并显示只读的“Total Price”
- 状态栏：
  - 增加并显示 `To be Purchasing Verify` 状态

## 权限与访问
- 组：
  - Department Purchase Manager：可进行部门审批
  - Purchase Request Manager：可进行采购核验与后续审批
- 限制：
  - 采购申请用户与部门采购经理不可修改 PR 编号
  - 服务器写入限制：在 `to_purchasing_verify`、`to_approve`、`approved`、`in_progress`、`done`、`rejected` 状态禁止上述两类用户修改

## 安装与配置
依赖：`purchase_request`、`purchase_request_user_pr_prefix`

1. 为用户设置 PR Prefix：设置 → 用户与公司 → 用户 → PR Prefix
2. 将相应用户加入“Department Purchase Manager”组

## 备注
- 若配套有“隐藏成本”模块，页面上“Total Price”的显示仍受该模块的组权限控制
- 已在 Odoo 17 与 OCA `purchase_request` 17.0 上测试

## 许可
AGPL-3

