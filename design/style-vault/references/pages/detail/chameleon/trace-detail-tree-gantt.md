---
id: pages/detail/chameleon/trace-detail-tree-gantt
type: page
name: Trace 详情（树/甘特双视图分屏）
description: LangSmith 式 trace 详情——header(返回 + GitBranch + request_id mono + 树/甘特 ViewToggle + 节点统计) → 树视图 grid-[2fr_3fr] 左观测树右节点详情 / 甘特视图上下分屏
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
- blocks/display/chameleon/trace-observation-tree-gantt
preview: /preview/pages/detail/chameleon/trace-detail-tree-gantt
---

# Chameleon Trace Detail Tree-Gantt

> LangSmith 式调用链路 trace 详情（`/traces/:requestId`）。外层 `space-y-3`。**header** 一行：返回按钮 + `/` + GitBranch + 「Trace 详情」+ request_id（mono）+ 右侧树/甘特 ViewToggle + 节点统计。**树视图** = `grid-cols-[minmax(0,2fr)_3fr] gap-3` 左「观测嵌套树」（mono 缩进树，每行 icon + type + name + duration 条）/ 右「节点详情」（type/model/agent_key 徽标 + duration/tokens/ttfb + Request/Response JsonViewer + spans）。**甘特视图** = 上「甘特时间轴」+ 下「节点详情」上下两 SectionCard 分屏。

## 视觉特征

- 外层 `space-y-3`；header `flex items-center gap-3`：返回 `rounded-md px-2 py-1 text-[12.5px] text-stone-500 hover:bg-stone-100`（ArrowLeft h-3.5）+ `/` stone-300 + flex-1 baseline 区（GitBranch h-3.5 stone-500 + 「Trace 详情」`text-[15px] font-medium text-stone-900` + request_id `font-mono text-[11px] text-stone-500`）+ ViewToggle
- ViewToggle：`inline-flex overflow-hidden rounded-md border border-stone-200/70 text-[11.5px]`，每段 `px-2.5 py-1`，选中 `bg-stone-800 text-white`、未选 `bg-white text-stone-600 hover:bg-stone-100`（树视图 / 甘特图）
- TreeStats（节点统计）`text-[10.5px] text-stone-500`：`<N font-mono tnum stone-700> 节点 · <ok font-mono tnum emerald-600> ok · <err font-mono tnum rose-600> err`
- 树视图：`grid grid-cols-1 gap-3 lg:grid-cols-[minmax(0,2fr)_3fr]`；两块 SectionCard `!p-3`，块标题行 `mb-2 flex items-center justify-between`：`text-[11.5px] font-medium text-stone-700`（观测嵌套树 / 节点详情）+ TreeStats（左块带）
- **观测树**（ObservationTree）`space-y-0.5 font-mono text-[11.5px]`：每行 `flex items-center gap-2 rounded px-1 py-1`，hover `bg-stone-100/70`，选中 `bg-blue-50` + 左侧高亮竖条 `absolute inset-y-0 left-0 w-[3px] rounded-r bg-blue-500`；缩进 `paddingLeft: depth*14+4`，depth>0 有竖向 guide `border-l border-stone-200/80`；折叠箭头 ChevronRight/Down h-3 stone-400；类型 icon `h-3.5 w-3.5`（按 TYPE_COLOR：trace stone-700 / span stone-500 / generation violet-600 / agent blue-600 / tool orange-600 / retriever emerald-600 / evaluator amber-600 / embedding cyan-600 / guardrail rose-600）+ type 标签 `w-16 font-medium`（同色）+ name truncate stone-800；失败 `AlertCircle h-3 + 错误消息 text-rose-500`；scores 徽章 + tokens Badge + duration 条 `h-1 flex-1 rounded-full bg-stone-100`（成功 bg-blue-400 / 失败 bg-rose-400）+ 数字 `tnum text-[10.5px] stone-500`
- **节点详情**（NodeDetail）`space-y-3`：头行 Bot h-3.5 stone-500 + type 徽标 `rounded px-1.5 py-0.5 font-mono text-[10.5px] uppercase`（成功 emerald-50/700 失败 rose-50/700）+ model_code 徽标 `rounded bg-violet-50 px-1.5 py-0.5 font-mono text-[10.5px] text-violet-700` + agent_key `font-mono text-[11px] stone-500` + 时间 `ml-auto font-mono text-[10.5px] stone-500`；指标行 `flex gap-3 text-[11px] stone-500`（duration / tokens / ttfb，值 `font-mono tnum stone-700`）；错误条 `rounded border border-rose-200 bg-rose-50 px-2 py-1 text-[11px] text-rose-700`
- DetailSection：标题 `mb-1 text-[10.5px] uppercase tracking-wider text-stone-500` + JsonViewer（Request payload / Response payload）；Spans `ul space-y-1`，每 li `rounded border border-stone-200/70 bg-white px-2 py-1 font-mono text-[11px]`（name stone-700 + 耗时 stone-500 + 状态 chip `rounded px-1 text-[10px]`：failed rose-50/700 / 否则 emerald-50/700）
- 甘特视图：上下两 SectionCard `!p-3`，上块标题「甘特时间轴」`text-[11.5px] font-medium text-stone-700` + TreeStats，含横向时间条；下块 NodeDetail

## 核心代码

```tsx
<div className="space-y-3">
  <header className="flex items-center gap-3">
    <button onClick={goBack} className="… text-[12.5px] text-stone-500 hover:bg-stone-100">
      <ArrowLeft className="h-3.5 w-3.5" /> 返回
    </button>
    <span className="text-stone-300">/</span>
    <div className="flex flex-1 items-baseline gap-2">
      <GitBranch className="h-3.5 w-3.5 text-stone-500" />
      <span className="text-[15px] font-medium text-stone-900">Trace 详情</span>
      <span className="font-mono text-[11px] text-stone-500">{rid}</span>
    </div>
    <ViewToggle mode={viewMode} onChange={setViewMode} />
  </header>

  {viewMode === 'gantt' ? (
    <div className="space-y-3">
      <SectionCard className="!p-3">… 甘特时间轴 + TreeStats … <TraceGantt root={root} /></SectionCard>
      <SectionCard className="!p-3"><NodeDetail tree={root} focusId={focusId} /></SectionCard>
    </div>
  ) : (
    <div className="grid grid-cols-1 gap-3 lg:grid-cols-[minmax(0,2fr)_3fr]">
      <SectionCard className="!p-3">… 观测嵌套树 … <ObservationTree root={root} … /></SectionCard>
      <SectionCard className="!p-3"><NodeDetail tree={root} focusId={focusId} /></SectionCard>
    </div>
  )}
</div>
```

## 适配指南

- 观测树整块用 `font-mono`——trace 是给工程师 debug 的，等宽字体让 type 列 / duration 列对齐
- 类型色编码（TYPE_COLOR）9 类各一色，是 trace 树的「图例」——一眼区分 generation(紫) / agent(蓝) / retriever(绿) / tool(橙)…
- duration 条按「占根节点总时长比例」画（`width = duration/totalDuration * 100%`，min 2%），成功 blue-400 / 失败 rose-400
- 选中节点同步右侧 NodeDetail（按 request_id 查找树节点，再按 id 拉 node detail）；树左侧高亮竖条 + bg-blue-50 双重标记选中
- 树 / 甘特 ViewToggle 黑底选中（`bg-stone-800 text-white`）——和 waveflow 命令面板 / dashboard 时间范围同款 segment 语言
- 切 trace 时 reset 视图态（选中 / 折叠 / 缩放）

## 反模式

- ❌ 观测树用变宽字体——type / duration 列对不齐，扫读链路费劲
- ❌ 9 类节点用同色——类型色编码是 trace 的核心可读性，必须各一 hue
- ❌ duration 条用绝对宽度——必须按占根总时长比例，才看得出哪个节点是瓶颈
- ❌ 树 / 甘特用浅蓝选中 toggle——这里要「硬」的黑底 segment，和 KB tab 的浅蓝区分语境
- ❌ 节点 type 徽标不区分成败——成功 emerald / 失败 rose，徽标本身就要带成败语义
