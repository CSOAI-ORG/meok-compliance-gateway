#!/usr/bin/env bash
# check-secret-perms.sh — audit & fix perms on MEOK's local secret files.
#
# Per the SOV3 master audit (CRITICAL #2, sov3_mcp_master_audit.docx 2026-06-08):
# the fleet stores API keys at ~/.meok/*.json and ~/.meok/*.key. The audit found
# these files world-readable by default on macOS / Linux — any process running
# as the user (or any local user on a shared host) can read all 76 MCP servers'
# API keys, including MEOK_ATTESTATION_KEY.
#
# This script:
#   1. Enumerates known secret files under ~/.meok/
#   2. Reports any file whose mode is not 0o600 (or stricter)
#   3. With --fix, tightens them in place
#   4. With --precommit, exits non-zero on any violation (use in CI / git hook)
#
# The PROPER fix is to move all secrets to the OS keyring (see CRITICAL_FIXES_2026-
# 06-08.md Fix #2) — this script is a stopgap until then.
#
# Usage:
#   scripts/check-secret-perms.sh                # audit (read-only)
#   scripts/check-secret-perms.sh --fix          # chmod 600 in place
#   scripts/check-secret-perms.sh --precommit    # exit 1 on any violation
#
# Exit codes:
#   0 — clean (or all violations fixed with --fix)
#   1 — at least one violation detected (--precommit / audit)
#   2 — bad usage

set -euo pipefail

usage() {
  sed -n '2,20p' "$0"
  exit "${1:-0}"
}

MODE="audit"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --fix)       MODE="fix" ;;
    --precommit) MODE="precommit" ;;
    -h|--help)   usage 0 ;;
    *)           echo "Unknown arg: $1" >&2; usage 2 ;;
  esac
  shift
done

# Known secret locations across the fleet. Add new patterns as they're added.
SECRET_DIR="${MEOK_HOME:-$HOME/.meok}"
PATTERNS=(
  "api_keys.json"
  "*.key"
  "*.secret"
  "*.pem"
  "webhook_secret"
  "stripe_webhook_secret"
)

if [[ ! -d "$SECRET_DIR" ]]; then
  case "$MODE" in
    audit|precommit)
      echo "OK  $SECRET_DIR does not exist — nothing to check."
      exit 0
      ;;
  esac
  echo "ERR  $SECRET_DIR does not exist; nothing to fix."
  exit 0
fi

violations=0
checked=0
for pattern in "${PATTERNS[@]}"; do
  # -L follows symlinks; nullglob ensures empty globs expand to nothing.
  shopt -s nullglob
  for f in "$SECRET_DIR"/$pattern; do
    [[ -e "$f" ]] || continue
    checked=$((checked + 1))
    # st_mode & 0o077 → bits for group + other. If ANY of those bits are set, the
    # file is readable by group/other. Owner-only is 0600 (or 0400 read-only).
    mode=$(stat -f '%Lp' "$f" 2>/dev/null || stat -c '%a' "$f" 2>/dev/null)
    group_other=$((mode & 077))
    if [[ "$group_other" -ne 0 ]]; then
      violations=$((violations + 1))
      case "$MODE" in
        fix)
          chmod 600 "$f"
          echo "FIX  $f  (was $mode, now 600)"
          ;;
        audit|precommit)
          echo "BAD  $f  (mode=$mode, group/other bits set)"
          echo "     fix with: chmod 600 \"$f\""
          ;;
      esac
    else
      case "$MODE" in
        audit)
          echo "OK   $f  (mode=$mode)"
          ;;
        fix)
          echo "OK   $f  (mode=$mode, no change)"
          ;;
      esac
    fi
  done
done

# Even when --fix is passed, also tighten the directory itself (no 'execute' for
# other is fine, but 'read' for other leaks filenames).
dir_mode=$(stat -f '%Lp' "$SECRET_DIR" 2>/dev/null || stat -c '%a' "$SECRET_DIR" 2>/dev/null)
if [[ $((dir_mode & 077)) -ne 0 ]]; then
  case "$MODE" in
    fix)
      chmod 700 "$SECRET_DIR"
      echo "FIX  $SECRET_DIR  (was $dir_mode, now 700)"
      ;;
    *)
      echo "BAD  $SECRET_DIR  (mode=$dir_mode, group/other readable — leaks filenames)"
      ;;
  esac
  [[ "$MODE" != "fix" ]] && violations=$((violations + 1))
fi

if [[ "$checked" -eq 0 ]]; then
  echo "OK  no secret files found under $SECRET_DIR (check the path if you expected some)."
fi

if [[ "$violations" -gt 0 ]]; then
  echo ""
  echo "Found $violations permission violation(s). Run: $0 --fix"
  [[ "$MODE" == "precommit" ]] && exit 1
fi

# Always print the keyring recommendation
echo ""
echo "── PROPER FIX ──────────────────────────────────────────────────────────"
echo "Migrate secrets to the OS keyring (macOS Keychain / Linux Secret Service):"
echo "  python -c \"import keyring; keyring.set_password('meok.ai', 'attestation-key', '<your-key>')\""
echo "  python -c \"import keyring; keyring.set_password('meok.ai', 'openai-api-key',    '<your-key>')\""
echo "Then delete the plaintext file:"
echo "  rm -f ~/.meok/*.key ~/.meok/*.json"
echo "See CRITICAL_FIXES_2026-06-08.md Fix #2 for the wrapper that reads from"
echo "keyring with file-fallback and a strict chmod 600 guard."
exit 0
