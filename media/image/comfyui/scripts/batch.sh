#!/usr/bin/env bash
# 通用 ComfyUI 批量生图入口(CLI)。读 <资产目录> 下所有 assets.json,照计划出图。
#
# 用法:
#   batch.sh <资产目录> [--workflows-dir DIR] [--project NAME] [--variants N]
#            [--only props,ui] [--redo] [--with-chars] [--timeout 1800] [--dry-run]
# 例:
#   先看计划(不生成):  batch.sh ~/Coding/Archer/quiver/assets --project quiver --dry-run
#   真跑(睡前):        batch.sh ~/Coding/Archer/quiver/assets --project quiver \
#                          --workflows-dir ~/Coding/Archer/quiver/comfy-workflows --variants 3
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-$HOME/.venvs/current/bin/python}"
exec "$PYTHON" "$HERE/batch/run.py" "$@"
