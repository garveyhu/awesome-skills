---
description: Write/rewrite plan.json for the given topic; runs Planner-Critic; does not execute
---

# /plan

Argument: $ARGUMENTS (topic)

1. Read `.claude/state/plan.schema.json`.
2. Write `.claude/state/plan.json` matching the schema for the topic. No hard upper bounds on counts — pick the granularity the topic genuinely needs. **Language-match rule (hard)**: every human-readable field in the plan body must use the same natural language as `$ARGUMENTS` (Chinese topic → Chinese body, English topic → English body). Schema field names, enums, ids, file paths, tool names stay as-is. See `references/plan-schema.md`.
3. Dispatch `planner-critic`. Iterate (max 3 attempts). On 3rd fail, leave plan.json with `meta.status = "blocked"` and exit.
4. On pass, persist and exit. Do **not** start execution.
