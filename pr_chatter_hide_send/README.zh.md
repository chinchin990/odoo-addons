# PR Chatter：隐藏“发送消息”

[中文] | [English](README.md)

在采购申请的 Chatter 中隐藏“发送消息”，仅保留“记录备注”，减少误发邮件的风险。

## 功能
- 作用范围仅限 purchase.request 表单。
- 纯 CSS 实现，无 JS/Python 覆盖。
- 样式注入 `web.assets_backend` 与 `mail.assets_messaging`（Odoo 17）。

## 安装
- Odoo 17。
- 安装模块后，强制刷新（或使用 `?debug=assets`）。

## 说明
- 非破坏性：卸载后恢复原状。

