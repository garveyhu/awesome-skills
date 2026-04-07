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

## Hard Schema Limits

`Planner-Critic` rejects any plan that violates these limits. `plan_lint.sh` enforces them as a script check:

| Limit | Value |
|---|---|
| Slice must have `user_value` | required |
| Slice must have ≥1 `acceptance` | required |
| Task `action` must start with a verb | required |
| Tasks per slice | ≤ 7 |
| Slices per phase | ≤ 5 |
| Phases per plan | ≤ 4 |
| Task may not nest sub-tasks | enforced |

These limits exist to prevent scope creep from accreting invisibly inside the plan tree. A plan that can't fit into 4×5×7 needs to be descoped, not expanded.

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

The full JSON Schema document is at `templates/state/plan.schema.json`. This is the source of truth for field names, types, and required/optional status. `plan_lint.sh` validates `plan.json` against this schema before each execution step.

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
