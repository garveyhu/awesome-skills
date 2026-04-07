---
name: self-improving-workflow
description: >
  Project-level self-learning workflow scaffold for Claude Code. Bootstraps
  .claude/ structure with three tiers (minimal/standard/full), installs phase
  protocols (start/review), and runs a continuous-improvement loop that
  captures lessons → distills patterns → evolves rules. Works for both new
  and existing projects (write-once, no destructive overwrites).
  TRIGGER WORDS: 总结教训, 踩坑了, 这次学到, Phase 完成, 阶段评审, 阶段总结,
  init workflow, self improve, self-improve, retrospective, lesson learned,
  scaffold .claude, project workflow, sop init, 工作流初始化, 升级工作流.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Self-Improving Workflow

> Bootstrap any project with a project-level Claude Code workflow that **learns from itself**. Three tiers (minimal / standard / full) for solo scripts up to government-grade systems. Source: distilled from a Java/Spring 政府项目（ProCare）经过 3 轮返工后形成的实践。

## Overview

This skill installs a `.claude/` directory in any project that gives the assistant:

1. **Modular rules** — `.claude/rules/*.md` for hard constraints, coding bans, compliance requirements
2. **Slash commands** — `/init-workflow`, `/upgrade-workflow`, `/self-improve`, plus phase protocols
3. **Review sub-agents** — `code-quality-reviewer`, `requirement-auditor`, `cross-module-checker`
4. **Three-layer memory** — semantic patterns (git-shared) + episodic experiences (private) + working state
5. **Continuous improvement loop** — lessons captured during development → distilled into patterns → promoted to rules → loaded automatically next session

The skill is **opinionated but tier-aware**: solo scripts get a 4-file minimal install (just a "lessons sink"), team projects get the full 20+ file scaffold with parallel review agents.

## Three Tiers

| Tier | Files | Use case |
|------|-------|----------|
| **minimal** | 4 | Solo scripts, experiments, single-file utilities. Just a `/self-improve` button to capture lessons. |
| **standard** | 10 | 2-5 person mid-size projects. Adds phase protocols, coding bans, 1 review agent. |
| **full** | 20+ | Team / large / compliance-critical projects. 3 parallel review agents, compliance presets, full phase review protocol. |

See [`references/tier-comparison.md`](references/tier-comparison.md) for the full file-by-file breakdown.

## When to Use

### Automatic Triggers (description keyword sniffing)

The `description` frontmatter contains trigger words. Claude loads this skill automatically when the user says any of:

- 总结教训 / 踩坑了 / 这次学到 / Phase 完成 / 阶段评审 / 阶段总结
- init workflow / self improve / retrospective / lesson learned
- scaffold .claude / project workflow / 工作流初始化 / 升级工作流

### Anchor Hooks (Claude judges and suggests)

After loading, Claude watches for these signals and **suggests (never executes)** the relevant command:

| Signal | Suggested action |
|--------|------------------|
| User fixed ≥3 compile errors in one session | "要不要 `/self-improve` 抓一下根因？" |
| ≥5 git commits in one session | "要不要走 `/phase-review` 评审一下？" |
| User says "完成了" / "搞定了" / "done" | "要不要 `/self-improve` 沉淀本次经验？" |
| User reports the same issue twice | "这个似乎重复了，建议加进 `coding-bans.md`，要 `/self-improve` 吗？" |
| Cross-module conflict resolved | "要不要把这条规则追加到 `module-isolation.md`？" |

**Critical constraint**: All suggestions are **questions**, not actions. Wait for explicit y/n before executing.

## Slash Commands Reference

| Command | Tier | What it does |
|---------|------|--------------|
| `/init-workflow [tier]` | all | Interactive Q&A to scaffold `.claude/`. Auto-detects existing files. |
| `/upgrade-workflow <target>` | all | Upgrade to higher tier. Diffs existing files, prompts user on conflicts. |
| `/self-improve [scope]` | all | Capture session lessons into `.claude/rules/dev-lessons.md`. Uses `charon-fan/agent-playbook@self-improving-agent` if installed; otherwise falls back to manual mode. |
| `/phase-start <name>` | standard+ | Phase startup protocol: write plan → build event/interface skeletons → list ServiceImpl checklist → confirm. |
| `/phase-review <name>` | standard+ | Phase completion protocol: full compile → frontend verification → parallel review agents → fix P0 → `/self-improve`. |
| `/compile-check` | full | Run module-by-module compile check in dependency order. |

## How `/init-workflow` Works

### Step 1 — Detect existing state

```bash
bash scripts/detect.sh
```

Outputs:
- Whether `.claude/` already exists
- File count and contents summary
- Recommended tier based on heuristics (project size, file count)

### Step 2 — Interactive Q&A (4 questions)

| Q | Field | Affects |
|---|-------|---------|
| 1 | Project type (script / small / mid / large) | Tier recommendation |
| 2 | Tech stack (Java/Python/Node/Vue/React/monorepo) | rules templates |
| 3 | Compliance (none / govt / fintech / healthcare / privacy) | `domain-compliance.md` preset |
| 4 | Confirmation | Show file plan, ask y/n |

### Step 3 — Execute

```bash
bash scripts/init.sh <tier> <stack> <compliance>
```

For each template file in the chosen tier:
1. Resolve target path (`.template` suffix stripped)
2. If target exists → **skip and log** (write-once principle)
3. Special case: `CLAUDE.md` exists → write `CLAUDE.md.skill-template` alongside it for user reference
4. Apply template variables (project name, tech stack, compliance preset)
5. Patch `.gitignore` idempotently (add `.claude/memory/episodic/`, `.claude/memory/working/`)

### Step 4 — Report

Show file-by-file action log:
```
✓ .claude/CLAUDE.md exists (87 lines), skipped
  → wrote .claude/CLAUDE.md.skill-template for reference
✗ .claude/rules/dev-lessons.md → created
✗ .claude/commands/self-improve.md → created
...
Done. Created 6 files, skipped 2 existing files.
```

## How `/upgrade-workflow` Works

1. Read `.claude/.workflow-tier` to know current tier
2. Compute target tier diff (which files are new in target tier)
3. For each new file: same write-once logic as init
4. For each file that **exists in both tiers but content differs** between tiers:
   - Compute diff between bundled template and current file on disk
   - Present user with options: `[k]eep existing` / `[n]ew template` / `[d]iff` / `[s]kip`
5. Update `.claude/.workflow-tier` to new tier

## How `/self-improve` Works

```bash
bash scripts/self_improve.sh <scope>
```

The script checks for `~/.agents/skills/self-improving-agent/` (charon-fan/agent-playbook):

**If installed**:
- Delegate to the full three-tier memory pipeline (episodic → semantic → rules)
- Episodic JSON written to `.claude/memory/episodic/YYYY-MM-DD-<scope>.json`
- High-confidence patterns appended to `.claude/memory/semantic-patterns.json`
- Critical patterns (≥3 repetitions or rating ≥7) **proposed for** `.claude/rules/dev-lessons.md`
- **User must confirm** before any write to `.claude/rules/`

**If not installed (fallback)**:
- Print: "Tip: install `charon-fan/agent-playbook@self-improving-agent` for richer memory features"
- Walk the user through 3 prompts:
  1. "What did you learn this session? (one-line per lesson)"
  2. "What category? (workflow / coding / module / compliance / other)"
  3. "Should this become a permanent rule in dev-lessons.md? (y/n)"
- If yes, append to `.claude/rules/dev-lessons.md` with date marker

## File Ownership Rules

**Write-once principle** (Tier 3 + part of Tier 2 from cookiecutter conventions):

1. **Init never overwrites**. Existing files are skipped and logged.
2. **CLAUDE.md exception**: skipped *and* a `.skill-template` companion is written for the user to compare.
3. **Upgrade never silently overwrites**. Same-name files with content differences trigger an interactive `[k/n/d/s]` prompt.
4. **User edits are sacred**. Once a file is on disk, only the user can modify it (or via explicit `[n]ew template` choice during upgrade).

This is the same model as `cookiecutter`, `yeoman`, `create-react-app eject`.

## Tier Recommendation Heuristic

`detect.sh` uses these signals to suggest a tier:

| Signal | Score weight |
|--------|--------------|
| Number of top-level dirs (excluding hidden) | +1 per dir, capped at 5 |
| Presence of `pom.xml` / `build.gradle` / `pyproject.toml` workspace | +2 |
| `git log --oneline | wc -l` | +1 per 10 commits, capped at 5 |
| Number of contributors (`git shortlog -sn`) | +2 per contributor, capped at 6 |
| Presence of `.github/workflows/` or `.gitlab-ci.yml` | +2 |
| User self-declared "compliance: yes" in Q3 | +5 |

| Score | Recommended tier |
|-------|------------------|
| 0-3 | minimal |
| 4-9 | standard |
| 10+ | full |

User can always override the suggestion.

## Self-Hosting (Meta Loop)

This skill is designed for **dogfooding**: install it on real projects, capture lessons via `/self-improve`, then **promote those lessons back into the skill itself** by editing `templates/` and `references/`. Each release should incorporate at least one lesson from real-world usage.

The skill versions itself via git tags in `garveyhu/awesome-skills` repo.

## Reference

- [`references/tier-comparison.md`](references/tier-comparison.md) — Full file-by-file comparison of three tiers
- [`references/existing-project-guide.md`](references/existing-project-guide.md) — Detailed workflow for adopting on an existing project
- [`references/compliance-presets.md`](references/compliance-presets.md) — Government / fintech / healthcare / privacy preset rules
- Design doc: `~/.agents/skills/docs/2026-04-07-self-improving-workflow-design.md`
- Origin story: ProCare Yangzhou Smart Childcare System (Java/Spring/JeecgBoot govt project, 153 features, 5 modules, 85 tables)

## Best Practices

### DO
- ✅ Run `/init-workflow` on any new project before writing the first feature
- ✅ Run `/self-improve` at every Phase boundary (or every Friday for ongoing projects)
- ✅ Confirm before any write to `.claude/rules/` — these are team-shared
- ✅ Upgrade tier explicitly (`/upgrade-workflow standard`) when project grows
- ✅ Read `.claude/CLAUDE.md.skill-template` after init on existing projects

### DON'T
- ❌ Don't run init twice expecting overwrites — use `/upgrade-workflow` or manual edits
- ❌ Don't add `.claude/` to `.gitignore` as a whole — use the granular pattern from this skill
- ❌ Don't let `/self-improve` auto-write rules without user confirmation
- ❌ Don't put project-specific things in your global `~/.claude/` config
- ❌ Don't use this for one-off scripts that you'll throw away in an hour
