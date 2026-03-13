# Contributing to Awesome Skills

**For AI assistants working in this directory.**

This file captures the conventions and constraints for creating or editing skills in this repo. Read it before making any changes.

---

## Repo Setup

**Two remotes — always push both:**

```bash
git remote -v
# origin   git@github.com:garveyhu/awesome-skills.git
# iktapp   git@repo.iktapp.com:ai/awesome-skills.git

git push origin main
git push iktapp main
```

**`.gitignore` uses a whitelist pattern** — everything is ignored by default, and skills are explicitly allowed:

```gitignore
# Ignore everything by default
*

# Allow these skills (whitelist)
!.gitignore
!README.md
!README.zh-CN.md
!my-new-skill/
!my-new-skill/**
```

When adding a new skill, add two lines to `.gitignore`:

```gitignore
!new-skill-name/
!new-skill-name/**
```

**`docs/` is local-only** — never add it to `.gitignore` whitelist. Planning documents stay on the local machine.

---

## Skill File Structure

Every skill lives in its own directory:

```
skill-name/
├── SKILL.md              # Main skill file (required)
└── references/           # Supporting templates/docs (optional)
    ├── simple-project.md
    ├── complex-project.md
    └── patterns.md
```

### SKILL.md Format

```markdown
---
name: skill-name
description: >
  English description of when this skill triggers.
  Include trigger phrases in both English and Chinese.
  Be specific about what the skill does.
---

# Skill Title

(Skill body in Chinese)
```

**Frontmatter rules:**
- `name`: kebab-case, matches directory name
- `description`: English only, written for Claude's trigger-matching — include concrete trigger phrases
- `description` is the only part external users/AI see for matching; make it precise

**Body language:** Chinese. The target user is Chinese-speaking; the skill body is instruction text, not public API.

---

## Skill Content Conventions

### Three-Phase Structure (Dev Workflow Skills)

Skills that guide development work follow this pattern:

- **阶段一：初始化（Init）** — Scaffold a new project from zero
- **阶段二：开发指南（Guide）** — Conventions for ongoing feature work
- **阶段三：代码审查（Review）** — Checklist for reviewing completed work

Each phase is self-contained. Users invoke whichever phase fits their current task.

### Multi-Phase Process Skills

Skills that orchestrate a workflow (e.g., `website-creator`, `docker-best-practices`) use sequential phases:

- **Phase 1**: Gather fixed information (always ask these)
- **Phase 2**: Dynamic clarification (up to N rounds, with a confidence gate)
- **Phase 3**: Output plan and wait for confirmation
- **Phase 4**: Execute

**Never generate files before the user confirms the plan.**

### No Hardcoded Paths

Never write personal paths like `/Users/links/...` or `~/username/...` in skill content. Use generic placeholders:

```
# Wrong
cd /Users/links/projects/{name}

# Correct
cd {target_dir}/{name}
```

Refer to AI skill directories generically: "当前 AI 助手的 skill 目录中" — not a hardcoded path.

### No Implementation Jargon in User-Facing Descriptions

README and frontmatter descriptions should describe outcomes, not internal mechanisms:

```
# Wrong
"Includes JWT authentication skeleton"

# Correct
"Includes user authentication skeleton"
```

---

## Git Commit Conventions

Use scoped conventional commits:

| Prefix | When |
|--------|------|
| `feat(skill):` | New skill or major new section |
| `fix(skill):` | Bug fix in skill content |
| `docs:` | README or CONTRIBUTING changes |
| `chore:` | .gitignore, repo config |

Example: `feat(skill): add docker-best-practices with full containerization workflow`

---

## Design Process

Before writing a new skill:

1. **Brainstorm first** — use the `brainstorming` skill to confirm requirements are understood
2. **Write a design doc** in `docs/plans/YYYY-MM-DD-skill-name-design.md` (local-only, not committed)
3. **Implement** — write SKILL.md and references/
4. **Review** — read back the full skill against the design doc

Design docs are for clarifying thinking. They are never committed.

---

## README Conventions

**`README.md`** — English default, written for GitHub visitors who may star/fork.

**`README.zh-CN.md`** — Chinese translation, mirrors the English README structure exactly.

Both files:
- Cross-link to each other at the top
- No license section
- No implementation jargon in skill descriptions
- Skills described by what they *produce*, not how they work internally

When adding a new skill, add a section to both READMEs following the existing format.

---

## Checklist: Adding a New Skill

- [ ] Create `skill-name/SKILL.md` with correct frontmatter
- [ ] Add `references/` directory if templates are needed
- [ ] Add `!skill-name/` and `!skill-name/**` to `.gitignore`
- [ ] Add skill section to `README.md`
- [ ] Add skill section to `README.zh-CN.md`
- [ ] Commit with `feat(skill): ...`
- [ ] Push to both `origin` and `iktapp`
