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

## Commands

Slash commands live at the skill itself (`commands/*.md`) — no copy step. They are available the moment the skill loads.

| Command | Purpose |
|---|---|
| `/run <topic>` | The main entrypoint |
| `/plan <topic>` | Plan only, no execution |
| `/review [scope]` | Diagnostic, read-only |
| `/learn` | Manual crystallization |
| `/resume` | Continue an unfinished plan |

## Reviewer subagents

The four reviewers also live at the skill (`agents/*.md`), shared across every project. Customize project-specific rubric items via `.claude/rules/dev-lessons.md` instead of forking the prompts.

## Bootstrap

First time `/run` is invoked, `scripts/init.sh` seeds **per-project state** into `.claude/` (state, memory, rules, CLAUDE.md). Idempotent, write-once. Existing files are never overwritten — `CLAUDE.md` triggers a `.skill-template` companion.

## See also

- `references/methodology.md` — the why behind the two pillars
- `references/plan-schema.md` — full plan model
- `references/reviewer-contracts.md` — IO contract for each reviewer
- `references/learning-loop.md` — crystallization algorithm
- `references/migration-from-tiered.md` — upgrade from the old tiered version
