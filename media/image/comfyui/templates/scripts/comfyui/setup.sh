#!/usr/bin/env bash
# 建反向软链:ComfyUI 的 output / workflows 指向本项目 → 出图与工作流直接进项目仓。
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PROJECT="${COMFY_PROJECT:-$(basename "$ROOT")}"
COMFY="${COMFYUI_HOME:-$HOME/Coding/Hub/ComfyUI}"
[[ -d "$COMFY" ]] || { echo "✗ ComfyUI 不在 $COMFY,用 COMFYUI_HOME 指定"; exit 1; }
mkdir -p "$ROOT/assets" "$ROOT/comfy-workflows"
mkdir -p "$COMFY/output/projects" "$COMFY/user/default/workflows/projects"
ln -sfn "$ROOT/assets" "$COMFY/output/projects/$PROJECT"
ln -sfn "$ROOT/comfy-workflows" "$COMFY/user/default/workflows/projects/$PROJECT"
echo "✓ 反向软链建好($PROJECT):"
echo "  $COMFY/output/projects/$PROJECT → $ROOT/assets"
echo "  $COMFY/user/default/workflows/projects/$PROJECT → $ROOT/comfy-workflows"
