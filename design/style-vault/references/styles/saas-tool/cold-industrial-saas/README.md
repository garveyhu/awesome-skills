---
id: styles/saas-tool/cold-industrial-saas
type: style
name: 冷感工业 SaaS
description: 冷感留白 + IBM Plex 双字体 + 几何切割，工具型 SaaS 的整站调性
platforms: [web]
theme: both
tags:
  aesthetic: [minimal, industrial]
  mood: [cold, serious]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/acme/slate-cyan-ice
  - tokens/typography/pairs/acme/ibm-plex-duo
  - tokens/motion/acme/instant-snap
  - components/buttons/acme/ghost-button
  - components/buttons/acme/cyan-cta
  - components/inputs/acme/mono-input
  - components/indicators/acme/status-pulse
  - blocks/nav/acme/saas-cold-topbar
  - blocks/display/acme/saas-metric-grid
  - blocks/display/acme/saas-data-table
  - blocks/feedback/acme/saas-status-banner
  - pages/landing/acme/saas-landing
  - pages/auth/acme/auth-cold-split
  - pages/dashboard/acme/saas-monitor-overview
  - pages/list-table/acme/saas-incident-list
  - pages/pricing/acme/saas-cold-pricing
preview: /preview/styles/saas-tool/cold-industrial-saas
---

# Cold Industrial SaaS

> 冷感留白、几何切割、无圆角的工具型 SaaS 整站调性

## 设计哲学

**信息密度优先**——所有视觉决策让位于"一屏看完更多"。装饰是反生产力的；状态是产品最重要的视觉资产。

## 视觉特征

- 全站暗色（`slate-950 #0f172a` 底；`slate-900` 用作 panel 比页面深一档）
- IBM Plex Sans 做 UI、Plex Mono 做**所有数字与时间戳**——绝不混入第三种字体
- 圆角 ≤ 4px；**完全无阴影**，层次靠 1px hairline 切割
- 单一 cyan-400 高亮色——只用在 primary CTA / focus ring / 选中态 / 关键 dot
- **状态用脉冲而非色块**：healthy 才有 pulse 光晕，degraded / critical 静态（告警态不打扰）
- 动效 100/150/200ms 全 ease-out，无 bounce / 无回弹 / 无 scale 放大
- 表格行高 40px；header 32px；**等宽数字列必右对齐**
- KPI 数字用 Plex Mono 36-48px，配 11px uppercase tracking-wider caption
- delta 涨用 emerald-400、跌用 rose-400；面积极小，不抢主视觉
- 时间戳用 ISO 短格式（`02:14:08 UTC`），**不用**相对时间
- 字符间距：UI 默认 `tracking-tight`，所有 uppercase caption / mono 标签 `tracking-wider` (0.08-0.18em)

## 设计原则

1. **零浪漫动效**：直接切，不浪漫。spring / bounce / overshoot 一律禁止
2. **一色一职**：cyan = action / focus；emerald = healthy / 涨；rose = critical / 跌；amber = warning；slate = 一切其余
3. **状态分级动效**：状态切换瞬切色，不淡入；只 healthy 持续呼吸（被动状态用持续光晕表达"在线"）
4. **数字的可读性 > 装饰**：数字一律 mono、右对齐、tabular-nums
5. **告警不打扰**：异常态静态 + 颜色提示，绝不闪烁 / 弹窗

## Tokens 注入

把 uses 里的 token 注入 CSS 变量：

```css
:root {
  --font-sans: 'IBM Plex Sans', system-ui, sans-serif;
  --font-mono: 'IBM Plex Mono', 'SF Mono', monospace;
  --color-bg-base:    #0f172a;  /* slate-950 */
  --color-bg-panel:   #0b1220;  /* slightly deeper */
  --color-bg-subtle:  #1e293b;  /* slate-800 hairline */
  --color-fg-base:    #e2e8f0;
  --color-fg-muted:   #94a3b8;
  --color-fg-subtle:  #64748b;
  --color-accent:     #22d3ee;  /* cyan-400 */
  --color-emerald:    #10b981;
  --color-rose:       #ef4444;
  --color-amber:      #f59e0b;
  --duration-fast:    100ms;
  --duration-base:    150ms;
  --duration-slow:    200ms;
  --easing-out:       cubic-bezier(0,0,0.2,1);
  --radius-base:      4px;
}
```

## 适配指南

- 套该 style 后只需覆盖以上 CSS 变量即可适配新产品
- pages/* 系列保留结构，仅按上面 token 注入
- ghost-button 作为次要 CTA，cyan-cta 作为主 CTA，**全站同屏不超过 1 个主 CTA**
- 列表 / 表格场景一律走 `saas-data-table` 模式，**不要**回退到 Antd 默认表格
- ⌘K 命令面板是工具型 SaaS 的标志性交互，topbar 中央保留

## 反模式

- 不要圆角 > 4px
- 不要任何 box-shadow（除了 status-pulse 的呼吸光晕这一例外）
- 不要暖色 accent / 渐变背景 / 柔光
- 不要混入第三种字体家族
- 不要 scale / spring / bounce 动效
- 不要给状态切换加淡入淡出
- 不要左对齐数字
- 不要相对时间
