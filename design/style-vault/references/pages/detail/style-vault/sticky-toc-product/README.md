---
id: pages/detail/style-vault/sticky-toc-product
type: page
name: Sticky TOC 产品详情页
description: Cover Hero（双 blob + 主 CTA）+ 88px 窄 sticky 数字 TOC + masonry 分段（pages / blocks / components / tokens）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, confident]
  stack: [react-antd-tailwind]
preview: /preview/pages/detail/style-vault/sticky-toc-product
---

# Sticky TOC Product Detail

> ProductDetailPage 的完整骨架——产品聚合页的"目录式"展开

## 视觉特征

```
┌─────────────────────────────────────────┐
│ Cover Hero                              │ ← 双 blob 装饰 + 复制 Prompt 主 CTA
├─────────────────────────────────────────┤
│ ┌────┐ ┌──────────────────────────────┐ │
│ │88px│ │ 01 设计风格 · 单 preview     │ │
│ │ 数 │ │ 02 页面 · masonry 列         │ │
│ │ 字 │ │ 03 模块 · masonry 列         │ │
│ │TOC │ │ 04 组件 · masonry 4 列       │ │
│ │    │ │ 05 原语 · 2 列               │ │
│ │stky│ │                              │ │
│ └────┘ └──────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Cover Hero

- 容器 `relative overflow-hidden border-b border-slate-100 bg-white`
- 双弱 blob（cyan-100/40 400×400 左 + slate-200/50 300×300 右）—— **比 landing 的 hero blob 透明度更低**，避免抢戏
- 内容居中 `mx-auto max-w-[1100px] px-8 pb-20 pt-20 text-center`
- kicker `cyan-dot-meta-pill`：`产品 · {category}`，圆点用 `categoryDot(category)` 切色
- h1 `font-display text-[64px] font-semibold leading-[1.03] tracking-[-0.025em]`
- 副文 `max-w-[640px] text-[17px] leading-relaxed text-slate-500`
- 主 CTA `dark-pill-cta`：`复制 Prompt · 一键复刻整套设计系统`，旁边 FavoriteButton
- 元信息 chip：platform + theme，全 `rounded-full border border-slate-200 bg-white/70 text-[12px]`

### Sticky TOC（左 88px 窄列）

`<aside className="sticky top-24 h-max">`（top-24 对应 96px 留 hero 滚出 + topbar 72px）

```
导航 (uppercase tracking-[0.22em] text-slate-400)

┃ 01 风格      ← 当前 section 高亮：左侧 2px 竖线 + slate-900 字 + slate-500 数字
  02 页面
  03 模块
  04 组件
  05 原语
```

active 检测用 `IntersectionObserver`，rootMargin `-120px 0px -60% 0px`：滚到 section 头部（视口上方 120px）就激活，下方 60% 缓冲避免快速滚动跳变。

数字用 `font-mono` 13px，激活态 slate-500 / 普通 slate-300（两态对比 = 编辑感锚点）。

### Body sections（右列 1fr）

`grid` 两列 `gridTemplateColumns: '88px 1fr'` + gap-10。每段 `<article>` 头部：

```jsx
<div className="flex items-baseline gap-4">
  <span className="font-mono text-[12px] text-slate-400">01</span>
  <h2 className="font-display text-[26px] font-semibold">设计风格</h2>
  <span className="text-[13px] text-slate-400">· {count}</span>
</div>
```

各段卡片用 `PreviewOnlyCard`（自然高度的虚拟视口缩放）：
- **风格段**：单 preview 铺满
- **页面段**：`columns-2 lg:columns-3` masonry
- **模块段**：`columns-2 lg:columns-3` masonry
- **组件段**：`columns-2 md:columns-3 lg:columns-4` masonry（更密）
- **原语段**：`columns-1 md:columns-2`，最大宽 `max-w-[760px]`

### PreviewOnlyCard（核心交互）

每张卡有两个独立交互：
- **点缩略图** → 跳详情页 `/item/{id}`
- **点 caption 名字** → 弹 `PreviewPeekModal` 快速预览（同页 modal，不离开 product 上下文）

caption 形态：`text-[11px] text-slate-500` + `1px slate-400` 圆点前缀，hover 整块 `bg-slate-100/70 text-slate-700`

### PreviewPeekModal

- 全屏遮罩 `bg-slate-950/40 backdrop-blur-sm`
- 卡片 `max-w-[1180px] rounded-2xl ring-1 ring-slate-200`
- header：mono uppercase `{type} · {id}` + 大字标题 + 描述
- body：自然高度按虚拟视口缩放
- footer：`按 ESC 关闭`（mono caption） + `查看完整详情 →`（链接）
- 锁滚动 `body.style.overflow = hidden`，ESC 关闭

## 适配指南

- 88px TOC 宽度是数字 + 中文 1-2 字 + padding 的紧凑阈值——**不要**撑到 120px+（破坏"窄列"对比）
- masonry 用 CSS columns 而非 grid—— grid 不支持 PreviewOnlyCard 的自然高度
- IntersectionObserver `rootMargin` 必须 `-120px 0px -60% 0px`——少了上方触发会过早，下方少了快速滚动会跳
- 每段可见的 active dot **左侧 2px 竖线** 而不是 background —— editorial 节奏

## 反模式

- 不要给 TOC 加 background hover——左竖线 + 字色变化已足
- 不要把 hero 设计复用 cool-blob-hero（更亮 blob）——detail 比 landing 弱一档
- 不要把 PreviewOnlyCard 改成 grid（破坏 masonry 自然高度感）
- 不要在 detail 页加二级 nav——单层 sticky TOC 是这一页的语言
