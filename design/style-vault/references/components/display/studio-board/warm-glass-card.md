---
id: components/display/studio-board/warm-glass-card
type: component
name: 暖白磨砂玻璃卡
description: 真半透 + 强模糊 + 亮边 + 顶部 light-leak 高光 + 玻璃内高光 + 柔暖投影的白玻璃卡；暗态自动转不透明深面
platforms: [web]
theme: both
tags:
  aesthetic: [glass, minimal]
  mood: [calm, warm]
  stack: [react-tailwind]
uses:
  - tokens/palettes/studio-board/warm-sand-ink
  - tokens/radius/studio-board/soft-sand-scale
preview: /preview/components/display/studio-board/warm-glass-card
---

# 暖白磨砂玻璃卡

> 详情页整套 UI 的承载件：一个 `.studio-glass` 类即得「真半透 + 强模糊 + 亮边 + 顶 light-leak 高光 + 玻璃内高光 + 柔暖投影」。暗态自动降级为不透明深面（去合成残影）。

## 视觉特征

- **真半透玻璃底**：`background: rgba(255,253,248,0.74)`（暖白·非纯白半透）+ `backdrop-filter: blur(30px) saturate(140%)`——身后暖砂底 + 颗粒隐约透出，才有纸感玻璃、不塑料
- **亮边**：`border: 1px solid rgba(255,255,255,0.82)`（近白高光边，比灰描边脆、有玻璃厚度）
- **柔暖投影 + 玻璃内高光**：`box-shadow: 0 18px 36px -24px rgba(74,54,20,0.12), 0 2px 8px -6px rgba(74,54,20,0.05), inset 0 1px 0 rgba(255,255,255,0.7)`——投影用**暖棕**基（`74,54,20`）不是冷黑；`inset` 顶内高光让玻璃「有厚度」
- **顶 light-leak 高光条**（`::before`）：`inset:0 8% auto · height:1px · linear-gradient(90deg, transparent, rgba(255,255,255,0.95), transparent)`——卡顶一道从中间亮起的细高光，玻璃「漏光」的招牌细节
- **大圆角** `rounded-lg`(16px)
- **暗态转不透明**：`[data-theme='dark']` 下 `background: var(--color-surface)` 且 `backdrop-filter:none`——暗底 blur-through 几乎零收益且会在 hover 重合成时留亮带残影，故去掉玻璃、保留深面 + 柔投影
- 详情页四大区块（顶栏 / 管线轨 / 主工作台 / 发布备料）全是这张卡，视口定高、各自块内滚

## 核心代码

```css
.studio-glass {
  position: relative;
  background: rgba(255, 253, 248, 0.74);
  backdrop-filter: blur(30px) saturate(140%);
  -webkit-backdrop-filter: blur(30px) saturate(140%);
  border: 1px solid rgba(255, 255, 255, 0.82);
  box-shadow:
    0 18px 36px -24px rgba(74, 54, 20, 0.12),
    0 2px 8px -6px rgba(74, 54, 20, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
  border-radius: 16px;
}
.studio-glass::before {
  content: ''; position: absolute; inset: 0 8% auto; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.95), transparent);
  pointer-events: none;
}
:root[data-theme='dark'] .studio-glass {
  background: var(--color-surface); backdrop-filter: none;
}
```

```tsx
<section className="studio-glass rounded-lg p-4">…</section>
```

## 适配指南

- 玻璃只在**有氛围底 + 颗粒**的暖砂场景成立（[[warm-paper-grain]]）——纯白平底上用玻璃=看不出、白费 backdrop-filter
- 投影务必用暖棕基 `rgba(74,54,20,·)` 不是冷黑，才与暖砂同温
- 一屏别铺太多张玻璃卡叠玻璃卡（模糊叠模糊会浑）；本例是「四大区块各一张、互不重叠」
- 暗态一定去 `backdrop-filter`（残影 + 零收益）

## 反模式

- 不要纯白不透明当「玻璃」（要真半透 + blur 透出身后）
- 不要冷黑投影（要暖棕，否则与暖砂割裂）
- 不要满屏毛玻璃兜底——玻璃是这套的 signature 承载件，但靠氛围底衬托，不是越多越好
