# Skill Improvements Design
**Date**: 2026-03-11
**Status**: Approved

---

## 概述

两个独立任务，顺序执行：

1. **Task A**：改进 `fastapi-best-practices` skill（基于 Sage 项目审查）
2. **Task B**：创建 `website-creator` skill（薄编排层，调用 react/fastapi best-practices）

---

## Task A：fastapi-best-practices 改进

### 文件改动清单

| 文件 | 操作 |
|------|------|
| `fastapi-best-practices/SKILL.md` | 新增 6 个 Guide 章节 + Review 清单 6 项 |
| `fastapi-best-practices/references/simple-project.md` | 新增 5 个文件模板，更新 2 个现有模板 |
| `fastapi-best-practices/references/complex-project.md` | 同步更新：加认证模式、无物理外键约定 |
| `fastapi-best-practices/references/patterns.md` | 新建：可选工具模式参考 |

### SKILL.md 新增 6 个 Guide 章节

**① JWT 认证模式**
- `auth_util.py`：`verify_token(token)`、`verify_and_get_user(token)` → User
- `AuthWhitelist`：类常量管理白名单，`is_whitelisted(path)` 判断
- `get_current_user`：FastAPI `Depends()` 依赖，API 层获取当前用户
- 中间件：白名单放行 + JWT 验证 + RequestContext 设置

**② 自定义业务异常**
- `CustomException(result_code, message)`：业务层抛异常携带 ResultCode
- `server.py` 中 `custom_exception_handler` 捕获，返回标准 Result 格式
- 使用场景：资源不存在、无权限等业务错误

**③ 分页模式**
- `PageParams(page: int = 1, page_size: int = 10)`：统一分页入参
- `PageResult[T](items, total, page, page_size)`：统一分页出参
- 用法：`Result.ok(PageResult(items=..., total=..., page=..., page_size=...))`

**④ CORS 配置**
- `create_app()` 中注册 `CORSMiddleware`
- 开发环境：`allow_origins=["*"]`
- 生产环境：配置具体域名列表

**⑤ SQLAlchemy Model 时间戳与外键约定**
- `created_at`：`server_default=text("(datetime('now', '+08:00'))")`（北京时间）
- `updated_at`：追加 `onupdate=text("(datetime('now', '+08:00'))")`
- **禁止物理外键（适用于所有数据库类型）**：关联字段只用 `Column(Integer, index=True, comment="关联 xxx 表 ID")`，不加 `ForeignKey()`。原因：统一多数据库适配，避免迁移复杂性，逻辑关联由应用层维护

**⑥ Pydantic Schema 约定**
- 响应 Schema：`model_config = ConfigDict(from_attributes=True)`（支持 ORM 对象直接映射）
- Create DTO：必填字段
- Update DTO：所有字段 `Optional`
- `Field(description="...")` 生成 API 文档
- `alias` 处理 camelCase ↔ snake_case（前后端字段名差异时使用）

### Review 清单新增 6 项

- [ ] Model 无 `ForeignKey()` 约束（只用 `index=True`）
- [ ] 关联字段有 `comment` 注明关联关系
- [ ] CORS 已配置，生产环境非 `*`
- [ ] 认证白名单包含 `/health`、`/ping`、`/docs`
- [ ] Update DTO 所有字段为 `Optional`
- [ ] 响应 Schema 有 `from_attributes=True`

### references/simple-project.md 新增模板

新增文件模板：
- `complex/auth/auth_util.py`（JWT 工具）
- `complex/auth/oauth.py`（`get_current_user` 依赖）
- `complex/constants/auth_whitelist.py`（白名单类）
- `complex/response/exception.py`（`CustomException`）
- `schemas/common/pagination.py`（`PageParams`、`PageResult[T]`）

更新现有模板：
- `models/user.py`：加时间戳 `server_default`，外键字段改为 `Column(Integer, index=True, comment="...")`，移除任何 `ForeignKey()`
- `modules/user/schemas/user_dto.py`：加 `ConfigDict(from_attributes=True)`、`Field(description=...)`、Update DTO 字段全 Optional

### references/complex-project.md 同步更新

- 认证模式（AuthWhitelist、get_current_user）加入 complex 结构
- Model 示例更新：无物理外键

### references/patterns.md（新建）

可选工具模式，标注"按需使用，需手动安装对应依赖"。在 SKILL.md Guide 末尾加链接：`详见 [references/patterns.md](references/patterns.md)`。

| 工具 | 额外依赖 | 用途 |
|------|----------|------|
| `convert_util.py` | 无 | `model_to_dict`、`model_to_schema`、`row_to_dict`、`to_camel_case` |
| `time_util.py` | 无 | `parse_time_range`（UTC → 北京时间 +8h） |
| `crypto_util.py` | `uv add cryptography` | AES-256-GCM 加密/解密（存储 API Key 等场景，仅提供思路，不保证安全合规，生产使用自行评估） |
| `request_context_util.py` | 无 | `get_required_space_id()`、`get_required_user_id()`（带 HTTPException 的便捷方法） |

---

## Task B：website-creator skill

### 定位

薄编排层：负责 Socratic 提问 + 规划输出，创建执行委托给 react-best-practices 和 fastapi-best-practices。

**前提条件**：执行前两个 skill 必须已存在于 `/Users/links/.agents/skills/`。如果不存在，输出错误提示停止执行。

### 文件结构

```
website-creator/
  SKILL.md    # 单文件，无 references
```

### 核心工作流

```
Phase 1（固定提问，总是问，不计入 Phase 2 轮数）
  Q1: 项目名称是什么？
  Q2: 前端网站 or 前后端全栈？
  Q3: 项目创建在哪个目录？（默认：当前工作目录）

Phase 2（动态追问，最多 5 轮，不含 Phase 1）
  目标：收集足够信息达到 95% 确认门槛
  每轮只问一个问题：
    - 核心功能/页面是什么？
    - 目标用户是谁？
    - 有特殊技术要求吗？
  超过 5 轮仍不确定：基于已有信息出规划，并在规划中标注"[待确认]"的假设项

95% 确认门槛：
  ✅ 项目名确定
  ✅ 类型（前端/全栈）确定
  ✅ 至少 3 个核心页面/功能明确
  ✅ 目标用户/用途清晰

Phase 3（输出规划，等用户明确确认）
  - 用户回复"yes / 确认 / 继续"等明确肯定 → 进入 Phase 4
  - 用户提出修改意见 → 根据修改更新规划，重新输出确认
  - 全栈项目的 JWT 认证是内置骨架，不可在此阶段取消
  - 格式见下方

Phase 4（确认后执行）
  1. 在目标目录创建 {name}/ 根目录
  2. git init（仅在根目录执行一次）
  3. 创建合并 .gitignore（见下方规则）
  4. 在 {name}/frontend/ 下执行 react-best-practices Init 阶段
     - 跳过该 skill 内的 `git init` 步骤（按步骤语义跳过，不依赖步骤序号）
  5. （全栈）在 {name}/backend/ 下执行 fastapi-best-practices Init 阶段
     - 同样跳过该 skill 内的 `git init` 步骤
  6. 创建根 README.md（内容：项目简介、技术栈、目录说明、本地启动命令）
  7. git add . && git commit -m "init: scaffold {name} project"
```

### "invoke" 说明

在 SKILL.md 中，"invoke react-best-practices" 的实现方式：
- 使用 Claude Code 的 `Skill` tool 调用对应 skill
- SKILL.md 中写明：`**REQUIRED SUB-SKILL:** Use react-best-practices (Init 阶段)`
- 同理引用 fastapi-best-practices

### "跳过 git init" 的传达方式

在 SKILL.md 中，Phase 4 的对应步骤明确标注：
> "执行 react-best-practices Init 阶段时，**跳过步骤 7（git init）**，因为 git 仓库已在根目录初始化。"

### 规划输出格式

```
📋 项目规划

项目名: {name}
类型: 前端 / 全栈

技术栈:
  前端: React + Vite + TypeScript + Antd + Tailwind CSS
  后端: FastAPI + SQLAlchemy + Alembic + SQLite  ← 仅全栈

核心页面/功能:
  - {功能 1}
  - {功能 2}
  - {功能 3}
  ...（[待确认] 标注不确定项，如有）

内置功能:
  - JWT 登录/注册（全栈项目默认包含，不可省略）

目录结构:
  {name}/          ← git 根目录
  ├── .gitignore
  ├── README.md
  └── frontend/
  └── backend/     ← 仅全栈

确认后开始创建，是否继续？
```

### .gitignore 合并规则

| 情况 | .gitignore 内容 |
|------|----------------|
| 纯前端 | node_modules/, dist/, .env, .DS_Store |
| 全栈 | 追加：.venv/, \_\_pycache\_\_/, config/\*.json, \*.pyc, data.db |

### 根 README.md 内容规范

```markdown
# {项目名}

{项目简介（1-2句，来自规划描述）}

## 技术栈
- 前端: React + Vite + TypeScript + Antd + Tailwind CSS
- 后端: FastAPI + SQLAlchemy（仅全栈）

## 目录
- frontend/ — React 前端
- backend/  — FastAPI 后端（仅全栈）

## 本地启动
# 前端
cd frontend && yarn dev

# 后端（仅全栈）
cd backend && ./run.sh
```

### 约束

- **禁止在 95% 确认前（或用户明确确认规划前）创建任何文件**
- `git init` 只在根目录执行一次
- 全栈项目始终包含 JWT 认证骨架
- 动态追问最多 5 轮，超出则带 [待确认] 假设出规划
- 依赖 react-best-practices 和 fastapi-best-practices 已存在；不存在时报错停止

---

## 执行顺序

1. Task A 先完成（fastapi-best-practices 改进）
2. Task B 再创建（website-creator 引用的 skill 均已是最新版）
3. 更新 .gitignore 白名单（已完成）
4. commit + push 到两个远程仓库（origin + iktapp）
