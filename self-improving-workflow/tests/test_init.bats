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

@test "creates expected layout" {
  bash "$INIT" "$TMP"
  [ -f .claude/CLAUDE.md ]
  [ -f .claude/commands/run.md ]
  [ -f .claude/commands/plan.md ]
  [ -f .claude/commands/review.md ]
  [ -f .claude/commands/learn.md ]
  [ -f .claude/commands/resume.md ]
  [ -f .claude/agents/planner-critic.md ]
  [ -f .claude/agents/implementation-reviewer.md ]
  [ -f .claude/agents/requirement-auditor.md ]
  [ -f .claude/agents/integration-checker.md ]
  [ -f .claude/rules/autonomy-stops.md ]
  [ -f .claude/rules/dev-lessons.md ]
  [ -f .claude/state/plan.schema.json ]
  [ -f .claude/state/plan.json ]
  [ -f .claude/state/decisions.jsonl ]
  [ -d .claude/memory/episodic ]
  [ -f .claude/memory/semantic-patterns.json ]
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
