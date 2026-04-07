# Self-Improving-Workflow Skill Refactor — Design

**Date**: 2026-04-07
**Status**: Approved (brainstorming session)
**Author**: Links + Claude (brainstorming skill)

## 1. Problem

Existing skill (`~/.agents/skills/self-improving-workflow`) has drifted from its intent:

- Coupled to specific tech stacks (Java/Python/React templates, compliance presets)
- Three-tier system (`minimal/standard/full`) is noise — adds files, not capability
- "Self-improving" is a manual `/self-improve` lesson sink, not a closed loop
- Phase protocols stop at "wait for user confirmation" — no long-running execution
- No central plan model; each slash command operates ad-hoc

The two things the skill should actually be about — **multi-agent collaborative learning** and **long-running uninterrupted execution** — are absent or weakly expressed.

## 2. Goals

Refactor into a **universal methodology skill**, fully tech-stack and project agnostic, built on two pillars:

1. **Multi-agent collaborative learning** — every plan, slice, task and phase is reviewed by 4 specialist sub-agents whose findings auto-crystallize into project rules.
2. **Long-running uninterrupted execution** — single `/run` entrypoint drives a hierarchical plan to completion fully autonomously; only halts on physically irreversible operations or 3 consecutive review failures.

### Non-goals

- Tech-stack templates (no Python/Java/React-specific files)
- Compliance presets (no govt/fintech/healthcare)
- Tier system
- `coding-bans.md` / `module-isolation.md` / `domain-compliance.md` as out-of-the-box files (these grow naturally inside `dev-lessons.md` via crystallization)

## 3. Six Pivotal Decisions

| # | Decision | Value |
|---|---|---|
| 1 | Autonomy boundary | Pure autonomous; only halt on physically irreversible ops |
| 2 | Plan granularity | `phase → slice → task` 3-level tree |
| 3 | Reviewer roster | Planner-Critic, Implementation-Reviewer, Requirement-Auditor, Integration-Checker |
| 4 | Learning loop | Fully automatic threshold crystallization (no human gate) |
| 5 | Tier system | Killed; one unified methodology |
| 6 | Entrypoint | Single `/run` command drives the entire closed loop |

## 4. Architecture Approach

**Hybrid (Approach C)**: Claude-native AI parts (`.claude/commands/*.md`, `.claude/agents/*.md`) + script-deterministic state parts (`scripts/guard.sh`, `scripts/crystallize.sh`, `scripts/plan_lint.sh` and `.claude/state/*.json`).

Reasoning:
- AI reasoning (planning, reviewing, code writing, re-planning) → Claude native
- State machine (plan tree, decision log, learning thresholds) → scripts, schema files
- Cross-session resumability requires schema-strict state, not LLM-managed JSON
- Threshold crystallization is a deterministic condition; LLM judgment drifts

## 5. Plan Model

```
Plan { meta, phases }
  Phase { id, title, goal, status, slices }
    Slice { id, title, user_value, acceptance[], status, tasks }
      Task { id, action, target, status, evidence }
```

**Hard schema limits** (Planner-Critic rejects on violation):

| Limit | Value |
|---|---|
| Slice must have `user_value` | required |
| Slice must have ≥1 `acceptance` | required |
| Task action must start with verb | required |
| Tasks per slice | ≤ 7 |
| Slices per phase | ≤ 5 |
| Phases per plan | ≤ 4 |
| Task may not nest sub-tasks | enforced |

**State machine**: `pending → in_progress → done | blocked`. At most 1 task in `in_progress` at any time across the whole tree.

**Storage**: `.claude/state/plan.json` (single file, atomic rewrites).

## 6. Multi-Agent Review Loop

Four reviewers, each as a `.claude/agents/*.md` Claude Code subagent. Read-only; never modify code; surface findings as structured JSON.

| Reviewer | Trigger | Reads | Output |
|---|---|---|---|
| **Planner-Critic** | After plan write / each re-plan | plan.json + topic + dev-lessons | verdict + issues |
| **Implementation-Reviewer** | After each task `done` | task evidence + dev-lessons | verdict + issues |
| **Requirement-Auditor** | After all slice tasks done | slice.user_value + acceptance + evidence | verdict + coverage_gap |
| **Integration-Checker** | After all phase slices done | phase products + adjacent phase acceptance | verdict + seams |

### Output schema (uniform)

```json
{
  "reviewer": "implementation-reviewer",
  "target": "P1-S1-T2",
  "verdict": "pass" | "fail",
  "severity": "P0" | "P1" | "P2",
  "issues": [
    {"what": "...", "why": "...", "fix_hint": "...",
     "category": "logic|boundary|spec|integration|style|risk"}
  ],
  "lessons_candidate": [
    {"pattern": "...", "evidence": "...", "confidence": 0.0-1.0}
  ]
}
```

### Constraints

- Reviewers only read; findings flow back into plan as new tasks/slices
- Reviewers run blocking; same-level reviewers can be parallel-dispatched
- Consecutive 3 fails on any reviewer → target marked `blocked` → plan blocked

## 7. Autonomy & Decision Log

### Halt conditions (only two)

1. **Irreversible operation detected** — `scripts/guard.sh` regex blocks the bash command, main loop catches `IRREVERSIBLE_BLOCKED`, writes decision log, exits.
2. **3 consecutive review fails** on the same target.

### Irreversible operation categories (`autonomy-stops.md`)

| Class | Examples |
|---|---|
| Data loss | `rm -rf` outside working tree, `git reset --hard` discarding uncommitted, drop db table |
| Remote irreversible | `git push --force` to non-personal branch, delete remote branch, PR merge, prod deploy |
| Credentials | edit `.env`/secrets, rotate token, paid external API |
| Shared comms | email/Slack/issue/PR comment, webhook |
| Process | `kill -9` non-self-spawned, stop db/container service |

User can append to this file; cannot remove seeded entries.

### Non-irreversible decisions: AI decides

Library choice, naming, mock vs real, caching — AI picks, writes `decisions.jsonl` entry with `kind=choice` and `why`. No user prompt.

### `decisions.jsonl` schema

Append-only JSONL. Four `kind`s:

- `choice` — non-obvious design decision
- `replan` — plan rewritten by reviewer feedback
- `error` — task failed + repair attempted
- `blocked` — halt condition triggered

### `/resume`

- Reads plan.json + tail of decisions.jsonl
- Continues from first non-`done` task
- If plan status is `blocked`, requires `--force-resume` flag

## 8. Learning Loop (Crystallization)

### Three-layer memory

```
.claude/memory/
├── episodic/             ← raw records, 1 file per event
├── semantic-patterns.json ← aggregated patterns (git tracked)
└── working/              ← session-scope cache (gitignored)

.claude/rules/
└── dev-lessons.md         ← crystallized rules (auto-loaded by Claude)
```

### Episodic record format

```json
{
  "id": "ep-20260407-1142",
  "ts": "...",
  "plan_id": "...",
  "scope": "P1-S2-T3",
  "source": "implementation-reviewer",
  "category": "boundary|logic|spec|integration|style|risk|process",
  "what": "...",
  "why": "...",
  "fix": "...",
  "fingerprint": "<category>:<sub>:<area>",
  "confidence": 0.0-1.0
}
```

`fingerprint` is generated by the writing reviewer, not by LLM at crystallize time.

### Crystallization algorithm (`scripts/crystallize.sh`)

```
for each new episodic E since last run:
  key = first 2 segments of E.fingerprint
  upsert pattern[key] (occurrences++, running avg confidence,
                       append episodic_id, update last_seen)

for each pattern P where not promoted_to_rule:
  if P.occurrences >= 3 AND P.avg_confidence >= 0.7:
    append rule entry to dev-lessons.md
    P.promoted_to_rule = true
    write decision log: kind=learn, scope=global
```

**Thresholds are hard-coded**: `≥3 occurrences AND ≥0.7 avg_confidence`. Not user-tunable.

### Triggers

- Each task `done` → reviewer writes episodic if it has `lessons_candidate`
- Each phase `done` → auto-run `crystallize.sh`
- `/run` exit → final `crystallize.sh`
- `/learn` manual → run anytime

### dev-lessons.md write template

```markdown
## L-{id}: {title}

**Rule**: ...

**Why**: ...

**How to apply**: ...

<!-- Crystallized: {date} | pattern: {fingerprint} | from {N} episodics | confidence: {avg} -->
```

Append-only. Conflicts marked `⚠ superseded by L-{new}`, never deleted automatically.

## 9. `/run` Main Loop (Pseudocode)

```
/run <topic>:
  bootstrap if needed (init.sh, idempotent)
  if existing unfinished plan: prompt overwrite (only user interaction point)

  AI writes initial plan.json
  dispatch Planner-Critic
    fail → re-plan; 3-fail → blocked exit
    pass → enter execute loop

  while plan.status != done:
    task = pick first pending in DFS
    if task is None:
      if slice all done: dispatch Req-Auditor → fail injects new tasks; pass marks slice done
      if phase all done: dispatch Integration-Checker → fail injects new slices; pass marks phase done
      if plan all done: final Planner-Critic; crystallize; mark done; break
      continue

    mark task in_progress
    AI executes (each bash command pre-checked by guard.sh)
      guard hit → write decisions blocked → exit
    write evidence
    mark task done
    dispatch Implementation-Reviewer
      fail → repair; 3-fail → blocked exit
      pass → write episodic if lessons_candidate → continue
```

## 10. Five Slash Commands

| Command | Args | Side effects | Exit |
|---|---|---|---|
| `/run <topic>` | topic | full closed loop | done / blocked |
| `/plan <topic>` | topic | write plan + Planner-Critic only | plan passes critic |
| `/review [scope]` | optional id | reviewer dispatch only, no repair | reviewers return |
| `/learn` | — | crystallize.sh | script exit |
| `/resume` | `[--force-resume]` | continue from first non-done task | same as /run |

### Invariants

1. ≤1 task `in_progress` at any time
2. `decisions.jsonl` append-only
3. `dev-lessons.md` append-only (supersede markers, not deletes)
4. `/run` exit → plan must be `done | blocked`
5. Every reviewer fail → episodic or decision log entry
6. `guard.sh`-rejected commands never execute

### Task idempotency

To survive session interruption: any task must be safely re-executable. `Implementation-Reviewer` checks idempotency as part of its rubric. Non-idempotent operations (random tokens, inserts) must include in-task pre-checks.

## 11. Skill Repo Layout

```
self-improving-workflow/
├── SKILL.md                    ← rewrite, two-pillar description
├── README.md / README.zh-CN.md ← rewrite
├── scripts/
│   ├── init.sh                ← rewrite, no tier/stack/compliance args
│   ├── guard.sh               ← NEW: irreversible-op regex check
│   ├── crystallize.sh         ← NEW: episodic→semantic→rules promotion
│   └── plan_lint.sh           ← NEW: plan.json schema validation
├── templates/                 ← single dir, no tier subdirs
│   ├── CLAUDE.md.template
│   ├── commands/{run,plan,review,learn,resume}.md.template
│   ├── agents/{planner-critic,implementation-reviewer,requirement-auditor,integration-checker}.md.template
│   ├── rules/{autonomy-stops,dev-lessons}.md.template
│   ├── state/{plan.schema.json,.gitkeep}
│   └── memory/{README.md.template,episodic/.gitkeep}
└── references/
    ├── methodology.md
    ├── plan-schema.md
    ├── reviewer-contracts.md
    └── learning-loop.md
```

### Files to delete

- `templates/{minimal,standard,full}/`
- `references/tier-comparison.md`
- `references/compliance-presets.md`
- `references/existing-project-guide.md`
- `scripts/upgrade.sh`
- `scripts/detect.sh`

## 12. Project-Side Output (`<project>/.claude/`)

```
.claude/
├── CLAUDE.md
├── commands/{run,plan,review,learn,resume}.md
├── agents/{planner-critic,implementation-reviewer,requirement-auditor,integration-checker}.md
├── rules/{autonomy-stops,dev-lessons}.md
├── state/
│   ├── plan.json (initially {})
│   ├── plan.schema.json
│   ├── decisions.jsonl
│   └── archive/
└── memory/
    ├── README.md
    ├── episodic/      (gitignored)
    ├── semantic-patterns.json (git tracked)
    └── working/        (gitignored)
```

`init.sh` idempotently appends to `.gitignore`:
```
.claude/memory/episodic/
.claude/memory/working/
.claude/state/working/
```

## 13. Installation & Migration

- **Trigger**: first `/run <topic>` auto-runs `init.sh` if `.claude/` missing
- **Idempotent**: existing files skipped, untouched
- **CLAUDE.md exception**: existing → write `.skill-template` companion (preserved from old skill)
- **No upgrade path**: tiers gone → no upgrade command
- **Migration from tiered version**: `references/migration-from-tiered.md` documents manual steps; old `.claude/` continues to work independently

## 14. Open Items (deferred to implementation plan)

- Concrete `guard.sh` regex list (will iterate)
- `plan.schema.json` exact JSON Schema document
- Reviewer prompt templates (`agents/*.md` content)
- `crystallize.sh` language choice (bash + jq vs python)
- Whether `/run` should background-dispatch reviewers via Task tool or sequential

## 15. Acceptance Criteria

Refactored skill is "done" when:

1. `templates/` contains exactly one set (no tier subdirs); `scripts/` has init/guard/crystallize/plan_lint
2. Fresh `init.sh` on empty project produces the layout in §12 in one shot
3. `/run "topic"` on a trivial test project completes a full plan tree, writes ≥1 episodic, runs `crystallize.sh` at least at exit
4. `guard.sh` blocks at least one entry from each of the 5 irreversible categories
5. `crystallize.sh` promotes a synthetic 3-occurrence pattern into `dev-lessons.md` deterministically
6. `/resume` mid-plan correctly picks up at the first non-done task
7. SKILL.md description leads with the two pillars; trigger words include `/run`, `long task`, `multi-agent review`
8. No file under `templates/` mentions Python, Java, React, FastAPI, or any framework name
