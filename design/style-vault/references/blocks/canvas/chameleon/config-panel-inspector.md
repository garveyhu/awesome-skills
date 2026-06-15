---
id: blocks/canvas/chameleon/config-panel-inspector
type: block
name: 画布右侧节点配置 inspector + 条件 builder
description: 选中节点时悬浮画布右侧的配置面板 - 单行头部（类型配色图标块 + 纯文本观感名字输入 + 测试/更多/关闭）+「设置/上次运行」下划线 Tab + 折叠 Section + 输出变量只读区 + if_else 三态条件 builder（IF/ELSE 卡 + AND/OR 胶囊 + 多分支 CASE）+ 节点 hover 快捷条
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
- tokens/palettes/chameleon/node-type-hue-system
- tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/blocks/canvas/chameleon/config-panel-inspector
---

# 画布右侧节点配置 inspector + 条件 builder

> 选中画布节点时悬浮于右侧的配置 inspector：单行头部（类型配色图标块 + 像纯文本一样的名字输入 + 操作）+「设置 / 上次运行」下划线 Tab + 折叠 Section 分区 + 字段 + 输出变量只读区 + 异常处理区。内含 if_else 的三态条件 builder（简单 / 多分支 CASE / 高级 JSON）。配合画布节点的 hover 快捷条。

源码：`node-inspector.tsx` + `node-panel/panel-kit.tsx`（Section / OutputVarsSection）+ `node-panel/panel-tabs.tsx` + `if-else-condition.tsx` + `nodes/node-toolbar.tsx`。

## 视觉特征

### 悬浮外壳 + 头部

- **外层悬浮容器**（editor-page）：`bg-warm-2/95 absolute top-16 right-3 bottom-3 overflow-hidden rounded-xl border border-stone-200/70 shadow-xl backdrop-blur`
- **aside**：`relative flex h-full flex-col overflow-y-auto bg-white`，宽 320~640px 可拖（`usePanelResize`，默认 320）
- **左缘拖拽把手**：`absolute left-0 w-2 cursor-col-resize`，内竖条 `h-10 w-px rounded bg-slate-200 group-hover:h-16 group-hover:bg-blue-400`
- **header** `sticky top-0 z-10 border-b border-slate-200/80 bg-white/90 backdrop-blur-sm`，`flex items-center gap-3 px-5 pt-4 pb-2.5`：
  - 图标块 `h-9 w-9 rounded-xl shadow-sm ring-1` + 类型 `meta.bg` / `meta.color` / `meta.ring`，内图标 `h-[18px] w-[18px]`
  - 名字 Input `-ml-1.5 h-8 flex-1 rounded-md border-none bg-transparent px-1.5 text-[15px] font-semibold tracking-tight text-stone-900 hover:bg-slate-50 focus:bg-white focus:shadow-[inset_0_0_0_1px_rgb(59_130_246/0.35)]`（平时纯文本观感，focus 才显输入框）
  - 操作 `Play / MoreHorizontal / X` 各 `rounded-lg p-1.5 text-stone-400`，Play hover 蓝、关闭 hover 灰，X 前有 `mx-0.5 h-4 w-px bg-stone-200` 分隔
- **PanelTabs**（设置 / 上次运行）：`flex gap-5`，按钮 `py-2.5 text-[12.5px] font-semibold tracking-tight`，active `text-blue-600` + 底部下划线 `-bottom-px h-[2px] rounded-full bg-blue-500`，非 active `text-stone-400`

### Section 折叠分区（panel-kit）

- 标题按钮 `text-[10.5px] font-semibold tracking-[0.06em] uppercase text-stone-500` + `ChevronDown h-3 text-stone-300`（折叠时 `-rotate-90`）
- 折叠动画：`grid transition-all duration-200`，open `grid-rows-[1fr] opacity-100` / 收 `grid-rows-[0fr] opacity-0`
- **输出变量区**（OutputVarsSection，默认折叠）：每行 `flex gap-2 rounded-lg border border-slate-100 bg-slate-50/70 px-2.5 py-1.5`，`{x}` `font-mono text-[10px] text-violet-400` + 字段名 `font-mono text-[11.5px] text-stone-700` + 右侧 VarTypeChip

### if_else 条件 builder

- **ModeTab**（简单 / 多分支 / 高级 JSON）：`rounded px-1.5 py-0.5 text-[10.5px]`，active `bg-blue-100 text-blue-700`，非 `text-stone-400 hover:bg-stone-100`
- **IF / CASE 卡**：`rounded-xl border border-slate-200 bg-slate-50 p-2.5`
- **CaseBadge**：`rounded-md bg-amber-100 px-1.5 py-0.5 text-[10px] font-bold tracking-wide uppercase text-amber-700`（IF / ELIF）
- **条件行**：`rounded-lg border border-slate-200 bg-white p-2`，字段 Input `h-8 flex-1 font-mono text-[12px]` + EnumSelect `w-24`（中文算子下拉）+ 比较值 Input `h-8 font-mono text-[12px]`
- **AND/OR 胶囊**：`rounded-full border border-blue-200 bg-blue-50 px-2 py-px font-mono text-[9.5px] font-bold tracking-wide text-blue-600 hover:border-blue-300 hover:bg-blue-100`「且 AND」/「或 OR」
- **ELIF 添加**：`rounded-xl border border-dashed border-slate-300 bg-white py-1.5 text-[11px] text-stone-500 hover:border-blue-300 hover:text-blue-600` + `Plus h-3`
- **ELSE 卡**：`rounded-xl border border-dashed border-slate-200 bg-slate-50/60 px-2.5 py-2`，badge `rounded-md bg-slate-200 px-1.5 py-0.5 text-[10px] font-bold uppercase text-stone-500`
- key error：`border-rose-300 focus-visible:ring-rose-200` + `text-[10px] text-rose-500` 提示

### 节点 hover 快捷条（node-toolbar）

- 容器 `nodrag nopan absolute -top-9 right-0 z-10 flex h-7 gap-0.5 rounded-lg border border-stone-200/80 bg-white/95 px-1 py-0.5 shadow-card backdrop-blur`
- `invisible scale-95 opacity-0 group-hover:visible group-hover:scale-100 group-hover:opacity-100`（过渡浮现）
- 按钮 `h-6 w-6 rounded-md text-stone-500 hover:scale-110 hover:bg-stone-100 hover:text-stone-800 active:scale-95`，图标 `Play / Pencil / Copy / Trash2 h-3.5`
- 分隔 `mx-0.5 h-3.5 w-px bg-stone-200`，删除钮 hover `bg-rose-50 text-rose-600`

## 核心代码

```tsx
// 名字输入：纯文本观感，focus 才显蓝色内描边
className="... border-none bg-transparent text-[15px] font-semibold hover:bg-slate-50 focus:bg-white focus:shadow-[inset_0_0_0_1px_rgb(59_130_246/0.35)]"

// AND/OR 胶囊
<button className="rounded-full border border-blue-200 bg-blue-50 px-2 py-px font-mono text-[9.5px] font-bold text-blue-600 hover:bg-blue-100">
  {combo === 'and' ? '且 AND' : '或 OR'}
</button>

// Section 折叠动画
className={cn('grid transition-all duration-200', open ? 'mt-2.5 grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0')}
```

## 适配指南

- 任何「选中元素 → 右侧配置面板」场景套用（Dify workflow-panel 套路）
- 名字输入做成「平时像标题、hover 提示可编辑、focus 才像输入框」是低 AI 味关键
- 分区标题用克制的小号大写信号字（uppercase + tracking + 次级灰），靠留白呼吸而非粗分隔
- 条件 builder 三态（可视化简单 / 多分支 CASE / 高级 JSON）兜住从简到繁；可视化卡片用浅灰底 + IF/ELIF/ELSE badge 表达分支语义
- 输出变量只读区列字段 + 值类型 chip，供下游引用 —— Dify 级信号特征

## 反模式

- ❌ 名字用普通边框 input —— 失去「像标题」的克制感
- ❌ 分区用粗分隔线堆叠 —— 用留白 + 小号大写标题
- ❌ 条件只给裸 JSON 编辑 —— 提供可视化 IF/ELSE 卡 + AND/OR 胶囊
- ❌ hover 快捷条常驻 —— group-hover 浮现（invisible → visible + scale）
- ❌ 删除项不转红 —— 危险操作统一 rose
