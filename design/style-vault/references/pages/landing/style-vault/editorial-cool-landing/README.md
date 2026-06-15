---
id: pages/landing/style-vault/editorial-cool-landing
type: page
name: 编辑感冷调落地页
description: Hero（双 blob）→ Logo 墙 → 3 段 01/02/03 大字叙事 → Manifesto 暗底 → Footer
platforms: [web]
theme: light
tags:
  aesthetic: [minimal, editorial]
  mood: [calm, cold, confident]
  stack: [react-antd-tailwind]
preview: /preview/pages/landing/style-vault/editorial-cool-landing
---

# Editorial Cool Landing

> Style Vault HomePage 的完整骨架 —— 五段堆叠的纯宣传落地页

## 视觉特征 · 五段结构

```
┌────────────────────────────────────────┐
│ 1. Hero（占首屏 100vh）                 │ ← 双 blob + fade-up cascade + dark CTA
│    blocks/marketing/style-vault/cool-blob-hero
├────────────────────────────────────────┤
│ 2. Logo 墙（slate-50 底 + 灰度排列）     │ ← 纯展示，不可点
├────────────────────────────────────────┤
│ 3. 价值点叙事 · 3 段                    │
│    01 / 02 / 03 大字 + 副文 + SVG 插图   │ ← 奇偶 flip 双列
├────────────────────────────────────────┤
│ 4. Manifesto（slate-900 暗底反白）       │ ← 大字 + cyan-300 italic 强调
├────────────────────────────────────────┤
│ 5. Footer（极简一行）                    │
└────────────────────────────────────────┘
```

### 1. Hero

直接套 `blocks/marketing/style-vault/cool-blob-hero`，无变化。

### 2. Logo 墙

- 底色 `bg-slate-50`，`border-y border-slate-100`
- 高度 `py-16`，居中
- caption `text-[11px] uppercase tracking-[0.28em] text-slate-400` "覆盖完整的美学光谱 · Curated aesthetic range"
- logo 排列：`flex flex-wrap items-center justify-center gap-x-12 gap-y-6 opacity-60` —— **不是真 logo 图，而是 font-display 文字 logo 排列**（取自 registry 真实条目名）
- 每条 `font-display text-[20px] font-medium tracking-[-0.01em] text-slate-600`

### 3. 价值点叙事 · 3 段

容器 `mx-auto max-w-[1200px] px-8 py-32` + `space-y-36`（**段间距巨大**，编辑感来源）

每段 `<ValueBlock>`：
- 双列 grid `grid-cols-1 md:grid-cols-2 gap-14 md:gap-20`
- 奇偶 flip：第二段 `md:[&>*:first-child]:order-last`
- 左列：mono 索引号 `01/02/03` + h2 标题 + 副文
  - 索引：`font-mono text-[13px] tracking-widest text-slate-400`
  - 标题：`font-display text-[44px] font-semibold leading-[1.08] tracking-[-0.025em] text-slate-900`
  - 副文：`text-[16px] leading-[1.75] text-slate-500 max-w-[480px]`
- 右列：纯 SVG / CSS 插图（`LayerStack` / `PromptPayload` / `PlatformTrio`），保持品牌调性

### 4. Manifesto

- 底色 `bg-slate-900`，文字 `text-white`，`border-y border-slate-100`
- 装饰：cyan-500/10 + slate-500/15 两颗弱 blob（透明度更低于 hero blob）
- 大字 `font-display text-[40px] md:text-[52px] font-medium leading-[1.2] tracking-[-0.015em]`
- 关键词用 `italic text-cyan-300` 包裹（"看见" / "记住"）—— **唯一允许 italic 的地方**
- 底部 caption `text-[11px] uppercase tracking-[0.28em] text-slate-400`

### 5. Footer

- 底色 `bg-white`，`flex items-center justify-between px-12 py-5`
- 左：logo 5×5 + 站名 `font-display text-[14px] font-medium text-slate-500`
- 右：版权 + 1px 分隔 + GitHub 文字链
- 整体 `text-[12px] text-slate-400` —— 极简

## 适配指南

- 五段都靠 `border-y border-slate-100` 切割，不用 padding 撑开 —— hairline 是身份
- 段间距宁可 `py-32 / space-y-36`，**不要**收紧到 `py-16`（编辑感来自呼吸）
- Manifesto 暗底是全站唯一大面积 dark —— 不要在其它段重复
- 装饰插图建议保留**纯 SVG / CSS**实现，不引图片（pixel-perfect + 主题切换无障碍）

## 反模式

- 不要插入 testimonial / 客户评价 / pricing —— 落地页是宣言，不是销售页
- 不要把 Logo 墙换成真彩色 logo —— 灰度文字 logo 是冷感落地的特征
- 不要给价值段加 hover 卡片化 —— 编辑感的对话感会丢
- 不要 manifesto 额外加 CTA —— 让 hero 唯一 CTA 站住
