---
description: Drive a long-running plan to PROVABLE end-to-end completion via strict 5-reviewer loop
---

# /run-strict — Strict-mode Long Task Driver

Argument: $ARGUMENTS (the topic, in natural language)

## When to use this instead of `/run`

Use `/run-strict` when partial completion is unacceptable: production rollouts, customer-facing features, anything where "done" must mean "actually delivered end-to-end". `/run-strict` is slower (more reviewer rounds, more repair cycles) but refuses to declare done until a 5th reviewer (`topic-auditor`) verifies the original topic is delivered.

For everyday refactors, exploration, and lower-stakes changes, use `/run`.

## Hard rules (in addition to /run's hard rules)

- **`plan.meta.mode = "strict"`** is set at bootstrap and never changes.
- **All 5 reviewers honor strict-mode addenda**: `planner-critic` enforces the Universal Completion Chain on the plan; `implementation-reviewer` enforces observable-proof evidence per task; `topic-auditor` is the terminal gate.
- **Progress-aware strike rule**: same-target failures count toward the 3-strike halt only when the reviewer's `issues[]` text is normalized-equal between rounds. If the issue is evolving, repair continues unbounded.
- **`plan.meta.status = "done"` may only be written after `topic-auditor` returns `verdict: pass`.**

## 0. Bootstrap

Three cases for `.claude/state/plan.json`:

1. **Missing** → run `bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"`, then write `{"meta":{"mode":"strict"}}` (a sentinel — §1 will fill the rest). Also delete `.claude/state/strike-state.json` if it exists. Proceed to §1.

2. **Empty seed** (file is `{}`, or has no `phases` array, or `phases` is empty) → no real plan exists yet. Set `meta.mode = "strict"` and proceed silently to §1.

3. **Real unfinished plan** (file has at least one phase AND `meta.status != "done"`) → ask the user once: `"Existing unfinished plan found. (o)verwrite / (r)esume / (a)bort?"`
   - `o` → archive current plan to `.claude/state/archive/plan-$(date +%s).json`, reset plan.json to `{"meta":{"mode":"strict"}}`, also reset `.claude/state/strike-state.json` to `{}`, proceed to §1
   - `r` → invoke `/resume` instead (resume preserves whatever mode the archived plan had)
   - `a` → exit

This is the only time you ask the user anything during the entire `/run-strict` lifecycle.

## 1. Write plan

Same as `/run` §1, but the plan must include `"meta": {..., "mode": "strict"}` and every phase must include `"kind": "main"` (recovery phases are added later, by topic-auditor failures, not by the planner).

No hard upper bound on phase / slice / task counts — pick the granularity the topic genuinely needs. The strict-mode `planner-critic` addendum (Universal Completion Chain) is what catches under-specification, not arbitrary caps. The `P_recovery` phase added later by `topic-auditor` follows the same rules as main phases.

## 2. Validate plan

Dispatch `planner-critic`. Strict-mode addendum activates automatically because `plan.meta.mode == "strict"`. If `verdict == fail`:

- Re-write the plan addressing every issue, **including** every Universal Completion Chain gap
- Re-dispatch
- Apply the **progress-aware strike rule** (see §5 below): only halt if the issue text is normalized-equal three rounds in a row

## 3. Execute loop

Identical to `/run` §3, except:

- Each `implementation-reviewer` dispatch sees `plan.meta.mode == "strict"` and applies the observable-proof rule.
- The strike counter is progress-aware (see §5).
- `guard.sh` is invoked on every shell command this executor runs (unchanged from `/run` §3). The `topic-auditor` reviewer dispatched in §4 honors its own guard.sh requirement per its agent prompt — the executor does not need to pre-guard those commands.

## 4. Slice / phase / plan completion

Identical to `/run` §4, with one critical addition: **before** writing `plan.meta.status = "done"` at the end, dispatch `topic-auditor`.

```
if all main phases done AND (no P_recovery exists OR P_recovery is fully done):
  dispatch topic-auditor
  if verdict == fail:
    if P_recovery does not exist:
      append a new phase: {id: "P_recovery", kind: "recovery", title: "Topic-auditor recovery", goal: "Patch missing chains", status: "in_progress", slices: []}
    for each missing_chain:
      append a new slice to P_recovery (id: P_recovery-S<n>)
      append the implied tasks under it
    set plan.meta.current_phase_id = "P_recovery"; persist
    persist; continue main loop (re-execute the new slices)
  else:
    dispatch planner-critic for final pass
    bash ~/.agents/skills/self-improving-workflow/scripts/crystallize.sh .claude
    set plan.meta.status = "done"; persist
    EXIT cleanly
```

`topic-auditor` may run multiple times — each `fail` injects more slices into the same `P_recovery`. Apply the progress-aware strike rule here too.

## 5. Progress-aware strike rule

Replace the simple "3 consecutive fails on same target → blocked" with:

```
on each reviewer fail for target T from reviewer R:
  current_hash = sha1(normalize(review.issues))
  if state[T,R].last_hash == current_hash:
    state[T,R].strike += 1
  else:
    state[T,R].strike = 1
    state[T,R].last_hash = current_hash

  if state[T,R].strike == 3:
    append decisions.jsonl: {kind:"blocked", scope:T, reviewer:R, reason:"same issue 3 rounds"}
    set target.status = "blocked"; set plan.meta.status = "blocked"; persist; EXIT
```

`normalize(issues)` strips whitespace, lowercases, and collapses runs of whitespace. This catches "the reviewer is stuck on the literal same complaint" without halting on slow-but-progressing fixes.

State for the strike counters is persisted to `.claude/state/strike-state.json` after each update so that `/resume` can pick up where the previous run left off. Format:

```json
{
  "<target>::<reviewer>": {"last_hash": "<sha1>", "strike": <int>},
  ...
}
```

The `strike-state.json` file is rewritten atomically (temp file + rename) on every counter change. On `/run-strict` start in case 1 (missing plan), or case 3-overwrite, the file is deleted. On case 2 (empty seed) or case 3-resume, it is loaded and the counters resume from their persisted values. This means a stuck loop cannot evade the strike rule by triggering a session restart.

## 6. Decision log discipline

Same as `/run` §5, plus: every dispatch of `topic-auditor` is logged as `kind: "audit"` with the reviewer's verdict and missing_chains count.

## 7. Crystallization

Same as `/run` §6. Crystallization happens after `topic-auditor` passes, before `status = done` is written.

## 8. Persistence atomicity

Same as `/run` §7. Write plan.json via temp file + rename.
