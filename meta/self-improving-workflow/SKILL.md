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

A universal methodology skill. No tech stack templates. No tier system. Two pillars.

## ⚡ First action when this skill is invoked — bootstrap

Whenever this skill is loaded (the user invoked it by name, or a trigger word matched), **immediately do the following before anything else**:

1. Run the bootstrap:
   ```bash
   bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"
   ```
2. Check the output:
   - If it created files (commands/, agents/, state/, memory/, rules/) → tell the user: *"Workflow scaffold installed in `.claude/`. You can now use `/run <topic>` to start an autonomous task, or `/plan <topic>` to plan only. See `.claude/CLAUDE.md` for the full operating contract."* Then **stop and wait** for the user's next instruction.
   - If everything was skipped (already initialized) → tell the user: *"Workflow already initialized. Use `/run <topic>` to start, `/resume` to continue an unfinished plan, or `/review` for a read-only diagnostic."* Then **stop and wait**.

This is the only purpose of invoking the skill by name. The skill is **not** an entrypoint that itself plans or executes — it lays down the slash commands and reviewer subagents into `.claude/`, after which the user drives everything via `/run`, `/plan`, `/resume`, etc.

Init is idempotent and write-once per file: it never overwrites your `CLAUDE.md`, your rules, or any local edits to commands/agents.

## The two pillars

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

Single `/run <topic>` command drives a hierarchical plan (`phase → slice → task`) to completion. **Only stops on**:

1. `guard.sh` blocks an irreversible operation (data loss, remote irreversible, credentials, shared comms, process kill)
2. 3 consecutive review failures on the same target

Decision log at `.claude/state/decisions.jsonl` records every non-trivial choice for post-hoc audit.

## Commands

Slash commands are mirrored from the skill into each project's `.claude/commands/` on bootstrap, so Claude Code can discover them. Re-running `init.sh` picks up new commands added to the skill in future versions.

| Command | Purpose |
|---|---|
| `/run <topic>` | The main entrypoint |
| `/run-strict <topic>` | Strict mode — 5-reviewer loop, refuses to mark done until topic-auditor verifies end-to-end delivery |
| `/plan <topic>` | Plan only, no execution |
| `/review [scope]` | Diagnostic, read-only |
| `/learn` | Manual crystallization |
| `/resume` | Continue an unfinished plan |

## Reviewer subagents

The five reviewers are mirrored from the skill into `.claude/agents/` on bootstrap (same reason — Claude Code only discovers subagents under `.claude/agents/` or `~/.claude/agents/`). The 5th reviewer (`topic-auditor`) only fires under `/run-strict`; the other four are used by both `/run` and `/run-strict`. Customize project-specific rubric items via `.claude/rules/dev-lessons.md` instead of forking the prompts.

## Strict mode

`/run-strict` is the opt-in stricter sibling of `/run`. Use it when partial completion is unacceptable. Three differences from `/run`:

1. **Universal Completion Chain enforcement** — `planner-critic` rejects plans where any acceptance item lacks a task chain reaching observable proof (test output, command stdout, file content, log line, etc. — never just "commit sha").
2. **Observable-proof evidence per task** — `implementation-reviewer` rejects task evidence that's just a commit sha. Static-only changes can use `static-only: <reason>` as an explicit exemption.
3. **5th reviewer `topic-auditor`** — runs once after all phases done, before the loop is allowed to write `plan.meta.status = "done"`. May execute read-only smoke commands (`pytest`, `curl`, `cat`, etc.) to verify end-to-end delivery against `plan.meta.topic`. If anything is missing, injects new slices into the single `P_recovery` phase.

Strict mode also uses a **progress-aware strike rule**: same-target failures only count toward the 3-strike halt when the reviewer's complaint is unchanged round-to-round. Slow-but-progressing repair never gets killed.

Tradeoff: `/run-strict` runs 2-5× longer than `/run`. Use it when you mean it.

## What bootstrap seeds

`scripts/init.sh` seeds the project's `.claude/` (see the top of this file for when it runs):

- `commands/` and `agents/` — mirrored from the skill (write-once per file, so Claude Code can discover them)
- `state/` — `plan.json`, `decisions.jsonl`, `plan.schema.json`, `archive/`
- `memory/` — `episodic/`, `working/`, `semantic-patterns.json`
- `rules/autonomy-stops.md`, `rules/dev-lessons.md`
- `CLAUDE.md` — only if the project doesn't already have one

Only `scripts/` stays in the skill repo and is invoked by absolute path from the commands.

## See also

- `references/methodology.md` — the why behind the two pillars
- `references/plan-schema.md` — full plan model
- `references/reviewer-contracts.md` — IO contract for each reviewer
- `references/learning-loop.md` — crystallization algorithm
- `references/migration-from-tiered.md` — upgrade from the old tiered version
