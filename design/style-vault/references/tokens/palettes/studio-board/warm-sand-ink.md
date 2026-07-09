---
id: tokens/palettes/studio-board/warm-sand-ink
type: token
name: 暖砂暖墨调色板
description: 暖砂/奶油双纸底 + 暖墨近黑 + 苔橄榄绿判成 + 暖近黑主 CTA + 金/陶土副色点睛 —— 亮暖砂 / 暗冷 slate 双主题
platforms: [web]
theme: both
tags:
  aesthetic: [editorial, minimal]
  mood: [warm, calm]
  stack: [react-tailwind]
preview: /preview/tokens/palettes/studio-board/warm-sand-ink
---

# 暖砂暖墨调色板

> 暖纸/暖砂打底 + 暖墨近黑主色 + 苔橄榄绿「判成/已发布」+ 暖近黑主操作 CTA + 金/陶土 ≤5% 点睛。亮暖砂、暗冷 slate 两套。

## 视觉特征

- **两套亮底同源不同温**：首页 board 用**奶油** `bg #f6f2e8` / `surface #fffdf7`（暖而亮，配冷蓝焦点 `#2557d6` 做链接高光）；详情页 workstation 用**暖砂** `bg #f0eeea` / `surface #fffdfa`（去黄一档、更灰更沉，配暖近黑焦点做主操作）。**同一张脸的两个温度档**，别混用焦点色
- **暖墨非冷黑**：文字 `#2a2620`（workstation·暖墨）/ `#161616`（board·近黑），`muted #8f8676`、`muted-strong #4a4438`——中性也带暖，绝不用纯 `#000`/冷 slate 文字
- **苔橄榄绿 `#5b8c5a` = 判「成/已发布」的语义主色**：管线完成节点、已发布徽标、通过态。低饱和橄榄，不刺、不荧光、不「科技绿」
- **暖近黑 `#2a2620` = 主操作 CTA**（focus token）：`打开成片`/`自动填充` 这类实底黑按钮就是它——focus 不是蓝，是暖墨本身，克制而权威
- **金 `#c8891f`（待发布/进行中）+ 陶土 `#c25a3a`（错误/冲突）= 副色**，各自 ≤5% 面积只点状态，不铺底
- **暗态换冷 slate**（仅 workstation 支持）：`bg #14161b` / `surface #1e222b` / 文字 `#eceef2`，绿 `#3fbe86`、金 `#e2a850`、陶土 `#e5686a` 提亮——暗场不跟暖砂走暖，改冷中性
- 配色纪律：**暖中性统治画面 + 苔绿判成一处点睛 + 金/陶土只标状态**，绝不彩虹、绝不紫靛渐变

## Tokens

```json
{
  "light-board": {
    "bg": "#f6f2e8",
    "surface": "#fffdf7",
    "surface-elevated": "#ffffff",
    "text": "#161616",
    "muted": "#746f66",
    "muted-strong": "#3d3934",
    "success": "#12805c",
    "warning": "#b77900",
    "risk": "#d92d20",
    "focus": "#2557d6"
  },
  "light-workstation": {
    "bg": "#f0eeea",
    "surface": "#fffdfa",
    "surface-elevated": "#ffffff",
    "text": "#2a2620",
    "muted": "#8f8676",
    "muted-strong": "#4a4438",
    "success": "#5b8c5a",
    "warning": "#c8891f",
    "risk": "#c25a3a",
    "focus": "#2a2620"
  },
  "dark-workstation": {
    "bg": "#14161b",
    "surface": "#1e222b",
    "surface-elevated": "#242a35",
    "text": "#eceef2",
    "muted": "#99a1ae",
    "muted-strong": "#c4c9d1",
    "success": "#3fbe86",
    "warning": "#e2a850",
    "risk": "#e5686a",
    "focus": "#3a4150"
  }
}
```

派生为 CSS 变量 `--color-bg` / `--color-surface` / `--color-text` / `--color-success` …；亮暖砂在 `:root[data-page='workstation']` 作用域覆盖，暗态挂 `[data-theme='dark']`。组件从变量取、零硬编码。

## 适配指南

- **换赛道**：整组换 `success`（判成语义色）+ `focus`（主 CTA）即换气质，结构零改；暖砂中性底建议保留（它是「暖纸感」的根）
- 主 CTA 用 `focus`（暖近黑）实底 + `surface` 反白字；语义状态用 `success`/`warning`/`risk` 描边 + `surface` 底 + 同色字（见 [[status-badge]]）
- 焦点色分场景：内容展示型（board）可用冷蓝做链接高光；工作/操作型（workstation）用暖近黑做主操作——**单页只用一种焦点色**
- 暗场不要沿用暖砂调暖，改冷 slate（暗底暖色发糊）

## 反模式

- 不要纯白 `#fff` 当底（要暖砂/奶油）、不要纯黑/冷 slate 当正文字（要暖墨 `#2a2620`）
- 不要把苔绿大面积当底——它是「判成」语义点睛，铺底就失效
- 不要金 + 陶土 + 蓝 + 绿一起上凑「彩虹」——一主暖中性 + 一判成绿 + 状态副色各点，克制
- 不要紫→靛渐变、不要青绿霓虹——违背暖纸产品脸
