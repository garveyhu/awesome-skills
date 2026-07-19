---
name: docker-best-practices
description: >-
  Use when containerizing or deploying a frontend, backend, or full-stack project
  for local testing, an internal registry, production, or offline delivery.
  Triggers include "docker化", "容器化", "写Dockerfile", "build镜像", "推送镜像",
  "部署到服务器", "docker-compose", Docker images, Compose, multi-stage or
  multi-arch buildx, registry delivery, tar-offline delivery, embedded MariaDB,
  dev/prod container environments, and image build/push/run scripts.
---

# Docker Best Practices

## 核心约定：三区结构

所有 Docker 工程化产物都收拢在项目根 `docker/` 下，分三个职责清晰的子目录：

```
docker/
  README.md                         ← 部署手册（不叫 DEPLOY.md）
  images/                           ← 镜像制作区
    Dockerfile.base / .code / .ui ...
    entrypoint.sh
    nginx.conf
    .env / .env.example             ← 镜像 tag 的唯一来源
  containers/                       ← 容器运行区
    docker-compose.yml              本地开发裸放在 containers/ 根
    data/                           本地开发挂载（脚本自动建）
    <env-name>/                     其他环境（生产 / 区域）
      docker-compose.yml
  scripts/                          ← 脚本区
    build-images.sh   [target ...]
    push-images.sh    [target ...]
    run-local.sh      [target ...]
    stop-local.sh     [-v]
    .registry.env / .registry.env.example
```

**为什么这样分**：

- **images/** = "怎么造镜像"（Dockerfile 和构建期资源）
- **containers/** = "怎么跑容器"（compose 编排 + 运行时挂载）
- **scripts/** = "怎么操作"（build / push / run 工作流）
- 三个区**互不交叉**——改 Dockerfile 不动 compose、改 compose 不动脚本、改脚本不动镜像。

**核心设计点**：

1. **本地开发的 compose 直接放在 `containers/` 根**（不放 `containers/dev/`），因为 dev 是默认场景，少一层目录就少一层心智负担。
2. **生产 / 区域环境放子目录**（`containers/syzh/`、`containers/prod/`），跟 dev 平级共存。
3. **`docker/images/.env` 是镜像 tag 的唯一来源**——build / push / 本地 compose 都从这里读，运维生产环境另写一份 `.env`。
4. **三个脚本统一参数协议**——不传参 = 处理全部镜像，传参 = 只处理指定的子集。

**参考实现**：

- [references/structure.md](references/structure.md) — 三区结构详解 + 单/多镜像选型
- [references/templates.md](references/templates.md) — Dockerfile / compose / nginx / entrypoint 模板
- [references/multi-image.md](references/multi-image.md) — 多镜像拆分（init 容器 + named volume + .version skip）
- [references/scripts.md](references/scripts.md) — 三脚本统一参数协议的实现
- [references/pitfalls.md](references/pitfalls.md) — buildx HTTP registry / nginx.conf / macOS bash 等踩坑记录
- [references/cn-mirrors.md](references/cn-mirrors.md) — 国内镜像源单一来源（apt/apk · npm/yarn · uv/pip · maven · go），所有 Dockerfile 照抄此处

---

## 阶段一：初始化（Init）

### Step 1：自动扫描项目类型

| 检测条件 | 判断结果 |
|---------|--------|
| 同时有 `frontend/` 和 `backend/` | 全栈 |
| 只有 `backend/`（含 `pyproject.toml` 或 `pom.xml`） | 纯后端 |
| 只有 `frontend/`（含 `package.json`） | 纯前端 |

### Step 2：收集必要信息（按顺序逐一询问）

**Q1**：项目名（用于镜像名前缀和 compose project name）

**Q2**：版本号（写入 `.env.example` 的初始值）

**Q3**：对外暴露端口
- 全栈默认：`80`（Nginx 统一入口）
- 纯后端默认：`8000`
- 纯前端默认：`80`

**Q4**（全栈 / 纯后端）：数据库策略
- **A** — SQLite（嵌入，零配置）
- **B** — 嵌入式 MariaDB（`USE_EMBEDDED_DB=true/false` 切换）
- **C** — 纯外部数据库（compose env 配连接）

**Q5**：镜像结构（**默认走多镜像**，单镜像只在以下三个条件全满足时考虑）：
- 项目最终镜像 < 1GB
- 部署只走 registry，不需要 tar 离线
- 团队就 1-2 个人，不在乎工程化复杂度

> 多镜像的层划分**按项目实际**：
> - Java 后端（如 waveflow）：`base / code / ui`
> - Python + ML（如 sage）：`base / venv / models / code`
> - 任意项目：层名按内容定，**`base` 始终是系统运行时**，其他层用 `code / ui / venv / models / deploy / data` 这种语义化名字。

**Q6**（仅多镜像）：部署通道是 registry 还是 tar 离线？
- **Registry**：data-only 镜像可 `FROM scratch`（buildkit 直接 push）
- **Tar + docker load**：data-only 镜像**必须** `FROM busybox:musl`（init 需要 `sh + cp`）

### Step 3：生成 `docker/` 三区目录

```
docker/
├── README.md                        ← 按项目模板生成（见 references/templates.md）
├── images/
│   ├── Dockerfile.base
│   ├── Dockerfile.code              ← 多镜像；单镜像直接叫 Dockerfile
│   ├── Dockerfile.ui                ← 仅多镜像 + 全栈
│   ├── entrypoint.sh
│   ├── nginx.conf                   ← 全栈 / 纯前端
│   ├── .env                         ← 跟随项目复制
│   └── .env.example
├── containers/
│   ├── docker-compose.yml           ← 本地开发（含 build profiles + ports）
│   └── <env>/docker-compose.yml     ← 生产 / 区域（image-only，无 build）
└── scripts/
    ├── build-images.sh
    ├── push-images.sh
    ├── run-local.sh
    ├── stop-local.sh
    ├── .registry.env
    └── .registry.env.example
```

项目根目录同步（**首次创建 docker 项目就把这两个 ignore 写好，避免运行时数据被误 commit 或拖进 build context**，详见 [references/templates.md](references/templates.md)）：

- `.dockerignore` —— 排除 `docker/containers/*/data/`、`packages/`、`**/target/`、凭据 `.env` 等
- `.gitignore` —— 同样排除 `docker/containers/*/data/`、`docker/images/.env`、`docker/scripts/.registry.env`

---

## 阶段二：开发指导（Guide）

### 子节 1：本地开发（一行命令）

```bash
./docker/scripts/run-local.sh           # 全部 rebuild + up
./docker/scripts/run-local.sh code      # 只 rebuild code（base/ui 不动）+ up
./docker/scripts/run-local.sh code ui   # 多个
```

`run-local.sh` 的标准动作：

1. 缺 `.env` 就从 `.env.example` 复制
2. `mkdir -p` 运行时挂载目录
3. 调 `build-images.sh` 透传参数
4. `docker compose down --remove-orphans`（保留 volume）
5. `docker compose up -d --remove-orphans`
6. 等主容器健康（最多 90s）
7. 打印访问入口 banner

> **关键**：`compose down + up` 让 init 容器**重新跑**，结合 dev compose 里去掉 `.version` skip 逻辑（每次全量 cp），代码改动一定生效。生产 compose 保留 `.version` skip，避免每次 restart 重 cp。

### 子节 2：推送到内网仓库

首次配置：

```bash
cp docker/scripts/.registry.env.example docker/scripts/.registry.env
vim docker/scripts/.registry.env   # 填 REGISTRY_URL / USER / PASSWORD / NAMESPACE
```

```bash
./docker/scripts/push-images.sh           # 全部多架构 push
./docker/scripts/push-images.sh code      # 只推 code（最常见）
./docker/scripts/push-images.sh code ui   # 多个
```

**关键设计**：
1. 不自动创建 buildx builder——尊重用户当前激活的（特别是配过 HTTP registry 的）
2. 登录走 `docker login`，凭据放 `.registry.env`（gitignored）
3. 多架构 venv build 必须 `--build-arg BASE_IMAGE={registry}/{ns}/{project}-base`，让 buildx 从 registry 拉对应架构

### 子节 3：生产部署（运维视角）

运维在服务器上维护两个文件，放在同一目录（docker compose 自动加载同级 `.env`）：

```
/apps/{project}/
  docker-compose.yml    ← 取自 docker/containers/<env>/docker-compose.yml
  .env                  ← N 行镜像 tag，每次发版随包提供
```

**Registry 通道**：

```bash
cd /apps/{project}
docker login {registry}
docker compose pull
docker compose up -d
```

**Tar 离线通道**（生产机不能访问 registry）：

中转机（能访问 registry）：拉 → retag 成短名 → save tar  
生产机：load 所有 tar → `docker compose up -d`

详见 [references/structure.md#tar-离线](references/structure.md)。

**升级**（只换 code，最常见）：

```bash
cd /apps/{project}
sed -i 's/^.*_CODE_TAG=.*/{PROJECT_UPPER}_CODE_TAG=2.1.1/' .env
docker compose pull   # 或 docker load -i {project}-code-2.1.1.tar
docker compose up -d
```

`.version` skip 让 base/ui 的 init 跳过；只有 code 重新 cp。

---

## 阶段三：代码审查（Review）

### 三区结构

- [ ] `docker/images/`、`docker/containers/`、`docker/scripts/` 三区齐备
- [ ] 本地开发 compose 在 `containers/docker-compose.yml`，**不**在 `containers/dev/`
- [ ] 生产 / 区域环境在 `containers/<env>/docker-compose.yml`
- [ ] `docker/images/.env` 是 tag 的唯一来源；运维生产环境用自己的 `.env`
- [ ] `docker/README.md` 在顶层（不叫 `DEPLOY.md`）

### 镜像质量

- [ ] 多阶段构建（最终镜像不含编译依赖）
- [ ] 每个 `apt-get install` 后 `rm -rf /var/lib/apt/lists/*`
- [ ] **所有包管理器镜像源照抄 [references/cn-mirrors.md](references/cn-mirrors.md)**（apt/apk · npm/yarn · uv/pip · maven · go 统一配；改镜像只改那一处）
- [ ] **uv 项目装包前配 `ENV UV_DEFAULT_INDEX`**（默认走官方 PyPI，国内极慢——最易漏）
- [ ] uv 项目 `uv sync --frozen --no-install-project --no-dev`
- [ ] `.dockerignore` 排除 `node_modules/`、`.venv/`、`.git/`、`tests/`、`docs/`、`*.log`、`*.tar`
- [ ] `.dockerignore` **必须排除 `docker/containers/*/data/`**（dev 跑时挂载产生的 mariadb / 日志运行时数据，可能数 GB；进 build context 会拖慢 build 且可能被误打进镜像）
- [ ] `.gitignore` **必须排除 `docker/containers/*/data/`、`docker/images/.env`、`docker/scripts/.registry.env`**（运行时数据 + 凭据真值，绝不入 git）

### 多镜像拆分

- [ ] data-only 镜像 `FROM busybox:musl`（不用 `scratch`——init 需要 sh+cp）
- [ ] data-only 镜像**不继承** base（否则 `docker save` 包含 base 层，拆分失效）
- [ ] venv builder 阶段 `WORKDIR` = 运行时挂载路径（venv shebang 是绝对路径）
- [ ] init 容器：稳定层（venv / models）带 `.version` skip；code 直接全量 cp（dev 也是，避免遗漏）
- [ ] **dev compose 的 init 全部去掉 `.version` skip**，每次都重 cp，避免 dev 改了代码但 init 跳过的 bug
- [ ] **生产 compose 的 init 保留 `.version` skip**，避免每次 restart 重 cp 大文件
- [ ] Volume 挂载顺序：浅 → 深（code → `/apps/{project}`，venv → `/apps/{project}/.venv`，models → `/apps/{project}/resources/models`）
- [ ] 主容器 `depends_on` 列出所有 init `condition: service_completed_successfully`

### Compose 设计

- [ ] dev compose 顶层 `name: {project}` 锁定 project name（不依赖 CWD 目录名）
- [ ] dev compose 含 `*-build` 服务 + `profiles: ["build"]`，方便单独 build
- [ ] 生产 compose 无 `build:` 块（image-only）
- [ ] `HEALTHCHECK` 已配置（compose 或 Dockerfile）
- [ ] `data/`（dev 挂载）相对于 compose 文件位置，脚本自动 `mkdir -p`

### 脚本质量

- [ ] 三个脚本都 `set -euo pipefail`
- [ ] 三个脚本统一参数协议：不传参 = 全部，传参 = 子集
- [ ] `ROOT="$(cd "$(dirname "$0")/../.." && pwd)"`（脚本在 `docker/scripts/`，上溯两层到项目根）
- [ ] `build-images.sh`：base skip-if-exists；其他每次重建（dev 场景）
- [ ] `push-images.sh`：登录走 `.registry.env`，不自动创建 buildx builder，多架构 venv 透传 `--build-arg BASE_IMAGE`
- [ ] `run-local.sh`：down → build → up → 等 healthy → banner，参数透传给 build
- [ ] 空数组展开用 `${arr[@]+"${arr[@]}"}` 兼容 macOS bash 3.2

### 安全

- [ ] 默认密码（`DB_ROOT_PASSWORD` 等）通过 compose `environment` 传入，不硬编码 Dockerfile
- [ ] `.registry.env` 在 `.gitignore`
- [ ] README.md 给运维的章节没有 registry IP 硬编码（用 `<harbor:port>` 占位）
- [ ] 生产机器操作步骤里**不出现仓库前缀**（中转机 retag 成短名解决）

### 网络（全栈项目）

- [ ] nginx.conf 含 `proxy_buffering off; proxy_cache off;`（SSE 必需）
- [ ] WebSocket：`proxy_http_version 1.1` + Upgrade / Connection headers
- [ ] 静态资源 `expires 7d`
- [ ] API 超时 `proxy_read_timeout 300s`（AI 长响应）

### 常见坑（详见 [references/pitfalls.md](references/pitfalls.md)）

- [ ] 不在 script 里自动 create buildx builder
- [ ] HTTP registry + buildx docker-container driver 需要 `buildkitd.toml` 标记 insecure
- [ ] 多架构 venv `FROM` 必须能从 registry 拉 base
- [ ] Apple Silicon 交叉构建 amd64 走 QEMU 慢
- [ ] dev 改了代码但 init 跳过 → dev compose 必须去掉 `.version` skip
