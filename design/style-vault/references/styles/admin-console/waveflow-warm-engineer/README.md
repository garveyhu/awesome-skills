---
id: styles/admin-console/waveflow-warm-engineer
type: style
name: Waveflow · 暖纸数据控制台
description: 暖白基底 (#fafaf7/#f4f3ee/#fffefb) + 墨黑 ink + blue-600 单一 CTA + Inter / JetBrains Mono / Instrument Serif 三字体 + tabular-nums 紧凑 + editorial 出口 (login serif italic)
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, industrial, editorial]
  mood: [calm, serious, confident]
  stack: [shadcn-radix]
uses:
  - tokens/palettes/waveflow/warm-paper-ink-blue
  - tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio
  - tokens/shadow/waveflow/soft-card-pop-trio
  - tokens/border/waveflow/translucent-stone-system
  - tokens/iconography/waveflow/engineer-detail-classes
  - tokens/motion/waveflow/keyframes-suite
  - tokens/motion/waveflow/three-icosahedron-bg
  - tokens/texture/waveflow/login-dot-grid-mask
  - tokens/texture/waveflow/login-floating-geom-quartet
  - tokens/layout/waveflow/data-console-shell
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
preview: /preview/styles/admin-console/waveflow-warm-engineer
---

# Waveflow Warm Engineer Style

> waveflow 整套设计语言——**暖白基底**让工程师后台不再冷冰冰、**墨黑 ink + blue-600 单一 CTA** 让信息层级简单，**Inter / JetBrains Mono / Instrument Serif 三字体**做语义切分（正文 sans / 数字密集 mono / editorial 出口 serif italic）、**`tnum` tabular-nums + `.kbd` + `.status-dot-*` + `.tree-line`** 等工程师细节，再加一个 **editorial 性格出口**（登录页 Three.js icosahedron + serif italic 诗句）让"工业 SaaS"不至于完全失去性格。

## 风格叙事

> 数据同步与任务调度平台的设计冲突：**严肃工程师感** vs **能让人想打开**。
>
> waveflow 的解法是：**admin 主体保持工业、紧凑、低饱和**（暖白 + 墨黑 + 蓝单 CTA + 等宽数字 + 极淡阴影），但在**唯一一个入口**——登录页——让位 editorial 风（Three.js + serif italic + dark dramatic）。每天登录时用户被"性格"一次，然后进入"严肃工作"——这是 waveflow 视觉策略的根。

## 视觉锚点（4 条 + 1）

### 锚点 1 · 三档暖白底色

`warm (#fafaf7)` 页面底 → `warm-2 (#f4f3ee)` 侧栏 / footer / 卡片头 → `paper (#fffefb)` 卡片 / dialog / popover —— 每往内 1 档亮一点，给"卡片浮起来"的层级感。**不出现 pure white**。

### 锚点 2 · 工程师细节四件套

- **`tnum` (tabular-nums)** 所有数字必加
- **`.status-dot[-running/-stopped/-error]`** 7px 状态点 + 2px 半透色 ring
- **`.tree-line + .tree-item`** sidebar 子项 L 形 connector
- **`.kbd`** 1px 底 shadow 键帽

四件套共同构成"这是工程师后台"的视觉签名。

### 锚点 3 · 三字体语义切分

**Inter** 正文 / UI · **JetBrains Mono** 所有数字/时间/cron/ID/路径 · **Instrument Serif** 只在登录右半页诗句"自如流转。" —— 三字体不滥用。

### 锚点 4 · 数据可视化语言

- **状态语言**：emerald running / red error / amber 执行中 / blue 进行中 / stone 灰停
- **任务类型**：11 种 GlueType chip 双变体（light 浅底深字 / solid 反显白字）
- **段方块视觉**：N 个 14×6px 方块 = N 个任务整体状态，一眼看到哪有问题
- **3-segment bar**：emerald/stone/red 横向比例
- **gauge 圆环**：CPU 蓝 / 内存红 / Load 自定

### 锚点 5 · Editorial 性格出口（独立于 admin）

登录页右半 Three.js 三层 icosahedron (indigo/pink/cyan wireframe) + 200 星点 + 鼠标 lerp + dark gradient bg + 30px serif italic 诗句 "自如流转。" + 11px tracking-[0.4em] tagline "实时编排 · 数据中枢" + 左半 dot grid mask + 4 SVG 浮件 + 动态连线 —— **整个登录页是 admin 视觉规则的反面**，故意做强对比。

## Tokens 矩阵

| 维度 | Token 引用 |
|---|---|
| Palette | `tokens/palettes/waveflow/warm-paper-ink-blue` |
| Typography | `tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio` |
| Shadow | `tokens/shadow/waveflow/soft-card-pop-trio` |
| Border | `tokens/border/waveflow/translucent-stone-system` |
| Layout | `tokens/layout/waveflow/data-console-shell` |
| Motion | `tokens/motion/waveflow/keyframes-suite` · `three-icosahedron-bg` |
| Iconography utility | `tokens/iconography/waveflow/engineer-detail-classes` |
| Texture (login only) | `tokens/texture/waveflow/login-dot-grid-mask` · `login-floating-geom-quartet` |

## 复刻指南

要做个同风格新产品，最小套餐：

1. 套全部 8 个 tokens（palette + typography 必，shadow/border/motion 强烈推荐）
2. 复用 `tree-line-sidebar` + `topbar-search-ping` + `cmdk-search-modal` 三件套 nav
3. 复用 `canonical-table-shell` + `data-table-leftbar-shimmer` + `table-toolbar-tri` 列表三件套
4. 不要复用登录 editorial split—— 那是 waveflow 的"性格出口"专属

## 反模式

- ❌ 把蓝 primary 换成其它色 —— 失去单一 CTA 的清晰感
- ❌ 把 stone 灰系换 zinc/gray —— 色温和暖底冲突
- ❌ admin 主体引入 serif —— 失去 editorial vs minimal 语义切分
- ❌ 数字段不加 `tnum` —— 表格对齐塌方
- ❌ 把状态色乱搭—— "成功"必 emerald / "错误"必 red 是不可妥协的语言
