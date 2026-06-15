# 三区结构详解

所有 Docker 工程化产物分三个区，对应"造镜像"、"跑容器"、"操作镜像和容器"三件事。本文档解释为什么这样分、每个区放什么、不同项目类型下的具体组合。

## 总体布局

```
{project-root}/
└── docker/
    ├── README.md                   ← 部署手册（命名固定为 README.md，不是 DEPLOY.md）
    ├── images/                     ← 区一：镜像制作
    ├── containers/                 ← 区二：容器运行
    └── scripts/                    ← 区三：脚本（自动化操作）
```

> **`docker/` 是单一入口**：项目里所有 docker 相关产物都在这一个目录下，根目录除了 `.dockerignore` 外不再散放 docker 相关文件。

> **配套两份 ignore**（首次建项目就要写好，模板见 [templates.md](templates.md)）：
>
> | 文件 | 作用 | 必须排除 |
> |------|------|--------|
> | `.gitignore` | 阻止 `git add` 误入库 | `docker/containers/data/`、`docker/containers/*/data/`、`docker/images/.env`、`docker/scripts/.registry.env` |
> | `.dockerignore` | 阻止文件进 build context | 同上四条 + `**/target/`、`packages/`、`**/node_modules/`、`*.log` |
>
> 漏掉 `docker/containers/*/data/` 这条最致命——dev 跑过一次后挂载产生的 mariadb 运行时文件会有几个 GB，`git add -A` 一把全推进去（已踩过 285 文件灾难），`docker build` 也会把它拷给 daemon 拖慢 build。

---

## 区一：images/（镜像制作）

```
docker/images/
├── Dockerfile.base                 ← 系统运行时层（基底）
├── Dockerfile.code                 ← 业务代码层（多镜像时）
├── Dockerfile.ui                   ← 前端层（多镜像 + 全栈）
├── Dockerfile.venv                 ← Python 依赖（仅 Python 项目多镜像）
├── Dockerfile.models               ← 离线模型（仅有模型的项目）
├── entrypoint.sh                   ← 主容器启动脚本（烧入 base）
├── nginx.conf                      ← Nginx 配置（全栈/纯前端）
├── .env                            ← 镜像 tag 的唯一来源（gitignored）
└── .env.example                    ← tag 模板
```

**核心原则**：

1. **本目录只放"构建期"资产**——Dockerfile、build 时被 COPY 进镜像的脚本/配置、镜像 tag。
2. **`.env` 是镜像 tag 的唯一来源**——build / push / 本地 compose 都从这里读。运维生产环境另写一份 `.env`。
3. **多镜像项目按层一个 Dockerfile**——`Dockerfile.{layer}` 命名，`base` 是系统运行时，其他层按内容命名。
4. **单镜像项目就一个 Dockerfile**（不带后缀），其余结构不变。

**`.env` 内容**：

```env
{PROJECT_UPPER}_BASE_TAG=1.0.0
{PROJECT_UPPER}_CODE_TAG=1.0.0
{PROJECT_UPPER}_UI_TAG=1.0.0
# 单镜像就一行 {PROJECT_UPPER}_TAG=1.0.0
```

---

## 区二：containers/（容器运行）

```
docker/containers/
├── docker-compose.yml              ← 本地开发：直接放在 containers/ 根
├── data/                           ← 本地开发挂载（脚本自动建）
│   ├── mysql/{data,logs}
│   └── logs/
├── <env-name>/                     ← 其他环境（生产 / 区域）
│   └── docker-compose.yml          ← image-only，无 build 块
└── <another-env>/
    └── docker-compose.yml
```

**核心原则**：

1. **本地开发 compose 直接裸放在 `containers/` 根**——dev 是默认场景，少一层目录心智负担更小。
2. **生产 / 区域环境放子目录**——`containers/syzh/`、`containers/prod/`、`containers/staging/` 平级共存。
3. **`data/` 相对于 compose 文件位置**——所以本地 dev 的 data 在 `containers/data/`，运维生产的 data 在他们自己的 `/apps/{project}/data/`。
4. **dev 和生产 compose 行为对齐**——init 容器、主容器、volume 声明完全一致；区别只在 `*-build` profile（dev 有，生产无）和环境变量。

### dev compose 的关键差异（vs 生产）

```yaml
# docker/containers/docker-compose.yml
name: {project}                     # ← 锁定 project name，不依赖 CWD 目录名

services:
  # build 壳服务（profiles: build，默认不启动）
  base-build:
    build:
      context: ../..                # ← 上溯到项目根
      dockerfile: docker/images/Dockerfile.base
    image: {project}-base:${{PROJECT_UPPER}_BASE_TAG}
    command: ["true"]
    restart: "no"
    profiles: ["build"]

  # init 容器（dev：每次都全量 cp，不做 .version skip）
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

  # 主容器
  {project}:
    image: {project}-base:${{PROJECT_UPPER}_BASE_TAG}
    volumes:
      - code-data:/apps/{project}
      - ./data/mysql/data:/var/lib/mysql
      # ...
    ports: ["{PORT}:{PORT}"]
    # ...
```

**为什么 dev 不做 `.version` skip**：dev 改完代码 → bump 还是不 bump tag 都是 friction。脚本默认每次重 build code 镜像 + compose down → up，init 容器**必须**全量重 cp 才能把新代码送到 volume。如果保留 `.version` skip，TAG 没变就跳过 cp，旧代码继续跑，bug。

**为什么生产 compose 保留 `.version` skip**：生产升级时 tag 总会 bump，`.version` 不匹配自然触发重 cp。restart 没 bump tag 时跳过，节省时间。

### 生产 compose 的差异

```yaml
# docker/containers/syzh/docker-compose.yml（举例）
name: {project}-syzh

services:
  # 没有 *-build 服务
  
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
        fi
      '
    restart: "no"

  {project}:
    image: {registry}/{ns}/{project}-base:${{PROJECT_UPPER}_BASE_TAG}
    # 业务侧差异（端口、环境变量、kafka 开关等）
```

---

## 区三：scripts/（脚本）

```
docker/scripts/
├── build-images.sh                 ← 本地 build（参数：[base|code|ui ...]）
├── push-images.sh                  ← 多架构 buildx + push（同样参数）
├── run-local.sh                    ← 一键启动（透传参数给 build）
├── stop-local.sh                   ← 停掉本地容器（-v 顺带清 named volume）
├── .registry.env.example           ← 仓库凭据模板
└── .registry.env                   ← 真实凭据（gitignored）
```

**核心原则**：

1. **三脚本统一参数协议**——`./xxx.sh` = 全部，`./xxx.sh code` = 只处理 code，`./xxx.sh code ui` = 多个。
2. **`run-local.sh` 透传参数给 `build-images.sh`**——本质上 run-local = build-images + compose down/up。
3. **脚本路径是 `docker/scripts/`**，不在项目根 `scripts/`。`ROOT="$(cd "$(dirname "$0")/../.." && pwd)"`（上溯两层到项目根）。

**典型调用方式**：

```bash
# 本地开发：改了 java 后端，只重 build code，其他镜像沿用旧的
./docker/scripts/run-local.sh code

# 改了前后端都需要重建
./docker/scripts/run-local.sh code ui

# 全部重建（首次启动 / 系统层升级）
./docker/scripts/run-local.sh

# 推送代码到仓库
./docker/scripts/push-images.sh code
```

详细脚本实现见 [scripts.md](scripts.md)。

---

## 单/多镜像选型

### 默认走多镜像

任何**满足以下任一条件**的项目都建议拆多镜像：

- 单镜像 > 1GB
- 部署需要 tar 离线下发
- 频繁更新代码但依赖/系统层稳定
- 团队 ≥ 3 人 / 跨团队协作

### 单镜像（degenerate case）

只有一个 Dockerfile，结构仍然是三区：

```
docker/
├── README.md
├── images/
│   ├── Dockerfile               ← 一个 Dockerfile
│   ├── entrypoint.sh
│   └── .env / .env.example      ← 只有一个 TAG
├── containers/
│   ├── docker-compose.yml       ← 没有 build 壳服务，没有 init 容器
│   └── <env>/docker-compose.yml
└── scripts/
    ├── build-images.sh          ← 不接受参数（就一个镜像）
    ├── push-images.sh           ← 同上
    ├── run-local.sh             ← 同上
    └── stop-local.sh            ← 不接受参数
```

单镜像情况下脚本不需要 target 参数（永远是那一个）。

### 多镜像层划分举例

| 项目类型 | 典型层划分 |
|---------|----------|
| Java + 前端（waveflow） | `base + code + ui` |
| Python + ML + 前端（sage） | `base + venv + models + code` |
| 纯 Python 后端 | `base + venv + code`（如果 venv 大） |
| 纯前端 | 通常单镜像（dist + nginx 都很小） |
| 纯 Java 后端 | `base + code`（jar 包跟代码一起） |

层名按内容定，`base` 始终是系统运行时层。

---

## Tar 离线分发的中转机模式

生产机不能访问 registry 时的标准操作。

### 中转机（能访问 registry）

```bash
HARBOR_HOST="<harbor:port>"
HARBOR_NAMESPACE="<namespace>"
echo '<password>' | docker login -u <user> --password-stdin "http://${HARBOR_HOST}"

source .env
PLATFORM=linux/amd64

# 拉镜像 → retag 成短名 → save 短名
for spec in \
    "{project}-base:${{PROJECT_UPPER}_BASE_TAG}" \
    "{project}-code:${{PROJECT_UPPER}_CODE_TAG}" \
    "{project}-ui:${{PROJECT_UPPER}_UI_TAG}"; do
    img="${spec%:*}"; tag="${spec#*:}"
    full="${HARBOR_HOST}/${HARBOR_NAMESPACE}/${img}:${tag}"
    docker pull --platform "$PLATFORM" "$full"
    docker tag "$full" "${img}:${tag}"           # ← 关键：retag 成短名
    docker save "${img}:${tag}" -o "${img}-${tag}.tar"
done
```

**关键点**：tar 里只装短名（`{project}-code:1.0.0`），不装 `{registry}/{ns}/...` 全名，这样：
- 生产机器 `docker load` 后直接 `docker compose up -d` 就能识别
- 生产机操作手册里看不到 registry 地址（运维更干净）

### 生产机器（不能访问 registry）

```bash
sudo mkdir -p /apps/{project}
cd /apps/{project}

# 收到 docker-compose.yml + .env + *.tar 文件
# 放到 /apps/{project}/ 下

# load 全部 tar
for f in *.tar; do
    docker load -i "$f"
done

# 启动
docker compose up -d
docker compose logs -f {project}

# 验证
curl http://localhost:{API_PORT}/ping

# 清 tar
rm *.tar
```

**增量升级**：只处理变动的镜像对应的 tar（通常就 `{project}-code-{newtag}.tar`），其他 init 容器靠 `.version` skip 跳过。

---

## 常见结构问题答疑

**Q：为什么 dev compose 直接放在 `containers/`？还是放在 `containers/dev/` 一致？**

A：默认场景就该最短路径。dev 是 99% 时间用的，应该最方便。生产环境（syzh、prod 等）用 `containers/<name>/` 子目录，跟 dev 平级共存。如果项目以后有了 staging / preview 等多个开发环境，再把 dev 收进 `containers/dev/`。

**Q：`.env` 在 images/ 还是 containers/？**

A：在 `docker/images/.env`，因为它语义上属于"镜像版本"。脚本和 compose 通过 `--env-file docker/images/.env` 引用。这样 containers/ 下不会出现真实的 `.env`（运维到生产环境时另写一份 `.env` 跟 compose 文件同级）。

**Q：能不能让 dev compose 自动加载 `.env` 不传 `--env-file`？**

A：能，但会引入 `containers/.env`（或软链）。当前的 `--env-file` 显式约定避免运维和 dev 混用同一个 `.env`，更清晰。`run-local.sh` 已经封装好了，开发者不会感知这个 flag。

**Q：脚本支持只 up 不 build 吗？**

A：直接 `docker compose -f docker/containers/docker-compose.yml up -d` 就行（带 `--env-file`）。`run-local.sh` 是"build + restart"的封装，纯重启用 docker compose 原命令。
