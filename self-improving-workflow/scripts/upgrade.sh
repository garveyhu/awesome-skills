#!/usr/bin/env bash
# upgrade.sh — 升档当前项目的 .claude/ 工作流
# 用法：bash upgrade.sh <target_tier> [project_root]
set -euo pipefail

TARGET="${1:?Usage: upgrade.sh <target_tier> [project_root]}"
ROOT="${2:-$(pwd)}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATES_DIR="$SKILL_DIR/templates"

cd "$ROOT"

if [[ ! "$TARGET" =~ ^(minimal|standard|full)$ ]]; then
    echo "Error: target tier must be one of: minimal, standard, full" >&2
    exit 1
fi

# 读取当前档位
CURRENT="none"
if [[ -f .claude/.workflow-tier ]]; then
    CURRENT=$(cat .claude/.workflow-tier)
fi

# 档位排序
tier_rank() {
    case "$1" in
        none) echo 0 ;;
        minimal) echo 1 ;;
        standard) echo 2 ;;
        full) echo 3 ;;
    esac
}

CURRENT_RANK=$(tier_rank "$CURRENT")
TARGET_RANK=$(tier_rank "$TARGET")

if (( TARGET_RANK <= CURRENT_RANK )); then
    echo "Error: target tier ($TARGET) must be higher than current tier ($CURRENT)." >&2
    echo "Downgrades are not supported (would risk deleting user data)." >&2
    exit 1
fi

echo "📦 Upgrading workflow: $CURRENT → $TARGET"
echo ""

# 收集需要安装的 tier 增量
TIERS_TO_ADD=()
if (( CURRENT_RANK < 1 && TARGET_RANK >= 1 )); then TIERS_TO_ADD+=(minimal); fi
if (( CURRENT_RANK < 2 && TARGET_RANK >= 2 )); then TIERS_TO_ADD+=(standard); fi
if (( CURRENT_RANK < 3 && TARGET_RANK >= 3 )); then TIERS_TO_ADD+=(full); fi

CREATED=0
SKIPPED=0
DIFFERED=0

prompt_diff() {
    local existing="$1"
    local template="$2"
    local rel="${existing##$ROOT/}"

    echo ""
    echo "⚠️  $rel exists with different content from new tier template."
    echo "   Options: [k]eep existing  [n]ew template  [d]iff  [s]kip"
    while true; do
        read -r -p "   Choice: " choice
        case "$choice" in
            k|K) echo "   → kept existing"; SKIPPED=$(( SKIPPED + 1 )); break ;;
            n|N) cp "$template" "$existing"; echo "   → replaced with new"; CREATED=$(( CREATED + 1 )); break ;;
            d|D) diff -u "$existing" "$template" || true ;;
            s|S) echo "   → skipped"; SKIPPED=$(( SKIPPED + 1 )); break ;;
            *) echo "   Invalid. Use k/n/d/s." ;;
        esac
    done
}

install_tier_upgrade() {
    local tier_name="$1"
    local src_root="$TEMPLATES_DIR/$tier_name"
    [[ -d "$src_root" ]] || return

    while IFS= read -r template_file; do
        local rel_path="${template_file#$src_root/}"
        local target_path=".claude/${rel_path%.template}"

        mkdir -p "$(dirname "$target_path")"

        if [[ ! -e "$target_path" ]]; then
            cp "$template_file" "$target_path"
            echo "✗ ${target_path##$ROOT/} created"
            CREATED=$(( CREATED + 1 ))
        elif ! diff -q "$template_file" "$target_path" >/dev/null 2>&1; then
            DIFFERED=$(( DIFFERED + 1 ))
            prompt_diff "$target_path" "$template_file"
        else
            SKIPPED=$(( SKIPPED + 1 ))
        fi
    done < <(find "$src_root" -type f -name '*.template')
}

for tier in "${TIERS_TO_ADD[@]}"; do
    echo "Adding $tier tier files..."
    install_tier_upgrade "$tier"
done

# 更新 tier marker
echo "$TARGET" > .claude/.workflow-tier

echo ""
echo "✅ Upgrade complete: $CURRENT → $TARGET"
echo "   Created: $CREATED files"
echo "   Skipped: $SKIPPED files (unchanged or kept by user)"
if (( DIFFERED > 0 )); then
    echo "   Diffs handled: $DIFFERED"
fi
