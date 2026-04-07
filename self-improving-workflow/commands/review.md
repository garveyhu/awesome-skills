---
description: Run reviewer agents over plan or a scope, without modifying anything
---

# /review

Argument: $ARGUMENTS (optional: phase/slice/task id, or "all")

- No arg or `all` → dispatch all 4 reviewers across the entire plan; collate output
- Phase id → integration-checker
- Slice id → requirement-auditor
- Task id → implementation-reviewer

Print collated JSON results. **Do not modify plan or code.** This is a read-only diagnostic command.
