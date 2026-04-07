# Tier Comparison

Three tiers, ordered from minimal to full. Each upper tier **includes** everything from the lower tiers (cumulative).

## Cumulative File Matrix

| File | minimal | standard | full |
|------|---------|----------|------|
| `.claude/CLAUDE.md` | ✓ | ✓ | ✓ |
| `.claude/.workflow-tier` (marker) | ✓ | ✓ | ✓ |
| `.claude/rules/dev-lessons.md` | ✓ | ✓ | ✓ |
| `.claude/commands/self-improve.md` | ✓ | ✓ | ✓ |
| `.claude/memory/README.md` | ✓ | ✓ | ✓ |
| `.claude/memory/episodic/.gitkeep` | ✓ | ✓ | ✓ |
| `.claude/settings.json` | — | ✓ | ✓ |
| `.claude/rules/coding-bans.md` | — | ✓ | ✓ |
| `.claude/rules/module-isolation.md` | — | ✓ | ✓ |
| `.claude/commands/phase-start.md` | — | ✓ | ✓ |
| `.claude/commands/phase-review.md` | — | ✓ | ✓ |
| `.claude/agents/code-quality-reviewer.md` | — | ✓ | ✓ |
| `.claude/memory/semantic-patterns.json` | — | ✓ | ✓ |
| `.claude/rules/domain-compliance.md` | — | — | ✓ |
| `.claude/commands/compile-check.md` | — | — | ✓ |
| `.claude/commands/upgrade-workflow.md` | — | — | ✓ |
| `.claude/agents/requirement-auditor.md` | — | — | ✓ |
| `.claude/agents/cross-module-checker.md` | — | — | ✓ |
| `.claude/memory/working/.gitkeep` | — | — | ✓ |

| | minimal | standard | full |
|---|---|---|---|
| **File count** | 6 | 13 | 19 |
| **Phase protocol** | — | ✓ | ✓ |
| **Review agents** | — | 1 | 3 (parallel) |
| **Compliance preset** | — | — | ✓ |

## Capability Matrix

| Capability | minimal | standard | full |
|---|---|---|---|
| Capture lessons via `/self-improve` | ✓ | ✓ | ✓ |
| Project background in CLAUDE.md | ✓ | ✓ | ✓ |
| Phase startup protocol | — | ✓ | ✓ |
| Phase completion protocol | — | ✓ | ✓ |
| Single-agent code quality review | — | ✓ | ✓ |
| Three-agent parallel review (req / quality / cross-module) | — | — | ✓ |
| Module isolation rules | — | ✓ | ✓ |
| Coding bans rules | — | ✓ | ✓ |
| Domain compliance preset | — | — | ✓ |
| Bash permission allow/deny | — | ✓ | ✓ |
| Semantic pattern memory | — | ✓ | ✓ |
| Episodic memory (gitignored) | ✓ | ✓ | ✓ |
| Working memory (gitignored) | — | — | ✓ |
| `/upgrade-workflow` command | — | — | ✓ |
| `/compile-check` command | — | — | ✓ |

## Use Case Decision Tree

```
Q: Solo developer, throwaway script (1-2 days)?
   → minimal

Q: Solo or pair, project lasting weeks-months, no compliance?
   → minimal (or standard if you want phase discipline)

Q: 2-5 person team, mid-size business app?
   → standard

Q: Team project with compliance (govt / fintech / healthcare)?
   → full

Q: Already-established team with their own conventions?
   → start with minimal, upgrade if needed (init is non-destructive)
```

## Upgrade Path

```
minimal → standard:
  Adds 7 files (settings, 2 rules, 2 commands, 1 agent, 1 memory file)
  No existing files modified.

standard → full:
  Adds 6 files (1 rule, 2 commands, 2 agents, 1 memory dir)
  No existing files modified.

minimal → full:
  Adds 13 files in one shot.
```

Run via `/upgrade-workflow <target>` which uses `scripts/upgrade.sh`. Existing files are never silently overwritten — diffs prompt the user with `[k]eep / [n]ew / [d]iff / [s]kip` for any conflicts.
