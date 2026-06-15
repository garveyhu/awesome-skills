---
id: tokens/motion/chameleon/canvas-edge-dash-flow
type: token
name: 画布连线流动 + 面板方向滑入运动
description: 工作流画布专属运动——相邻高亮边 6/4 流动虚线 + 150ms stroke/width/opacity 过渡、fail 边 5/3 静态虚线、palette/copilot fade-in 方向滑入、node hover 微浮起 + handle 放大
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
uses: []
preview: /preview/tokens/motion/chameleon/canvas-edge-dash-flow
---

# Chameleon Canvas Edge Dash Flow

> Chameleon 工作流画布（React Flow）专属的连线 / 面板 / 节点运动集。区别于 waveflow 的 keyframes-suite（shimmer / pulse / halo 等通用动效），这套全部围绕「画布」语境：相邻边走 6/4 流动虚线、失败分支走 5/3 静态虚线、节点 hover 微浮起 1px、handle hover 放大、palette / copilot 面板从左 / 从右 fade-in 滑入。每条都 150ms 上下、ease，**克制有反馈不喧哗**。

## Tokens

```json
{
  "edge-transition": {
    "value": "stroke 150ms ease, stroke-width 150ms ease, opacity 150ms ease",
    "用法": "graph-edge BaseEdge style.transition —— 边的色 / 粗细 / 透明度全部 150ms ease 过渡，选中 / 高亮 / 淡化切换不闪"
  },
  "edge-highlighted-dash": {
    "strokeDasharray": "6 4",
    "strokeWidth": "2.25 (active) / 1.5 (默认)",
    "color": "焦点节点类型 hue 500 阶 hex（缺省回退 var(--color-primary-500)）",
    "用法": "相邻节点被选中 / hover 时，其链路边走 6/4 流动虚线 + 加粗，凸显数据流方向"
  },
  "edge-fail-dash": {
    "strokeDasharray": "5 3",
    "color": "#fb7185 (rose-400 默认) / #f43f5e (rose-500 active)",
    "用法": "error_strategy=fail_branch 的失败分支边 —— 静态 5/3 虚线（非流动），红色，带「失败」rose 标签"
  },
  "edge-dimmed": {
    "opacity": "0.35",
    "用法": "存在焦点节点但本边不在其链路 → 淡化降透明，让焦点链路更突出"
  },
  "edge-curvature": {
    "value": "getBezierPath curvature=0.2",
    "用法": "平滑贝塞尔曲线（替换 React Flow 内置 smoothstep 直角折线）；连接预览线 strokeDasharray 5 3 + 端点 r3 白心圆"
  },
  "edge-arrow": {
    "value": "MarkerType.ArrowClosed width 14 height 14 color #d6d3d1",
    "用法": "默认边箭头 —— stone-300 克制小箭头"
  },
  "node-hover": {
    "value": "hover:-translate-y-px hover:shadow-card transition-all duration-150",
    "用法": "节点卡 hover 微浮起 1px + 阴影从 shadow-soft 升到 shadow-card；选中态 -translate-y-px + ring-2 ring-offset-2"
  },
  "node-running": {
    "value": "border-primary-400 animate-pulse",
    "用法": "运行中节点边框脉冲（叠加在 cardTint 之上）"
  },
  "handle-hover": {
    "value": "!h-2.5 !w-2.5 → hover:!h-3.5 hover:!w-3.5  transition-all duration-150",
    "用法": "连接点小圆点 hover 从 10px 放大到 14px（白底 + 1.5px 边 + shadow-sm）"
  },
  "palette-enter": {
    "value": "animate-in fade-in slide-in-from-left-2 duration-200",
    "用法": "节点面板（左上角）展开 —— 从左淡入滑入 200ms"
  },
  "copilot-enter": {
    "value": "animate-in fade-in slide-in-from-right-2 duration-200",
    "用法": "AI 编排助手 / inspector（右侧）打开 —— 从右淡入滑入 200ms"
  },
  "ghost-follow": {
    "value": "cursor-copy + fixed top-0 left-0 z-50 幽灵卡跟随光标",
    "用法": "点击 palette 节点后进入放置态：光标变 cursor-copy，一张虚线幽灵卡（border-2 border-dashed）跟随光标，点画布落位"
  },
  "panel-z-yield": {
    "value": "失焦面板 translate-x-[-14px] translate-y-[10px] 露角",
    "用法": "inspector 与 copilot 共存时，非置顶面板向左下错位露出一角（点击切换 z-20/z-10）"
  }
}
```

## 视觉特征

- **相邻高亮边 = 流动 6/4 虚线**：纯 edge 点选保持实线粗（active 2.25px），但相邻节点被选中 / hover 派生的高亮走 `strokeDasharray="6 4"` —— 虚线本身随 React Flow 重渲染产生「流动」错觉，凸显数据流向
- **fail 边 = 静态 5/3 虚线**：失败分支 `strokeDasharray="5 3"`、rose 色、不流动；与高亮边的 6/4 区分（更密的破折号 = 警示）
- **高亮色跟随焦点节点类型 hue**：KB 绿 / LLM 紫 / if_else 琥珀… 取焦点节点 TYPE_META.edgeColor（各类型 500 阶 hex），不是统一蓝
- **节点 hover 只浮起 1px**：`-translate-y-px` 极克制，配 shadow 升档（soft→card）；不放大、不变色，靠阴影传达「可拖」
- **handle hover 放大 40%**：10px→14px，是画布上唯一「明显放大」的交互反馈，因为连接点要给足热区提示
- **面板方向滑入有语义**：palette 在左 → 从左滑（slide-in-from-left-2）；copilot / inspector 在右 → 从右滑（slide-in-from-right-2）。方向 = 它在画布的位置，不是随机
- **全部 120–200ms**：边过渡 150ms、面板 200ms、handle 150ms、「+」按钮显隐 120ms —— 统一在「快到几乎瞬时但仍可感知」的区间

## 适配指南

- 边过渡写在 `BaseEdge` 的 `style.transition`，不写 className（React Flow 边是 SVG path，transition 直接挂 style）
- 高亮 / 淡化 / fail 三态互斥优先级：fail > active(selected‖highlighted) > dimmed > normal；`active` 时即便 dimmed 也不淡化
- palette / copilot 用 Tailwind `animate-in` 工具类（tailwindcss-animate）：`animate-in fade-in slide-in-from-{left|right}-2 duration-200`
- 节点 cardTint（类型色温底）是「静态层」，本运动集叠在其上：hover 浮起 / running pulse / selected ring 都不破坏 cardTint
- 幽灵跟随用 `document` 级 mousemove 监听（palette 常驻会挡画布 onMouseMove），ref 直接设 transform

## 反模式

- ❌ 相邻高亮边也用 5/3（fail 同款）—— 流动方向感会和「失败」语义撞，必须 6/4 区分
- ❌ 节点 hover 放大 scale —— 画布上节点放大会和邻居重叠遮挡，只许 -translate-y-px
- ❌ 面板从顶 / 底滑入 —— 滑入方向必须等于面板在画布的物理边（左 palette / 右 inspector），否则方向语义错乱
- ❌ 边过渡时长 > 200ms —— 选中节点时一片边同时过渡，慢了会有「拖泥带水」的廉价感
- ❌ 把这套画布运动用到普通后台列表 —— 流动虚线 / 方向滑入是画布专属语言，列表用 waveflow keyframes-suite
