# 沉淀计划 · sage

日期：2026-04-27
作者：links
模式：create
起点：from-project (`~/Coding/A-complex/ikt/sage/frontend/`)
档位：Tier 3 · 全量级（目标 30–50+ 条 · 实际 38 条）
namespace：`sage`（关联 `products/sage`）

## 目标

把 sage 这个 "12 主题色多智能体数据分析平台" 的视觉语言整套沉淀——
从 12 主题色动态着色系统 / 9 阶 rgb 灰阶 / Inter 字体 / tailwindcss-animate 动效套件，
到雪人飘雪的 RevolverMenu / Cmd+P 命令面板 / 复古 CRT 404 / 玻璃质感 CrystalProgress 等独家 signature 组件。

## 字典变更（先于条目写入）

新增 `category: ai`（dot=#0ea5e9，order=1）。其它分类 order 顺位 +1。

> follow-up：未来如需 product 支持双 category（"category × ai"），需要单独升级 schema（`category: string` → `categories: string[]`）+ sync 脚本兼容。本次暂以 `ai` 单值 category 形式落地。

## 涉及条目（依赖拓扑序 · 38 条）

### Tokens（5）
1. `tokens/palettes/sage/twelve-theme-spectrum`
2. `tokens/palettes/sage/neutral-rgb-ladder`
3. `tokens/typography/pairs/sage/inter-stack`
4. `tokens/motion/sage/animate-in-suite`
5. `tokens/motion/sage/styled-keyframes`

### Components（8）
6. `components/buttons/sage/theme-bg-cta`
7. `components/buttons/sage/icon-circle-ghost`
8. `components/buttons/sage/stop-pulse-button`
9. `components/inputs/sage/glow-border-textarea`
10. `components/inputs/sage/icon-prefix-input`
11. `components/avatars-icons/sage/themed-circle-avatar`
12. `components/indicators/sage/crystal-progress-bar`
13. `components/indicators/sage/hairline-scrollbar`

### Blocks（13）
14. `blocks/nav/sage/themed-sidebar-shell`
15. `blocks/nav/sage/sidebar-session-row`
16. `blocks/nav/sage/space-switcher-dropdown`
17. `blocks/nav/sage/revolver-menu-fab`
18. `blocks/nav/sage/command-palette`
19. `blocks/layout/sage/management-layout-header`
20. `blocks/layout/sage/sidebar-detail-split`
21. `blocks/feedback/sage/spin-fullscreen-loader`
22. `blocks/feedback/sage/delete-confirm-modal`
23. `blocks/feedback/sage/admin-overlay-modal`
24. `blocks/marketing/sage/auth-emerald-card`
25. `blocks/form/sage/chat-composer`
26. `blocks/display/sage/datasource-card`

### Pages（10）
27. `pages/auth/sage/login-emerald-card`
28. `pages/dashboard/sage/agent-chat-stream`
29. `pages/list-table/sage/datasource-grid`
30. `pages/form-flow/sage/rule-set-stepper-modal`
31. `pages/list-table/sage/agent-store-split-tabs`
32. `pages/list-table/sage/space-management-split`
33. `pages/list-table/sage/admin-table-management`
34. `pages/dashboard/sage/analytics-feedback`
35. `pages/dashboard/sage/analytics-usage`
36. `pages/empty-error/sage/crt-tv-404`

### Style + Product（2）
37. `styles/saas-tool/sage-multitheme-data-platform`
38. `products/sage`

## 依赖关系（DAG）

```
products/sage
  → refs.style: styles/saas-tool/sage-multitheme-data-platform
  → refs.pages: [pages/auth/sage/login-emerald-card, ...10 pages]
  → refs.blocks: [...13 blocks]
  → refs.components: [...8 components]
  → refs.tokens.palette: tokens/palettes/sage/twelve-theme-spectrum
  → refs.tokens.typography: tokens/typography/pairs/sage/inter-stack
  → refs.tokens.motion: tokens/motion/sage/animate-in-suite

styles/saas-tool/sage-multitheme-data-platform
  → uses: 同上（style 是设计语言聚合，product 是聚合视图）

pages/* → uses: blocks + components + tokens
blocks/* → uses: components + tokens
components/* → refs.tokens: tokens/palettes/sage/* + tokens/motion/sage/*
tokens/* → 不引用任何上层
```

## 元信息填写方式

- AI 自动填：全部 38 条（步骤 2 用户授权 Y）
- 用户手填：（无）
- 后续 review 时可单条改

## Tier 3 覆盖率

| 维度 | 目标 | 实际 | 覆盖率 |
|---|---|---|---|
| 主路由 | 14 | 12（admin tables / collections / datasource / spaces 多路由合并 1 条 page）| 86% ✅ |
| 全局模式 | 5 | 5（themeClasses 119 / rgb-ladder / rounded家族 / animate-in / hover-to-reveal）| 100% ✅ |
| 表单 | 5 | 5（auth / chat-composer / rule-set / datasource / space）| 100% ✅ |
| 状态 | 5 | 5（spin / delete-confirm / admin-overlay / stop-pulse / crystal-progress）| 100% ✅ |
| 动效 | 7 | 7（animate-in suite + 7 keyframes）| 100% ✅ |

## 执行状态

☑ 用户已确认 · 待写入
