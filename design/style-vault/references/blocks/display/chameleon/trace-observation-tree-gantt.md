---
id: blocks/display/chameleon/trace-observation-tree-gantt
type: block
name: Trace 观测树 + 甘特双视图
description: trace 嵌套观测树(9 类 observation 各 icon+色 / 14px 缩进竖向 guide / 折叠 / 选中蓝竖条 / duration 条) + 虚拟滚动甘特时间轴(横向缩放 + ruler 同步 + bar 按 type 着色叠 cost/token) - LangFuse/LangSmith 范式
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
- tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio
preview: /preview/blocks/display/chameleon/trace-observation-tree-gantt
---

# Trace 观测树 + 甘特双视图

> LangFuse / LangSmith 范式的 trace 可视化，两个可切换视图共一套 observation 语义色：
> **① 观测树**：每行 `[type icon] type  名称/模型code  scores 徽章  token  duration 条+ms`，9 类 observation 各自 icon + 色，子节点 14px 缩进 + 竖向 guide 线，可折叠，选中态左侧蓝竖条。
> **② 甘特时间轴**：竖向虚拟滚动撑 1000+ spans，label 列 sticky-left，时间区横向缩放 + ruler 同步，bar 按 `observation_type` 着色叠 cost/token 标签。
> waveflow 无 trace，全新。

## 视觉特征

### ① 观测树（ObservationTree）

- **容器**：`space-y-0.5 font-mono text-[11.5px]`
- **TreeRow**：`group relative flex w-full items-center gap-2 rounded px-1 py-1 text-left transition hover:bg-stone-100/70`，`style.paddingLeft = depth*14 + 4`；选中 `bg-blue-50 hover:bg-blue-50`
  - 选中竖条：`absolute inset-y-0 left-0 w-[3px] rounded-r bg-blue-500`（无边框）
  - depth guide：`absolute top-0 bottom-0 border-l border-stone-200/80`，`style.left = (depth-1)*14 + 10`
  - 折叠箭头：ChevronDown/Right `h-3 w-3 text-stone-400`，无子节点占位 `w-4`
- **type icon**（`h-3.5 w-3.5`）+ **type label**（`w-16 shrink-0 font-medium`），9 类 icon + 色：
  | type | icon | 色 |
  |------|------|----|
  | trace | Layers | text-stone-700 |
  | span | CircleDashed | text-stone-500 |
  | generation | Sparkles | text-violet-600 |
  | agent | Bot | text-blue-600 |
  | tool | Wrench | text-orange-600 |
  | retriever | Database | text-emerald-600 |
  | evaluator | ShieldCheck | text-amber-600 |
  | embedding | Cpu | text-cyan-600 |
  | guardrail | ShieldCheck | text-rose-600 |
- **名称列**：`min-w-0 flex-1 truncate text-stone-800`（子观测显 node_id / generation 优先 model_code / 否则 agent_key）；失败追加 `text-rose-500` + `AlertCircle h-3 w-3` + error 截 40 字
- **scores 徽章**（≤3 + 余数）：按 source 配色 `rounded border px-1 py-0.5 text-[10px]`：feedback `bg-emerald-50 text-emerald-700 border-emerald-200` / annotation amber / eval violet / api blue；👍👎 用 ThumbsUp/ThumbsDown `h-3 w-3`
- **token Badge**：`variant=outline font-mono text-[10px]`「N tok」（generation 才有）
- **duration**：`flex w-32 shrink-0 items-center gap-1.5`，条 `h-1 flex-1 overflow-hidden rounded-full bg-stone-100` 内填（成功 `bg-blue-400` / 失败 `bg-rose-400`，width = duration/total%），数字 `tnum w-12 text-right text-[10.5px] text-stone-500`「Nms」
- **ObservationIconRail**（收起态纵向 icon 轨）：`flex flex-col items-center gap-0.5`，每 icon `rounded p-1 hover:bg-stone-100`，选中 `bg-blue-100`，失败 icon `text-rose-500`

### ② 甘特时间轴（TraceGantt）

- **常量**：LABEL_W 210 / ROW_H 30 / RULER_H 24
- **缩放工具条**（右上）：`mb-1 flex items-center justify-end gap-1 text-stone-500`，Minus/Plus `h-3.5 rounded p-0.5 hover:bg-stone-100` + 百分比 `w-10 text-center font-mono text-[10.5px] tabular-nums`，步进 `*1.5`
- **ruler**：label 占位 `text-[10.5px] text-stone-400`「时间轴」+ 刻度区 `border-b border-stone-200/70`，tick `absolute top-0 font-mono text-[9.5px] text-stone-400`，`transform: translateX(-scrollLeft)` 同步横滚
- **行**：`absolute left-0 flex items-stretch border-b border-stone-100`，选中 `bg-amber-50/60` / hover `bg-stone-50` / 默认 `bg-white`，高 ROW_H
  - label 列：`sticky left-0 z-10 flex shrink-0 items-center gap-1 px-1.5`，`width=LABEL_W` `paddingLeft = 6 + depth*12`，选中底 `bg-amber-50/95`
    - type chip：`shrink-0 rounded px-1 py-px font-mono text-[9px] uppercase`（成功 `bg-stone-100 text-stone-500` / 失败 `bg-rose-50 text-rose-600`），显 `observation_type.slice(0,4)`
    - agent_key：`truncate text-[11px] text-stone-700`
- **GanttBar**：`absolute top-1/2 h-[14px] -translate-y-1/2 rounded-[3px] transition`，OBS_COLOR 着色（trace `bg-stone-400` / span `bg-sky-400` / generation `bg-violet-400` / agent `bg-indigo-400` / tool `bg-amber-400` / retriever `bg-teal-400` / evaluator `bg-fuchsia-400` / embedding `bg-cyan-400` / guardrail `bg-rose-300`），失败统一 `bg-rose-500`；选中 `ring-2 ring-stone-800 ring-offset-1`，hover `brightness-110 ring-1 ring-stone-500`；width>12% 内显时长 `font-mono text-[9.5px] text-white/90`
- **CostLabel**：有成本 `text-emerald-700` / 仅 token `text-stone-400`，`font-mono text-[10px] tabular-nums`；bar 偏右（leftPct+widthPct ≥ 82）时贴左避溢出
- **body 高**：`min(520, max(180, rows*30 + 8))`

## 核心代码

```tsx
// 树：缩进 + guide 线 + 选中竖条
<button style={{ paddingLeft: depth * 14 + 4 }} className={cn('group relative ...', isSelected && 'bg-blue-50')}>
  {isSelected && <span className="absolute inset-y-0 left-0 w-[3px] rounded-r bg-blue-500" />}
  {depth > 0 && <span className="absolute top-0 bottom-0 border-l border-stone-200/80" style={{ left: (depth-1)*14 + 10 }} />}
  <Icon className={cn('h-3.5 w-3.5 shrink-0', colorCls)} />
  <span className={cn('w-16 shrink-0 font-medium', colorCls)}>{otype}</span>
  ...
  <div className="flex w-32 shrink-0 items-center gap-1.5">
    <div className="h-1 flex-1 overflow-hidden rounded-full bg-stone-100">
      <div className={cn('h-full', node.success ? 'bg-blue-400' : 'bg-rose-400')} style={{ width: `${widthPct}%` }} />
    </div>
    <span className="tnum w-12 text-right text-[10.5px] text-stone-500">{node.duration_ms}ms</span>
  </div>
</button>

// 甘特：bar 按 type 着色，失败统一 rose-500
const OBS_COLOR = { trace:'bg-stone-400', span:'bg-sky-400', generation:'bg-violet-400', agent:'bg-indigo-400',
  tool:'bg-amber-400', retriever:'bg-teal-400', evaluator:'bg-fuchsia-400', embedding:'bg-cyan-400', guardrail:'bg-rose-300' };
const color = node.success ? OBS_COLOR[node.observation_type] : 'bg-rose-500';

// 虚拟滚动 + ruler 同步横滚（label sticky-left，刻度 translateX(-scrollLeft)）
const virtualizer = useVirtualizer({ count: rows.length, estimateSize: () => ROW_H, overscan: 15 });
```

## 适配指南

- **9 类 observation 色是身份标识**，树（text-*-600）与甘特（bg-*-400）共一套语义，跨视图一致
- 树用蓝系选中（`bg-blue-50` + `w-[3px] bg-blue-500` 竖条），甘特用 amber 系选中行（`bg-amber-50/60` + bar `ring-stone-800`）——两视图选中态各自识别
- 1000+ spans 必须虚拟滚动（@tanstack/react-virtual），label 列 sticky-left 让横滚时节点名不丢
- generation 节点优先显 model_code（被测/裁判一眼辨）；duration 条按"占父节点总时长比例"画

## 反模式

- ❌ 9 类 observation 同色——type 即身份，必须各自 icon + 色，糊成一色无法快速定位某类
- ❌ 树缩进不画 guide 线——深嵌套时丢失父子层级，必须 `border-l` 竖向引导
- ❌ 甘特不虚拟滚动——1000+ spans 会卡死
- ❌ 失败节点用各自 type 色——失败统一 rose（树 `bg-rose-400` / 甘特 `bg-rose-500`），一眼看出哪步挂了
- ❌ ruler 不随 body 横滚同步——刻度与 bar 错位，时间读数失真（用 `translateX(-scrollLeft)`）
