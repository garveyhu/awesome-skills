---
id: blocks/media/studio-board/work-card
type: block
name: 频道作品卡
description: 首页作品网格卡——纸感封面 + 右上发布状态点(绿/灰) + hover 浮起「预览」眼睛 pill + 标题 line-clamp + 播放量·日期 mono meta
platforms: [web]
theme: light
tags:
  aesthetic: [editorial, minimal]
  mood: [warm, calm]
  stack: [react-tailwind]
uses:
  - tokens/palettes/studio-board/warm-sand-ink
  - tokens/motion/studio-board/liquid-ease
preview: /preview/blocks/media/studio-board/work-card
---

# 频道作品卡

> 首页频道 board 的作品网格单元：封面 + 标题 + 播放量/日期，右上一颗发布状态点，hover 从封面角浮起「预览」pill（观众视角弹层入口）。

## 视觉特征

- **封面**：`Cover` 组件——`relative overflow-hidden bg-ink rounded-lg`，图 `object-cover` 满格不裁；无图时走 `linear-gradient(150deg, hsl(h 20% 34%), hsl(h+28 24% 19%))`（按 slug hash 取色）+ 居中标题白字
- **发布状态点**（封面右上）：`absolute right-2 top-2 h-2.5 w-2.5 rounded-full ring-2 ring-white/70`——已发布=苔绿 `var(--sb-mint)`、未发布=中性冷灰 `#8a8f98`（未发布不用蓝/暖：小尺寸难分、黄封面上暖色发糊，中性 slate 黄底深底都清晰）
- **hover「预览」pill**（封面左上角，`WorkCard` 壳）：`bg-ink/85 text-white rounded-full px-3 py-1.5 text-[11px] font-black backdrop-blur-sm` + `shadow-[0_3px_12px_rgba(0,0,0,0.28)]`，内含**苔绿眼睛** SVG；默认 `opacity-0 translate-y-1.5 scale-90`，`group-hover` 浮起为 `opacity-100 translate-y-0 scale-100`，`ease-[var(--ease-standard)]`
- **标题**：`mt-2 line-clamp-2 text-[13px] font-bold leading-snug text-ink`
- **meta**：`mt-1 text-[11px] text-ink-soft`——播放量 + 平台指标名 + `·` + 日期（如 `22.3万 播放 · 7-06 20:00`）
- 整卡点击进工作站；网格 `grid-cols-2 sm:3 lg:4 xl:5 2xl:6 · gap-x-4 gap-y-6`

## 核心代码

```tsx
<div className="group relative">
  <Link to={`/c/${slug}`} className="block no-underline">
    <Cover content={content} ratioKey={ratio} className="w-full" />
    <div className="mt-2 line-clamp-2 text-[13px] font-bold leading-snug text-ink">{title}</div>
    <div className="mt-1 text-[11px] text-ink-soft">{metric} 播放 · {date}</div>
  </Link>
  <button className="absolute left-2 top-2 z-10 inline-flex items-center gap-1.5 rounded-full bg-ink/85 px-3 py-1.5 text-[11px] font-black text-white opacity-0 shadow-[0_3px_12px_rgba(0,0,0,0.28)] backdrop-blur-sm transition-all duration-200 ease-[var(--ease-standard)] group-hover:opacity-100 motion-safe:translate-y-1.5 motion-safe:scale-90 motion-safe:group-hover:translate-y-0 motion-safe:group-hover:scale-100">
    <EyeIcon className="h-3.5 w-3.5 text-mint" /> 预览
  </button>
</div>
```

## 适配指南

- 发布状态点色随 `success`（苔绿）token；未发布用中性冷灰而非蓝（小尺寸/黄封面上更清晰）
- hover pill 从封面角**浮起**（位移 + 缩放 + 透明度同步），不是简单 fade——阻尼缓动是手感关键
- 各平台格子按自身主封面比例取图（16:9 / 4:3 / 3:4），满格不裁

## 反模式

- 不要 hover 只 fade 无位移（要 translate + scale 浮起）
- 不要未发布点用蓝/暖色（要中性冷灰）
- 不要封面加重描边/圆角不一致（纸感封面靠图本身，卡片克制）
