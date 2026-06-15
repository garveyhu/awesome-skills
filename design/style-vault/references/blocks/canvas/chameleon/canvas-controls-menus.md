---
id: blocks/canvas/chameleon/canvas-controls-menus
type: block
name: 画布角落浮层控件 + 三态右键菜单
description: 工作流画布的白卡浮层控件全套（左下撤销重做 / 右下缩放栏 / 左上运行状态徽标 + 节点幽灵 / 右上工具栏 checklist 徽标 + 发布 split button）+ 节点/多选/空白三态右键菜单（对齐分布 + 快捷键标注 + 危险红删除）
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
- tokens/shadow/waveflow/soft-card-pop-trio
preview: /preview/blocks/canvas/chameleon/canvas-controls-menus
---

# 画布角落浮层控件 + 三态右键菜单

> 工作流画布四角的浮层控件群 + 右键三态语境菜单。统一 `rounded-lg border border-stone-200/80 bg-white/95 shadow-md backdrop-blur` 的白卡浮层语言；右键菜单按 节点 / 多选 / 空白 三态切换内容。

源码：`graph-editor-page.tsx`（缩放 / 撤销 / 状态徽标 / 节点幽灵 / 右上工具栏 + 三态右键菜单）+ `zoom-control.tsx` + `checklist-badge.tsx` + `helper-lines.tsx`。

## 视觉特征

### 浮层控件（白卡语言）

- **撤销 / 重做栏**（左下）：`flex gap-0.5 rounded-lg border border-stone-200/80 bg-white/95 px-1 py-1 shadow-md backdrop-blur`，按钮 `h-6 w-6 rounded text-stone-500 hover:bg-stone-100 hover:text-stone-800 disabled:opacity-35` + `Undo2 / Redo2 h-3.5`
- **缩放栏**（右下，同款白卡）：`Maximize2`（全屏自适应）/ `LayoutGrid`（自动整理）`h-3.5` + 分隔 `mx-0.5 h-3.5 w-px bg-stone-200/80` + `Minus` + 百分比 `min-w-[40px] text-center font-mono text-[11px] tabular-nums text-stone-600` + `Plus`
- **运行状态徽标**（左上）：`rounded-lg border border-stone-200/70 bg-white/90 px-2.5 py-1 text-[11.5px] shadow-md backdrop-blur`
  - running：蓝点 `h-1.5 w-1.5 animate-pulse rounded-full bg-blue-500` + `text-blue-600`「运行中…」
  - success：`text-emerald-600`「✓ 运行成功 · Nms」
  - failed：`text-rose-600`「✗ 运行失败」
  - paused：`text-amber-600`「⏸ 已暂停」
- **节点幽灵**（跟随光标）：`rounded-md border-2 border-dashed bg-white/95 px-2.5 py-1.5 text-[11.5px] font-medium` + 类型 color + 图标 `h-3.5` + `text-[10px] text-stone-400`「点击画布放置 · Esc 取消」
- **右上工具栏**：`rounded-xl border border-stone-200/70 bg-white/85 px-2 py-1.5 shadow-md backdrop-blur`，含 checklist 徽标 + AI(`Sparkles`)/日志(`History`)/更多(`MoreHorizontal`) ghost 钮 + 测试 / 保存 outline 钮 + 发布 split button
- **checklist 徽标** `h-7 w-7 rounded-md hover:bg-stone-100`：error → `h-4 min-w-4 rounded-full bg-rose-500 px-1 font-mono text-[9.5px] font-semibold text-white` 数字胶囊 / warning → `bg-amber-400` 数字胶囊 / ready → `CheckCircle2 h-3.5 text-emerald-500` / checking → 蓝点 `h-2 w-2 animate-pulse bg-blue-400` / idle → `Minus h-3 text-stone-300`
- **发布 split button**：主钮 `rounded-r-none` + `Rocket`；副钮 `rounded-l-none border-l border-white/25 px-1.5` + `ChevronDown opacity-80` 下拉
- **HelperLines**：canvas 画主题 `--color-primary-500` 线（lineWidth 1）+ 端点叉（CROSS_SIZE 4），`pointer-events:none`

### 三态右键菜单

- 容器 `shadow-pop fixed z-50 min-w-[176px] overflow-hidden rounded-lg border border-stone-200 bg-white py-1`
- `MENU_BTN`：`flex w-full gap-2 px-3 py-1.5 text-left text-[12.5px] text-stone-700 hover:bg-stone-100 disabled:text-stone-300`，图标 `h-3.5 w-3.5 text-stone-400`，快捷键 `ml-auto text-[10px] text-stone-300`
- 删除项叠 `text-rose-600 hover:bg-rose-50`
- `MENU_SEP`：`my-1 h-px bg-stone-100`
- `MENU_LABEL`：`px-3 pt-1 pb-0.5 text-[10px] font-medium tracking-wide text-stone-400`（「已选 N 个节点」/「对齐」/「分布」）
- 节点态：复制 ⌘C / 粘贴 ⌘V / 创建副本 ⌘D / 测试此节点 / 删除节点 ⌫
- 多选态：复制 / 创建副本 / 对齐 6 行（`AlignStartVertical` … `AlignEndHorizontal`）/ 水平垂直均分 / 批量删除
- 空白态：粘贴 / 在此处添加大模型节点 / 自动整理布局

## 核心代码

```tsx
// 统一白卡浮层（缩放 / 撤销 / 状态徽标共用）
'rounded-lg border border-stone-200/80 bg-white/95 px-1 py-1 shadow-md backdrop-blur'

const MENU_BTN = 'flex w-full items-center gap-2 px-3 py-1.5 text-left text-[12.5px] text-stone-700 transition hover:bg-stone-100 disabled:cursor-not-allowed disabled:text-stone-300';
const MENU_SEP = 'my-1 h-px bg-stone-100';
const MENU_LABEL = 'px-3 pt-1 pb-0.5 text-[10px] font-medium tracking-wide text-stone-400';
```

## 适配指南

- 任何画布 / 编辑器的角落控件统一这一套白卡语言（`bg-white/95 + shadow-md + backdrop-blur`），别一处一个样
- 状态徽标用「点 + 一句话」表达运行态，颜色按 running 蓝 / success 绿 / failed 红 / paused 琥珀
- 右键菜单按上下文三态切换内容，快捷键右对齐用 `text-stone-300` 极淡灰
- 删除 / 批量删除项一律转 rose 红（hover `bg-rose-50`），与中性项区分

## 反模式

- ❌ 控件卡用不透明纯白 —— 失去画布上「浮层」的层次（要 `bg-white/95 + backdrop-blur`）
- ❌ 右键菜单不分态全堆一起 —— 节点 / 多选 / 空白上下文不同，按场景给项
- ❌ 快捷键标注用深色 —— 用 `text-stone-300` 极淡，是辅助信息不抢主项
- ❌ checklist 徽标加多余清单图标 —— 状态本身就是图标（绿勾 / 红数 / 黄数 / 蓝点）
- ❌ 发布按钮做成普通单钮 —— split button 主钮发布 + 下拉收次要项（发布为智能体 / 版本历史）
