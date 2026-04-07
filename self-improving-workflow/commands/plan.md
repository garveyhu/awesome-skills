---
description: Write/rewrite plan.json for the given topic; runs Planner-Critic; does not execute
---

# /plan

Argument: $ARGUMENTS (topic)

1. Read `.claude/state/plan.schema.json`.
2. Write `.claude/state/plan.json` matching the schema for the topic, respecting hard limits (≤4 phases, ≤5 slices/phase, ≤7 tasks/slice).
3. Dispatch `planner-critic`. Iterate (max 3 attempts). On 3rd fail, leave plan.json with `meta.status = "blocked"` and exit.
4. On pass, persist and exit. Do **not** start execution.
