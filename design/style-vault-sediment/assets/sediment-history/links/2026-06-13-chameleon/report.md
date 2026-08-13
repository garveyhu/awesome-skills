# 沉淀报告 · Chameleon

日期：2026-06-13
模式：create
起点：from-project（~/Coding/Archer/Chameleon/frontend + frontend/embed）
档位：Tier 3 · 全量级（目标 30–50+ · 实际 **76 条新建** + 复用 23 waveflow）
作者：links
策略：**智能去重**（Chameleon 与 waveflow 同源，共享地基 ref 复用，只建独有/分叉面）

## 涉及条目（76 新建）

| 层 | 数量 | signature |
|---|---|---|
| token | 5 | themeable-8x4-system · neon-ai-suite · node-type-hue-system · canvas-edge-dash-flow（+ keyframes-anim-modes） |
| component | 27 | neon-loader · themeable-cva-button · codemirror-json-editor · graph-config-field-kit · sliding-thumb-segmented · recharts-time-series 等 |
| block | 33 | 画布 7(node-palette/graph-node-card/bezier-edge-add/config-panel-inspector/subflow/copilot/controls) · 导航重构 3 · trace-tree-gantt · eval-spreadsheet · run-compare-heatmap · kb 三栏×2 · 对话气泡/HITL/embed · schema-form · generation-panel |
| page | 9 | workflow-graph-editor · model-compare-chat-lab · observability-overview · trace-detail · kb-detail · eval-dataset/run-detail · app-card-library · embed-fullscreen |
| style | 1 | styles/admin-console/chameleon-ai-orchestration |
| product | 1 | products/chameleon（category: ai） |

39 条标 signature。

## 复用 waveflow（23 条 cross-namespace ref，未新建）

暖白 palette / 三字体 / 阴影 / 边框 / 工程师细节类 / data-console-shell / CVA 按钮 / blue-focus 输入 / emerald 开关 / status-dot / 两个 badge / 树状侧栏 / topbar / cmdk / canonical 表格 / 工具栏 / cron / 空态 / 顶部进度条 / master-detail。

## 元信息来源

AI 自动填（Y · 用户授权全量开始写）。stack 一律 shadcn-radix，theme 默认 light（themeable/embed 标 both）。
**写入后归一修正**：tags.aesthetic/mood 被写入智能体误填为视觉描述词组（328 处越界）→ 用 discovery 阶段合法 tag 过滤 + 兜底（minimal/industrial · calm/serious）批量归一到 taxonomy。

## Tier 3 覆盖率

| 维度 | 实际 | 覆盖率 |
|---|---|---|
| 路由 | 39/39 全映射（独特页新建 / CRUD 页 ref waveflow） | 100% ✅ |
| 全局模式（themeable/neon/节点配色/暖白/cmdk/工程师细节类） | 沉淀为 token/component | ≥80% ✅ |
| 表单（schema-form/generation-panel/graph-run-dialog/cron·login ref） | 覆盖 | ✅ |
| 状态（neon-loader/skeleton-kit/nav-progress/flair-empty/status-pill） | 覆盖 | ✅ |

## 验收（用户要求"一定要验收·通过"）

- **yarn sync**：✓ 296 items，0 dangling、0 unresolved（修了 1 YAML + 328 tag 归一 + 1 缺 stack + 25 文件 uses 断链重映射）。
- **tsc**：chameleon preview 全绿（修 7 处未用变量/重复 key）。
- **浏览器 1:1 视觉抽检**（对照真实站 localhost:6006）：node-palette / graph-node-card / neon-loader / product 板——结构+配色+图标逐一吻合 ✅。
- **源码保真度审计**（11 Opus 4.8 智能体重读 .md+.tsx vs 源码）：**70/74 HIGH · 4 MEDIUM · 0 LOW**。4 MEDIUM 已全部修复：
  - message-actions-bar：active 底 amber-200/rose-200 → amber-100 #fef3c7 / rose-100 #ffe4e6
  - graph-run-dialog：删除源码不存在的 NodeRow 展开 chevron
  - domain-tab-topbar-account：渐变 logo→中性占位、退出项常驻红底→透明（仅 hover 红）
  - eval-run-detail：右栏宽 280→420px、明细列 200/220→260/280（对齐源码与自身 .md）

## Commit

- 网站仓：`457dcf7` · `feat(preview): add chameleon AI 编排平台 preview (76)`
- skill 仓：见本 batch 的 feat(style-vault) commit（含 references + 本报告）
- **均未 push**（保留给用户）

## 下一步

1. `cd ~/Coding/Archer/style-vault/frontend && yarn dev`（已在 6001 跑），肉眼过更多 preview
2. OK 后 `git push` 两仓
3. 发现问题 `git reset --soft HEAD~1` 回工作区

## 自迭代

发现 1 个 pattern 错误（写入智能体把 tags 填成自由描述词组），已回写硬规矩到 sediment skill + 登记 lessons-loopback（见独立 docs(skill) commit）。

---
*由 style-vault-sediment skill 生成 · 起点 from-project · 智能去重 · 76 新建 + 23 复用*
