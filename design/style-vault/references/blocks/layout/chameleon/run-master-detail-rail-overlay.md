---
id: blocks/layout/chameleon/run-master-detail-rail-overlay
type: block
name: 244px run 列表栏 + 中详情 + 右覆盖物三栏
description: 评测运行详情整页 - 左 244px run 列表(状态点/优化徽标/分数/时间) + 中 run 详情主区 + 右侧 URL 驱动单层覆盖物(样本详情 or 优化侧栏)
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
preview: /preview/blocks/layout/chameleon/run-master-detail-rail-overlay
---

# Chameleon Run 主从覆盖物三栏

> 评测运行详情整页（路由 `/datasets/:id/runs/:runId`）。外层 `flex h-[calc(100vh-130px)] flex-col gap-3`：顶部面包屑 header（ArrowLeft + 数据集名 + `/` + 「运行详情」）+ 主体一张 `rounded-xl border border-stone-200 bg-white` 卡片，横向切 **244px run 列表 aside（master）+ 中详情 main（`bg-[var(--color-paper)]`）+ 右侧同屏最多一层覆盖物**（样本详情 or 优化侧栏）。覆盖物由 URL `?item=` / `?optimize=1` 驱动，切换走 `replace` 不污染历史。

## 视觉特征

- **外层 `flex h-[calc(100vh-130px)] flex-col gap-3`**：列方向，header 与主体 12px 间隙
- **header `flex items-center gap-2`**：面包屑回链 `inline-flex items-center gap-1 rounded-md px-2 py-1 text-[12.5px] text-stone-500 hover:bg-stone-100 hover:text-stone-800`，前置 `ArrowLeft h-3.5 w-3.5`(14px) + 数据集名；分隔 `<span className="text-stone-300">/</span>`；末「运行详情」`text-[13px] font-medium text-stone-900`
- **主体卡 `flex min-h-0 flex-1 overflow-hidden rounded-xl(12px) border border-stone-200(#e7e5e0) bg-white`**：一张大卡裹三栏，无 gap，靠 `border-r` 分割
- **run 列表 aside**：`flex h-full w-[244px] shrink-0 flex-col overflow-hidden border-r border-stone-200 bg-white`
  - 头：`border-b border-stone-200 px-3 py-2.5 text-[12px] font-medium text-stone-700` —— 「运行（N）」
  - 列表容器：`flex-1 overflow-auto py-1`
  - **run 按钮**：`flex w-full flex-col gap-1 border-l-2 px-3 py-2 text-left transition`；选中 `border-stone-800 bg-stone-50` / 默认 `border-transparent hover:bg-stone-50/60` —— **左 2px 竖条**是选中锚点（非整行高亮）
  - 第一行：状态点 `h-1.5 w-1.5 shrink-0 rounded-full`（success `bg-emerald-400` / failed `bg-rose-400` / 其它 `bg-stone-300`）+ 名称 `flex-1 truncate text-[12.5px]`（选中 `font-medium text-stone-900` / 默认 `text-stone-700`）+ 已优化时 `Sparkles h-3 w-3 text-violet-400`(12px)
  - 第二行 `flex items-center gap-1.5 pl-3`：优化产物 `Badge variant=outline bg-violet-50 px-1 py-0 text-[9px] text-violet-700` + 分数 `tnum text-[11px]` 走 scoreColor（≥0.8 emerald-600 / ≥0.5 amber-600 / <0.5 red-600 / 无 stone-400）+ `ml-auto text-[10px] text-stone-400` 状态文字
  - 第三行 `pl-3 text-[9.5px] text-stone-400` 时间
  - 空/加载态 `px-3 py-4 text-[11.5px] text-stone-400`
- **中详情 main**：`min-w-0 flex-1 bg-[var(--color-paper)]`(#fffefb)
  - 内 RunDetailPanel：header `border-b border-stone-200 px-5 py-3.5`，标题 `text-[16px] font-medium text-stone-900` + 优化徽标 + 右侧「对比上一版本」`GitCompare` / 「智能优化」`Sparkles bg-violet-50 text-violet-700` 按钮；meta 行 `mt-2 ... text-[11.5px] text-stone-500` 含状态 Badge + 评分器 + 模型 + 均分
  - body `flex-1 space-y-6 overflow-auto px-5 py-4`：可折叠「评估配置」+ 分数分布柱 + 样本明细 DataTable（选中行 `leftBar='bg-stone-700'`）
- **右覆盖物**：`selectedItem &&` 渲染 RunSampleDetailPanel / `optimizeOpen &&` 渲染 RunOptimizePanel —— 互斥，同屏最多一层

## 适配指南

- 覆盖物用 `setParams(next, { replace: true })`：同页浮层切换不逐级压栈，刷新/分享仍靠 URL 定位
- 打开样本时 `next.delete('optimize')`、打开优化时 `next.delete('item')` —— 保证互斥
- id/runId 全程保留 `string`（雪花 64-bit 超 MAX_SAFE_INTEGER，`Number()` 丢精度）
- 选中 run 用左 2px 竖条 + 浅灰底，**不要**整块蓝高亮——这是 investigative 语义不是导航

## 与 waveflow/master-detail-list-aside 区分

| 维度 | waveflow master-detail-list-aside | 本条 run-master-detail-rail-overlay |
|------|-----------------------------------|-------------------------------------|
| 列表宽 | 256px aside（可折叠 unmount + ChevronsRight 弹出按钮） | 244px aside（不可折叠） |
| 容器 | 左右**两张独立卡**（各自 `rounded-xl border bg-paper shadow-soft`，`gap-4`） | **一张大卡裹三栏**（`border + bg-white`，无独立卡 / 无 shadow，靠 `border-r` 切栏） |
| 列表项 | SetCard（icon + 名 + count + segmented 状态条），选中 `border-blue-400/50 + 蓝半透底` | run 按钮（状态点 + 名 + 优化徽标 + 分数 + 时间三行），选中**左 2px stone-800 竖条 + stone-50 底** |
| 右侧 | 单一详情面板（HERO + MetricCard 四宫 + 内嵌表） | 中详情 main **+ 右侧 URL 驱动单层覆盖物**（样本/优化侧栏滑出） |
| 语义 | 任务集运维总览 | 评测 run 调查（分数热力 + 样本下钻 + Prompt 优化） |
| URL | 无 URL 驱动 | `?item=` / `?optimize=1` 驱动右覆盖物（replace） |

选条原则：要「列表 + 详情」标准主从用 waveflow；要「列表 + 详情 + 可滑出的第三层调查浮层 + URL 可分享态」用本条。

## 反模式

- ❌ 右覆盖物同时开样本 + 优化两层——只允许一层，互斥
- ❌ 覆盖物切换用 push 而非 replace——回退会在样本间逐级弹，污染历史
- ❌ run 列表项整行蓝底——破坏 investigative 的克制；用左竖条 + 浅灰
- ❌ 三栏拆成三张带 shadow 的卡——失去「一个 run = 一张卡」的整体语义
