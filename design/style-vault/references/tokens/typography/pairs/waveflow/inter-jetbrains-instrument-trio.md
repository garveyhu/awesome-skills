---
id: tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio
type: token
name: Inter · JetBrains Mono · Instrument Serif 三字体栈
description: 三字体策略 (sans / mono / serif-italic) + `tabular-nums` 工程师细节 + 内网静态打包（@fontsource，无外网）
platforms: [web]
theme: light
tags:
  aesthetic: [editorial, minimal, industrial]
  mood: [serious, calm, confident]
  stack: [shadcn-radix]
uses: []
preview: /preview/tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio
---

# Waveflow Inter · JetBrains · Instrument Trio

> waveflow 用**三字体**做语义切分：**Inter** 跑所有正文/UI；**JetBrains Mono** 跑所有数字/cron/ID/路径/日志；**Instrument Serif (italic)** 只在登录页右半页诗句出现，做"editorial 性格出口"。所有字体走 `@fontsource` npm 包静态打包到 `dist/assets/`，部署在纯内网无 CDN 也能 work。

## Tokens

```json
{
  "fontFamily": {
    "sans":  "'Inter', -apple-system, 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif",
    "mono":  "'JetBrains Mono', ui-monospace, sfmono-regular, 'SF Mono', menlo, consolas, monospace",
    "serif": "'Instrument Serif', 'Songti SC', 'STSong', georgia, serif"
  },
  "imports": {
    "inter":      ["@fontsource/inter/400.css", "/500.css", "/600.css", "/700.css"],
    "jetbrains":  ["@fontsource/jetbrains-mono/400.css", "/500.css", "/700.css"],
    "instrument": ["@fontsource/instrument-serif/400.css", "/400-italic.css"]
  },
  "scale": {
    "10":    "10px (icon-only meta · sidebar 用户在线状态 / sidebar child badge)",
    "10.5":  "10.5px (uppercase tracking-wider 元信息 caps · GlueType badge / Meta caps label)",
    "11":    "11px (table mono numbers / KPI delta)",
    "11.5":  "11px (table cell mono numbers / sidebar 在线计数 / kbd font / Toast description)",
    "12":    "12px (form label / sidebar online state / DropdownMenuItem)",
    "12.5":  "12px (sidebar nav text / DialogDescription / TableToolbar input)",
    "13":    "13px (Input default / Select trigger / form Label / SearchPanel row title)",
    "13.5":  "13px (sidebar brand label / Section title / Card-section h3)",
    "14":    "14px (page header h1 / Dialog body text)",
    "15":    "15px (DialogTitle / login form input)",
    "15.5":  "15px (sidebar brand)",
    "16":    "16px (json-format h2 / login subtitle small)",
    "20":    "20px (page h1 / Dialog 关闭按钮)",
    "24":    "24px (MetricCard value)",
    "28":    "28px (KPI big num · letter-spacing -0.02em / login title)",
    "30":    "30px (login 'Waveflow.' 右半页诗句)"
  },
  "weight": {
    "normal":   400,
    "medium":   500,
    "semibold": 600,
    "bold":     700
  },
  "tracking": {
    "tight":    "-0.02em (KPI 大数字 / 登录 'Waveflow.' / dashboard 大标题)",
    "normal":   "0",
    "wider":    "0.05em (text-[10.5px] uppercase / text-[11px] uppercase 元信息 caps · 9 处)",
    "ultra":    "0.4em ('实时编排 · 数据中枢' tagline · 1 处)"
  },
  "utilities": {
    ".tnum":    "font-variant-numeric: tabular-nums  (所有数字列必加)",
    ".kbd":     "padding:1px 5px; font-family:mono; font-size:10px; bg:white; border:1px stone-200; shadow:0 1px 0 stone-200"
  }
}
```

## 视觉特征

- **mono 不是给代码用**：是给"数字 / 时间戳 / cron / 路径 / ID"用——这是 waveflow 的工程师身份认证。`font-mono text-[11.5px] tnum text-stone-600` 是 7 处文件共用的"数字列范式"
- **`.tnum`（tabular-nums）必加**：让数字"立起来"对齐，没了它表格里的 0-9 等宽就废了
- **serif italic 只用 1 处**：登录右半页"自如流转。" 4 个字——这是整站的 editorial 出口，**整个 admin 主体不出现 serif**
- **uppercase tracking-wider 10.5–11px 元信息**：sidebar 分组标题（"调度"/"系统"）、breadcrumb meta、GlueType badge——9 处共享同一规格
- **`text-[28px] font-bold tnum letter-spacing -0.02em`** 是 KPI 卡的大数字范式

## 适配指南

- 三字体走 CSS var：`var(--font-sans)` / `var(--font-mono)` / `var(--font-serif)`
- 数字一律加 `font-mono tnum`，文字一律默认 Inter（无需声明）
- 元信息小标题：`text-[10.5px] uppercase tracking-wider text-stone-500`
- 内网部署：必走 `@fontsource`，**绝不**用 Google Fonts CDN

## 反模式

- ❌ 标题字重超 700——waveflow 没有 800/900 展示字体层级
- ❌ 把 mono 用到正文——立刻变 IDE 风
- ❌ 数字列不加 `tnum`——表格美感塌方
- ❌ 把 Instrument Serif 用到 admin 正文——破坏 editorial vs minimal 的语义切分
