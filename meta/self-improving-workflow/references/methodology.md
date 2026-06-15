# Methodology — Why Two Pillars

## What This Skill Is For

Self-improving-workflow is a **universal methodology skill** for Claude Code projects. It is fully tech-stack agnostic and project agnostic — it carries no Python templates, no Java scaffolding, no React starters, no compliance presets. Those concerns belong to the project, not to the methodology.

The skill encodes two capabilities that every non-trivial AI-assisted development project needs and that neither vanilla Claude Code nor the previous tiered scaffold provided:

1. **Multi-agent collaborative learning** — automated, closed-loop improvement of project rules from real development events.
2. **Long-running uninterrupted execution** — autonomous progression through a structured plan without requiring human checkpoints at every step.

---

## Why Pillar 1: Multi-Agent Collaborative Learning

### The problem with manual lesson capture

The previous skill provided `/self-improve` as a manual lesson-sink: the user remembered to run it, answered three prompts, and maybe a lesson got added. In practice, lessons are skipped when sessions are intense and forgotten when they're not. The improvement loop has a human bottleneck.

### The solution: four specialist reviewers

Four sub-agents review work at four distinct levels of abstraction. Each has a single responsibility and a defined trigger:

| Reviewer | Trigger | What it checks |
|---|---|---|
| `planner-critic` | every new plan / re-plan | plan quality, hard schema limits, alignment with dev-lessons |
| `implementation-reviewer` | every task `done` | code quality, boundary conditions, idempotency, spec adherence |
| `requirement-auditor` | every slice `done` | user-value coverage, acceptance criteria gaps |
| `integration-checker` | every phase `done` | seam correctness, phase boundary contracts |

Reviewers are read-only. They never modify code or files. They output structured JSON with `lessons_candidate` entries — fingerprinted patterns that feed into the learning loop automatically.

### Why four separate agents, not one

A single "review everything" agent loses specialization: plan-level structural issues (wrong verb in task action, slice with no acceptance criteria) are invisible to a reviewer focused on code logic. The four-reviewer roster mirrors what effective engineering teams actually do — separate architecture review, code review, requirement review, and integration review.

### Decision table context (§3 rows 3 & 4 of design doc)

| # | Decision | Value |
|---|---|---|
| 3 | Reviewer roster | Planner-Critic, Implementation-Reviewer, Requirement-Auditor, Integration-Checker |
| 4 | Learning loop | Fully automatic threshold crystallization (no human gate) |

Row 4 is critical: crystallization is deterministic and threshold-gated (`≥3 occurrences AND ≥0.7 avg_confidence`). No human approval step. When a pattern crosses the threshold, it becomes a rule. This removes the bottleneck from the improvement loop entirely.

---

## Why Pillar 2: Long-Running Uninterrupted Execution

### The problem with phase-stop protocols

The previous `/phase-start` and `/phase-review` commands required user confirmation at every phase boundary. For a three-phase plan, the user had to be present for three handoffs. For long tasks (multi-day implementation, large refactors, exploratory research), this is a blocking constraint — the user cannot delegate and walk away.

### The solution: a single `/run` entrypoint with only two halt conditions

`/run <topic>` drives a full `phase → slice → task` plan tree to completion. It halts only when:

1. `guard.sh` detects an irreversible operation (data loss, remote write, credential mutation, shared communications, process kill).
2. 3 consecutive review failures on the same target — meaning the AI has tried and failed three times and further automation would be noise.

Everything else — re-planning, repair, retry, reviewer dispatch — happens automatically.

### Decision table context (§3 rows 1 & 6 of design doc)

| # | Decision | Value |
|---|---|---|
| 1 | Autonomy boundary | Pure autonomous; only halt on physically irreversible ops |
| 6 | Entrypoint | Single `/run` command drives the entire closed loop |

Row 1 makes the boundary explicit: the skill trusts AI judgment on non-irreversible decisions (library choice, naming, mock vs real). It records these in `decisions.jsonl` for audit, but does not interrupt the user. Row 6 collapses five previous entry commands (`/init-workflow`, `/phase-start`, `/phase-review`, `/self-improve`, `/compile-check`) into one.

---

## Why Hybrid Claude-Native + Scripts (§4)

The implementation uses **Approach C — Hybrid**:

- **Claude-native** (`.claude/commands/*.md`, `.claude/agents/*.md`): AI reasoning — planning, reviewing, writing code, re-planning in response to feedback.
- **Script-deterministic** (`scripts/guard.sh`, `scripts/crystallize.sh`, `scripts/plan_lint.sh`, `.claude/state/*.json`): state machine — plan tree, decision log, learning thresholds.

The split is principled:

| Concern | Implementation | Why |
|---|---|---|
| Reasoning (plan, review, code) | Claude native | LLMs are good at this |
| State (plan tree, decisions) | JSON + scripts | Cross-session resumability requires strict schema |
| Crystallization threshold | `crystallize.sh` | Deterministic condition; LLM judgment on threshold drifts |
| Irreversible-op guard | `guard.sh` regex | Safety property; must not depend on LLM interpretation |

---

## Canonical Reference

If a section here ever drifts from the design doc at `docs/plans/2026-04-07-self-improving-workflow-refactor-design.md`, the design doc wins.

---

## Strict mode (`/run-strict`)

The everyday `/run` command is built for speed and tolerance: it accepts that some plans will be slightly under-specified and that not every task will have runtime evidence. For most exploratory and refactor work, that tradeoff is right.

But there's a class of tasks where partial completion is the wrong answer at any speed — production rollouts, customer-facing features, security work, anything where "done" must mean "actually delivered end-to-end". For those, `/run-strict` exists.

### What strict mode adds — three layers of defense

**Layer 1 — Plan-time gate.** `planner-critic` applies the Universal Completion Chain rule (see below). Plans that don't trace every acceptance item to observable proof are rejected before execution starts. The bad plan never wastes a single task.

**Layer 2 — Task-time gate.** `implementation-reviewer` rejects task evidence that doesn't include observable proof. Pure refactors use `static-only: <reason>` as an explicit escape hatch — anything else needs runtime evidence.

**Layer 3 — Plan-done gate.** A new 5th reviewer, `topic-auditor`, runs exactly once at the end of the plan, before the loop is allowed to write `meta.status = done`. It reads `plan.meta.topic` (the user's original ask), all evidence, and may execute read-only smoke commands (`pytest`, `curl`, `cat`, `--help`, etc.) to verify the deliverable in situ. If it says no, the missing chains are injected as new slices in the special `P_recovery` phase, and the execute loop re-enters. The plan only reaches `done` when topic-auditor says yes.

### Universal Completion Chain — the rule that drives all three layers

> For each acceptance item, the plan must contain a task chain that traces:
>
> **trigger → all components touched → observable proof**
>
> *Observable proof* means at least one of: test output, command stdout, generated file content, log line with sentinel, HTTP response body, rendered doc, or runnable example. Bare commit sha is not observable proof.

This rule is universal — it applies regardless of tech stack:

- **Feature code**: trigger = user action / API call → components = endpoint + service + DB → proof = response body + UI assertion
- **CLI tool**: trigger = command run → components = argparse + handlers → proof = exit code + stdout match
- **Refactor**: trigger = structural change → components = files moved → proof = old tests still pass + measured complexity drop
- **Doc**: trigger = reader question → components = sections written → proof = doc renders + executable example actually runs
- **Data pipeline**: trigger = input dataset → components = transforms → proof = output rows match snapshot
- **Library/SDK**: trigger = caller import → components = public API → proof = example calling code asserts
- **Investigation**: trigger = research question → components = sources read → proof = written conclusion + citations + reproducible commands

### Progress-aware strike rule

Strict mode replaces the simple "3 fails → blocked" rule with a progress-aware version:

> Same-target failures only count toward the 3-strike halt when the reviewer's `issues[]` text is normalized-equal between rounds. If the issue is evolving (the reviewer is finding new things to fix, or the executor is making progress against the old complaint), the counter resets.

Hard halt only when the reviewer is stuck on the literal same complaint three runs in a row — i.e. genuine stuckness. Slow-but-progressing repair runs unbounded. Strike state is persisted to `.claude/state/strike-state.json` so a session restart cannot evade the rule.

### When to use strict vs normal

| Situation | Use |
|---|---|
| Exploration, prototypes, refactors | `/run` |
| Customer-facing or production-bound features | `/run-strict` |
| Security or compliance work | `/run-strict` |
| One-off scripts, internal tools, dev experience tweaks | `/run` |
| Anything where "looks done" must equal "actually delivered" | `/run-strict` |

`/run-strict` is typically 2-5× slower than `/run` because of the extra reviewer rounds and the topic-auditor recovery loop. Use it when you mean it.
