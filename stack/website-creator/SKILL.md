---
name: website-creator
description: >
  Use when a user wants to create a new website or web application from scratch.
  Triggers include: "create a website", "build an app", "new project", "帮我做一个网站",
  "创建项目", "新建应用", or any request describing a product/app to be built.
  Uses Socratic questioning to reach 95% requirement certainty before planning.
  Then creates the project: frontend-only uses react-best-practices; full-stack
  adds fastapi-best-practices for the backend. Single git repo at project root.
---

# Website Creator

## 概述

通过苏格拉底式提问理解用户真实需求，在 95% 确定后输出规划，用户确认后直接创建完整项目骨架。

**依赖**：执行前必须确认以下 skill 已安装在当前 AI 助手的 skill 目录中：
- `react-best-practices`（前端）
- `fastapi-best-practices`（全栈后端，仅全栈项目需要）

若任一不存在，立即报错停止。

---

## Phase 1：固定提问（总是问，不计入 Phase 2 轮数）

按顺序提问，每次只问一个：

**Q1**: 项目名称是什么？（将作为根目录名和 package 名）

**Q2**: 这是前端网站还是前后端全栈项目？
- 前端网站：纯 React，无后端 API
- 全栈项目：React 前端 + FastAPI 后端

**Q3**: 项目创建在哪个目录下？（直接回车跳过 = 当前工作目录）

---

## Phase 2：动态追问（最多 5 轮，不含 Phase 1）

目标：收集足够信息达到 95% 确认门槛。每轮只问一个问题。

**95% 确认门槛**（全部满足才出规划）：
- ✅ 项目名确定
- ✅ 类型（前端/全栈）确定
- ✅ 至少 3 个核心页面或功能明确
- ✅ 目标用户/用途清晰

**常用追问方向**：
- "核心功能/页面有哪些？"
- "目标用户是谁？主要解决什么问题？"
- "有特殊的技术或业务要求吗？"

**超过 5 轮仍不满足门槛**：基于已有信息生成规划，用 `[待确认]` 标注假设项。

---

## Phase 3：输出规划（等用户明确确认）

按以下格式输出规划，等待用户确认：

```
📋 项目规划

项目名: {name}
类型: 前端 / 全栈
创建位置: {target_dir}/{name}/

技术栈:
  前端: React 19 + Vite + TypeScript + Antd + Tailwind CSS
  后端: FastAPI + SQLAlchemy + Alembic + SQLite   ← 仅全栈

核心页面/功能:
  - {功能 1}
  - {功能 2}
  - {功能 3}
  ...（[待确认] 标注假设项）

内置功能:
  - JWT 登录/注册（全栈项目默认包含，不可省略）

目录结构:
  {name}/          ← git 根目录
  ├── .gitignore
  ├── README.md
  ├── frontend/    ← React 项目
  └── backend/     ← FastAPI 项目（仅全栈）

确认后开始创建，是否继续？
```

**用户响应处理**：
- 回复"yes / 确认 / 继续"等明确肯定 → 进入 Phase 4
- 提出修改意见 → 根据修改更新规划，重新输出确认
- 全栈项目的 JWT 认证骨架不可在此阶段取消

---

## Phase 4：确认后执行

按顺序执行，每步完成后继续下一步：

### 步骤 1：创建根目录并初始化 git

```bash
mkdir -p {target_dir}/{name}
cd {target_dir}/{name}
git init
```

### 步骤 2：创建根 .gitignore

合并前后端忽略规则：

```gitignore
# 前端
node_modules/
dist/
.env.local

# 后端（仅全栈项目追加）
.venv/
__pycache__/
*.pyc
config/*.json
!config/*.json.example
data.db
logs/

# 通用
.DS_Store
*.log
```

纯前端项目只包含"前端"和"通用"部分。

### 步骤 3：创建前端（invoke react-best-practices）

**REQUIRED SUB-SKILL:** Use `react-best-practices`，执行其 **阶段一：初始化新项目（Init）** 的全部步骤，在 `{name}/frontend/` 目录下创建 React 项目。

> **重要**：跳过 react-best-practices Init 中的 `git init` 步骤（按步骤语义跳过，因为 git 仓库已在根目录初始化）。

### 步骤 4：创建后端（仅全栈项目，invoke fastapi-best-practices）

**REQUIRED SUB-SKILL:** Use `fastapi-best-practices`，执行其 **阶段一：初始化新项目（Init）** 的全部步骤，在 `{name}/backend/` 目录下创建 FastAPI 项目。

> **重要**：跳过 fastapi-best-practices Init 中的 `git init` 步骤（按步骤语义跳过）。

### 步骤 5：创建根 README.md

```markdown
# {项目名}

{项目简介，1-2 句，来自规划中的功能描述}

## 技术栈

- 前端: React 19 + Vite + TypeScript + Antd + Tailwind CSS
- 后端: FastAPI + SQLAlchemy + Alembic（仅全栈）

## 目录结构

\`\`\`
{name}/
├── frontend/    React 前端
└── backend/     FastAPI 后端（仅全栈）
\`\`\`

## 本地启动

**前端**
\`\`\`bash
cd frontend
yarn dev
\`\`\`

**后端**（仅全栈）
\`\`\`bash
cd backend
./run.sh
\`\`\`
```

### 步骤 6：初始提交

```bash
cd {target_dir}/{name}
git add .
git commit -m "init: scaffold {name} project"
```

---

## 约束

- **禁止在 Phase 3 规划被用户明确确认前创建任何文件或目录**
- `git init` 只在根目录执行一次，react/fastapi Init 步骤中的 git init 跳过
- 全栈项目始终包含 JWT 认证骨架（内置于 fastapi-best-practices）
- 动态追问最多 5 轮（不含 Phase 1），超出则带 [待确认] 假设出规划
- 两个依赖 skill 不存在时报错停止，不降级执行
