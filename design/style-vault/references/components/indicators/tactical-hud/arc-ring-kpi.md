---
id: components/indicators/tactical-hud/arc-ring-kpi
type: component
name: 270° 圆环 KPI
description: SVG 圆环（270° 弧 + 8 个 cardinal 刻度 + 渐变描边 + drop-shadow 霓虹光） + 中心 Orbitron 数字 + 单位，HUD / 战术屏标志性 KPI 形态
platforms: [web]
theme: dark
tags:
  aesthetic: [industrial, glass]
  mood: [confident, cold]
  stack: [html-tailwind, react-tailwind]
uses:
  - tokens/palettes/tactical-hud/hud-cyan-glass
  - tokens/typography/pairs/tactical-hud/orbitron-rajdhani-trio
preview: /preview/components/indicators/tactical-hud/arc-ring-kpi
---

# Arc Ring KPI

> 钢铁侠贾维斯界面的核心元素之一：270° 圆环作为 KPI 容器，中央放数字。圆环带 cardinal tick marks + 渐变描边 + 极淡霓虹光晕。

## 视觉锚点

- **270° 弧（不是 360°）**：起点 135°、终点 45°，底部缺口给"目标值 / target" caption
- **8 个 cardinal tick marks**：圆周每 45° 一根 1px 短线（4px 长），作为"刻度感"
- **渐变描边**：`linearGradient` 从 `hud #38bdf8` 到 `hud-2 #22d3ee`
- **drop-shadow 霓虹光**：`filter: drop-shadow(0 0 4px rgba(56,189,248,.6))`
- **中心数字**：Orbitron / 28-36px，状态色染色（ok 用 t1 偏蓝白 / fail 时整体染 bad 红）
- **下方单位 / 副 caption**：mono / 10-11px / t3 灰

尺寸建议 74×74 px（KPI 卡内）或 120×120 px（独立大圆环 KPI）。

## 用到的 tokens

- color：`hud #38bdf8` / `hud-2 #22d3ee` 渐变描边 / `t1` 中心数字 / `t3` 单位
- font：`orbi` 数字 + `mono` 单位
- 阴影：`drop-shadow(0 0 4-6px rgba(56,189,248,.4-.6))`

## 核心代码（SVG + Orbitron）

```html
<div class="arc-kpi relative" style="width:120px;height:120px">
  <svg viewBox="0 0 120 120" style="filter: drop-shadow(0 0 4px rgba(56,189,248,.5))">
    <defs>
      <linearGradient id="arcGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%"   stop-color="#38bdf8" />
        <stop offset="100%" stop-color="#22d3ee" />
      </linearGradient>
    </defs>

    <!-- 背景极淡圆 -->
    <circle cx="60" cy="60" r="48"
            fill="none" stroke="rgba(56,189,248,.1)" stroke-width="1.5" />

    <!-- 270° 弧：起 135°、终 45° -->
    <path d="M 26 94 A 48 48 0 1 1 94 94"
          fill="none" stroke="url(#arcGrad)" stroke-width="2.5"
          stroke-linecap="round" />

    <!-- 8 cardinal ticks -->
    <g stroke="rgba(56,189,248,.4)" stroke-width="1">
      <line x1="60" y1="6"  x2="60" y2="10" />
      <line x1="60" y1="110" x2="60" y2="114" />
      <line x1="6"  y1="60" x2="10" y2="60" />
      <line x1="110" y1="60" x2="114" y2="60" />
      <line x1="22" y1="22" x2="25" y2="25" />
      <line x1="98" y1="22" x2="95" y2="25" />
      <line x1="22" y1="98" x2="25" y2="95" />
      <line x1="98" y1="98" x2="95" y2="95" />
    </g>
  </svg>

  <!-- 中心数字 + 单位 -->
  <div class="absolute inset-0 flex flex-col items-center justify-center">
    <span class="orbi"
          style="font-size:32px;font-weight:600;color:rgba(220,240,255,.95);letter-spacing:.5px">
      98.7
    </span>
    <span class="mono" style="font-size:10.5px;color:rgba(160,195,225,.4);margin-top:2px">% SUCCESS</span>
  </div>
</div>
```

## 适配指南

- 圆环 stroke-width 与尺寸成比例：74px 圆 → 1.5px stroke / 120px 圆 → 2.5px stroke
- 中心数字字号 ≈ 圆直径 × 0.27（120 → 32px）
- 状态变红时**只染数字 + 描边**，不染整个 component（保持 HUD 蓝主调）
- 单位 caption 用 uppercase + letter-spacing 0.05em，强化"工程仪表"感
- 圆环初次进入用 `stroke-dasharray` 描出动画（1.2s ease-out）

## 反模式

- 不要做 360° 闭合圆——270° 的缺口才有"仪表盘"味
- 不要把刻度数搞太多（> 12 根）——cardinal 8 根足够，太密会乱
- 不要用 emoji 当中心内容
- 不要堆 hover 放大动画（保持静态克制感）
- 不要给圆环加渐变填充（fill）——只描边，让中心透出底色
