# 多镜像拆分方案（4-Image Split）

适用于：**重型项目** + **tar 离线下发** 或 **频繁更新代码但 deps/模型稳定** 的场景。

## 架构思想

把单一 7GB 重型镜像拆成 4 个**互不继承**的镜像，运行时靠 compose 的 init 容器把 data-only 镜像内容拷到 named volume，主容器挂载这些 volume 启动。效果：代码变更只传 ~100MB 的 `code` tar，其余层不动。

### 镜像职责边界

| 镜像 | 基底 | 内容 | 更新频率 | 典型大小 |
|------|------|------|---------|---------|
| `{project}-base` | `python:3.11-slim`（或语言基底） | 系统包（nginx、mariadb、libs）+ 配置 + `entrypoint.sh` + `uv` 二进制 | 极少（系统包升级） | ~900MB |
| `{project}-venv` | `busybox:musl` | 仅 `/export/.venv`（uv sync / pip install 产物） | 少（`uv.lock` 变化时） | ~1-2GB |
| `{project}-models` | `busybox:musl` | 仅 `/export/models`（离线模型等） | 几乎不 | ~400MB-数 GB |
| `{project}-code` | `busybox:musl` | `/export/` 下：后端源码 + pyproject + 启动器 + migrations + 配置 + 前端 dist + nginx.conf | 每次发版 | ~50-200MB |

### 边界判断原则

- `nginx.conf` 随代码走（路由变化是业务改动）
- `entrypoint.sh` 放 base（启动流程稳定）
- `pyproject.toml` / lock 文件放 code（运行时 migration 等可能需要读）
- `frontend/dist` 放 code（前端在 code 的 Dockerfile 里多阶段 build）
- 数据库 migration 脚本放 code（随版本走）

### 硬性约束

1. **data-only 镜像用 `busybox:musl`**（~2MB）而非 `scratch` — init 容器需要 `sh + cp`。
2. **data-only 镜像不继承 base** — 否则 `docker save` 会把 base 层打包进 tar，拆分失效。
3. **venv 镜像 builder 阶段的 `WORKDIR` 必须等于主容器运行时挂载路径**（如 `/apps/{project}`） — uv 生成的 `.venv/bin/python` 有绝对路径 shebang，挂错位置直接炸。

---

## Dockerfile 模板

### Dockerfile.base

```dockerfile
FROM python:3.11-slim

# 国内加速（按需）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y \
    nginx \
    mariadb-server mariadb-client \
    libportaudio2 \
    curl vim net-tools iproute2 lsof iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# MariaDB 目录权限
RUN mkdir -p /var/run/mysqld /var/lib/mysql /var/log/mysql && \
    chown -R mysql:mysql /var/run/mysqld /var/lib/mysql /var/log/mysql

# MariaDB 监听端口（按项目定）
RUN printf "[mariadbd]\nskip-networking = off\nport = {DB_PORT}\nbind-address = 0.0.0.0\n" \
    > /etc/mysql/mariadb.conf.d/99-force-tcp.cnf

# uv binary（venv builder 阶段需要）
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# entrypoint 烧进 base
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/apps/{project} \
    PATH="/apps/{project}/.venv/bin:$PATH" \
    TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1 \
    # ...（其他运行时环境变量）

WORKDIR /apps/{project}
EXPOSE {PORT} {DB_PORT} {API_PORT} 5280 5281
ENTRYPOINT ["/entrypoint.sh"]
```

### Dockerfile.venv

**关键点**：`ARG BASE_IMAGE` 让多架构 buildx 能从 registry 拉 base（见下面 push 流程）。

```dockerfile
ARG BASE_IMAGE={project}-base
ARG BASE_TAG=1.0.0
FROM ${BASE_IMAGE}:${BASE_TAG} AS builder
WORKDIR /apps/{project}

# 编译依赖（仅 builder 阶段）
RUN apt-get update && apt-get install -y build-essential portaudio19-dev && \
    rm -rf /var/lib/apt/lists/*

# 动态子包发现（减少加子包时的 Dockerfile 改动）
COPY backend/ /src/
RUN cp /src/pyproject.toml /src/uv.lock . && \
    find /src -maxdepth 3 -name "pyproject.toml" -not -path "/src/pyproject.toml" | \
    while read f; do \
      pkg_dir=$(dirname "$f" | sed 's|^/src/||'); \
      mkdir -p "$pkg_dir/src/sage"; \
      cp "$f" "$pkg_dir/"; \
      touch "$pkg_dir/README.md"; \
      touch "$pkg_dir/src/sage/__init__.py"; \
    done

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# data-only 最终镜像
FROM busybox:musl
COPY --from=builder /apps/{project}/.venv /export/.venv
```

### Dockerfile.models

```dockerfile
FROM busybox:musl
COPY resources/models /export/models
```

### Dockerfile.code

前端在 Stage 1 构建，Stage 2 是 busybox 汇总所有代码资产。

```dockerfile
# Stage 1: 前端构建
FROM node:20-slim AS frontend-builder
WORKDIR /apps/frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn config set registry https://registry.npmmirror.com && \
    yarn install --frozen-lockfile --network-timeout 1000000
COPY frontend/ ./
RUN yarn build

# Stage 2: 汇总到 busybox
FROM busybox:musl
# 后端源码（按子包列）
COPY backend/{subpkg1}/src /export/{subpkg1}/src
COPY backend/{subpkg2}/src /export/{subpkg2}/src
# pyproject（运行时 alembic 等需要）
COPY backend/{subpkg1}/pyproject.toml /export/{subpkg1}/
COPY backend/{subpkg2}/pyproject.toml /export/{subpkg2}/
COPY backend/pyproject.toml backend/uv.lock /export/
# 启动器 + migration + 配置
COPY backend/launcher.py /export/
COPY backend/alembic.ini /export/
COPY backend/migrations  /export/migrations
COPY backend/config      /export/config
# 前端产物
COPY --from=frontend-builder /apps/frontend/dist /export/frontend/dist
# Nginx 配置（烧进 code，entrypoint 启动时复制到 /etc/nginx/）
COPY docker/nginx.conf /export/nginx.conf
```

---

## 运行时组合（Compose）

### `.env.example`

```env
# 4 个镜像独立 bump；典型发版只改 CODE_TAG
{PROJECT_UPPER}_BASE_TAG=1.0.0
{PROJECT_UPPER}_VENV_TAG=1.0.0
{PROJECT_UPPER}_MODELS_TAG=1.0.0
{PROJECT_UPPER}_CODE_TAG=2.1.0
```

### `docker-compose.yml`（本地开发）

```yaml
services:
  # ─── 4 个镜像的构建壳（profile=build，默认不起，方便单独 build）───
  base-build:
    build: { context: .., dockerfile: docker/Dockerfile.base }
    image: {project}-base:${BASE_TAG}
    command: ["true"]
    restart: "no"
    profiles: ["build"]

  venv-build:
    build:
      context: ..
      dockerfile: docker/Dockerfile.venv
      args: { BASE_TAG: "${BASE_TAG}" }
    image: {project}-venv:${VENV_TAG}
    command: ["true"]
    restart: "no"
    profiles: ["build"]

  models-build:
    build: { context: .., dockerfile: docker/Dockerfile.models }
    image: {project}-models:${MODELS_TAG}
    command: ["true"]
    restart: "no"
    profiles: ["build"]

  code-build:
    build: { context: .., dockerfile: docker/Dockerfile.code }
    image: {project}-code:${CODE_TAG}
    command: ["true"]
    restart: "no"
    profiles: ["build"]

  # ─── init 容器 ───
  venv-init:
    image: {project}-venv:${VENV_TAG}
    volumes: [ "venv-data:/target" ]
    environment: [ "TAG=${VENV_TAG}" ]
    command: >
      sh -c '
        if [ "$$(cat /target/.version 2>/dev/null)" = "$$TAG" ]; then
          echo "venv $$TAG already synced, skip";
        else
          rm -rf /target/* /target/.[!.]* 2>/dev/null || true;
          cp -a /export/.venv/. /target/;
          echo "$$TAG" > /target/.version;
        fi
      '
    restart: "no"

  models-init:
    image: {project}-models:${MODELS_TAG}
    volumes: [ "models-data:/target" ]
    environment: [ "TAG=${MODELS_TAG}" ]
    command: >
      sh -c '
        if [ "$$(cat /target/.version 2>/dev/null)" = "$$TAG" ]; then
          echo "models $$TAG already synced, skip";
        else
          rm -rf /target/* /target/.[!.]* 2>/dev/null || true;
          cp -a /export/models/. /target/;
          echo "$$TAG" > /target/.version;
        fi
      '
    restart: "no"

  code-init:
    # 代码每次发版 tag 都变，不走 .version 判断，每次重写
    image: {project}-code:${CODE_TAG}
    volumes: [ "code-data:/target" ]
    command: >
      sh -c '
        rm -rf /target/* /target/.[!.]* 2>/dev/null || true;
        cp -a /export/. /target/;
      '
    restart: "no"

  # ─── 主业务容器 ───
  {project}:
    image: {project}-base:${BASE_TAG}
    container_name: {project}
    restart: always
    ports:
      - "{PORT}:{PORT}"
      - "{API_PORT}:{API_PORT}"
      # ...
    depends_on:
      venv-init:   { condition: service_completed_successfully }
      models-init: { condition: service_completed_successfully }
      code-init:   { condition: service_completed_successfully }
    volumes:
      # ⚠️ 顺序：浅 → 深（Docker 支持嵌套挂载）
      - code-data:/apps/{project}
      - venv-data:/apps/{project}/.venv
      - models-data:/apps/{project}/resources/models
      # 运行时持久化
      - ./resources/mysql/data:/var/lib/mysql
      - ./resources/mysql/logs:/var/log/mysql
      - ./logs:/apps/{project}/logs
    environment:
      # ...（运行时 env）
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{API_PORT}/ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  venv-data:
  models-data:
  code-data:
```

### `docker-compose.prod.yml`

和 dev 相比删除 4 个 `*-build` 服务、去 `ports:` 改 `network_mode: host`、env 换成生产值；**init 容器和主服务结构完全一致**，保证行为对齐。

---

## entrypoint.sh 要点

`nginx.conf` 通过 code volume 挂到 `/apps/{project}/nginx.conf`，不在 nginx 默认读取路径。**启动 nginx 前必须 cp 到默认位置**，否则 nginx 用系统默认配置（监听 80、不知道后端在哪）：

```bash
echo "🌐 Starting Nginx on port {PORT}..."
# 4 镜像拆分后 nginx.conf 随 code 发布，通过 volume 挂到 /apps/{project}/nginx.conf
# 启动前复制到默认路径，确保生效
cp /apps/{project}/nginx.conf /etc/nginx/nginx.conf
nginx
```

---

## 常见坑

1. **venv shebang 路径**：uv 生成的 `.venv/bin/python` 有 `#!/apps/{project}/.venv/bin/python`。Dockerfile.venv 的 builder 阶段必须 `WORKDIR /apps/{project}`，compose 也必须把 volume 挂到这个路径。错一个字符都不行。

2. **nested volume 挂载顺序**：compose 声明顺序决定挂载先后。`code-data:/apps/{project}` 要在 `venv-data:/apps/{project}/.venv` **之前**，否则后者会被前者覆盖。

3. **init 容器每次都写会慢**：首次 30-60s（1.3GB venv 拷到 volume）。加 `.version` 标记可以让 venv/models 的后续重启毫秒级返回。code 不加（tag 每次都变）。

4. **code-init 必须先清空再写**：`rm -rf /target/* /target/.[!.]*` — 否则老代码里被删的 `.py` 文件会残留，导致奇怪的行为。

5. **多架构 venv 推送**：`FROM {base}:${BASE_TAG}` 在多架构 buildx 下，buildx 会为每个目标架构单独拉 base。base 必须先 push 到 registry 且**两架构都推了**。push script 必须 `--build-arg BASE_IMAGE={registry}/{namespace}/{project}-base`，否则 buildx 会尝试找本地镜像（只有当前 host 架构那一个）。

---

## 增量升级的效果

| 场景 | 变动 tar | 传输量 |
|------|---------|-------|
| 只改代码 | `{project}-code.tar` | ~100MB |
| 加 Python 依赖 | `{project}-venv.tar` + code | ~1.4GB |
| 换模型 | `{project}-models.tar` | ~400MB |
| 改系统包 | `{project}-base.tar` + venv（builder 基于 base） | ~1GB |

原单镜像方案每次都是 ~7GB。70x 改善。
