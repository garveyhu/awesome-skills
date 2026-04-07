#!/usr/bin/env bash
# crystallize.sh — episodic → semantic → rules promotion (deterministic)
# Usage: crystallize.sh <claude_dir>
# Thresholds (HARD-CODED, do not parameterize): occurrences >= 3 AND avg_confidence >= 0.7

if [[ $# -lt 1 ]]; then
  echo "Usage: crystallize.sh <.claude dir>" >&2
  exit 2
fi

CDIR="$1"
if [[ ! -d "$CDIR" ]]; then
  echo "ERROR: $CDIR is not a directory" >&2
  exit 2
fi

EP_DIR="$CDIR/memory/episodic"
SEM="$CDIR/memory/semantic-patterns.json"
RULES="$CDIR/rules/dev-lessons.md"

if [[ ! -d "$EP_DIR" ]]; then
  echo "ERROR: missing $EP_DIR" >&2
  exit 2
fi
[[ -f "$SEM" ]] || echo '{"patterns":[]}' > "$SEM"
[[ -f "$RULES" ]] || : > "$RULES"

THRESHOLD_OCC=3
THRESHOLD_CONF=0.7

WORK=$(mktemp)
cp "$SEM" "$WORK"

# === Aggregation phase ===
# For each episodic file, derive 2-segment key from fingerprint and upsert.
shopt -s nullglob
for ep_file in "$EP_DIR"/*.json; do
  fp=$(jq -r '.fingerprint // empty' "$ep_file")
  [[ -z "$fp" ]] && continue
  conf=$(jq -r '.confidence // 0.5' "$ep_file")
  ep_id=$(jq -r '.id' "$ep_file")
  ts=$(jq -r '.ts' "$ep_file")
  what=$(jq -r '.what // ""' "$ep_file")

  # Derive 2-segment key (everything before the 3rd colon)
  key=$(echo "$fp" | awk -F: '{print $1":"$2}')

  # Idempotency: skip if this episodic id is already counted
  exists=$(jq --arg key "$key" --arg eid "$ep_id" '
    [.patterns[] | select(.fingerprint == $key) | .episodic_ids[]] | index($eid) != null
  ' "$WORK")
  if [[ "$exists" == "true" ]]; then
    continue
  fi

  # Upsert
  WORK2=$(mktemp)
  jq --arg key "$key" --arg eid "$ep_id" --arg ts "$ts" --arg what "$what" --argjson conf "$conf" '
    if (.patterns | map(.fingerprint) | index($key)) == null then
      .patterns += [{
        fingerprint: $key,
        title: $what,
        occurrences: 1,
        first_seen: $ts,
        last_seen: $ts,
        avg_confidence: $conf,
        episodic_ids: [$eid],
        promoted_to_rule: false
      }]
    else
      .patterns |= map(
        if .fingerprint == $key then
          .occurrences = (.occurrences + 1)
          | .last_seen = $ts
          | .avg_confidence = ((.avg_confidence * (.occurrences - 1) + $conf) / .occurrences)
          | .episodic_ids = (.episodic_ids + [$eid])
        else
          .
        end
      )
    end
  ' "$WORK" > "$WORK2"
  mv "$WORK2" "$WORK"
done
shopt -u nullglob

# === Promotion phase ===
# For each pattern not yet promoted, check thresholds and promote.
to_promote=$(jq -c --argjson th_occ "$THRESHOLD_OCC" --argjson th_conf "$THRESHOLD_CONF" '
  .patterns[] | select(.promoted_to_rule == false and .occurrences >= $th_occ and .avg_confidence >= $th_conf)
' "$WORK")

while IFS= read -r p; do
  [[ -z "$p" ]] && continue
  fp=$(echo "$p" | jq -r '.fingerprint')
  title=$(echo "$p" | jq -r '.title')
  occ=$(echo "$p" | jq -r '.occurrences')
  conf=$(echo "$p" | jq -r '.avg_confidence')
  date=$(date +%Y-%m-%d)
  # Stable id derived from fingerprint + first promotion date
  lid="L-$(date +%Y%m%d)-$(echo "$fp" | tr ':' '-')"

  cat >> "$RULES" <<RULE

## $lid: $title

**Rule**: Avoid the recurring pattern observed across $occ instances.

**Why**: Pattern surfaced by reviewers $occ times with average confidence $conf.

**How to apply**: Whenever scope matches the pattern signature, apply the fix uniformly.

<!-- crystallized-pattern: $fp | date: $date | occurrences: $occ | confidence: $conf -->
RULE

  WORK2=$(mktemp)
  jq --arg fp "$fp" '.patterns |= map(if .fingerprint == $fp then .promoted_to_rule = true else . end)' "$WORK" > "$WORK2"
  mv "$WORK2" "$WORK"
done <<< "$to_promote"

mv "$WORK" "$SEM"
echo "crystallize: ok"
exit 0
