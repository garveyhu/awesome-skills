#!/usr/bin/env bash
# guard.sh — block irreversible operations
# Usage: guard.sh "<command line>"
# Exit: 0 allowed, 1 blocked, 2 usage
#
# Note: no set -e here; we rely on explicit exit codes only.

if [[ $# -lt 1 ]]; then
  echo "Usage: guard.sh \"<command>\"" >&2
  exit 2
fi

CMD="$1"

block() {
  echo "IRREVERSIBLE_BLOCKED [$1]: $CMD" >&2
  exit 1
}

# --- data-loss ---
# rm with recursive flag targeting absolute paths or home (~)
if [[ "$CMD" =~ rm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*[[:space:]]+'/' ]]; then block "data-loss"; fi
if [[ "$CMD" =~ rm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*[[:space:]]+'~' ]]; then block "data-loss"; fi
# git reset --hard
if [[ "$CMD" =~ git[[:space:]]+reset[[:space:]]+--hard ]]; then block "data-loss"; fi
# git clean -f (any flag combo containing f)
if [[ "$CMD" =~ git[[:space:]]+clean[[:space:]]+-[a-z]*f ]]; then block "data-loss"; fi
# DROP TABLE/DATABASE/SCHEMA (case-insensitive via both cases)
if [[ "$CMD" =~ [Dd][Rr][Oo][Pp][[:space:]]+[Tt][Aa][Bb][Ll][Ee] ]]; then block "data-loss"; fi
if [[ "$CMD" =~ [Dd][Rr][Oo][Pp][[:space:]]+[Dd][Aa][Tt][Aa][Bb][Aa][Ss][Ee] ]]; then block "data-loss"; fi
if [[ "$CMD" =~ [Dd][Rr][Oo][Pp][[:space:]]+[Ss][Cc][Hh][Ee][Mm][Aa] ]]; then block "data-loss"; fi
if [[ "$CMD" =~ [Tt][Rr][Uu][Nn][Cc][Aa][Tt][Ee][[:space:]]+[Tt][Aa][Bb][Ll][Ee] ]]; then block "data-loss"; fi

# --- remote-irreversible ---
# git push with -f or --force or --force-with-lease (flag anywhere after "git push")
if [[ "$CMD" =~ git[[:space:]]+push([[:space:]]+[^[:space:]]*)*[[:space:]]--force([[:space:]]|$) ]]; then block "remote-irreversible"; fi
if [[ "$CMD" =~ git[[:space:]]+push([[:space:]]+[^[:space:]]*)*[[:space:]]--force-with-lease ]]; then block "remote-irreversible"; fi
if [[ "$CMD" =~ git[[:space:]]+push([[:space:]]+[^[:space:]]*)*[[:space:]]-[a-zA-Z]*f ]]; then block "remote-irreversible"; fi
# git push --delete
if [[ "$CMD" =~ git[[:space:]]+push[[:space:]]+--delete ]]; then block "remote-irreversible"; fi
# git branch -D
if [[ "$CMD" =~ git[[:space:]]+branch[[:space:]]+-D ]]; then block "remote-irreversible"; fi
# gh pr merge
if [[ "$CMD" =~ gh[[:space:]]+pr[[:space:]]+merge ]]; then block "remote-irreversible"; fi
# kubectl delete
if [[ "$CMD" =~ kubectl[[:space:]]+delete ]]; then block "remote-irreversible"; fi
# terraform apply/destroy
if [[ "$CMD" =~ terraform[[:space:]]+(apply|destroy) ]]; then block "remote-irreversible"; fi

# --- credentials ---
# editing .env files
if [[ "$CMD" =~ (vim|vi|nano|code|tee)[[:space:]]+.*\.env ]]; then block "credentials"; fi
if [[ "$CMD" =~ (vim|vi|nano|code)[[:space:]]+.*secrets ]]; then block "credentials"; fi
# aws iam key management
if [[ "$CMD" =~ aws[[:space:]]+iam[[:space:]]+(create|delete|update)-access-key ]]; then block "credentials"; fi

# --- shared-comms ---
# curl to webhook endpoints
if [[ "$CMD" =~ curl.*hooks\.(slack|discord|teams|zapier)\.com ]]; then block "shared-comms"; fi
if [[ "$CMD" =~ curl.*api\.slack\.com ]]; then block "shared-comms"; fi
# gh issue/pr comment/create/close
if [[ "$CMD" =~ gh[[:space:]]+(issue|pr)[[:space:]]+(comment|create|close) ]]; then block "shared-comms"; fi
# mail / sendmail
if [[ "$CMD" =~ mail[[:space:]]+-s ]]; then block "shared-comms"; fi
if [[ "$CMD" =~ sendmail ]]; then block "shared-comms"; fi

# --- process ---
# kill -9 or kill -KILL
if [[ "$CMD" =~ kill[[:space:]]+(-9|-KILL) ]]; then block "process"; fi
# pkill -9
if [[ "$CMD" =~ pkill[[:space:]]+-9 ]]; then block "process"; fi
# systemctl stop/disable/mask
if [[ "$CMD" =~ systemctl[[:space:]]+(stop|disable|mask) ]]; then block "process"; fi
# docker rm/kill/stop -f
if [[ "$CMD" =~ docker[[:space:]]+(rm|kill|stop)[[:space:]]+-f ]]; then block "process"; fi

exit 0
