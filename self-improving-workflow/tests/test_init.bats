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

@test "creates per-project layout including commands/agents" {
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
  # Claude Code requires commands/ and agents/ to live in .claude/ to discover them.
  [ -f .claude/commands/run.md ]
  [ -f .claude/commands/run-strict.md ]
  [ -f .claude/commands/plan.md ]
  [ -f .claude/commands/review.md ]
  [ -f .claude/commands/learn.md ]
  [ -f .claude/commands/resume.md ]
  [ -f .claude/agents/planner-critic.md ]
  [ -f .claude/agents/implementation-reviewer.md ]
  [ -f .claude/agents/requirement-auditor.md ]
  [ -f .claude/agents/integration-checker.md ]
  [ -f .claude/agents/topic-auditor.md ]
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

@test "leaves existing CLAUDE.md untouched and writes no sidecar" {
  mkdir -p .claude
  echo "# pre-existing" > .claude/CLAUDE.md
  bash "$INIT" "$TMP"
  grep -q "pre-existing" .claude/CLAUDE.md
  [ ! -f .claude/CLAUDE.md.skill-template ]
}

@test "re-running picks up newly added commands/agents" {
  bash "$INIT" "$TMP"
  rm .claude/commands/run.md
  bash "$INIT" "$TMP"
  [ -f .claude/commands/run.md ]
}

@test "rejects non-directory arg" {
  run bash "$INIT" "/nonexistent/xyz"
  [ "$status" -ne 0 ]
}
