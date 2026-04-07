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
