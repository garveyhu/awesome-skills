#!/usr/bin/env bash
# init.sh — scaffold a project's .claude/ for self-improving-workflow.
# Usage: init.sh [project_root]
#
# What this DOES seed in the project's .claude/:
#   - commands/  (slash commands — copied from skill, so Claude Code can find them)
#   - agents/    (reviewer subagents — copied from skill, so Claude Code can find them)
#   - state/ (plan.json, decisions.jsonl, plan.schema.json, archive/)
#   - memory/ (episodic/, working/, semantic-patterns.json, README.md)
#   - rules/ (autonomy-stops.md, dev-lessons.md) — copied from skill seeds
#   - CLAUDE.md — copied from skill seeds ONLY if no CLAUDE.md exists yet
#   - .gitignore patch
#
# What this does NOT seed (stays in the skill repo, called by absolute path):
#   - scripts/   (init/guard/plan_lint/crystallize)
#
# Idempotent. Existing files are skipped (write-once).
# Re-running picks up new commands/agents added to the skill.
set -euo pipefail

ROOT="${1:-$(pwd)}"
if [[ ! -d "$ROOT" ]]; then
  echo "ERROR: $ROOT is not a directory" >&2
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SEEDS="$SKILL_DIR/seeds"

cd "$ROOT"

CREATED=0
SKIPPED=0

copy_once() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [[ -e "$dst" ]]; then
    SKIPPED=$((SKIPPED+1))
    echo "  - $dst exists, skip"
    return
  fi
  cp "$src" "$dst"
  CREATED=$((CREATED+1))
  echo "  + $dst"
}

# Mirror an entire directory from skill into .claude/, file-by-file (write-once per file).
# New files added to the skill in future versions get picked up on re-run.
mirror_dir() {
  local src_dir="$1" dst_dir="$2"
  [[ -d "$src_dir" ]] || return 0
  mkdir -p "$dst_dir"
  local f rel
  while IFS= read -r -d '' f; do
    rel="${f#$src_dir/}"
    copy_once "$f" "$dst_dir/$rel"
  done < <(find "$src_dir" -type f -print0)
}

# CLAUDE.md — write-once. If the project already has one, leave it alone.
copy_once "$SEEDS/CLAUDE.md" ".claude/CLAUDE.md"

# commands/ and agents/ — must live in .claude/ for Claude Code to discover them.
mirror_dir "$SKILL_DIR/commands" ".claude/commands"
mirror_dir "$SKILL_DIR/agents" ".claude/agents"

# rules
copy_once "$SEEDS/rules/autonomy-stops.md" ".claude/rules/autonomy-stops.md"
copy_once "$SEEDS/rules/dev-lessons.md" ".claude/rules/dev-lessons.md"

# state
copy_once "$SEEDS/plan.schema.json" ".claude/state/plan.schema.json"
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
copy_once "$SEEDS/memory/README.md" ".claude/memory/README.md"
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
