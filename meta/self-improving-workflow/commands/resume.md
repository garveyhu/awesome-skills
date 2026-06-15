---
description: Continue an unfinished plan from where it stopped
---

# /resume

Argument: $ARGUMENTS (optional: `--force-resume`)

1. Read `.claude/state/plan.json`.
2. If `meta.status == "done"`, print a summary and exit.
3. If `meta.status == "blocked"` and `--force-resume` not given, refuse with the last `decisions.jsonl` entry as context.
4. Otherwise, set `meta.status = "in_progress"` and re-enter the `/run` execute loop from the first non-`done` task.
5. Re-load the tail of `decisions.jsonl` (last 50 entries) into reasoning context to avoid relitigating settled choices.
