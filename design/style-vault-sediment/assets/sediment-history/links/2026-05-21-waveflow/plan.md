# 沉淀计划 · waveflow

日期：2026-05-21
作者：links
模式：create
起点：from-project (/Users/links/Coding/A-complex/ikt/waveflow-ui)
档位：Tier 3 · 全量级（目标 30-50+ 条 · 实际 59 条 + 1 跨 namespace 复用）

## 目标

把 waveflow-ui（DataX 风格的数据同步与任务调度平台）的暖工程师风格 100% 沉淀到 vault，覆盖全部 17 条路由 + 全部组件库 + 全局 className 模式 + 表单 / 状态 / 动效系统。

## 涉及条目（59 条 · 依赖拓扑序）

### tokens (10)
1. tokens/palettes/waveflow/warm-paper-ink-blue
2. tokens/typography/pairs/waveflow/inter-jetbrains-instrument-trio
3. tokens/shadow/waveflow/soft-card-pop-trio
4. tokens/border/waveflow/translucent-stone-system
5. tokens/motion/waveflow/keyframes-suite
6. tokens/motion/waveflow/three-icosahedron-bg
7. tokens/texture/waveflow/login-dot-grid-mask
8. tokens/texture/waveflow/login-floating-geom-quartet
9. tokens/layout/waveflow/data-console-shell
10. tokens/iconography/waveflow/engineer-detail-classes

### components (14)
11. components/buttons/waveflow/cva-engineer-button
12. components/buttons/waveflow/dark-pill-arrow-cta
13. components/inputs/waveflow/blue-focus-input
14. components/inputs/waveflow/underline-bare-input
15. components/inputs/waveflow/datetime-range-presets
16. components/toggles/waveflow/emerald-switch
17. components/selects/waveflow/multi-select-popover
18. components/indicators/waveflow/status-dot-ring
19. components/indicators/waveflow/segmented-blocks
20. components/indicators/waveflow/pulse-ping-dot
21. components/tags-badges/waveflow/glue-type-badge-duo
22. components/tags-badges/waveflow/code-status-badge
23. components/typography-atoms/waveflow/kbd-key-cap
24. components/typography-atoms/waveflow/meta-caps-mono-pair

### blocks (22)
25. blocks/nav/waveflow/tree-line-sidebar
26. blocks/nav/waveflow/icon-collapsed-sidebar
27. blocks/nav/waveflow/topbar-search-ping
28. blocks/nav/waveflow/cmdk-search-modal
29. blocks/display/waveflow/canonical-table-shell
30. blocks/display/waveflow/data-table-leftbar-shimmer
31. blocks/display/waveflow/dashboard-kpi-six-row
32. blocks/display/waveflow/article-gauge-monitor
33. blocks/display/waveflow/metric-card-quartet
34. blocks/display/waveflow/set-card-segmented
35. blocks/layout/waveflow/master-detail-list-aside
36. blocks/filters/waveflow/table-toolbar-tri
37. blocks/form/waveflow/dialog-vertical-form
38. blocks/form/waveflow/login-editorial-form
39. blocks/form/waveflow/login-three-decor-right
40. blocks/form/waveflow/cron-builder-modal
41. blocks/form/waveflow/stepper-section-form
42. blocks/feedback/waveflow/top-progress-bar
43. blocks/feedback/waveflow/empty-dashed-state
44. blocks/feedback/waveflow/danger-confirm-modal
45. blocks/feedback/waveflow/log-pre-viewer
46. blocks/feedback/waveflow/action-dropdown-more

### pages (11)
47. pages/dashboard/waveflow/admin-runtime-report
48. pages/list-table/waveflow/canonical-section-list （适用 project/datasource/executor/user）
49. pages/list-table/waveflow/job-mgmt-with-switch （适用 jobInfo/jobTemplate）
50. pages/list-table/waveflow/job-log-batch-select
51. pages/detail/waveflow/jobset-master-detail
52. pages/form-flow/waveflow/json-build-stepper （适用 json-build/json-build-batch）
53. pages/dashboard/waveflow/registry-monitor-articles
54. pages/auth/waveflow/login-editorial-three
55. pages/empty-error/waveflow/minimal-text-401
56. pages/dashboard/waveflow/json-format-ace-dual
57. pages/detail/waveflow/log-viewer-pre

### styles + products (2)
58. styles/admin-console/waveflow-warm-engineer
59. products/waveflow

### 跨 namespace 复用 (0 新增)
- pages/empty-error/sage/crt-tv-404 (已存在 - 由 sage 沉淀过的 CRT TV 404，waveflow 同款源码直接 refs)

## 依赖关系（DAG）

```
products/waveflow
  → styles/admin-console/waveflow-warm-engineer
    → tokens × 10 (palette/typography/shadow/border/motion×2/texture×2/layout/iconography)
    → components × 14
    → blocks × 22
    → pages × 11 + 跨 ns refs sage/crt-tv-404
```

## 元信息填写方式

- AI 自动填（用户首批确认时授权）：全部 59 条

## Tier 3 覆盖率

| 维度 | 目标 | 实际 | 覆盖率 |
|---|---|---|---|
| 路由 | 17 | 17 | 100% ✅ |
| 全局模式 | 3 | 8 | 100% ✅ |
| 表单 | 8 | 8 | 100% ✅ |
| 状态 | 13 | 13 | 100% ✅ |
| 动效 | 14 | 14 | 100% ✅ |

## 起点 / 来源

源码路径：`/Users/links/Coding/A-complex/ikt/waveflow-ui`

技术栈指纹：
- React 18 + TypeScript + Vite 7
- Radix UI (shadcn-style components in `src/components/ui/`)
- Tailwind CSS 4 (CSS-first `@theme`)
- Three.js (login background)
- ECharts (dashboard)
- lucide-react (icons)
- Fonts: Inter + JetBrains Mono + Instrument Serif (all via @fontsource)
- styled-components (404 page)
- ace-builds + react-ace (JSON format tool)
- React Router v6 (lazy + nested + Layout 不 unmount)

## 执行状态

☑ 用户已确认 · 已写入 59 条 + sync 全绿 · 待 commit
