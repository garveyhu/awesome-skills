---
id: components/feedback/chameleon/neon-loader
type: component
name: 霓虹 AI Loader
description: 紫→品红→青 conic-gradient 旋转环（mask 中空 + 双层 drop-shadow 辉光）+ 流光渐变文字 + 可选呼吸辉光底，4 档尺寸
platforms:
- web
theme: light
tags:
  aesthetic:
  - industrial
  mood:
  - confident
  - energetic
  stack:
  - shadcn-radix
uses:
- tokens/motion/chameleon/neon-ai-suite
preview: /preview/components/feedback/chameleon/neon-loader
---

# Chameleon 霓虹 AI Loader

> 站点的 AI signature moment——长耗时 AI 任务（评测 / 分析 / 对比 / 扩样 / 优化 / 生图 / playground「思考中…」）通用的 loading。紫 `#8b5cf6` → 品红 `#d946ef` → 青 `#22d3ee` 的 conic-gradient 旋转环（radial mask 中空成环 + 双层 drop-shadow 辉光）+ 可选流光渐变文字，4 档尺寸（xs 内联按钮 / sm 紧凑 / md 默认 / lg 大面板）。组件经 CSS var `--neon-d`（环直径）/ `--neon-t`（环厚）注入尺寸驱动 `theme.css` 的 `.neon-loader__*` 样式。waveflow keyframes-suite 只有 shimmer/spin/breathe，无 conic 霓虹环——Chameleon 独有的霓虹强调件。

## 视觉特征

- **容器**：`inline-flex items-center gap-2(8px) rounded-lg(8px)`；`glow=true` 时追加 `neon-loader--glow px-3(12px) py-1.5(6px)`
- **旋转环 `.neon-loader__ring`**（`shrink-0`，`aria-hidden`）：
  - `width/height = var(--neon-d)`；`border-radius: 9999px`
  - `background: conic-gradient(from 90deg, transparent 0%, #8b5cf6 35%, #d946ef 55%, #22d3ee 75%, transparent 100%)`
  - `mask: radial-gradient(farthest-side, transparent calc(100% - var(--neon-t)), #000 0)`（中空成环）
  - `filter: drop-shadow(0 0 3px rgba(139,92,246,.85)) drop-shadow(0 0 7px rgba(34,211,238,.5))`（双层辉光）
  - `animation: neon-spin .85s linear infinite`
- **流光文字 `.neon-loader__text`**（`font-medium tracking-wide`）：
  - `background: linear-gradient(90deg, #7c3aed, #d946ef, #22d3ee, #7c3aed)` + `background-size: 200% auto`
  - `background-clip: text; color: transparent`
  - `animation: neon-shimmer 2.6s linear infinite`
- **呼吸辉光底 `.neon-loader--glow`**：
  - `background: rgba(139,92,246,.05)`；`box-shadow: 0 0 0 1px rgba(139,92,246,.22), 0 0 16px rgba(139,92,246,.14)`
  - `animation: neon-breathe 2.4s ease-in-out infinite`（50% 帧切到品红 ring + 青色外晕）
- **4 档尺寸 SIZES**（直径 d / 环厚 t / 字号 text）：
  - `xs { d:12, t:2,    text:'text-[11px]' }`（内联按钮）
  - `sm { d:14, t:2.25, text:'text-[11.5px]' }`（紧凑）
  - `md { d:16, t:2.5,  text:'text-[12px]' }`（默认）
  - `lg { d:24, t:3.25, text:'text-[13.5px]' }`（大面板）

## 核心代码

```tsx
const SIZES = {
  xs: { d:12, t:2,    text:'text-[11px]' },
  sm: { d:14, t:2.25, text:'text-[11.5px]' },
  md: { d:16, t:2.5,  text:'text-[12px]' },
  lg: { d:24, t:3.25, text:'text-[13.5px]' },
};

<div className={cn('inline-flex items-center gap-2 rounded-lg', glow && 'neon-loader--glow px-3 py-1.5')}>
  <span className="neon-loader__ring shrink-0"
        style={{ '--neon-d': `${s.d}px`, '--neon-t': `${s.t}px` }} aria-hidden />
  {label && <span className={cn('neon-loader__text font-medium tracking-wide', textClassName ?? s.text)}>{label}</span>}
</div>
```

```css
.neon-loader__ring {
  background: conic-gradient(from 90deg, transparent 0%, #8b5cf6 35%, #d946ef 55%, #22d3ee 75%, transparent 100%);
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - var(--neon-t)), #000 0);
  filter: drop-shadow(0 0 3px rgba(139,92,246,.85)) drop-shadow(0 0 7px rgba(34,211,238,.5));
  animation: neon-spin .85s linear infinite;
}
.neon-loader__text {
  background: linear-gradient(90deg, #7c3aed, #d946ef, #22d3ee, #7c3aed);
  background-size: 200% auto; -webkit-background-clip: text; color: transparent;
  animation: neon-shimmer 2.6s linear infinite;
}
```

## 适配指南

- 这是全站唯一的霓虹强调件——只用在 AI 长耗时任务，别滥用到普通 loading（普通用 `Loader2` 灰旋转）
- 内联在按钮 / 行内文字旁用 `xs`，紧凑 toolbar 用 `sm`，独立成块的「思考中」面板用 `lg` + `glow`
- `glow` 仅在独立成块时开（有呼吸氛围）；内联场景不开 glow，避免辉光底干扰周边
- 尺寸由 CSS var 注入，加新档只需扩 SIZES，不改 CSS

## 反模式

- ❌ 用在非 AI 场景的普通 loading——霓虹是 AI 语义专属，滥用会冲淡 signature
- ❌ 改 conic 三色为单色蓝——失去霓虹未来感，退化成普通 spinner
- ❌ 去掉双层 drop-shadow——环失去辉光，扁平像普通边框
- ❌ 旋转环不加 `aria-hidden`——纯装饰元素会被读屏念出
