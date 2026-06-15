# Scripts 工作流（build / push / run-local / stop-local）

四个脚本封装"本地构建、多架构推送、本地一键启动、停掉本地容器"的常用操作。

## 共同约定

- 放在 `docker/scripts/` 下（不是项目根 `scripts/`），可执行位（`chmod +x`）
- `set -euo pipefail`
- `ROOT="$(cd "$(dirname "$0")/../.." && pwd)"`（脚本上溯两层到项目根）
- 读 `docker/images/.env` 拿镜像 tag
- 仓库凭据读 `docker/scripts/.registry.env`（gitignored，真实值）
- 输出用 emoji 前缀 + 中文提示
- **不要自动创建 buildx builder**——用户可能已经配好了 default builder（特别是对 HTTP registry 有特殊配置的），覆盖会炸

## 统一参数协议

build / push / run-local 三个脚本都接受同样的可选参数 `[target ...]`（stop-local 不需要参数，只接 `-v` 控制是否清 volume）：

```bash
./docker/scripts/<script>.sh              # 不传参 = 处理全部镜像
./docker/scripts/<script>.sh code         # 只处理 code
./docker/scripts/<script>.sh code ui      # 多个
./docker/scripts/<script>.sh base         # 只处理 base
```

target 是镜像简短名（不带 `{project}-` 前缀），如 `base / code / ui / venv / models`。

`run-local.sh` 的 target 透传给 `build-images.sh`，build 完后无论参数如何都做完整的 compose down → up。

---

## 1. `docker/scripts/build-images.sh`

**核心逻辑**：base 用 skip-if-exists（系统层几乎不变），其他层默认每次都重建（dev 改了代码就要新版本）。

```bash
#!/usr/bin/env bash
# 按 docker/images/.env 的 tag 构建镜像
# 用法：
#   ./docker/scripts/build-images.sh           → 全部 (base skip-if-exists；其他重建)
#   ./docker/scripts/build-images.sh code      → 只 build code
#   ./docker/scripts/build-images.sh code ui   → 多个
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

ENV_FILE="docker/images/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ $ENV_FILE not found. Copy from docker/images/.env.example first."
    exit 1
fi

# shellcheck disable=SC1090
set -a; . "$ENV_FILE"; set +a

build_one() {
    local which=$1
    case "$which" in
        base)
            # 系统层几乎不变，已存在 tag 跳过
            if docker image inspect "{project}-base:${{PROJECT_UPPER}_BASE_TAG}" >/dev/null 2>&1; then
                echo "✓ {project}-base:${{PROJECT_UPPER}_BASE_TAG} already exists, skip"
            else
                echo "→ building {project}-base:${{PROJECT_UPPER}_BASE_TAG}"
                docker build -t "{project}-base:${{PROJECT_UPPER}_BASE_TAG}" \
                    -f docker/images/Dockerfile.base .
            fi
            ;;
        code)
            echo "→ building {project}-code:${{PROJECT_UPPER}_CODE_TAG}"
            docker build -t "{project}-code:${{PROJECT_UPPER}_CODE_TAG}" \
                -f docker/images/Dockerfile.code .
            ;;
        ui)
            echo "→ building {project}-ui:${{PROJECT_UPPER}_UI_TAG}"
            docker build -t "{project}-ui:${{PROJECT_UPPER}_UI_TAG}" \
                -f docker/images/Dockerfile.ui .
            ;;
        # venv / models 等其他层按相同模式追加
        *)
            echo "❌ unknown target: $which (expected: base|code|ui)"
            exit 1
            ;;
    esac
}

if [ $# -eq 0 ]; then
    targets=(base code ui)
else
    targets=("$@")
fi

for t in "${targets[@]}"; do
    build_one "$t"
done

echo ""
echo "✅ built: ${targets[*]}"
docker image ls --format '{{.Repository}}:{{.Tag}}\t{{.Size}}' | grep -E '^{project}-(base|code|ui):'
```

**关键决策**：

| 层 | skip-if-exists？ | 原因 |
|----|-----------------|------|
| `base` | 是 | 系统包升级时才 bump tag，平时跳过省时间 |
| `venv` / `models` | 是（如果有） | 依赖 / 模型变化时才 bump |
| `code` | 否，每次重建 | dev 频繁改 java/python 代码，每次都要新版本 |
| `ui` | 否，每次重建 | dev 频繁改前端，且前端代码常用 git clone 进镜像 |

---

## 2. `docker/scripts/push-images.sh`

**核心设计**：
- 登录用 `.registry.env` 的凭据
- **不创建/切换 buildx builder**——用当前激活的（`docker buildx inspect --bootstrap` 显示）
- multi-arch `docker buildx build --push` 每个镜像一次
- venv 的 `FROM` 通过 `--build-arg BASE_IMAGE={host}/{ns}/{project}-base` 指向 registry，让 buildx 为每个目标架构从 registry 拉 base

```bash
#!/usr/bin/env bash
# 多架构 buildx + push 到内网镜像仓库
# 用法：
#   ./docker/scripts/push-images.sh              → 全部（顺序：base → venv → models → code → ui）
#   ./docker/scripts/push-images.sh code         → 只推 code
#   ./docker/scripts/push-images.sh code ui      → 多个
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

ENV_FILE="docker/images/.env"
REG_ENV_FILE="docker/scripts/.registry.env"

[ -f "$ENV_FILE" ] || { echo "❌ $ENV_FILE not found."; exit 1; }
[ -f "$REG_ENV_FILE" ] || { echo "❌ $REG_ENV_FILE not found. Copy from .registry.env.example."; exit 1; }

# shellcheck disable=SC1090
set -a; . "$ENV_FILE"; . "$REG_ENV_FILE"; set +a

: "${REGISTRY_URL:?REGISTRY_URL not set}"
: "${REGISTRY_USER:?REGISTRY_USER not set}"
: "${REGISTRY_PASSWORD:?REGISTRY_PASSWORD not set}"
: "${REGISTRY_NAMESPACE:?REGISTRY_NAMESPACE not set}"

PLATFORMS="${PLATFORMS:-linux/amd64,linux/arm64}"

REGISTRY_HOST="${REGISTRY_URL#http://}"
REGISTRY_HOST="${REGISTRY_HOST#https://}"
REGISTRY_HOST="${REGISTRY_HOST%/}"

echo "🔐 docker login $REGISTRY_HOST ..."
echo "$REGISTRY_PASSWORD" | docker login -u "$REGISTRY_USER" --password-stdin "$REGISTRY_URL"

# 用当前激活的 buildx builder（不抢管，尊重用户已配置的 HTTP registry builder）
docker buildx version >/dev/null 2>&1 || { echo "❌ docker buildx 不可用"; exit 1; }
echo "🛠  using current buildx builder: $(docker buildx inspect --bootstrap 2>/dev/null | awk '/^Name:/{print $2; exit}')"

push_one() {
    local which=$1
    local image tag dockerfile
    local -a extra_args=()
    case "$which" in
        base)
            image={project}-base; tag="${{PROJECT_UPPER}_BASE_TAG}"
            dockerfile=docker/images/Dockerfile.base
            ;;
        venv)
            image={project}-venv; tag="${{PROJECT_UPPER}_VENV_TAG}"
            dockerfile=docker/images/Dockerfile.venv
            # 多架构构建时 venv 的 FROM 必须能从仓库拉 base
            extra_args+=(
              --build-arg "BASE_IMAGE=${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/{project}-base"
              --build-arg "BASE_TAG=${{PROJECT_UPPER}_BASE_TAG}"
            )
            ;;
        code)
            image={project}-code; tag="${{PROJECT_UPPER}_CODE_TAG}"
            dockerfile=docker/images/Dockerfile.code
            ;;
        ui)
            image={project}-ui; tag="${{PROJECT_UPPER}_UI_TAG}"
            dockerfile=docker/images/Dockerfile.ui
            ;;
        *) echo "❌ unknown target: $which"; exit 1 ;;
    esac

    local full_tag="${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/${image}:${tag}"
    echo ""
    echo "→ buildx push: $full_tag  [$PLATFORMS]"
    # macOS bash 3.2 + set -u 下空数组要用 ${arr[@]+...} 形式
    docker buildx build \
        --platform "$PLATFORMS" \
        -t "$full_tag" \
        -f "$dockerfile" \
        ${extra_args[@]+"${extra_args[@]}"} \
        --push \
        .
}

if [ $# -eq 0 ]; then
    targets=(base code ui)         # 顺序：base 必须先（venv 等依赖）
else
    targets=("$@")
fi

# 若指定了 venv 但没指定 base，提醒仓库里已存在 base
if [[ " ${targets[*]} " == *" venv "* ]] && [[ " ${targets[*]} " != *" base "* ]]; then
    echo "⚠️  venv 依赖 ${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/{project}-base:${{PROJECT_UPPER}_BASE_TAG}，确保已推送。"
fi

for t in "${targets[@]}"; do
    push_one "$t"
done

echo ""
echo "===================================================================="
echo "✅ 推送完成：${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/"
for t in "${targets[@]}"; do
    case "$t" in
        base) echo "  - {project}-base:${{PROJECT_UPPER}_BASE_TAG}" ;;
        venv) echo "  - {project}-venv:${{PROJECT_UPPER}_VENV_TAG}" ;;
        code) echo "  - {project}-code:${{PROJECT_UPPER}_CODE_TAG}" ;;
        ui)   echo "  - {project}-ui:${{PROJECT_UPPER}_UI_TAG}"     ;;
    esac
done
echo "===================================================================="
```

### `.registry.env.example`

```env
# 复制为 .registry.env 并填入真实值；.registry.env 不入 git
REGISTRY_URL=http://<harbor:port>
REGISTRY_USER=<user>
REGISTRY_PASSWORD=<password>
REGISTRY_NAMESPACE=<namespace>
PLATFORMS=linux/amd64,linux/arm64
```

---

## 3. `docker/scripts/run-local.sh`

一键本地：build（按参数）→ down → up → 等就绪 → banner。

**关键设计**：
1. 参数透传给 `build-images.sh`，达到"只重 build code"等选择性 rebuild 的能力
2. **总是 `down + up`**，确保 init 容器重新跑（因为 dev compose 已经去掉 .version skip，每次都全量 cp 新内容）
3. 等待主容器健康（curl 端点最多 90s），超时打印日志

```bash
#!/usr/bin/env bash
# 一键本地：build → down → up → 等就绪
# 用法：
#   ./docker/scripts/run-local.sh           → build 全部 + up
#   ./docker/scripts/run-local.sh code      → 只 rebuild code，base/ui 沿用旧镜像 + up
#   ./docker/scripts/run-local.sh code ui   → 多个
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

# --- 初始化：.env + 挂载目录 ---
if [ ! -f docker/images/.env ]; then
    echo "📋 首次运行：复制 docker/images/.env.example → docker/images/.env"
    cp docker/images/.env.example docker/images/.env
fi

# 挂载目录（按项目类型实际需要调整）
mkdir -p docker/containers/data/mysql/data \
         docker/containers/data/mysql/logs \
         docker/containers/data/logs

# --- build（参数透传给 build-images.sh）---
echo ""
echo "📦 building images ..."
"${ROOT}/docker/scripts/build-images.sh" "$@"

# --- compose down + up（无论是否在跑都先 down，保证 init 容器重跑）---
DC="docker compose --env-file docker/images/.env -f docker/containers/docker-compose.yml"

echo ""
echo "🧹 stopping existing compose stack (keeping volumes) ..."
$DC down --remove-orphans 2>/dev/null || true

echo ""
echo "🚀 docker compose up -d ..."
$DC up -d --remove-orphans

# --- 等主容器健康（最多 90s）---
echo ""
echo "⏳ 等待 {project} 就绪 (最多 90s) ..."
healthy=false
for i in $(seq 1 90); do
    if curl -fs http://localhost:{API_PORT}/ping >/dev/null 2>&1; then
        echo "✅ {project} is healthy"
        healthy=true
        break
    fi
    sleep 1
done
$healthy || echo "⚠️  健康检查超时，最近日志："
$healthy || $DC logs --tail=30 {project}

# --- 打印访问入口 ---
cat <<'BANNER'

====================================================================
🎉 {project} 已启动（本地开发）
====================================================================

📱 通过 Nginx 统一入口（{PORT}）：
   http://localhost:{PORT}/{prefix}/        前端 UI
   http://localhost:{PORT}/{prefix}/api/    API（代理到 {API_PORT}）

🔌 直连服务：
   http://localhost:{API_PORT}/             API
   localhost:{DB_PORT}                      内置 MariaDB（root/changeme）

🔁 改完代码后再跑一次（按改动范围选择性 rebuild）：
   ./docker/scripts/run-local.sh                全部重建
   ./docker/scripts/run-local.sh code           只改了后端
   ./docker/scripts/run-local.sh ui             只改了前端
====================================================================
BANNER
```

---

## 4. `docker/scripts/stop-local.sh`

跟 `run-local.sh` 配对的退出口子。`exec docker compose logs -f` 启动后用户 Ctrl+C 只退日志，容器还在后台跑——用这个停。

```bash
#!/usr/bin/env bash
# 停掉本地 docker compose 跑的容器
# 用法：
#   ./docker/scripts/stop-local.sh         停（保留 volume + bind mount 数据）
#   ./docker/scripts/stop-local.sh -v      停 + 清空 named volume（code-data / ui-data）
#                                          ⚠️ 不会清 ./data 等 bind mount，那些是宿主机文件
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

DC="docker compose --env-file docker/images/.env -f docker/containers/docker-compose.yml"

if [ "${1:-}" = "-v" ] || [ "${1:-}" = "--clean" ]; then
    echo "🧹 docker compose down -v (清 named volume) ..."
    $DC down -v --remove-orphans
else
    echo "🛑 docker compose down (保留 volume) ..."
    $DC down --remove-orphans
fi

echo ""
echo "✅ 已停止"
```

**典型使用**：

```bash
./docker/scripts/run-local.sh code      # 起来 + attach 日志，确认 OK 后 Ctrl+C 退日志
./docker/scripts/stop-local.sh          # 改用 IDE 跑后端时停容器，避免端口冲突
./docker/scripts/stop-local.sh -v       # 清空 code/ui named volume，下次 init 容器全量重 cp
```

**注**：
- 默认 `down` 保留 named volume 和 bind mount 数据。下次 `run-local.sh` 上次的 mariadb 数据还在。
- `-v` 只清 docker named volume（`{project}_code-data` 等），**不会**清 `docker/containers/data/` 下的 mariadb / 日志这些 bind mount 文件——那些是宿主机文件，要清就 `rm -rf docker/containers/data`。

---

## 关键设计原则

### 为什么 `run-local.sh` 透传参数给 `build`？

dev 场景下"改代码 → 重启"是高频操作。让用户能选择性 rebuild：
- `run-local.sh` = 全部（首次启动 / 系统层升级）
- `run-local.sh code` = 只改了后端 java/python（最常见，几分钟省下一半）
- `run-local.sh ui` = 只改了前端

build 跑完后无论参数如何，**始终做完整的 `compose down + up`**，让 init 容器重新跑，把 volume 里的旧内容用新镜像内容替换。

### 为什么 dev compose 必须去掉 `.version` skip？

如果 dev compose 的 init 容器保留 `.version` skip：
- 用户改完代码 → `run-local.sh code` → code 镜像被重 build（**同 tag** 1.4.0，新内容）
- compose down → up → init 容器跑 → 看到 `.version=1.4.0` 等于 `TAG=1.4.0` → 跳过 cp → 旧代码继续跑
- **bug**

去掉 skip 后每次 init 都全量 cp，新代码生效。

生产 compose 保留 skip 是因为生产升级时**总会** bump tag（1.4.0 → 1.4.1），`.version=1.4.0` 跟 `TAG=1.4.1` 不匹配自然触发重 cp。restart 没 bump tag 时跳过节省时间。

### 为什么不用 `docker compose restart`？

`restart` 不会重跑 `restart: "no"` 的 init 容器，所以新镜像内容不会同步到 volume。必须 `down + up`。

---

## 经验沉淀

- macOS 自带 bash 3.2，`set -u` + `"${arr[@]}"`（空数组）会报 unbound variable。统一用 `${arr[@]+"${arr[@]}"}`。
- registry 地址格式：`REGISTRY_URL` 保留 protocol（`http://` 或 `https://`），需要 `host:port` 时剥掉（`${REGISTRY_URL#http://}`）。`docker login` 接受完整 URL，tag 用 `host:port`。
- `--remove-orphans` 加在 `up -d` 上避免历史 service 残留导致每次都报 WARN。
- `down` 不加 `-v`，保留 named volume；只有 `down -v` 清空 volume。dev 场景日常用 `down`，重置数据用 `down -v`。
