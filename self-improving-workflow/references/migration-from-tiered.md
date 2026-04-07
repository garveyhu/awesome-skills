# Migrating from the tiered version

If your project's `.claude/` was created by the old tiered (minimal/standard/full) version, it will keep working — slash commands are decoupled from the skill binary. To adopt the two-pillar model:

## Option A — In place

1. Inside the project, delete only the old tier-marker: `rm .claude/.workflow-tier`
2. Re-run from the skill: `bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"`
3. The init is idempotent: existing files are skipped, missing files (`commands/run.md`, `agents/*`, `state/`, `memory/semantic-patterns.json`, etc.) are created.
4. Manually delete commands you no longer want: `phase-start.md`, `phase-review.md`, `compile-check.md`, `upgrade-workflow.md`, `self-improve.md`.
5. The old `coding-bans.md`, `module-isolation.md`, `domain-compliance.md` files are not touched. Decide whether to keep them as project-specific seeded rules or delete them and let crystallization rebuild.

## Option B — Clean slate

1. `mv .claude .claude.tiered-backup`
2. `bash ~/.agents/skills/self-improving-workflow/scripts/init.sh "$(pwd)"`
3. Diff the two if you want to lift over project-specific lessons.

## What the old version had that the new one doesn't

- 3 tiers — replaced by single methodology
- `coding-bans.md`, `module-isolation.md`, `domain-compliance.md` — not seeded; expected to grow via crystallization
- Tech-stack templates (Python/Java/React/etc) — removed
- `/phase-start`, `/phase-review`, `/self-improve`, `/compile-check`, `/upgrade-workflow` — replaced by `/run`, `/plan`, `/review`, `/learn`, `/resume`
- `scripts/detect.sh`, `scripts/upgrade.sh` — removed
