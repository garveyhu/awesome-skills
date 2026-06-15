# 多镜像拆分方案

适用于：**默认情况**——任何不是"genuinely tiny"的项目。把单一大镜像拆成多层互不继承的镜像，运行时靠 compose 的 init 容器把 data-only 镜像内容拷到 named volume，主容器挂载这些 volume 启动。

## 架构思想

```
┌──────────────────────────────────────────┐
│ {project}-base (主容器基底)              │
│   系统包 + 配置 + entrypoint.sh + (uv)   │
│   ── 极少更新（系统包升级时） ──         │
└──────────────────────────────────────────┘
            ▲
            │ image 引用（不继承）
            │
┌──────────────────────────────────────────┐
│ {project}-code / -ui / -venv / -models   │
│   busybox:musl + /export/<...>           │
│   ── 频繁更新（每次发版） ──             │
└──────────────────────────────────────────┘
            │
            │ init 容器 cp
            ▼
┌──────────────────────────────────────────┐
│ Named Volumes                            │
│   code-data / venv-data / ui-data / ...  │
└──────────────────────────────────────────┘
            │
            │ volume mount
            ▼
┌──────────────────────────────────────────┐
│ {project} 主容器（基于 base）            │
│   挂载所有 volume + 启动业务进程         │
└──────────────────────────────────────────┘
```

效果：代码变更只传 ~100MB 的 `code` tar，依赖/系统层不动。

---

## 镜像职责边界

按层语义命名，不是数字编号。常见层：

| 层 | 基底 | 内容 | 更新频率 | 典型大小 |
|----|------|------|---------|---------|
| `base` | `python:3.11-slim` / `eclipse-temurin:8-jdk` 等 | 系统包（nginx、mariadb、libs）+ 配置 + `entrypoint.sh` | 极少 | 800MB-1.5GB |
| `venv` | `busybox:musl` | `/export/.venv`（uv sync / pip install 产物） | 少（lock 变化） | ~1-2GB |
| `code` | `busybox:musl` | `/export/`：源码 + pyproject + migrations + 配置 | 每次发版 | ~50-200MB |
| `ui` | `busybox:musl` | `/export/`：前端 dist + nginx.conf | 每次前端发版 | ~50MB |
| `models` | `busybox:musl` | `/export/models`（离线模型） | 几乎不 | 400MB-数 GB |

> 不是所有项目都需要全部层。waveflow（Java + 前端）= `base + code + ui`；sage（Python + ML + 前端）= `base + venv + models + code`。**`base` 总是必须的，其他按需**。

### 边界判断原则

- **`entrypoint.sh` 放 base**——启动流程稳定，不随业务变
- **`nginx.conf` 跟着前端走**——多镜像项目里通常和前端一起放在 `ui` 层
- **migration 脚本放 code**——随代码版本走
- **配置文件放 code**——随代码版本走
- **依赖包放 venv（Python）/ 放 code（Java jar）**——Python 的 venv 大且独立，单独成层；Java 的 jar 通常和代码一起打到 code 层

### 硬性约束

1. **data-only 镜像用 `busybox:musl`**（~2MB）而非 `scratch`——init 容器需要 `sh + cp`
2. **data-only 镜像不继承 base**——否则 `docker save` 把 base 层打进 tar，拆分失效
3. **venv 镜像 builder 阶段的 `WORKDIR` 必须等于主容器运行时挂载路径**（如 `/apps/{project}`）——uv 生成的 `.venv/bin/python` 有绝对路径 shebang，挂错位置直接炸

---

## Dockerfile 模板

文件全部放 `docker/images/`。

### `docker/images/Dockerfile.base`

```dockerfile
FROM python:3.11-slim   # 或 eclipse-temurin:8-jdk 等

# 国内加速（按需）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y \
    nginx \
    mariadb-server mariadb-client \
    curl vim net-tools && \
    rm -rf /var/lib/apt/lists/*

# MariaDB 目录权限
RUN mkdir -p /var/run/mysqld /var/lib/mysql /var/log/mysql && \
    chown -R mysql:mysql /var/run/mysqld /var/lib/mysql /var/log/mysql

# MariaDB 监听端口（按项目定）
RUN printf "[mariadbd]\nport = {DB_PORT}\nbind-address = 0.0.0.0\n" \
    > /etc/mysql/mariadb.conf.d/99-port.cnf

# uv（仅 Python 项目，venv builder 阶段需要）——pip 从阿里云装，别用 ghcr（国内多架构不可达，见 cn-mirrors.md）
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ uv

# entrypoint 烧进 base
COPY docker/images/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV TZ=Asia/Shanghai \
    PYTHONUNBUFFERED=1 \
    PATH="/apps/{project}/.venv/bin:$PATH"

WORKDIR /apps/{project}
EXPOSE {PORT} {DB_PORT} {API_PORT}
ENTRYPOINT ["/entrypoint.sh"]
```

### `docker/images/Dockerfile.venv`（Python 项目）

```dockerfile
ARG BASE_IMAGE={project}-base
ARG BASE_TAG=1.0.0
FROM ${BASE_IMAGE}:${BASE_TAG} AS builder
WORKDIR /apps/{project}

RUN apt-get update && apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY backend/ /src/
RUN cp /src/pyproject.toml /src/uv.lock . && \
    find /src -maxdepth 3 -name "pyproject.toml" -not -path "/src/pyproject.toml" | \
    while read f; do \
      pkg_dir=$(dirname "$f" | sed 's|^/src/||'); \
      mkdir -p "$pkg_dir/src/{project}"; \
      cp "$f" "$pkg_dir/"; \
      touch "$pkg_dir/README.md" "$pkg_dir/src/{project}/__init__.py"; \
    done

# 国内 PyPI 镜像（见 references/cn-mirrors.md）——uv 默认走官方源，国内极慢
ENV UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

FROM busybox:musl
COPY --from=builder /apps/{project}/.venv /export/.venv
```

### `docker/images/Dockerfile.code`（Java + Maven 例子）

```dockerfile
# Stage 1: maven build → 解开 tar → 跑 install.sh 展开 modules/
FROM maven:3.9.6-eclipse-temurin-8 AS builder
WORKDIR /build

COPY pom.xml ./
COPY {module1}/ {module1}/
COPY {module2}/ {module2}/
COPY {module-assembly}/ {module-assembly}/
COPY bin/ bin/

RUN --mount=type=cache,target=/root/.m2 \
    mvn clean install package -DskipTests

RUN mkdir -p /output && \
    tar -zxf build/{project}-parent-*.tar.gz -C /output && \
    mv /output/{project}-parent-* /output/{project} && \
    cd /output/{project} && \
    ./bin/install.sh --force && \
    rm -rf packages/

# Stage 2: 数据镜像
FROM busybox:musl
COPY --from=builder /output/{project} /export
```

### `docker/images/Dockerfile.code`（Python + 前端 例子）

前端在同一个 Dockerfile 的另一个 stage 里 build。如果前端是独立组，建议拆 `Dockerfile.ui`。

```dockerfile
# Stage 1: 前端构建
FROM node:20-slim AS frontend-builder
WORKDIR /apps/frontend
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn config set registry https://registry.npmmirror.com && \
    yarn install --frozen-lockfile --network-timeout 1000000
COPY frontend/ ./
RUN yarn build

# Stage 2: 汇总
FROM busybox:musl
COPY backend/{subpkg1}/src /export/{subpkg1}/src
COPY backend/{subpkg2}/src /export/{subpkg2}/src
COPY backend/{subpkg1}/pyproject.toml /export/{subpkg1}/
COPY backend/{subpkg2}/pyproject.toml /export/{subpkg2}/
COPY backend/pyproject.toml backend/uv.lock /export/
COPY backend/launcher.py /export/
COPY backend/alembic.ini /export/
COPY backend/migrations /export/migrations
COPY backend/config /export/config
COPY --from=frontend-builder /apps/frontend/dist /export/frontend/dist
COPY docker/images/nginx.conf /export/nginx.conf
```

### `docker/images/Dockerfile.ui`（独立前端层）

```dockerfile
# Stage 1: 构建
FROM node:20-slim AS builder
WORKDIR /build
RUN git clone -b main https://github.com/{org}/{project}-ui.git . && \
    yarn config set registry https://registry.npmmirror.com && \
    yarn install --frozen-lockfile && \
    yarn build

# Stage 2: 汇总到 busybox
FROM busybox:musl
COPY --from=builder /build/dist /export/dist
COPY docker/images/nginx.conf /export/nginx.conf
```

### `docker/images/Dockerfile.models`

```dockerfile
FROM busybox:musl
COPY resources/models /export/models
```

---

## 运行时编排（Compose）

### `docker/images/.env.example`

```env
# 各层独立 bump；典型发版只改 CODE_TAG
{PROJECT_UPPER}_BASE_TAG=1.0.0
{PROJECT_UPPER}_VENV_TAG=1.0.0       # 仅 Python 项目
{PROJECT_UPPER}_MODELS_TAG=1.0.0     # 仅有模型的项目
{PROJECT_UPPER}_CODE_TAG=1.0.0
{PROJECT_UPPER}_UI_TAG=1.0.0          # 仅独立前端层
```

### `docker/containers/docker-compose.yml`（本地开发）

```yaml
# 本地开发：内置 mariadb，code/ui init 每次都全量 cp（dev 场景）
name: {project}

services:
  # ─── 4 个镜像的构建壳（profiles: build，默认不起）───
  base-build:
    build:
      context: ../..
      dockerfile: docker/images/Dockerfile.base
    image: {project}-base:${{PROJECT_UPPER}_BASE_TAG}
    command: ["true"]
    restart: "no"
    profiles: ["build"]

  code-build:
    build:
      context: ../..
      dockerfile: docker/images/Dockerfile.code
    image: {project}-code:${{PROJECT_UPPER}_CODE_TAG}
    command: ["true"]
    restart: "no"
    profiles: ["build"]

  ui-build:
    build:
      context: ../..
      dockerfile: docker/images/Dockerfile.ui
    image: {project}-ui:${{PROJECT_UPPER}_UI_TAG}
    command: ["true"]
    restart: "no"
    profiles: ["build"]

  # ─── init 容器（dev：每次全量 cp，不做 .version skip）───
  code-init:
    image: {project}-code:${{PROJECT_UPPER}_CODE_TAG}
    volumes: [code-data:/target]
    command: >
      sh -c '
        rm -rf /target/* /target/.[!.]* 2>/dev/null || true;
        cp -a /export/. /target/;
        echo "code synced";
      '
    restart: "no"

  ui-init:
    image: {project}-ui:${{PROJECT_UPPER}_UI_TAG}
    volumes: [ui-data:/target]
    command: >
      sh -c '
        rm -rf /target/* /target/.[!.]* 2>/dev/null || true;
        cp -a /export/. /target/;
        echo "ui synced";
      '
    restart: "no"

  # ─── 主业务容器 ───
  {project}:
    image: {project}-base:${{PROJECT_UPPER}_BASE_TAG}
    container_name: {project}
    restart: always
    ports:
      - "{PORT}:{PORT}"
      - "{DB_PORT}:{DB_PORT}"
      - "{API_PORT}:{API_PORT}"
    depends_on:
      code-init: { condition: service_completed_successfully }
      ui-init:   { condition: service_completed_successfully }
    volumes:
      # ⚠️ 顺序：浅 → 深（Docker 支持嵌套挂载）
      - code-data:/apps/{project}
      - ui-data:/apps/{project}-ui
      - ./data/mysql/data:/var/lib/mysql
      - ./data/mysql/logs:/var/log/mysql
      - ./data/logs:/apps/{project}/logs
    environment:
      - TZ=Asia/Shanghai
      - USE_EMBEDDED_DB=true
      - DB_NAME={project}
      - DB_PASS=changeme
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:{API_PORT}/ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

volumes:
  code-data:
  ui-data:
```

### `docker/containers/<env>/docker-compose.yml`（生产 / 区域）

跟 dev 比四点差异：

1. **删除 `*-build` 服务**（生产不在本机 build）
2. **image 名带 registry 前缀**（`{registry}/{ns}/{project}-base:...`）
3. **init 容器加回 `.version` skip 逻辑**（生产升级 bump tag 才触发重 cp）
4. **环境变量替换为生产值**（kafka 开关、端口、密码等）

```yaml
name: {project}-{env}

services:
  code-init:
    image: {registry}/{ns}/{project}-code:${{PROJECT_UPPER}_CODE_TAG}
    volumes: [code-data:/target]
    environment: [TAG=${{PROJECT_UPPER}_CODE_TAG}]
    command: >
      sh -c '
        if [ "$$(cat /target/.version 2>/dev/null)" = "$$TAG" ]; then
          echo "code $$TAG already synced, skip";
        else
          rm -rf /target/* /target/.[!.]* 2>/dev/null || true;
          cp -a /export/. /target/;
          echo "$$TAG" > /target/.version;
          echo "code $$TAG synced";
        fi
      '
    restart: "no"

  # ui-init 类似

  {project}:
    image: {registry}/{ns}/{project}-base:${{PROJECT_UPPER}_BASE_TAG}
    container_name: {project}-{env}
    # ...生产侧业务变量
```

---

## entrypoint.sh 要点

`nginx.conf` 通过 ui-data volume 挂到 `/apps/{project}-ui/nginx.conf`，不在 nginx 默认读取路径。**启动 nginx 前必须 cp 到默认位置**：

```bash
echo "🌐 Starting Nginx on port {PORT}..."
cp /apps/{project}-ui/nginx.conf /etc/nginx/nginx.conf
nginx
```

否则 nginx 会用系统默认配置（监听 80、不知道后端在哪）。

---

## 常见坑

1. **venv shebang 路径**：uv 生成的 `.venv/bin/python` 有 `#!/apps/{project}/.venv/bin/python`。Dockerfile.venv 的 builder 阶段必须 `WORKDIR /apps/{project}`，compose 也必须把 volume 挂到这个路径。错一个字符都不行。

2. **nested volume 挂载顺序**：compose 声明顺序决定挂载先后。`code-data:/apps/{project}` 要在 `venv-data:/apps/{project}/.venv` **之前**，否则后者会被前者覆盖。

3. **init 容器每次都写会慢**：首次 30-60s（1.3GB venv 拷到 volume）。生产保留 `.version` 标记可以让 venv/models 的后续重启毫秒级返回。**dev 场景不要做这个优化**——否则改了代码但 init 跳过的 bug 极易出现。

4. **code-init 必须先清空再写**：`rm -rf /target/* /target/.[!.]*`——否则老代码里被删的文件会残留，导致奇怪行为。

5. **多架构 venv 推送**：`FROM {base}:${BASE_TAG}` 在多架构 buildx 下，buildx 为每个目标架构单独拉 base。base 必须先 push 到 registry 且**两架构都推了**。push script 必须 `--build-arg BASE_IMAGE={registry}/{ns}/{project}-base`，否则 buildx 会尝试找本地镜像（只有当前 host 架构那一个）。

6. **dev compose 漏掉去 `.version` skip**：本地修改 java 代码后 run-local.sh 已经重 build 了 code 镜像（同 tag），但 init 容器看到 `.version` 匹配跳过 cp，volume 里还是旧代码。表现：改了代码但页面没反应。**必检项**。

---

## 增量升级的效果

| 场景 | 变动 tar | 传输量 |
|------|---------|-------|
| 只改代码 | `{project}-code.tar` | ~100MB |
| 只改前端 | `{project}-ui.tar` | ~50MB |
| 加 Python 依赖 | `{project}-venv.tar` + code | ~1.4GB |
| 换模型 | `{project}-models.tar` | ~400MB |
| 改系统包 | `{project}-base.tar` + venv（builder 基于 base） | ~1GB |

原单镜像方案每次都是 ~7GB。70x 改善。
