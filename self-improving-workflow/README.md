# self-improving-workflow

> Bootstrap any project with a project-level Claude Code workflow that **learns from itself**. Three tiers from solo scripts to government-grade systems. Works on both new and existing projects, never overwrites your files.

> 中文版：[README.zh-CN.md](README.zh-CN.md)

## Why This Exists

Every non-trivial project ends up reinventing the same `.claude/` configuration: `CLAUDE.md`, rules, slash commands, review agents, memory. And every team learns the same lessons the hard way: forgetting to write event skeletons before business logic, letting agents trample each other across modules, discovering missed requirements during review instead of planning.

This skill encodes those lessons as a **three-tier scaffold** plus a **continuous improvement loop**:

- **Init** — `/init-workflow` asks 4 questions, creates the right `.claude/` structure for your project size.
- **Phase protocols** — `/phase-start` and `/phase-review` give discipline without ceremony.
- **Self-improving** — `/self-improve` captures lessons from every session and (with your confirmation) promotes them into team-shared rules.
- **Non-destructive** — Run on existing projects safely. Never overwrites your files.

## Three Tiers

| Tier | Files | Use case |
|------|-------|----------|
| **minimal** | 6 | Solo scripts, throwaway experiments. Just a `/self-improve` button to capture lessons. |
| **standard** | 13 | 2-5 person mid-size projects. Phase protocols + 1 review agent + coding bans. |
| **full** | 19 | Team / large / compliance-critical. 3 parallel review agents + compliance presets. |

See [`references/tier-comparison.md`](references/tier-comparison.md) for the complete file matrix.

## Quick Start

### New Project

```
/init-workflow
```

Answers 4 questions → installs the recommended tier → done in 30 seconds.

### Existing Project (with CLAUDE.md or .claude/ already)

```
/init-workflow minimal
```

`minimal` is the safest entry. Existing files are skipped, never overwritten. Your `CLAUDE.md` stays untouched but gets a `.skill-template` companion for reference. Read [`references/existing-project-guide.md`](references/existing-project-guide.md) for details.

### Capturing a Lesson

```
/self-improve

> Q1: What did you learn this session?
> A: Cross-module Autowire caused circular dependency 3 times this week.

> Q2: Category? (workflow / coding / module / compliance / other)
> A: module

> Q3: Should this become a permanent rule in dev-lessons.md? (y/n)
> A: y

✓ Appended to .claude/rules/dev-lessons.md
```

### Upgrading

```
/upgrade-workflow standard   # minimal → standard
/upgrade-workflow full       # standard → full or minimal → full
```

Existing files with content differences trigger an interactive `[k]eep / [n]ew / [d]iff / [s]kip` prompt. You stay in control.

## Slash Commands

| Command | Tier | What it does |
|---------|------|--------------|
| `/init-workflow [tier]` | all | Interactive Q&A to scaffold `.claude/`. Auto-detects existing files. |
| `/upgrade-workflow <target>` | all | Upgrade to higher tier. Diffs conflicts. |
| `/self-improve [scope]` | all | Capture session lessons into `dev-lessons.md`. |
| `/phase-start <name>` | standard+ | Phase startup protocol. |
| `/phase-review <name>` | standard+ | Phase completion protocol with review agents + auto-`/self-improve`. |
| `/compile-check` | full | Full-module compile in dependency order. |

## Key Design Principles

1. **Write-once**. Never overwrites. Existing files are skipped, with optional `.skill-template` companion.
2. **User confirmation before any rule write**. `/self-improve` proposes; user approves; only then does it touch `.claude/rules/`.
3. **Three-tier modularity**. Solo scripts shouldn't pay for team rituals; team projects shouldn't reinvent them.
4. **Non-invasive on existing projects**. Detects `.gitignore` collisions, warns instead of patching destructively.
5. **Optional dependency on `charon-fan/agent-playbook@self-improving-agent`**. Uses it if present (richer memory engine), falls back to a 3-prompt manual mode otherwise.
6. **Bash-only scripts**. Zero runtime dependencies. macOS + Linux native.

## Architecture

```
self-improving-workflow/
├── SKILL.md                    # Entry: trigger words + anchor hooks
├── README.md / README.zh-CN.md # Bilingual user docs
├── templates/
│   ├── minimal/                # 4 file templates
│   ├── standard/               # +7 files (incremental)
│   └── full/                   # +5 files (incremental)
├── scripts/
│   ├── init.sh                 # /init-workflow implementation
│   ├── upgrade.sh              # /upgrade-workflow implementation
│   └── detect.sh               # Project signal detection
└── references/
    ├── tier-comparison.md      # Feature matrix
    ├── existing-project-guide.md
    └── compliance-presets.md   # govt / fintech / healthcare / privacy
```

## File Ownership Model

Same as `cookiecutter` / `yeoman` / `create-react-app eject`: **write-once, user owns forever**.

- Init never overwrites existing files
- Upgrade prompts on conflicts, never silently overwrites
- User edits to skill-generated files are sacred
- The skill versioning lives in `garveyhu/awesome-skills` repo, not individual project files

## Compliance Presets

The `full` tier offers four presets for `domain-compliance.md`:

- **govt** — Public sector audit/isolation/encryption requirements
- **fintech** — Idempotency keys, decimal arithmetic, immutable logs
- **healthcare** — PHI protection, access logging, break-glass access
- **privacy** — GDPR/CCPA/PIPL: data minimization, right to access/delete, consent

Selected via Q3 in `/init-workflow`. Details in [`references/compliance-presets.md`](references/compliance-presets.md).

## Origin Story

Distilled from a Java/Spring government childcare management system (153 features, 5 modules, 85 tables) after 3 cycles of phase rework. The hard lessons:

1. Build event/interface skeletons **before** business logic, not after
2. Multi-agent parallelism **only works with strict module isolation**
3. ServiceImpl checklists must be **listed upfront**, never discovered during review
4. Compile validation must happen **after every agent**, not at end
5. Phase reviews must be **mandatory and parallel** (3+ angles), not optional and serial
6. Lessons learned must be **captured immediately**, not "we'll remember next time"

This skill encodes all six as enforceable workflow.

## Contributing

This skill lives in [`garveyhu/awesome-skills`](https://github.com/garveyhu/awesome-skills). Issues and PRs welcome.

The skill is **dogfooded**: it's installed on its own repo. If you find issues using it on a real project, capture them via `/self-improve` and contribute the lessons back as PRs to `templates/` or `references/`.

## License

MIT (inherits from `awesome-skills` repo).
