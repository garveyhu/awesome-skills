#!/usr/bin/env bash
# codex-image-gen —— 用 Codex 订阅账号经 `codex exec` 调内置 image_gen(gpt-image-2)出图。
#
# 用法:
#   gen-image.sh --prompt "画面描述" --out 路径.png [--ref 参考图 ...] [--size 16:9] [--dir 工作目录]
#
# 参数:
#   --prompt  必填。图片内容描述(英文/中文均可,英文对模型更稳)。
#   --out     必填。产物保存路径(相对则相对当前目录);父目录自动创建。
#   --ref     可选,可重复。参考图路径,用于锁定角色/风格一致性。
#   --size    可选。宽高比或尺寸,如 16:9 / 1:1 / 1536x1024。
#   --dir     可选。codex 的工作目录,默认取 --out 的父目录。
#
# 依赖:已登录的 Codex(~/.codex/auth.json,订阅或 API key 均可);codex 在 PATH,否则自动退回 npx。
# 成本:每张约 1.5w~3w Codex token(走订阅额度,非按张计费)。
set -euo pipefail

PROMPT=""; OUT=""; SIZE=""; DIR=""; REFS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --prompt) PROMPT="${2:-}"; shift 2;;
    --out)    OUT="${2:-}"; shift 2;;
    --ref)    REFS+=("${2:-}"); shift 2;;
    --size)   SIZE="${2:-}"; shift 2;;
    --dir)    DIR="${2:-}"; shift 2;;
    -h|--help) grep '^#' "$0" | sed 's/^#\{1,\} \{0,1\}//'; exit 0;;
    *) echo "未知参数: $1" >&2; exit 2;;
  esac
done

[ -n "$PROMPT" ] || { echo "缺少 --prompt" >&2; exit 2; }
[ -n "$OUT" ]    || { echo "缺少 --out" >&2; exit 2; }

# 绝对化输出路径与工作目录
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT";; esac
OUTDIR="$(dirname "$OUT")"; mkdir -p "$OUTDIR"
[ -n "$DIR" ] || DIR="$OUTDIR"
case "$DIR" in /*) ;; *) DIR="$PWD/$DIR";; esac
mkdir -p "$DIR"

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
GEN_DIR="$CODEX_HOME/generated_images"

# 选 codex:优先全局,退回 npx
if command -v codex >/dev/null 2>&1; then
  CODEX=(codex)
else
  CODEX=(npx --yes @openai/codex@latest)
fi

# 组装给 codex 的指令(让它只生成 + 保存,别干别的)
INSTR="Use the built-in image generation tool to generate exactly ONE image and save it to this absolute path: ${OUT}
Image description: ${PROMPT}"
[ -n "$SIZE" ] && INSTR="${INSTR}
Aspect ratio / size: ${SIZE}"
if [ "${#REFS[@]}" -gt 0 ]; then
  rabs=()
  for r in "${REFS[@]}"; do case "$r" in /*) rabs+=("$r");; *) rabs+=("$PWD/$r");; esac; done
  INSTR="${INSTR}
Use these reference image(s) to keep the character/style consistent: ${rabs[*]}"
fi
INSTR="${INSTR}
Do not edit any other files. Once ${OUT} is saved, stop."

# 出图前打时间标记,供兜底定位新产物
MARK="$(mktemp)"; trap 'rm -f "$MARK"' EXIT

echo "[codex-image-gen] 出图中 → $OUT" >&2
"${CODEX[@]}" exec -C "$DIR" -s workspace-write --skip-git-repo-check \
  -c model_reasoning_effort="low" "$INSTR" >&2 \
  || echo "[codex-image-gen] codex exec 退出码非零,尝试兜底" >&2

# agent 没把图拷到 --out 时,从 generated_images 找最新产物补上
if [ ! -f "$OUT" ] && [ -d "$GEN_DIR" ]; then
  newest="$(find "$GEN_DIR" -type f -name '*.png' -newer "$MARK" -exec stat -f '%m %N' {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)"
  [ -n "${newest:-}" ] && cp "$newest" "$OUT"
fi

if [ -f "$OUT" ]; then
  echo "[codex-image-gen] 完成: $OUT" >&2
  echo "$OUT"
else
  echo "[codex-image-gen] 失败:未生成 $OUT" >&2
  exit 1
fi
