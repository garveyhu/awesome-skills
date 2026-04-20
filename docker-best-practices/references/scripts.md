# Scripts 工作流（build / push / run-local）

三个脚本封装"本地构建、多架构推送、本地一键启动"的常用操作，**单镜像和多镜像都适用**。

## 共同约定

- 放在项目根 `scripts/` 下，可执行位（`chmod +x`）
- `set -euo pipefail`
- 读 `docker/.env` 拿镜像 tag（用户可改）
- 仓库凭据读 `scripts/.registry.env`（gitignored，真实值）
- 输出用 emoji 前缀 + 中文提示
- **不要自动创建 buildx builder** — 用户可能已经配好了 default builder（特别是对 HTTP registry 有特殊配置的），覆盖会炸

## 1. `scripts/build-images.sh`

**单镜像**：一次 `docker build`（可选 `--no-cache`）。
**多镜像**：按 base → venv → models → code 顺序；**base/venv/models 按 tag 检查 skip**，code 每次重建。

```bash
#!/usr/bin/env bash
# 按 .env 中的 tag 构建镜像；已存在的 tag 跳过（code 除外）。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ENV_FILE="docker/.env"
[ -f "$ENV_FILE" ] || { echo "❌ $ENV_FILE not found. Copy from docker/.env.example first."; exit 1; }

# shellcheck disable=SC1090
set -a; . "$ENV_FILE"; set +a

build_if_missing() {
    local image=$1 tag=$2 dockerfile=$3 extra_args=${4:-}
    if docker image inspect "${image}:${tag}" >/dev/null 2>&1; then
        echo "✓ ${image}:${tag} already exists, skip"
        return
    fi
    echo "→ building ${image}:${tag}"
    # shellcheck disable=SC2086
    docker build -t "${image}:${tag}" -f "${dockerfile}" ${extra_args} .
}

build_if_missing {project}-base   "${BASE_TAG}"   docker/Dockerfile.base
build_if_missing {project}-venv   "${VENV_TAG}"   docker/Dockerfile.venv   "--build-arg BASE_TAG=${BASE_TAG}"
build_if_missing {project}-models "${MODELS_TAG}" docker/Dockerfile.models

# code 每次都 build（tag 每次都变）
echo "→ building {project}-code:${CODE_TAG}"
docker build -t "{project}-code:${CODE_TAG}" -f docker/Dockerfile.code .

echo "✅ all images ready:"
docker image ls --format '{{.Repository}}:{{.Tag}}\t{{.Size}}' | grep -E "^{project}-(base|venv|models|code):"
```

---

## 2. `scripts/push-images.sh`

关键设计：
- 登录用 `.registry.env` 的凭据（用户唯一维护的秘密）
- **不创建/切换 buildx builder** — 打印当前激活的那个，留给用户管理
- multi-arch `docker buildx build --push` 每个镜像一次
- venv 的 `FROM` 通过 `--build-arg BASE_IMAGE={host}/{ns}/{project}-base` 指向 registry，让 buildx 为每个目标架构从 registry 拉 base

```bash
#!/usr/bin/env bash
# 多架构 buildx + push 到内网镜像仓库
# 用法：./scripts/push-images.sh [target...] (base|venv|models|code)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ENV_FILE="docker/.env"
REG_ENV_FILE="scripts/.registry.env"

[ -f "$ENV_FILE" ]     || { echo "❌ $ENV_FILE not found."; exit 1; }
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

# 使用当前激活的 buildx builder（不自动创建/切换 — 用户如果配过支持 HTTP registry
# 的 default builder，抢管会失效）
docker buildx version >/dev/null 2>&1 || { echo "❌ docker buildx 不可用"; exit 1; }
echo "🛠  using current buildx builder: $(docker buildx inspect --bootstrap 2>/dev/null | awk '/^Name:/{print $2; exit}')"

push_one() {
    local which=$1
    local image tag dockerfile
    local -a extra_args=()
    case "$which" in
        base)
            image={project}-base; tag="$BASE_TAG"; dockerfile=docker/Dockerfile.base ;;
        venv)
            image={project}-venv; tag="$VENV_TAG"; dockerfile=docker/Dockerfile.venv
            # 多架构构建时 venv 的 FROM 必须能从仓库拉 base
            extra_args+=(
              --build-arg "BASE_IMAGE=${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/{project}-base"
              --build-arg "BASE_TAG=${BASE_TAG}"
            )
            ;;
        models)
            image={project}-models; tag="$MODELS_TAG"; dockerfile=docker/Dockerfile.models ;;
        code)
            image={project}-code; tag="$CODE_TAG"; dockerfile=docker/Dockerfile.code ;;
        *) echo "❌ unknown target: $which"; exit 1 ;;
    esac

    local full_tag="${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/${image}:${tag}"
    echo ""
    echo "→ buildx push: $full_tag  [$PLATFORMS]"
    # ⚠️ macOS bash 3.2 + set -u 下空数组要用 ${arr[@]+...} 形式
    docker buildx build \
        --platform "$PLATFORMS" \
        -t "$full_tag" \
        -f "$dockerfile" \
        ${extra_args[@]+"${extra_args[@]}"} \
        --push \
        .
}

if [ $# -eq 0 ]; then
    targets=(base venv models code)     # 顺序：base 必须先（venv 依赖）
else
    targets=("$@")
fi

# 若指定了 venv 但没指定 base，提醒仓库里已存在 base
if [[ " ${targets[*]} " == *" venv "* ]] && [[ " ${targets[*]} " != *" base "* ]]; then
    echo "⚠️  venv 依赖 ${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/{project}-base:${BASE_TAG}，确保已推送。"
fi

for t in "${targets[@]}"; do
    push_one "$t"
done

echo ""
echo "===================================================================="
echo "✅ 推送完成：${REGISTRY_HOST}/${REGISTRY_NAMESPACE}/"
for t in "${targets[@]}"; do
    case "$t" in
        base)   echo "  - {project}-base:${BASE_TAG}" ;;
        venv)   echo "  - {project}-venv:${VENV_TAG}" ;;
        models) echo "  - {project}-models:${MODELS_TAG}" ;;
        code)   echo "  - {project}-code:${CODE_TAG}" ;;
    esac
done
```

### `scripts/.registry.env.example`

```env
# 复制为 .registry.env 并填入真实值；.registry.env 不入 git
REGISTRY_URL=http://<harbor:port>
REGISTRY_USER=<user>
REGISTRY_PASSWORD=<password>
REGISTRY_NAMESPACE=<namespace>
PLATFORMS=linux/amd64,linux/arm64
```

---

## 3. `scripts/run-local.sh`

一键本地：初始化 → build（增量） → **停掉已有 compose 栈 → up** → 等 healthy → 打印访问/运维提示。

**关键设计**：脚本必须支持重复执行。直接 `docker compose up -d` 在容器已存在时会报 `container name 'xxx' already in use`，所以先 `docker compose down --remove-orphans`（保留 volume，只销毁容器）。已经干净的状态下 down 是 no-op。

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# 初始化 .env
if [ ! -f docker/.env ]; then
    echo "📋 首次运行：复制 docker/.env.example → docker/.env"
    cp docker/.env.example docker/.env
fi

# 挂载目录（按项目类型）
mkdir -p docker/resources/mysql/data \
         docker/resources/mysql/logs \
         docker/resources/diskcache \
         docker/resources/chromadb \
         docker/logs

# Build（skip-if-exists）
echo ""
echo "📦 building images (skip-if-exists) ..."
"${ROOT}/scripts/build-images.sh"

# 先停掉现有栈（保留 named volume），让脚本可重复执行
cd docker
if docker compose ps --quiet 2>/dev/null | grep -q .; then
    echo ""
    echo "🧹 stopping existing compose stack (keeping volumes) ..."
    docker compose down --remove-orphans
fi

# 启动
echo ""
echo "🚀 docker compose up -d ..."
docker compose up -d

# 等 healthy（最多 90s）
echo ""
echo "⏳ 等待 {project} 容器 healthy (最多 90s) ..."
healthy=false
for i in $(seq 1 90); do
    status=$(docker inspect --format='{{.State.Health.Status}}' {project} 2>/dev/null || echo "missing")
    if [ "$status" = "healthy" ]; then
        echo "✅ {project} is healthy"
        healthy=true
        break
    fi
    sleep 1
done
$healthy || { echo "⚠️  健康检查超时，最近日志："; docker compose logs --tail=30 {project}; }

# 打印访问 + 常用命令
cat <<'BANNER'

====================================================================
🎉 {project} 已启动（本地开发模式）
====================================================================

📱 通过 Nginx 统一入口（端口 {PORT}）：
   http://localhost:{PORT}/{prefix}/   前端
   http://localhost:{PORT}/{prefix}/api/   后端 API

🔌 直连服务：
   http://localhost:{API_PORT}/ping   健康检查

🔍 常用命令：
   docker compose logs -f {project}       跟日志
   docker exec -it {project} bash         进容器
   docker compose down                    停止（保留 volume）
   docker compose down -v                 清空数据

📝 只改代码的快速重启（多镜像模式）：
   sed -i '' 's/^CODE_TAG=.*/CODE_TAG=<new>/' docker/.env
   docker compose --profile build build code-build
   docker compose up -d

☁️  推送到内网仓库：
   ./scripts/push-images.sh          推全部
   ./scripts/push-images.sh code     只推代码
====================================================================
BANNER
```

---

## 使用习惯建议

- **写新项目先出 `.env.example`**。用户复制一份为 `.env`，脚本从 `.env` 读取。`.env` gitignored。
- **build-images.sh 的 skip-if-exists** 对多镜像很有用（venv/models 稳定），单镜像场景可以简化为单次 `docker build`。
- **push-images.sh 不做 builder 管理**。失败时给用户提示，不代替他们决策。
- **run-local.sh 的"等 healthy + 打印提示"模式** 对任何 Docker 项目都适用，无论是否拆分。

## 经验沉淀

- macOS 自带 bash 3.2，`set -u` + `"${arr[@]}"`（空数组）会报 unbound variable。统一用 `${arr[@]+"${arr[@]}"}`。
- registry 地址格式：`REGISTRY_URL` 保留 protocol（`http://` 或 `https://`），需要 `host:port` 时剥掉（`${REGISTRY_URL#http://}`）。
- `docker login` 接受完整 URL（带 `http://`），tag 里用 `host:port` 形式。两个用法的脚本内要分清。
