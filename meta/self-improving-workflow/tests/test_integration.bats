#!/usr/bin/env bats

SKILL_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"

setup() {
  TMP=$(mktemp -d)
  cd "$TMP"
  git init -q
}

teardown() {
  rm -rf "$TMP"
}

@test "init produces a layout that passes plan_lint on a synthetic plan" {
  bash "$SKILL_DIR/scripts/init.sh" "$TMP"

  # Drop a synthetic valid plan into state (overwrite the empty {} init produced)
  cp "$SKILL_DIR/tests/fixtures/plans/valid_minimal.json" .claude/state/plan.json

  run bash "$SKILL_DIR/scripts/plan_lint.sh" .claude/state/plan.json
  [ "$status" -eq 0 ]
}

@test "guard blocks an irreversible op even from inside a freshly inited project" {
  bash "$SKILL_DIR/scripts/init.sh" "$TMP"
  run bash "$SKILL_DIR/scripts/guard.sh" "git push --force origin main"
  [ "$status" -eq 1 ]
}

@test "crystallize promotes a 3-occurrence pattern end-to-end" {
  bash "$SKILL_DIR/scripts/init.sh" "$TMP"

  # Inject 3 episodics with same 2-seg fingerprint
  jq -c '.[]' "$SKILL_DIR/tests/fixtures/memory/episodic_3x_boundary.json" | while IFS= read -r ep; do
    id=$(echo "$ep" | jq -r '.id')
    echo "$ep" > ".claude/memory/episodic/$id.json"
  done

  run bash "$SKILL_DIR/scripts/crystallize.sh" .claude
  [ "$status" -eq 0 ]
  grep -q "boundary:null-input" .claude/rules/dev-lessons.md
}

@test "init twice + crystallize twice is fully idempotent" {
  bash "$SKILL_DIR/scripts/init.sh" "$TMP"
  bash "$SKILL_DIR/scripts/init.sh" "$TMP"

  jq -c '.[]' "$SKILL_DIR/tests/fixtures/memory/episodic_3x_boundary.json" | while IFS= read -r ep; do
    id=$(echo "$ep" | jq -r '.id')
    echo "$ep" > ".claude/memory/episodic/$id.json"
  done

  bash "$SKILL_DIR/scripts/crystallize.sh" .claude
  bash "$SKILL_DIR/scripts/crystallize.sh" .claude
  count=$(grep -c "boundary:null-input" .claude/rules/dev-lessons.md || true)
  [ "$count" -eq 1 ]
}
