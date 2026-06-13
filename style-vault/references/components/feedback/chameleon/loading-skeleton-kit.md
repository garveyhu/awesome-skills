---
id: components/feedback/chameleon/loading-skeleton-kit
type: component
name: 占位骨架套件 + 生图等待态
description: Skeleton/SkeletonText/SkeletonCard 暖灰 shimmer 占位三件套 + 4:3 文生图等待态（图标 + 旋转徽标 + mm:ss 计时）
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  mood:
  - calm
  stack:
  - shadcn-radix
uses:
- tokens/motion/waveflow/keyframes-suite
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/components/feedback/chameleon/loading-skeleton-kit
---

# Chameleon 占位骨架套件 + 生图等待态

> 两组占位件共用 waveflow 全局 `.skeleton` 暖灰横向 shimmer 渐变波。其一是基础三件套 `Skeleton`（可控宽高 + 5 档圆角）/ `SkeletonText`（多行 + 末行 60% 短宽 pill）/ `SkeletonCard`（可选圆头像 + 多行）；其二是 `ImageGenLoading`——本地 ComfyUI 出图 ~1 分钟的高级等待态：4:3 骨架流光框 + 居中 ImageIcon + 右下角旋转 Loader2 徽标 + mm:ss 计时，替代逐行打印 SSE 文字的廉价进度。

## 视觉特征

### Skeleton 基础件

- **`.skeleton` 全局类**：`linear-gradient(90deg, #ebe9e3 0%, #f5f4ee 50%, #ebe9e3 100%)` + `background-size: 400px 100%` + `animation: shimmer 1.6s ease-in-out infinite`（暖灰横向流光，亮端 `#f5f4ee` 暗端 `#ebe9e3`）
- **Skeleton**：`<div className="skeleton {rounded}">` + `style={{ width, height }}`；rounded 5 档映射 `rounded-none / -sm(2px) / -md(6px) / -lg(8px) / -full`，默认 `md`
- **SkeletonText**：`flex flex-col` + `style.gap=gap`(默认 8px)；`lines` 默认 3，每行 `height=lineHeight`(默认 10px) `rounded="full"`，宽度 = 末行 `${lastLineWidth*100}%`(默认 0.6 → 60%) 其余 `100%`
- **SkeletonCard**：`flex flex-col gap-3(12px) rounded-lg(8px) border border-stone-200/60 bg-paper p-4(16px)`；`avatar` 时顶部 `flex items-center gap-3(12px)` + `Skeleton 36×36 rounded-full` + `flex-1` 内 `Skeleton h10 w-40% rounded-full`，下接 `SkeletonText lines`

### ImageGenLoading 生图等待态

- **框**：`skeleton relative flex aspect-[4/3] w-full flex-col items-center justify-center gap-2.5(10px) rounded-xl(12px) border border-stone-200`
- **图标组**：`<ImageIcon className="h-9 w-9(36px) text-stone-300"/>` + 右下角 `absolute -right-2 -bottom-2 flex h-5 w-5(20px) items-center justify-center rounded-full bg-white shadow-sm` 内含 `<Loader2 className="h-3.5 w-3.5(14px) animate-spin text-violet-500(#8b5cf6)"/>`
- **标题**：`text-[13px] font-medium text-stone-600` 「正在生成图片」
- **计时**：`font-mono text-[12px] tabular-nums text-stone-400`，格式 `m:ss`（`setInterval` 250ms 刷新，`Math.floor(elapsed/60):pad2(elapsed%60)`）
- **hint**：`max-w-[80%] text-center text-[11px] leading-snug text-stone-400`（仅 hint 传入时渲染）

## 核心代码

```tsx
const ROUNDED = { none:'rounded-none', sm:'rounded-sm', md:'rounded-md', lg:'rounded-lg', full:'rounded-full' };

<div className={cn('skeleton', ROUNDED[rounded], className)} style={{ width, height }} />

// 末行短宽 pill
<Skeleton height={lineHeight} width={i === lines-1 ? `${lastLineWidth*100}%` : '100%'} rounded="full" />

// 生图等待态：计时 250ms 刷新
const label = `${Math.floor(elapsed/60)}:${String(elapsed%60).padStart(2,'0')}`;
<div className="skeleton relative flex aspect-[4/3] w-full flex-col items-center justify-center gap-2.5 rounded-xl border border-stone-200">
  <div className="relative">
    <ImageIcon className="h-9 w-9 text-stone-300" />
    <span className="absolute -right-2 -bottom-2 flex h-5 w-5 items-center justify-center rounded-full bg-white shadow-sm">
      <Loader2 className="h-3.5 w-3.5 animate-spin text-violet-500" />
    </span>
  </div>
  <div className="text-[13px] font-medium text-stone-600">正在生成图片</div>
  <div className="font-mono text-[12px] tabular-nums text-stone-400">{label}</div>
</div>
```

## 适配指南

- 列表加载用 `SkeletonCard avatar` × N，撑住布局高度防内容到位时跳动
- 生图 / 图生视频等待态用 `ImageGenLoading`，`hint="首次含模型加载可能数分钟"` 给用户耐心预期
- 计时用 `font-mono tabular-nums` 让数字定宽，跳秒时不抖动——这是「专业等待」的关键细节
- shimmer 复用全局 `.skeleton`，不要在组件里另写 keyframes——同站所有骨架同一道流光波

## 反模式

- ❌ 末行不收窄到 60%——满宽多行看不出是「文字」骨架，像色块
- ❌ 生图等待用纯 spinner 不给计时——长耗时任务不显时长，用户以为卡死
- ❌ 计时用变宽数字字体——跳秒时宽度抖动，廉价
- ❌ 徽标 Loader2 用主题蓝——这里刻意用 `violet-500` 标记「AI 生成」语义
