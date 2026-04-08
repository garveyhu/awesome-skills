#!/usr/bin/env bats

SKILL_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
SCHEMA="$SKILL_DIR/seeds/plan.schema.json"

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

@test "schema accepts meta.mode = strict" {
  run jq -e '.meta.mode == "strict"' "$SKILL_DIR/tests/fixtures/plans/valid_strict_mode.json"
  [ "$status" -eq 0 ]
}

@test "schema definition declares meta.mode field" {
  run jq -e '.properties.meta.properties.mode' "$SKILL_DIR/seeds/plan.schema.json"
  [ "$status" -eq 0 ]
}

@test "schema mode field has the right enum" {
  run jq -e '.properties.meta.properties.mode.enum == ["normal","strict"]' "$SKILL_DIR/seeds/plan.schema.json"
  [ "$status" -eq 0 ]
}

@test "schema definition declares phase.kind field" {
  run jq -e '.definitions.phase.properties.kind' "$SKILL_DIR/seeds/plan.schema.json"
  [ "$status" -eq 0 ]
}

@test "phase.kind enum is main and recovery" {
  run jq -e '.definitions.phase.properties.kind.enum == ["main","recovery"]' "$SKILL_DIR/seeds/plan.schema.json"
  [ "$status" -eq 0 ]
}
