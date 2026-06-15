---
id: blocks/marketing/style-vault/cool-blob-hero
type: block
name: 冷感漂浮 Hero
description: 全屏 hero · 双 blob 漂浮 + 三段 fade-up cascade + 渐变 bg-clip 标题 + dark pill CTA
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, cold, confident]
  stack: [react-antd-tailwind, html-tailwind]
uses:
  - tokens/palettes/style-vault/slate-cyan-cool
  - tokens/typography/pairs/style-vault/inter-editorial-display
  - tokens/gradient/style-vault/cool-blob-decor
  - tokens/motion/style-vault/editorial-flow
  - components/tags-badges/style-vault/cyan-dot-meta-pill
  - components/buttons/style-vault/dark-pill-cta
preview: /preview/blocks/marketing/style-vault/cool-blob-hero
---

# Cool Blob Hero

> Style Vault HomePage 第一屏的完整骨架

## 视觉特征

**容器**：`relative overflow-hidden border-b border-slate-100`，最小高 `calc(100vh - 72px)`，内容居中（`flex flex-col items-center justify-center text-center`）

**装饰层**（z-0，pointer-events-none）：
- 左 blob `cyan-100/50` 520x520，`-left-40 -top-40`，`sv-anim-blob` 14s
- 右 blob `slate-200/55` 440x440，`-right-40 top-20`，`sv-anim-blob-slow` 18s
- 都套 `blur-3xl`

**内容层**（relative，z-10），按 fade-up cascade 入场：

1. **kicker**（`sv-delay-0`）—— `cyan-dot-meta-pill`：1.5px cyan dot + "Style Vault · 风格库" uppercase tracking-[0.22em]
2. **主标题**（`sv-delay-150`）—— `font-display text-[64px] md:text-[88px] font-semibold leading-[1.08] tracking-[-0.03em]`
   - 第一行 `text-slate-900` 普通文本
   - 第二行 `bg-gradient-to-br from-cyan-700 via-slate-800 to-slate-900 bg-clip-text text-transparent` —— 这条渐变是 hero 视觉核心
3. **副文**（`sv-delay-300`）—— `text-[17px] leading-[1.8] text-slate-500 max-w-[560px]`，两行换行 `<br />`
4. **CTA**（`sv-delay-500`）—— `dark-pill-cta` lg 档（h-14 px-9 + 大投影）

**入场曲线**：`sv-anim-fade-up` `0.9s cubic-bezier(0.2, 0.7, 0.2, 1) forwards`，`from { opacity: 0; transform: translate3d(0,16px,0); } to { opacity: 1; transform: translate3d(0,0,0); }`

## 核心代码骨架

```tsx
<section className="relative overflow-hidden border-b border-slate-100">
  {/* blobs */}
  <div className="pointer-events-none absolute -left-40 -top-40 h-[520px] w-[520px] rounded-full bg-cyan-100/50 blur-3xl sv-anim-blob" />
  <div className="pointer-events-none absolute -right-40 top-20 h-[440px] w-[440px] rounded-full bg-slate-200/55 blur-3xl sv-anim-blob-slow" />

  <div className="relative mx-auto flex min-h-[calc(100vh-72px)] max-w-[1200px] flex-col items-center justify-center px-8 py-24 text-center">
    {/* 1. kicker */}
    <div className="sv-anim-fade-up sv-delay-0 inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white/85 px-3 py-1 text-[11px] font-medium uppercase tracking-[0.22em] text-slate-500 backdrop-blur-sm">
      <span className="h-1.5 w-1.5 rounded-full bg-cyan-500" />
      Style Vault · 风格库
    </div>

    {/* 2. headline */}
    <h1 className="sv-anim-fade-up sv-delay-150 mt-8 max-w-[1000px] font-display text-[64px] font-semibold leading-[1.08] tracking-[-0.03em] text-slate-900 md:text-[88px]">
      为 AI 编码而造的
      <br />
      <span className="bg-gradient-to-br from-cyan-700 via-slate-800 to-slate-900 bg-clip-text text-transparent">
        设计风格库
      </span>
    </h1>

    {/* 3. body */}
    <p className="sv-anim-fade-up sv-delay-300 mx-auto mt-8 max-w-[560px] text-[17px] leading-[1.8] text-slate-500">
      六个层级，六道清晰边界。
      <br />复刻一种成熟的视觉风格，只需把一段 Prompt 贴给 AI。
    </p>

    {/* 4. CTA */}
    <div className="sv-anim-fade-up sv-delay-500 mt-12">
      <DarkPillCta size="lg">进入风格库</DarkPillCta>
    </div>
  </div>
</section>
```

## 适配指南

- 占满首屏 = `min-h-[calc(100vh-72px)]`（72px 是 TopBar 高度）；嵌入子页时改 `min-h-[600px]`
- 主标题渐变可换语义但**不要**换色相——cyan→slate 这套是身份
- 副文必须显式 `<br />` 换行——视觉节奏靠这两段呼吸控制
- CTA 必须 lg 档（带大投影），sm/md 在 hero 太小

## 反模式

- 不要 hero 里塞双 CTA（次 CTA 会和 dark-pill 抢戏；ghost 太弱）
- 不要把 blob 颜色换暖色——破坏冷感
- 不要给 hero 加 video 背景（noisy，与冷感不符）
- 不要把入场动画 delay 缩到 < 75ms 的间隔——cascade 节奏会丢
