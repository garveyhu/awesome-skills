---
id: tokens/layout/quiver/iso-grid
type: token
name: 等距像素网格
description: 64×32 菱形瓦片 + 体素三面着色 + 画家算法层序的纯 DOM 等距坐标系，无 canvas / 无引擎
platforms: [web]
theme: dark
tags:
  aesthetic: [pixel, retro]
  mood: [playful, nostalgic]
  stack: [vanilla-css]
---

# 等距像素网格

> 64×32 菱形瓦片、体素三面着色、画家算法 z-index——纯 React + CSS（绝对定位 div + clip-path）搭出的等距世界，不用 canvas 也不用 Phaser

## 视觉特征

- **2:1 菱形瓦片**：瓦片宽 `TW = 64`、高 `TH = 32`（横纵对角线 2:1），墙高 `WALLH = 42`；办公室网格 `C = 13` 列 × `R = 9` 行
- **瓦片就是一个 clip-path 菱形 div**：`clip-path: polygon(50% 0, 100% 50%, 50% 100%, 0 50%)`，绝对定位、`margin-left: -TW/2` / `margin-top: -TH/2` 自居中
- **网格→屏幕的纯数学**：`iso(c,r,z) → { x: (c-r)*TW/2 + ox, y: (c+r)*TH/2 + oy - z }`（z 为离地高度，向上为负 y）
- **画家算法层序**：`zidx(c,r,z) = round((c+r)*10 + z*0.5) + 50`——越靠前（c+r 越大）越压上层，z 微调同格高低，无需 z-buffer
- **体素 = 三个 clip-path 面**：`isoBox` 画顶面 + 左面 + 右面三阶明暗（顶亮、左暗、右中）。常用配色 `WOOD {top:#9a7350, l:#5a4636, r:#7a5a3c}`、`DARK {top:#2a2f3e, l:#15131a, r:#20242f}`
- **墙体侧光**：西墙用 `filter: brightness(.6)` 压暗，模拟单向光源
- **文字浮层不进 world**：房间标签/人名走屏幕空间浮层，由相机 `project()` 算屏幕坐标定位——避免被 `transform: scale` 上采样糊字（DPR=1 也清晰）
- **包围盒留白**：`computeLayout()` 取四角投影 + 墙高 + 顶部光晕 50px 余量，边距 `mX 60 / mT 44 / mB 30`

## Tokens

```json
{
  "tile": { "TW": 64, "TH": 32, "WALLH": 42, "clip-path": "polygon(50% 0, 100% 50%, 50% 100%, 0 50%)" },
  "grid": { "C": 13, "R": 9 },
  "iso": { "x": "(c - r) * TW/2 + ox", "y": "(c + r) * TH/2 + oy - z" },
  "zidx": "round((c + r) * 10 + z * 0.5) + 50",
  "voxel-faces": {
    "WOOD": { "top": "#9a7350", "l": "#5a4636", "r": "#7a5a3c" },
    "WOOD2": { "top": "#a87f57", "l": "#5a4636", "r": "#7a5a3c" },
    "DARK": { "top": "#2a2f3e", "l": "#15131a", "r": "#20242f" }
  },
  "wall-side-light": "brightness(.6)",
  "margin": { "mX": 60, "mT": 44, "mB": 30, "top-glow": 50 }
}
```

## 适配指南

- 体素拼装：`isoBox(c,r, wc,dc, h, faces)` 给定格子起点 + 宽深格数 + 高度像素 + 三面色；浮空道具用 `chip`，地毯用 `rug`，正面屏/海报用 `southPanel`
- **任何要清晰的文字别画进 world**：收集世界坐标，交给屏幕空间浮层 + 相机 `project()`，文字 1:1 渲染
- 缩放别用 `will-change: transform` / 合成层——会先按原尺寸栅格化再 GPU 放大（DPR=1 糊）；静态缩放直接重栅格化更清晰

## 反模式

- 不要为这种规模上 canvas / WebGL / Phaser——纯 DOM clip-path 体素足够，且可直接用 CSS 调试、无引擎依赖（Quiver 正是从 Phaser 迁回 DOM）
- 不要把 z-index 写死——一律走 `zidx(c,r,z)` 画家算法，新增家具自动正确遮挡
- 不要让瓦片偏离 2:1（64×32）——等距菱形的贴合全靠这个比例，改了家具就拼不齐
