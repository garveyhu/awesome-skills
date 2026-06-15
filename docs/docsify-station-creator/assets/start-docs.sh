# 整个 docsify 站点都在 docs/docsify/（index.html / 配置 / 脚本 / 动画资源）；
# 文档内容在 docs/* 兄弟目录。docsify 是纯前端库，用任意静态服务器即可：
# 从 docs/ 根起服务（这样 docs/* 内容可达），浏览器访问 /docsify/。
# 注意：不要用 `docsify serve`，它要求服务根有 index.html，而我们的 index.html 在子目录。

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"   # docs/  （脚本在 docs/docsify/scripts/）
PORT=3000
URL="http://localhost:$PORT/docsify/"

cd "$DOCS_ROOT" || exit 1
echo "Serving: $DOCS_ROOT"
echo "→ 打开 $URL"

if command -v python3 >/dev/null 2>&1; then
    python3 -m http.server "$PORT"
elif command -v python >/dev/null 2>&1; then
    python -m http.server "$PORT"
elif command -v npx >/dev/null 2>&1; then
    npx --yes http-server . -p "$PORT" -c-1
else
    echo "需要 python3 或 Node(npx) 来启动静态服务器，请先安装其一。"
    exit 1
fi
