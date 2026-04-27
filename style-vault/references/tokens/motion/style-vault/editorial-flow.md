---
id: tokens/motion/style-vault/editorial-flow
type: token
name: Editorial Flow Motion
description: cubic-bezier(0.2, 0.7, 0.2, 1) + 阶梯 fade-up + 卡片浮起 + 长周期 blob drift + 入场延迟序列
platforms: [any]
theme: both
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind, html-tailwind]
preview: /preview/tokens/motion/style-vault/editorial-flow
---

# Editorial Flow

> 一条标志曲线 + 阶梯入场 + 卡片浮起 + 慢周期装饰 = 编辑感不浮夸的动效系统

## 视觉特征

**单一 easing**：`cubic-bezier(0.2, 0.7, 0.2, 1)`——前期快速发力 + 末尾轻微减速，比 `ease-out` 更有"克制感"。除 blob ease-in-out 与 toast spring 两处例外，**全站走这条曲线**。

**入场分层 fade-up**：hero / 标题级元素入场时按内容重要性分阶——0ms (kicker) → 150ms (主标题) → 300ms (副文) → 500ms (CTA)，每条 `translateY(16px) → 0 + opacity 0 → 1`，duration `0.9s`。

**卡片浮起**：`.sv-card:hover` 三参数同步过渡（transform / box-shadow / border-color）400ms，`translate3d(0,-4px,0)` + 多层柔投影替代描边变化。**预览图同步 scale 1.05** 600ms（origin-top-center），让缩略图"放大里面而非外框"。

**列表行动效**：`sv-text-link`（查看更多）下划线 hover scaleX 0.35 → 1，260ms；箭头 `translateX(4px)` 220ms。

**toast 入场**：例外用 spring `cubic-bezier(0.34, 1.56, 0.64, 1)` 320ms——只此一处用回弹。

## Tokens

```json
{
  "easing": {
    "signature": "cubic-bezier(0.2, 0.7, 0.2, 1)",
    "blob":      "ease-in-out",
    "toast":     "cubic-bezier(0.34, 1.56, 0.64, 1)"
  },
  "duration": {
    "fast":  "200ms",
    "base":  "260ms",
    "slow":  "400ms",
    "hero":  "900ms",
    "blob":  "14s / 18s",
    "toast": "320ms"
  },
  "fade-up": {
    "from":   { "opacity": 0, "transform": "translate3d(0,16px,0)" },
    "to":     { "opacity": 1, "transform": "translate3d(0,0,0)" },
    "delays": [0, 75, 150, 225, 300, 400, 500, 600]
  },
  "card-lift": {
    "transform":  "translate3d(0,-4px,0)",
    "duration":   "400ms",
    "shadow":     "0 2px 6px -1px rgba(15,23,42,0.06), 0 14px 32px -10px rgba(15,23,42,0.22), 0 24px 48px -20px rgba(15,23,42,0.14)",
    "preview-scale": "1.05",
    "preview-origin": "top center",
    "preview-duration": "600ms"
  },
  "tab-underline": {
    "rest":     { "transform": "scaleX(0)" },
    "active":   { "transform": "scaleX(1)", "transformOrigin": "left center", "duration": "320ms" },
    "fill":     "linear-gradient(90deg, #0891b2, #0f172a)"
  },
  "text-link": {
    "underline-hover": { "from-scaleX": 0.35, "to-scaleX": 1, "duration": "260ms" },
    "arrow-hover":     { "transform": "translateX(4px)", "duration": "220ms" }
  }
}
```

## 适配指南

- 全局 transition 默认 `transition: all 260ms cubic-bezier(0.2, 0.7, 0.2, 1);`——任何不在上面表里的元素都用这个
- 入场动画用 CSS 类 `.sv-anim-fade-up.sv-delay-{0|150|300|500}` 组合 —— **8 个固定延迟槽**（0/75/150/225/300/400/500/600），不要写硬编码 ms
- 卡片浮起的 box-shadow 是**三层叠加**（近距离 + 中距离 + 远距离）——单层 shadow 会显得机械
- toast 是**唯一**允许回弹的元素——overshoot 1.56 让胶囊"钻"出顶部
- blob drift 周期 ≥ 14s——更短会变焦虑

## 反模式

- 不要用 `ease-in-out` 做交互（只 blob 可以）
- 不要给卡片 hover 加 `scale(1.02)` 整卡放大——本系统是"卡片浮起 + 内容放大"分离
- 不要把 fade-up 改成 fade-in（少了 16px translateY 就丢了"翻页"质感）
- 不要堆超过 6 级延迟（hero 一组通常 3-4 级足够）
- 不要为按钮 hover 加 transform——只用 background-color 切换
