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
  Also covers multi-image (4-image) split for heavy projects where code updates
  need small transfer size (especially tar-based offline deployment), and a
  reusable script trio (build-images.sh / push-images.sh / run-local.sh) to
  drive local build, multi-arch push, and one-shot local startup.
  Outputs: docker/ directory with Dockerfile(s), entrypoint.sh, nginx.conf,
  docker-compose.yml, docker-compose.prod.yml, .env.example, DEPLOY.md, and
  .dockerignore; plus scripts/ directory with the three helpers.
---

# Docker Best Practices

## 概述

从成品项目到容器化的全流程封装：分析项目结构、决定单/多镜像、生成 `docker/` 和 `scripts/`、本地测试、推送仓库、生产部署。

**支持项目类型**：
- **全栈**：React 前端 + FastAPI 后端（含 Nginx 反向代理）
- **纯后端**：FastAPI only
- **纯前端**：React 静态站（Nginx serve）

**支持镜像结构**：
- **单镜像**（简单、registry 场景下最省事）
- **多镜像拆分（4 镜像）**（tar 离线分发 / 重型项目 / 模型隔离需求）

**参考实现**：
- [references/templates.md](references/templates.md)：单镜像 + compose + nginx + entrypoint 模板
- [references/multi-image.md](references/multi-image.md)：4 镜像拆分的 Dockerfile / compose / 运行时组合
- [references/scripts.md](references/scripts.md)：`build-images.sh` / `push-images.sh` / `run-local.sh` 脚本模板
- [references/pitfalls.md](references/pitfalls.md)：常见坑 + 解决方法（buildx HTTP registry、nginx.conf、macOS bash 空数组等）

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

**Q1**：镜像名称？（格式 `{namespace}/{project}`，如 `ai/sage`、`complex/onesub`）

**Q2**：版本号？（如 `1.0.0`）

**Q3**：对外暴露端口？
- 全栈默认：`80`（Nginx 统一入口）
- 纯后端默认：`8000`
- 纯前端默认：`80`

**Q4**（全栈 / 纯后端）：数据库策略？
- **A** — SQLite（嵌入，零配置，适合轻量项目）
- **B** — 嵌入式 MariaDB（支持 `USE_EMBEDDED_DB=true/false` 一键切换外部 MySQL，适合中大型项目）
- **C** — 纯外部数据库（容器不内置 DB，通过 compose env 配置连接）

**Q5**：镜像结构 — **单镜像 vs 多镜像拆分**？

> **决策框架**：

| 场景 | 选单镜像 | 选多镜像拆分 |
|------|---------|------------|
| 部署走 **registry push/pull** | ✅ layer 去重自动起作用 | 收益有限，不值得增加复杂度 |
| 部署走 **tar 离线下发** | ❌ 改一行代码也要传整个 tar | ✅ 只传变动的那个 tar |
| 单镜像大小 **< 2GB** | ✅ | ❌ 拆分回报低 |
| 单镜像大小 **> 3GB** 且更新频繁 | ❌ 迭代低效 | ✅ 80% 以上是稳定层（deps/模型），拆出来一次性传 |
| 有**离线 ML 模型**不随代码更新 | 勉强 | ✅ 模型独立镜像，几乎不再更新 |

**拆分阈值启发**：观察项目哪些层"很少变但很大"。典型 Python + ML 项目：venv ~1-2GB、模型 ~400MB-数 GB、系统包 ~500MB、代码 ~50-100MB。代码占比 <5% 但却是每次发版的唯一变化 → 强烈建议拆分。

拆分则走 [references/multi-image.md](references/multi-image.md) 的 4 镜像方案：`{project}-base` + `{project}-venv` + `{project}-data` + `{project}-code`。

**Q6**（仅多镜像）：**部署通道是 registry 还是 tar**？
- 直接影响 data-only 镜像的基底选择：
  - **Registry push**：data-only 镜像可以 `FROM scratch`（buildkit 能直接 push）
  - **Tar + docker load**：data-only 镜像**必须** `FROM busybox:musl`（init 容器需要 `sh + cp` 把数据拷到 volume）

### Step 3：生成 `docker/` 和 `scripts/` 目录

**单镜像模式**：

```
docker/
├── Dockerfile                  ← 多阶段构建
├── entrypoint.sh               ← 启动脚本（全栈 + 纯后端）
├── nginx.conf                  ← 反向代理（全栈 + 纯前端）
├── docker-compose.yml          ← 本地测试（build-based）
├── docker-compose.prod.yml     ← 生产部署（image-based）
└── DEPLOY.md                   ← 部署流程
```

**多镜像模式**（按 [references/multi-image.md](references/multi-image.md) 生成）：

```
docker/
├── Dockerfile.base             ← 系统运行时层
├── Dockerfile.venv             ← Python 依赖（data-only）
├── Dockerfile.models           ← 离线模型（data-only）   ← 仅当有离线数据
├── Dockerfile.code             ← 业务代码 + 前端 dist（data-only）
├── entrypoint.sh               ← 烧入 base
├── nginx.conf                  ← 烧入 code（通过 code volume 暴露，entrypoint 复制到 /etc/nginx/）
├── docker-compose.yml          ← 本地：build profiles + init + sage
├── docker-compose.prod.yml     ← 生产：image + init + sage（host 网络）
├── .env.example                ← 4 个镜像独立 tag
└── DEPLOY.md                   ← 分层构建 + 多架构推送 + tar 离线部署 + 回滚
```

**两种模式通用的 `scripts/` 工作流脚本**（详见 [references/scripts.md](references/scripts.md)）：

```
scripts/
├── build-images.sh             ← 本地 build（多镜像时 skip 已存在 tag）
├── push-images.sh              ← 多架构 buildx + push 到仓库
├── run-local.sh                ← 一键：init + build + up + 等 healthy + 打印提示
└── .registry.env.example       ← 仓库凭据模板（真实值在 .registry.env，gitignored）
```

项目根目录同步更新：
- `.dockerignore` ← 最小化镜像体积
- `.gitignore` ← 加 `scripts/.registry.env`、`dist/`（tar 输出）、`docker/resources/`、`docker/logs/`

---

## 阶段二：开发指导（Guide）

### 子节 1：本地测试

**推荐**：走 `./scripts/run-local.sh` 一键启动。手动走：

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
# 单镜像
cd docker
docker compose build && docker compose up -d --force-recreate

# 多镜像（走脚本检查 skip-if-exists）
./scripts/build-images.sh
cd docker && docker compose up -d
```

**Step 3 — 验证运行**

```bash
docker compose logs -f                       # 实时日志
docker ps                                    # 确认 Up (healthy)
curl http://localhost:{PORT}/ping            # 验证健康端点
```

**Step 4 — 停止**

```bash
docker compose down        # 停止，保留 volume
docker compose down -v     # 停止并清除 volume（重置 venv/models/code data）
```

---

### 子节 2：推送镜像

**推荐走脚本**：`./scripts/push-images.sh`（详见 [references/scripts.md](references/scripts.md)）。

**关键原则**：
1. **不要自动创建 buildx builder**。很多用户的 Docker Desktop / 工作环境已经配好了支持 HTTP registry 的 default builder。尊重 `docker buildx inspect` 当前激活的那个。
2. **HTTP registry 的 buildx 配置**是全局的（操作系统层的 buildx config），不在 script 里动手脚。如果用户报 `http: server gave HTTP response to HTTPS client`，指示他们配 buildx builder 的 `buildkitd.toml`（见 pitfalls）。
3. **登录走 `docker login`**，不要在 script 里写死账号密码。凭据放 `scripts/.registry.env`（gitignored）。

**单镜像推送**：

```bash
# 登录
docker login {registry}

# 多架构 push
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t {registry}/{namespace}/{project}:{version} \
  -f docker/Dockerfile \
  --push .
```

**多镜像推送**：走 `./scripts/push-images.sh`（4 个镜像按顺序 base → venv → models → code）。

> 多架构 venv build 的 `FROM {base}:${BASE_TAG}` 必须在仓库里能拉到目标架构 → Dockerfile.venv 用 `ARG BASE_IMAGE=sage-base`，push script 传 `--build-arg BASE_IMAGE={registry}/{namespace}/{project}-base`，让 builder 去仓库拉。详见 [references/multi-image.md](references/multi-image.md#dockerfilevenv)。

**架构选择**：

| 目标 | 推荐 |
|------|------|
| 纯 x86_64 服务器 | `linux/amd64` |
| 混合 / ARM 环境 | `linux/amd64,linux/arm64` |
| Apple Silicon 本地 + x86 生产 | 必须 `linux/amd64`（交叉构建走 QEMU，venv 构建可能慢 2-5x） |

---

### 子节 3：生产环境部署

**两条路线，按 Q6 决定**：

#### A. Registry 通道（`docker pull` + `docker compose up`）

```bash
cd /apps/{project}
docker login {registry}                                    # 私有仓库
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --force-recreate
```

#### B. Tar 离线下发（生产机器无仓库访问）

> 运维视角：生产机器只看到 `.env` + `docker-compose.yml` + `*.tar`，不知道 Harbor 存在。

**中转机**（有仓库访问的一台 Docker 机）：拉 → retag 成短名 → save tar：

```bash
HARBOR_HOST="<harbor:port>"
HARBOR_NAMESPACE="<namespace>"
docker login -u <user> --password-stdin "http://${HARBOR_HOST}" <<< '<password>'

source .env
PLATFORM=linux/amd64
for spec in "{project}-base:${BASE_TAG}" "{project}-venv:${VENV_TAG}" \
            "{project}-models:${MODELS_TAG}" "{project}-code:${CODE_TAG}"; do
    img="${spec%:*}"; tag="${spec#*:}"
    full="${HARBOR_HOST}/${HARBOR_NAMESPACE}/${img}:${tag}"
    docker pull --platform "$PLATFORM" "$full"
    docker tag "$full" "${img}:${tag}"      # ← 关键：中转机就 retag，tar 里是短名
    docker save "${img}:${tag}" -o "${img}-${tag}.tar"
done
```

**生产机器**：load + compose up（看不到 Harbor 前缀）：

```bash
cd /apps/{project}
for f in *.tar; do docker load -i "$f"; done
docker compose up -d
curl http://localhost:{API_PORT}/ping
rm *.tar
```

**增量升级**：只处理变动的 tag 对应的那个 tar。其他镜像的 init 容器会按 `.version` 标记自动跳过重复同步（见 [references/multi-image.md](references/multi-image.md#init-容器)）。

---

## 阶段三：代码审查（Review）

### 镜像质量

- [ ] 多阶段构建（最终镜像不含 `build-essential` 等编译依赖）
- [ ] 每个 `apt-get install` 后执行 `rm -rf /var/lib/apt/lists/*`
- [ ] `uv sync` 使用 `--frozen --no-install-project --no-dev`
- [ ] `.dockerignore` 排除：`node_modules/`、`.venv/`、`.git/`、`tests/`、`docs/`、`*.log`、`*.tar`

### 多镜像拆分专属

- [ ] data-only 镜像用 `FROM busybox:musl`（不用 `scratch` — init 需要 sh+cp）
- [ ] data-only 镜像**不继承** base（否则 `docker save` 会包含 base 层，拆分失效）
- [ ] `Dockerfile.venv` 的 builder 阶段 `WORKDIR /apps/{project}`（保证 venv shebang 路径对）
- [ ] 运行时 volume 必须挂到和构建时 `WORKDIR` 同一路径（`/apps/{project}/.venv`）
- [ ] init 容器：venv/models 带 `.version` 跳过；code 每次重写
- [ ] Compose volume 挂载顺序：浅 → 深（code → `/apps/{project}`，venv → `/apps/{project}/.venv`，models → `/apps/{project}/resources/models`）
- [ ] `nginx.conf` 如果在 code 镜像，entrypoint.sh 启动 nginx 前要 `cp /apps/{project}/nginx.conf /etc/nginx/nginx.conf`

### 安全

- [ ] 默认密码（`DB_ROOT_PASSWORD` 等）通过 compose `environment` 传入，不硬编码 Dockerfile
- [ ] 生产 `docker-compose.prod.yml` 无 `build:` 块（只引用镜像）
- [ ] `scripts/.registry.env` 在 `.gitignore`
- [ ] DEPLOY.md 给运维的章节**没有 registry IP 硬编码**（用 `<harbor:port>` 占位）
- [ ] 生产机器的操作步骤里**不出现仓库前缀**（通过在中转机 retag 成短名解决）

### 可维护性

- [ ] `docker/DEPLOY.md` 存在，包含完整目录创建 + 启动命令
- [ ] `docker-compose.yml`（build-based）和 `docker-compose.prod.yml`（image-based / host 网络）已分离
- [ ] `HEALTHCHECK` 已配置
- [ ] 多镜像方案：`.env.example` 列出 4 个独立 tag；DEPLOY.md 的"增量升级"章节讲清楚只改对应 tag

### 网络（全栈项目）

- [ ] nginx.conf 含 `proxy_buffering off; proxy_cache off;`（SSE 流式响应必需）
- [ ] WebSocket 支持：`proxy_http_version 1.1` + `Upgrade` / `Connection` headers
- [ ] 静态资源设置 `expires 7d` 缓存头
- [ ] API 超时 `proxy_read_timeout 300s`（AI 长时响应场景）

### 脚本质量

- [ ] `set -euo pipefail` 全部脚本都有
- [ ] 空数组展开用 `${arr[@]+"${arr[@]}"}` 兼容 macOS bash 3.2
- [ ] push-images.sh 不动 buildx builder，用用户当前激活的那个
- [ ] build-images.sh 对稳定层（base/venv/models）skip-if-tag-exists；代码层每次重建
- [ ] run-local.sh 在 compose up 后等容器 `healthy`（带超时），然后打印访问地址

### 常见坑（见 [references/pitfalls.md](references/pitfalls.md)）

- [ ] 不要在 script 里自动 create buildx builder（会覆盖用户已有配置）
- [ ] HTTP registry + buildx docker-container driver 需要 `buildkitd.toml` 标记 insecure（用户配一次，不走 script）
- [ ] 多架构 venv `FROM` 必须能从 registry 拉 base（`ARG BASE_IMAGE` + build-arg）
- [ ] Apple Silicon 交叉构建 amd64 走 QEMU，慢，心里有数
