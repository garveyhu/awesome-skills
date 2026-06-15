---
id: pages/dashboard/acme/saas-monitor-overview
type: page
name: SaaS 监控总览
description: ICEOPS 主页 · topbar + status banner + KPI grid + latency 图 + 服务表格
platforms: [web]
theme: dark
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses:
  - blocks/nav/acme/saas-cold-topbar
  - blocks/feedback/acme/saas-status-banner
  - blocks/display/acme/saas-metric-grid
  - blocks/display/acme/saas-data-table
  - components/buttons/acme/ghost-button
preview: /preview/pages/dashboard/acme/saas-monitor-overview
---

# SaaS Monitor Overview

> 监控型 SaaS 的主页：所有关键指标 + 服务状态一屏看完，0 滚动看到核心。

## 视觉特征

自上而下结构：

1. **topbar (56px)**：`<SaasColdTopbar breadcrumb={['Monitoring','production']} />`
2. **status banner (32px, optional)**：当前 neutral 态信息提示
3. **主区**（max-w-1400, px-10 py-8）
   - 标题行："Monitoring · production" + 右侧时段切换 tab（Last 1h / 24h / 7d）+ ghost 按钮 "Export"
   - **KPI grid**：`<SaasMetricGrid />` 4 列
   - **latency 大图**：高 240px 折线区域，背景 `slate-900`，1px slate-800 outer border，title 行嵌 mini legend（emerald=p50, cyan=p99）
   - **services 表格**：`<SaasDataTable density="compact" />`，行高 40px，标题"Services · 12 active"

### 节奏

- block 之间间距 32px（不要 gap > 40，密度优先）
- 图表 + 表格各占满 100% 宽

## 反模式

- 不要在主页放 onboarding banner / 升级提示（破坏冷感专业度）
- 不要给 KPI 卡加边框 / 阴影
- 不要把图表做 3D / 立体阴影
