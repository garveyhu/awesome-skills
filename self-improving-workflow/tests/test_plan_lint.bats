#!/usr/bin/env bats

SKILL_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
LINT="$SKILL_DIR/scripts/plan_lint.sh"
F="$SKILL_DIR/tests/fixtures/plans"

@test "lint passes valid plan" {
  run bash "$LINT" "$F/valid_minimal.json"
  [ "$status" -eq 0 ]
}

@test "lint rejects slice missing user_value" {
  run bash "$LINT" "$F/invalid_slice_no_user_value.json"
  [ "$status" -ne 0 ]
}

@test "lint rejects task action not starting with verb" {
  run bash "$LINT" "$F/invalid_task_action_not_verb.json"
  [ "$status" -ne 0 ]
}

@test "lint exits 2 if no arg given" {
  run bash "$LINT"
  [ "$status" -eq 2 ]
}

@test "lint passes valid strict-mode plan" {
  run bash "$LINT" "$F/valid_strict_mode.json"
  [ "$status" -eq 0 ]
}

@test "lint rejects bogus mode value" {
  run bash "$LINT" "$F/invalid_bad_mode.json"
  [ "$status" -ne 0 ]
  [[ "$output" == *"meta.mode invalid"* ]]
}

@test "lint passes plan with 5 phases (no upper bound)" {
  run bash "$LINT" "$F/valid_5phases_with_recovery.json"
  [ "$status" -eq 0 ]
}

@test "lint passes phase with 6 slices (no upper bound)" {
  run bash "$LINT" "$F/valid_recovery_with_6_slices.json"
  [ "$status" -eq 0 ]
}

@test "lint rejects more than one recovery phase" {
  run bash "$LINT" "$F/invalid_two_recovery_phases.json"
  [ "$status" -ne 0 ]
  [[ "$output" == *"more than one recovery phase"* ]]
}

@test "lint passes the recovery-phase fixture from Task 2" {
  run bash "$LINT" "$F/valid_with_recovery_phase.json"
  [ "$status" -eq 0 ]
}

@test "lint rejects recovery phase with 0 slices" {
  run bash "$LINT" "$F/invalid_recovery_zero_slices.json"
  [ "$status" -ne 0 ]
  [[ "$output" == *"slices count 0"* || "$output" == *"slices count"* ]]
}
