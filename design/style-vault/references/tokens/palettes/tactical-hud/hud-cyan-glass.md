---
id: tokens/palettes/tactical-hud/hud-cyan-glass
type: token
name: HUD 青光玻璃
description: 深空蓝径向渐变 + HUD 蓝主色 + 玻璃透视卡片底 + 4 色状态（绿/琥珀/红/紫），钢铁侠贾维斯 / 银翼杀手 2049 战术屏调色板
platforms: [web]
theme: dark
tags:
  aesthetic: [industrial, glass]
  mood: [cold, confident]
  stack: [html-tailwind, react-tailwind]
preview: /preview/tokens/palettes/tactical-hud/hud-cyan-glass
---

# HUD Cyan Glass

> 战术 HUD / 全息控制台风格的核心配色——深空蓝径向底 + HUD 蓝主色 + 玻璃面板 + 4 状态色

## 视觉特征

- **径向深空蓝**：从 `#040816`（外圈）到 `#0a1228`（中心）的 radial gradient，模拟"全息投影台"的纵深
- **HUD 双蓝**：`hud #38bdf8` 主、`hud-2 #22d3ee` 副，所有发光元素 / accent 都走这俩
- **玻璃面板背景**：`rgba(56,189,248,0.05)` 极淡 HUD 蓝 + `backdrop-filter: blur(20px)`，模拟"透明全息层"
- **4 状态色**：`ok #4ade80` 绿 / `warn #fbbf24` 琥珀 / `bad #f43f5e` 玫瑰红 / `info #c084fc` 紫
- **3 级文本**：`t1 (95%)` 偏蓝白 / `t2 (62%)` 中性 / `t3 (40%)` 暗弱

## Tokens

```css
:root {
  --bg-deep: radial-gradient(ellipse at center, #0a1228 0%, #040816 100%);
  --hud:      #38bdf8;
  --hud-2:    #22d3ee;
  --ok:       #4ade80;
  --warn:     #fbbf24;
  --bad:      #f43f5e;
  --info:     #c084fc;

  --line:      rgba(56, 189, 248, 0.25);
  --line-soft: rgba(56, 189, 248, 0.10);
  --glass:     rgba(56, 189, 248, 0.05);

  --t1: rgba(220, 240, 255, 0.95);
  --t2: rgba(190, 215, 240, 0.62);
  --t3: rgba(160, 195, 225, 0.40);
}
```

```json
{
  "bg": {
    "deep": "radial-gradient(ellipse at center, #0a1228 0%, #040816 100%)"
  },
  "hud": { "primary": "#38bdf8", "secondary": "#22d3ee" },
  "state": { "ok": "#4ade80", "warn": "#fbbf24", "bad": "#f43f5e", "info": "#c084fc" },
  "glass": "rgba(56,189,248,0.05)",
  "line":      "rgba(56,189,248,0.25)",
  "line-soft": "rgba(56,189,248,0.10)",
  "text":      { "1": "rgba(220,240,255,0.95)", "2": "rgba(190,215,240,0.62)", "3": "rgba(160,195,225,0.40)" }
}
```

## 适配指南

- 卡片必走 `glass` 背景 + `line` 1px 边 + `backdrop-filter: blur(20px)`——没有 blur 就退化成普通 card
- 发光描边用 `box-shadow: 0 0 0 1px var(--hud), 0 0 12px rgba(56,189,248,.3)`
- 文字主体用 `t1` 偏蓝白（不要纯白，破坏全息感）
- 状态色用 4 色，**不要再加第 5 个**——HUD 风的克制就在这 4 色上

## 反模式

- 不要替换 hud 蓝为绿 / 紫——HUD 蓝是这套配色的灵魂
- 不要把 bg 改成纯黑 `#000`——会失去径向纵深感
- 不要给 t1 用纯白 `#fff`——失去"投影感"，要带极淡蓝偏色
- 不要在 hud 蓝上叠任何渐变色装饰
