# Plan Schema — phase → slice → task

## Tree Shape

A plan is a strict 3-level tree:

```
Plan { meta, phases }
  Phase { id, title, goal, status, slices }
    Slice { id, title, user_value, acceptance[], status, tasks }
      Task { id, action, target, status, evidence }
```

**Plan** — the root. One plan active at a time. Stored at `.claude/state/plan.json` (single file, atomic rewrites).

**Phase** — a major delivery unit with a goal. Reviewed by `integration-checker` when all slices are done.

**Slice** — a user-value unit. Must have a `user_value` statement and at least one `acceptance` criterion. Reviewed by `requirement-auditor` when all tasks are done.

**Task** — the atomic unit of execution. Single action, single target. Reviewed by `implementation-reviewer` when done. Tasks may not nest sub-tasks.

---

## Schema Constraints

`Planner-Critic` rejects any plan that violates these constraints. `plan_lint.sh` enforces them as a script check:

| Constraint | Value |
|---|---|
| Slice must have `user_value` | required |
| Slice must have ≥1 `acceptance` | required |
| Task `action` must start with a verb | required |
| Plan tree must trace user intent → outcome | required |
| Task may not nest sub-tasks | enforced |
| At most one phase with `kind: "recovery"` | enforced |
| Plan and decisions log content language matches the user's input language | required |

There is no upper bound on phase / slice / task counts — granularity is the planner's call.

### Language-match rule

The `meta.topic`, every `phase.title` / `phase.goal`, every `slice.title` / `slice.user_value` / `slice.acceptance[]`, every `task.action` / `task.target` / `task.evidence`, and every `decisions.jsonl` entry's human-readable fields (e.g. `reason`, `note`, `description`) **must be written in the same natural language the user used in their original `/run` (or `/run-strict`) topic argument.**

The point is auditability: the user must be able to open `plan.json` and `decisions.jsonl` and read what's there without translation. If the user typed Chinese, the plan body is Chinese. If the user typed English, the plan body is English. Mixed-language topics → the planner picks the dominant language and stays consistent throughout.

This rule does NOT apply to:
- Schema field names (always English: `meta`, `phases`, `tasks`, `evidence`, `verdict`, `kind`, etc.)
- Enum values (always English: `pending`, `in_progress`, `done`, `blocked`, `main`, `recovery`, `strict`, `normal`)
- Id strings (always ASCII: `P1`, `P1-S2-T3`, `P_recovery-S1`)
- File paths and code identifiers in `task.target` (always literal)
- Tool names, command names, library names, error messages copied verbatim from tools

`planner-critic` checks language consistency at plan-write time and rejects plans whose body strings drift from the topic's language.

---

## State Machine

Each node (Plan, Phase, Slice, Task) independently tracks status:

```
pending → in_progress → done
                      → blocked
```

Transitions:
- `pending → in_progress`: execution begins (task) or first child moves to `in_progress` (phase/slice/plan)
- `in_progress → done`: all children are `done` AND the relevant reviewer passes
- `in_progress → blocked`: 3 consecutive reviewer failures on the same target, OR `guard.sh` halt condition triggered

**Invariant**: At most 1 task is `in_progress` at any time across the entire tree. The main loop enforces this: it picks the first `pending` task in DFS order, marks it `in_progress`, executes, then marks it `done` or `blocked` before moving to the next.

---

## Canonical JSON Schema

The full JSON Schema document is at `seeds/plan.schema.json` in the skill, and is copied by `init.sh` into each project at `.claude/state/plan.schema.json`. This is the source of truth for field names, types, and required/optional status. `plan_lint.sh` validates `plan.json` against this schema before each execution step.

---

## Example Minimal Plan

```json
{
  "meta": { "id": "plan-20260407-001", "topic": "Add search feature", "status": "in_progress" },
  "phases": [
    {
      "id": "P1", "title": "Backend", "goal": "Search API returns results", "status": "in_progress",
      "slices": [
        {
          "id": "P1-S1", "title": "Query endpoint",
          "user_value": "User can search by keyword and get matching records",
          "acceptance": ["GET /search?q=foo returns 200 with results array"],
          "status": "in_progress",
          "tasks": [
            { "id": "P1-S1-T1", "action": "Write search service method", "target": "src/search/service.py", "status": "done", "evidence": "function search() defined, returns list" },
            { "id": "P1-S1-T2", "action": "Add GET /search route", "target": "src/search/router.py", "status": "in_progress", "evidence": "" }
          ]
        }
      ]
    }
  ]
}
```
