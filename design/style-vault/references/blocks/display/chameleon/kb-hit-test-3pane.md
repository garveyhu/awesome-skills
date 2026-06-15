---
id: blocks/display/chameleon/kb-hit-test-3pane
type: block
name: 检索命中测试三栏面板
description: 左参数(query/topK/召回模式/多查询/标签元数据过滤) / 中命中 chunk 卡(rank + 文档 + 分项得分 + 摘要) / 右选中原文(关键词高亮) + 分项得分 - RAG 召回调试 amber 强调
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
- components/display/chameleon/distribution-score-bars
- tokens/palettes/waveflow/warm-paper-ink-blue
preview: /preview/blocks/display/chameleon/kb-hit-test-3pane
---

# 检索命中测试三栏面板

> RAG 召回调试面：**①参数**（query textarea + topK range + 召回模式 select + 多查询 switch + 标签/元数据过滤 + 搜索按钮）、**②命中 chunk 卡**（rank + 文档名 + 分项得分条 + 摘要 line-clamp-2）、**③选中原文**（文档名 Link + seq + 全分项得分 + 关键词高亮原文）。amber 是命中/选中态的强调色。waveflow 无 KB，全新。

## 视觉特征

- **网格**：`grid grid-cols-1 gap-3 lg:grid-cols-[260px_minmax(0,1fr)_minmax(0,1.05fr)]`（参数 260px 固定 / 命中列表 1fr / 原文 1.05fr）
- **① 参数栏**（`space-y-3`）：
  - Field label：`mb-1 block text-[12px] text-stone-600`
  - query：Textarea `rows={5}`
  - top_k range：`w-full accent-amber-600`，label「top_k = N」（N 走 `tnum font-mono`）
  - 召回模式：Select `h-8 text-[12.5px]`（向量/混合/关键词）
  - 多查询扩展：`flex items-center justify-between gap-2 text-[12px] text-stone-600` + Switch
  - 标签过滤：Input `h-8 text-[12.5px]`
  - 元数据过滤：每行 `flex items-center gap-2`，标签 `w-16 shrink-0 truncate text-[11px] text-stone-500` + Select/Input `h-7 text-[11.5px]`
  - 搜索：Button `w-full` + `Search h-3.5 w-3.5`
- **② 命中列表**（`min-h-[280px] space-y-2`）：
  - HitCard：`block w-full rounded-lg border bg-white p-2.5 text-left transition`，active `border-amber-300 ring-1 ring-amber-200` / 未选 `border-stone-200/70 hover:border-amber-200`
    - 头 `mb-1.5 flex items-center gap-2 text-[11px] text-stone-500`：`#{rank}`（font-mono）+ 文档名 truncate + `ml-auto seq N`（font-mono）
    - ScoreBreakdown compact：`flex flex-wrap items-center gap-x-2.5 gap-y-0.5`，每通道 `text-[10.5px] text-stone-500`「向量」+ 值 `ml-0.5 font-mono tabular-nums text-stone-700` N%
    - 正文 `mt-1.5 line-clamp-2 text-[12px] leading-snug text-stone-700`
- **③ 选中原文**（`rounded-lg border border-stone-200/70 bg-white`，`flex h-full flex-col`）：
  - 头 `border-b border-stone-200/70 p-3`：文档名 Link `truncate font-medium hover:underline` + `ml-auto seq N`（`font-mono text-[10.5px] text-stone-400`）；下方 ScoreBreakdown 全模式
  - ScoreBreakdown 全模式 ChannelRow：`flex items-center gap-2`，标签 `w-16 text-right text-[10.5px] text-stone-500` + 条 `h-1.5 flex-1 overflow-hidden rounded-full bg-stone-100`（向量 `bg-sky-500` / 关键词 `bg-amber-500` / 精排 `bg-violet-500`）+ 值 `w-9 text-right font-mono text-[10.5px] tabular-nums text-stone-600`
  - 原文 `flex-1 overflow-y-auto p-3 text-[12.5px] leading-relaxed whitespace-pre-wrap text-stone-800`，`dangerouslySetInnerHTML` 关键词高亮
- **空态 Centered**：`flex h-full min-h-[240px] flex-col items-center justify-center gap-2 text-stone-400` + `SearchX h-8 w-8 strokeWidth={1.4}` + 文案 `text-[12.5px]`

## 核心代码

```tsx
// ScoreBreakdown 不展示融合「综合」分（RRF 量纲小无区分度），只显各通道原始相似度
const CHANNELS = [
  { key: 'vector_score', short: '向量', bar: 'bg-sky-500' },
  { key: 'bm25_score', short: '关键词', bar: 'bg-amber-500' },
  { key: 'rerank_score', short: '精排', bar: 'bg-violet-500' },
];

// HitCard 选中态
active ? 'border-amber-300 ring-1 ring-amber-200' : 'border-stone-200/70 hover:border-amber-200'

// 全模式 ChannelRow 进度条
<div className="h-1.5 flex-1 overflow-hidden rounded-full bg-stone-100">
  <div className={cn('h-full rounded-full', bar)} style={{ width: `${clampPct(value)}%` }} />
</div>

// 原文关键词高亮
<div className="... whitespace-pre-wrap" dangerouslySetInnerHTML={{ __html: highlight(hit.content, query) }} />
```

## 适配指南

- **不展示融合综合分**：混合模式 RRF 融合分量纲小且彼此接近，无区分度；只显各通道原始分（向量余弦/BM25/精排），排名即综合相关度
- range 用 `accent-amber-600` 染原生滑块；命中/选中态全用 amber（与 chunking-preview、chunk-card-wall 同源调试色）
- 命中卡 compact 一行通道分，选中原文用全模式带进度条，信息层级递进
- 关键词高亮走 `dangerouslySetInnerHTML`，配套 `highlight()` 工具包 query 命中词

## 反模式

- ❌ 展示「综合得分 92%」——RRF 融合分无区分度会全部落「最相关」，误导调试
- ❌ 命中/选中用蓝色——RAG 调试域统一 amber 强调
- ❌ 三通道用同色条——向量 sky / 关键词 amber / 精排 violet，颜色即通道身份
- ❌ 命中卡正文不截断——用 `line-clamp-2` 保持列表密度，全文看右栏
