---
id: blocks/display/style-vault/floating-cover-row
type: block
name: 浮起作品照行卡
description: 宽行卡片 · 左侧渐变底盒里浮起白卡作品照 · 右侧元信息 + 三段 mono 数字徽标
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
  - tokens/motion/style-vault/editorial-flow
preview: /preview/blocks/display/style-vault/floating-cover-row
---

# Floating Cover Row

> 产品列表的视觉签名 —— 380×220 渐变底盒 + 92%×86% 浮起的真实作品缩略

## 视觉特征

**容器**：`grid` 两列 `380px 1fr`，整体 `border border-slate-200/80 rounded-xl bg-white`

**左列封面**（380×220，关键视觉）：
- 底盒 `bg-gradient-to-br from-slate-50 via-white to-slate-100/60` —— 三色冷感渐变托底
- 内层浮起白卡 92%×86%（即 ~350×189），`bg-white border border-slate-200 rounded-lg shadow-[0_8px_24px_-10px_rgba(15,23,42,0.22)]`
- 白卡里再缩 `1440×900` 真实预览（`scale = 350/1440 ≈ 0.243`）
- 这种"渐变底 → 浮起白卡 → 缩略组件"三层叠是 style-vault 产品列表的视觉签名

**右列元信息**：
- 顶行：category-dot（按 product.category 切色：productivity=purple / design=indigo / ...）+ category 文字 + platform · 右侧收藏 icon-only
- 标题 `font-display text-[20px] font-semibold` + 描述 `text-[13px] line-clamp-2 text-slate-600`
- 底部三段 mono 数字徽标：`PAGES N · BLOCKS N · COMPONENTS N` —— `font-mono tracking-wider`
- 最右 `查看 →` 文字链 group-hover slate-700

**hover**：用 `.sv-card` 卡片浮起（translateY -4 + 三层投影）

## 核心代码骨架

```tsx
<article className="sv-card group relative block w-full cursor-pointer overflow-hidden rounded-xl border border-slate-200/80 bg-white">
  <div className="grid" style={{ gridTemplateColumns: '380px 1fr' }}>
    {/* 封面 · 渐变底 + 浮起白卡 */}
    <div className="relative flex items-center justify-center bg-gradient-to-br from-slate-50 via-white to-slate-100/60" style={{ height: 220 }}>
      <div ref={previewRef}
           className="relative overflow-hidden rounded-lg border border-slate-200 bg-white shadow-[0_8px_24px_-10px_rgba(15,23,42,0.22)]"
           style={{ width: '92%', height: '86%' }}>
        <div className="pointer-events-none absolute origin-top-left"
             style={{ width: 1440, height: 900, transform: `scale(${scale})` }}>
          <CoverComp />
        </div>
      </div>
    </div>

    {/* 信息 */}
    <div className="flex flex-col justify-between p-6">
      <div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-[10px] uppercase tracking-[0.12em] text-slate-500">
            <span className="h-1.5 w-1.5 rounded-full" style={{ background: categoryDot(product.category) }} />
            {categoryLabel(product.category)} · {platformLabel(...)}
          </div>
          <FavBtn />
        </div>
        <h3 className="mt-2 font-display text-[20px] font-semibold leading-tight">{product.name}</h3>
        <p className="mt-2 line-clamp-2 text-[13px] text-slate-600">{product.description}</p>
      </div>
      <div className="mt-4 flex items-center gap-6 text-[11px] text-slate-400">
        <span className="font-mono tracking-wider">PAGES <span className="text-slate-700">{n}</span></span>
        <span className="font-mono tracking-wider">BLOCKS <span className="text-slate-700">{n}</span></span>
        <span className="font-mono tracking-wider">COMPONENTS <span className="text-slate-700">{n}</span></span>
        <span className="ml-auto text-[12px] text-slate-900 group-hover:text-slate-700">查看 →</span>
      </div>
    </div>
  </div>
</article>
```

## 适配指南

- **必须**保留"渐变底 + 浮起白卡 + 真实缩略"三层结构 —— 这是产品集列表的身份特征，去掉任何一层都变成普通行卡
- 浮起白卡阴影必须 `shadow-[0_8px_24px_-10px_rgba(15,23,42,0.22)]` 单层中距离 —— 不要堆三层（那是卡片浮起的领地）
- 三段 mono 数字徽标 KEY 用 `text-slate-400`，VALUE 用 `text-slate-700` —— 双色对比是数字的层级语言
- 当 `coverItem` 缺失时，浮起白卡里显示 `repeating-linear-gradient` 斜纹占位（保留三层结构）

## 反模式

- 不要把封面区改成图片背景 cover —— 浮起白卡是视觉重心
- 不要把"PAGES / BLOCKS / COMPONENTS"汉化 —— mono uppercase 是数字语义的载体
- 不要把右侧"查看 →"换成 button —— 文字链是 editorial 节奏
- 不要把行卡间隔 < `gap-4`（16px）—— 浮起卡片之间需要呼吸
