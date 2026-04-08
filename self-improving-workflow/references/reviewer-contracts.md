# Reviewer Contracts — Five Specialists

## Trigger Matrix

| Reviewer | Trigger | Reads | Output |
|---|---|---|---|
| **Planner-Critic** | After plan write / each re-plan | `plan.json` + topic + `dev-lessons.md` | `verdict` + `issues` |
| **Implementation-Reviewer** | After each task `done` | task evidence + `dev-lessons.md` | `verdict` + `issues` |
| **Requirement-Auditor** | After all slice tasks `done` | `slice.user_value` + `acceptance[]` + task evidence | `verdict` + `coverage_gap` |
| **Integration-Checker** | After all phase slices `done` | phase products + adjacent phase acceptance | `verdict` + `seams` |
| **Topic-Auditor** *(strict mode only)* | After all phases `done`, before `plan.meta.status = done` | `plan.meta.topic` + all evidence + live read-only smoke commands | `verdict` + `missing_chains` |

---

## Unified Output JSON Shape

All five reviewers emit the same JSON structure:

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
- `issues[]` fields are exactly `what`, `why`, `fix_hint`, `category` — never renamed to `description`, `problem`, `file`, etc. File/line info goes inside `what`.
- `lessons_candidate[].pattern`: three-segment fingerprint `category:sub-area:scope`. The first two segments are the crystallization key.
- `lessons_candidate`: optional. When present, the learning loop writes an episodic record and runs threshold check.
- `missing_chains[]` (topic-auditor only): each entry has `acceptance_ref`, `what_is_missing`, `suggested_slice`. Same hard rule as coverage_gap and seams: non-empty → verdict must be fail.

---

## Hard Invariants (enforced by every reviewer)

These rules exist because the `/run` loop relies on them to decide whether to inject repair work. Violations silently drop findings.

### I1. Strict JSON output — no prose, no drift

Each reviewer's entire final response is a single JSON object matching the shape above (plus its specialist field: `coverage_gap` for requirement-auditor, `seams` for integration-checker). No preamble, no markdown fences around the top-level object, no extra top-level keys, no renamed fields. Field names are case-sensitive.

### I2. Verdict vs severity consistency

`verdict == "fail"` iff at least one `issues[]` entry has `severity` of `P0` or `P1`, **or** the reviewer's specialist field (`coverage_gap` / `seams` / `missing_chains`) is non-empty. A P2-only issue list with no specialist findings → `verdict == "pass"`.

### I3. Specialist-field vs verdict consistency (coverage_gap / seams)

A **coverage gap** (requirement-auditor) is a missing acceptance requirement. A **seam** (integration-checker) is a missing cross-slice bridge. Both are, by definition, blocking. The `missing_chains` field (topic-auditor) follows the same template — non-empty means blocking fail — see I5 for the topic-auditor specialization. Therefore:

> If `coverage_gap` is non-empty → `verdict` MUST be `"fail"` and `severity` MUST be `"P0"` or `"P1"`.
> If `seams` is non-empty → `verdict` MUST be `"fail"` and `severity` MUST be `"P0"` or `"P1"`.

If a finding feels "minor", the reviewer has exactly two choices:
1. Drop it from `coverage_gap` / `seams` and log it instead as a P2 entry in `issues[]` (observation only, no repair task).
2. Commit to `fail` and let the main loop inject the repair task/slice.

There is **no** third option of `pass` + non-empty specialist field. The `/run` loop only injects repair work on `fail`, so any such combination silently discards the finding — the exact failure mode I3 exists to prevent.

### I4. Three consecutive failures → blocked

Same reviewer failing on the same target three times in a row marks the target `blocked`, writes a `decisions.jsonl` entry (`kind=blocked`), and halts `/run` for user attention. A repair task injected in response to a failure resets the counter for the repaired target.

**Strict-mode override (replaces I4 above when running `/run-strict`):** the strike rule is progress-aware. The counter only increments when consecutive failures from the same reviewer on the same target carry a normalized-equal `issues[]` text (whitespace-stripped, lowercased, runs of whitespace collapsed). If the issue text changes between rounds, the counter resets to 1. Hard halt only when the same issue repeats three runs in a row — i.e. the reviewer is stuck on the literal same complaint, not just slowly making progress. This applies to all 5 reviewers under strict mode, including `topic-auditor`.

**Under normal `/run`, the original three-strike rule above applies unchanged** — there is no progress-aware counter outside strict mode.

### I5. Topic-auditor `missing_chains` consistency (strict mode only)

The 5th reviewer, `topic-auditor`, runs only under `/run-strict`. Its specialist field is `missing_chains[]` — entries describing acceptance items whose end-to-end delivery cannot be traced to observable proof.

> If `missing_chains` is non-empty → `verdict` MUST be `"fail"` and `severity` MUST be `"P0"` or `"P1"`.

A missing chain is by definition a broken delivery and cannot coexist with `verdict == "pass"`. The main loop converts each entry into a new slice in the (single) `P_recovery` phase, then re-enters the execute loop. The plan can only reach `meta.status = "done"` after `topic-auditor` returns `verdict: pass` with empty `missing_chains`.

**No downgrade path.** Unlike I3's `coverage_gap` and `seams` (which allow a reviewer to drop a finding to a P2 `issues[]` entry if it feels minor), `missing_chains` has no such escape hatch. The 5th reviewer is the terminal gate of strict mode — if the reviewer is unsure whether a chain is delivered, the safe answer is to add it as a `missing_chain` and let the recovery loop patch it. A topic-auditor that downgrades a real gap to a "P2 observation" defeats the entire purpose of `/run-strict`.

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

Each reviewer's behavior is defined in its agent prompt file, mirrored from the skill into the project on bootstrap (Claude Code only discovers subagents under `.claude/agents/`):

- `.claude/agents/planner-critic.md`
- `.claude/agents/implementation-reviewer.md`
- `.claude/agents/requirement-auditor.md`
- `.claude/agents/integration-checker.md`
- `.claude/agents/topic-auditor.md` *(strict mode only)*

The skill copy is the source of truth. Re-running `init.sh` after upgrading the skill picks up new reviewers, but write-once: any local edits in a project are never overwritten. To customize per-project, prefer appending rubric items to `.claude/rules/dev-lessons.md` over editing the agent prompts directly.
