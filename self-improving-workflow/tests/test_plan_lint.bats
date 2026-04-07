#!/usr/bin/env bats

SKILL_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
LINT="$SKILL_DIR/scripts/plan_lint.sh"
F="$SKILL_DIR/tests/fixtures/plans"

@test "lint passes valid plan" {
  run bash "$LINT" "$F/valid_minimal.json"
  [ "$status" -eq 0 ]
}

@test "lint rejects too many phases" {
  run bash "$LINT" "$F/invalid_too_many_phases.json"
  [ "$status" -ne 0 ]
}

@test "lint rejects slice missing user_value" {
  run bash "$LINT" "$F/invalid_slice_no_user_value.json"
  [ "$status" -ne 0 ]
}

@test "lint rejects task action not starting with verb" {
  run bash "$LINT" "$F/invalid_task_action_not_verb.json"
  [ "$status" -ne 0 ]
}

@test "lint rejects phase with too many slices" {
  run bash "$LINT" "$F/invalid_phase_too_many_slices.json"
  [ "$status" -ne 0 ]
}

@test "lint exits 2 if no arg given" {
  run bash "$LINT"
  [ "$status" -eq 2 ]
}
