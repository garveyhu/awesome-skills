#!/usr/bin/env bats

SKILL_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
GUARD="$SKILL_DIR/scripts/guard.sh"

@test "allows ls" {
  run bash "$GUARD" "ls -la /tmp"
  [ "$status" -eq 0 ]
}

@test "allows git status" {
  run bash "$GUARD" "git status"
  [ "$status" -eq 0 ]
}

@test "blocks rm -rf outside cwd" {
  run bash "$GUARD" "rm -rf /Users/foo/bar"
  [ "$status" -eq 1 ]
  [[ "$output" == *"data-loss"* ]]
}

@test "blocks git push --force" {
  run bash "$GUARD" "git push --force origin main"
  [ "$status" -eq 1 ]
  [[ "$output" == *"remote-irreversible"* ]]
}

@test "blocks git push -f" {
  run bash "$GUARD" "git push -f origin main"
  [ "$status" -eq 1 ]
}

@test "blocks git reset --hard" {
  run bash "$GUARD" "git reset --hard HEAD~3"
  [ "$status" -eq 1 ]
  [[ "$output" == *"data-loss"* ]]
}

@test "blocks dropping db table" {
  run bash "$GUARD" "psql -c 'DROP TABLE users'"
  [ "$status" -eq 1 ]
}

@test "blocks editing .env" {
  run bash "$GUARD" "vim .env"
  [ "$status" -eq 1 ]
  [[ "$output" == *"credentials"* ]]
}

@test "blocks kill -9" {
  run bash "$GUARD" "kill -9 1234"
  [ "$status" -eq 1 ]
  [[ "$output" == *"process"* ]]
}

@test "blocks curl webhook" {
  run bash "$GUARD" "curl -X POST https://hooks.slack.com/services/xxx"
  [ "$status" -eq 1 ]
  [[ "$output" == *"shared-comms"* ]]
}

@test "exits 2 if no arg" {
  run bash "$GUARD"
  [ "$status" -eq 2 ]
}
