---
id: products/sage
type: product
name: Sage · AI 数据分析平台
description: 多智能体 NL→SQL 数据问答 / 多空间多用户 / 12 主题色个性化 / 雪人 FAB 彩蛋
platforms: [web]
theme: light
category: ai
refs:
  style: styles/saas-tool/sage-multitheme-data-platform
  pages:
    - pages/dashboard/sage/agent-chat-stream
    - pages/list-table/sage/datasource-grid
    - pages/list-table/sage/collection-list
    - pages/detail/sage/collection-detail
    - pages/detail/sage/datasource-detail-tabs
    - pages/form-flow/sage/rule-set-stepper-modal
    - pages/form-flow/sage/datasource-new-form
    - pages/settings/sage/ai-model-config
    - pages/settings/sage/space-core-config
    - pages/list-table/sage/agent-store-split-tabs
    - pages/list-table/sage/space-management-split
    - pages/list-table/sage/admin-table-management
    - pages/dashboard/sage/analytics-feedback
    - pages/dashboard/sage/analytics-usage
    - pages/auth/sage/login-emerald-card
    - pages/empty-error/sage/crt-tv-404
  blocks:
    - blocks/nav/sage/themed-sidebar-shell
    - blocks/nav/sage/sidebar-session-row
    - blocks/nav/sage/space-switcher-dropdown
    - blocks/nav/sage/revolver-menu-fab
    - blocks/nav/sage/command-palette
    - blocks/nav/sage/conversation-history-modal
    - blocks/nav/sage/user-menu-popout
    - blocks/layout/sage/management-layout-header
    - blocks/layout/sage/sidebar-detail-split
    - blocks/feedback/sage/spin-fullscreen-loader
    - blocks/feedback/sage/delete-confirm-modal
    - blocks/feedback/sage/admin-overlay-modal
    - blocks/feedback/sage/vector-test-modal
    - blocks/marketing/sage/auth-emerald-card
    - blocks/form/sage/chat-composer
    - blocks/form/sage/user-assignment-transfer
    - blocks/form/sage/row-column-rule-builder
    - blocks/display/sage/datasource-card
    - blocks/display/sage/chart-card-tabs
  components:
    - components/buttons/sage/theme-bg-cta
    - components/buttons/sage/icon-circle-ghost
    - components/buttons/sage/stop-pulse-button
    - components/inputs/sage/glow-border-textarea
    - components/inputs/sage/icon-prefix-input
    - components/inputs/sage/sql-editor-monaco
    - components/avatars-icons/sage/themed-circle-avatar
    - components/indicators/sage/crystal-progress-bar
    - components/indicators/sage/hairline-scrollbar
  tokens:
    palette: tokens/palettes/sage/twelve-theme-spectrum
    typography: tokens/typography/pairs/sage/inter-stack
    motion: tokens/motion/sage/animate-in-suite
tags:
  aesthetic: [minimal]
  mood: [calm, confident, dreamy]
  stack: [react-antd-tailwind]
uses: []
preview: /preview/products/sage
---

## 产品定位

Sage 是面向团队的 AI 数据分析平台 —— 把"自然语言提问"变成"数据库查询 + 可视化结果"，让非工程岗也能直接和数据说话。

- **多智能体内核**：`data_qa` (NL→SQL · LangGraph 驱动) / `data_qa_v2` (多步推理) / `general` (通用问答) / Dify Apps（外部接入）/ 自定义 Agent —— 一套 chat 界面接多个推理后端
- **多空间多用户**：每个空间独立的数据源 / 模型配置 / 规则集 / 成员；用户可在多空间间切换
- **多数据库**：MySQL / PostgreSQL / Oracle / SQL Server / Kingbase / DaMeng / ClickHouse / Doris / StarRocks / Elasticsearch / Redshift / Excel —— 12 种内置 logo 与连接器
- **行/列规则集**：admin 配置规则（行级权限 / 列级脱敏）+ 分配给具体用户，data_qa 生成的 SQL 自动注入规则
- **12 主题色个性化**：每位用户可在头像菜单切换主题，整站 119 处主题着色随之更新

## 设计叙事

sage 是一个"严肃工具 + 一处彩蛋"的混合体——

**严肃面**（chat / 仪表盘 / 表 / 表单）走极简：白底 + slate / 9 阶手调 RGB 灰阶 + 1px 边框分割 + Inter 单字体；视觉决策让位于"信息密度"和"主题色个性化"两个目标。

**彩蛋面**（RevolverMenu 雪人飘雪 FAB · 屏幕右下角）和（NotFound 复古橘色 CRT 电视机）是 sage 的"性格出口"——告诉用户"我们写代码的人有体温"。这两处不参与日常工作流，但当你不小心 pin 住了 RevolverMenu 看雪花飘下、或者打错路由进了 CRT 电视机页面时，会让 sage 立刻有了"灵魂"。

**主题色个性化**是 sage 跟 Linear / Notion / Vercel 最大的差异——用户不被品牌色绑架。当用户选了 "rose" 主题，整站 119 处 CTA / 选中态 / 进度条都会变成她喜欢的颜色——而沉浸感反而更强。

## 组成（Tier 3 全量 38 条）

### Style
- `styles/saas-tool/sage-multitheme-data-platform` · 整套设计语言

### Pages · 10 类（覆盖 14 个主路由）

| 路由 | Page 条目 |
|---|---|
| `/login` | `pages/auth/sage/login-emerald-card` |
| `/chat` + `/chat/:sessionId` | `pages/dashboard/sage/agent-chat-stream` |
| `/datasource` + `/new` + `/:id` | `pages/list-table/sage/datasource-grid` |
| `/admin/rules` | `pages/form-flow/sage/rule-set-stepper-modal` |
| `/admin/agent-store` | `pages/list-table/sage/agent-store-split-tabs` |
| `/spaces` + 子路由 | `pages/list-table/sage/space-management-split` |
| `/admin/users` + `/admin/roles` + `/collections` | `pages/list-table/sage/admin-table-management` |
| `/analysis/feedback` | `pages/dashboard/sage/analytics-feedback` |
| `/analysis/usage` | `pages/dashboard/sage/analytics-usage` |
| `*` (404) | `pages/empty-error/sage/crt-tv-404` |

覆盖率 12/14 = **86%**（admin tables / collections / datasource 三联 / spaces 三联 合并视觉模板）

### Blocks · 13 条
- Nav (5)：themed-sidebar-shell / sidebar-session-row / space-switcher-dropdown / revolver-menu-fab / command-palette
- Layout (2)：management-layout-header / sidebar-detail-split
- Feedback (3)：spin-fullscreen-loader / delete-confirm-modal / admin-overlay-modal
- Marketing (1)：auth-emerald-card
- Form (1)：chat-composer
- Display (1)：datasource-card

### Components · 8 条
- Buttons (3)：theme-bg-cta / icon-circle-ghost / stop-pulse-button
- Inputs (2)：glow-border-textarea / icon-prefix-input
- Avatars (1)：themed-circle-avatar
- Indicators (2)：crystal-progress-bar / hairline-scrollbar

### Tokens · 5 条
- Palettes (2)：twelve-theme-spectrum / neutral-rgb-ladder
- Typography (1)：inter-stack
- Motion (2)：animate-in-suite / styled-keyframes

## 复刻指南

要做一个 sage 风格的产品，最小集是：
1. tokens/palettes/sage/twelve-theme-spectrum + neutral-rgb-ladder
2. tokens/typography/pairs/sage/inter-stack
3. components/buttons/sage/theme-bg-cta + icon-circle-ghost
4. blocks/nav/sage/themed-sidebar-shell + sidebar-session-row
5. blocks/form/sage/chat-composer
6. pages/dashboard/sage/agent-chat-stream

加这 4 个就是 sage：
7. blocks/nav/sage/revolver-menu-fab（彩蛋灵魂）
8. pages/empty-error/sage/crt-tv-404（彩蛋灵魂）
9. tokens/motion/sage/styled-keyframes（动效底子）
10. components/indicators/sage/crystal-progress-bar（玻璃质感）

## 反模式

- ❌ 不允许只复刻"严肃面"而砍掉雪人 + CRT —— 失去性格
- ❌ 不允许把 12 主题色削减到 1 主色 —— 失去 sage 的"我的工具"立意
