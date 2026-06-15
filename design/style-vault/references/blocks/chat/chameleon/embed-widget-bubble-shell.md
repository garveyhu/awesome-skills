---
id: blocks/chat/chameleon/embed-widget-bubble-shell
type: block
name: 嵌入式浮动气泡对话挂件
description: vanilla-TS + Shadow DOM 浮动圆气泡 + 弹出对话面板（header/messages/composer/brand 水印 + 历史会话 overlay 侧栏），全视觉由 admin ui_config 驱动，主色默认 indigo
platforms:
- web
theme: both
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses: []
preview: /preview/blocks/chat/chameleon/embed-widget-bubble-shell
---

# Chameleon Embed Widget · 浮动气泡对话挂件

> 独立打包的 vanilla-TS + **Shadow DOM (`:host { all: initial }`)** 浮动挂件：右下角圆气泡（点开弹出对话面板），面板含 header / messages / composer / brand 水印 + 历史会话 overlay 侧栏。**全部视觉由 admin 端 `ui_config` 单一对象驱动**——主色 / header 底 / 字号 / 阴影档 / 圆角 / 暗色 auto 全可调，`fullscreen` 模式供 iframe 复用。这是 Chameleon 唯一对外可嵌入表面，是它的 signature moment：一个完整的可主题化聊天产品塞进一个 shadow root。

源码：`embed/src/styles.ts`（buildStyles 把 ui_config 映射成整张 CSS）· `embed/src/widget.ts`（渲染 DOM）。主色默认 `theme_color #6366F1`（indigo），与系统内部暖白蓝（blue-600）刻意不同。

## 视觉特征

### 气泡 bubble

- `width/height = bubble_size`（默认 56，clamp 40–96）`border-radius 50% background bubbleColor(#6366F1) color #fff`
- 阴影默认 lg：`0 12px 40px rgba(0,0,0,.18), 0 4px 12px rgba(0,0,0,.08)`；hover `transform: scale(1.06)`
- 内 icon `width/height ≈ 47% × bubble_size`（56→~26px）
- `transparent` 模式：去 background/box-shadow，icon 加 `drop-shadow(0 1px 2px rgba(0,0,0,.25))` 描黑外环
- 固定 4 角位 `right/left × bottom/top`，距边 24px
- tooltip line（招呼语）：`background paneBg border 1px borderColor border-radius 14px padding 7px 12px max-width 220px box-shadow 0 4px 14px rgba(0,0,0,.08)` + `bubble-tip-in .35s` 淡入上移

### 面板 panel

- `width = panel_width`（默认 400，clamp 280–520）`height = panel_height`（默认 600，clamp 360–800）`border-radius = border_radius`（默认 12，clamp 0–32）阴影同气泡 lg
- `max-height: calc(100vh - 120px)`，开态 `opacity 1 transform translateY(0) scale(1)`，`transition .18s`；闭态 `translateY(8px) scale(.98)`
- 角位 `bottom/top: 96px`（让出气泡 24+56+16）
- `z-index: 2147483647`（最大整数，盖一切宿主元素）
- **fullscreen 模式**（iframe）：`inset: 0; width/height 100%; border-radius 0; box-shadow none; transform none`

### header

- `padding 14px 16px background headerBg`，文字色按 headerBg 亮度 YIQ>175 自适应（浅底→`#111827`深字 / 深底→`#FFFFFF`）
- emoji `font-size 22px`（或 `icon_url` 图 `22×22 rounded 4`）+ title `14px/600 line-height 1.3` + sub `12px opacity .85 margin-top 2px`
- 关闭按钮 `padding 4 border-radius 6`，hover `rgba(255,255,255,.18)`

### messages 流

- `padding 16 gap 12 display flex column`
- `.msg` `max-width 88% gap 6`；user `align-self flex-end flex-direction row-reverse`
- bot 头像 `font-size 18px` 或 `22×22 rounded 4` 图
- **bubble-text** `padding 9px 12px border-radius 18px(bubbleRadius) font-size font.panel(md 13.5px) line-height 1.6`
  - user `background userBubble(themeColor) color #fff border-top-right-radius 4`（贴头像侧直角 tail）
  - bot `background botBubble border 1px botBubbleBorder color paneText border-top-left-radius 4`
  - error `background errorBg color errorText border errorBorder`
- 打字 typing：三个 `6×6 圆 background subtleText`，`typing 1.2s` 上跳 -4px（delay 0/.15/.3s）
- citation-chip `border-radius 10 background citationBg border citationBorder color citationText font.meta` inline-flex
- suggested-questions `border-radius 999 border 1px themeColor color themeColor`，hover 反色（`background themeColor color #fff`）
- msg-tools（hover 浮现于 user）icon `13×13`，active `color themeColor`，danger hover `rgba(220,38,38,.10) #dc2626`

### composer

- `padding 12px 14px 6px gap 6 display flex align-items center`
- textarea `border 1px inputBorder border-radius 12 min-height 38 padding 8px 14px font.panel line-height 1.4 max-height 110`，soft shadow `0 1px 2px rgba(15,23,42,.04), 0 4px 12px rgba(15,23,42,.04)`，focus `border-color inputFocus(themeColor)`
- upload-btn `38×38 border-radius 10 color subtleText`，hover `rgba(127,127,127,.10)`
- send-btn `38×38 border-radius 12 background themeColor color #fff box-shadow 0 2px 6px rgba(99,102,241,.30)`，hover `scale(1.05)` + 更深阴影，disabled `opacity .45`

### 历史会话 overlay 侧栏

- `position absolute inset 0 z-index 5`，覆盖主对话区，开态淡入 `transition .14s`
- sidebar-title `14px/600`，`::before` 一根 `3px × 14px border-radius 2 background themeColor` 竖条
- new-session-btn `border-radius 999 border 1px themeColor55 color themeColor`，hover `background themeColor0d`
- sidebar-item `padding 9px 10px border-radius 8`，active `background themeColor14 color themeColor`，avatar `24×24 圆 background themeColor1a`

### brand 水印

- `text-align center font-size 11px color brandText padding 4px 0 8px`「powered by Chameleon」

## Tokens

```json
{
  "theme_color": "#6366F1 (主色，气泡/user 气泡/send/链接/侧栏强调)",
  "font_px": {
    "sm": { "panel": 12.5, "meta": 11 },
    "md": { "panel": 13.5, "meta": 12 },
    "lg": { "panel": 14.5, "meta": 12.5 }
  },
  "shadow": {
    "none": "none",
    "sm": "0 2px 8px rgba(0,0,0,.08)",
    "md": "0 6px 18px rgba(0,0,0,.12), 0 2px 6px rgba(0,0,0,.06)",
    "lg": "0 12px 40px rgba(0,0,0,.18), 0 4px 12px rgba(0,0,0,.08)"
  },
  "clamp": {
    "bubble_size": "40–96 (默认 56)",
    "panel_width": "280–520 (默认 400)",
    "panel_height": "360–800 (默认 600)",
    "border_radius": "0–32 (默认 12)"
  },
  "bubble_radius": 18,
  "bubble_tail_radius": 4,
  "light": {
    "paneBg": "#FFFFFF", "paneText": "#111827", "subtleText": "#6B7280",
    "borderColor": "#E5E7EB", "inputBorder": "#D1D5DB",
    "botBubble": "#FFFFFF", "botBubbleBorder": "#E5E7EB",
    "citationBg": "#F8FAFC", "citationBorder": "#E2E8F0", "citationText": "#475569",
    "errorBg": "#FEF2F2", "errorBorder": "#FECACA", "errorText": "#B91C1C",
    "brandText": "#94A3B8"
  },
  "dark": {
    "paneBg": "#0F172A", "paneText": "#F1F5F9", "subtleText": "#94A3B8",
    "borderColor": "#1E293B", "inputBorder": "#334155",
    "botBubble": "#1E293B", "botBubbleBorder": "#334155",
    "citationBg": "#1E293B", "citationBorder": "#334155", "citationText": "#CBD5E1",
    "errorBg": "#7F1D1D", "errorBorder": "#991B1B", "errorText": "#FCA5A5",
    "brandText": "#475569"
  }
}
```

## 核心代码

```ts
// styles.ts —— header 文字按底色亮度自适应（YIQ）
const isLightHex = (hex: string): boolean => {
  const full = /* 展开成 6 位 */;
  const r = parseInt(full.slice(0,2),16), g = parseInt(full.slice(2,4),16), b = parseInt(full.slice(4,6),16);
  return (r*299 + g*587 + b*114) / 1000 > 175;  // 阈值 175
};
const headerText = configuredHeaderText
  ? configuredHeaderText
  : isLightHex(headerBg) ? (dark ? '#F1F5F9' : '#111827') : '#FFFFFF';

// clamp 安全边界
const radius = Math.max(0, Math.min(32, ui.border_radius ?? 12));
const panelW = Math.max(280, Math.min(520, ui.panel_width ?? 400));
const bubbleSize = Math.max(40, Math.min(96, ui.bubble_size ?? 56));
const bubbleIconSize = Math.round(bubbleSize * 0.47);
```

```css
/* 气泡贴头像侧的直角 tail —— 18 圆角 + 单角 4px */
.msg.user .bubble-text { background: var(--userBubble); border-top-right-radius: 4px; }
.msg.bot  .bubble-text { background: var(--botBubble); border: 1px solid var(--botBubbleBorder); border-top-left-radius: 4px; }
```

## 适配指南

- 所有视觉调参收口到一个 `ui_config` 对象——加新主题字段只改 `resolveTheme` + 注入 CSS，不散落
- 必须包进 Shadow DOM `:host { all: initial }`，否则宿主页面 CSS 会污染气泡
- `z-index: 2147483647` 不可省——业务方页面常有高 z 元素
- 暗色走 `mode: 'auto'` 跟随 `prefers-color-scheme`，paneBg `#0F172A` / text `#F1F5F9`
- iframe 复用走 `fullscreen` 类：去圆角阴影 transform，占满父容器
- @media ≤480: panel `width calc(100vw-24)`，角位收到 12/16

## 反模式

- ❌ 不进 Shadow DOM——宿主页 reset/CSS 会击穿气泡样式
- ❌ header 文字写死白色——浅底（白 header_bg）白字看不见，必须按 YIQ 亮度自适应
- ❌ 气泡四角全圆——贴头像那一角必须 4px 直角做「指向」语义
- ❌ 把主色硬编码成系统内部 blue-600——挂件主色独立走 theme_color（默认 indigo #6366F1），允许业务方换色
- ❌ panel 给固定 height 不留 `max-height: calc(100vh-120px)`——小屏会溢出视口
