---
id: blocks/display/chameleon/run-compare-heatmap-matrix
type: block
name: 运行对比 score 热力矩阵
description: 样本行 × 运行列的 score 色块热力图(sticky 首列样本·预期) - 点行开居中弹窗并排各运行预期/实际输出 + 可折叠对比统计区(雷达/分布/折线/胜负 + AI 分析) + 导出 PNG/Excel
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
- components/feedback/chameleon/neon-loader
- components/display/chameleon/distribution-score-bars
preview: /preview/blocks/display/chameleon/run-compare-heatmap-matrix
---

# 运行对比 score 热力矩阵

> 借鉴 Langfuse 的评测运行对比：**样本行 × 运行列**的 score 色块热力图（sticky 首列「样本·预期」+ sticky 表头），点任一行开居中弹窗并排看各运行在该样本上的「预期 / 实际」输出。带可折叠**对比统计区**（能力雷达 / 分数分布 / 逐题折线 / 逐样本胜负 + AI 总结分析）+ 导出 PNG / Excel。waveflow 无，全新。

## 视觉特征

- **矩阵 table**：`w-full border-collapse text-[11.5px]`，外层 `rounded-lg border border-stone-200` + `overflow-auto`（导出态去 overflow）
- **thead**：`bg-stone-50`
  - 首列 th：`min-w-[220px] border-b border-r border-stone-200 bg-stone-50 px-3 py-2 text-left font-medium text-stone-500` + `sticky left-0 z-10`（非导出态）「样本 · 预期」
  - 运行列 th：`min-w-[116px] border-b border-stone-200 px-3 py-2 text-left font-medium text-stone-600`，内 `truncate` 运行名 + `mt-0.5 text-[10px] text-stone-400`「均值 N」
- **数据行**：`cursor-pointer hover:bg-stone-50/60`，点击 `setSelItem(itemId)` 开弹窗
  - 首格：`max-w-[260px] border-b border-r border-stone-200 bg-white px-3 py-2 align-top` + `sticky left-0 z-10`，样本预览 `truncate text-stone-700` + 预期 `mt-0.5 truncate text-[10px] text-stone-400`「预期 …slice(0,40)」
  - score 格：`border-b border-stone-100 px-1.5 py-1.5 align-top`，内块 `tnum w-full rounded px-2 py-1 text-left` + **scoreBg 色阶**（≥0.8 `bg-emerald-50 text-emerald-700` / 0.5–0.8 `bg-amber-50 text-amber-700` / <0.5 `bg-red-50 text-red-700` / null `bg-stone-100 text-stone-400`），错误显「错误」
- **对比统计折叠**（`section`）：触发 `flex items-center gap-1 text-[12.5px] font-medium text-stone-800`，ChevronDown/Right `h-3.5 text-stone-400` +「对比统计」+ 副标 `ml-1.5 text-[10.5px] font-normal text-stone-400`「能力雷达 · 分数分布 · 逐题得分 · AI 分析」；展开 `mt-2 rounded-lg border border-stone-200 bg-white p-3`
  - **图表网格**：`grid grid-cols-1 gap-4 lg:grid-cols-2`，ChartCard `rounded-lg border border-stone-200 bg-white p-3`，标题 `text-[11.5px] font-medium text-stone-700` + hint `text-[10px] text-stone-400`
  - **recharts 色板**：`['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#f43f5e', '#06b6d4']`（雷达 fillOpacity 0.12 / 柱 radius [2,2,0,0] / 折线 strokeWidth 1.6 dot=false）
  - **AI 总结分析**：`rounded-lg border border-violet-200/70 bg-violet-50/30 p-3`，标题 `text-[12px] font-medium text-violet-800` + 「生成 AI 分析」按钮 `bg-violet-600 text-white`（分析中走 NeonLoader）+ Markdown 渲染结果
  - **逐样本胜负**：每行 `flex items-center gap-2.5 text-[11.5px]`，胜 `tnum text-emerald-600` / 平 `text-stone-400` / 负 `text-rose-600` + 三段条 `h-1.5 flex-1 rounded-full bg-stone-100`（emerald-400 / stone-300 / rose-400）
- **弹窗 Modal size="xl"**：问题 `text-[12.5px] text-stone-800` + 预期块 `rounded-md border border-emerald-200/70 bg-emerald-50/40 p-2.5`（标题 `text-[10px] font-medium text-emerald-700`）+ OutputBlock `pre max-h-72 overflow-auto whitespace-pre-wrap rounded bg-stone-50 p-2 font-mono text-[11.5px] text-stone-700` + 运行列 `grid repeat(N, minmax(0,1fr)) gap-3`，每列 `rounded-md border border-stone-200 bg-white p-2.5` + 得分 chip scoreBg
- **导出报告头**（仅 exporting 态）：`border-b border-stone-200 pb-2.5`，「运行对比报告 · 数据集名」`text-[14px] font-semibold text-stone-800` + 日期 + 运行均分 chip `rounded-md bg-stone-100 px-2 py-0.5 text-[11px]`

## 核心代码

```tsx
// scoreBg 色阶（贯穿 datasets / eval 列表·详情·矩阵）
export const scoreBg = (s) =>
  s == null ? 'bg-stone-100 text-stone-400'
  : s >= 0.8 ? 'bg-emerald-50 text-emerald-700'
  : s >= 0.5 ? 'bg-amber-50 text-amber-700'
  : 'bg-red-50 text-red-700';

// 热力格
<div className={cn('tnum w-full rounded px-2 py-1 text-left', scoreBg(cell.score))}>
  {cell.score != null ? formatScore(cell.score) : cell.error ? '错误' : '—'}
</div>

// sticky 首列 + 表头（非导出态）
className={cn('... px-3 py-2', !exporting && 'sticky left-0 z-10')}

// 导出 PNG：展开统计 + 双 rAF + 600ms 等 recharts/AI 渲染稳 → exportImage pixelRatio 1.5
const recharts色板 = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#f43f5e', '#06b6d4'];
```

## 适配指南

- score 色阶 scoreBg 全站统一（列表 chip / 矩阵格 / 弹窗得分），≥0.8 绿 / 0.5–0.8 黄 / <0.5 红
- 首列样本 + 表头 sticky 让宽矩阵横滚时锚点不丢；导出态去 sticky/overflow（截图取全）
- 对比统计默认折叠——多数时候先扫热力图，统计按需展开；导出时强制展开入图
- AI 分析走 ai_tasks 异步子系统（提交即返 + 轮询 + 缓存反显），导出图片时整块省略（长 markdown 栅格化慢）

## 反模式

- ❌ score 用单色深浅——必须三档语义色（绿/黄/红）一眼分好坏
- ❌ 宽矩阵首列不 sticky——横滚后丢失「这一行是哪个样本」
- ❌ recharts 各系列随机配色——固定 6 色板按运行索引取，跨图一致
- ❌ AI 分析也截进导出 PNG——长 markdown 栅格化极慢，用面板「复制」分享文字
