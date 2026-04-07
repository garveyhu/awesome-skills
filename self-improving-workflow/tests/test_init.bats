#!/usr/bin/env bats

SKILL_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
INIT="$SKILL_DIR/scripts/init.sh"

setup() {
  TMP=$(mktemp -d)
  cd "$TMP"
  git init -q
}

teardown() {
  rm -rf "$TMP"
}

@test "creates per-project layout (no commands/agents — those live at skill)" {
  bash "$INIT" "$TMP"
  [ -f .claude/CLAUDE.md ]
  [ -f .claude/rules/autonomy-stops.md ]
  [ -f .claude/rules/dev-lessons.md ]
  [ -f .claude/state/plan.schema.json ]
  [ -f .claude/state/plan.json ]
  [ -f .claude/state/decisions.jsonl ]
  [ -d .claude/state/archive ]
  [ -d .claude/memory/episodic ]
  [ -d .claude/memory/working ]
  [ -f .claude/memory/semantic-patterns.json ]
  [ -f .claude/memory/README.md ]
  # Per-project layout deliberately does NOT include commands/ or agents/
  [ ! -d .claude/commands ]
  [ ! -d .claude/agents ]
}

@test "is idempotent — second run touches nothing" {
  bash "$INIT" "$TMP"
  echo "MARKER" > .claude/rules/dev-lessons.md
  bash "$INIT" "$TMP"
  grep -q "MARKER" .claude/rules/dev-lessons.md
}

@test "patches .gitignore idempotently" {
  bash "$INIT" "$TMP"
  bash "$INIT" "$TMP"
  count=$(grep -c "^\.claude/memory/episodic/$" .gitignore)
  [ "$count" -eq 1 ]
}

@test "writes .skill-template companion if CLAUDE.md exists" {
  mkdir -p .claude
  echo "# pre-existing" > .claude/CLAUDE.md
  bash "$INIT" "$TMP"
  [ -f .claude/CLAUDE.md.skill-template ]
  grep -q "pre-existing" .claude/CLAUDE.md
}

@test "rejects non-directory arg" {
  run bash "$INIT" "/nonexistent/xyz"
  [ "$status" -ne 0 ]
}
