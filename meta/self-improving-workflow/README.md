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

Single `/run <topic>` drives a hierarchical plan (`phase → slice → task`) to completion. Halts only on:
1. `guard.sh` detects an irreversible operation (data loss, remote write, credential mutation, shared comms, process kill)
2. 3 consecutive review failures on the same target

Every non-trivial decision is logged to `.claude/state/decisions.jsonl` for post-hoc audit.

---

## Quickstart

From your project root, after the skill is installed in `~/.agents/skills/`:

```
# Step 1 (one time per project) — invoke the skill by name to bootstrap.
# This mirrors commands/ and agents/ into .claude/ so Claude Code can
# discover them, and seeds state/ and memory/.
/self-improving-workflow

# Step 2 — start a fully autonomous plan + execute + review loop
/run implement the user search feature

# Strict mode — refuses to mark done until topic-auditor verifies
# end-to-end delivery against the original topic. Slower but provable.
/run-strict ship the password reset feature with email sending

# Plan only — review without executing
/plan refactor the auth module

# Resume an interrupted plan
/resume
```

After step 1, the project has its own `.claude/{commands,agents,state,memory,rules}/`. Step 1 is idempotent — re-invoking the skill picks up new commands/agents from upgraded skill versions but never overwrites local edits.

---

## How It Works — From Surface to Internals

### One-line definition

**Hand the AI a long task; the AI plans, executes, self-reviews, and improves until done. Four reviewer agents keep each other honest along the way. Pitfalls are auto-crystallized into rules that govern the next run.**

### User's perspective — you do exactly 3 things

```
1. Install the skill (git clone awesome-skills; self-improving-workflow ships with it)
2. In any project, say one sentence: /run add a user login feature
3. Wait. Watch the terminal.
```

You make zero decisions in between. When the AI is finished, it tells you "done" or "blocked".

### AI's perspective — what `/run` actually does

Treat `/run` as a finite state machine:

```
[bootstrap]                                ← first run: init.sh seeds .claude/
     ↓
[write plan]                               ← AI splits the task into a phase→slice→task tree
     ↓
[planner-critic reviews the plan]          ← review 1: is the plan itself good enough?
     ↓ pass
[execute loop] ←──────────────────────────┐
     ↓                                      │
   pick next pending task                   │
     ↓                                      │
   guard.sh checks every bash command       │ irreversible hit → BLOCKED, exit
     ↓ allowed                              │
   AI writes code / runs tests / commits    │
     ↓                                      │
   [implementation-reviewer per task]       │ review 2: did this task get done right?
     ↓ pass                                 │
   slice all done? → [requirement-auditor]  │ review 3: does the slice fulfill its user_value?
     ↓ pass                                 │
   phase all done? → [integration-checker]  │ review 4: do the seams between slices line up?
     ↓ pass                                 │
   plan all done? → [crystallize.sh] → done │
     ↓ no                                   │
     └──────────────────────────────────────┘
```

**Only two halt conditions**:
1. `guard.sh` blocks an irreversible command (delete data / force-push / edit secrets / send webhook / kill -9 / drop table)
2. Three consecutive review failures on the same target (bad plan / unfixable task / missing requirement)

For any other "should I pick A or B" call, **the AI decides itself**, appends a line to `decisions.jsonl`, and keeps moving.

### Plan shape (the central data structure)

```
Plan
├── Phase 1 (no upper bound)
│   ├── Slice 1.1 — must have user_value and acceptance
│   │   ├── Task 1.1.1 — must start with a verb
│   │   ├── Task 1.1.2
│   │   └── ...
│   ├── Slice 1.2
│   └── ...
├── Phase 2
└── ...
```

`plan_lint.sh` enforces this schema with jq. If the AI writes a "100 tasks in one phase" monstrosity, `planner-critic` rejects it and the AI re-plans.

**Why three levels**: granularity maps to reviewer depth.
- task done → `implementation-reviewer` checks the code
- slice done → `requirement-auditor` checks whether the user value is actually delivered
- phase done → `integration-checker` checks whether interfaces / state / events line up across slices

### Four reviewer agents, each in its lane

| Agent | Triggered when | Reads | Fix on failure |
|---|---|---|---|
| **planner-critic** | plan written / re-planned | the plan + accumulated lessons | AI re-writes the plan |
| **implementation-reviewer** | each task completed | the task's code change | AI redoes the task |
| **requirement-auditor** | each slice completed | slice user_value + all task evidence | inject missing requirements as new tasks |
| **integration-checker** | each phase completed | seams across the phase's slices | inject missing seams as new slices |

**Hard constraint**: reviewers are **read-only**. They emit JSON reports (pass / fail + issues); the main loop applies the fix. This prevents reviewers from fighting the executor for the steering wheel.

### How the two pillars actually run

**Pillar 1 — Multi-Agent Collaborative Learning**

Not "many agents working together" in a vague sense. Three role classes are isolated:
- **Executor** (the main loop running tasks)
- **Four reviewers** (independent subagents, each in its lane)
- **Learner** (`crystallize.sh`, a deterministic script)

Concretely how it learns:

```
implementation-reviewer finds: "this task didn't validate null input"
    ↓
write an episodic record to .claude/memory/episodic/ep-xxx.json
    fingerprint: "boundary:null-input:user-service"
    confidence: 0.8
    ↓
crystallize.sh runs (after each phase done + at exit)
    ↓
aggregate: has fingerprint's first 2 segments "boundary:null-input"
    appeared 3+ times AND avg_confidence ≥ 0.7?
    ↓ yes
auto-append a rule to .claude/rules/dev-lessons.md
    ↓
on the next /run, planner-critic and implementation-reviewer
read dev-lessons.md and check the new rule against the plan and code
```

**Thresholds are hard-coded**: ≥3 occurrences AND ≥0.7 avg confidence. Not user-tunable. Intentional, to prevent users from dialing it to "learn less" or "learn more".

**Pillar 2 — Long-Running Uninterrupted Execution**

Not just "AI keeps running". The substance:
- **Decision authority delegated**: every non-irreversible decision is the AI's call (pick a lib, naming, cache or not, mock or real dep…)
- **Decisions are auditable**: `decisions.jsonl` is append-only, capturing every non-trivial choice with reasoning so you can replay later
- **Cross-session resume**: `plan.json` + `decisions.jsonl` are the state snapshot. If the process gets killed, `/resume` picks up at the first non-done task next time
- **Tasks must be idempotent**: rerunning a task after interruption must leave the system in the same state. `implementation-reviewer` includes idempotency in its rubric

### How the file layout maps to this mechanism

**Key design**: `scripts/` lives in the skill itself (called by absolute path); `commands/` and `agents/` are mirrored from the skill into each project's `.claude/` on bootstrap (Claude Code only discovers slash commands and subagents under `.claude/`, so they have to physically live there). State / memory / rules are seeded once per project and grow as you use it.

Learning is per-project — pitfalls in project A do not pollute project B. On the next `/run` against the same project, crystallized rules become hard checklists for plan and code review. The skill **gets smarter about your project the more you use it**.

### A concrete walkthrough

```
You type: /run add a user-registration endpoint

[bootstrap] init.sh runs (if .claude/ doesn't exist)

[plan]  AI writes:
        Phase 1: User Registration MVP
        ├── Slice 1.1: Database schema
        │   ├── T1: Implement User model
        │   ├── T2: Write alembic migration
        │   └── T3: Verify migration on test database
        ├── Slice 1.2: Registration endpoint
        │   ├── T1: Implement POST /register
        │   ├── T2: Add email format validation
        │   ├── T3: Add password hashing
        │   └── T4: Write integration tests
        └── Slice 1.3: Error handling + rate limiting

[planner-critic] pass

[execute T1.1.1] AI writes the model
[guard.sh "vim models/user.py"]  exit 0
[guard.sh "alembic upgrade head"] exit 0
[implementation-reviewer T1.1.1] pass
[execute T1.1.2] ...
[implementation-reviewer T1.1.2] FAIL — "migration didn't use batch_alter_table; SQLite will choke"
   AI fixes
   [implementation-reviewer T1.1.2] pass
   write episodic: fingerprint=spec:sqlite-batch-alter:migration, confidence=0.9
[execute T1.1.3] ...

[slice 1.1 done → requirement-auditor] pass

[execute slice 1.2 ...] ...
[implementation-reviewer T1.2.2] FAIL — "email validation doesn't handle unicode"
   AI fixes
   write episodic: fingerprint=boundary:unicode:input-validation, confidence=0.7

[slice 1.2 done → requirement-auditor]
   FAIL — "user_value says 'user can register' but I see no JWT-on-success path"
   inject new task: T1.2.5 Implement returning JWT after successful registration
[execute T1.2.5] ...
[requirement-auditor re-review] pass

[slice 1.3 done] [phase 1 done → integration-checker] pass

[plan done → crystallize.sh]
   aggregate episodics → no fingerprint reached 3 occurrences → no promotion
   (this /run produced no new rules, but episodics are stored;
    the next time the same fingerprint comes up will be #3, then promotion)

[exit] plan.meta.status = done
```

The second time you `/run` against the same project: `planner-critic` and `implementation-reviewer` read `dev-lessons.md`; crystallized rules become hard checklists. The first run may step on many rakes; ten runs in, the rule library stabilizes.

### Strict mode (`/run-strict`)

For high-stakes work where partial completion is unacceptable, use `/run-strict` instead of `/run`. Three differences:

- **Plan-time gate**: `planner-critic` enforces the Universal Completion Chain — every acceptance item must have a task chain reaching observable proof (test output, command stdout, file content, log line). Plans with shallow tasks are rejected before execution.
- **Task-time gate**: `implementation-reviewer` requires runtime evidence per task; bare commit sha is rejected. Pure refactors/renames use `static-only: <reason>` as an explicit escape hatch.
- **Plan-done gate**: a new 5th reviewer `topic-auditor` runs once after all phases finish, with permission to execute read-only smoke commands (`pytest`, `curl`, `cat`, etc.). It answers one question: "given only the topic and the resulting artifacts, would a fresh user say this is delivered?" If not, missing chains are injected as new slices in the special `P_recovery` phase, and the loop re-enters execution. The plan can only reach `status: done` after `topic-auditor` says yes.

Strict mode also uses a **progress-aware strike rule**: the 3-fail halt only fires when the reviewer's complaint is literally unchanged across three rounds — slow-but-progressing repair runs unbounded.

`/run-strict` is 2-5× slower than `/run`. Use it when you mean it.

---

## Commands

| Command | Purpose |
|---|---|
| `/run <topic>` | Main entrypoint — full autonomous plan + execute + review loop |
| `/run-strict <topic>` | Strict mode — 5-reviewer loop, refuses to mark done until topic-auditor verifies end-to-end delivery |
| `/plan <topic>` | Plan only, no execution; Planner-Critic review included |
| `/review [scope]` | Dispatch reviewers diagnostically, read-only |
| `/learn` | Manual crystallization of episodic memory → rules |
| `/resume` | Continue an unfinished plan from first non-done task |

---

## Skill Repo Layout

```
self-improving-workflow/
├── SKILL.md
├── README.md / README.zh-CN.md
├── commands/                         ← mirrored into each project's .claude/commands/
│   ├── run.md
│   ├── run-strict.md
│   ├── plan.md
│   ├── review.md
│   ├── learn.md
│   └── resume.md
├── agents/                           ← mirrored into each project's .claude/agents/
│   ├── planner-critic.md
│   ├── implementation-reviewer.md
│   ├── requirement-auditor.md
│   ├── integration-checker.md
│   └── topic-auditor.md
├── scripts/                          ← stays in skill, called by absolute path
│   ├── init.sh                       ← seeds .claude/ in the target project
│   ├── guard.sh                      ← irreversible-op regex check
│   ├── crystallize.sh                ← episodic→semantic→rules promotion
│   └── plan_lint.sh                  ← plan.json schema validation
├── seeds/                            ← per-project files copied by init.sh
│   ├── CLAUDE.md
│   ├── plan.schema.json
│   ├── rules/{autonomy-stops,dev-lessons}.md
│   └── memory/README.md
├── references/
│   ├── methodology.md
│   ├── plan-schema.md
│   ├── reviewer-contracts.md
│   ├── learning-loop.md
│   └── migration-from-tiered.md
└── tests/                            ← bats suite + fixtures
```

## File Layout — Project Side (`.claude/`)

After `init.sh` runs in your project:

```
.claude/
├── CLAUDE.md                          ← from seeds/, only if you don't already have one
├── commands/                          ← mirrored from skill (Claude Code discovers these)
│   ├── run.md
│   ├── run-strict.md
│   ├── plan.md
│   ├── review.md
│   ├── learn.md
│   └── resume.md
├── agents/                            ← mirrored from skill (Claude Code discovers these)
│   ├── planner-critic.md
│   ├── implementation-reviewer.md
│   ├── requirement-auditor.md
│   ├── integration-checker.md
│   └── topic-auditor.md
├── rules/
│   ├── autonomy-stops.md              ← from seeds/, you may append
│   └── dev-lessons.md                 ← from seeds/, auto-populated by /learn
├── state/
│   ├── plan.schema.json               ← from seeds/
│   ├── plan.json                      ← `{}` initially
│   ├── decisions.jsonl                ← empty initially
│   └── archive/                       ← old plans
└── memory/
    ├── README.md                      ← from seeds/
    ├── episodic/                      (gitignored)
    ├── semantic-patterns.json         (git-tracked)
    └── working/                       (gitignored)
```

`commands/` and `agents/` are write-once per file: re-running `init.sh` after upgrading the skill picks up newly-added files but never overwrites edits you made locally.

`.gitignore` is patched idempotently to exclude `episodic/` and `working/`.

---

## Reference

- [`references/methodology.md`](references/methodology.md) — why two pillars and the hybrid architecture approach
- [`references/plan-schema.md`](references/plan-schema.md) — phase/slice/task tree shape and schema constraints
- [`references/reviewer-contracts.md`](references/reviewer-contracts.md) — four reviewer triggers and IO shapes
- [`references/learning-loop.md`](references/learning-loop.md) — episodic→semantic→rules crystallization algorithm
- [`references/migration-from-tiered.md`](references/migration-from-tiered.md) — upgrading from the old tiered version
