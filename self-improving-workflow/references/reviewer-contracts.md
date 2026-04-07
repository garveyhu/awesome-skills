# Reviewer Contracts — Four Specialists

## Trigger Matrix

| Reviewer | Trigger | Reads | Output |
|---|---|---|---|
| **Planner-Critic** | After plan write / each re-plan | `plan.json` + topic + `dev-lessons.md` | `verdict` + `issues` |
| **Implementation-Reviewer** | After each task `done` | task evidence + `dev-lessons.md` | `verdict` + `issues` |
| **Requirement-Auditor** | After all slice tasks `done` | `slice.user_value` + `acceptance[]` + task evidence | `verdict` + `coverage_gap` |
| **Integration-Checker** | After all phase slices `done` | phase products + adjacent phase acceptance | `verdict` + `seams` |

---

## Unified Output JSON Shape

All four reviewers emit the same JSON structure:

```json
{
  "reviewer": "implementation-reviewer",
  "target": "P1-S1-T2",
  "verdict": "pass",
  "severity": "P0",
  "issues": [
    {
      "what": "Missing null check on search result",
      "why": "Returns 500 when query matches no records",
      "fix_hint": "Return empty list, not None",
      "category": "boundary"
    }
  ],
  "lessons_candidate": [
    {
      "pattern": "Search endpoints must handle empty result set explicitly",
      "evidence": "P1-S1-T2 returned 500 on empty query",
      "confidence": 0.85
    }
  ]
}
```

Field notes:
- `verdict`: `"pass"` or `"fail"`. Pass means the reviewer found no blocking issues.
- `severity`: `"P0"` (blocks execution), `"P1"` (should fix), `"P2"` (cosmetic/optional). Relevant on `fail`.
- `issues[].category`: one of `logic | boundary | spec | integration | style | risk`.
- `lessons_candidate`: optional. When present, the learning loop writes an episodic record and runs threshold check.

---

## Core Constraints

### Reviewers only read; never write

Reviewers are read-only agents. They inspect plan state, evidence, dev-lessons, and code — but they never modify any file. All findings flow back through the main `/run` loop, which decides whether to inject new tasks, re-plan, or mark a target blocked.

This separation ensures that reviewer output is auditable and that the plan tree remains the single source of truth for what has been done and what needs to happen.

### 3 consecutive failures → blocked

If the same reviewer fails on the same target 3 times in a row:
- The target is marked `blocked`
- A `decisions.jsonl` entry of `kind=blocked` is written
- The `/run` loop halts and surfaces the block to the user

"Same target" means the same `phase.id`, `slice.id`, or `task.id`. A repair task injected in response to a failure resets the consecutive-fail counter for the repaired target.

### Same-level reviewers can be parallel-dispatched

When multiple reviewers trigger at the same level (e.g., final plan review runs Planner-Critic after Integration-Checker), they may be dispatched in parallel using the `Task` tool. Results are collected before the loop continues.

---

## Reviewer Agent Prompts

Each reviewer's behavior is defined in its agent prompt file, living at the skill itself:

- `agents/planner-critic.md`
- `agents/implementation-reviewer.md`
- `agents/requirement-auditor.md`
- `agents/integration-checker.md`

These files are skill-global, not per-project. Every project that uses the skill shares the same reviewer roster — there is no copy step. To customize per-project, append rubric items to `.claude/rules/dev-lessons.md` rather than forking the agent prompts.
