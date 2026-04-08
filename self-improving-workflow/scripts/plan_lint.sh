#!/usr/bin/env bash
# plan_lint.sh — validate plan.json against plan.schema.json (pure jq)
# Usage: plan_lint.sh <plan.json>
# Exit: 0 ok, 1 schema violation, 2 usage error, 3 not JSON
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: plan_lint.sh <plan.json>" >&2
  exit 2
fi

PLAN="$1"
if ! jq empty "$PLAN" 2>/dev/null; then
  echo "ERROR: $PLAN is not valid JSON" >&2
  exit 3
fi

# Verb regex (English + Chinese subset). Anchored at start.
VERB_RE='^(Implement|Modify|Add|Remove|Verify|Refactor|Write|Update|Delete|Validate|Generate|Configure|Install|Run|Migrate|Document|实现|修改|添加|删除|验证|重构|编写|更新|配置|安装|运行|迁移)([[:space:]]|$)'

# Use jq to emit FAIL: <msg> lines for every violation, then we count.
errors=$(jq -r --arg verb "$VERB_RE" '
  [
    # meta
    (if (.meta.topic // "") == "" then "FAIL: meta.topic missing/empty" else empty end),
    (if .meta.status as $s | (["pending","in_progress","done","blocked"] | index($s)) == null
       then "FAIL: meta.status invalid" else empty end),
    ((.meta.mode // "normal") as $m | if (["normal","strict"] | index($m)) == null
       then "FAIL: meta.mode invalid (\($m))" else empty end),

    # at most one recovery phase
    ((.phases | map(select((.kind // "main") == "recovery")) | length) as $rec_count |
      if $rec_count > 1
        then "FAIL: more than one recovery phase (\($rec_count))" else empty end),

    # walk phases
    (.phases[] |
      (if (.id | test("^(P[0-9]+|P_recovery)$")) | not then "FAIL: phase id \(.id) bad pattern" else empty end),
      (if (.slices | length) < 1
         then "FAIL: phase \(.id) slices count 0 (must be >= 1)" else empty end),
      (.slices[] |
        (if (.id | test("^(P[0-9]+|P_recovery)-S[0-9]+$")) | not then "FAIL: slice id \(.id) bad pattern" else empty end),
        (if (.user_value // "") == "" then "FAIL: slice \(.id) user_value empty" else empty end),
        (if (.acceptance | length) < 1 then "FAIL: slice \(.id) acceptance empty" else empty end),
        (if (.tasks | length) < 1
           then "FAIL: slice \(.id) tasks count 0 (must be >= 1)" else empty end),
        (.tasks[] |
          (if (.id | test("^(P[0-9]+|P_recovery)-S[0-9]+-T[0-9]+$")) | not then "FAIL: task id \(.id) bad pattern" else empty end),
          (if (.action | test($verb)) | not then "FAIL: task \(.id) action does not start with whitelisted verb: \(.action)" else empty end)
        )
      )
    )
  ] | .[]
' "$PLAN")

if [[ -n "$errors" ]]; then
  echo "$errors" >&2
  count=$(echo "$errors" | wc -l | tr -d ' ')
  echo "$count error(s)" >&2
  exit 1
fi

echo "OK"
exit 0
