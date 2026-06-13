# 沉淀计划 · Chameleon

日期：2026-06-13
作者：links
模式：create
起点：from-project（$PROJECT = /Users/links/Coding/Archer/Chameleon/frontend + frontend/embed）
档位：Tier 3 · 全量级（穷举每域）
技术栈指纹：react19 + shadcn-radix（Radix + CVA + Tailwind v4 CSS-first @theme）+ vite + lucide-react
设计「脸」：工程师暖白 SaaS 控制台 + 霓虹 AI 强调色

## 目标

把 Chameleon（LLM 编排平台）前端 1:1 沉淀进 style-vault。**智能去重**：Chameleon 与已有 `waveflow` 是同一套设计系统，共享地基 cross-namespace ref 复用 waveflow（23 条），只为 Chameleon 独有/分叉面新建 `chameleon/*`（74 条）。

## 涉及条目（74 新建 + 2 聚合 = 76）

- TOKENS 5：themeable-8x4-system(VAR) · neon-ai-suite(NEW) · keyframes-anim-modes(VAR) · node-type-hue-system(NEW) · canvas-edge-dash-flow(NEW)
- COMPONENTS 27：themeable 按钮/输入/开关/徽章/状态点(VAR) + radix-single-select / pickers / param-slider / codemirror-json-editor / graph-config-field-kit / stat-tile / recharts-time-series / neon-loader / radix-overlay-primitives / 等(NEW)
- BLOCKS 33：canvas 7(画布) + nav/layout 5(导航重构) + display 9(trace/eval/kb/app-card) + chat 6 + form/filters/feedback 6
- PAGES 9：workflow-graph-editor · model-compare-chat-lab · observability-overview-tabs · trace-detail-tree-gantt · kb-detail-tabbed-workbench · eval-dataset/run-detail · app-card-library · embed-fullscreen-chat
- 聚合（fan-out 后由主流程写）：styles/admin-console/chameleon-ai-orchestration · products/chameleon

详见 plan-entries.json（每条带 source_files + visual_spec + dedup + refs_uses）。

## product 复用 waveflow（23 条 cross-namespace ref，不新建）

tokens: palettes/warm-paper-ink-blue · typography/pairs · shadow/soft-card-pop-trio · border · iconography · layout/data-console-shell · motion/keyframes-suite
components: buttons/cva-engineer-button · inputs/blue-focus-input · inputs/datetime-range-presets · toggles/emerald-switch · indicators/status-dot-ring · tags-badges/code-status-badge · tags-badges/glue-type-badge-duo
blocks: nav/{tree-line-sidebar,topbar-search-ping,cmdk-search-modal} · display/data-table-leftbar-shimmer · filters/table-toolbar-tri · form/cron-builder-modal · feedback/{empty-dashed-state,top-progress-bar} · layout/master-detail-list-aside

## 依赖关系

tokens 无依赖 → components/blocks/pages uses tokens（chameleon 新建 + waveflow 复用）→ styles 聚合 → products/chameleon refs style + pages + 关键 blocks/components/tokens（chameleon 与 waveflow 混引）

## 元信息填写方式

AI 自动填（Y · 用户授权"全量开始写"）——name/description/tags 由写入智能体据源码与上下文填，stack 一律 [shadcn-radix]，theme 默认 light（themeable 条目标 both）。

## Tier 3 覆盖率

| 维度 | 实际 | 覆盖率 |
|---|---|---|
| 路由 | 39/39 全映射（独特页新建 / CRUD 页 ref waveflow） | 100% ✅ |
| 全局模式 | themeable / neon / 节点配色 / 暖白基底 / cmdk / 工程师细节类 等均沉淀为 token/component | ≥80% ✅ |
| 表单 | schema-dynamic-form / generation-panel / graph-run-dialog / cron(ref) / login(ref) | ✅ |
| 状态 | neon-loader / skeleton-kit / nav-progress / flair-empty-state / status-pill | ✅ |

## 执行状态

☑ 用户已确认全量 74 · 待 fan-out 写入（11 组 × Opus 4.8）
