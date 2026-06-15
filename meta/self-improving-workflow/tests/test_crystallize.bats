#!/usr/bin/env bats

SKILL_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
CRYS="$SKILL_DIR/scripts/crystallize.sh"
F="$SKILL_DIR/tests/fixtures/memory"

setup() {
  TMP=$(mktemp -d)
  mkdir -p "$TMP/.claude/memory/episodic" "$TMP/.claude/rules"
  cp "$F/empty_semantic.json" "$TMP/.claude/memory/semantic-patterns.json"
  : > "$TMP/.claude/rules/dev-lessons.md"
}

teardown() {
  rm -rf "$TMP"
}

@test "promotes pattern at 3 occurrences" {
  jq -c '.[]' "$F/episodic_3x_boundary.json" | while IFS= read -r ep; do
    id=$(echo "$ep" | jq -r '.id')
    echo "$ep" > "$TMP/.claude/memory/episodic/$id.json"
  done

  run bash "$CRYS" "$TMP/.claude"
  [ "$status" -eq 0 ]

  occ=$(jq '.patterns[0].occurrences' "$TMP/.claude/memory/semantic-patterns.json")
  [ "$occ" -eq 3 ]

  grep -q "boundary:null-input" "$TMP/.claude/rules/dev-lessons.md"

  promoted=$(jq '.patterns[0].promoted_to_rule' "$TMP/.claude/memory/semantic-patterns.json")
  [ "$promoted" = "true" ]
}

@test "does NOT promote at 2 occurrences" {
  jq -c '.[]' "$F/episodic_2x_only.json" | while IFS= read -r ep; do
    id=$(echo "$ep" | jq -r '.id')
    echo "$ep" > "$TMP/.claude/memory/episodic/$id.json"
  done

  run bash "$CRYS" "$TMP/.claude"
  [ "$status" -eq 0 ]

  ! grep -q "boundary:null-input" "$TMP/.claude/rules/dev-lessons.md"

  occ=$(jq '.patterns[0].occurrences' "$TMP/.claude/memory/semantic-patterns.json")
  [ "$occ" -eq 2 ]
}

@test "is idempotent — re-run does not double-append" {
  jq -c '.[]' "$F/episodic_3x_boundary.json" | while IFS= read -r ep; do
    id=$(echo "$ep" | jq -r '.id')
    echo "$ep" > "$TMP/.claude/memory/episodic/$id.json"
  done
  bash "$CRYS" "$TMP/.claude"
  bash "$CRYS" "$TMP/.claude"
  count=$(grep -c "boundary:null-input" "$TMP/.claude/rules/dev-lessons.md" || true)
  [ "$count" -eq 1 ]
}

@test "exits 2 if claude dir missing" {
  run bash "$CRYS" "/nonexistent/path"
  [ "$status" -eq 2 ]
}
