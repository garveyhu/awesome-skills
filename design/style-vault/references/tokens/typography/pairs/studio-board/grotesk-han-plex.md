---
id: tokens/typography/pairs/studio-board/grotesk-han-plex
type: token
name: Grotesk × 苹方 × Plex 字体栈
description: Space Grotesk / IBM Plex Condensed 展示 + 苹方·Plex 正文 + JetBrains Mono 元信息 —— 几何 grotesk 配中文黑体的产品级排版
platforms: [web]
theme: both
tags:
  aesthetic: [editorial, minimal]
  mood: [warm, confident]
  stack: [react-tailwind]
---

# Grotesk × 苹方 × Plex 字体栈

> 西文几何 grotesk 做展示字骨架 + 中文苹方原生正文 + 等宽 JetBrains Mono 承载 slug/时间戳/进度/编号。产品级克制，非营销冲击。

## 视觉特征

- **display（展示/标题）**：workstation 用 `'Space Grotesk', 'IBM Plex Sans', 'PingFang SC', sans-serif`；board 用 `'IBM Plex Sans Condensed', 'PingFang SC', sans-serif`（更窄更紧、密度感）。标题 `font-semibold`（600）为主、hero 大标题 `font-bold`（700），字号走 `clamp(20px,2.4vw,28px)`，`leading-tight` + `tracking-tight`
- **body（正文）**：`'PingFang SC', 'Space Grotesk', 'Source Han Sans', sans-serif`——苹方原生不拉网络字体；正文 `13px`、`leading-relaxed`；次要说明 `text-muted-strong`
- **mono（等宽）= 结构承重字**：`'JetBrains Mono', ui-monospace, monospace`——slug、时间戳（`7-07 11:54`）、进度（`2/3`、`9/9`）、分组小标（`创意 · 需你定稿` uppercase tracking-[0.14em]）、文件 tab（`bilibili.md`）全走 mono。**mono 用得多而克制，是这套产品感的关键**
- **kicker 范式**：`font-display · text-[11px] · font-semibold · uppercase · tracking-[0.16em] · text-warning`（如「待发布 · 全矩阵同步」）
- 数字统计用 `tabular-nums`（等宽数字对齐，如交付统计 `74.6` / `4/4` / `9/9`）
- 极小字精致化：标签/元信息敢用 `text-[10px]`/`text-[11px]`，与大标题拉极端对比

## Tokens

```json
{
  "font-display-workstation": "'Space Grotesk', 'IBM Plex Sans', 'PingFang SC', 'Source Han Sans', sans-serif",
  "font-display-board": "'IBM Plex Sans Condensed', 'PingFang SC', 'Source Han Sans', sans-serif",
  "font-body": "'PingFang SC', 'Space Grotesk', 'IBM Plex Sans', 'Source Han Sans', sans-serif",
  "font-mono": "'JetBrains Mono', ui-monospace, monospace",
  "title-weight": 600,
  "hero-weight": 700,
  "title-tracking": "-0.01em",
  "kicker": "display · 11px · 600 · uppercase · 0.16em tracking",
  "meta": "mono · 10-11px",
  "nums": "tabular-nums"
}
```

## 适配指南

- **换字**：display 换任一几何 grotesk（Space Grotesk / Geist / Satoshi）即换气质；中文正文保留苹方原生（省加载、稳）；**mono 别省**——它是产品结构感的承重字
- 标题克制在 600/700，别一路 900（那是 banner 脸，不是产品脸）；靠字号 + tracking + 极小 mono 元信息拉层级
- 状态/编号/时间戳一律 mono + tabular-nums，横向对齐才「工程台」

## 反模式

- 不要 Inter / Roboto / 系统字兜底当主脸（要有性格的 grotesk）
- 不要中文标题堆 900 超粗（那是内容营销脸 [[han-black-grotesk]]，不是工具产品脸）
- 不要正文也用 mono（mono 只承载结构/元信息，正文用苹方）
