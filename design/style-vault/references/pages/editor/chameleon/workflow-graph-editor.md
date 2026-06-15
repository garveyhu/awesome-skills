---
id: pages/editor/chameleon/workflow-graph-editor
type: page
name: 工作流画布编辑器（全屏三栏 + React Flow 画布）
description: Chameleon 最大 signature 表面——左应用 rail + 中 React Flow 冷白点阵画布(贝塞尔连线 + 类型色节点卡 + 浮控群 + 右键菜单) + 右悬浮 inspector/AI 助手(z 竞争互斥)；编排/监测 Tab + 全套调试闭环
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
- blocks/canvas/chameleon/ai-copilot-panel
- blocks/canvas/chameleon/bezier-edge-add
- blocks/canvas/chameleon/canvas-controls-menus
- blocks/canvas/chameleon/config-panel-inspector
- blocks/canvas/chameleon/graph-node-card
- blocks/canvas/chameleon/node-palette
- blocks/canvas/chameleon/subflow-group-editor
- blocks/form/chameleon/graph-run-dialog
- blocks/nav/chameleon/detail-left-tab-rail
- tokens/motion/chameleon/canvas-edge-dash-flow
- tokens/palettes/chameleon/node-type-hue-system
preview: /preview/pages/editor/chameleon/workflow-graph-editor
---

# Chameleon Workflow Graph Editor

> Chameleon 最大的 signature 表面（`/graphs/:id/edit`）——对标 Dify / FastGPT 的全屏工作流编辑器。根 `flex h-screen bg-[var(--color-warm)]`：**左** GraphAppRail（w-64 白栏：应用头 返回/图标/名称/形态切换/key/发布状态/保存状态 + 二级导航 编排/监测 + Web App / 后端服务 API 卡片）+ **中** React Flow 画布（`absolute inset-0 bg-slate-50` 冷白替暖白外壳 + 点阵底 + 贝塞尔连线 + 类型色节点卡 + 浮层控件群 + 右键菜单）+ **右** 悬浮 inspector / AI 编排助手（top-16 right-3 bottom-3 圆角浮卡，z 竞争互斥，失焦露角）。Tab 切「编排」/「监测」。全套调试闭环：单节点测试 / 整图运行 / 对话调试 + 发布 / 版本 / 导入导出 / AI 编排 / checklist 体检。waveflow 无画布编辑器，整页 new。

## 视觉特征

- 根 `flex h-screen bg-[var(--color-warm)]`
- **左 GraphAppRail** `w-64 shrink-0 border-r border-slate-200/80 bg-white`：应用头 `border-b p-3.5`——返回 ChevronLeft `text-[11.5px]` + 收起 ChevronsLeft；图标块 `h-9 w-9 rounded-xl ring-1`（chat violet-50/600 / workflow sky-50/600）+ 名称 `text-[13px] font-semibold` + key `font-mono text-[10.5px] text-stone-400`；形态切换 KindSelect `h-6 w-[88px]` + 发布徽标（v3 emerald-50/700 ring / 草稿 amber-50/700 ring）+ 保存状态点（保存中 blue-400 animate-pulse / 未保存 amber-400 / 已保存 stone-300）；二级导航 `p-2`，每项 `rounded-lg py-1.5 pr-2.5 pl-3 text-[12.5px] font-medium`，active `bg-blue-50 text-blue-700` + 左侧色条 `w-[3px] rounded-full bg-blue-500`；应用卡片区 `bg-slate-50/40 p-2.5`，卡 `rounded-xl border border-slate-200/80 bg-white p-3 shadow-sm`
- **中画布**：容器 `absolute inset-0 bg-slate-50`（pendingType 时 cursor-copy）；ReactFlow 配 `selectionOnDrag / panOnDrag={[1]}(中键) / panOnScroll / SelectionMode.Partial / selectNodesOnDrag={false}`；defaultEdgeOptions `type:'graphEdge'` + ArrowClosed `14×14 #d6d3d1`；connectionLineComponent GraphConnectionLine
- Background `variant Dots gap 16 size 1 color var(--color-slate-200)`（浅冷灰点阵）
- 节点卡（GraphNode）`min-w-[180px] rounded-[14px] border px-2.5 pb-2 pt-2 text-[11.5px]` + meta.cardTint（整卡极淡类型色温底，如 `bg-violet-50/40`，无白板感、无色块分界）+ `shadow-soft hover:-translate-y-px hover:shadow-card`；选中 `ring-2 ring-offset-2 ring-offset-warm`（meta.ring）；图标块 `h-[26px] w-[26px] rounded-[9px] ring-1 ring-inset ring-stone-900/5`（meta.bg）含 icon `h-3.5 w-3.5`（meta.color）；标题 `text-[12.5px] font-semibold tracking-tight text-stone-800` + 类型副标 `text-[9.5px] font-medium uppercase`（meta.color）；handle 小圆点 `!h-2.5 !w-2.5 !rounded-full !border-[1.5px] !bg-white` hover 放大到 14px
- 连线：贝塞尔 curvature 0.2，默认 stone-300 1.5px，相邻高亮 6/4 流动虚线 2.25px（焦点类型色），fail 5/3 rose 静态虚线 + 「失败」标签；边中点 hover 出「+」插入菜单
- **浮控群**：左上 NodePalette（收起 `h-8 w-8 rounded-lg bg-white/95` Plus / 展开 `w-[21rem] rounded-2xl shadow-xl` 双列 Tab）；左上运行状态条 `rounded-lg bg-white/90 px-2.5 py-1 shadow-md backdrop-blur`；右上工具条 `rounded-xl bg-white/85 px-2 py-1.5 shadow-md backdrop-blur`（checklist 徽标 + AI Sparkles + 日志 History + 更多 MoreHorizontal + 运行/对话调试 + 保存 + 发布 split button）；右下 MiniMap `!bg-warm-2`（inspector 开时 right 340 否则 12）+ ZoomControl；左下撤销/重做 `rounded-lg bg-white/95 shadow-md backdrop-blur`
- **右悬浮面板**：`absolute top-16 right-3 bottom-3 rounded-xl border border-stone-200/70 shadow-xl`，inspector `bg-warm-2/95 backdrop-blur` / copilot `bg-white`；z 竞争 topPanel 决定 z-20/z-10，失焦面板 `translate-x-[-14px] translate-y-[10px]` 露角
- 点击放置幽灵：`pointer-events-none fixed z-50` 虚线卡 `border-2 border-dashed bg-white/95 px-2.5 py-1.5 shadow-lg`（类型 icon + label + 「点击画布放置 · Esc 取消」）跟随光标
- 右键菜单：`shadow-pop fixed z-50 min-w-[176px] rounded-lg border border-stone-200 bg-white py-1`，节点 / 多选 / 空白三态
- 节点类型 hue（TYPE_META）：start emerald · end stone · llm violet · image_gen purple · kb emerald · tool orange · if_else amber · classifier 多出口 lime …（color 700 阶文字 / bg 50 阶图标块 / cardTint 50/40 整卡色温 / ring 200 阶选中环 / edgeColor 500 阶连线高亮）

## 核心代码

```tsx
<div className="flex h-screen bg-[var(--color-warm)]">
  <GraphAppRail graph={graph} kind={kind} tab={tab} onTab={setTab} dirty={dirty} saving={saving} />
  <div className="flex min-w-0 flex-1 flex-col">
    {tab === 'orchestrate' && (
      <div className="relative min-h-0 flex-1">
        <div ref={rfWrapperRef} className={cn('absolute inset-0 bg-slate-50', pendingType && 'cursor-copy')}>
          <ReactFlow nodes={nodes} edges={displayEdges} nodeTypes={NODE_TYPES} edgeTypes={EDGE_TYPES}
            defaultEdgeOptions={{ type: 'graphEdge', markerEnd: { type: MarkerType.ArrowClosed, width: 14, height: 14, color: '#d6d3d1' } }}
            connectionLineComponent={GraphConnectionLine}
            selectionOnDrag panOnDrag={[1]} panOnScroll selectionMode={SelectionMode.Partial} selectNodesOnDrag={false}>
            <Background variant={BackgroundVariant.Dots} gap={16} size={1} color="var(--color-slate-200)" />
            <MiniMap className="!bg-warm-2" position="bottom-right" style={{ right: selectedSpec ? 340 : 12, bottom: 50 }} />
            <Panel position="bottom-right"><ZoomControl … /></Panel>
          </ReactFlow>

          {/* 右上浮控工具条 */}
          <div className="absolute top-3 right-3 z-20 flex items-center gap-1.5 rounded-xl border border-stone-200/70 bg-white/85 px-2 py-1.5 shadow-md backdrop-blur">…</div>

          {/* 右悬浮 inspector / copilot —— z 竞争互斥 */}
          {selectedSpec && (
            <div onMouseDownCapture={() => setTopPanel('inspector')}
              className={cn('bg-warm-2/95 absolute top-16 right-3 bottom-3 rounded-xl border border-stone-200/70 shadow-xl backdrop-blur',
                topPanel === 'inspector' ? 'z-20' : 'z-10',
                aiGenOpen && topPanel !== 'inspector' && 'translate-x-[-14px] translate-y-[10px]')}>
              <NodeInspector … />
            </div>
          )}
          <NodePalette kind={kind} onAdd={t => setPendingType(t)} />
        </div>
      </div>
    )}
    {tab === 'monitor' && <ObserveView … />}
  </div>
</div>
```

## 适配指南

- 画布外壳故意用 `bg-slate-50`（冷白）替全站暖白——配浅冷灰点阵 `var(--color-slate-200)` 更清爽，对齐 Dify/FastGPT；左 rail / 节点卡仍走暖系
- 节点类型色靠 cardTint「整卡染色」而非左色条 / 色块——色彩是卡片自身表面色，无任何分界缝；更强类型信号由彩色图标块 + 类型副标题色承载
- inspector 与 copilot 都钉右侧 `top-16 right-3 bottom-3`，共存时靠 z 竞争（点谁谁 z-20）+ 失焦错位露角（`-translate-x-14 +translate-y-10`），不并排挤画布
- 浮控群全用半透明白 + backdrop-blur（`bg-white/85` ~ `/95`）浮在画布上，不抢点阵底
- 中键拖平移（panOnDrag=[1]），右键留给上下文菜单；左键拖空白 = 框选（Partial 碰边即选）
- 发布用 split button（主体直接发布 + 下拉收「发布为智能体」/「版本历史」）；运行 / 对话调试按 kind 二选一

## 反模式

- ❌ 画布用暖白底——这是唯一用冷白 slate-50 的表面，配冷灰点阵才有「专业画布」感
- ❌ 节点类型用左色条 / 左色块——有边界的色块产生「白卡旁一块彩色」的隔阂感，必须 cardTint 整卡染色
- ❌ inspector 和 copilot 并排各占一栏——共存靠 z 竞争 + 露角，保画布最大可视
- ❌ 浮控用实色卡——必须半透明 + backdrop-blur，让画布点阵透出
- ❌ 节点卡 hover 放大 scale——只许 `-translate-y-px`，放大会和邻居重叠
- ❌ 连线用直角折线——贝塞尔 curvature 0.2，对齐 Dify/FastGPT 曲线质感
