---
name: docker-best-practices
description: >
  Use when containerizing a project for local testing or production deployment.
  Triggers: "docker化", "容器化", "写Dockerfile", "build镜像", "推送镜像",
  "部署到服务器", "docker-compose", or any request about containerizing,
  building Docker images, pushing to a registry, or deploying containers.
  Covers three project types: full-stack (React + FastAPI), backend-only (FastAPI),
  frontend-only (React static site). Includes embedded MariaDB dual-mode pattern,
  multi-arch buildx, test/prod compose split, and production deployment commands.
  Outputs: docker/ directory with Dockerfile, entrypoint.sh, nginx.conf,
  docker-compose.yml, docker-compose.prod.yml, DEPLOY.md, and .dockerignore.
---

# Docker Best Practices

## 概述

从成品项目到容器化的全流程封装：分析项目结构、生成 docker/ 目录、本地测试、推送镜像仓库、生产环境部署。

**支持项目类型**：
- **全栈**：React 前端 + FastAPI 后端（含 Nginx 反向代理）
- **纯后端**：FastAPI only
- **纯前端**：React 静态站（Nginx serve）

**参考实现**：[references/](references/) 目录包含完整模板文件。

---

## 阶段一：初始化（Init）

### Step 1：自动扫描项目类型

扫描项目根目录，无需用户回答：

| 检测条件 | 判断结果 |
|---------|--------|
| 同时有 `frontend/` 和 `backend/` | 全栈 |
| 只有 `backend/`（含 `pyproject.toml`） | 纯后端 |
| 只有 `frontend/`（含 `package.json`） | 纯前端 |

### Step 2：收集必要信息（按顺序逐一询问）

**Q1**：镜像名称？（格式 `{namespace}/{project-name}`，如 `ai/sage`、`complex/onesub`）

**Q2**：版本号？（如 `1.0.0`）

**Q3**：对外暴露端口？
- 全栈默认：`80`（Nginx 统一入口）
- 纯后端默认：`8000`
- 纯前端默认：`80`

**Q4**（全栈 / 纯后端）：数据库策略？
- **A** — SQLite（嵌入，零配置，适合轻量项目）
- **B** — 嵌入式 MariaDB（支持 `USE_EMBEDDED_DB=true/false` 一键切换外部 MySQL，适合中大型项目）
- **C** — 纯外部数据库（容器不内置 DB，通过 compose env 配置连接）

### Step 3：生成 docker/ 目录

一次性产出所有文件：

```
docker/
├── Dockerfile              ← 多阶段构建（按项目类型裁剪）
├── entrypoint.sh           ← 启动脚本（全栈 + 纯后端）
├── nginx.conf              ← 反向代理配置（全栈 + 纯前端）
├── docker-compose.yml      ← 本地测试（build-based）
├── docker-compose.prod.yml ← 生产部署（image-based）
└── DEPLOY.md               ← 构建与部署全流程说明
```

项目根目录同步生成/更新：
- `.dockerignore` ← 最小化镜像体积

参考各类型模板：[references/templates.md](references/templates.md)

---

## 阶段二：开发指导（Guide）

### 子节 1：本地测试

**Step 1 — 创建本地持久化目录**（一次性，按项目类型）

```bash
# 全栈 + 嵌入式 MariaDB
mkdir -p ./docker/{logs,resources/{mysql/{data,logs},diskcache,chromadb}}

# 全栈 + SQLite / 纯后端
mkdir -p ./docker/{logs,data}

# 纯前端：无需创建目录
```

**Step 2 — 构建并启动**

```bash
cd docker
docker-compose build && docker-compose up -d --force-recreate
```

**Step 3 — 验证运行**

```bash
docker-compose logs -f                        # 实时日志
docker ps                                     # 确认 Up 状态
curl http://localhost:{PORT}/ping             # 验证健康端点
```

**Step 4 — 停止**

```bash
docker-compose down        # 停止，保留 volume 数据
docker-compose down -v     # 停止并清除 volume（重置数据）
```

---

### 子节 2：推送镜像

**前置：确保 buildx 支持多架构**（首次使用执行一次）

```bash
docker buildx create --use --platform linux/amd64,linux/arm64
docker buildx inspect --bootstrap
```

**登录提醒**（每次推送前必须先登录）

```bash
docker login {私有仓库地址}    # 如 docker login 192.168.1.91:9528
docker login                   # Docker Hub
```

**Step 1 — 询问推送目标**

- A — 私有仓库（提供地址，如 `192.168.1.91:9528/ai/sage:1.0.0`）
- B — Docker Hub（提供 `username/project:tag`）
- C — 两者都推

**Step 2 — 询问目标架构**

- A — 单架构 amd64（快，适合纯 x86_64 服务器）
- B — 双架构 amd64 + arm64（适合混合/ARM 环境）

**Step 3 — 生成构建推送命令**

```bash
# 多架构 → 私有仓库
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t 192.168.1.91:9528/{namespace}/{project}:{version} \
  -f docker/Dockerfile \
  --push .

# 单架构 → Docker Hub
docker buildx build \
  --platform linux/amd64 \
  -t {dockerhub_user}/{project}:{version} \
  -f docker/Dockerfile \
  --push .

# 可选：本地加载验证（推送前本地测试，仅单架构）
docker buildx build \
  --platform linux/amd64 \
  --load \
  -t {project}:{version} \
  -f docker/Dockerfile .

# 可选：导出 tar 包（离线部署 / 归档）
docker buildx build \
  --platform linux/amd64 \
  --output type=docker,dest={project}-{version}-amd64.tar \
  -f docker/Dockerfile .
```

---

### 子节 3：生产环境部署

**Step 1 — 服务器创建目录**（默认路径 `/apps/{project}`）

```bash
# 全栈 + 嵌入式 MariaDB
sudo mkdir -p /apps/{project}/{logs,resources/{mysql/{data,logs},diskcache,chromadb}}

# 全栈 + SQLite / 纯后端
sudo mkdir -p /apps/{project}/{logs,data}

# 纯前端：无需创建目录
```

**Step 2 — 设置权限**（可选，出现权限问题时执行）

```bash
sudo chmod -R 777 /apps/{project}
sudo chown -R root:root /apps/{project}
```

**Step 3 — 上传 docker-compose.prod.yml 到服务器**

将 `docker/docker-compose.prod.yml` 放到服务器 `/apps/{project}/` 目录。

> `docker-compose.prod.yml` 使用 `./` 相对路径，放在 `/apps/{project}/` 下即自动解析为正确绝对路径。

**Step 4 — 拉取镜像并启动**

```bash
cd /apps/{project}
docker login {registry}                                           # 私有仓库登录
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

**Step 5 — 验证**

```bash
docker ps
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 阶段三：代码审查（Review）

### 镜像质量

- [ ] Dockerfile 使用多阶段构建（最终镜像不含 `build-essential` 等编译依赖）
- [ ] 每个 `apt-get install` 后执行 `rm -rf /var/lib/apt/lists/*`
- [ ] uv sync 使用 `--frozen --no-install-project --no-dev`（三个 flag 都需要）
- [ ] `.dockerignore` 排除：`node_modules/`、`.venv/`、`.git/`、`tests/`、`docs/`、`*.log`

### 安全

- [ ] 默认密码（`DB_ROOT_PASSWORD` 等）通过 compose `environment` 传入，不硬编码在 Dockerfile
- [ ] 生产 `docker-compose.prod.yml` 无 `build:` 块（只引用镜像）
- [ ] 敏感配置不出现在镜像层中

### 可维护性

- [ ] `docker/DEPLOY.md` 存在，包含完整目录创建命令和启动命令
- [ ] `docker-compose.yml`（测试 build-based）和 `docker-compose.prod.yml`（生产 image-based）已分离
- [ ] `HEALTHCHECK` 已配置

### 网络（全栈项目）

- [ ] nginx.conf 含 `proxy_buffering off; proxy_cache off;`（SSE 流式响应必需）
- [ ] WebSocket 支持：`proxy_http_version 1.1` + `Upgrade` / `Connection` headers
- [ ] 静态资源设置 `expires 7d` 缓存头
- [ ] API 超时 `proxy_read_timeout 300s`（AI 长时响应场景）
