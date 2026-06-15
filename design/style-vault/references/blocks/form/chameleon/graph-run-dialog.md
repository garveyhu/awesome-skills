---
id: blocks/form/chameleon/graph-run-dialog
type: block
name: 工作流运行调试弹窗
description: 运行工作流的输入 + 结果弹窗——start 声明字段则渲染表单否则裸 JSON；Test Run(流式不落库)/Run(持久化)双钮；逐节点进度折叠行(状态徽标+子图执行中+重试中+错误已兜底+展开 NodeRunResult)+最终输出 JsonViewer；配套带 diff 的版本历史抽屉
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
- components/inputs/chameleon/graph-config-field-kit
- tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/blocks/form/chameleon/graph-run-dialog
---

# 工作流运行调试弹窗

> Chameleon 工作流编辑器的运行调试闭环。`RunDialog`（`system/graphs/components/run-dialog.tsx`）：start 声明输入字段则按字段渲染表单（文本 / 数字 / 段落 / select / checkbox / JSON），否则裸 JSON 输入；`Test Run`（流式调试不落库）/ `Run`（持久化写 call_logs）双钮；逐节点进度折叠行（状态徽标 + 子图执行中 + 重试中 + 错误已兜底，展开 `NodeRunResult`）+ 最终输出 `JsonViewer`。配套 `VersionHistoryPanel` 右侧抽屉：版本列表 → 点选展开「当前草稿 vs vN」节点级 diff 摘要 → 恢复此版本到草稿。

## 视觉特征

### RunDialog（ModalContent size=lg / max-h-[88vh]）

- **表单字段 label**：`text-[11.5px] text-stone-600`，required `span.ml-0.5 text-rose-400` 星号，字段引用 `span.ml-1.5 font-mono text-[9.5px] text-stone-300` 显示「start.{name}」
- **Input / select**：`h-8 text-[12.5px]`（select 加 `focus:border-blue-300 focus:ring-1 focus:ring-blue-200`）；JSON / paragraph Textarea `font-mono text-[12px]`（JSON）或 `text-[12.5px]`（段落）
- **dirty 提示**：`text-[10.5px] text-amber-600`（画布有未保存改动）
- **双钮**：`Test Run` = primary Button size=sm + `Play h-3 w-3 mr-1`；`Run（持久化）` = outline Button + `Zap h-3 w-3 mr-1`；旁注 `text-[10.5px] text-stone-400`
- **运行摘要行**：`flex items-center gap-2 border-t border-stone-200/70 pt-3`——NodeRunStatusBadge + 耗时 `tnum text-[11px] text-stone-500` + 节点数 + 右侧 `ml-auto text-[10.5px] text-stone-400`「调试运行 / 持久化执行」；暂停态 `rounded-full bg-amber-50 px-2 py-0.5 text-[11px] font-medium text-amber-700`
- **节点进度行**：`rounded-md border border-stone-200 bg-white`，触发 `flex w-full items-center gap-2 px-2 py-1.5 text-[11.5px]`——名 `text-stone-800` + type `font-mono text-[10px] text-stone-400` + 右侧徽标区 `ml-auto flex items-center gap-1.5`：子图执行中 `text-[10px] font-medium text-blue-600`、重试中 `text-amber-600`、错误已兜底 `rounded-full bg-amber-50 px-1.5 py-0.5 text-[10px] text-amber-700` 胶囊、NodeRunStatusBadge
- **展开 NodeRunResult**：`border-t border-stone-100 px-2 py-2`——error `rounded-md border-rose-200 bg-rose-50 px-2 py-1.5 text-rose-700`（type `font-mono text-[10px] uppercase text-rose-400`）；推理 details `summary text-[10.5px] uppercase text-violet-500`，body `border-violet-100 bg-violet-50/40 italic`；output JsonViewer maxHeight 240px
- **最终输出 / 错误**：失败 `rounded-md border-rose-200 bg-rose-50 px-2.5 py-2 text-[11.5px] text-rose-700`；成功输出 JsonViewer maxHeight 280px

### VersionHistoryPanel（Sheet w-[420px]）

- **SheetHeader**：`p-4`，标题 `flex items-center gap-2 text-[14px]` + `History h-4 w-4 text-stone-400`
- **版本卡**：`rounded-lg border bg-white transition`，选中 `border-stone-400 shadow-sm` / 否 `border-stone-200`
  - 头：`flex w-full items-center gap-2 px-3 py-2`——v号 `font-mono text-[12px] font-semibold text-stone-800` + 线上徽标 `rounded bg-emerald-50 px-1.5 py-0.5 text-[9.5px] font-medium text-emerald-700` + 时间 `ml-auto text-[10.5px] text-stone-400`
  - note：`px-3 pb-2 text-[11px] leading-snug text-stone-500`
- **展开区**：`border-t border-stone-100 px-3 py-2.5`，标题 `text-[10.5px] uppercase tracking-wider text-stone-400`「当前草稿 vs vN」
- **DiffBadge**：`inline-flex rounded px-1.5 py-0.5 text-[9.5px] font-medium`——emerald `bg-emerald-50 text-emerald-700` / rose `bg-rose-50 text-rose-700` / amber `bg-amber-50 text-amber-700`
- **diff 条目**：`flex items-center gap-1.5 rounded bg-stone-50 px-1.5 py-1 text-[10.5px]`——nodeId `font-mono text-stone-500` + type `font-mono text-[9.5px] text-stone-400` + name `ml-auto truncate text-stone-600`
- **恢复按钮**：outline Button size=sm `mt-2.5 w-full` + `RotateCcw h-3 w-3 mr-1`
- **空态**：`rounded-md border border-dashed border-stone-200 px-3 py-6 text-center text-[11.5px] text-stone-400`
- **lucide**：`Play` / `Zap`（RunDialog）；`History` / `RotateCcw`（VersionHistoryPanel）

## 核心代码

```tsx
// Test/Run 双钮
<Button size="sm" onClick={() => trigger('test')} disabled={!parsed.value || running}>
  <Play className="mr-1 h-3 w-3" /> Test Run
</Button>
<Button variant="outline" size="sm" onClick={() => trigger('persist')}>
  <Zap className="mr-1 h-3 w-3" /> Run（持久化）
</Button>

// 节点进度行右侧徽标
<span className="ml-auto flex items-center gap-1.5">
  {status === 'running' && run?.subActive && (
    <span className="text-[10px] font-medium text-blue-600">子图执行中 · {run.subActive}</span>
  )}
  {status === 'running' && run?.retry && (
    <span className="text-[10px] font-medium text-amber-600">重试中 {run.retry.attempt}/{run.retry.maxRetries}</span>
  )}
  {run?.errorHandled && (
    <span className="inline-flex items-center rounded-full bg-amber-50 px-1.5 py-0.5 text-[10px] font-medium text-amber-700">错误已兜底</span>
  )}
  <NodeRunStatusBadge status={status} />
</span>

// 版本卡选中态 + 线上徽标
<div className={cn('rounded-lg border bg-white transition', isSel ? 'border-stone-400 shadow-sm' : 'border-stone-200')}>
  <span className="font-mono text-[12px] font-semibold text-stone-800">v{v.version}</span>
  {v.version === publishedVersion && (
    <span className="rounded bg-emerald-50 px-1.5 py-0.5 text-[9.5px] font-medium text-emerald-700">线上</span>
  )}
</div>
```

## 适配指南

- Test Run 走 `runner.runTest`（流式、逐节点回投 canvas + 这里列出），Run 走 `runPersist`（写 call_logs）；二者共用 input，按 graphId 记忆到 localStorage
- 持久化执行只给最终结果，调试运行才有逐节点进度（`!runner.persisted`）
- 版本回滚是「恢复到草稿」语义——覆盖当前 draft，不自动发布（confirm 弹窗强调线上不受影响）
- diff 五组：草稿新增（emerald）/ 草稿已删（rose）/ 配置变更（amber）/ 新增连线（emerald）/ 删连线（rose）

## 反模式

- ❌ Test 和 Run 用同色钮——一个 primary 一个 outline 区分「调试 vs 写库」是关键
- ❌ 节点行不区分子图执行中 / 重试中 / 错误已兜底——这三态是工作流调试的核心反馈
- ❌ 版本卡选中态只加底色不加 border——`border-stone-400 + shadow-sm` 是选中的视觉锚
- ❌ diff 条目不分色——emerald / rose / amber 三色对应增 / 删 / 改，是可扫读的关键
