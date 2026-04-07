# Self-Improving-Workflow Skill Refactor Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refactor `~/.agents/skills/self-improving-workflow` from a tier-coupled, tech-stack-flavored scaffold into a universal methodology skill built on two pillars: multi-agent collaborative learning and long-running uninterrupted execution.

**Architecture:** Hybrid Claude-native + script-deterministic. AI parts (planning, reviewing, executing) live in `.claude/commands/*.md` and `.claude/agents/*.md`. State and threshold logic (plan validation, irreversible-op guard, crystallization) live in shell scripts under `scripts/`. State persists in JSON files under `.claude/state/` with strict schema. Single `/run` entrypoint drives the end-to-end loop.

**Tech Stack:** bash, jq (for JSON state mutations), bats (for shell test harness), JSON Schema (Draft-07), Markdown templates. Zero runtime dependencies beyond bash + jq.

**Reference:** [Design doc](./2026-04-07-self-improving-workflow-refactor-design.md)

---

## Conventions

- **Working dir for all paths**: `~/.agents/skills/self-improving-workflow/` unless absolute path given.
- **Test framework**: `bats-core` (install via `brew install bats-core` if missing — **Phase 1 Task 0** verifies).
- **Test fixtures**: under `tests/fixtures/`. Tests under `tests/`.
- **Each task ends in a commit**. Use Conventional Commits style: `feat:`, `refactor:`, `test:`, `chore:`.
- **Skills referenced**: @superpowers:executing-plans, @superpowers:test-driven-development.

---

## Phase 0 — Preflight & Cleanup

### Task 0.1: Verify toolchain & start clean branch

**Files:** none

**Step 1: Check tools**

Run:
```bash
command -v bash && bash --version | head -1
command -v jq && jq --version
command -v bats || echo "bats missing"
```
Expected: bash ≥ 3.2, jq ≥ 1.6, bats present.
If bats missing → `brew install bats-core` (macOS).

**Step 2: Confirm clean tree at parent repo**

Run:
```bash
cd ~/.agents/skills && git status --short
```
Expected: only the new `self-improving-workflow/docs/plans/*` files from brainstorming session as untracked. No staged changes.

**Step 3: Create feature branch on parent repo**

Run:
```bash
cd ~/.agents/skills && git checkout -b refactor/siw-two-pillar
```
Expected: switched to new branch.

**Step 4: Commit the design + plan as starting point**

Run:
```bash
cd ~/.agents/skills && git add self-improving-workflow/docs/plans/
git commit -m "docs(siw): add refactor design and implementation plan"
```

---

### Task 0.2: Snapshot current files-to-delete list

**Files:**
- Create: `self-improving-workflow/docs/plans/_artifacts/old-tree.txt` (audit trail)

**Step 1: List current skill tree**

Run:
```bash
cd ~/.agents/skills/self-improving-workflow && find . -type f -not -path './.git/*' -not -path './docs/plans/*' | sort > docs/plans/_artifacts/old-tree.txt
cat docs/plans/_artifacts/old-tree.txt
```
Expected: ~30 files including `templates/{minimal,standard,full}/`, `references/tier-comparison.md`, `scripts/{detect,upgrade}.sh` etc.

**Step 2: Commit snapshot**

```bash
git add docs/plans/_artifacts/old-tree.txt
git commit -m "chore(siw): snapshot pre-refactor file tree"
```

---

### Task 0.3: Delete obsolete files (single bulk commit)

**Files to delete:**
- `templates/minimal/` (entire dir)
- `templates/standard/` (entire dir)
- `templates/full/` (entire dir)
- `references/tier-comparison.md`
- `references/compliance-presets.md`
- `references/existing-project-guide.md`
- `scripts/upgrade.sh`
- `scripts/detect.sh`

**Step 1: Verify each path exists**

Run:
```bash
cd ~/.agents/skills/self-improving-workflow
for p in templates/minimal templates/standard templates/full \
         references/tier-comparison.md references/compliance-presets.md references/existing-project-guide.md \
         scripts/upgrade.sh scripts/detect.sh; do
  [ -e "$p" ] && echo "FOUND $p" || echo "MISSING $p"
done
```
Expected: all FOUND.

**Step 2: Delete via git rm**

```bash
git rm -r templates/minimal templates/standard templates/full
git rm references/tier-comparison.md references/compliance-presets.md references/existing-project-guide.md
git rm scripts/upgrade.sh scripts/detect.sh
```

**Step 3: Sanity check what remains**

Run: `find . -type f -not -path './.git/*' | sort`
Expected: only `SKILL.md`, `README*.md`, `scripts/init.sh`, `references/`, `docs/plans/...` left.

**Step 4: Commit**

```bash
git commit -m "refactor(siw): remove tier system, stack templates, compliance presets"
```

---

## Phase 1 — Plan Schema + plan_lint.sh (TDD)

### Task 1.1: Write failing test for plan.schema.json existence and validity

**Files:**
- Create: `tests/test_plan_schema.bats`
- Create: `tests/fixtures/plans/.gitkeep`

**Step 1: Write the failing test**

```bash
cat > tests/test_plan_schema.bats <<'BATS'
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
BATS
```

**Step 2: Run test, expect FAIL**

Run: `bats tests/test_plan_schema.bats`
Expected: 3 failing assertions (file does not exist).

**Step 3: Create the schema**

Create `templates/state/plan.schema.json`:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "self-improving-workflow plan",
  "type": "object",
  "required": ["meta", "phases"],
  "additionalProperties": false,
  "properties": {
    "meta": {
      "type": "object",
      "required": ["topic", "created_at", "status"],
      "additionalProperties": false,
      "properties": {
        "topic": {"type": "string", "minLength": 1},
        "created_at": {"type": "string", "format": "date-time"},
        "status": {"enum": ["pending", "in_progress", "done", "blocked"]},
        "current_phase_id": {"type": ["string", "null"]}
      }
    },
    "phases": {
      "type": "array",
      "minItems": 1,
      "maxItems": 4,
      "items": {"$ref": "#/definitions/phase"}
    }
  },
  "definitions": {
    "phase": {
      "type": "object",
      "required": ["id", "title", "goal", "status", "slices"],
      "additionalProperties": false,
      "properties": {
        "id": {"type": "string", "pattern": "^P[0-9]+$"},
        "title": {"type": "string", "minLength": 1},
        "goal": {"type": "string", "minLength": 1},
        "status": {"enum": ["pending", "in_progress", "done", "blocked"]},
        "slices": {
          "type": "array",
          "minItems": 1,
          "maxItems": 5,
          "items": {"$ref": "#/definitions/slice"}
        }
      }
    },
    "slice": {
      "type": "object",
      "required": ["id", "title", "user_value", "acceptance", "status", "tasks"],
      "additionalProperties": false,
      "properties": {
        "id": {"type": "string", "pattern": "^P[0-9]+-S[0-9]+$"},
        "title": {"type": "string", "minLength": 1},
        "user_value": {"type": "string", "minLength": 1},
        "acceptance": {
          "type": "array",
          "minItems": 1,
          "items": {"type": "string", "minLength": 1}
        },
        "status": {"enum": ["pending", "in_progress", "done", "blocked"]},
        "tasks": {
          "type": "array",
          "minItems": 1,
          "maxItems": 7,
          "items": {"$ref": "#/definitions/task"}
        }
      }
    },
    "task": {
      "type": "object",
      "required": ["id", "action", "target", "status"],
      "additionalProperties": false,
      "properties": {
        "id": {"type": "string", "pattern": "^P[0-9]+-S[0-9]+-T[0-9]+$"},
        "action": {
          "type": "string",
          "pattern": "^(Implement|Modify|Add|Remove|Verify|Refactor|Write|Update|Delete|Validate|Generate|Configure|Install|Run|Migrate|Document|实现|修改|添加|删除|验证|重构|编写|更新|配置|安装|运行|迁移)\\b.+"
        },
        "target": {"type": "string", "minLength": 1},
        "status": {"enum": ["pending", "in_progress", "done", "blocked"]},
        "evidence": {"type": ["string", "null"]}
      }
    }
  }
}
```

**Step 4: Run test, expect PASS**

Run: `bats tests/test_plan_schema.bats`
Expected: 3/3 PASS.

**Step 5: Commit**

```bash
git add tests/test_plan_schema.bats tests/fixtures/plans/.gitkeep templates/state/plan.schema.json
git commit -m "feat(siw): add plan.schema.json with strict 3-level tree contract"
```

---

### Task 1.2: Plan-lint test fixtures (valid + invalid samples)

**Files:**
- Create: `tests/fixtures/plans/valid_minimal.json`
- Create: `tests/fixtures/plans/invalid_too_many_phases.json`
- Create: `tests/fixtures/plans/invalid_slice_no_user_value.json`
- Create: `tests/fixtures/plans/invalid_task_action_not_verb.json`
- Create: `tests/fixtures/plans/invalid_phase_too_many_slices.json`

**Step 1: Write a valid minimal plan**

`tests/fixtures/plans/valid_minimal.json`:
```json
{
  "meta": {
    "topic": "test",
    "created_at": "2026-04-07T00:00:00Z",
    "status": "pending",
    "current_phase_id": null
  },
  "phases": [
    {
      "id": "P1",
      "title": "Phase one",
      "goal": "Do the thing",
      "status": "pending",
      "slices": [
        {
          "id": "P1-S1",
          "title": "Slice one",
          "user_value": "User can foo",
          "acceptance": ["foo returns bar"],
          "status": "pending",
          "tasks": [
            {
              "id": "P1-S1-T1",
              "action": "Implement foo function",
              "target": "src/foo.py",
              "status": "pending",
              "evidence": null
            }
          ]
        }
      ]
    }
  ]
}
```

**Step 2: Write 4 invalid fixtures (each violates exactly one rule)**

`invalid_too_many_phases.json`: 5 phases (max 4).
`invalid_slice_no_user_value.json`: same as valid but slice has empty `user_value`.
`invalid_task_action_not_verb.json`: task action starts with "考虑" (not in verb list).
`invalid_phase_too_many_slices.json`: 6 slices in one phase.

(Use the valid one as the base; mutate the offending field.)

**Step 3: Sanity-check fixtures parse as JSON**

Run: `for f in tests/fixtures/plans/*.json; do jq empty "$f" || echo "BAD $f"; done`
Expected: no BAD output.

**Step 4: Commit**

```bash
git add tests/fixtures/plans/
git commit -m "test(siw): add plan-schema fixtures (1 valid + 4 invalid)"
```

---

### Task 1.3: TDD plan_lint.sh

**Files:**
- Create: `tests/test_plan_lint.bats`
- Create: `scripts/plan_lint.sh`

**Step 1: Write the failing test**

```bash
cat > tests/test_plan_lint.bats <<'BATS'
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
  [[ "$output" == *"phases"* ]] || [[ "$output" == *"maxItems"* ]]
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
BATS
```

**Step 2: Run, expect all fail**

Run: `bats tests/test_plan_lint.bats`
Expected: 6 fails.

**Step 3: Implement plan_lint.sh**

```bash
cat > scripts/plan_lint.sh <<'SH'
#!/usr/bin/env bash
# plan_lint.sh — validate plan.json against plan.schema.json (pure jq, no ajv)
# Usage: plan_lint.sh <plan.json>
# Exit: 0 ok, 1 schema violation, 2 usage error, 3 not JSON
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: plan_lint.sh <plan.json>" >&2
  exit 2
fi

PLAN="$1"
if ! jq empty "$PLAN" 2>/dev/null; then
  echo "ERROR: $PLAN is not valid JSON" >&2
  exit 3
fi

errs=0
fail() { echo "FAIL: $*" >&2; errs=$((errs+1)); }

# meta
jq -e '.meta.topic | type == "string" and length > 0' "$PLAN" >/dev/null || fail "meta.topic missing/empty"
jq -e '.meta.status | IN("pending","in_progress","done","blocked")' "$PLAN" >/dev/null || fail "meta.status invalid"

# phases count
phase_count=$(jq '.phases | length' "$PLAN")
[[ "$phase_count" -ge 1 && "$phase_count" -le 4 ]] || fail "phases count $phase_count not in [1,4]"

# verb regex (English + Chinese subset)
VERB='^(Implement|Modify|Add|Remove|Verify|Refactor|Write|Update|Delete|Validate|Generate|Configure|Install|Run|Migrate|Document|实现|修改|添加|删除|验证|重构|编写|更新|配置|安装|运行|迁移)\b'

# walk phases/slices/tasks
phases=$(jq -c '.phases[]' "$PLAN")
while IFS= read -r ph; do
  pid=$(echo "$ph" | jq -r '.id')
  [[ "$pid" =~ ^P[0-9]+$ ]] || fail "phase id $pid pattern"

  slice_count=$(echo "$ph" | jq '.slices | length')
  [[ "$slice_count" -ge 1 && "$slice_count" -le 5 ]] || fail "phase $pid slices count $slice_count not in [1,5]"

  echo "$ph" | jq -c '.slices[]' | while IFS= read -r sl; do
    sid=$(echo "$sl" | jq -r '.id')
    [[ "$sid" =~ ^P[0-9]+-S[0-9]+$ ]] || { echo "FAIL: slice id $sid pattern" >&2; exit 1; }

    uv=$(echo "$sl" | jq -r '.user_value // ""')
    [[ -n "$uv" ]] || { echo "FAIL: slice $sid user_value empty" >&2; exit 1; }

    acc=$(echo "$sl" | jq '.acceptance | length')
    [[ "$acc" -ge 1 ]] || { echo "FAIL: slice $sid acceptance empty" >&2; exit 1; }

    task_count=$(echo "$sl" | jq '.tasks | length')
    [[ "$task_count" -ge 1 && "$task_count" -le 7 ]] || { echo "FAIL: slice $sid tasks count $task_count not in [1,7]" >&2; exit 1; }

    echo "$sl" | jq -c '.tasks[]' | while IFS= read -r tk; do
      tid=$(echo "$tk" | jq -r '.id')
      [[ "$tid" =~ ^P[0-9]+-S[0-9]+-T[0-9]+$ ]] || { echo "FAIL: task id $tid pattern" >&2; exit 1; }
      action=$(echo "$tk" | jq -r '.action')
      [[ "$action" =~ $VERB ]] || { echo "FAIL: task $tid action does not start with verb: '$action'" >&2; exit 1; }
    done || exit 1
  done || errs=$((errs+1))
done <<< "$phases"

if [[ $errs -gt 0 ]]; then
  echo "$errs error(s)" >&2
  exit 1
fi
echo "OK"
exit 0
SH
chmod +x scripts/plan_lint.sh
```

**Step 4: Run test, expect PASS**

Run: `bats tests/test_plan_lint.bats`
Expected: 6/6 PASS.

> If any test fails, fix the script (most likely the subshell `while` loop swallowing exits — convert to process substitution `done < <(echo "$ph" | jq -c '.slices[]')` instead of pipe) and re-run.

**Step 5: Commit**

```bash
git add tests/test_plan_lint.bats scripts/plan_lint.sh
git commit -m "feat(siw): add plan_lint.sh enforcing 3-level tree limits"
```

---

## Phase 2 — guard.sh (TDD)

### Task 2.1: TDD guard.sh

**Files:**
- Create: `tests/test_guard.bats`
- Create: `scripts/guard.sh`

**Step 1: Write the failing test**

```bash
cat > tests/test_guard.bats <<'BATS'
#!/usr/bin/env bats

SKILL_DIR="$(cd "$(dirname "$BATS_TEST_FILENAME")/.." && pwd)"
GUARD="$SKILL_DIR/scripts/guard.sh"

# 1 = blocked, 0 = allowed, 2 = usage

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
BATS
```

**Step 2: Run, expect all fail**

Run: `bats tests/test_guard.bats`

**Step 3: Implement guard.sh**

```bash
cat > scripts/guard.sh <<'SH'
#!/usr/bin/env bash
# guard.sh — block irreversible operations
# Usage: guard.sh "<command line>"
# Exit: 0 allowed, 1 blocked, 2 usage
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: guard.sh \"<command>\"" >&2
  exit 2
fi

CMD="$1"

block() {
  echo "IRREVERSIBLE_BLOCKED [$1]: $CMD" >&2
  exit 1
}

# data-loss
[[ "$CMD" =~ rm[[:space:]]+-rf?[[:space:]]+/ ]] && block "data-loss"
[[ "$CMD" =~ rm[[:space:]]+-rf?[[:space:]]+~ ]] && block "data-loss"
[[ "$CMD" =~ git[[:space:]]+reset[[:space:]]+--hard ]] && block "data-loss"
[[ "$CMD" =~ git[[:space:]]+clean[[:space:]]+-[a-z]*f ]] && block "data-loss"
[[ "$CMD" =~ DROP[[:space:]]+(TABLE|DATABASE|SCHEMA) ]] && block "data-loss"
[[ "$CMD" =~ TRUNCATE[[:space:]]+TABLE ]] && block "data-loss"

# remote-irreversible
[[ "$CMD" =~ git[[:space:]]+push[[:space:]]+(.*[[:space:]])?(-f|--force|--force-with-lease) ]] && block "remote-irreversible"
[[ "$CMD" =~ git[[:space:]]+push[[:space:]]+--delete ]] && block "remote-irreversible"
[[ "$CMD" =~ git[[:space:]]+branch[[:space:]]+-D ]] && block "remote-irreversible"
[[ "$CMD" =~ gh[[:space:]]+pr[[:space:]]+merge ]] && block "remote-irreversible"
[[ "$CMD" =~ kubectl[[:space:]]+delete ]] && block "remote-irreversible"
[[ "$CMD" =~ terraform[[:space:]]+(apply|destroy) ]] && block "remote-irreversible"

# credentials
[[ "$CMD" =~ (vim|vi|nano|code|cat[[:space:]]+\>|tee)[[:space:]]+.*\.env ]] && block "credentials"
[[ "$CMD" =~ (vim|vi|nano|code)[[:space:]]+.*secrets ]] && block "credentials"
[[ "$CMD" =~ aws[[:space:]]+iam[[:space:]]+(create|delete|update)-access-key ]] && block "credentials"

# shared-comms
[[ "$CMD" =~ curl.*hooks\.(slack|discord|teams|zapier)\.com ]] && block "shared-comms"
[[ "$CMD" =~ curl.*api\.slack\.com/(chat\.postMessage|files\.upload) ]] && block "shared-comms"
[[ "$CMD" =~ gh[[:space:]]+(issue|pr)[[:space:]]+(comment|create|close) ]] && block "shared-comms"
[[ "$CMD" =~ mail[[:space:]]+-s ]] && block "shared-comms"
[[ "$CMD" =~ sendmail ]] && block "shared-comms"

# process
[[ "$CMD" =~ kill[[:space:]]+(-9|-KILL) ]] && block "process"
[[ "$CMD" =~ pkill[[:space:]]+-9 ]] && block "process"
[[ "$CMD" =~ systemctl[[:space:]]+(stop|disable|mask) ]] && block "process"
[[ "$CMD" =~ docker[[:space:]]+(rm|kill|stop)[[:space:]]+-f ]] && block "process"

exit 0
SH
chmod +x scripts/guard.sh
```

**Step 4: Run test, expect PASS**

Run: `bats tests/test_guard.bats`
Expected: 11/11 PASS.

**Step 5: Commit**

```bash
git add tests/test_guard.bats scripts/guard.sh
git commit -m "feat(siw): add guard.sh blocking 5 classes of irreversible ops"
```

---

## Phase 3 — crystallize.sh (TDD)

### Task 3.1: Episodic + semantic fixtures

**Files:**
- Create: `tests/fixtures/memory/episodic_3x_boundary.json` (single file containing 3 episodics with same fingerprint root)
- Create: `tests/fixtures/memory/episodic_2x_only.json` (only 2, should NOT promote)
- Create: `tests/fixtures/memory/empty_semantic.json`

**Step 1: Write fixtures**

`episodic_3x_boundary.json`:
```json
[
  {"id":"ep-1","ts":"2026-04-01T10:00:00Z","scope":"P1-S1-T1","source":"implementation-reviewer","category":"boundary","what":"null input not validated","why":"missing guard","fix":"add not-null check","fingerprint":"boundary:null-input:user-service","confidence":0.8},
  {"id":"ep-2","ts":"2026-04-02T10:00:00Z","scope":"P1-S2-T3","source":"implementation-reviewer","category":"boundary","what":"empty string accepted","why":"missing guard","fix":"add length check","fingerprint":"boundary:null-input:auth-service","confidence":0.75},
  {"id":"ep-3","ts":"2026-04-03T10:00:00Z","scope":"P2-S1-T2","source":"implementation-reviewer","category":"boundary","what":"undefined header","why":"missing guard","fix":"add header check","fingerprint":"boundary:null-input:api-gateway","confidence":0.7}
]
```

`episodic_2x_only.json`: same shape, only 2 entries.

`empty_semantic.json`:
```json
{"patterns":[]}
```

**Step 2: Validate**

Run: `for f in tests/fixtures/memory/*.json; do jq empty "$f"; done`

**Step 3: Commit**

```bash
git add tests/fixtures/memory/
git commit -m "test(siw): add episodic + semantic fixtures for crystallize"
```

---

### Task 3.2: TDD crystallize.sh

**Files:**
- Create: `tests/test_crystallize.bats`
- Create: `scripts/crystallize.sh`

**Step 1: Write the failing test**

```bash
cat > tests/test_crystallize.bats <<'BATS'
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

  # semantic updated
  occ=$(jq '.patterns[0].occurrences' "$TMP/.claude/memory/semantic-patterns.json")
  [ "$occ" -eq 3 ]

  # rule appended
  grep -q "boundary:null-input" "$TMP/.claude/rules/dev-lessons.md"

  # promoted_to_rule flag set
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

  # rule file should remain empty
  ! grep -q "boundary:null-input" "$TMP/.claude/rules/dev-lessons.md"

  # semantic should still track the pattern
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
BATS
```

**Step 2: Run, expect fail**

Run: `bats tests/test_crystallize.bats`

**Step 3: Implement crystallize.sh**

```bash
cat > scripts/crystallize.sh <<'SH'
#!/usr/bin/env bash
# crystallize.sh — episodic → semantic → rules promotion
# Usage: crystallize.sh <claude_dir>
# Thresholds: occurrences >= 3 AND avg_confidence >= 0.7
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: crystallize.sh <.claude dir>" >&2
  exit 2
fi

CDIR="$1"
[[ -d "$CDIR" ]] || { echo "ERROR: $CDIR not a directory" >&2; exit 2; }

EP_DIR="$CDIR/memory/episodic"
SEM="$CDIR/memory/semantic-patterns.json"
RULES="$CDIR/rules/dev-lessons.md"

[[ -d "$EP_DIR" ]] || { echo "ERROR: missing $EP_DIR" >&2; exit 2; }
[[ -f "$SEM" ]] || echo '{"patterns":[]}' > "$SEM"
[[ -f "$RULES" ]] || : > "$RULES"

THRESHOLD_OCC=3
THRESHOLD_CONF=0.7

# Build a working copy of semantic
WORK=$(mktemp)
cp "$SEM" "$WORK"

# For each episodic file, derive 2-segment key and upsert into semantic
shopt -s nullglob
for ep_file in "$EP_DIR"/*.json; do
  fp=$(jq -r '.fingerprint // empty' "$ep_file")
  [[ -z "$fp" ]] && continue
  conf=$(jq -r '.confidence // 0.5' "$ep_file")
  ep_id=$(jq -r '.id' "$ep_file")
  ts=$(jq -r '.ts' "$ep_file")
  what=$(jq -r '.what // ""' "$ep_file")

  # 2-segment key
  key=$(echo "$fp" | awk -F: '{print $1":"$2}')

  # Check if pattern already includes this episodic id (idempotency)
  exists=$(jq --arg key "$key" --arg eid "$ep_id" \
    '(.patterns[] | select(.fingerprint == $key) | .episodic_ids | index($eid)) // null' "$WORK")

  if [[ "$exists" != "null" ]]; then
    continue
  fi

  # Upsert
  WORK2=$(mktemp)
  jq --arg key "$key" --arg eid "$ep_id" --arg ts "$ts" --arg what "$what" --argjson conf "$conf" '
    if (.patterns | map(.fingerprint) | index($key)) == null then
      .patterns += [{
        fingerprint: $key,
        title: $what,
        occurrences: 1,
        first_seen: $ts,
        last_seen: $ts,
        avg_confidence: $conf,
        episodic_ids: [$eid],
        promoted_to_rule: false
      }]
    else
      .patterns |= map(
        if .fingerprint == $key then
          .occurrences += 1
          | .last_seen = $ts
          | .avg_confidence = ((.avg_confidence * (.occurrences - 1) + $conf) / .occurrences)
          | .episodic_ids += [$eid]
        else . end
      )
    end
  ' "$WORK" > "$WORK2"
  mv "$WORK2" "$WORK"
done
shopt -u nullglob

# Promotion phase
to_promote=$(jq -c --argjson th_occ "$THRESHOLD_OCC" --argjson th_conf "$THRESHOLD_CONF" '
  .patterns[] | select(.promoted_to_rule == false and .occurrences >= $th_occ and .avg_confidence >= $th_conf)
' "$WORK")

while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  fp=$(echo "$p" | jq -r '.fingerprint')
  title=$(echo "$p" | jq -r '.title')
  occ=$(echo "$p" | jq -r '.occurrences')
  conf=$(echo "$p" | jq -r '.avg_confidence')
  date=$(date +%Y-%m-%d)
  lid="L-$(date +%s)-$(echo "$fp" | tr ':' '-')"

  cat >> "$RULES" <<RULE

## $lid: $title

**Rule**: Avoid the recurring pattern \`$fp\` observed across $occ instances.

**Why**: Pattern surfaced by reviewers $occ times with average confidence $conf.

**How to apply**: Whenever scope matches the pattern signature, apply the fix uniformly.

<!-- Crystallized: $date | pattern: $fp | from $occ episodics | confidence: $conf -->
RULE

  WORK2=$(mktemp)
  jq --arg fp "$fp" '.patterns |= map(if .fingerprint == $fp then .promoted_to_rule = true else . end)' "$WORK" > "$WORK2"
  mv "$WORK2" "$WORK"
done <<< "$to_promote"

mv "$WORK" "$SEM"
echo "crystallize: ok"
SH
chmod +x scripts/crystallize.sh
```

**Step 4: Run, expect PASS**

Run: `bats tests/test_crystallize.bats`
Expected: 4/4 PASS.

> Likely first-attempt failures: jq syntax issues with `--argjson` for floats, or `index()` returning the wrong type. Fix incrementally; each test pinpoints the broken case.

**Step 5: Commit**

```bash
git add tests/test_crystallize.bats scripts/crystallize.sh
git commit -m "feat(siw): add crystallize.sh with deterministic threshold promotion"
```

---

## Phase 4 — init.sh rewrite (TDD)

### Task 4.1: TDD new init.sh

**Files:**
- Create: `tests/test_init.bats`
- Modify (rewrite): `scripts/init.sh`

**Step 1: Write the failing test**

```bash
cat > tests/test_init.bats <<'BATS'
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
BATS
```

**Step 2: Run, expect fail**

Run: `bats tests/test_init.bats`

**Step 3: Rewrite init.sh**

Replace `scripts/init.sh` with:

```bash
cat > scripts/init.sh <<'SH'
#!/usr/bin/env bash
# init.sh — scaffold .claude/ for self-improving-workflow (no tier/stack/compliance)
# Usage: init.sh [project_root]
set -euo pipefail

ROOT="${1:-$(pwd)}"
[[ -d "$ROOT" ]] || { echo "ERROR: $ROOT is not a directory" >&2; exit 1; }
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TPL="$SKILL_DIR/templates"

cd "$ROOT"

CREATED=0
SKIPPED=0

copy_once() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [[ -e "$dst" ]]; then
    if [[ "$(basename "$dst")" == "CLAUDE.md" ]]; then
      cp "$src" "${dst}.skill-template"
      echo "  ~ $dst exists; wrote ${dst}.skill-template"
    else
      SKIPPED=$((SKIPPED+1))
      echo "  - $dst exists, skip"
    fi
    return
  fi
  cp "$src" "$dst"
  CREATED=$((CREATED+1))
  echo "  + $dst"
}

# CLAUDE.md
copy_once "$TPL/CLAUDE.md.template" ".claude/CLAUDE.md"

# commands
for c in run plan review learn resume; do
  copy_once "$TPL/commands/${c}.md.template" ".claude/commands/${c}.md"
done

# agents
for a in planner-critic implementation-reviewer requirement-auditor integration-checker; do
  copy_once "$TPL/agents/${a}.md.template" ".claude/agents/${a}.md"
done

# rules
copy_once "$TPL/rules/autonomy-stops.md.template" ".claude/rules/autonomy-stops.md"
copy_once "$TPL/rules/dev-lessons.md.template" ".claude/rules/dev-lessons.md"

# state
copy_once "$TPL/state/plan.schema.json" ".claude/state/plan.schema.json"
[[ -f .claude/state/plan.json ]] || { echo '{}' > .claude/state/plan.json; CREATED=$((CREATED+1)); echo "  + .claude/state/plan.json"; }
[[ -f .claude/state/decisions.jsonl ]] || { : > .claude/state/decisions.jsonl; CREATED=$((CREATED+1)); echo "  + .claude/state/decisions.jsonl"; }
mkdir -p .claude/state/archive

# memory
copy_once "$TPL/memory/README.md.template" ".claude/memory/README.md"
mkdir -p .claude/memory/episodic .claude/memory/working
[[ -f .claude/memory/semantic-patterns.json ]] || { echo '{"patterns":[]}' > .claude/memory/semantic-patterns.json; CREATED=$((CREATED+1)); echo "  + .claude/memory/semantic-patterns.json"; }

# gitignore patch (idempotent)
GI=".gitignore"
touch "$GI"
for line in ".claude/memory/episodic/" ".claude/memory/working/" ".claude/state/working/"; do
  grep -qxF "$line" "$GI" || echo "$line" >> "$GI"
done

echo "init: created=$CREATED skipped=$SKIPPED"
SH
chmod +x scripts/init.sh
```

**Step 4: Stub all referenced template files** so init has something to copy.

Run:
```bash
mkdir -p templates/{commands,agents,rules,state,memory}
echo "# placeholder" > templates/CLAUDE.md.template
for f in run plan review learn resume; do echo "# placeholder $f" > templates/commands/$f.md.template; done
for f in planner-critic implementation-reviewer requirement-auditor integration-checker; do echo "# placeholder $f" > templates/agents/$f.md.template; done
echo "# placeholder" > templates/rules/autonomy-stops.md.template
echo "# placeholder" > templates/rules/dev-lessons.md.template
echo "# placeholder" > templates/memory/README.md.template
```
(`templates/state/plan.schema.json` already exists from Phase 1.)

**Step 5: Run test, expect PASS**

Run: `bats tests/test_init.bats`
Expected: 5/5 PASS.

**Step 6: Commit**

```bash
git add tests/test_init.bats scripts/init.sh templates/CLAUDE.md.template templates/commands/ templates/agents/ templates/rules/ templates/memory/
git commit -m "feat(siw): rewrite init.sh — no tiers, single layout, idempotent"
```

---

## Phase 5 — Reviewer Agent Templates

### Task 5.1: planner-critic.md

**Files:**
- Modify: `templates/agents/planner-critic.md.template`

**Step 1: Write template**

```markdown
---
name: planner-critic
description: Critique a plan.json against schema, granularity limits, and dev-lessons. Read-only.
tools: Read, Bash
---

# Planner-Critic

You are the Planner-Critic. Your job is to **reject bad plans before they execute**.

## Inputs

- `.claude/state/plan.json` — the candidate plan
- `.claude/state/plan.schema.json` — the schema
- `.claude/rules/dev-lessons.md` — accumulated rules
- The user topic that originated the plan

## Procedure

1. Run `bash $(find ~/.agents/skills/self-improving-workflow/scripts -name plan_lint.sh) .claude/state/plan.json`. Any non-zero exit → **fail** with the lint output.
2. Read `dev-lessons.md`. For each rule, scan the plan for violations.
3. For each slice, check:
   - `user_value` is concrete and user-visible (not "refactor X")
   - `acceptance` items are observable (not "code is clean")
4. For each task, check:
   - Action is one verb + one target (no "and"-chains)
   - Idempotent or has explicit pre-check
5. Cross-check that the plan covers the topic. Anything in the topic that has no matching slice → fail.

## Output

Return ONLY a single JSON object matching this shape:

```json
{
  "reviewer": "planner-critic",
  "target": "plan",
  "verdict": "pass" | "fail",
  "severity": "P0" | "P1" | "P2",
  "issues": [
    {"what": "...", "why": "...", "fix_hint": "...", "category": "spec|logic|integration|risk"}
  ],
  "lessons_candidate": []
}
```
```

**Step 2: Verify the file is the only thing changed**

Run: `git diff --stat templates/agents/planner-critic.md.template`

**Step 3: Commit**

```bash
git add templates/agents/planner-critic.md.template
git commit -m "feat(siw): planner-critic agent template"
```

---

### Task 5.2: implementation-reviewer.md

**Files:**
- Modify: `templates/agents/implementation-reviewer.md.template`

**Step 1: Write template**

```markdown
---
name: implementation-reviewer
description: Review a single completed task's evidence for logic, boundaries, idempotency, dev-lessons compliance. Read-only.
tools: Read, Grep, Bash
---

# Implementation-Reviewer

You review **one task** at a time, immediately after it is marked done.

## Inputs

- The task object (id, action, target, evidence)
- `.claude/rules/dev-lessons.md`
- The actual files modified (read them)

## Rubric

For the target task, check:

1. **Correctness** — does the change implement the action?
2. **Boundaries** — null/empty/unicode/error paths handled?
3. **Idempotency** — re-running this task leaves the system in the same state? If not, is there an explicit pre-check?
4. **dev-lessons compliance** — any rule in `dev-lessons.md` violated?
5. **Side effects** — anything modified outside `target`?
6. **Evidence quality** — does the evidence pointer (commit/file/test output) actually exist and demonstrate the change?

## Output

Single JSON object:

```json
{
  "reviewer": "implementation-reviewer",
  "target": "<task id>",
  "verdict": "pass" | "fail",
  "severity": "P0" | "P1" | "P2",
  "issues": [
    {"what": "...", "why": "...", "fix_hint": "...", "category": "logic|boundary|spec|integration|style|risk"}
  ],
  "lessons_candidate": [
    {"pattern": "...", "evidence": "...", "confidence": 0.0-1.0}
  ]
}
```

If verdict is `fail`, the main loop will instruct the executor to repair and re-submit. Three consecutive fails on the same task → blocked.

**You never modify code yourself.**
```

**Step 2: Commit**

```bash
git add templates/agents/implementation-reviewer.md.template
git commit -m "feat(siw): implementation-reviewer agent template"
```

---

### Task 5.3: requirement-auditor.md

**Files:**
- Modify: `templates/agents/requirement-auditor.md.template`

**Step 1: Write template**

```markdown
---
name: requirement-auditor
description: Audit a completed slice against its user_value and acceptance criteria. Read-only.
tools: Read, Grep, Bash
---

# Requirement-Auditor

You audit **one slice** after all its tasks are done.

## Inputs

- The slice object (`user_value`, `acceptance[]`, `tasks[]`)
- All evidence pointers from the slice's tasks
- The original topic that the plan addresses

## Rubric

1. For each `acceptance` item, find concrete evidence in the task outputs that proves it. Missing evidence → coverage gap.
2. Reverse: scan the slice's `user_value` against the topic. Any user-visible behavior promised by the topic but not delivered by this slice → coverage gap.
3. Spec drift: if any task action diverges from what the slice promises → flag.
4. Hidden assumptions: are there preconditions (auth, config, schema) the user must do manually? Flag as gap.

## Output

```json
{
  "reviewer": "requirement-auditor",
  "target": "<slice id>",
  "verdict": "pass" | "fail",
  "severity": "P0" | "P1" | "P2",
  "issues": [
    {"what": "...", "why": "...", "fix_hint": "...", "category": "spec"}
  ],
  "coverage_gap": [
    {"missing": "...", "suggested_task": "<verb> <target>"}
  ],
  "lessons_candidate": []
}
```

The main loop converts each `coverage_gap` into a new pending task at the end of the same slice.
```

**Step 2: Commit**

```bash
git add templates/agents/requirement-auditor.md.template
git commit -m "feat(siw): requirement-auditor agent template"
```

---

### Task 5.4: integration-checker.md

**Files:**
- Modify: `templates/agents/integration-checker.md.template`

**Step 1: Write template**

```markdown
---
name: integration-checker
description: Check seams between slices in a phase and across adjacent phases. Read-only.
tools: Read, Grep, Bash
---

# Integration-Checker

You run **once per phase**, after all slices in the phase are done.

## Inputs

- The phase object (all slices, all tasks, all evidence)
- The previous phase (if any) — for cross-phase contracts
- `.claude/rules/dev-lessons.md`

## Rubric

1. **Interface alignment** — every consumer in slice B references something the producer in slice A actually exports?
2. **State machine closure** — every state any slice introduces has at least one transition out?
3. **Event/listener pairing** — every event publish has at least one listener? Every listener has at least one publish path?
4. **Data flow closure** — every read has a write somewhere upstream; every write has a consumer (or is logged as terminal)?
5. **Naming consistency** — same concept named the same way across slices?

## Output

```json
{
  "reviewer": "integration-checker",
  "target": "<phase id>",
  "verdict": "pass" | "fail",
  "severity": "P0" | "P1" | "P2",
  "issues": [
    {"what": "...", "why": "...", "fix_hint": "...", "category": "integration"}
  ],
  "seams": [
    {"between": ["P1-S1", "P1-S2"], "problem": "...", "suggested_slice": "..."}
  ],
  "lessons_candidate": []
}
```

The main loop converts each `seam` entry into a new slice at the end of the phase.
```

**Step 2: Commit**

```bash
git add templates/agents/integration-checker.md.template
git commit -m "feat(siw): integration-checker agent template"
```

---

## Phase 6 — Slash Command Templates

### Task 6.1: run.md

**Files:**
- Modify: `templates/commands/run.md.template`

**Step 1: Write the template**

The full content goes verbatim into the file. Includes: bootstrap, plan, planner-critic loop, execute loop with reviewer dispatches, halt conditions, decision log writes. Must be self-contained because Claude reads this when `/run` is invoked.

```markdown
---
description: Drive a long-running plan to completion fully autonomously
---

# /run — Two-Pillar Long Task Driver

Argument: $ARGUMENTS (the topic, in natural language)

## Hard rules

- **Single user interaction point**: only the bootstrap-overwrite prompt below.
- **Halt only on**: irreversible operation detected by `guard.sh`, OR 3 consecutive review fails on the same target.
- **Every non-trivial decision** writes a `decisions.jsonl` entry with `kind=choice`.
- **No question to user** mid-loop, ever.

## 0. Bootstrap

If `.claude/state/plan.json` is missing:
- Run `bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"`
- Initialize plan.json to `{}`

If `.claude/state/plan.json` exists with `meta.status` not `done`:
- Ask the user once: `"Existing unfinished plan found. (o)verwrite / (r)esume / (a)bort?"`
- `o` → archive current plan to `.claude/state/archive/plan-$(date +%s).json`, proceed
- `r` → invoke `/resume` instead
- `a` → exit
**This is the only time you ask the user anything.**

## 1. Write plan

Generate a plan.json for the topic following the schema in `.claude/state/plan.schema.json`. Hard limits: ≤4 phases, ≤5 slices/phase, ≤7 tasks/slice. Write to `.claude/state/plan.json`.

## 2. Validate plan

Dispatch the `planner-critic` subagent. If `verdict == fail`:
- Re-write the plan addressing every issue
- Re-dispatch
- After 3 consecutive fails: write `decisions.jsonl kind=blocked scope=plan`, mark plan blocked, exit

## 3. Execute loop

```
while plan.meta.status != "done":
  task = first task in DFS order with status == "pending"
  if task is None:
    handle slice/phase completion (see §4)
    continue

  set task.status = "in_progress"; persist plan.json

  for each shell command you intend to run:
    bash ~/.agents/skills/self-improving-workflow/scripts/guard.sh "<command>"
    if exit != 0:
      append decisions.jsonl: {kind:"blocked", scope:task.id, action:"<command>"}
      set task.status = "blocked"; set plan.meta.status = "blocked"; persist; EXIT

  execute the task
  write evidence (file path / commit sha / test output) to task.evidence
  set task.status = "done"; persist

  dispatch implementation-reviewer subagent on this task
  if verdict == fail:
    increment local fail counter for this task
    if counter == 3:
      append decisions.jsonl: {kind:"blocked", scope:task.id, ...}
      set task.status = "blocked"; set plan.meta.status = "blocked"; persist; EXIT
    repair the task (re-execute the action with the issues addressed)
    set task.status = "done"; persist
    re-dispatch reviewer
  else:
    if review has lessons_candidate, append episodic record(s) to .claude/memory/episodic/
```

## 4. Slice/phase completion

```
if all tasks in current slice are done:
  dispatch requirement-auditor on the slice
  if fail:
    for each coverage_gap, append a new task to slice.tasks
    persist; continue main loop
  else:
    set slice.status = "done"; persist

if all slices in current phase are done:
  dispatch integration-checker on the phase
  if fail:
    for each seam, append a new slice to phase.slices
    persist; continue main loop
  else:
    set phase.status = "done"; persist

if all phases done:
  dispatch planner-critic for final pass
  bash ~/.agents/skills/self-improving-workflow/scripts/crystallize.sh .claude
  set plan.meta.status = "done"; persist
  EXIT cleanly
```

## 5. Decision log discipline

Append to `.claude/state/decisions.jsonl` for every:
- non-obvious choice (`kind=choice`) — even small ones, e.g. lib selection
- replan (`kind=replan`)
- task error + repair (`kind=error`)
- halt (`kind=blocked`)

JSONL format: one line per record, see schema in design doc §7.

## 6. Crystallization

Periodically (after each phase done, and at exit) run:
```bash
bash ~/.agents/skills/self-improving-workflow/scripts/crystallize.sh .claude
```
This is the only place new rules enter `dev-lessons.md`.

## 7. Persistence atomicity

When writing plan.json, write to a temp file then `mv` over the target. Never leave plan.json half-written.
```

**Step 2: Commit**

```bash
git add templates/commands/run.md.template
git commit -m "feat(siw): /run command — full closed-loop driver"
```

---

### Task 6.2: plan.md, review.md, learn.md, resume.md

**Files:**
- Modify: `templates/commands/plan.md.template`
- Modify: `templates/commands/review.md.template`
- Modify: `templates/commands/learn.md.template`
- Modify: `templates/commands/resume.md.template`

**Step 1: Write each (each is short — they're subset operations of /run)**

`plan.md.template`:
```markdown
---
description: Write/rewrite plan.json for the given topic; runs Planner-Critic; does not execute
---

# /plan

Argument: $ARGUMENTS (topic)

1. Read `.claude/state/plan.schema.json`.
2. Write `.claude/state/plan.json` matching the schema for the topic, respecting hard limits (≤4 phases, ≤5 slices/phase, ≤7 tasks/slice).
3. Dispatch `planner-critic`. Iterate (max 3 attempts). On 3rd fail, leave plan.json with `meta.status = "blocked"` and exit.
4. On pass, persist and exit. Do **not** start execution.
```

`review.md.template`:
```markdown
---
description: Run reviewer agents over plan or a scope, without modifying anything
---

# /review

Argument: $ARGUMENTS (optional: phase/slice/task id, or "all")

- No arg or `all` → dispatch all 4 reviewers across the entire plan; collate output
- Phase id → integration-checker
- Slice id → requirement-auditor
- Task id → implementation-reviewer

Print collated JSON results. **Do not modify plan or code.** This is a read-only diagnostic command.
```

`learn.md.template`:
```markdown
---
description: Run the crystallization pipeline manually
---

# /learn

Run:
```bash
bash ~/.agents/skills/self-improving-workflow/scripts/crystallize.sh .claude
```

Print before/after counts of `semantic-patterns.json` patterns and any new lines appended to `dev-lessons.md`.
```

`resume.md.template`:
```markdown
---
description: Continue an unfinished plan from where it stopped
---

# /resume

Argument: $ARGUMENTS (optional: `--force-resume`)

1. Read `.claude/state/plan.json`.
2. If `meta.status == "done"`, print a summary and exit.
3. If `meta.status == "blocked"` and `--force-resume` not given, refuse with the last `decisions.jsonl` entry as context.
4. Otherwise, set `meta.status = "in_progress"` and re-enter the `/run` execute loop from the first non-`done` task.
5. Re-load the tail of `decisions.jsonl` (last 50 entries) into reasoning context to avoid relitigating settled choices.
```

**Step 2: Commit**

```bash
git add templates/commands/plan.md.template templates/commands/review.md.template templates/commands/learn.md.template templates/commands/resume.md.template
git commit -m "feat(siw): /plan /review /learn /resume command templates"
```

---

## Phase 7 — Rules Templates + CLAUDE.md + memory README

### Task 7.1: autonomy-stops.md (the seed)

**Files:**
- Modify: `templates/rules/autonomy-stops.md.template`

**Step 1: Write template**

```markdown
# Irreversible operations — never execute autonomously

> Seeded by self-improving-workflow skill. **You may add entries; you may not remove seeded entries.**
> `guard.sh` enforces these via regex.

## Data loss
- `rm -rf` outside the working tree
- `git reset --hard` discarding uncommitted changes
- `git clean -fd`
- SQL `DROP TABLE/DATABASE/SCHEMA`, `TRUNCATE TABLE`

## Remote-irreversible
- `git push --force` / `git push -f` to any branch
- `git push --delete`
- `git branch -D` on shared branches
- `gh pr merge`
- `kubectl delete`
- `terraform apply` / `terraform destroy`

## Credentials
- Editing `.env`, `secrets/*`, `.npmrc`, `.pypirc` containing tokens
- `aws iam create/delete/update-access-key`
- Token rotation commands
- Any paid external API call

## Shared communications
- Slack/Discord/Teams webhooks
- `gh issue|pr comment|create|close`
- Email send (`mail`, `sendmail`, SMTP CLIs)

## Process / system
- `kill -9`, `pkill -9` of non-self-spawned processes
- `systemctl stop|disable|mask`
- `docker rm|kill|stop -f` of shared containers

## Project additions

<!-- append below; never remove anything above this line -->
```

**Step 2: Commit**

```bash
git add templates/rules/autonomy-stops.md.template
git commit -m "feat(siw): autonomy-stops.md seed (5 categories)"
```

---

### Task 7.2: dev-lessons.md (empty seed)

**Files:**
- Modify: `templates/rules/dev-lessons.md.template`

**Step 1: Write template**

```markdown
# Development lessons — auto-crystallized

> Auto-populated by `/learn` (or by `/run` at phase boundaries) when patterns reach the threshold of ≥3 occurrences with average confidence ≥0.7.
>
> **Do not edit by hand.** If a rule is wrong, mark the offending entry with `⚠ superseded by <new>` and let the next crystallization pass produce the replacement.

<!-- crystallize.sh appends entries below this line -->
```

**Step 2: Commit**

```bash
git add templates/rules/dev-lessons.md.template
git commit -m "feat(siw): dev-lessons.md empty seed"
```

---

### Task 7.3: CLAUDE.md.template

**Files:**
- Modify: `templates/CLAUDE.md.template`

**Step 1: Write template**

```markdown
# Project workflow — self-improving-workflow

This project uses the `self-improving-workflow` skill methodology. Two pillars:

1. **Multi-agent collaborative learning** — every plan, slice, task, and phase is reviewed by 4 specialist sub-agents (`planner-critic`, `implementation-reviewer`, `requirement-auditor`, `integration-checker`). Findings auto-crystallize into `.claude/rules/dev-lessons.md`.

2. **Long-running uninterrupted execution** — single `/run <topic>` entrypoint drives a hierarchical plan (phase → slice → task) to completion fully autonomously. Halts only on irreversible operations or 3 consecutive review failures.

## Commands

| Command | What it does |
|---|---|
| `/run <topic>` | Full closed-loop driver — bootstraps, plans, executes, reviews, learns |
| `/plan <topic>` | Plan only, no execution |
| `/review [scope]` | Read-only diagnostic across reviewers |
| `/learn` | Run crystallization manually |
| `/resume [--force-resume]` | Continue an unfinished plan |

## State

- `.claude/state/plan.json` — current plan tree
- `.claude/state/decisions.jsonl` — append-only decision log
- `.claude/memory/episodic/` — raw experiences (gitignored)
- `.claude/memory/semantic-patterns.json` — aggregated patterns (git-tracked)
- `.claude/rules/dev-lessons.md` — crystallized rules (auto-loaded; do not hand-edit)
- `.claude/rules/autonomy-stops.md` — irreversible-op blocklist (you may add)

## Operating principles

- Trust `/run` to make every non-irreversible decision. Don't pre-approve.
- The decision log is your audit window — read it after a long run, not during.
- New project conventions emerge naturally via crystallization. Don't pre-seed `dev-lessons.md`.
```

**Step 2: Commit**

```bash
git add templates/CLAUDE.md.template
git commit -m "feat(siw): CLAUDE.md.template for two-pillar projects"
```

---

### Task 7.4: memory/README.md.template

**Files:**
- Modify: `templates/memory/README.md.template`

**Step 1: Write template**

```markdown
# Memory layout

Three layers, written by reviewers and `crystallize.sh`. **Do not hand-edit.**

```
.claude/memory/
├── episodic/                ← raw event records (gitignored)
│   └── ep-<date>-<id>.json
├── semantic-patterns.json    ← aggregated by fingerprint (git tracked)
└── working/                  ← session-scope cache (gitignored)
```

Promotion path: `episodic → semantic → .claude/rules/dev-lessons.md`.

Threshold: 3 occurrences with same 2-segment fingerprint AND average confidence ≥ 0.7.
```

**Step 2: Commit**

```bash
git add templates/memory/README.md.template
git commit -m "feat(siw): memory README explaining 3-layer promotion"
```

---

## Phase 8 — SKILL.md + README + references

### Task 8.1: Rewrite SKILL.md

**Files:**
- Modify: `SKILL.md`

**Step 1: Write the new SKILL.md**

```markdown
---
name: self-improving-workflow
description: >
  Universal methodology skill for Claude Code projects. Two pillars:
  (1) Multi-agent collaborative learning — every plan, slice, task and phase
  is reviewed by 4 specialist sub-agents (planner-critic, implementation-reviewer,
  requirement-auditor, integration-checker) whose findings auto-crystallize into
  project rules. (2) Long-running uninterrupted execution — single /run entrypoint
  drives a hierarchical plan (phase→slice→task) to completion fully autonomously,
  halting only on physically irreversible operations or 3 consecutive review fails.
  Tech-stack agnostic, project agnostic, no tier system.
  TRIGGER WORDS: /run, long task, autonomous plan, multi-agent review,
  self improving, 长任务, 多智能体评审, 自主执行, 不间断, 工作流初始化, scaffold .claude.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
---

# Self-Improving Workflow

A universal methodology skill. No tech stack templates. No tier system. Two pillars:

## Pillar 1 — Multi-Agent Collaborative Learning

Four sub-agents review the work at four levels:

| Reviewer | Triggers on |
|---|---|
| `planner-critic` | every new plan / re-plan |
| `implementation-reviewer` | every task done |
| `requirement-auditor` | every slice done |
| `integration-checker` | every phase done |

All findings flow to `.claude/memory/episodic/` and are auto-promoted to `.claude/rules/dev-lessons.md` once a pattern hits the threshold (≥3 occurrences, ≥0.7 avg confidence).

## Pillar 2 — Long-Running Uninterrupted Execution

Single `/run <topic>` command drives a hierarchical plan (`phase → slice → task`, hard limits: 4×5×7) to completion. **Only stops on**:

1. `guard.sh` blocks an irreversible operation (data loss, remote irreversible, credentials, shared comms, process kill)
2. 3 consecutive review failures on the same target

Decision log at `.claude/state/decisions.jsonl` records every non-trivial choice for post-hoc audit.

## Commands installed in `.claude/commands/`

| Command | Purpose |
|---|---|
| `/run <topic>` | The main entrypoint |
| `/plan <topic>` | Plan only, no execution |
| `/review [scope]` | Diagnostic, read-only |
| `/learn` | Manual crystallization |
| `/resume` | Continue an unfinished plan |

## Bootstrap

First time `/run` is invoked, `scripts/init.sh` writes the `.claude/` skeleton (idempotent, write-once). Existing files are never overwritten — `CLAUDE.md` triggers a `.skill-template` companion.

## See also

- `references/methodology.md` — the why behind the two pillars
- `references/plan-schema.md` — full plan model
- `references/reviewer-contracts.md` — IO contract for each reviewer
- `references/learning-loop.md` — crystallization algorithm
```

**Step 2: Commit**

```bash
git add SKILL.md
git commit -m "docs(siw): rewrite SKILL.md around two pillars"
```

---

### Task 8.2: Write references/*.md

**Files:**
- Create: `references/methodology.md`
- Create: `references/plan-schema.md`
- Create: `references/reviewer-contracts.md`
- Create: `references/learning-loop.md`

**Step 1: Create each as a focused 1-2 page reference**

Each document should be lifted directly from the corresponding section of the design doc:
- `methodology.md` ← design §2 + §3
- `plan-schema.md` ← design §5 (and embeds the JSON Schema by ref)
- `reviewer-contracts.md` ← design §6
- `learning-loop.md` ← design §8

Use the same prose; do not invent. The design doc is the source of truth.

**Step 2: Verify all 4 exist and are non-empty**

Run:
```bash
for f in methodology plan-schema reviewer-contracts learning-loop; do
  [[ -s "references/$f.md" ]] || echo "EMPTY $f"
done
```
Expected: no EMPTY output.

**Step 3: Commit**

```bash
git add references/methodology.md references/plan-schema.md references/reviewer-contracts.md references/learning-loop.md
git commit -m "docs(siw): four reference docs covering methodology/plan/reviewers/learning"
```

---

### Task 8.3: README + zh-CN sync

**Files:**
- Modify: `README.md`
- Modify: `README.zh-CN.md`

**Step 1: Mirror SKILL.md content into README, drop the YAML frontmatter**

Both READMEs should:
- Lead with the two pillars
- List the 5 commands
- Show the file layout from §11/§12 of the design
- Link to references/

**Step 2: Commit**

```bash
git add README.md README.zh-CN.md
git commit -m "docs(siw): rewrite README EN/zh around two pillars"
```

---

### Task 8.4: Migration guide

**Files:**
- Create: `references/migration-from-tiered.md`

**Step 1: Write the migration doc**

```markdown
# Migrating from the tiered version

If your project's `.claude/` was created by the old tiered (minimal/standard/full) version, it will keep working — slash commands are decoupled from the skill binary. To adopt the two-pillar model:

## Option A — In place

1. Inside the project, delete only the old tier-marker: `rm .claude/.workflow-tier`
2. Re-run from the skill: `bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"`
3. The init is idempotent: existing files are skipped, missing files (`commands/run.md`, `agents/*`, `state/`, `memory/semantic-patterns.json`, etc.) are created.
4. Manually delete commands you no longer want: `phase-start.md`, `phase-review.md`, `compile-check.md`, `upgrade-workflow.md`, `self-improve.md`.
5. The old `coding-bans.md`, `module-isolation.md`, `domain-compliance.md` files are not touched. Decide whether to keep them as project-specific seeded rules or delete them and let crystallization rebuild.

## Option B — Clean slate

1. `mv .claude .claude.tiered-backup`
2. `bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"`
3. Diff the two if you want to lift over project-specific lessons.

## What the old version had that the new one doesn't

- 3 tiers — replaced by single methodology
- `coding-bans.md`, `module-isolation.md`, `domain-compliance.md` — not seeded; expected to grow via crystallization
- Tech-stack templates (Python/Java/React/etc) — removed
- `/phase-start`, `/phase-review`, `/self-improve`, `/compile-check`, `/upgrade-workflow` — replaced by `/run`, `/plan`, `/review`, `/learn`, `/resume`
- `scripts/detect.sh`, `scripts/upgrade.sh` — removed
```

**Step 2: Commit**

```bash
git add references/migration-from-tiered.md
git commit -m "docs(siw): migration guide from tiered to two-pillar"
```

---

## Phase 9 — End-to-End Integration Test

### Task 9.1: Full integration test (all scripts together on a tmp project)

**Files:**
- Create: `tests/test_integration.bats`

**Step 1: Write the integration test**

```bash
cat > tests/test_integration.bats <<'BATS'
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

  # Drop a synthetic valid plan into state
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
  cp "$SKILL_DIR/tests/fixtures/memory/episodic_3x_boundary.json" /tmp/eps.json
  jq -c '.[]' /tmp/eps.json | while IFS= read -r ep; do
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

  cp "$SKILL_DIR/tests/fixtures/memory/episodic_3x_boundary.json" /tmp/eps.json
  jq -c '.[]' /tmp/eps.json | while IFS= read -r ep; do
    id=$(echo "$ep" | jq -r '.id')
    echo "$ep" > ".claude/memory/episodic/$id.json"
  done

  bash "$SKILL_DIR/scripts/crystallize.sh" .claude
  bash "$SKILL_DIR/scripts/crystallize.sh" .claude
  count=$(grep -c "boundary:null-input" .claude/rules/dev-lessons.md || true)
  [ "$count" -eq 1 ]
}
BATS
```

**Step 2: Run, expect PASS**

Run: `bats tests/test_integration.bats`
Expected: 4/4 PASS.

If any fail, root-cause in the underlying script (`init.sh`, `plan_lint.sh`, `guard.sh`, `crystallize.sh`), fix in that script's task, commit a fix-up, then re-run.

**Step 3: Commit**

```bash
git add tests/test_integration.bats
git commit -m "test(siw): end-to-end integration covering init+lint+guard+crystallize"
```

---

### Task 9.2: Run the full test suite

**Files:** none

**Step 1: Run everything**

Run: `cd ~/.agents/skills/self-improving-workflow && bats tests/`
Expected: total ~30 tests, all PASS.

**Step 2: Audit acceptance criteria from design §15**

Verify each:
1. ✅ `templates/` has no tier subdirs; `scripts/` has `init.sh`, `guard.sh`, `crystallize.sh`, `plan_lint.sh`
2. ✅ `init.sh` on empty project produces full layout (covered by `test_init.bats`)
3. — `/run` end-to-end on a real test project — manual smoke; document deferral
4. ✅ `guard.sh` blocks ≥1 entry from each of 5 categories (covered by `test_guard.bats`)
5. ✅ `crystallize.sh` promotes synthetic 3-occurrence pattern (covered by `test_crystallize.bats`)
6. — `/resume` mid-plan — manual smoke; document deferral
7. ✅ SKILL.md leads with two pillars (visual check)
8. ✅ No file under `templates/` mentions Python/Java/React/FastAPI:
   ```bash
   grep -ri -E "(Python|Java|React|FastAPI|Spring|Django|Vue|Angular)" templates/ && echo "VIOLATION" || echo "clean"
   ```

**Step 3: If anything fails, fix and re-run before proceeding.**

**Step 4: Commit smoke results to a file**

Run:
```bash
mkdir -p docs/plans/_artifacts
{
  echo "# Refactor smoke results — $(date +%Y-%m-%d)"
  echo
  echo "## bats"
  bats tests/ 2>&1
  echo
  echo "## stack-leak grep"
  grep -ri -E "(Python|Java|React|FastAPI|Spring|Django|Vue|Angular)" templates/ || echo "clean"
} > docs/plans/_artifacts/smoke-results.txt
git add docs/plans/_artifacts/smoke-results.txt
git commit -m "chore(siw): record full-suite smoke results"
```

---

## Phase 10 — Final wrap

### Task 10.1: Update top-level CLAUDE.md (if any)

**Files:**
- Verify if `~/.agents/skills/CLAUDE.md` mentions this skill; update if so.

**Step 1: Search**

Run: `cd ~/.agents/skills && grep -l "self-improving-workflow" CLAUDE.md README.md 2>/dev/null || echo "no mention"`

**Step 2: If found, update reference paragraph to reflect two-pillar.**

**Step 3: Commit if changed**

---

### Task 10.2: Push branch (manual)

**Files:** none

**Step 1: Push for review**

Run: `cd ~/.agents/skills && git log --oneline refactor/siw-two-pillar ^main | head -30`
Expected: ~25 commits, all conventional commit prefix, one logical change each.

**Step 2: STOP — wait for user**

Do NOT push without explicit user request. Print the suggested command:
```
Suggested: cd ~/.agents/skills && git push -u origin refactor/siw-two-pillar
```

---

## Done criteria

- All 4 phases of bats tests pass (`bats tests/` exits 0)
- `grep -ri -E "(Python|Java|React|FastAPI|Spring|Django|Vue|Angular)" templates/` finds nothing
- Old `templates/{minimal,standard,full}/`, `scripts/{detect,upgrade}.sh`, `references/{tier-comparison,compliance-presets,existing-project-guide}.md` are gone from `git ls-files`
- `.claude/` produced by `init.sh` matches design §12 exactly
- Branch `refactor/siw-two-pillar` is ready for human review or merge

## Deferred (post-merge follow-ups, not part of this plan)

- Real `/run` smoke against a live trivial project (requires interactive Claude session)
- Reviewer prompt iteration based on real run feedback
- Parallel reviewer dispatch (currently sequential)
- crystallize.sh perf tuning if episodic dir grows past ~1k files
