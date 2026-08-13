# 素材溯源 · sage

## 项目路径
- $PROJECT = ~/Coding/A-complex/ikt/sage/frontend/
- 技术栈指纹：react-antd-tailwind + vite + tailwindcss v4 + styled-components + lucide-react

## 关键源文件

### Tokens 来源
- `tailwind.config.js`（无 extend，跑标准 Tailwind v4）
- `src/core/utils/themeUtils.ts`（12 主题色 4 张映射表 THEME_COLORS / THEME_CLASSES / THEME_HEX_COLORS / THEME_LIGHT_HEX_COLORS / THEME_SELECTION_COLORS）
- `src/core/assets/styles/index.less`（全局滚动条 + Inter font 注入）
- `src/core/assets/fonts/inter.css`（本地 Inter 字体）

### Style / Theme 注入
- `src/App.tsx`（AntdApp + I18nProvider + SpaceProvider + DifyProvider 的 Provider stack，从 localStorage 读 themeColor）
- `src/main.tsx`（VITE_BASE_PATH 路由前缀 + APP_NAME 注入）

### 路由
- `src/router/index.ts`（Vite import.meta.glob 自动收集 module routes）
- `src/router/init.tsx`（RouteWrapper + 认证守卫）
- `src/system/{chat,auth,admin,space,collection,model,analytics}/routes.ts`
- `src/agents/data-qa/routes.ts`

### Layout
- `src/core/components/layout/MainLayout.tsx`（871 行 — 侧栏 + admin overlay + 删除确认）
- `src/core/components/layout/SpaceSwitcher.tsx`（106 行 — 空间下拉 + 主题色注入）
- `src/core/components/layout/RevolverMenu.tsx`（1106 行 — 雪人飘雪 FAB）

### Pages
- `src/system/chat/pages/ChatPage.tsx`（960 行 — 主聊天页）
- `src/system/auth/pages/index.tsx`（202 行 — 登录页）
- `src/system/admin/pages/{UserManagement,RoleManagement}.tsx`
- `src/system/admin/pages/agent-store/AgentStorePage.tsx`（842 行 — Agent 商店）
- `src/system/space/pages/{SpaceManagement,ModelConfig,CoreConfigPage,SpaceDetail}.tsx`（SpaceManagement 1135 行）
- `src/system/collection/pages/{Collections,CollectionDetail}.tsx`
- `src/system/analytics/pages/{feedback,usage}/`
- `src/agents/data-qa/pages/datasource/{DataSourceList,DataSourceNew,DataSourceDetail}.tsx`
- `src/agents/data-qa/pages/rule/RuleSetManagement.tsx`（951 行 — 规则集 stepper modal）
- `src/agents/data-qa/pages/knowledge/{BusinessRule,PrefabSql}.tsx`
- `src/core/pages/NotFound.tsx`（647 行 — CRT TV 404）

### Common Components
- `src/core/components/common/Loading.tsx`（47 行 — Spin + 主题注入）
- `src/core/components/common/CrystalProgress.tsx`（128 行 — 玻璃进度条）
- `src/core/components/common/CommandPalette.tsx`（393 行 — Cmd+P 命令面板）
- `src/core/components/common/ManagementLayout.tsx`（111 行 — 管理 header）
- `src/system/chat/components/{ChatInput,ChatMessage,...}.tsx`

## 全局模式扫描结果
- `${themeClasses.*}` 出现 119 次（grep 命中）
- `bg-[rgb(231,231,231|237,237,237|239,239,239|242,242,242|244,244,244|246,246,246|249,249,249|251,251,251|252,252,252)]` 9 阶手调灰
- `rounded-(xl|2xl|3xl)` 48 次
- `animate-in` 10 次
- `backdrop-blur` 10 次
- `uppercase tracking-wider` 9 次
- `bg-slate-*` 92 次（slate 体系基底）

## 7 段 styled-components keyframes
- `RevolverMenu.tsx:55,61,66,73`：bling / earthSpin / snowFall / wobble
- `CrystalProgress.tsx:5,11,17`：shimmer / pulse / stripes

## 识别的技术栈
react-antd-tailwind + vite + tailwindcss v4 + styled-components + lucide-react

## 字典变更
- `assets/taxonomy.json` 新增 `category: ai`（dot=#0ea5e9，order=1），其它 category order 顺位 +1
- 后续 follow-up：如需 product 支持双 category（"category × ai"），需要单独升级 schema
