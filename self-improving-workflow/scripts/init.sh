#!/usr/bin/env bash
# init.sh — 初始化 .claude/ 工作流配置
# 用法：bash init.sh <tier> [tech_stack] [compliance] [project_root]
#   tier: minimal | standard | full
#   tech_stack: java | python | node | vue | react | monorepo | other
#   compliance: none | govt | fintech | healthcare | privacy
set -euo pipefail

TIER="${1:?Usage: init.sh <tier> [tech_stack] [compliance] [project_root]}"
TECH_STACK="${2:-other}"
COMPLIANCE="${3:-none}"
ROOT="${4:-$(pwd)}"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATES_DIR="$SKILL_DIR/templates"

cd "$ROOT"

if [[ ! "$TIER" =~ ^(minimal|standard|full)$ ]]; then
    echo "Error: tier must be one of: minimal, standard, full" >&2
    exit 1
fi

# 项目名 = 当前目录名
PROJECT_NAME=$(basename "$ROOT")
CREATED_DATE=$(date +%Y-%m-%d)

# 计数器
CREATED=0
SKIPPED=0
TEMPLATES_WRITTEN=0

# render_template <source_template> <target_path>
# 渲染模板：替换 {{VAR}}，跳过已存在的目标文件
render_template() {
    local src="$1"
    local dst="$2"
    local target_dir
    target_dir=$(dirname "$dst")

    mkdir -p "$target_dir"

    if [[ -e "$dst" ]]; then
        # CLAUDE.md 例外：写 .skill-template 旁置
        if [[ "$(basename "$dst")" == "CLAUDE.md" ]]; then
            local companion="${dst}.skill-template"
            sed \
                -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
                -e "s|{{PROJECT_TYPE}}|$TIER|g" \
                -e "s|{{TECH_STACK}}|$TECH_STACK|g" \
                -e "s|{{PROJECT_SCALE}}|$TIER tier|g" \
                -e "s|{{CREATED_DATE}}|$CREATED_DATE|g" \
                -e "s|{{TIER}}|$TIER|g" \
                -e "s|{{COMPLIANCE_PRESET}}|$COMPLIANCE|g" \
                "$src" > "$companion"
            echo "✓ $dst exists, wrote ${companion##$ROOT/} for reference"
            TEMPLATES_WRITTEN=$(( TEMPLATES_WRITTEN + 1 ))
        else
            echo "✓ ${dst##$ROOT/} exists, skipped"
        fi
        SKIPPED=$(( SKIPPED + 1 ))
        return
    fi

    sed \
        -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" \
        -e "s|{{PROJECT_TYPE}}|$TIER|g" \
        -e "s|{{TECH_STACK}}|$TECH_STACK|g" \
        -e "s|{{PROJECT_SCALE}}|$TIER tier|g" \
        -e "s|{{CREATED_DATE}}|$CREATED_DATE|g" \
        -e "s|{{TIER}}|$TIER|g" \
        -e "s|{{COMPLIANCE_PRESET}}|$COMPLIANCE|g" \
        "$src" > "$dst"
    echo "✗ ${dst##$ROOT/} created"
    CREATED=$(( CREATED + 1 ))
}

# install_tier <tier_name>
# 把 templates/<tier>/ 下所有 .template 文件渲染到 .claude/ 对应位置
install_tier() {
    local tier_name="$1"
    local src_root="$TEMPLATES_DIR/$tier_name"

    if [[ ! -d "$src_root" ]]; then
        return
    fi

    # 找所有 .template 文件
    while IFS= read -r template_file; do
        # 计算相对路径并去掉 .template 后缀
        local rel_path="${template_file#$src_root/}"
        local target_path=".claude/${rel_path%.template}"
        render_template "$template_file" "$target_path"
    done < <(find "$src_root" -type f -name '*.template')
}

echo "📦 Installing self-improving-workflow ($TIER tier) into $ROOT"
echo ""

# 按档位累加：full 包含 standard 包含 minimal
case "$TIER" in
    minimal)
        install_tier minimal
        ;;
    standard)
        install_tier minimal
        install_tier standard
        ;;
    full)
        install_tier minimal
        install_tier standard
        install_tier full
        ;;
esac

# 创建 episodic / working 目录的 .gitkeep
mkdir -p .claude/memory/episodic
[[ -e .claude/memory/episodic/.gitkeep ]] || touch .claude/memory/episodic/.gitkeep
if [[ "$TIER" == "full" ]]; then
    mkdir -p .claude/memory/working
    [[ -e .claude/memory/working/.gitkeep ]] || touch .claude/memory/working/.gitkeep
fi

# 写 .workflow-tier 标记
echo "$TIER" > .claude/.workflow-tier

# .gitignore patch（幂等）
if [[ -f .gitignore ]]; then
    if grep -q '^\.claude/$' .gitignore 2>/dev/null; then
        echo ""
        echo "⚠️  WARNING: .gitignore contains '.claude/' which ignores the entire dir."
        echo "   This skill assumes .claude/ should be git-tracked (except memory subdirs)."
        echo "   Manually remove '.claude/' line and add the granular pattern below:"
        echo ""
        echo "   # Claude — project config tracked, ignore private/temp data"
        echo "   .claude/settings.local.json"
        echo "   .claude/memory/episodic/"
        echo "   .claude/memory/working/"
        echo ""
    elif ! grep -q '\.claude/memory/episodic/' .gitignore 2>/dev/null; then
        cat >> .gitignore <<'EOF'

# Claude — project config tracked, ignore private/temp data
.claude/settings.local.json
.claude/memory/episodic/
.claude/memory/working/
EOF
        echo "✗ .gitignore patched"
        CREATED=$(( CREATED + 1 ))
    fi
fi

echo ""
echo "✅ Done. Tier: $TIER"
echo "   Created: $CREATED files"
echo "   Skipped: $SKIPPED existing files"
if (( TEMPLATES_WRITTEN > 0 )); then
    echo "   Reference templates written: $TEMPLATES_WRITTEN (.skill-template)"
fi
echo ""
echo "Next steps:"
echo "  1. Read .claude/CLAUDE.md (or CLAUDE.md.skill-template if you had one)"
echo "  2. Try /self-improve to capture your first lesson"
if [[ "$TIER" != "minimal" ]]; then
    echo "  3. Use /phase-start <name> for your next phase"
fi
