---
id: pages/detail/chameleon/eval-run-detail-master-detail
type: page
name: 评测运行详情（master-detail + URL 覆盖物）
description: 左 run 列表 rail / 中 run 详情（逐样本得分 + 分数分布桶 + 优化入口）/ 右 URL 驱动覆盖物（样本详情 or 优化侧栏）；可跳运行对比热力矩阵
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
- blocks/display/chameleon/run-compare-heatmap-matrix
- blocks/layout/chameleon/run-master-detail-rail-overlay
preview: /preview/pages/detail/chameleon/eval-run-detail-master-detail
---

# Chameleon Eval Run Detail Master-Detail

> 评测「运行详情」整页（`/datasets/:id/runs/:runId`）。三栏 master-detail 全在一张 `rounded-xl border bg-white` 大框里：**左** run 列表 rail（244px，状态点 + 均分 + 优化产物徽标）、**中** run 详情主区（header 状态/评分器/均分 + 折叠的评估配置 + 分数分布桶 + 逐样本明细表）、**右** URL 驱动的覆盖物侧栏（点样本行滑出 `?item=` 的样本详情 420px，或点「智能优化」滑出 `?optimize=1` 的优化侧栏）。顶部面包屑可跳「运行对比」整页（Langfuse 式样本行 × 运行列得分色块热力矩阵）。

## 视觉特征

- 外层 `flex h-[calc(100vh-130px)] flex-col gap-3`；header `flex items-center gap-2`：面包屑 Link `rounded-md px-2 py-1 text-[12.5px] text-stone-500 hover:bg-stone-100`（ArrowLeft h-3.5 + 数据集名）+ `/` stone-300 + 「运行详情」`text-[13px] font-medium text-stone-900`
- 主框 `flex min-h-0 flex-1 overflow-hidden rounded-xl border border-stone-200 bg-white`，内含三栏：
- **左 rail**（RunListRail）`flex h-full w-[244px] shrink-0 flex-col border-r border-stone-200 bg-white`：头 `border-b px-3 py-2.5 text-[12px] font-medium text-stone-700`「运行（N）」；每个 run 按钮 `flex w-full flex-col gap-1 border-l-2 px-3 py-2`，选中 `border-stone-800 bg-stone-50`、未选 `border-transparent hover:bg-stone-50/60`；第一行 状态点 `h-1.5 w-1.5 rounded-full`（success emerald-400 / failed rose-400 / 否则 stone-300）+ 名称 `text-[12.5px]`（active font-medium stone-900）+ 优化产物 `Sparkles h-3 w-3 text-violet-400`；第二行 `pl-3` 优化产物 Badge `bg-violet-50 text-[9px] text-violet-700` + 均分 `tnum text-[11px]`（scoreColor）+ 状态文字 `ml-auto text-[10px] text-stone-400`；第三行 `pl-3 text-[9.5px] text-stone-400` 时间
- **中 detail**（RunDetailPanel）`min-w-0 flex-1 bg-[var(--color-paper)]`：header `border-b px-5 py-3.5`——run 名 `text-[16px] font-medium` + 「← 优化自上一版本」Badge violet-50/700 + 右侧 `ml-auto` 动作（对比上一版本 `bg-stone-50 px-2 py-1 text-[11px]` GitCompare + 智能优化 `bg-violet-50 px-2 py-1 text-[11px] text-violet-700` Sparkles）；副行 状态 Badge（statusBg）+ 评分器 + 模型 + 均分；主体 `flex-1 space-y-6 overflow-auto px-5 py-4`
- 评估配置 section：可折叠按钮 `text-[12.5px] font-medium text-stone-800`（ChevronDown/Right h-3.5 stone-400），展开 `rounded-md border border-stone-200/70 bg-stone-50/40 p-3 text-[11.5px]`，含 被测模型/评分器/裁判模型（font-mono stone-800）+ 评分要点/系统提示词 `pre rounded bg-white p-2 font-mono text-[11px]`
- 分数分布 section：`mb-3 text-[12.5px] font-medium`「分数分布」+ `text-[10.5px] text-stone-400`「点击柱子可筛选下方样本」；柱状桶（绿/黄/红按分段）点击筛选
- 样本明细 section：`mb-3 text-[12.5px] font-medium`「样本明细（N）」+ 筛选 chip `bg-stone-100 px-2 py-0.5 text-[10.5px]`；DataTable 列 = 输入(max-w-260 truncate 11.5px) / 模型回答(max-w-280) / 分数(verdict Badge + `rounded px-1.5 py-0.5 text-[10.5px]` scoreBg) / 耗时(tnum 11px stone-400) / 错误点(rose-500 ●)；选中行左条 `bg-stone-700`
- **右覆盖物**（RunSampleDetailPanel）`flex h-full w-[420px] shrink-0 border-l bg-[var(--color-paper)]`：header `border-b px-4 py-3` 样本 id(font-mono 10.5px stone-400) + 分数 chip(scoreBg) + 耗时 + X 收起；体 `space-y-3 px-4 py-3`——「查看调用 trace」`bg-sky-50 px-2 py-1 text-[11px] text-sky-700`（ExternalLink）+ 输入(stone-500)/理想回答(emerald-600)/模型回答(sky-600)/参照(violet-600) JsonEditor 段 + 评分理由 `rounded border bg-white px-2 py-1.5 text-[11.5px]` + 错误 `rounded border-rose-100 bg-rose-50 text-[10.5px] text-rose-700`
- scoreBg / scoreColor 分段：≥0.8 emerald-50/700·emerald-600 / 0.5–0.8 amber-50/700·amber-600 / <0.5 red-50/700·red-600 / 无 stone-100/400·stone-400
- **运行对比矩阵**（RunCompareMatrix，对比页）：header GitCompare + 「运行对比 · N 个运行」+ `ml-auto` 导出图片/数据按钮；可折叠「对比统计」+ 得分表 `rounded-lg border` 内 table：表头 `bg-stone-50` 行 `min-w-[220px]` 样本·预期列 + 各 run 列（均值副行 text-[10px] stone-400）；每格 `tnum rounded px-2 py-1`(scoreBg) 分数；行 hover `bg-stone-50/60`，点行开 ModalContent xl 并排看各 run 预期 / 实际

## 核心代码

```tsx
{/* 整页三栏：rail + detail + URL 覆盖物 */}
<div className="flex h-[calc(100vh-130px)] flex-col gap-3">
  <header className="flex items-center gap-2">
    <Link to={`/datasets/${dsId}?tab=runs`} className="… text-[12.5px] text-stone-500">
      <ArrowLeft className="h-3.5 w-3.5" /> {dsName}
    </Link>
    <span className="text-stone-300">/</span>
    <span className="text-[13px] font-medium text-stone-900">运行详情</span>
  </header>
  <div className="flex min-h-0 flex-1 overflow-hidden rounded-xl border border-stone-200 bg-white">
    <RunListRail runs={runs} activeRunId={rid} onSelect={goRun} />
    <main className="min-w-0 flex-1 bg-[var(--color-paper)]">
      <RunDetailPanel run={run} onSelectItem={ri => openSample(ri.id)} onOptimize={openOptimize} onCompareParent={goCompare} />
    </main>
    {selectedItem && <RunSampleDetailPanel ri={selectedItem} onClose={closeOverlay} />}
    {optimizeOpen && <RunOptimizePanel runId={rid} … onClose={closeOverlay} />}
  </div>
</div>
```

## 适配指南

- 三栏全在一张白卡里（`rounded-xl border bg-white` 包住 rail + detail + overlay），不是三块独立卡——给「同一份运行」的整体感
- 覆盖物用 URL `?item=` / `?optimize=` 驱动，`setParams(next, { replace: true })`——刷新 / 分享可定位，但浮层切换不污染浏览器历史
- 同屏最多 1 层覆盖物：开样本详情则清 optimize，开优化则清 item，互斥
- 分数色编码统一走 `score.ts` 的 scoreBg / scoreColor / formatScore，贯穿 rail / detail 表 / 样本侧栏 / 对比矩阵
- 「智能优化」对智能体运行禁用（`disabled={!!run.agent_key}`）——智能体 Prompt 在工作流编排里，外部不可覆盖
- 跳对比矩阵：父子两版本 `?ids=parent,child`，多版本 `?ids=a,b,c`，复用同一 RunCompareMatrix

## 反模式

- ❌ 样本详情用行内嵌套小框——必须是整页右侧滑出的 420px 侧栏，给逐字段对照空间
- ❌ 用 Number() 转 run id / dataset id——雪花 64-bit 超 MAX_SAFE_INTEGER，全程 string
- ❌ 覆盖物切换写进浏览器历史——用 replace，否则回退在样本间逐级跳很烦
- ❌ 分数色散落硬编码——统一 scoreBg/scoreColor 分段，三处一致
- ❌ 对比矩阵每格用饱和色块——用 scoreBg 浅底 chip，热力感来自「整列对比」而非单格炫色
