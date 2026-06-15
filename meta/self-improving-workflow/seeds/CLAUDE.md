# Project workflow — self-improving-workflow

This project uses the `self-improving-workflow` skill methodology. Two pillars:

1. **Multi-agent collaborative learning** — every plan, slice, task, and phase is reviewed by 4 specialist sub-agents (`planner-critic`, `implementation-reviewer`, `requirement-auditor`, `integration-checker`). Findings auto-crystallize into `.claude/rules/dev-lessons.md`.

2. **Long-running uninterrupted execution** — single `/run <topic>` entrypoint drives a hierarchical plan (phase → slice → task) to completion fully autonomously. Halts only on irreversible operations or 3 consecutive review failures.

## Commands

| Command | What it does |
|---|---|
| `/run <topic>` | Full closed-loop driver — bootstraps, plans, executes, reviews, learns |
| `/plan <topic>` | Plan only, no execution |
| `/review [scope]` | Read-only diagnostic across reviewers |
| `/learn` | Run crystallization manually |
| `/resume [--force-resume]` | Continue an unfinished plan |

## State

- `.claude/state/plan.json` — current plan tree
- `.claude/state/decisions.jsonl` — append-only decision log
- `.claude/memory/episodic/` — raw experiences (gitignored)
- `.claude/memory/semantic-patterns.json` — aggregated patterns (git-tracked)
- `.claude/rules/dev-lessons.md` — crystallized rules (auto-loaded; do not hand-edit)
- `.claude/rules/autonomy-stops.md` — irreversible-op blocklist (you may add)

## Operating principles

- Trust `/run` to make every non-irreversible decision. Don't pre-approve.
- The decision log is your audit window — read it after a long run, not during.
- New project conventions emerge naturally via crystallization. Don't pre-seed `dev-lessons.md`.
