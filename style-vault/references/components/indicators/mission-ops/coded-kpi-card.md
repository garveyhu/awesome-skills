---
id: components/indicators/mission-ops/coded-kpi-card
type: component
name: 代号 KPI 卡
description: 带 KPI-NN 大写编号 + value/unit 拆分 + delta + 内嵌 sparkline 的工程 KPI 卡片，模仿 Bloomberg Terminal / NASA MOCR 的"模块化数据格"
platforms: [web]
theme: dark
tags:
  aesthetic: [industrial, editorial]
  mood: [cold, serious]
  stack: [html-tailwind, react-tailwind]
uses:
  - tokens/palettes/mission-ops/deep-space-amber
  - tokens/typography/pairs/mission-ops/plex-mono-inter-duo
preview: /preview/components/indicators/mission-ops/coded-kpi-card
---

# Coded KPI Card

> 工程屏标志性的 KPI 卡：左侧 2px accent bar + 顶部 `KPI-NN` 代号 + 中央数字+单位 + 右上角微 sparkline + 底部 delta/σ/max/min 三段统计

## 视觉锚点

- **必备 `KPI-NN` 编号**（uppercase mono 10-11px）——4 张卡分别是 `KPI-01 / KPI-02 / KPI-03 / KPI-04`
- **value/unit 拆分**：`12.4` 大字 mono + `M` 小字 mono 灰色尾标；数字部分 `tabular-nums`
- **左侧 2px accent bar**（state 色，根据 KPI 性质：ok=绿 / info=青 / warn=琥珀）
- **80×24 px 内嵌 sparkline**（SVG polyline，1.5px stroke，stroke 色 = accent）
- **底部 3 段微统计**（Δ / σ / max 或 min），每段独立 mono 数字 + 极小灰 label

## 用到的 tokens

- color：`text-1` 主数字 / `text-2` label / `text-3` 单位 / `text-4` 微统计 label
- state：`ok #34d399` / `info #22d3ee` / `warn #fbbf24` / `fail #fb7185`
- font：`mono` 数字 + 标签，`sans`（Inter）用于中文 title（如"今日总事件"）

## 核心代码（HTML + Tailwind + inline CSS）

```html
<div class="kpi-card relative bg-[#0a0e1a] border border-white/10 px-4 py-3.5"
     style="border-left:2px solid #34d399">
  <div class="flex items-center justify-between">
    <span class="mono" style="font-size:10.5px;letter-spacing:.08em;color:rgba(255,255,255,.38);text-transform:uppercase">KPI-01</span>
    <svg width="80" height="24" viewBox="0 0 80 24">
      <polyline points="0,18 12,16 24,12 36,14 48,8 60,10 72,4 80,6"
        fill="none" stroke="#34d399" stroke-width="1.5" />
      <circle cx="80" cy="6" r="2" fill="#34d399" />
    </svg>
  </div>
  <div class="sans mt-1.5" style="font-size:11px;color:rgba(255,255,255,.62)">今日总事件</div>
  <div class="mono flex items-baseline gap-1.5 mt-2"
       style="font-variant-numeric:tabular-nums">
    <span style="font-size:32px;font-weight:500;color:rgba(255,255,255,.96);letter-spacing:-.02em">12.4</span>
    <span style="font-size:14px;color:rgba(255,255,255,.38)">M</span>
  </div>
  <div class="mono flex items-center gap-4 mt-2.5"
       style="font-size:10.5px;color:rgba(255,255,255,.38)">
    <span><span style="color:#34d399">▲ 12.3%</span></span>
    <span>σ 0.42</span>
    <span>max 16.0M</span>
  </div>
</div>
```

## 适配指南

- 4 张卡一行：`grid grid-cols-4 gap-3`
- accent bar 颜色 = 第一 state 色：吞吐用 ok 绿、延迟用 info 青、告警用 warn 琥珀、可用率用 ok 绿
- delta 涨用 `▲ + ok 色`，跌用 `▼ + fail 色`
- 4 个 KPI 的 sparkline 应该是真实数据，**不要全是平/全是涨**，要有节奏对比

## 反模式

- 不要给卡加圆角 > 4px——工程屏统一直角 / 微圆角，圆角越大越不工程
- 不要加 box-shadow——层次靠 1px hairline 切割
- 不要让代号 `KPI-NN` 字号 > 11px——它是 caption 不是标题
- 不要把 sparkline 做成 area fill chart——卡内空间小，line + 末端 dot 最克制
