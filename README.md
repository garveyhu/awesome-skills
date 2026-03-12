# Awesome Skills

A collection of AI agent skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and other AI coding assistants. These skills cover the full lifecycle of building and shipping a web application — from idea to production.

---

## The Full Stack Workflow

Skills in this collection are designed to be used together. Here's the complete journey from idea to deployed product:

```
想法 → website-creator → 项目骨架
          ↓                    ↓
  react-best-practices   fastapi-best-practices
  （前端开发细节）         （后端开发细节）
          ↓
     wiki-creator
    （生成项目文档）
          ↓
  docsify-station-creator
   （文档建站，可浏览）
          ↓
  docker-best-practices
  （容器化 → 测试 → 推送 → 部署）
```

**典型使用流程：**

1. **`website-creator`** — 描述你的产品想法，skill 通过苏格拉底式提问确认需求，输出规划，确认后自动调用 `react-best-practices` 和 `fastapi-best-practices` 创建完整项目骨架
2. **`react-best-practices`** — 在已有前端项目中添加页面、组件、API 服务，或审查前端代码质量
3. **`fastapi-best-practices`** — 在已有后端项目中添加接口、数据模型，或审查后端代码规范
4. **`wiki-creator`** — 深度扫描项目代码，自动生成结构化的多文件 Markdown 文档
5. **`docsify-station-creator`** — 将 `docs/` 目录一键转为可浏览的 Docsify 文档站
6. **`docker-best-practices`** — 分析项目结构，生成完整 `docker/` 目录，引导本地测试、多架构镜像推送、生产环境部署

---

## Skills

### website-creator

从产品想法到完整项目骨架的全流程引导。

**Features:**
- 苏格拉底式提问（固定 3 问 + 最多 5 轮动态追问，达到 95% 需求确定度才出规划）
- 输出结构化项目规划，用户确认后执行，不提前创建任何文件
- 自动判断前端/全栈类型，调用对应 skill 的 Init 阶段
- 单 git 仓库管理前后端（`frontend/` + `backend/` 在同一 repo 根目录）
- 全栈项目始终内置 JWT 认证骨架

**Requires:** `react-best-practices`（前端），`fastapi-best-practices`（全栈）

---

### react-best-practices

基于 `yarn + Vite + TypeScript + React + Ant Design + Tailwind CSS` 的 React 项目全生命周期规范。

**Features:**
- **Init** — 脚手架创建 + 完整代码规范工具链（ESLint、Prettier、Stylelint、Commitlint、Husky、ls-lint、lint-staged）
- **Guide** — 添加页面、组件、API 服务的分层规范；全局 Loading 两层模式（Suspense 全屏 + 页面内 Spin）
- **Review** — 结构、命名、代码质量、配置一致性检查清单

包含 9 份配置模板和 7 份源码模板（含完整 `App.tsx` 模板）。支持简单项目（静态路由）和复杂项目（`import.meta.glob` 动态路由发现）两种规模。

---

### fastapi-best-practices

基于 `FastAPI + uv + SQLAlchemy + Alembic` 的 Python 后端项目全生命周期规范。

**Features:**
- **Init** — uv 项目初始化，依赖安装，ruff 代码格式化，Alembic 迁移配置，`run.sh` 本地启动脚本
- **Guide** — HTTP 方法约束（仅 GET/POST）、Result 响应格式、MVC 分层、JWT 认证三件套（auth_util / oauth / AuthWhitelist）、CustomException、分页模式（PageParams/PageResult）、CORS 配置、SQLAlchemy Model 时间戳与逻辑外键约定、Pydantic Schema 约定
- **Review** — 认证检查、数据库 Schema 检查、Schema 检查等完整清单
- **Optional patterns** — convert_util、time_util、request_context_util、crypto_util

支持简单项目（单包）和复杂项目（UV workspaces 多包，动态路由注册）。**禁止物理外键设计**，所有关联字段使用逻辑外键（`index=True + comment`）。

---

### docker-best-practices

从成品项目到容器化测试和生产部署的全流程规范，基于真实生产环境打磨的经验。

**Features:**
- **Init** — 自动扫描项目类型（全栈/纯后端/纯前端），收集必要信息，一次性生成完整 `docker/` 目录
- **Guide** — 本地测试（一行 mkdir + build + up）、镜像推送（buildx 多架构、登录提醒、tar 导出）、生产部署（目录创建 + 权限 + docker-compose.prod.yml）
- **Review** — 镜像质量、安全、可维护性、网络（SSE/WebSocket）检查清单

输出文件：`Dockerfile`（多阶段构建）、`entrypoint.sh`、`nginx.conf`（含 SSE + WebSocket 支持）、`docker-compose.yml`（测试 build-based）、`docker-compose.prod.yml`（生产 image-based）、`DEPLOY.md`（构建与部署说明文档）、`.dockerignore`。

内置嵌入式 MariaDB 双模式（`USE_EMBEDDED_DB=true/false` 切换外部 MySQL）。

---

### wiki-creator

深度扫描项目代码库，生成结构化的 DeepWiki 风格多文件 Markdown 文档。

**Features:**
- 4 阶段工作流：深度扫描 → 规划结构 → 生成文档 → 审查
- 从入口文件出发，追踪 import 链，阅读真实源码
- 根据项目特征灵活生成 4–10 个文档文件（非固定模板）
- Mermaid 图表（含渲染安全样式指南和颜色方案）
- 中文输出，兼容 Docsify 展示

**Pairs with** `docsify-station-creator` — wiki-creator 生成内容，docsify-station-creator 负责建站展示。

---

### docsify-station-creator

将已有 `docs/` 目录一键转为功能完整的 Docsify 文档站。

**Features:**
- 深色/浅色主题切换
- 右侧目录（含滚动高亮和折叠）
- 全文搜索
- Mermaid 图表渲染 + Panzoom 点击放大
- 代码高亮（16 种语言）+ 复制按钮
- 响应式布局
- 跨平台启动脚本（Windows `.bat` + Unix `.sh`）

---

## Installation

### Claude Code

```bash
# 从 GitHub 安装（所有 skills）
git clone https://github.com/garveyhu/awesome-skills.git ~/.claude/skills/awesome-skills

# 或只安装需要的 skill
cp -r awesome-skills/react-best-practices ~/.claude/skills/
```

### Manual

将所需 skill 文件夹复制到你的 AI 助手 skill 目录。每个 skill 自包含，只需复制文件夹即可。

---

## Usage

Skills 在相关场景下自动触发。示例：

```
# 触发 website-creator（从想法开始）
"帮我做一个订阅管理平台"
"创建一个前后端项目"

# 触发 react-best-practices
"给这个 React 项目创建一个用户管理页面"
"审查一下前端代码结构"

# 触发 fastapi-best-practices
"添加一个商品分页查询接口"
"检查后端代码是否符合规范"

# 触发 docker-best-practices
"帮我把这个项目 docker 化"
"写 Dockerfile 然后推送到私有仓库"

# 触发 wiki-creator
"为这个项目生成技术文档"

# 触发 docsify-station-creator
"把 docs/ 目录做成一个可以浏览的文档站"
```

---

## License

MIT
