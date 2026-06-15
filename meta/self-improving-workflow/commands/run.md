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

Three cases for `.claude/state/plan.json`:

1. **Missing** → run `bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"`, then write `{}` to plan.json. Proceed to §1.

2. **Empty seed** (file is `{}`, or has no `phases` array, or `phases` is empty) → no real plan exists yet, this is the freshly-seeded state. Proceed silently to §1 with no user prompt.

3. **Real unfinished plan** (file has at least one phase AND `meta.status != "done"`) → ask the user once: `"Existing unfinished plan found. (o)verwrite / (r)esume / (a)bort?"`
   - `o` → archive current plan to `.claude/state/archive/plan-$(date +%s).json`, reset plan.json to `{}`, proceed to §1
   - `r` → invoke `/resume` instead
   - `a` → exit

**This (case 3) is the only time you ask the user anything during the entire `/run` lifecycle.**

## 1. Write plan

Generate a plan.json for the topic following the schema in `.claude/state/plan.schema.json`. Use as many phases / slices / tasks as the topic genuinely needs — no hard upper bound, but every task must be atomic, every slice must deliver concrete user value, and the plan tree must trace from user intent to outcome. Reviewers and crystallization handle quality, not artificial caps.

**Language-match rule (hard)**: every human-readable field in the plan (`meta.topic`, every `title`, `goal`, `user_value`, `acceptance[]`, `action`, `target` description, `evidence`) MUST be written in the same natural language the user used in `$ARGUMENTS`. If the user wrote Chinese, the plan body is Chinese. If they wrote English, the plan body is English. The user must be able to open `plan.json` and read it without translation. Schema field names, enum values, id strings, file paths, and tool names stay as-is (always English/ASCII). See `references/plan-schema.md` for the full rule.

Write to `.claude/state/plan.json`.

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

**Language-match rule (hard)**: every human-readable field in a decision entry — `reason`, `note`, `description`, free-text `detail` — must use the same natural language as `plan.meta.topic`. The user must be able to `cat decisions.jsonl` and read it without translation. Field names (`kind`, `scope`, `target`, `reviewer`), enum values (`choice`, `replan`, `error`, `blocked`, `audit`), id strings, file paths, and verbatim tool/error output stay as-is.

## 6. Crystallization

Periodically (after each phase done, and at exit) run:
```bash
bash ~/.agents/skills/self-improving-workflow/scripts/crystallize.sh .claude
```
This is the only place new rules enter `dev-lessons.md`.

## 7. Persistence atomicity

When writing plan.json, write to a temp file then `mv` over the target. Never leave plan.json half-written.
