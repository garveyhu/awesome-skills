---
id: pages/list-table/acme/saas-incident-list
type: page
name: SaaS 事件列表
description: 高密度事件表格 · 顶栏 + filter chip 行 + 时间戳 + 严重度 tag + 状态 pulse
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/acme/saas-cold-topbar
  - blocks/display/acme/saas-data-table
  - components/buttons/acme/ghost-button
preview: /preview/pages/list-table/acme/saas-incident-list
---

# SaaS Incident List

> 事件 / 告警的全量列表页：高密度表格 + 多维筛选 + 等宽时间戳。

## 视觉特征

自上而下：

1. **topbar (56px)**：breadcrumb = `Monitoring › Incidents`
2. **page header (px-10 pt-8)**：
   - 标题 "Incidents · 47 active"（slate-100 28px）
   - 右侧 ghost CTA "Export CSV" + ghost "Create rule"
3. **filter chip 行 (py-3 border-b)**：
   - chip 形态：`severity: critical` 等可关闭项（×）+ "+ Add filter" 触发器
   - chip 用 `bg-slate-900 border border-slate-700 text-[12px] px-3 py-1 rounded`
4. **table**：使用 `<SaasDataTable />`，columns:
   - status (pulse, 48px)
   - id (Plex Mono, 100px)
   - title (1fr)
   - severity (tag, 80px)
   - opened_at (timestamp, 140px)
   - assignee (letter-avatar + name, 1fr)
   - rules_matched (number, 80px right)

severity tag 用纯色文字 + 1px border，**不**填色：critical=rose, high=amber, medium=cyan, low=slate

## 反模式

- 不要 filter chip 用色填充——只 1px border，避免视觉过载
- 不要 row 加 expand 折叠——点 row 进详情页
- 不要把"未读"用红点标——severity 已经表达紧急程度
