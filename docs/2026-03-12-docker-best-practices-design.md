# docker-best-practices Skill Design

**Date**: 2026-03-12
**Goal**: Create a `docker-best-practices` skill that encapsulates years of Docker experience — from analyzing a finished project to containerized local testing, multi-arch image push, and production deployment. Based primarily on Sage (production-grade, multi-stage, embedded MariaDB, nginx+WebSocket+SSE) with OneSub patterns (test/prod compose split, SQLite option).

**Skill location**: `/Users/links/.agents/skills/docker-best-practices/SKILL.md`
**Reference files**: `/Users/links/.agents/skills/docker-best-practices/references/`

---

## Overview

Three-phase skill (Init / Guide / Review) matching the established react-best-practices and fastapi-best-practices convention.

| Phase | Purpose |
|-------|---------|
| **Init** | Auto-scan project → ask only unknowable questions → generate complete `docker/` directory + `.dockerignore` |
| **Guide** | Step-by-step commands for: local test → image push → production deploy |
| **Review** | Quality checklist: image size, security, .dockerignore completeness, healthcheck |

---

## Phase 1: Init

### Auto-Detection (no questions)

Scan the project root to determine type:

| Condition | Type |
|-----------|------|
| `frontend/` + `backend/` both exist | Full-stack |
| Only `backend/` (with `pyproject.toml`) | Backend-only |
| Only `frontend/` (with `package.json`) | Frontend-only |

### Questions (only what can't be inferred, one at a time)

**Q1**: Image name? (format: `{namespace}/{project-name}`, e.g. `ai/sage`)

**Q2**: Version tag? (e.g. `1.0.0`)

**Q3**: Exposed port? (defaults: full-stack → 80 via Nginx, backend-only → 8000, frontend-only → 80)

**Q4** (full-stack / backend-only only): Database strategy?
- **A** — SQLite (embedded, zero-config)
- **B** — Embedded MariaDB (supports `USE_EMBEDDED_DB=true/false` toggle for external MySQL fallback)
- **C** — External only (no DB in container; configure connection via compose env)

### Files Generated

All files created under `docker/` at project root:

```
docker/
├── Dockerfile              ← multi-stage build (variant by project type)
├── entrypoint.sh           ← startup script (full-stack + backend-only only)
├── nginx.conf              ← reverse proxy config (full-stack + frontend-only)
├── docker-compose.yml      ← local test (build-based)
├── docker-compose.prod.yml ← production (image-based)
└── DEPLOY.md               ← build & deploy documentation
```

Project root:
- `.dockerignore` — updated/created to minimize image size

---

## File Templates

### Dockerfile — Full-Stack (React + FastAPI + uv workspaces)

Three-stage build pattern from Sage:

```dockerfile
# ========================
# Stage 1: Frontend Build
# ========================
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn config set registry https://registry.npmmirror.com && \
    yarn install --frozen-lockfile --network-timeout 1000000
COPY frontend/ ./
RUN yarn build

# ========================
# Stage 2: Backend Deps
# ========================
FROM python:3.11-slim AS backend-builder
WORKDIR /app

# China mirror
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# UV workspace: copy all pyproject.toml files first (cache deps layer)
COPY backend/pyproject.toml backend/uv.lock ./
COPY backend/{subpkg}/pyproject.toml ./{subpkg}/
# ... repeat for each workspace package

# Stub src dirs (uv sync needs them)
RUN for pkg in {subpkg1} {subpkg2}; do \
    mkdir -p $pkg/src && touch $pkg/src/__init__.py $pkg/README.md; done

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ========================
# Stage 3: Runtime Image
# ========================
FROM python:3.11-slim
WORKDIR /app

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y \
    nginx \
    # [IF embedded MariaDB] mariadb-server mariadb-client \
    curl vim net-tools && \
    rm -rf /var/lib/apt/lists/*

# [IF embedded MariaDB]
# RUN mkdir -p /var/run/mysqld /var/lib/mysql /var/log/mysql && \
#     chown -R mysql:mysql /var/run/mysqld /var/lib/mysql /var/log/mysql
# RUN printf "[mariadbd]\nport = {DB_PORT}\nbind-address = 0.0.0.0\n" \
#     > /etc/mysql/mariadb.conf.d/99-port.cnf

COPY --from=backend-builder /bin/uv /bin/uv
COPY --from=backend-builder /app/.venv /app/.venv
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Copy backend source (each workspace package)
COPY backend/{subpkg}/src /app/{subpkg}/src
COPY backend/{subpkg}/pyproject.toml /app/{subpkg}/
# ... repeat
COPY backend/pyproject.toml backend/uv.lock /app/
COPY backend/alembic.ini backend/migrations /app/

# Copy config, nginx, entrypoint
COPY backend/config /app/config
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Runtime dirs (mounted via volume)
RUN mkdir -p /app/logs /app/data

ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
ENV TZ=Asia/Shanghai
ENV PYTHONUNBUFFERED=1

EXPOSE {PORT}
# [IF embedded MariaDB] EXPOSE {DB_PORT}

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=60s \
    CMD curl -f http://localhost:{API_PORT}/ping || exit 1

ENTRYPOINT ["/entrypoint.sh"]
```

### Dockerfile — Backend-Only (FastAPI + uv)

Two-stage (builder + runtime), same uv pattern, no frontend stage, no nginx.

### Dockerfile — Frontend-Only (React static)

Two-stage (node builder + nginx static server), no Python at all.

---

### entrypoint.sh — Full-Stack with Embedded MariaDB Option

```bash
#!/bin/bash
set -e

echo "=== {ProjectName} {Version} ==="

mkdir -p /app/logs /app/data

USE_EMBEDDED="${USE_EMBEDDED_DB:-true}"

if [ "$USE_EMBEDDED" = "true" ]; then
    echo "📊 Database Mode: Embedded MariaDB"
    DB_ROOT_PASS="${DB_ROOT_PASSWORD:-changeme}"
    DB_NAME="${DB_NAME:-{project}}"

    if [ ! -d "/var/lib/mysql/mysql" ]; then
        mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql > /dev/null 2>&1
        service mariadb start > /dev/null 2>&1
        mysql -uroot <<EOF
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('${DB_ROOT_PASS}');
CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '${DB_ROOT_PASS}' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF
        service mariadb stop > /dev/null 2>&1
    fi

    service mariadb start > /dev/null 2>&1
    export MYSQL_HOST="127.0.0.1"
    export MYSQL_PORT="{DB_PORT}"
    export MYSQL_DB="${DB_NAME}"
    export MYSQL_USER="root"
    export MYSQL_PASSWORD="${DB_ROOT_PASS}"
else
    echo "📊 Database Mode: External MySQL"
fi

echo "🌐 Starting Nginx..."
nginx

echo "🚀 Starting FastAPI on port {API_PORT}..."
exec python -m {module.app}
```

### nginx.conf — Full-Stack (with WebSocket + SSE support)

```nginx
worker_processes 2;
events { worker_connections 1024; }

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile on;
    keepalive_timeout 65;

    gzip on;
    gzip_types text/plain text/css application/json application/javascript;
    gzip_min_length 1000;

    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    server {
        listen {PORT};

        # Static assets with long cache
        # Note: use root + rewrite (not alias) to avoid nginx alias+regex path bug
        location ~* ^/{prefix}/assets/.*\.(js|css|png|jpg|svg|woff2?)$ {
            root /app/frontend/dist;
            rewrite ^/{prefix}/(.*)$ /$1 break;
            expires 7d;
            add_header Cache-Control "public, immutable";
        }

        # React SPA (alias quirk: try_files checks against root, not alias path)
        location /{prefix} {
            alias /app/frontend/dist/;
            index index.html;
            try_files $uri $uri/ @spa_fallback;
        }

        location @spa_fallback {
            root /app/frontend/dist;
            rewrite ^/{prefix}(/.*)?$ /index.html break;
        }

        # API proxy (SSE + WebSocket compatible)
        location /{prefix}/api/ {
            proxy_pass http://127.0.0.1:{API_PORT}/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_read_timeout 300s;
            proxy_send_timeout 300s;
            proxy_buffering off;   # required for SSE streaming
            proxy_cache off;
        }

        location = / { return 301 /{prefix}/; }
    }
}
```

### docker-compose.yml — Local Test (build-based)

```yaml
services:
  {project}:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    image: {project}:{version}
    container_name: {project}
    ports:
      - "{PORT}:{PORT}"
      # [IF embedded MariaDB] - "{DB_PORT}:{DB_PORT}"
    volumes:
      # [IF embedded MariaDB]
      - ./resources/mysql/data:/var/lib/mysql
      - ./resources/mysql/logs:/var/log/mysql
      - ./logs:/app/logs
      - ./data:/app/data
    environment:
      - TZ=Asia/Shanghai
      # [IF embedded MariaDB]
      - USE_EMBEDDED_DB=true
      - DB_ROOT_PASSWORD=changeme
      - DB_NAME={project}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{API_PORT}/ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    restart: always
```

### docker-compose.prod.yml — Production (image-based)

```yaml
services:
  {project}:
    image: {registry}/{namespace}/{project}:{version}
    container_name: {project}
    ports:
      - "{HOST_PORT}:{PORT}"
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      # [IF embedded MariaDB]
      - ./resources/mysql/data:/var/lib/mysql
      - ./resources/mysql/logs:/var/log/mysql
    environment:
      - TZ=Asia/Shanghai
      # [IF embedded MariaDB]
      - USE_EMBEDDED_DB=true
      - DB_ROOT_PASSWORD=changeme
      - DB_NAME={project}
    restart: always
```

Production compose uses `./` relative paths — which resolve correctly because the file is placed in `/apps/{project}/` on the server, making `./logs` → `/apps/{project}/logs`.

### .dockerignore

```
# Git
.git
.gitignore

# Python
**/__pycache__/
**/*.pyc
**/*.pyo
**/.venv/
**/*.egg-info/
**/.ruff_cache/
**/.pytest_cache/

# Node
**/node_modules/
**/dist/
**/build/
**/.npm/
**/.yarn/

# Runtime data (mounted as volumes)
docker/resources/
docker/logs/
docker/data/

# Dev tools
.vscode/
.idea/
.DS_Store
Thumbs.db

# Docs / CI / Agent files
docs/
.github/
.claude/
.gemini/
*.md
!docker/DEPLOY.md

# Logs
*.log

# Tests
**/tests/
```

### DEPLOY.md — docker/ directory documentation

Structure:
1. 项目概述（类型、技术栈、端口说明）
2. 本地测试（创建目录 → build → up → verify 命令）
3. 镜像推送（登录 → buildx 命令 → tar 导出可选）
4. 生产部署（创建目录 → 权限 → docker-compose.prod.yml 命令）
5. 常用运维命令（logs、restart、进入容器、清理）
6. 环境变量说明表

---

## Phase 2: Guide

### 子节 1：本地测试

```bash
# 1. 创建本地持久化目录（一次性，按项目类型）
# 全栈 + MariaDB:
mkdir -p ./docker/{logs,resources/{mysql/{data,logs},diskcache,chromadb}}
# 全栈 + SQLite:
mkdir -p ./docker/{logs,data}
# 纯后端:
mkdir -p ./docker/{logs,data}

# 2. 构建并启动
cd docker
docker-compose build && docker-compose up -d --force-recreate

# 3. 验证
docker-compose logs -f
curl http://localhost:{PORT}/ping

# 4. 停止
docker-compose down        # 保留数据
docker-compose down -v     # 清除数据（重置）
```

### 子节 2：推送镜像

**登录提醒**（每次推送前先提示）：
```bash
docker login {PRIVATE_REGISTRY}   # 私有仓库
docker login                       # Docker Hub
```

询问用户：目标仓库（私库/Hub/两者）+ 架构（amd64/双架构）

**前置：确保 buildx builder 支持多架构**（首次使用时执行一次）
```bash
docker buildx create --use --platform linux/amd64,linux/arm64
docker buildx inspect --bootstrap
```

```bash
# 多架构推送私有仓库
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t {registry}/{namespace}/{project}:{version} \
  -f docker/Dockerfile \
  --push .

# 单架构推送 Docker Hub
docker buildx build \
  --platform linux/amd64 \
  -t {dockerhub_user}/{project}:{version} \
  -f docker/Dockerfile \
  --push .

# 可选：本地加载测试（单架构，推送前本地验证）
docker buildx build \
  --platform linux/amd64 \
  --load \
  -t {project}:{version} \
  -f docker/Dockerfile .

# 可选：导出 tar（离线部署/归档）
docker buildx build \
  --platform linux/amd64 \
  --output type=docker,dest={project}-{version}-amd64.tar \
  -f docker/Dockerfile .
```

### 子节 3：生产部署

```bash
# 服务器上执行
# 1. 创建目录（默认 /apps/{project}）
sudo mkdir -p /apps/{project}/{logs,data}
# [IF embedded MariaDB]
sudo mkdir -p /apps/{project}/resources/{mysql/{data,logs},diskcache,chromadb}

# 2. 权限（可选，出现权限问题时再执行）
sudo chmod -R 777 /apps/{project}
sudo chown -R root:root /apps/{project}

# 3. 上传 docker-compose.prod.yml 到 /apps/{project}/

# 4. 拉取并启动
cd /apps/{project}
docker login {registry}
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# 5. 验证
docker ps
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Phase 3: Review Checklist

### 镜像质量
- [ ] Dockerfile 使用多阶段构建（最终镜像不含 build-essential 等编译依赖）
- [ ] `apt-get` 安装后执行 `rm -rf /var/lib/apt/lists/*`
- [ ] uv sync 同时使用 `--no-install-project`（缓存层技巧）和 `--no-dev`（排除开发依赖）
- [ ] `.dockerignore` 排除 `node_modules/`、`.venv/`、`.git/`、`tests/`、`docs/`

### 安全
- [ ] 默认密码（`DB_ROOT_PASSWORD`）已在 compose 中覆盖或走环境变量
- [ ] 生产 compose 无 `build:` 块（只引用镜像，不在服务器上构建）
- [ ] 敏感配置不硬编码在 Dockerfile 里（通过 compose env 传入）

### 可维护性
- [ ] `docker/DEPLOY.md` 存在且包含完整的目录创建命令
- [ ] `docker-compose.yml`（测试）和 `docker-compose.prod.yml`（生产）分离
- [ ] HEALTHCHECK 已配置

### 网络
- [ ] nginx.conf 含 `proxy_buffering off` + `proxy_cache off`（SSE/流式响应必需）
- [ ] WebSocket 支持：`proxy_http_version 1.1` + `Upgrade`/`Connection` headers
- [ ] 静态资源 `expires 7d` 缓存头已设置

---

## Skill Frontmatter Description

```yaml
name: docker-best-practices
description: >
  Use when containerizing a project for testing or production deployment.
  Triggers: "docker化", "容器化", "写Dockerfile", "build镜像", "部署到服务器",
  "推送镜像", "docker-compose", or any request about containerizing,
  building Docker images, pushing to registry, or deploying containers.
  Covers three project types: full-stack (React+FastAPI), backend-only (FastAPI),
  frontend-only (React static). Includes embedded MariaDB pattern, multi-arch
  buildx, test/prod compose split, and production deployment commands.
  Outputs: docker/ directory with Dockerfile, entrypoint.sh, nginx.conf,
  docker-compose.yml, docker-compose.prod.yml, DEPLOY.md, and .dockerignore.
```

---

## Key Patterns (from Sage production experience)

1. **Aliyun apt mirror**: `sed -i 's/deb.debian.org/mirrors.aliyun.com/g'` — faster in China
2. **uv workspace stub pattern**: Create empty `src/__init__.py` + `README.md` before `uv sync` to enable layer caching
3. **USE_EMBEDDED_DB toggle**: Single image supports both embedded MariaDB and external MySQL
4. **SSE streaming**: `proxy_buffering off; proxy_cache off;` in nginx required for AI streaming responses
5. **MariaDB port config**: Use `99-force-tcp.cnf` override file to set custom port
6. **test vs prod compose split**: Test uses `build:`, prod uses `image:` with registry URL
7. **Production bind mounts**: Use absolute paths in prod compose (`./data` → `/apps/{project}/data`)
8. **One-line mkdir**: `mkdir -p ./{logs,resources/{mysql/{data,logs},diskcache,chromadb}}` brace expansion
9. **Permissions pattern**: `chmod -R 777` only when needed (not default), `chown root:root`
10. **buildx multi-arch**: Always use `docker buildx build` even for single-arch (consistent tooling)
