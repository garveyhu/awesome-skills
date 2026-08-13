# 素材溯源 · waveflow

## 项目路径

- $PROJECT = `~/Coding/A-complex/ikt/waveflow-ui`
- 技术栈指纹：`shadcn-radix` (React 18 + Vite 7 + Radix UI + Tailwind v4 + CVA) + Three.js + ECharts + lucide-react + Inter/JetBrains Mono/Instrument Serif via @fontsource

## 关键源文件

### 全局风格 DNA
- `src/styles/global.css` (296 行) — 整套设计 tokens：暖白三档 + Inter/JetBrains Mono/Instrument Serif + soft/card/pop shadows + .tnum/.kbd/.status-dot/.tree-line/.skeleton utilities + 9 个 keyframes (accordion×2/decor-drift×3/ping-soft/global-progress/boot-dot/shimmer)
- `src/assets/custom-theme/index.css` — 兼容旧 ant-design vars (主要不沉淀，旧资源)

### 路由
- `src/router/index.tsx` (130 行) — 17 路由全枚举：dashboard/project/datasource/job(4 子)/jobSet/log/executor/user/registry/tool/login/401/404/data-log/404 通配

### 布局 (3 文件)
- `src/layout/index.tsx` — 主 Layout (sidebar + topbar + main + Toaster + SearchPanel + GlobalProgress)
- `src/layout/Sidebar.tsx` (443 行) — tree-line 侧栏 + 折叠态 + 任务集动态子项 + 底部用户 dropdown
- `src/layout/Topbar.tsx` — 48px topbar + ⌘K 搜索 + ping 在线状态

### 登录 (3 文件)
- `src/pages/login/index.tsx` (249 行) — editorial split 整页
- `src/pages/login/components/ThreeBackground.tsx` (143 行) — Three.js 三层 icosahedron + 200 stars + 鼠标 lerp
- `src/pages/login/components/LeftDecor.tsx` (250 行) — 4 SVG 浮件 + RAF 动态连线 + 鼠标 multiply 柔光 + radial dot grid mask

### Dashboard (8 文件)
- `src/pages/dashboard/admin/index.tsx` — 主页面
- `src/pages/dashboard/admin/components/KPIRow.tsx` (358 行) — 6 KPI 大数字（DispatchCard sparkline / SuccessRateCard gradient / AvgTimeCard min-max / ExecutorOnlineCard health dots / ActiveJobsCard chips / FailedCountCard）
- 其他: LineChart / StatusPieChart / DurationBarChart / ExecutorHealthTable / RecentFailures / TopList

### 列表页 (8 模块)
- `src/pages/datax/jobProject/` — canonical list-table 范式
- `src/pages/datax/jobInfo/index.tsx` (560 行) — 带 leftBar + Switch + MultiSelect 项目 + 3 filter + MoreHorizontal dropdown
- `src/pages/datax/jobSet/index.tsx` (997 行) — master/detail 主从布局 + HERO + 4 MetricCard + MembersTable + 7 Dialog
- `src/pages/datax/jobLog/index.tsx` (683 行) — 4 input/select filter + datetime-range + checkbox batch + 清理 dialog + CodeBadge + 富文本 sanitize
- `src/pages/datax/json-build/index.tsx` (896 行) — 4-step Stepper Reader→Writer→Mapper→Build + Drawer 模板
- `src/pages/datax/jobTemplate/index.tsx` — list + NextTriggerPopover + RegisterNodePopover
- `src/pages/datax/registry/index.tsx` (119 行) — article 堆叠 + 3-gauge
- `src/pages/datax/jobLog/log/index.tsx` (85 行) — `/data/log` 独立 pre viewer 页

### 工具 / 错误页
- `src/pages/tool/jsonFormat/index.tsx` (158 行) — 双 ACE editor
- `src/pages/complex/404.tsx` (646 行) — styled-components 复古 CRT TV（与 sage 同款，跨 namespace 复用）
- `src/pages/complex/401.tsx` (19 行) — minimal 401

### 组件库 (40+ 文件)
- `src/components/ui/` (23 个 Radix wrapper)：button (CVA 7 variant × 5 size) / input / textarea / checkbox / switch / select / multi-select / dialog / drawer / popover / dropdown-menu / tooltip / radio-group / tabs / table / accordion / card / label / datetime-range-picker / stepper / toaster / confirm-dialog
- `src/components/common/` (8 个业务原子)：StatusDot (含 deriveJobStatus/deriveRunStatus) / SegmentedBlocks (+ ThreeSegmentBar) / MetricCard (4 tone) / Badges (GlueTypeBadge × 2 variants + GlueTypeCountChip + ProjectTag + CountTag) / EmptyState / Kbd / GlobalProgress / TruncatedText
- `src/components/table/` (3 文件)：DataTable (含 leftBar + delayed shimmer) + TableToolbar (title + search + filters + extra) + TablePagination
- `src/components/search/SearchPanel.tsx` (481 行) — ⌘K cmdk 命令面板
- `src/components/CronBuilder.tsx` (256 行) — 5 mode 可视化 cron 构建器
- `src/components/CodeEditor.tsx` / `DynamicParamsEditor.tsx` — 辅助编辑器

## 识别的设计 DNA

1. **暖白三档**（warm/warm-2/paper）+ 墨黑 ink + 蓝单 CTA
2. **三字体语义切分**：Inter / JetBrains Mono / Instrument Serif
3. **工程师四件套**：`.tnum` / `.status-dot` / `.tree-line` / `.kbd`
4. **极淡阴影**（4-8% alpha）3 档：soft / card / pop
5. **数据可视化语言**：emerald running / red error / amber warning / blue progress / stone stopped
6. **GlueType 11 业务类型 × 双变体 chip**（light + solid）
7. **Editorial 性格出口**：登录 Three.js + serif italic — 故意与 admin 主体形成视觉断层

## 跨 namespace 复用

- `pages/empty-error/sage/crt-tv-404` — sage 已沉淀过的复古 CRT TV 404 与 waveflow 是同一段 styled-components 代码（CSS 艺术品，从 CSS art 集合借用）。waveflow product refs 直接引用，不重复沉淀

## 备注

- 17 条路由的 11 条独立 page 沉淀（4 个 canonical 列表合一条 / 2 个 job-mgmt 合一条 / 2 个 json-build 合一条 / 404 复用 sage）
- 跨文件 className 模式扫描发现 8 条全局模式，全落 token 或 component
- 表单 / 状态 / 动效系统全扫，13 个状态 + 14 个动效全部归位
