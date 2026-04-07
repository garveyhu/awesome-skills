#!/usr/bin/env bash
# init.sh — scaffold .claude/ for self-improving-workflow (no tier/stack/compliance)
# Usage: init.sh [project_root]
# Idempotent: existing files are skipped (write-once); CLAUDE.md exception writes a .skill-template companion.
set -euo pipefail

ROOT="${1:-$(pwd)}"
if [[ ! -d "$ROOT" ]]; then
  echo "ERROR: $ROOT is not a directory" >&2
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TPL="$SKILL_DIR/templates"

cd "$ROOT"

CREATED=0
SKIPPED=0

copy_once() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [[ -e "$dst" ]]; then
    if [[ "$(basename "$dst")" == "CLAUDE.md" ]]; then
      cp "$src" "${dst}.skill-template"
      echo "  ~ $dst exists; wrote ${dst}.skill-template"
    else
      SKIPPED=$((SKIPPED+1))
      echo "  - $dst exists, skip"
    fi
    return
  fi
  cp "$src" "$dst"
  CREATED=$((CREATED+1))
  echo "  + $dst"
}

# CLAUDE.md
copy_once "$TPL/CLAUDE.md.template" ".claude/CLAUDE.md"

# commands
for c in run plan review learn resume; do
  copy_once "$TPL/commands/${c}.md.template" ".claude/commands/${c}.md"
done

# agents
for a in planner-critic implementation-reviewer requirement-auditor integration-checker; do
  copy_once "$TPL/agents/${a}.md.template" ".claude/agents/${a}.md"
done

# rules
copy_once "$TPL/rules/autonomy-stops.md.template" ".claude/rules/autonomy-stops.md"
copy_once "$TPL/rules/dev-lessons.md.template" ".claude/rules/dev-lessons.md"

# state
copy_once "$TPL/state/plan.schema.json" ".claude/state/plan.schema.json"
if [[ ! -f .claude/state/plan.json ]]; then
  echo '{}' > .claude/state/plan.json
  CREATED=$((CREATED+1))
  echo "  + .claude/state/plan.json"
fi
if [[ ! -f .claude/state/decisions.jsonl ]]; then
  : > .claude/state/decisions.jsonl
  CREATED=$((CREATED+1))
  echo "  + .claude/state/decisions.jsonl"
fi
mkdir -p .claude/state/archive

# memory
copy_once "$TPL/memory/README.md.template" ".claude/memory/README.md"
mkdir -p .claude/memory/episodic .claude/memory/working
if [[ ! -f .claude/memory/semantic-patterns.json ]]; then
  echo '{"patterns":[]}' > .claude/memory/semantic-patterns.json
  CREATED=$((CREATED+1))
  echo "  + .claude/memory/semantic-patterns.json"
fi

# gitignore patch (idempotent)
GI=".gitignore"
touch "$GI"
for line in ".claude/memory/episodic/" ".claude/memory/working/" ".claude/state/working/"; do
  grep -qxF "$line" "$GI" || echo "$line" >> "$GI"
done

echo "init: created=$CREATED skipped=$SKIPPED"
