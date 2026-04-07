# Migrating from the tiered version

If your project's `.claude/` was created by the old tiered (minimal/standard/full) version, the layout has changed: there is now a single methodology (no tiers), the old phase commands have been replaced by `/run`, and the four reviewers have new names. `commands/` and `agents/` still live under `.claude/` (Claude Code requires that for discovery), but they are now mirrored fresh from the skill on init rather than hand-edited.

## Option A — In place

1. Inside the project, delete the old tier-marker and obsolete commands/agents:
   ```bash
   rm -f .claude/.workflow-tier
   rm -rf .claude/commands .claude/agents
   ```
2. Re-run init from the skill:
   ```bash
   bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"
   ```
3. The init is idempotent: it mirrors the new `commands/` and `agents/` from the skill, and creates any missing per-project files (`state/`, `memory/semantic-patterns.json`, `rules/{autonomy-stops,dev-lessons}.md`) from `seeds/`. Existing files (including your `CLAUDE.md` and any rules you've written) are never overwritten.
4. The old `coding-bans.md`, `module-isolation.md`, `domain-compliance.md` files are not touched. Decide whether to keep them as project-specific rules or delete them and let crystallization rebuild.

## Option B — Clean slate

1. `mv .claude .claude.tiered-backup`
2. `bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"`
3. Diff the two if you want to lift over project-specific lessons.

## What the old version had that the new one doesn't

- 3 tiers — replaced by single methodology
- Hand-edited `commands/` and `agents/` per project — now mirrored from the skill on init (still under `.claude/` so Claude Code can find them, but write-once)
- `coding-bans.md`, `module-isolation.md`, `domain-compliance.md` — not seeded; expected to grow via crystallization
- Tech-stack templates (Python/Java/React/etc) — removed
- `/phase-start`, `/phase-review`, `/self-improve`, `/compile-check`, `/upgrade-workflow` — replaced by `/run`, `/plan`, `/review`, `/learn`, `/resume`
- `scripts/detect.sh`, `scripts/upgrade.sh` — removed
