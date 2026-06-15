---
id: components/display/chameleon/distribution-score-bars
type: component
name: 占比 / 多通道 / 分数色条三件套
description: 单维 top-N 占比条 + RAG 多通道相似度条 + 0–1 分数色编码（贯穿 dashboard 分布卡 / KB 检索测试 / eval 评测矩阵）
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
preview: /preview/components/display/chameleon/distribution-score-bars
---

# 占比 / 多通道 / 分数色条三件套

> Chameleon 数据可视化的三个细粒度原语：① **占比条**（dashboard 渠道/错误分布 + Top 表内嵌渐变条），② **多通道相似度条**（RAG 命中向量/关键词/精排三色条），③ **分数色编码**（0–1 评测分的统一绿黄红着色，作 chip 底色或纯文字色）。共用「极细 1.5px 进度条 + tnum 数字 + 主题/语义色填充」的视觉基因。

## 视觉特征

### 占比条（DistributionCard）

- 卡片：`Card` > `CardContent pt-5`（20px）；标题 `h3 mb-3 text-sm font-medium text-stone-900`
- 列表 `ul space-y-2.5`（行距 10px）
- 行内 label/count 行：`mb-1 flex items-center justify-between text-[12px]`
  - label：`truncate text-stone-700`
  - count：`tnum shrink-0 pl-2 text-stone-500`，内嵌百分比 `ml-1 text-stone-400`，`((count/total)*100).toFixed(0)%`（**整数**百分比）
- 进度条轨：`relative h-1.5 w-full overflow-hidden rounded bg-stone-100`（1.5=6px 高，`rounded`=Tailwind 默认 4px）
- 填充：`bg-primary-400 absolute inset-y-0 left-0 rounded`，`style.width = (count/total)*100%`（**主题 primary-400，随主题色**）

### Top 表内嵌变体（overview-tab）

- 进度条轨：`h-1.5 w-16 overflow-hidden rounded-full bg-stone-100`（**w-16=64px 固定宽 + 全圆角**）
- 填充：`from-primary-300 to-primary-500 h-full rounded-full bg-gradient-to-r`（**左→右 primary 渐变**，非纯色）
- 右侧值：`tnum w-10 text-right text-stone-600`，搭配 `RankBadge` 排名徽标

### RankBadge 排名徽标（rank-badge.tsx）

- 外形：`inline-flex h-5 w-5(20px) shrink-0 items-center justify-center rounded-full text-[10px] font-semibold tabular-nums ring-1 ring-inset`（**圆形 20px + 1px inset ring**）
- 金/银/铜/其余 4 档（每档 bg/text/ring 三色）：
  - rank1 金：`bg-amber-100(#fef3c7) text-amber-700(#b45309) ring-amber-200(#fde68a)`
  - rank2 银：`bg-slate-200(#e2e8f0) text-slate-600(#475569) ring-slate-300(#cbd5e1)`
  - rank3 铜：`bg-orange-100(#ffedd5) text-orange-700(#c2410c) ring-orange-200(#fed7aa)`
  - 其余：`bg-stone-100(#f5f5f4) text-stone-400(#a8a29e) ring-stone-200(#e7e5e4)`
- 内容：`{index + 1}`（1-based 名次）

### 多通道相似度条（ScoreBreakdown · full 模式）

- 容器 `space-y-1`；每行 `ChannelRow`：`flex items-center gap-2`
  - label：`w-16 shrink-0 text-right text-[10.5px] text-stone-500`（右对齐 64px）
  - 轨：`h-1.5 flex-1 overflow-hidden rounded-full bg-stone-100`
  - 填充：`h-full rounded-full` + **通道语义色**：向量 `bg-sky-500`(#0ea5e9) / 关键词 `bg-amber-500`(#f59e0b) / 精排 `bg-violet-500`(#8b5cf6)，`width = clamp(round(v*100), 0, 100)%`
  - 值：`w-9 shrink-0 text-right font-mono text-[10.5px] tabular-nums text-stone-600`，`{pct}%`

### 多通道 · compact 模式

- 容器 `flex flex-wrap items-center gap-x-2.5 gap-y-0.5`
- 每通道一段：`text-[10.5px] text-stone-500`，short 文字（向量/关键词/精排）+ 内嵌值 `ml-0.5 font-mono tabular-nums text-stone-700`，如「向量 88%」
- 空态（无分项）：full 显 `text-[10.5px] text-stone-400` 「仅按综合排序，无分项」；compact 返回 null

### 分数色编码（score.ts）

- `scoreColor`（纯文字色）：≥0.8 `text-emerald-600`(#059669) / 0.5–0.8 `text-amber-600`(#d97706) / <0.5 `text-red-600`(#dc2626) / null|NaN `text-stone-400`
- `scoreBg`（chip 底+字色）：≥0.8 `bg-emerald-50 text-emerald-700` / 0.5–0.8 `bg-amber-50 text-amber-700` / <0.5 `bg-red-50 text-red-700` / null `bg-stone-100 text-stone-400`
- `formatScore`：`n.toFixed(2)`（两位小数），null → `—`
- 矩阵单元格用法：`rounded px-2 py-1 tnum w-full text-left`，值 `font-mono` + `tabular-nums`

## Tokens

仅局部语义 token：

```json
{
  "score": {
    "high": { "threshold": 0.8, "text": "#059669", "bg": "#ecfdf5", "bgText": "#047857" },
    "mid": { "threshold": 0.5, "text": "#d97706", "bg": "#fffbeb", "bgText": "#b45309" },
    "low": { "text": "#dc2626", "bg": "#fef2f2", "bgText": "#b91c1c" },
    "empty": { "text": "#a8a29e", "bg": "#f5f5f4" }
  },
  "channel": {
    "vector": "#0ea5e9",
    "keyword": "#f59e0b",
    "rerank": "#8b5cf6"
  },
  "bar": {
    "height": "6px",
    "track": "#f5f5f4",
    "radiusDistribution": "4px",
    "radiusTopAndChannel": "9999px",
    "fillThemed": "var(--color-primary-400)"
  }
}
```

## 核心代码

```tsx
// 占比条单行
<div className="mb-1 flex items-center justify-between text-[12px]">
  <span className="truncate text-stone-700">{label}</span>
  <span className="tnum shrink-0 pl-2 text-stone-500">
    {count}<span className="ml-1 text-stone-400">{((count/total)*100).toFixed(0)}%</span>
  </span>
</div>
<div className="relative h-1.5 w-full overflow-hidden rounded bg-stone-100">
  <div className="bg-primary-400 absolute inset-y-0 left-0 rounded" style={{ width: `${(count/total)*100}%` }} />
</div>

// 分数色编码
const scoreBg = (s) => s == null ? 'bg-stone-100 text-stone-400'
  : s >= 0.8 ? 'bg-emerald-50 text-emerald-700'
  : s >= 0.5 ? 'bg-amber-50 text-amber-700'
  : 'bg-red-50 text-red-700';
```

## 适配指南

- 占比条 total 用 `rows.reduce(sum,count) || 1` 兜底防除零
- Top 表条用 `count/max`（相对最大值）而非 `count/total`（相对总和）——单行最长的占满 64px
- 多通道分数先 `clampPct(round(v*100))` 再渲染——精排分可能 >1 或 <0
- 分数色 0.8 / 0.5 阈值是全站统一档位，datasets/eval-jobs/对比矩阵都从 `score.ts` 取，别在组件里硬编码绿黄红

## 反模式

- ❌ 进度条用 `h-2`/`h-3`——破坏「极细数据条」克制感，Chameleon 全站统一 `h-1.5`
- ❌ 占比条填充写死 `bg-blue-400`——用 `bg-primary-400` 跟主题
- ❌ 多通道用同色三条——通道语义色（sky/amber/violet）是区分向量/关键词/精排的唯一线索
- ❌ 分数百分比用 `toFixed(1)`——占比条统一 `toFixed(0)` 整数、分数统一 `toFixed(2)`，别混
