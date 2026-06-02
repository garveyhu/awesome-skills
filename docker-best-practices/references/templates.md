# 单镜像模板（degenerate case）

> ⚠️ 单镜像只用于"genuinely tiny"的项目。任何稍微复杂一点的项目都走 [multi-image.md](multi-image.md)。
>
> 单镜像用于：纯前端静态站、单文件 Python 脚本服务、镜像 < 500MB 且不需要 tar 离线分发的场景。

模板变量说明：
- `{project}` — 项目名，如 `myapp`
- `{version}` — 镜像版本
- `{PORT}` — 对外暴露端口
- `{API_PORT}` — FastAPI 内部端口
- `{DB_PORT}` — 嵌入式 MariaDB 端口
- `{prefix}` — URL 前缀
- `{namespace}` — 镜像仓库命名空间
- `{registry}` — 私有仓库地址
- `{module.app}` — Python 启动模块

单镜像下三区结构仍然保留（一致性 > 简洁），只是 images/ 下只有一个 Dockerfile：

```
docker/
├── README.md
├── images/
│   ├── Dockerfile               ← 单文件，不带 .base/.code 后缀
│   ├── entrypoint.sh
│   ├── nginx.conf
│   └── .env / .env.example      ← 只有一个 {PROJECT_UPPER}_TAG
├── containers/
│   ├── docker-compose.yml       ← 没有 build 壳服务，没有 init 容器
│   └── <env>/docker-compose.yml
└── scripts/
    ├── build-images.sh          ← 单镜像版本，不接受 target 参数
    ├── push-images.sh           ← 同上
    └── run-local.sh             ← 同上
```

---

## Dockerfile — 全栈（React + FastAPI + uv workspaces）

三阶段构建：前端 → 后端依赖 → 运行时。

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

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ uv

COPY backend/pyproject.toml backend/uv.lock ./
COPY backend/{subpkg1}/pyproject.toml ./{subpkg1}/
COPY backend/{subpkg2}/pyproject.toml ./{subpkg2}/

RUN for pkg in {subpkg1} {subpkg2}; do \
    mkdir -p $pkg/src && touch $pkg/src/__init__.py $pkg/README.md; done

# 国内 PyPI 镜像（见 references/cn-mirrors.md）——uv 默认走官方源，国内极慢
ENV UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ========================
# Stage 3: Runtime
# ========================
FROM python:3.11-slim
WORKDIR /app

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y \
    nginx \
    # 嵌入式 MariaDB（按需取消注释）：
    # mariadb-server mariadb-client \
    curl vim && \
    rm -rf /var/lib/apt/lists/*

# 嵌入式 MariaDB 目录权限：
# RUN mkdir -p /var/run/mysqld /var/lib/mysql /var/log/mysql && \
#     chown -R mysql:mysql /var/run/mysqld /var/lib/mysql /var/log/mysql

# MariaDB 端口配置：
# RUN printf "[mariadbd]\nport = {DB_PORT}\nbind-address = 0.0.0.0\n" \
#     > /etc/mysql/mariadb.conf.d/99-port.cnf

COPY --from=backend-builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=backend-builder /app/.venv /app/.venv
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# 后端源码（每个 workspace 子包）
COPY backend/{subpkg1}/src /app/{subpkg1}/src
COPY backend/{subpkg1}/pyproject.toml /app/{subpkg1}/
COPY backend/{subpkg2}/src /app/{subpkg2}/src
COPY backend/{subpkg2}/pyproject.toml /app/{subpkg2}/
COPY backend/pyproject.toml backend/uv.lock /app/
COPY backend/alembic.ini /app/
COPY backend/migrations /app/migrations
COPY backend/config /app/config

# nginx + 启动脚本
COPY docker/images/nginx.conf /etc/nginx/nginx.conf
COPY docker/images/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN mkdir -p /app/logs /app/data

ENV PYTHONPATH=/app \
    PATH="/app/.venv/bin:$PATH" \
    TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1

EXPOSE {PORT}

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=60s \
    CMD curl -f http://localhost:{API_PORT}/ping || exit 1

ENTRYPOINT ["/entrypoint.sh"]
```

---

## Dockerfile — 纯后端（FastAPI + uv）

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ uv

COPY pyproject.toml uv.lock ./
# 国内 PyPI 镜像（见 references/cn-mirrors.md）——uv 默认走官方源，国内极慢
ENV UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

FROM python:3.11-slim
WORKDIR /app

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder /app/.venv /app/.venv

COPY src/ ./src/
COPY alembic.ini ./
COPY migrations/ ./migrations/
COPY config/ ./config/
COPY pyproject.toml uv.lock ./

RUN mkdir -p /app/logs /app/data

ENV PYTHONPATH=/app \
    PATH="/app/.venv/bin:$PATH" \
    TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1

EXPOSE {API_PORT}
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=30s \
    CMD curl -f http://localhost:{API_PORT}/ping || exit 1

CMD ["python", "-m", "{module.app}"]
```

---

## Dockerfile — 纯前端（React 静态站）

```dockerfile
FROM node:20-slim AS builder
WORKDIR /app

COPY package.json yarn.lock ./
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn config set registry https://registry.npmmirror.com && \
    yarn install --frozen-lockfile --network-timeout 1000000

COPY . ./
RUN yarn build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY docker/images/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE {PORT}
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -q --spider http://localhost:{PORT}/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

---

## entrypoint.sh — 全栈（嵌入式 MariaDB 双模式）

```bash
#!/bin/bash
set -e

echo "=== {project} {version} ==="

mkdir -p /app/logs /app/data

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
    fi

    service mariadb start > /dev/null 2>&1
    export MYSQL_HOST="127.0.0.1" MYSQL_PORT="{DB_PORT}" MYSQL_DB="${DB_NAME}" \
           MYSQL_USER="root" MYSQL_PASSWORD="${DB_ROOT_PASS}"
else
    echo "[DB] Mode: External MySQL (${MYSQL_HOST}:${MYSQL_PORT})"
fi

echo "[Web] Starting Nginx on port {PORT}..."
nginx

echo "[API] Starting FastAPI on port {API_PORT}..."
exec python -m {module.app}
```

---

## nginx.conf — 全栈（含 WebSocket + SSE）

```nginx
worker_processes 2;
events { worker_connections 1024; }

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    sendfile      on;
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
        server_name localhost;

        # 静态资源强缓存
        location ~* ^/{prefix}/assets/.*\.(js|css|png|jpg|gif|ico|svg|woff2?|ttf|eot)$ {
            root /app/frontend/dist;
            rewrite ^/{prefix}/(.*)$ /$1 break;
            expires 7d;
            add_header Cache-Control "public, immutable";
        }

        # React SPA
        location /{prefix} {
            alias /app/frontend/dist/;
            index index.html;
            try_files $uri $uri/ @spa_fallback;
        }

        location @spa_fallback {
            root /app/frontend/dist;
            rewrite ^/{prefix}(/.*)?$ /index.html break;
        }

        # API 反向代理
        location /{prefix}/api/ {
            proxy_pass http://127.0.0.1:{API_PORT}/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            proxy_read_timeout 300s;
            proxy_send_timeout 300s;
            proxy_connect_timeout 60s;

            # SSE / 流式响应必须关闭缓冲
            proxy_buffering off;
            proxy_cache off;
        }

        location = / { return 301 /{prefix}/; }
    }
}
```

---

## docker/containers/docker-compose.yml — 本地开发

```yaml
name: {project}

services:
  {project}:
    build:
      context: ../..
      dockerfile: docker/images/Dockerfile
    image: {project}:${{PROJECT_UPPER}_TAG}
    container_name: {project}
    ports:
      - "{PORT}:{PORT}"
      # 嵌入式 MariaDB：- "{DB_PORT}:{DB_PORT}"
    volumes:
      - ./data/logs:/app/logs
      - ./data/app:/app/data
      # 嵌入式 MariaDB：
      # - ./data/mysql/data:/var/lib/mysql
      # - ./data/mysql/logs:/var/log/mysql
    environment:
      - TZ=Asia/Shanghai
      # 嵌入式 MariaDB：
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

## docker/containers/<env>/docker-compose.yml — 生产部署

```yaml
name: {project}-{env}

services:
  {project}:
    image: {registry}/{namespace}/{project}:${{PROJECT_UPPER}_TAG}
    container_name: {project}-{env}
    ports:
      - "{HOST_PORT}:{PORT}"
    volumes:
      - ./data/logs:/app/logs
      - ./data/app:/app/data
      # 嵌入式 MariaDB：
      # - ./data/mysql/data:/var/lib/mysql
      # - ./data/mysql/logs:/var/log/mysql
    environment:
      - TZ=Asia/Shanghai
      # - USE_EMBEDDED_DB=true
      # - DB_ROOT_PASSWORD={prod-pass}
    restart: always
```

---

## .dockerignore（项目根）

控制 `docker build .` 时拷给 daemon 的 build context。**关键作用两个**：
1. **不要把宿主机的运行时数据进 context**（`docker/containers/data/` 下可能有几个 GB 的 mariadb 数据，拷给 docker daemon 巨慢且会被误打进镜像）
2. **不要把凭据进镜像**（`.registry.env` / `images/.env` 真值不能泄进镜像）

```
# ============================================================================
# .dockerignore — 控制 docker build 时拷给 daemon 的 build context
# ============================================================================

# Git / VCS / IDE
.git
.idea
.vscode
*.iml

# 构建产物（builder 阶段会重新生成）
**/target/
**/build/
packages/
**/__pycache__/
**/*.pyc
**/.venv/
**/*.egg-info/
**/.pytest_cache/
**/.mypy_cache/
**/.ruff_cache/

# Node / 前端
**/node_modules/
**/dist/

# 运行时数据（绝不能打进镜像，dev 跑时 volume 挂载产生）
**/logs/
**/data/
docker/containers/data/
docker/containers/*/data/

# 真值 / 凭据（不要泄进镜像）
docker/images/.env
docker/scripts/.registry.env
docker/.env

# 文档（保留 docker/README.md 没意义；Dockerfile 不需要）
docs/
*.md
!docker/README.md

# 日志 / OS / 杂项
*.log
*.tmp
derby.log
.DS_Store
**/.DS_Store
*.swp

# 测试
**/tests/

# 反向例外：保留 docker/（COPY docker/images/entrypoint.sh 等需要）
# 上面的 .env / data/ 等敏感子目录已显式排除
!docker/
```

---

## .gitignore（项目根）

```
# ============================================================================
# 构建产物 / IDE
# ============================================================================
**/target/
**/*.iml
/.idea/
/.vscode/
/build/
/packages/
/logs/
/data/

# ============================================================================
# 日志 / 杂项
# ============================================================================
*.log
*.tmp
.DS_Store

# ============================================================================
# Docker 三区结构
# ============================================================================
# 镜像 tag 真值（.env.example 入库；真值含密码 / 内部地址，不入）
docker/images/.env
# dev 跑时挂载的运行时数据（mariadb / 日志等，体积可能很大）
docker/containers/data/
docker/containers/*/data/
# 仓库凭据
docker/scripts/.registry.env
```

> ⚠️ **常见踩坑**：`.gitignore` 漏写 `docker/containers/data/` → `git add -A` 一次把几个 GB 的 mariadb 运行时数据全 commit 入库，commit 巨大、反向修复成本高（要 `git rm --cached -r` 撤掉 + 重做 commit）。新建 docker 项目第一步就把这两个 ignore 文件写好。

---

## docker/images/.env.example

```env
{PROJECT_UPPER}_TAG={version}
```

---

## 单镜像下的脚本简化

`build-images.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT"

[ -f docker/images/.env ] || cp docker/images/.env.example docker/images/.env
set -a; . docker/images/.env; set +a

echo "→ building {project}:${{PROJECT_UPPER}_TAG}"
docker build -t "{project}:${{PROJECT_UPPER}_TAG}" -f docker/images/Dockerfile .

echo "✅ done"
```

`run-local.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT"

[ -f docker/images/.env ] || cp docker/images/.env.example docker/images/.env

mkdir -p docker/containers/data/{logs,app}

"${ROOT}/docker/scripts/build-images.sh"

DC="docker compose --env-file docker/images/.env -f docker/containers/docker-compose.yml"
$DC down --remove-orphans 2>/dev/null || true
$DC up -d --remove-orphans

echo "🎉 {project} 已启动 → http://localhost:{PORT}"
```

`push-images.sh` 类似多镜像版，去掉 case 分支即可。
