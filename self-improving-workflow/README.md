# self-improving-workflow

> A universal methodology skill for Claude Code projects. No tech stack templates. No tier system. Two pillars.

> 中文版：[README.zh-CN.md](README.zh-CN.md)

## Two Pillars

**Pillar 1 — Multi-Agent Collaborative Learning**

Four specialist sub-agents review every plan, task, slice, and phase. Their findings auto-crystallize into project rules without requiring human intervention at each step.

| Reviewer | Triggers on |
|---|---|
| `planner-critic` | every new plan / re-plan |
| `implementation-reviewer` | every task done |
| `requirement-auditor` | every slice done |
| `integration-checker` | every phase done |

**Pillar 2 — Long-Running Uninterrupted Execution**

Single `/run <topic>` drives a hierarchical plan (`phase → slice → task`, limits: 4×5×7) to completion. Halts only on:
1. `guard.sh` detects an irreversible operation (data loss, remote write, credential mutation, shared comms, process kill)
2. 3 consecutive review failures on the same target

Every non-trivial decision is logged to `.claude/state/decisions.jsonl` for post-hoc audit.

---

## Quickstart

From your project root, after the skill is installed in `~/.agents/skills/`:

```
# Start a fully autonomous plan-and-execute loop
/run implement the user search feature

# Plan only — review without executing
/plan refactor the auth module

# Resume an interrupted plan
/resume
```

The first time `/run` is called, `init.sh` bootstraps the `.claude/` skeleton automatically (idempotent; existing files are never overwritten).

---

## Commands

| Command | Purpose |
|---|---|
| `/run <topic>` | Main entrypoint — full autonomous plan + execute + review loop |
| `/plan <topic>` | Plan only, no execution; Planner-Critic review included |
| `/review [scope]` | Dispatch reviewers diagnostically, read-only |
| `/learn` | Manual crystallization of episodic memory → rules |
| `/resume` | Continue an unfinished plan from first non-done task |

---

## File Layout — Project Side (`.claude/`)

After `init.sh` runs in your project:

```
.claude/
├── CLAUDE.md
├── commands/
│   ├── run.md
│   ├── plan.md
│   ├── review.md
│   ├── learn.md
│   └── resume.md
├── agents/
│   ├── planner-critic.md
│   ├── implementation-reviewer.md
│   ├── requirement-auditor.md
│   └── integration-checker.md
├── rules/
│   ├── autonomy-stops.md
│   └── dev-lessons.md
├── state/
│   ├── plan.json
│   ├── plan.schema.json
│   ├── decisions.jsonl
│   └── archive/
└── memory/
    ├── README.md
    ├── episodic/          (gitignored)
    ├── semantic-patterns.json  (git-tracked)
    └── working/           (gitignored)
```

`.gitignore` is patched idempotently to exclude `episodic/` and `working/`.

---

## Skill Repo Layout

```
self-improving-workflow/
├── SKILL.md
├── README.md / README.zh-CN.md
├── scripts/
│   ├── init.sh            ← bootstrap, no tier/stack/compliance args
│   ├── guard.sh           ← irreversible-op regex check
│   ├── crystallize.sh     ← episodic→semantic→rules promotion
│   └── plan_lint.sh       ← plan.json schema validation
├── templates/             ← single directory, no tier subdirs
│   ├── CLAUDE.md.template
│   ├── commands/{run,plan,review,learn,resume}.md.template
│   ├── agents/{planner-critic,implementation-reviewer,
│   │          requirement-auditor,integration-checker}.md.template
│   ├── rules/{autonomy-stops,dev-lessons}.md.template
│   ├── state/{plan.schema.json,.gitkeep}
│   └── memory/{README.md.template,episodic/.gitkeep}
└── references/
    ├── methodology.md
    ├── plan-schema.md
    ├── reviewer-contracts.md
    ├── learning-loop.md
    └── migration-from-tiered.md
```

---

## Reference

- [`references/methodology.md`](references/methodology.md) — why two pillars and the hybrid architecture approach
- [`references/plan-schema.md`](references/plan-schema.md) — phase/slice/task tree shape and hard limits
- [`references/reviewer-contracts.md`](references/reviewer-contracts.md) — four reviewer triggers and IO shapes
- [`references/learning-loop.md`](references/learning-loop.md) — episodic→semantic→rules crystallization algorithm
- [`references/migration-from-tiered.md`](references/migration-from-tiered.md) — upgrading from the old tiered version
