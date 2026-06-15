---
id: products/waveflow
type: product
name: Waveflow · 数据同步与任务调度平台
description: 暖工业感数据控制台 · 任务编排全流程 + 任务集主从详情 + 6 KPI 实时 dashboard + 多机房资源监控 + 多数据库 JDBC 数据源
platforms: [web]
theme: light
category: productivity
refs:
  style: styles/admin-console/waveflow-warm-engineer
  pages:
    - pages/dashboard/waveflow/admin-runtime-report
    - pages/list-table/waveflow/canonical-section-list
    - pages/list-table/waveflow/job-mgmt-with-switch
    - pages/list-table/waveflow/job-log-batch-select
    - pages/detail/waveflow/jobset-master-detail
    - pages/form-flow/waveflow/json-build-stepper
    - pages/dashboard/waveflow/registry-monitor-articles
    - pages/auth/waveflow/login-editorial-three
    - pages/empty-error/waveflow/minimal-text-401
    - pages/empty-error/sage/crt-tv-404
    - pages/dashboard/waveflow/json-format-ace-dual
    - pages/detail/waveflow/log-viewer-pre
  blocks:
    - blocks/nav/waveflow/tree-line-sidebar
    - blocks/nav/waveflow/icon-collapsed-sidebar
    - blocks/nav/waveflow/topbar-search-ping
    - blocks/nav/waveflow/cmdk-search-modal
    - blocks/display/waveflow/canonical-table-shell
    - blocks/display/waveflow/data-table-leftbar-shimmer
    - blocks/display/waveflow/dashboard-kpi-six-row
    - blocks/display/waveflow/article-gauge-monitor
    - blocks/display/waveflow/metric-card-quartet
    - blocks/display/waveflow/set-card-segmented
    - blocks/layout/waveflow/master-detail-list-aside
    - blocks/filters/waveflow/table-toolbar-tri
    - blocks/form/waveflow/dialog-vertical-form
    - blocks/form/waveflow/login-editorial-form
    - blocks/form/waveflow/login-three-decor-right
    - blocks/form/waveflow/cron-builder-modal
    - blocks/form/waveflow/stepper-section-form
    - blocks/feedback/waveflow/top-progress-bar
    - blocks/feedback/waveflow/empty-dashed-state
    - blocks/feedback/waveflow/danger-confirm-modal
    - blocks/feedback/waveflow/log-pre-viewer
    - blocks/feedback/waveflow/action-dropdown-more
  components:
    - components/buttons/waveflow/cva-engineer-button
    - components/buttons/waveflow/dark-pill-arrow-cta
    - components/inputs/waveflow/blue-focus-input
    - components/inputs/waveflow/underline-bare-input
    - components/inputs/waveflow/datetime-range-presets
    - components/toggles/waveflow/emerald-switch
    - components/selects/waveflow/multi-select-popover
    - components/indicators/waveflow/status-dot-ring
    - components/indicators/waveflow/segmented-blocks
    - components/indicators/waveflow/pulse-ping-dot
    - components/tags-badges/waveflow/glue-type-badge-duo
    - components/tags-badges/waveflow/code-status-badge
    - components/typography-atoms/waveflow/kbd-key-cap
    - components/typography-atoms/waveflow/meta-caps-mono-pair
  tokens:
    palette: tokens/palettes/waveflow/warm-paper-ink-blue
    typography: tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio
    motion: tokens/motion/waveflow/keyframes-suite
tags:
  aesthetic: [minimal, industrial, editorial]
  mood: [calm, serious, confident]
  stack: [shadcn-radix]
uses: []
preview: /preview/pages/dashboard/waveflow/admin-runtime-report
---

## 产品定位

Waveflow 是面向**数据团队和运维工程师**的数据同步与任务调度平台 —— 把企业级调度内核包装成现代化暖工业感界面：

- **任务编排全流程**：从 Reader / Writer / 字段映射 4-step 可视化构建 → 任务模板复用 → 单任务运行 / 暂停 / 立即触发 → 任务集批量编排 → 日志查看与终止
- **跨网数据同步**：JDBC 数据源管理 + 12 数据库内置支持 (MySQL / PostgreSQL / Oracle / SQL Server / Kingbase / DM / ClickHouse / Doris / ...)
- **6 KPI 实时 dashboard**：调度量 + 成功率 + 平均耗时 + 在线执行器 + 活跃任务 + 24h 失败 · 30s 自动刷新 · ECharts 可视化
- **资源监控**：每台执行器 CPU / 内存 / Load 三 gauge 圆环 · 多机房多节点 article 堆叠
- **多用户多权限**：用户管理 + 角色 (ROLE_ADMIN) + 项目隔离 + 任务集成员分配

## 设计叙事

详见 [styles/admin-console/waveflow-warm-engineer](../../styles/admin-console/waveflow-warm-engineer)。一句话总结：**admin 主体严肃工业** + **登录入口 editorial 出口**——平衡"严肃可用"和"愿意打开"。

## 引用关系

```
products/waveflow
  → styles/admin-console/waveflow-warm-engineer
    → tokens × 8 + blocks × 22 + components × 14 + pages × 12 (其中 retro TV 404 跨 namespace 复用 sage)
```

## 跨 namespace 引用

- `pages/empty-error/sage/crt-tv-404` — sage 的复古 CRT 电视 404 是和 waveflow 同款（共用 styled-components 代码），跨 namespace 引用避免重复沉淀

## 适配指南

复刻一个同风格的内部 admin 平台（如内部数据中台 / 运维平台 / 任务调度系统）：

1. **完全复用 style**（8 tokens 全套）
2. **复用 nav 三件套**：tree-line-sidebar + topbar-search-ping + cmdk-search-modal
3. **复用列表三件套**：canonical-table-shell + data-table-leftbar-shimmer + table-toolbar-tri
4. **复用反馈三件套**：top-progress-bar + danger-confirm-modal + empty-dashed-state
5. **要不要复刻 editorial 登录**？—— 这是 waveflow 的"性格出口"，**不建议**直接复刻到别的产品（会"撞脸"）；新产品应该有自己的"性格出口"
