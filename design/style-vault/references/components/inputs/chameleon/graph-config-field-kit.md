---
id: components/inputs/chameleon/graph-config-field-kit
type: component
name: 画布节点配置控件套件
description: Dify 式工作流节点 inspector 的六件套配置控件——提示词消息块 / 变量树选择器 / 常量·变量二态段控 / 列声明表格编辑器 / CodeMirror 单字段 / 滑块数字联动
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
- tokens/palettes/chameleon/node-type-hue-system
preview: /preview/components/inputs/chameleon/graph-config-field-kit
---

# 画布节点配置控件套件

> Chameleon 工作流画布节点 inspector 的招牌配置控件套件，逐件对标 Dify workflow-panel——六件套（提示词消息块 / 变量树选择器 / 常量·变量二态段控 / 列声明表格编辑器 / CodeMirror 单字段 / 滑块数字联动）共用 `ControlField` 标签外壳，统一「克制但精致」的字段密度。signature 在第一件：角色头行 + CodeMirror 文本区融成一张 `rounded-xl` 卡，`{{#node.field#}}` 引用经 `MatchDecorator` 渲染成蓝底圆角 chip，focus 时整卡 `0 0 0 3px rgb(59 130 246/0.10)` 蓝环。

## 视觉特征

### 通用标签外壳 ControlField
- 标签行 `mb-1.5 flex min-h-[16px] items-center gap-1`，label `text-[11px] font-semibold tracking-[0.01em] text-stone-700`，required 红星 `text-[11px] text-rose-500`，`right` 槽 `ml-auto`
- description `mt-1.5 text-[10.5px] leading-relaxed text-stone-400`，error 同字号 `text-rose-500`

### A·提示词消息块（PromptEditor，signature）
- 外壳 `overflow-hidden rounded-xl border border-slate-200 bg-white shadow-[0_1px_2px_rgb(0_0_0/0.03)]`，focus `focus-within:border-blue-300 focus-within:shadow-[0_0_0_3px_rgb(59_130_246/0.10)]`
- 头行 `flex items-center gap-2 bg-slate-50/80 px-3 py-1.5`：角色标签 `text-[10px] font-semibold tracking-[0.07em] uppercase text-stone-500`，字数 `ml-auto text-[10px] text-stone-300 tabular-nums`「N 字」，末尾跟变量按钮
- 编辑区 CodeMirror：正文 `12.5px` / mono 模式 `12px`，行高 `1.7`，内边距 `9px 12px`
- 变量 chip 三段 mark：背景 `#eff6ff`(blue-50)、font-mono `11px`、上下 padding `1.5px`；定界符 `{{#`/`#}}` 用 `#93c5fd`(blue-300)，变量名 `#2563eb`(blue-600) `font-weight:500`；首段 `border-radius:5px 0 0 5px;padding-left:4px`，尾段 `border-radius:0 5px 5px 0;padding-right:4px`
- PromptField 高度 = `rows * 21 + 20`px 作 minHeight

### B·变量树选择器（VarTreePicker，见 uses）
- 触发 `inline-flex items-center gap-1 rounded-md border border-slate-200 bg-white text-stone-500 hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600`；sm=`px-1.5 py-0.5 text-[10.5px]`，md=`px-2 py-1 text-[11.5px]`；`Braces h-3 w-3` + `ChevronDown h-3 w-3 opacity-50`
- Popover `w-64 p-0`；搜索行 `border-b border-stone-100 px-2.5 py-1.5`，`Search h-3 w-3 text-stone-300`；列表 `max-h-72`

### C·常量·变量二态段控（ConstVarSwitch / ConstVarField）
- 段控 `inline-flex items-center gap-px rounded-lg bg-slate-100 p-0.5`；按钮 `rounded-md px-1.5 py-1`，active `bg-white text-stone-700 shadow-sm`，idle `text-stone-400 hover:text-stone-600`；图标 `Pencil`(常量)/`Braces`(变量) `h-3 w-3`
- 变量态 chip `inline-flex min-w-0 items-center gap-1 rounded-md border border-violet-200 bg-violet-50 px-2 py-1 text-[11px] text-violet-700`，`Braces h-3 w-3 text-violet-400` + `truncate font-mono` 变量名
- 未选态 `rounded-md border border-dashed border-slate-300 bg-slate-50/60 px-2 py-1.5`，「未选择变量」`text-[11px] text-stone-400`

### D·列声明表格编辑器（TableEditor）
- 行卡 `space-y-1 rounded-lg border border-slate-200 bg-white p-2 shadow-[0_1px_0_rgba(0,0,0,0.02)] hover:border-slate-300`
- 序号 `flex h-4 w-4 items-center justify-center rounded bg-stone-100 font-mono text-[10px] text-stone-500`
- Cell Input `h-6 text-[11px]`；fullRow 列单独占行 `pl-5`
- 排序按钮 `ArrowUp/ArrowDown` `h-3 w-3 text-stone-400 hover:bg-stone-100 hover:text-stone-700 disabled:opacity-30`，`X` `hover:bg-rose-50 hover:text-rose-600`
- 添加行 `border border-dashed border-slate-300 bg-slate-50/60 py-1.5 text-[11px] font-medium text-stone-500 hover:border-blue-300 hover:bg-blue-50 hover:text-blue-600` + `Plus h-3.5 w-3.5`
- 空态 `border border-dashed border-slate-200 px-2 py-2 text-center text-[10.5px] text-stone-400`

### E·CodeMirror 单字段（CodeEditorField）
- 外壳 `overflow-hidden rounded-lg border bg-white focus-within:ring-2 focus-within:ring-blue-100`；正常 `border-slate-200 focus-within:border-blue-300`，error `border-rose-300 focus-within:border-rose-400`
- langBadge 行 `border-b border-slate-100 bg-slate-50 px-2 py-1`，badge `rounded bg-slate-100 px-1.5 py-px font-mono text-[9.5px] uppercase tracking-wide text-stone-400`
- 编辑器字号 `11.5px`，等宽 `ui-monospace`，gutters 透明 `#d6d3d1`(stone-300)，content padding `6px 0`；basicSetup 开 lineNumbers + highlightActiveLine + bracketMatching

### F·滑块数字联动（SliderField）
- 数字框 Input（放 ControlField `right` 槽）`h-6 w-20 text-right font-mono text-[11.5px] tabular-nums`
- range `mt-0.5 w-full cursor-pointer accent-blue-600`，undefined 态加 `opacity-60`
- 刻度行 `mt-0.5 flex justify-between text-[9.5px] tabular-nums text-stone-400` 显 min/max

## 核心代码

```tsx
// A·提示词消息块外壳 + chip 高亮
<div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-[0_1px_2px_rgb(0_0_0/0.03)] transition focus-within:border-blue-300 focus-within:shadow-[0_0_0_3px_rgb(59_130_246/0.10)]">
  <div className="flex items-center gap-2 bg-slate-50/80 px-3 py-1.5">
    <span className="truncate text-[10px] font-semibold tracking-[0.07em] uppercase text-stone-500">{label}</span>
    <span className="ml-auto text-[10px] text-stone-300 tabular-nums">{value.length} 字</span>
    <VarTreePicker onInsert={insertAtCursor} nodeVars={nodeVars} />
  </div>
  <CodeMirror {...} basicSetup={BASIC_SETUP} />
</div>

// chip 三段 mark（MatchDecorator /\{\{#([^#}]+)#\}\}/g）
'.cm-pvar':       { backgroundColor: '#eff6ff', fontFamily: 'ui-monospace', fontSize: '11px', paddingTop: '1.5px', paddingBottom: '1.5px' }
'.cm-pvar-brace': { color: '#93c5fd' }
'.cm-pvar-name':  { color: '#2563eb', fontWeight: '500' }
'.cm-pvar-open':  { borderRadius: '5px 0 0 5px', paddingLeft: '4px' }
'.cm-pvar-close': { borderRadius: '0 5px 5px 0', paddingRight: '4px' }

// C·二态段控
<div className="inline-flex shrink-0 items-center gap-px rounded-lg bg-slate-100 p-0.5">
  <button className={active ? 'bg-white text-stone-700 shadow-sm' : 'text-stone-400 hover:text-stone-600'}><Pencil className="h-3 w-3" /></button>
  <button ...><Braces className="h-3 w-3" /></button>
</div>
```

## 适配指南
- 字段壳一律走 `ControlField`（label/required/tip/description/error/right），不要散写 `<label>` —— `right` 槽专放变量按钮 / 二态段控
- 变量按钮永远复用 `VarTreePicker`（行内用 `size="sm"`），不要重写下拉
- LLM 节点参数（temperature/top_k）走 SliderField；运营/全站非节点场景用 `param-slider`（accent-amber-600 暖色款，区别开）
- code 节点 / JSON schema 用 CodeEditorField；提示词 / template / Answer 用 PromptEditor 消息块
- TableEditor 用 `ColumnSpec[]` 声明列（text/select/bool + withVars + fullRow），不要为每个节点手写表格

## 反模式
- ❌ 提示词块用 widget 替换变量 chip —— 必须用 `Decoration.mark`（mark 装饰），否则光标进不去 chip 逐字编辑
- ❌ chip 用纯 blue-500 实心 —— 是 blue-50 浅底 + blue-300 定界符 + blue-600 名，三段分色
- ❌ 二态段控变量 chip 用蓝色 —— 变量态统一 violet（border-violet-200 / bg-violet-50 / text-violet-700），与提示词内 chip 的蓝区分语义
- ❌ SliderField 滑块用 amber —— 节点配置滑块是 `accent-blue-600`，amber 是 param-slider 专属
- ❌ 把外壳 radius 写成 lg(8px) —— 提示词消息块是 `rounded-xl`(12px)，CodeEditor/TableEditor 行卡才是 `rounded-lg`(8px)
