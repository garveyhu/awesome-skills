# Migrating from the tiered version

If your project's `.claude/` was created by the old tiered (minimal/standard/full) version, the slash commands and reviewer agents you used to have copied into the project are now skill-global — they live at `~/.agents/skills/self-improving-workflow/{commands,agents}/`. The project no longer needs its own copies.

## Option A — In place

1. Inside the project, delete the old tier-marker and the now-redundant copies:
   ```bash
   rm -f .claude/.workflow-tier
   rm -rf .claude/commands .claude/agents     # now skill-global, not per-project
   rm -f .claude/commands/phase-start.md .claude/commands/phase-review.md \
         .claude/commands/compile-check.md .claude/commands/upgrade-workflow.md \
         .claude/commands/self-improve.md     # obsolete commands
   ```
2. Re-run init from the skill:
   ```bash
   bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"
   ```
3. The init is idempotent: existing files are skipped, missing per-project files (`state/`, `memory/semantic-patterns.json`, `rules/{autonomy-stops,dev-lessons}.md`) are created from `seeds/`.
4. The old `coding-bans.md`, `module-isolation.md`, `domain-compliance.md` files are not touched. Decide whether to keep them as project-specific seeded rules or delete them and let crystallization rebuild.

## Option B — Clean slate

1. `mv .claude .claude.tiered-backup`
2. `bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"`
3. Diff the two if you want to lift over project-specific lessons.

## What the old version had that the new one doesn't

- 3 tiers — replaced by single methodology
- `.claude/commands/` and `.claude/agents/` per-project copies — now skill-global
- `coding-bans.md`, `module-isolation.md`, `domain-compliance.md` — not seeded; expected to grow via crystallization
- Tech-stack templates (Python/Java/React/etc) — removed
- `/phase-start`, `/phase-review`, `/self-improve`, `/compile-check`, `/upgrade-workflow` — replaced by `/run`, `/plan`, `/review`, `/learn`, `/resume`
- `scripts/detect.sh`, `scripts/upgrade.sh` — removed
