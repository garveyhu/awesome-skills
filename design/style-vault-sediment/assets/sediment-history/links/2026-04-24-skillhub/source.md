# 素材溯源 · SkillHub

## 项目路径

- `$PROJECT = ~/Coding/A-complex/ikt/skills/skillhub`
- 技术栈指纹：**react 19 + antd 6 + tailwind 4 + vite 8 + framer-motion 12**
- 构建链：yarn · ESLint · Prettier · Stylelint · ls-lint · Husky · Commitlint · Vitest

## 关键源文件

### 全局样式 / 主题
- `frontend/src/App.tsx:23-37` · Antd ConfigProvider `colorPrimary='#0f172a' borderRadius=8 fontFamily='Inter + Space Grotesk'`
- `frontend/src/core/assets/styles/index.less`
  - `:5-6` · `--font-sans` / `--font-mono` 定义
  - `:8-18` · teal primary-50 ~ primary-900
  - `:30-34` · body bg `#f5f7fa` + font-feature-settings `cv02/03/04/11`
  - `:37-58` · `shimmer` / `flow-right` / `fadeIn` keyframes
  - `:63-70` · `.glass` / `.glass-dark` utility
  - `:88-126` · Antd card / tabs / table / button 覆盖
  - `:129-272` · prose 排版细节（markdown 渲染）

### 布局
- `frontend/src/core/components/layout/MainLayout.tsx`
  - `:76-164` · 玻璃 pill navbar（外层 `bg-white/80 backdrop-blur-lg` + 内层 `rounded-2xl shadow-[0_1px_4px_rgba(0,0,0,0.04)] border border-gray-100`）
  - `:64-69` · `navLinkClass` active/default 状态
  - `:173-231` · 移动端底部 tab bar（此次未单独沉淀成 block，归入 navbar 系列后续再补）
  - `:233-261` · footer（含 emerald pulse 点）

### 发现 / 首页
- `frontend/src/system/discovery/pages/home/index.tsx`
  - `:26-30` · AVATAR_COLORS 12 色
  - `:34-85` · BorderTraceButton（追光按钮实现）
  - `:98` · RANK_COLORS 3 色
  - `:117-128` · LetterAvatar 组件
  - `:207-242` · Hero + gradient emphasis word
  - `:251-331` · TOP Skills 榜单（LeaderboardRow 源型）
  - `:333-411` · 分类图标导航 + 搜索（CategoryIconButton + 搜索 form）
  - `:412-538` · Skill 网格 + 分页（SkillCard + Pagination 源型）
  - `:307-313` · Teal pill 的源型

### 管理后台
- `frontend/src/system/admin/pages/index.tsx`
  - 整页结构 · Tabs 多域 + StatCard 总览
  - 引用 `AdminTable` / `AdminTableToolbar`（来自 blocks/display/table · blocks/layout/toolbar-bar，已存在）

### 其它参考（未直接沉淀但贡献视觉理解）
- `frontend/src/system/auth/pages/login/index.tsx` · slate-800→950 gradient logo 方块 · bg-slate-50 全屏布局
- `frontend/src/system/practice/pages/index.tsx` · "发布实践" 按钮的 group-hover 流光 overlay · `Input.Search` 覆盖 colorPrimary
- `frontend/src/system/skill/pages/detail/index.tsx` · Prism `oneLight` 语法高亮配色 · prose 标题下划线

## 项目定位

来自 `README.md`：

> SkillHub 是一个用于发现、管理和分享 AI Agent 技能的全栈社区平台。
> 它聚合一个或多个 Git 仓库，扫描含有 `SKILL.md` 的文件夹，将其转化为可浏览的技能页面，
> 并提供社区互动与管理后台。

核心功能：
- 技能发现（首页 / 详情 / 相关推荐）
- 仓库同步（Git 远程 / 本地 / 定时 + 手动 + 快照审计）
- 社区互动（点赞 / 评分 / 评论 / 实践广场 / 关注 / 私信）
- 技能投稿（zip / tar.gz 上传 + 管理员审核）
- 管理后台（概览 / 内容审核 / 角色管理）

## 识别的技术栈

`react-antd-tailwind` —— 完全匹配 style-vault taxonomy 已有 slug，直接使用。

## 工具链细节（不影响沉淀，仅记录）

- 路由：React Router 7（动态模块路由 · 按 `system/*` 自动聚合）
- HTTP：Axios + humps（camelCase ↔ snake_case 自动转换）
- Markdown：`react-markdown` + `rehype-raw` + `remark-gfm` + Prism `oneLight`
- Lint：ESLint 9 + Prettier 3 + Stylelint 17 + ls-lint
- 测试：Vitest 4 + Testing Library + JSDOM
- 后端：FastAPI + SQLAlchemy 2.0 + Alembic + Loguru + uv（非沉淀范围）
