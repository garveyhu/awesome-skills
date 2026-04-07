#!/usr/bin/env bash
# detect.sh — 探测当前项目状态，给出推荐档位
# 用法：bash detect.sh [project_root]
# 输出：JSON 格式的探测结果（供 init.sh 解析）
set -euo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

# 1. 是否已有 .claude/
HAS_CLAUDE_DIR=0
EXISTING_FILES=0
EXISTING_TIER="none"
if [[ -d .claude ]]; then
    HAS_CLAUDE_DIR=1
    EXISTING_FILES=$(find .claude -type f 2>/dev/null | wc -l | tr -d ' ')
    if [[ -f .claude/.workflow-tier ]]; then
        EXISTING_TIER=$(cat .claude/.workflow-tier 2>/dev/null || echo "none")
    fi
fi

# 2. 项目体征评分
SCORE=0

# 顶层目录数（排除隐藏）
TOP_DIRS=$(find . -maxdepth 1 -type d ! -name '.*' ! -name '.' 2>/dev/null | wc -l | tr -d ' ')
DIR_SCORE=$(( TOP_DIRS > 5 ? 5 : TOP_DIRS ))
SCORE=$(( SCORE + DIR_SCORE ))

# 多模块构建工具
if [[ -f pom.xml ]] && grep -q '<modules>' pom.xml 2>/dev/null; then
    SCORE=$(( SCORE + 2 ))
fi
if [[ -f settings.gradle ]] || [[ -f settings.gradle.kts ]]; then
    SCORE=$(( SCORE + 2 ))
fi
if [[ -f pyproject.toml ]] && grep -q 'workspace' pyproject.toml 2>/dev/null; then
    SCORE=$(( SCORE + 2 ))
fi
if [[ -f pnpm-workspace.yaml ]] || [[ -f lerna.json ]]; then
    SCORE=$(( SCORE + 2 ))
fi

# git commit 数
if [[ -d .git ]]; then
    COMMITS=$(git log --oneline 2>/dev/null | wc -l | tr -d ' ')
    COMMIT_SCORE=$(( COMMITS / 10 ))
    COMMIT_SCORE=$(( COMMIT_SCORE > 5 ? 5 : COMMIT_SCORE ))
    SCORE=$(( SCORE + COMMIT_SCORE ))

    # 贡献者数
    CONTRIBUTORS=$(git shortlog -sn 2>/dev/null | wc -l | tr -d ' ')
    CONTRIB_SCORE=$(( CONTRIBUTORS * 2 ))
    CONTRIB_SCORE=$(( CONTRIB_SCORE > 6 ? 6 : CONTRIB_SCORE ))
    SCORE=$(( SCORE + CONTRIB_SCORE ))
fi

# CI 配置
if [[ -d .github/workflows ]] || [[ -f .gitlab-ci.yml ]] || [[ -f Jenkinsfile ]]; then
    SCORE=$(( SCORE + 2 ))
fi

# 3. 推荐档位
RECOMMENDED="minimal"
if (( SCORE >= 4 && SCORE < 10 )); then
    RECOMMENDED="standard"
elif (( SCORE >= 10 )); then
    RECOMMENDED="full"
fi

# 4. 输出 JSON
cat <<EOF
{
  "project_root": "$ROOT",
  "has_claude_dir": $HAS_CLAUDE_DIR,
  "existing_files": $EXISTING_FILES,
  "existing_tier": "$EXISTING_TIER",
  "score": $SCORE,
  "recommended_tier": "$RECOMMENDED",
  "signals": {
    "top_dirs": $TOP_DIRS,
    "is_multi_module": $(( DIR_SCORE > 1 ? 1 : 0 )),
    "git_commits": ${COMMITS:-0},
    "contributors": ${CONTRIBUTORS:-0}
  }
}
EOF
