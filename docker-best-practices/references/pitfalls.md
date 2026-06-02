# Docker 常见坑 + 解决方法

实战中踩过的，记录下来下次别再踩。

---

## 1. buildx push 到 HTTP registry 报 "http: server gave HTTP response to HTTPS client"

**现象**：`docker push` 能成功，但 `docker buildx build --push` 失败：

```
failed to push {registry}/{img}:{tag}: failed to do request: Head "https://{registry}/v2/...":
http: server gave HTTP response to HTTPS client
```

**根因**：buildx 的 `docker-container` driver 在**独立的 buildkit 容器**里跑，**不继承** Docker daemon 的 `insecure-registries` 配置。daemon 那边配了 `insecure-registries: ["{registry}"]` 只对 `docker login/pull/push` 有效，buildx 看不到。

**解决方法**（**让用户做，不在 script 里自动做**）：

给 buildx builder 配 `buildkitd.toml`：

```toml
[registry."{host:port}"]
  http = true
  insecure = true
```

然后创建 builder 时传 `--config`：

```bash
docker buildx rm default-insecure 2>/dev/null || true
docker buildx create \
  --name default-insecure \
  --use \
  --driver docker-container \
  --driver-opt network=host \
  --config /path/to/buildkitd.toml \
  --platform linux/amd64,linux/arm64
docker buildx inspect --bootstrap
```

**为什么 script 不自动做**：用户可能已经配好了支持 HTTP registry 的 default builder（全局配置）。自动 create 会覆盖或产生混乱。如果用户原来的 `docker buildx build --platform ... --push` 就能成功，说明环境已经配好，script 直接用当前激活的 builder 即可。

---

## 2. 多镜像拆分后 nginx 不工作

**现象**：`docker compose up` 一切正常，但访问 `http://localhost:{PORT}/` 空白或 404。

**根因**：单镜像方案里 `Dockerfile` 有 `COPY docker/nginx.conf /etc/nginx/nginx.conf`，把配置烧在默认路径。多镜像方案里 `nginx.conf` 打进 `{project}-code`，运行时通过 code volume 挂到 `/apps/{project}/nginx.conf`，**不在** nginx 默认读取路径。`entrypoint.sh` 里 `nginx` 命令默认读 `/etc/nginx/nginx.conf`（系统默认，不是我们的），所以 nginx 监听 80 而不是业务端口。

**修复**：`entrypoint.sh` 在 `nginx` 启动前复制：

```bash
echo "🌐 Starting Nginx on port {PORT}..."
cp /apps/{project}/nginx.conf /etc/nginx/nginx.conf
nginx
```

或者用 `-c` 指定：

```bash
nginx -c /apps/{project}/nginx.conf
```

前者和旧流程一致，推荐。

**验证**：

```bash
docker exec {project} head -5 /etc/nginx/nginx.conf
# 应看到你的 worker_processes 2; 等内容，而不是 nginx 自带的 user www-data 等
```

---

## 3. macOS bash 3.2 + `set -u` + 空数组报 unbound variable

**现象**：

```
./scripts/push-images.sh: line 90: extra_args[@]: unbound variable
```

**根因**：macOS 自带 bash 3.2，在 `set -u` 下把 `"${arr[@]}"`（空数组）当作未绑定变量。

**解决**：用 `${arr[@]+"${arr[@]}"}` 形式：

```bash
local -a extra_args=()
# ...（可能追加元素或不追加）
docker buildx build \
  --platform "$PLATFORMS" \
  ${extra_args[@]+"${extra_args[@]}"} \       # ← 空数组展开为空，非空正常展开
  --push .
```

**语义**：`${arr[@]+x}` — 如果 arr 已设置（Bash 3.2 认为空数组是"未设置"），则展开为 `x`；否则展开为空。配合 `"${arr[@]}"` 的元素级引用，兼容 3.2 和新版 bash。

---

## 4. 多架构 venv build 时 `FROM sage-base` 找不到

**现象**：`docker buildx build --platform linux/amd64,linux/arm64 -f Dockerfile.venv --push` 报 `sage-base:1.0.0: not found`。

**根因**：多架构构建时，buildx 对每个目标平台单独拉 FROM 镜像。本地 `docker image inspect sage-base:1.0.0` 能看到是**当前 host 架构**那一份，但 buildx 尝试拉的是**目标架构**那一份，要么在 registry 里找（找不到），要么走本地缓存（架构不匹配）。

**解决**：两步

a. **先 push base 多架构到 registry**（用 buildx 做）
b. **venv build 时显式指向 registry**：Dockerfile.venv 加 `ARG BASE_IMAGE=sage-base`（默认值给本地开发用），push script 传 `--build-arg BASE_IMAGE={registry}/{ns}/{project}-base`，这样 buildx 会从 registry 拉对应架构的 base。

```dockerfile
# Dockerfile.venv
ARG BASE_IMAGE=sage-base
ARG BASE_TAG=1.0.0
FROM ${BASE_IMAGE}:${BASE_TAG} AS builder
```

```bash
# push-images.sh venv case
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t "${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/{project}-venv:${VENV_TAG}" \
    -f docker/Dockerfile.venv \
    --build-arg BASE_IMAGE="${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/{project}-base" \
    --build-arg BASE_TAG="${BASE_TAG}" \
    --push .
```

**相关坑（同属多架构 buildx 拉镜像国内不可达）**：`COPY --from=ghcr.io/astral-sh/uv:latest`
装 uv，多架构 push 时对每个平台拉 ghcr.io 元数据，国内报
`failed to fetch anonymous token ... ghcr.io/token ... EOF`（单架构本地 build 因有缓存可能
侥幸通过，多架构必拉 ghcr → 挂）。**改用 `RUN pip install --no-cache-dir -i
https://mirrors.aliyun.com/pypi/simple/ uv` 从阿里云装**（见 cn-mirrors.md）；pip 装的 uv 在
`/usr/local/bin/uv`，多阶段 runtime 用 `COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv`。

---

## 5. Apple Silicon 交叉构建 amd64 慢

**现象**：M 系 Mac 上 `docker buildx build --platform linux/amd64` 构建 Python venv，比原生构建慢 2-5 倍。

**根因**：buildx 用 QEMU 模拟 amd64，`uv sync` / `pip install` 的所有 CPU 密集操作都走模拟。

**应对**：
- 首次构建接受慢（uv sync 可能 20-30 分钟 vs 原生 5-10 分钟）
- 后续只要 `uv.lock` 不变就走缓存
- 如果频繁发版，考虑找一台 amd64 构建机

---

## 6. `docker save` + tar 包部署：短名 vs 带仓库前缀

**现象**：tar 里 image 名字是 `{registry}/{ns}/{project}-code:2.1.0`，但 compose 里引用 `{project}-code:2.1.0`（短名），服务器 `docker load` 后 compose 找不到镜像。

**两个解决思路**：

**思路 A（推荐）**：在**中转机** retag 成短名再 save。生产机器 load 后直接 `docker compose up`，不见仓库前缀。

```bash
# 中转机
docker pull --platform linux/amd64 {registry}/{ns}/{project}-code:2.1.0
docker tag {registry}/{ns}/{project}-code:2.1.0 {project}-code:2.1.0
docker save {project}-code:2.1.0 -o {project}-code-2.1.0.tar

# 生产机器
docker load -i {project}-code-2.1.0.tar
docker compose up -d   # ← 不用 retag
```

**思路 B**：生产机器 load 后 retag。compose 可以继续用短名。

```bash
docker load -i {project}-code-2.1.0.tar
docker tag {registry}/{ns}/{project}-code:2.1.0 {project}-code:2.1.0
```

A 的好处：生产 / 运维手册里看不到 registry 地址，更干净。

---

## 7. compose profile 的 `build` 服务启动时也会跑

**现象**：`docker compose up -d` 时不小心把所有 `*-build` 服务也启动了。

**原因**：没给 build 服务加 `profiles` 键。

**修复**：每个 build 服务加 `profiles: ["build"]`，这样默认 `up` 不会启动它们：

```yaml
base-build:
  build: { context: .., dockerfile: docker/Dockerfile.base }
  image: {project}-base:${BASE_TAG}
  command: ["true"]
  restart: "no"
  profiles: ["build"]   # ← 关键
```

单独 build：`docker compose --profile build build base-build`。

---

## 8. venv 在 volume 里但 `import X` 失败

**现象**：main 容器启动后 `python -c "import fastapi"` 报 ModuleNotFoundError。`ls /apps/{project}/.venv/bin/python` 存在。

**排查**：

a. 看 shebang：`head -1 /apps/{project}/.venv/bin/python`，应为 `#!/apps/{project}/.venv/bin/python`（绝对路径）。如果是别的路径，说明 builder 阶段 WORKDIR 不对。
b. 看 `PATH`：`echo $PATH`，应含 `/apps/{project}/.venv/bin`。
c. 看 volume 挂载路径：`docker inspect {project} | grep -A3 Mounts | grep venv-data`，destination 应是 `/apps/{project}/.venv`。

**根因几乎总是 builder WORKDIR 不等于运行时 volume 挂载路径**。修 Dockerfile.venv：

```dockerfile
ARG BASE_IMAGE=sage-base
ARG BASE_TAG=1.0.0
FROM ${BASE_IMAGE}:${BASE_TAG} AS builder
WORKDIR /apps/{project}                # ← 必须和运行时挂载路径一致
# ...
```

---

## 9. `docker compose down -v` 后数据没了但 named volume 还在

**现象**：跑了 `down -v`，但 `docker volume ls` 还能看到 `{project}_venv-data`。

**原因**：`down -v` 清的是本次 compose project 里声明的 volume，如果 project 名字因为目录名变化等导致 compose 认不出"旧的 project"，旧 volume 不会被清。

**手动清**：

```bash
docker volume ls --filter name={project}
docker volume rm {project}_venv-data {project}_models-data {project}_code-data
```

---

## 10. push 时 `docker login` 成功但 push 失败（401 / forbidden）

**现象**：login 返回 succeeded，push 返回 403 / unauthorized。

**排查**：

a. `REGISTRY_NAMESPACE` 写错，或 Harbor project 权限不对。去 Harbor UI 确认当前用户对该 project 有 `Push` 权限。
b. 镜像名超过长度 / 有非法字符。Harbor 通常要求 lowercase。
c. Harbor project 设置了"禁止覆盖 tag"，推相同 tag 会失败。bump 版本号或在 Harbor 里开启覆盖。

---

## 11. dev 改了代码 run-local.sh 后页面还是旧版本

**现象**：本地改了 java / python 代码 → `./docker/scripts/run-local.sh code` → 看到 code 镜像被重新 build（同 tag 1.4.0，新内容） → compose down + up 完成 → 但访问页面还是旧逻辑。

**根因**：dev compose 的 init 容器保留了 `.version` skip 逻辑：

```yaml
code-init:
  image: {project}-code:${CODE_TAG}
  environment: [TAG=${CODE_TAG}]
  command: >
    sh -c '
      if [ "$$(cat /target/.version 2>/dev/null)" = "$$TAG" ]; then
        echo "code $$TAG already synced, skip";   # ← 这里跳过了
      else
        ...
      fi
    '
```

`.version` 文件里是 `1.4.0`，TAG 也是 `1.4.0`，匹配 → 跳过 cp → volume 里还是上次的旧代码。

**修复**：dev compose 的 init 容器**直接去掉 .version skip**，每次都全量 cp：

```yaml
code-init:
  image: {project}-code:${CODE_TAG}
  volumes: [code-data:/target]
  command: >
    sh -c '
      rm -rf /target/* /target/.[!.]* 2>/dev/null || true;
      cp -a /export/. /target/;
      echo "code synced";
    '
  restart: "no"
```

**生产 compose 保留 skip**：因为生产升级**总会** bump tag（1.4.0 → 1.4.1），`.version` 不匹配自然触发重 cp。restart 没 bump tag 时跳过节省时间（避免每次重启重 cp 1GB venv）。

**为什么 dev 不能像生产那样靠 bump tag 触发**：dev 改代码每次都 bump 太烦人；同 tag 重 build + 全量 cp 是 dev 场景下"语义最一致"的做法。代价是 init 每次跑一次 cp（dev 的 code 通常 ~200MB，秒级完成，可以接受）。

---

## 12. `run-local.sh` 第二次跑报 `container name already in use`

**现象**：第一次跑 `./scripts/run-local.sh` 成功，第二次跑报：

```
Error response from daemon: Conflict. The container name "/sage" is already in use by container "...".
You have to remove (or rename) that container to be able to reuse that name.
```

**根因**：compose 的 `container_name: sage` 指定了固定名字，`docker compose up -d` 在已有容器时不会自动销毁重建，就报冲突。

**解决**：脚本里 `up -d` 之前先尝试 `down`，保证幂等。判断当前是否有已运行的服务，避免空 down 无意义输出：

```bash
if docker compose ps --quiet 2>/dev/null | grep -q .; then
    echo "🧹 stopping existing compose stack (keeping volumes) ..."
    docker compose down --remove-orphans
fi
docker compose up -d
```

`down` 只销毁容器，**保留 named volume 和 bind mount 数据**。`--remove-orphans` 清理掉已经从 compose 里删掉但容器还在的老 service（比如重命名后的残留）。

**避免用 `down -v`**：那会清掉 `venv-data` / `models-data` / `code-data` 三个命名 volume，下次启动 init 容器要重新把 1.3GB venv + 400MB models 拷一遍，几分钟起步。除非确实需要重置。

**顺带**：给 `up -d` 也加 `--remove-orphans`。compose 用目录名作项目名，若历史上在同目录跑过别的 compose 栈，那边的容器会被当作"orphan"每次 up 都报 WARN。加 `--remove-orphans` 把它们也清掉：

```bash
docker compose up -d --remove-orphans
```

注意 orphan 判定基于**同项目名下当前 compose 文件未声明的 service**，不会误删其它项目（不同目录 / 不同 `-p` 指定项目名）的容器。

---

## 13. `git add -A` 把 mariadb 运行时数据全 commit 入库

**现象**：dev 跑过一次 `run-local.sh` 后做 `git add -A && git commit`，commit message 显示 `285 files changed`，里面全是 `docker/containers/data/mysql/data/**/*.ibd` `*.frm` 这种 mariadb 内部文件。push 上去会被同事吐槽（commit 巨大、影响 clone 速度）。

**根因**：`.gitignore` 没把 `docker/containers/*/data/` 这条加上。dev compose 里 mariadb / 日志走 bind mount 挂到 `docker/containers/data/`（按"compose 文件同级 data/"约定），跑一次后 mysql 数据文件、日志文件就在那里堆着——`git add -A` 一把全收。

**修复（已发生）**：

```bash
# 撤回 commit 但保留改动
git reset --soft HEAD~1

# .gitignore 加规则（templates.md 有完整模板）
cat >> .gitignore <<'EOF'
docker/containers/data/
docker/containers/*/data/
docker/images/.env
docker/scripts/.registry.env
EOF

# 把已 staging 的运行时数据从 git index 移除（保留本地文件）
git rm --cached -r docker/containers/data
git rm --cached docker/images/.env docker/scripts/.registry.env

# 重新 commit
git add -A
git commit -m "..."
```

**预防（首选）**：用本 skill 创建 docker 项目时，`.gitignore` + `.dockerignore` **同步生成**。模板见 [templates.md](templates.md)。两个 ignore 缺一不可——`.dockerignore` 漏 `docker/containers/*/data/` 会让 build context 拖到几个 GB 拖慢 build。
