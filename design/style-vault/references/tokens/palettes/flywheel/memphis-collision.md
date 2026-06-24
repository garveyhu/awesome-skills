---
id: tokens/palettes/flywheel/memphis-collision
type: token
name: 孟菲斯撞色板
description: 米白纸底 + 黑墨主色 + 黄/蓝/红三撞色 + 薄荷青 signature accent —— 鲜艳潮 IP 脸，可整组换脸
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist, maximal]
  mood: [playful, energetic, confident]
  stack: [react-tailwind]
preview: /preview/tokens/palettes/flywheel/memphis-collision
---

# 孟菲斯撞色板

> 米白纸底 + 黑墨超粗大字 + 黄/蓝/红孟菲斯撞色 + 薄荷青 signature（= IP 黑猫眼睛色）

## 视觉特征

- 主色 `ink #1A1A1A` 统治画面：超粗黑大字 / 2.5px 粗描边 / 硬位移阴影。**近黑非纯黑**
- 纸底 `paper #FFF8EC` 米白（**非纯白**）——手绘温度来源；叠层 `paper-2 #F3EAD8` 做卡面 / 分隔 / 次级区底
- 三撞色块：`yellow #FFD12E`（主撞色·最常用区底）/ `blue #2B5BE8` / `red #FF4D4D`（爆点 / 删除线）
- `mint #16C79A` 是 **signature 锐利强调** = IP 黑猫眼睛色——同屏极克制（只点高亮 / 进度条 / 当前态），**绝不大面积当底**
- `ink-soft #6E6A62` 暖中性灰做次要文字 / kicker / 水印；`ip-ear #FF8FA3` 仅 IP 粉内耳
- 配色纪律：**一个区一个主撞色底 + 黑墨大字主导 + mint 只点**；撞色有序、不堆花

## Tokens

```json
{
  "ink":          "#1A1A1A",
  "paper":        "#FFF8EC",
  "paper-2":      "#F3EAD8",
  "accent-yellow":"#FFD12E",
  "accent-blue":  "#2B5BE8",
  "accent-red":   "#FF4D4D",
  "accent-mint":  "#16C79A",
  "ip-ear":       "#FF8FA3",
  "ink-soft":     "#6E6A62"
}
```

派生为 CSS 变量（Tailwind v4 `@theme`）：`--color-ink` / `--color-paper` / `--color-mint` …，组件零硬编码、从变量取。事实源是 DTCG `tokens.dtcg.json`，改值后重派生、模板零改。

## 适配指南

- **换脸**：把 5 主色（ink / paper / yellow / blue / red / mint）整组替换即换风格，结构零改
- `mint` 同屏 ≤ 3 处，永远是"锐利强调"不是底色（呼应 signature）
- 撞色块当区底时配黑墨大字——**不要撞色叠撞色文字**
- **暗场反相**：`ink` 区底 + `paper` 文字 + `mint` 点（如长内容里插一段暗场强调），同一套 token 反着用即可

## 反模式

- 不要纯白底（要 `#FFF8EC` 米白）/ 不要纯黑字（要 `#1A1A1A`）
- 不要 `mint` 大面积当底——signature 会失效
- 不要紫→靛渐变 / 满屏玻璃拟态——违背孟菲斯硬扁平脸
- 不要三撞色平均分——要一个主撞色统治 + 黑墨主导
