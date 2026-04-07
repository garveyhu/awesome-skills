#!/usr/bin/env bats

SKILL_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
SCHEMA="$SKILL_DIR/templates/state/plan.schema.json"

@test "plan.schema.json exists" {
  [ -f "$SCHEMA" ]
}

@test "plan.schema.json is valid JSON" {
  jq empty "$SCHEMA"
}

@test "schema declares draft-07" {
  run jq -r '."$schema"' "$SCHEMA"
  [[ "$output" == *"draft-07"* ]]
}
