---
id: tokens/shadow/flywheel/hard-offset-stack
type: token
name: 硬位移阴影体系
description: 0 模糊的硬位移阴影（6/3px）+ 2.5px 粗描边 —— 孟菲斯/新粗野的去塑料感签名
platforms: [web]
theme: light
tags:
  aesthetic: [brutalist]
  mood: [confident, playful]
  stack: [react-tailwind]
preview: /preview/tokens/shadow/flywheel/hard-offset-stack
---

# 硬位移阴影体系

> 不带模糊的"硬位移"阴影 + 2.5px 实心粗描边——这套脸的去塑料感来源，brutalist 标志

## 视觉特征

- **硬阴影**：`box-shadow: 6px 6px 0 #1A1A1A`（**位移、0 模糊、0 扩散**）——卡片像被实心黑块垫在右下，立体感来自硬边不是柔光
- 小号 `box-shadow: 3px 3px 0 #1A1A1A`（次级卡 / 小标签）
- **signature 变体**：`6px 6px 0 #16C79A`（薄荷青硬阴影）——强调卡 / CTA 用，呼应 IP 眼睛色
- **必配 2.5px 实心描边** `border: 2.5px solid #1A1A1A`——硬阴影 + 粗黑边成对出现，缺一个就软
- hover 微动：`translate(-2px,-2px)` 让阴影"变厚"（或 `hover:-translate-y-0.5`），不是改模糊
- 顶部进度 / 标签的小阴影 `2px 2px 0 #1A1A1A`

## Tokens

```json
{
  "shadow-hard":    "6px 6px 0 #1A1A1A",
  "shadow-hard-sm": "3px 3px 0 #1A1A1A",
  "shadow-hard-xs": "2px 2px 0 #1A1A1A",
  "shadow-signature":"6px 6px 0 #16C79A",
  "stroke":         "2.5px solid #1A1A1A",
  "stroke-thin":    "1.5px solid rgba(26,26,26,0.3)"
}
```

CSS 变量：`--shadow-hard` / `--shadow-hard-sm` / `--stroke`。Tailwind 任意值落地：`shadow-[6px_6px_0_#1A1A1A]` + `border-[2.5px] border-ink`。

## 适配指南

- 硬阴影**永远配粗描边**——`card-hard = border-[2.5px] border-ink + shadow-[6px_6px_0_#1A1A1A]`
- signature 薄荷青阴影只给"想强调的一个"（CTA / 当前态卡），不滥用
- 换脸时阴影色跟 ink 走（深主色），signature 阴影跟 accent 走
- 嵌套卡降一档：外卡 6px、内卡 3px，避免阴影打架

## 反模式

- ❌ 用模糊柔光阴影（`shadow-lg` 那种）——立刻塑料、失去 brutalist
- ❌ 硬阴影不配描边（会显得"飘"）
- ❌ 阴影色用半透明灰（要实心 ink）
- ❌ hover 改 blur 而非位移
