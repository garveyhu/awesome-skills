---
id: blocks/chat/chameleon/markdown-message-citation
type: block
name: 紧凑气泡 Markdown + 引用折叠条
description: react-markdown + remark-gfm 映射成 13.5px 紧凑 Tailwind 样式（a/img 自动识别 .mp4/.webm/.mov → 内联 video），配 RAG 引用 details 折叠条
platforms:
- web
theme: light
tags:
  aesthetic:
  - minimal
  - industrial
  mood:
  - calm
  - serious
  stack:
  - shadcn-radix
uses:
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/chat/chameleon/markdown-message-citation
---

# Chameleon Markdown Message + Citation · 气泡内 Markdown + 引用条

> 两件套：（1）`Markdown` 组件——react-markdown + remark-gfm 把每个元素映射成 **13.5px 紧凑 Tailwind 样式**给 assistant 气泡用，独有点是 `a`/`img` 的 href 自动匹配 `.mp4/.webm/.mov` → 渲染成内联 `<video controls>`，图片 lazy + `max-h-[420px]` 防 reflow；（2）引用折叠条——agent 返回 citation 事件时，气泡下方一列 `<details>`，summary 显示来源标题，展开显示 `line-clamp-3` 片段。

源码：`core/components/chat/markdown.tsx:19-100` · `system/playground/components/message-thread.tsx:250-269`。

## 视觉特征

### Markdown（markdown.tsx）

- **根 div** `text-[13.5px] leading-relaxed break-words`——13.5px 基准专为气泡内紧凑排版
- **p** `mb-2(8) last:mb-0`
- **ul** `mb-2 list-disc space-y-0.5(2) pl-5(20) last:mb-0`；**ol** `list-decimal`，li `leading-relaxed`
- **a** `text-sky-600(#0284c7) underline underline-offset-2 target=_blank`
- **video**（由 `a`/`img` href 匹配 `/\.(mp4|webm|mov)(\?|$)/i` 触发）`my-1 max-h-[420px] max-w-full rounded-lg(8) border border-stone-200`
- **img** `my-1 max-h-[420px] max-w-full rounded-lg border border-stone-200 object-contain loading=lazy`
- **strong** `font-semibold`；**em** `italic`
- **h1** `mt-1 mb-1.5 text-[15px] font-semibold`；**h2** `text-[14px]`；**h3** `mt-1 mb-1 text-[13px]`
- **blockquote** `mb-2 border-l-2 border-stone-300(#d6d3d1) pl-2 text-stone-500`
- **code (inline)** `rounded bg-stone-100(#f5f5f4) px-1 py-0.5 font-mono text-[0.85em] text-stone-800`
- **pre** `mb-2 overflow-x-auto rounded-md(6) bg-stone-100 p-2.5(10) font-mono text-[12px]`，`[&>code]:bg-transparent [&>code]:p-0`
- **table** 外包 `mb-2 overflow-x-auto`，table `w-full border-collapse text-[12px]`；th/td `border border-stone-200 px-2 py-1`，th `text-left font-medium`
- **hr** `my-2 border-stone-200`

### 引用折叠条（message-thread.tsx）

- **容器** `max-w-full space-y-1 px-1`
- **每条 details** `rounded-md border border-stone-200 bg-stone-50/80 px-2 py-1 text-[11px] text-stone-600`
- **summary** `cursor-pointer select-none truncate text-stone-500`「📄 标题 / 来源 / 引用 N」（纯 📄 emoji + 标题，无 chevron / 无 FileText）
- **片段** `mt-1 line-clamp-3 whitespace-pre-wrap text-stone-500`

## 核心代码

```tsx
// markdown.tsx —— a/img href 匹配视频后缀 → 内联 <video>
const IS_VIDEO = /\.(mp4|webm|mov)(\?|$)/i;
a: ({ children, href }) =>
  href && IS_VIDEO.test(href)
    ? <video src={href} controls className="my-1 max-h-[420px] max-w-full rounded-lg border border-stone-200" />
    : <a href={href} target="_blank" rel="noreferrer" className="text-sky-600 underline underline-offset-2">{children}</a>,
img: ({ src, alt }) =>
  typeof src === 'string' && IS_VIDEO.test(src)
    ? <video src={src} controls className="my-1 max-h-[420px] max-w-full rounded-lg border border-stone-200" />
    : <img src={src} alt={alt} loading="lazy" className="my-1 max-h-[420px] max-w-full rounded-lg border border-stone-200 object-contain" />,
```

```tsx
// citation 折叠条
<div className="max-w-full space-y-1 px-1">
  {msg.citations.map((c, i) => (
    <details key={i} className="rounded-md border border-stone-200 bg-stone-50/80 px-2 py-1 text-[11px] text-stone-600">
      <summary className="cursor-pointer select-none truncate text-stone-500">📄 {c.title || c.source || `引用 ${i + 1}`}</summary>
      {c.snippet && <div className="mt-1 line-clamp-3 whitespace-pre-wrap text-stone-500">{c.snippet}</div>}
    </details>
  ))}
</div>
```

## 适配指南

- 只接 `content: string`，不透传 `node`（避免无效 DOM 属性告警）
- 链接走 sky-600（信息蓝）而非主操作 blue-600——区分「正文链接」与「按钮」语义
- 代码 / 引用 / 表格全走暖灰底（stone-100 / stone-50）而非默认冷灰——呼应暖白基底
- 图片必须 `loading=lazy` + `max-h-[420px]`——气泡内大图不约束会撑爆 + 加载抖动
- 引用条与 widget / 编辑器调试同水位（同款 details 样式）

## 反模式

- ❌ 用默认 react-markdown 样式——行距 / margin 太松，气泡内显得空荡
- ❌ 正文链接用 blue-600——和发送按钮主色撞，链接专用 sky-600
- ❌ 图片不限高——大图撑爆气泡、加载时 reflow 抖动
- ❌ 引用条用框型卡而非 `<details>`——多条引用占满气泡，必须可折叠
