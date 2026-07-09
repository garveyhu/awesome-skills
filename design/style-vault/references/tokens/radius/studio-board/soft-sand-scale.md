---
id: tokens/radius/studio-board/soft-sand-scale
type: token
name: 暖砂大软圆角阶
description: 7/10/12/16(基)/20/22 六档大软圆角 —— 详情页卡/抽屉走大圆角，柔而沉，配白玻璃有「软件产品」手感
platforms: [web]
theme: both
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, warm]
  stack: [react-tailwind]
---

# 暖砂大软圆角阶

> 详情页 workstation 走**大软圆角**（基准 16px、卡/抽屉到 20–22px），比首页 board（基准 8px）明显更圆——大圆角 + 白玻璃 = 现代软件产品的松弛手感。

## 视觉特征

- **workstation 阶（大软）**：`xs 7 · sm 10 · DEFAULT 12 · md/基 16 · lg 20 · drawer 22`。玻璃卡用 `lg`(rounded-lg→16)，抽屉 22，chip/pill 用 `full`
- **board 阶（收紧）**：`xs 4 · sm 6 · DEFAULT/基 8 · lg 12 · drawer 18`——首页密度更高、圆角更收，卡片用 `rounded-lg`(12)/`rounded-xl`
- **pill/徽标恒 `rounded-full`**（状态徽标、平台切换、计数、文件 tab 全走胶囊）
- 封面图用 `rounded-xl`(12)；封面泼色光晕外扩用 `rounded-[36px]`（大到几乎看不出角、只为柔化光斑边缘）
- 圆角成体系写进 CSS 变量 `--radius-*`，全站从变量取——同一元素类别用同一档

## Tokens

```json
{
  "workstation": { "xs": 7, "sm": 10, "DEFAULT": 12, "base": 16, "lg": 20, "drawer": 22 },
  "board": { "xs": 4, "sm": 6, "DEFAULT": 8, "lg": 12, "drawer": 18 },
  "pill": "9999px",
  "cover": 12,
  "glow-halo": 36
}
```

## 适配指南

- 「工作/操作台」型页面用大软阶（≥16 基准）配白玻璃；「密集信息/列表」型页面用收紧阶（8 基准）
- 卡与卡内元素圆角要拉开层级（外卡 16–20、内 chip full、内小块 10–12），别同一个圆角一刀切
- pill 永远 full，不要给徽标/切换用中等圆角（那会显「半成品组件级」）

## 反模式

- 不要详情页也用小圆角（8 以下）——会失去松弛的产品手感
- 不要圆角混乱（同类元素一会 12 一会 16）——成体系从变量取
