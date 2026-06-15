#!/usr/bin/env bash
# 项目批量生图入口 —— 调用已安装的 comfyui skill 引擎,对本项目 assets/ 计划批量出图。
# 用法(在项目根):
#   bash scripts/comfyui/batch.sh --dry-run            # 先预览
#   bash scripts/comfyui/batch.sh --variants 3         # 真跑
#   bash scripts/comfyui/batch.sh --only props,ui --variants 3
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"                       # 项目根 = scripts/comfyui/../..
PROJECT="${COMFY_PROJECT:-$(basename "$ROOT")}"          # 项目名(默认目录名,可用 COMFY_PROJECT 覆盖)
SKILL="${COMFYUI_SKILL_DIR:-$HOME/.claude/skills/comfyui}"
if [[ ! -f "$SKILL/scripts/batch.sh" ]]; then
  echo "✗ 找不到 comfyui skill 引擎: $SKILL"; echo "  装好 skill,或设 COMFYUI_SKILL_DIR 指向它。"; exit 1
fi
exec bash "$SKILL/scripts/batch.sh" "$ROOT/assets" \
  --project "$PROJECT" --workflows-dir "$ROOT/comfy-workflows" "$@"
