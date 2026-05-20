---
id: blocks/display/tactical-hud/radar-sweep-panel
type: block
name: 雷达扫描全息面板
description: backdrop-blur 玻璃面板 + 4 角 HUD 角标 + 缓慢旋转的雷达扫描扇形 + PING 脉冲圆，HUD / 战术屏的标志性容器
platforms: [web]
theme: dark
tags:
  aesthetic: [industrial, glass]
  mood: [confident, cold]
  stack: [html-tailwind, react-tailwind]
uses:
  - tokens/palettes/tactical-hud/hud-cyan-glass
  - tokens/typography/pairs/tactical-hud/orbitron-rajdhani-trio
preview: /preview/blocks/display/tactical-hud/radar-sweep-panel
---

# Radar Sweep Panel

> 战术 HUD 的"实时态"容器：玻璃面板 + 4 角角标 + 雷达扫描动效 + PING 脉冲。模仿钢铁侠贾维斯 / Halo 战术屏的"持续观测中"感觉。

## 视觉锚点

- **玻璃面板基底**：`backdrop-filter: blur(20px)` + `bg: rgba(56,189,248,0.05)` + `border: 1px solid rgba(56,189,248,0.25)`
- **4 角 HUD 角标**：每个角 `⌐` 形状（2 条 1px 短线呈直角），HUD 蓝 70% 透明度
- **雷达扫描扇形**：SVG 内的 conic-gradient 扇形（90° 弧 + 蓝渐变 + 半透明），`animation: sweep 5s linear infinite` 缓慢旋转
- **PING 脉冲圆**：顶部一个小圆点，box-shadow 扩散 0 → 20px 透明度 1 → 0，1.5s 周期
- **顶部 panel header**：左侧 Orbitron 大写代号 + Rajdhani 副标题 + 右侧状态点（与 mission-ops 的 coded-panel-header 风格相近但调色更"全息"）

## 用到的 tokens

- glass / line / line-soft 三色
- hud / hud-2 双蓝
- orbi 字体（代号）+ sans（副标题）

## 核心代码（HTML + CSS keyframes + SVG）

```html
<style>
  .radar-panel {
    position: relative;
    background: rgba(56,189,248,0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 4px;
    padding: 16px;
    box-shadow: inset 0 0 24px rgba(56,189,248,0.04);
    overflow: hidden;
  }
  .radar-panel::before, .radar-panel::after {
    content: '';
    position: absolute;
    width: 12px; height: 12px;
    border-color: rgba(56,189,248,0.7);
    border-style: solid;
    border-width: 0;
  }
  .radar-panel::before { top: 4px; left: 4px;  border-top-width: 1px; border-left-width: 1px; }
  .radar-panel::after  { bottom: 4px; right: 4px; border-bottom-width: 1px; border-right-width: 1px; }
  /* 加另外 2 个角通过子元素或 inner shadow 实现 */

  .radar-sweep {
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: conic-gradient(from 0deg, transparent 0deg, rgba(56,189,248,0.18) 60deg, transparent 90deg);
    mask: radial-gradient(circle at center, transparent 30%, black 100%);
    animation: sweep 5s linear infinite;
    opacity: 0.6;
  }
  @keyframes sweep { to { transform: rotate(360deg); } }

  .ping-dot {
    position: absolute;
    top: 12px; right: 18px;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 0 0 rgba(74,222,128,0.5);
    animation: ping 1.5s ease-out infinite;
  }
  @keyframes ping {
    0%   { box-shadow: 0 0 0 0   rgba(74,222,128,0.6); }
    100% { box-shadow: 0 0 0 12px rgba(74,222,128,0); }
  }
</style>

<div class="radar-panel">
  <div class="radar-sweep"></div>
  <span class="ping-dot"></span>

  <header class="flex items-center gap-2 mb-3">
    <span class="orbi" style="font-size:11px;letter-spacing:2px;color:#38bdf8;text-transform:uppercase">RDR-LIVE</span>
    <span style="width:1px;height:10px;background:rgba(56,189,248,0.4)"></span>
    <span class="sans" style="font-size:12px;color:rgba(190,215,240,0.62)">实时观测</span>
  </header>

  <div class="content" style="color:rgba(220,240,255,0.95)">
    <!-- panel 主体内容 -->
  </div>
</div>
```

## 适配指南

- 雷达扫描的 sweep 角度（60deg）可调，但**不要超过 90deg**——扇形太大失去"扫描线"感
- ping 用绿色（ok 态）；panel 转 fail 时 ping 切红、脉冲速度加快到 0.8s
- 4 角角标可省略到 2 个（左上 + 右下），保持对角即可
- panel 高度 > 240px 时 sweep 才显眼，矮 panel 不要加扫描

## 反模式

- 不要让 sweep 动画过快（< 3s 周期 = 廉价"游戏 UI"）
- 不要在同屏放 > 2 个 sweep panel（视觉竞争）
- 不要把 glass 透明度调到 > 0.1（失去"透出底色"感）
- 不要用纯色 background 代替 backdrop-blur（玻璃感是这个 block 的核心）
- 不要把 ping 颜色弄成 hud 蓝——会和扫描扇形混色识别度低
