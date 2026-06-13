---
id: blocks/canvas/chameleon/bezier-edge-add
type: block
name: 平滑贝塞尔连线 + 边中点加节点
description: 对齐 Dify/FastGPT 的画布连线 - 平滑贝塞尔（curvature 0.2）替代直角折线，stone 灰默认 / 主题 primary 流动高亮 / fail rose 红虚线 + 失败标签 / 焦点外淡化；hover 边中点出现「+」点开节点选择菜单就地 split 插入
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
- blocks/canvas/chameleon/node-palette
- tokens/motion/chameleon/canvas-edge-dash-flow
- tokens/palettes/chameleon/node-type-hue-system
preview: /preview/blocks/canvas/chameleon/bezier-edge-add
---

# 平滑贝塞尔连线 + 边中点加节点

> 工作流画布的连线层：替换 React Flow 内置 smoothstep 直角折线为平滑贝塞尔（curvature 0.2）。默认 stone 灰细线，选中 / 相邻节点高亮时主题 primary 加粗 + 流动虚线，焦点链路外淡化，fail 分支 rose 红虚线 + 「失败」标签。hover 边中点出现「+」按钮，点开节点选择菜单就地 split 插入。

源码：`src/system/graphs/components/nodes/graph-edge.tsx`（`GraphEdge` / `GraphConnectionLine`）+ `nodes/edge-insert-menu.tsx`（`EdgeInsertMenu`）。

## 视觉特征

### 连线（GraphEdge）

- **EDGE_COLOR**：normal `#d6d3d1`（stone-300）/ active `var(--color-primary-500)`（主题色，默认蓝 `#3b82f6`）/ fail `#fb7185`（rose-400）/ failActive `#f43f5e`（rose-500）
- **CURVATURE 0.2**（getBezierPath），source 右出、target 左入
- **strokeWidth**：active `2.25` / 默认 `1.5`
- **strokeDasharray**：相邻高亮（connected）`'6 4'`、fail `'5 3'`、纯选中保持实线（undefined）
- **opacity**：dimmed（焦点外）`0.35`，否则 `1`；过渡 `stroke 150ms / stroke-width 150ms / opacity 150ms`
- **透明加宽交互路径**：同 path、`stroke transparent` `strokeWidth 20`，扩大 hover 命中区驱动「+」显隐
- **markerEnd**：`ArrowClosed` 14×14 `#d6d3d1`
- **fail 标签**：`rounded-full border border-rose-200 bg-rose-50 px-1.5 py-px font-mono text-[9px] leading-tight text-rose-500`「失败」，定位边中点（有「+」时上移 16px 让位）

### 拖拽连接线（GraphConnectionLine）

- 主题 active 色贝塞尔 path、`strokeWidth 2`、`strokeDasharray '5 3'`
- 目标端竖向锚点 `circle r3` 白底 + active 描边 `strokeWidth 1.5`

### 「+」按钮 + 插入菜单（EdgeInsertMenu）

- **「+」按钮** `h-5 w-5 rounded-full border shadow-sm`（20px 圆）：
  - 闭：`border-stone-300 bg-white text-stone-500 hover:scale-110 hover:border-blue-300 hover:text-blue-600`
  - 开：`border-blue-300 bg-blue-50 text-blue-600`
  - 内 `Plus h-3`，仅 hover / 菜单展开时 `opacity 1`（否则 0，120ms 过渡）
- **插入菜单**（portal 到 body）：`fixed z-[1000] w-60 flex flex-col overflow-hidden rounded-xl border border-stone-200/80 bg-white shadow-xl ring-1 ring-stone-900/5`
  - 搜索框 `h-7 rounded-lg border border-stone-200 bg-stone-50 pl-7 pr-2 text-[11.5px] focus:border-blue-300 focus:bg-white focus:ring-1 focus:ring-blue-200` + `Search h-3.5 text-stone-400`
  - 分组标题 `text-[9.5px] font-semibold tracking-wide text-stone-400`
  - 节点行 `flex gap-2 rounded-lg px-1.5 py-1.5 hover:bg-stone-50`：图标块 `h-6 w-6 rounded-md ring-1 ring-stone-900/5 group-hover:scale-105` + 类型 bg/color，名 `text-[11.5px] font-medium text-stone-700`

## 核心代码

```tsx
const EDGE_COLOR = { normal: '#d6d3d1', active: 'var(--color-primary-500)', fail: '#fb7185', failActive: '#f43f5e' };
const CURVATURE = 0.2;
const [edgePath, labelX, labelY] = getBezierPath({ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition, curvature: CURVATURE });

const stroke = isFail ? (active ? EDGE_COLOR.failActive : EDGE_COLOR.fail) : (active ? activeColor : EDGE_COLOR.normal);
const dashArray = isFail ? '5 3' : connected ? '6 4' : undefined;
<BaseEdge style={{ stroke, strokeWidth: active ? 2.25 : 1.5, strokeDasharray: dashArray, opacity: dimmed ? 0.35 : 1 }} />
```

## 适配指南

- 任何 React Flow 画布连线要「高级感」就用贝塞尔（curvature 0.2）而非内置 smoothstep 折线
- 连线主色走 CSS 变量随主题切换；灰 / 红走固定 token
- 相邻高亮（焦点节点的相连边）走流动虚线动画凸显方向；纯边点选保持实线
- fail 分支统一 rose 红虚线 + 小标签，是「这条路失败时走」的语义信号
- 「+」按钮克制：仅 hover / 展开可见，对齐 Dify custom-edge 套路

## 反模式

- ❌ 用直角折线（smoothstep）—— 显工程师草图、不够顺滑
- ❌ 连线全用一个颜色 —— 丢掉选中 / 相邻 / fail / dimmed 四态语义
- ❌ 「+」按钮常驻可见 —— 画布会很吵，只在 hover 边时浮现
- ❌ 插入菜单留在边层 —— 会被节点层盖住，必须 portal 到 body 用 fixed 定位
- ❌ markerEnd 用默认大箭头 —— 这里是克制的 14×14 灰箭头
