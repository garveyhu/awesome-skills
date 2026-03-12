# Docker Templates Reference

模板变量说明：
- `{project}` — 项目名，如 `sage`、`onesub`
- `{version}` — 镜像版本，如 `1.0.0`
- `{PORT}` — 对外暴露端口（Nginx，如 `80`、`5273`）
- `{API_PORT}` — FastAPI 内部端口（如 `8000`、`5275`）
- `{DB_PORT}` — 嵌入式 MariaDB 端口（如 `3306`、`5274`）
- `{prefix}` — URL 前缀（如 `sage`，访问路径为 `/sage/`）
- `{namespace}` — 镜像仓库命名空间，如 `ai`、`complex`
- `{registry}` — 私有仓库地址，如 `192.168.1.91:9528`
- `{module.app}` — Python 启动模块，如 `sage.app`、`app.main:app`

---

## Dockerfile — 全栈（React + FastAPI + uv workspaces）

三阶段构建：前端构建 → 后端依赖构建 → 最终运行镜像。

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
# Stage 2: Backend Deps (uv workspace)
# ========================
FROM python:3.11-slim AS backend-builder
WORKDIR /app

# 阿里云 apt 镜像（国内加速，bookworm 格式）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 先复制所有 pyproject.toml + uv.lock（利用 Docker 层缓存，依赖不变就不重新安装）
COPY backend/pyproject.toml backend/uv.lock ./
COPY backend/{subpkg1}/pyproject.toml ./{subpkg1}/
COPY backend/{subpkg2}/pyproject.toml ./{subpkg2}/
# ... 每个 workspace 子包重复一行

# 创建占位目录（uv sync --no-install-project 需要目录存在）
RUN for pkg in {subpkg1} {subpkg2}; do \
    mkdir -p $pkg/src && touch $pkg/src/__init__.py $pkg/README.md; done

# 安装依赖（--frozen 锁定版本，--no-install-project 只装依赖不装项目，--no-dev 排除开发依赖）
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
    # [如果使用嵌入式 MariaDB，取消注释以下两行]
    # mariadb-server \
    # mariadb-client \
    curl vim net-tools iproute2 && \
    rm -rf /var/lib/apt/lists/*

# [嵌入式 MariaDB：初始化目录权限]
# RUN mkdir -p /var/run/mysqld /var/lib/mysql /var/log/mysql && \
#     chown -R mysql:mysql /var/run/mysqld /var/lib/mysql /var/log/mysql

# [嵌入式 MariaDB：自定义端口配置]
# RUN printf "[mariadbd]\nport = {DB_PORT}\nbind-address = 0.0.0.0\n" \
#     > /etc/mysql/mariadb.conf.d/99-port.cnf && \
#     chmod 644 /etc/mysql/mariadb.conf.d/99-port.cnf

# 从 builder 阶段复制 uv 和虚拟环境
COPY --from=backend-builder /bin/uv /bin/uv
COPY --from=backend-builder /app/.venv /app/.venv

# 从 frontend-builder 复制构建产物
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# 复制后端源码（每个 workspace 子包）
COPY backend/{subpkg1}/src /app/{subpkg1}/src
COPY backend/{subpkg1}/pyproject.toml /app/{subpkg1}/
COPY backend/{subpkg2}/src /app/{subpkg2}/src
COPY backend/{subpkg2}/pyproject.toml /app/{subpkg2}/
# ... 重复

# 复制根配置
COPY backend/pyproject.toml backend/uv.lock /app/
COPY backend/alembic.ini /app/
COPY backend/migrations /app/migrations
COPY backend/config /app/config

# 复制 nginx + 启动脚本
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 运行时数据目录（通过 volume 挂载持久化）
RUN mkdir -p /app/logs /app/data

ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
ENV TZ=Asia/Shanghai
ENV PYTHONUNBUFFERED=1

EXPOSE {PORT}
# [嵌入式 MariaDB] EXPOSE {DB_PORT}

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=60s \
    CMD curl -f http://localhost:{API_PORT}/ping || exit 1

ENTRYPOINT ["/entrypoint.sh"]
```

---

## Dockerfile — 纯后端（FastAPI + uv）

两阶段构建，无前端，无 nginx。

```dockerfile
# ========================
# Stage 1: Backend Deps
# ========================
FROM python:3.11-slim AS builder
WORKDIR /app

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ========================
# Stage 2: Runtime Image
# ========================
FROM python:3.11-slim
WORKDIR /app

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y curl vim && rm -rf /var/lib/apt/lists/*

COPY --from=builder /bin/uv /bin/uv
COPY --from=builder /app/.venv /app/.venv

COPY src/ ./src/
COPY alembic.ini ./
COPY migrations/ ./migrations/
COPY config/ ./config/
COPY pyproject.toml uv.lock ./

RUN mkdir -p /app/logs /app/data

ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
ENV TZ=Asia/Shanghai
ENV PYTHONUNBUFFERED=1

EXPOSE {API_PORT}

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=30s \
    CMD curl -f http://localhost:{API_PORT}/ping || exit 1

CMD ["python", "-m", "{module.app}"]
```

---

## Dockerfile — 纯前端（React 静态站）

两阶段构建，最终只有 nginx + 静态文件。

```dockerfile
# ========================
# Stage 1: Build
# ========================
FROM node:20-slim AS builder
WORKDIR /app

COPY package.json yarn.lock ./
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn config set registry https://registry.npmmirror.com && \
    yarn install --frozen-lockfile --network-timeout 1000000

COPY . ./
RUN yarn build

# ========================
# Stage 2: Serve
# ========================
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE {PORT}

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -q --spider http://localhost:{PORT}/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

---

## entrypoint.sh — 全栈（支持嵌入式 MariaDB 切换）

```bash
#!/bin/bash
set -e

echo "=== {project} {version} ==="
echo "Starting at $(date)"

mkdir -p /app/logs /app/data

# ========================
# 数据库模式
# ========================
USE_EMBEDDED="${USE_EMBEDDED_DB:-true}"

if [ "$USE_EMBEDDED" = "true" ]; then
    echo "[DB] Mode: Embedded MariaDB"
    DB_ROOT_PASS="${DB_ROOT_PASSWORD:-changeme}"
    DB_NAME="${DB_NAME:-{project}}"

    if [ ! -d "/var/lib/mysql/mysql" ]; then
        echo "[DB] First run: initializing MariaDB..."
        mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql > /dev/null 2>&1
        service mariadb start > /dev/null 2>&1
        mysql -uroot <<EOF
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('${DB_ROOT_PASS}');
CREATE DATABASE IF NOT EXISTS ${DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '${DB_ROOT_PASS}' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF
        service mariadb stop > /dev/null 2>&1
        echo "[DB] Initialized successfully."
    fi

    service mariadb start > /dev/null 2>&1
    export MYSQL_HOST="127.0.0.1"
    export MYSQL_PORT="{DB_PORT}"
    export MYSQL_DB="${DB_NAME}"
    export MYSQL_USER="root"
    export MYSQL_PASSWORD="${DB_ROOT_PASS}"
    echo "[DB] MariaDB started on port {DB_PORT}"
else
    echo "[DB] Mode: External MySQL (${MYSQL_HOST}:${MYSQL_PORT})"
fi

# ========================
# Nginx
# ========================
echo "[Web] Starting Nginx on port {PORT}..."
nginx

# ========================
# FastAPI
# ========================
echo "[API] Starting FastAPI on port {API_PORT}..."
exec python -m {module.app}
```

---

## nginx.conf — 全栈（含 WebSocket + SSE 支持）

```nginx
worker_processes 2;
events { worker_connections 1024; }

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile      on;
    keepalive_timeout 65;

    # Gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    gzip_min_length 1000;
    gzip_vary on;

    # WebSocket 升级映射
    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    server {
        listen {PORT};
        server_name localhost;

        # 静态资源强缓存（JS/CSS hash 文件名，永不过期）
        # 使用 root + rewrite 避免 nginx alias+regex 路径丢失问题
        location ~* ^/{prefix}/assets/.*\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            root /app/frontend/dist;
            rewrite ^/{prefix}/(.*)$ /$1 break;
            expires 7d;
            add_header Cache-Control "public, immutable";
        }

        # React SPA（alias + named location 解决 try_files 路径问题）
        location /{prefix} {
            alias /app/frontend/dist/;
            index index.html;
            try_files $uri $uri/ @spa_fallback;
        }

        location @spa_fallback {
            root /app/frontend/dist;
            rewrite ^/{prefix}(/.*)?$ /index.html break;
        }

        # API 反向代理（支持 SSE 流式输出 + WebSocket）
        location /{prefix}/api/ {
            proxy_pass http://127.0.0.1:{API_PORT}/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # AI 长时响应超时
            proxy_read_timeout 300s;
            proxy_send_timeout 300s;
            proxy_connect_timeout 60s;

            # SSE 流式响应必须关闭缓冲
            proxy_buffering off;
            proxy_cache off;
        }

        # 根路径重定向
        location = / { return 301 /{prefix}/; }
    }
}
```

---

## nginx.conf — 纯前端静态站

```nginx
server {
    listen {PORT};
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    gzip on;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml image/svg+xml;

    # SPA 路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源缓存
    location ~* \.(?:ico|css|js|gif|jpe?g|png|svg|woff2?|eot|ttf|webp)$ {
        expires 6M;
        access_log off;
        add_header Cache-Control "public, max-age=15552000, immutable";
    }
}
```

---

## docker-compose.yml — 本地测试（build-based）

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
      # [嵌入式 MariaDB] - "{DB_PORT}:{DB_PORT}"
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      # [嵌入式 MariaDB]
      # - ./resources/mysql/data:/var/lib/mysql
      # - ./resources/mysql/logs:/var/log/mysql
      # [ChromaDB / DiskCache 等]
      # - ./resources/chromadb:/app/resources/chromadb
      # - ./resources/diskcache:/app/resources/diskcache
    environment:
      - TZ=Asia/Shanghai
      # [嵌入式 MariaDB]
      # - USE_EMBEDDED_DB=true
      # - DB_ROOT_PASSWORD=changeme
      # - DB_NAME={project}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{API_PORT}/ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    restart: always
```

---

## docker-compose.prod.yml — 生产部署（image-based）

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
      # [嵌入式 MariaDB]
      # - ./resources/mysql/data:/var/lib/mysql
      # - ./resources/mysql/logs:/var/log/mysql
    environment:
      - TZ=Asia/Shanghai
      # [嵌入式 MariaDB]
      # - USE_EMBEDDED_DB=true
      # - DB_ROOT_PASSWORD=changeme
      # - DB_NAME={project}
    restart: always
```

> 此文件放在服务器 `/apps/{project}/` 目录下，`./` 路径即解析为该目录。

---

## .dockerignore

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
**/.mypy_cache/

# Node
**/node_modules/
**/dist/
**/build/
**/.npm/
**/.yarn/

# 运行时数据（通过 volume 挂载，不打进镜像）
docker/resources/
docker/logs/
docker/data/

# IDE / OS
.vscode/
.idea/
.DS_Store
Thumbs.db
*.swp

# Agent / CI 文件
.claude/
.gemini/
.github/
*.skill

# 文档（保留 docker/DEPLOY.md）
docs/
*.md
!docker/DEPLOY.md

# 日志
*.log

# 测试
**/tests/
```

---

## DEPLOY.md — docker/ 目录说明文档模板

生成时根据实际项目填充，放在 `docker/DEPLOY.md`：

```markdown
# {project} Docker 构建与部署

## 项目信息

| 项目 | 说明 |
|------|------|
| 类型 | 全栈 / 纯后端 / 纯前端 |
| 技术栈 | React + FastAPI / FastAPI / React |
| 镜像名 | {registry}/{namespace}/{project}:{version} |
| 对外端口 | {PORT}（Nginx / API / Nginx） |
| API 端口 | {API_PORT}（容器内部） |
| 数据库 | SQLite / 嵌入式 MariaDB:{DB_PORT} / 外部 MySQL |

## 目录结构

```
docker/
├── Dockerfile
├── entrypoint.sh
├── nginx.conf
├── docker-compose.yml      ← 本地测试
├── docker-compose.prod.yml ← 生产部署
└── DEPLOY.md               ← 本文档
```

## 本地测试

```bash
# 1. 创建本地持久化目录（首次执行）
mkdir -p ./docker/{logs,data}
# 如果使用嵌入式 MariaDB：
# mkdir -p ./docker/{logs,resources/{mysql/{data,logs}}}

# 2. 构建并启动
cd docker
docker-compose build && docker-compose up -d --force-recreate

# 3. 验证
docker-compose logs -f
curl http://localhost:{PORT}/ping

# 4. 停止
docker-compose down         # 保留数据
docker-compose down -v      # 清除数据
```

## 推送镜像

```bash
# 首次使用需配置 buildx 多架构支持
docker buildx create --use --platform linux/amd64,linux/arm64
docker buildx inspect --bootstrap

# 登录仓库
docker login {registry}

# 构建并推送（多架构）
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t {registry}/{namespace}/{project}:{version} \
  -f docker/Dockerfile \
  --push .

# 或导出 tar（离线部署）
docker buildx build \
  --platform linux/amd64 \
  --output type=docker,dest={project}-{version}-amd64.tar \
  -f docker/Dockerfile .
```

## 生产部署

```bash
# 服务器上执行

# 1. 创建目录
sudo mkdir -p /apps/{project}/{logs,data}
# 如果使用嵌入式 MariaDB：
# sudo mkdir -p /apps/{project}/resources/{mysql/{data,logs}}

# 2. 权限（出现权限问题时执行）
sudo chmod -R 777 /apps/{project}
sudo chown -R root:root /apps/{project}

# 3. 将 docker-compose.prod.yml 放到 /apps/{project}/

# 4. 拉取并启动
cd /apps/{project}
docker login {registry}
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# 5. 验证
docker ps
docker-compose -f docker-compose.prod.yml logs -f
```

## 常用运维命令

```bash
# 查看日志
docker logs {project} -f --tail 100

# 进入容器
docker exec -it {project} bash

# 重启服务
docker restart {project}

# 查看资源占用
docker stats {project}

# 清理无用镜像（释放磁盘）
docker image prune -f
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `TZ` | `Asia/Shanghai` | 时区 |
| `USE_EMBEDDED_DB` | `true` | 是否使用嵌入式 MariaDB |
| `DB_ROOT_PASSWORD` | `changeme` | MariaDB root 密码（**生产必须修改**） |
| `DB_NAME` | `{project}` | 数据库名 |
```
