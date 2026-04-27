---
id: components/inputs/sage/sql-editor-monaco
type: component
name: SQL 编辑器
description: CodeMirror SQL 编辑器 + 主题色 active line / cursor / selection + Maximize2 全屏 Drawer 双视图（pagination ↔ list 可拉伸）
platforms: [web]
theme: light
tags:
  aesthetic: [minimal]
  mood: [calm, serious]
  stack: [react-antd-tailwind]
preview: /preview/components/inputs/sage/sql-editor-monaco
---

# SQL Editor (Monaco / CodeMirror)

> sage 全站只读 SQL 展示组件。inline 模式高 200px；点右上 Maximize2 进 Drawer 全屏，placement=right size=690，mask=false，shadow=transparent —— 看起来像贴在右侧滑出而不是覆盖。Drawer 顶部支持 pagination（多 SQL 上下翻页）/ list（列表逐条 + 拖拽改高度）两种切换。

## 主题色注入（最关键）

CodeMirror `EditorView.theme()` 注入主题色：
- `.cm-activeLine`：`backgroundColor: ${themeHex}15`（8% alpha 当前行底色）
- `.cm-activeLineGutter`：`backgroundColor: ${themeHex}20`，`color: ${themeHex}`
- `.cm-cursor`：`borderLeftColor: ${themeHex}`
- `.cm-selectionBackground`：`backgroundColor: ${themeHex}30`（18% alpha）
- 外层 `hover:border-${themeName}-400`（动态 className）

## Inline 模式

- 容器：`relative border border-slate-200 rounded-md overflow-hidden transition-colors hover:border-${themeName}-400`
- focus-within 还套 `themeClasses.borderFocusWithin`
- CodeMirror：`height=200px`，extensions=`[sql()]`，basicSetup（lineNumbers / foldGutter / autocompletion / bracketMatching）
- 右上角 Maximize2：`absolute right-4 top-0.5 z-10`，14px slate-400

## Drawer 全屏

- `<Drawer placement="right" size={690} closable={false} mask={false}>`
- 透明壳：`[&_.ant-drawer-content-wrapper]:!shadow-none [&_.ant-drawer-content]:!bg-transparent`
- styles：`{ body: { padding: 0, backgroundColor: 'transparent' }, wrapper: { boxShadow: 'none' } }`
- 内层 collapse handle（左侧 5px 宽 ChevronRight 触发收起）+ 主内容卡 `flex-1 flex flex-col h-full bg-white border-l border-gray-100 shadow-xl`

### Drawer Header
- `flex justify-between items-center px-4 py-3 bg-white border-b border-gray-100 shrink-0 relative`
- 左：`<span className="text-sm font-medium text-gray-700">SQL Preview</span>`
- 中：分页控件（条件 `sqlValues.length > 1 && layout === 'pagination'`）`absolute left-1/2 -translate-x-1/2 flex items-center gap-2` + ChevronLeft + `text-xs text-slate-500 font-mono` + ChevronRight
- 右：toolbar `flex items-center gap-1`
  - LayoutList / SquareStack 切换布局（list ↔ pagination）
  - Wand2 一键格式化（sql-formatter）
  - Copy / Check 复制（timeout 1500ms 切回 Copy）

### Drawer Editor 区
- 双布局：
  1. **list 模式**：`h-full overflow-y-auto`，每条 `border-b border-gray-100 last:border-0 relative flex flex-col`
     - 索引徽章：`absolute top-2 right-4 z-10 px-2 py-0.5 bg-slate-100 text-slate-500 text-xs rounded-full font-mono` "{idx+1}/{total}"
     - 拖拽手柄：`h-2 cursor-row-resize hover:bg-slate-200 absolute bottom-0 left-0 right-0 z-20 opacity-0 hover:opacity-100`，鼠标 down 进 `handleResizeStart`，写 `rowHeights[idx]`
  2. **pagination 模式**：单 CodeMirror `height=100%`

## 反模式

- ❌ Drawer 不要 closable=true —— sage 用左侧自定义 collapse handle，不显 antd 的 X
- ❌ 不要用 mask={true} —— 全屏 SQL 是辅助查看，不该遮住右侧空白让用户失去上下文
- ❌ list 模式不要禁用 cursor-row-resize —— 用户经常想把某条 SQL 拉高

## 视觉要点

1. **主题色 alpha 层级**：active line 15 / activeGutter 20 / selection 30 —— 三阶递增让"当前行 < 当前 gutter < 高亮选区"层次清晰
2. **font-mono 等宽数字**：`text-xs text-slate-500 font-mono` —— 索引 / 行号都走等宽
3. **shadow=transparent**：Drawer 不投影 —— 让 SQL 像直接贴在主内容右边
4. **drawer 内自定义 collapse handle**：5px 宽透明竖条 + 居中 ChevronRight，hover 才显灰

## 使用上游
- `agents/data-qa/components/QueryResult` 内嵌 inline 模式
- `agents/data-qa/pages/datasource/components/VectorTestModal` 内嵌
- 任何需要展示 SQL 的卡片
