---
id: products/chameleon
type: product
name: Chameleon · LLM 应用编排平台
description: 工程师暖白控制台跑 LLM 编排全流程——可视化工作流画布(xyflow) + 多模型对比 playground + LangSmith 式 Trace 树/Gantt + 知识库分段工作台 + 评测电子表格 + 嵌入式对话挂件，长耗时 AI 任务以霓虹环点睛
platforms: [web]
theme: light
category: ai
refs:
  style: styles/admin-console/chameleon-ai-orchestration
  pages:
    - pages/editor/chameleon/workflow-graph-editor
    - pages/playground/chameleon/model-compare-chat-lab
    - pages/dashboard/chameleon/observability-overview-tabs
    - pages/detail/chameleon/trace-detail-tree-gantt
    - pages/detail/chameleon/kb-detail-tabbed-workbench
    - pages/detail/chameleon/eval-dataset-detail-spreadsheet
    - pages/detail/chameleon/eval-run-detail-master-detail
    - pages/list-table/chameleon/app-card-library
    - pages/chat/chameleon/embed-fullscreen-chat
  blocks:
    - blocks/canvas/chameleon/node-palette
    - blocks/canvas/chameleon/graph-node-card
    - blocks/canvas/chameleon/bezier-edge-add
    - blocks/canvas/chameleon/config-panel-inspector
    - blocks/canvas/chameleon/subflow-group-editor
    - blocks/canvas/chameleon/ai-copilot-panel
    - blocks/layout/chameleon/domain-tab-app-shell
    - blocks/nav/chameleon/domain-tab-topbar-account
    - blocks/nav/chameleon/borderless-bookmark-rail
    - blocks/display/chameleon/responsive-overlay-data-table
    - blocks/display/chameleon/trace-observation-tree-gantt
    - blocks/display/chameleon/eval-spreadsheet-airtable
    - blocks/display/chameleon/run-compare-heatmap-matrix
    - blocks/display/chameleon/kb-chunking-3pane-preview
    - blocks/display/chameleon/app-card-gallery-grid
    - blocks/chat/chameleon/message-list-bubble-thread
    - blocks/chat/chameleon/hitl-human-input-prompt
    - blocks/chat/chameleon/embed-widget-bubble-shell
    - blocks/form/chameleon/json-schema-dynamic-form
    - blocks/form/chameleon/generation-panel
    - blocks/display/waveflow/canonical-table-shell
    - blocks/form/waveflow/cron-builder-modal
    - blocks/feedback/waveflow/empty-dashed-state
  components:
    - components/feedback/chameleon/neon-loader
    - components/buttons/chameleon/themeable-cva-button
    - components/inputs/chameleon/codemirror-json-editor
    - components/inputs/chameleon/graph-config-field-kit
    - components/toggles/chameleon/sliding-thumb-segmented
    - components/display/chameleon/recharts-time-series
    - components/display/chameleon/stat-tile-delta
    - components/selects/chameleon/model-picker-popover
    - components/selects/chameleon/agent-picker-popover
    - components/avatars-icons/chameleon/provider-bot-avatar
    - components/buttons/waveflow/cva-engineer-button
    - components/inputs/waveflow/blue-focus-input
    - components/indicators/waveflow/status-dot-ring
    - components/typography-atoms/waveflow/kbd-key-cap
  tokens:
    palette: tokens/palettes/chameleon/themeable-8x4-system
    typography: tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio
    motion: tokens/motion/chameleon/neon-ai-suite
    border: tokens/border/waveflow/translucent-stone-system
    iconography: tokens/iconography/waveflow/engineer-detail-classes
tags:
  aesthetic: [minimal, industrial]
  mood: [calm, serious, confident]
  stack: [shadcn-radix]
preview: /preview/products/chameleon
---

# Chameleon · LLM 应用编排平台

> 把「工程师暖白数据控制台」从数据调度（waveflow）迁移到 **LLM 应用编排**：可视化工作流画布、多模型对比 playground、可观测 Trace 树、知识库工作台、评测电子表格、嵌入式对话挂件，统一在 [[styles/admin-console/chameleon-ai-orchestration]] 设计语言下。

## 设计语言

绑定 style [[styles/admin-console/chameleon-ai-orchestration]]——暖白纸墨 + blue-600 单一 CTA + Inter/JetBrains Mono/Instrument Serif，长耗时 AI 任务霓虹环点睛，工作流画布按节点类型微染色温，主题运行时可切换（8×4×3）。

## 与 waveflow 的关系

Chameleon 与 [[products/waveflow]] 是同一套设计系统的两个产品。**通用地基**（暖白 palette / 三字体 / 阴影 / 边框 / 工程师细节类 / CVA 按钮 / blue-focus 输入 / status-dot / canonical 表格 / cron / empty-state 等）直接 cross-namespace 复用 waveflow；Chameleon 只新建 **AI 编排专属面**（工作流画布 7 件 + playground 对话 + Trace 树 + KB/eval + NeonLoader + 可切换主题 + 导航重构 + embed widget）。

## 信息架构（4 域导航）

顶部域 Tab（工作台 / 知识库 / 观测 / 设置）+ 左侧无边书签竖条（`borderless-bookmark-rail`）+ ⌘K 命令面板。详见 `blocks/layout/chameleon/domain-tab-app-shell`。

## 核心页面

- **工作流编辑器**（`pages/editor/...workflow-graph-editor`）：全屏三栏 xyflow 画布——左节点面板、中画布、右配置 inspector。
- **Playground**（`model-compare-chat-lab`）：多列模型对比对话台。
- **可观测总览 / Trace 详情**：KPI tabs + LangSmith 式 span 树 + Gantt。
- **知识库工作台 / 评测电子表格**：三栏分段预览/命中测试 + Airtable 式打分表 + 运行对比热力矩阵。
- **嵌入式对话**：浮动气泡挂件 + 全屏 iframe 对话。
