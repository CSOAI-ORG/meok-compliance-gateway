#!/usr/bin/env bash
#
# merge_dependabot_prs.sh — batch-merge all Dependabot PRs across the MEOK fleet.
#
# Per [[meok-deep-audit-2026-06-08]] P2-3: 100+ open Dependabot PRs across
# 20 repos are a manual-merge burden for Nick (~30 min of clicking).
# This script does `gh pr merge --auto --squash` for the ones with the
# "dependencies" label, in batches of 10 per repo. Hermetic, no shared state.
#
# Usage:
#   ./merge_dependabot_prs.sh                  # merge all, all repos
#   ./merge_dependabot_prs.sh CSOAI-ORG/meok-hive   # one repo
#   ./merge_dependabot_prs.sh --dry-run        # show what would merge
#
# Per [[keyring-token-push-rule]]: env GITHUB_TOKEN 403s; we unset it so
# the keyring token (full perms) gets through.
#
# Per [[agentaudit-concurrent-session-hazards]]: this is read-only with
# respect to the keystone tree. It only touches the GitHub API.

set -euo pipefail

ORG="${ORG:-CSOAI-ORG}"
BATCH_SIZE="${BATCH_SIZE:-10}"
DRY_RUN="false"

# Repos that have dependabot PRs (per the AGENT COORDINATION BOARD)
REPOS=(
  "eu-ai-act-compliance-mcp"
  "cra-compliance-mcp"
  "dora-compliance-mcp"
  "nis2-compliance-mcp"
  "csrd-compliance-mcp"
  "gdpr-compliance-ai-mcp"
  "hipaa-compliance-mcp"
  "iso-42001-ai-mcp"
  "soc2-compliance-ai-mcp"
  "bias-detection-mcp"
  "csoai-governance-crosswalk-mcp"
  "meok-mcp-injection-scan-mcp"
  "meok-governance-engine-mcp"
  "meok-hive"
  "csoai-hive"
  "proofof-hive"
  "cobolbridge-hive"
  "agentaudit"
  "meok-cross-post"
)

# Argparse (lightweight — no dep on getopt)
TARGET_REPO=""
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN="true" ;;
    --help|-h)
      sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    CSOAI-ORG/*) TARGET_REPO="${arg#CSOAI-ORG/}" ;;
    *) echo "Unknown arg: $arg" >&2; exit 1 ;;
  esac
done

# Unset env token; let keyring token through (per [[keyring-token-push-rule]])
unset GITHUB_TOKEN
unset GH_TOKEN

merge_repo() {
  local repo="$1"
  echo
  echo "==> ${ORG}/${repo}"

  # List open Dependabot PRs. Filter on author (app/dependabot) rather than
  # the "dependencies" label — the label is only auto-applied to PRs opened
  # AFTER the .github/dependabot.yml `labels:` block is merged. Pre-existing
  # PRs (or orgs where the label isn't yet configured) come back label-less.
  local prs
  prs=$(gh pr list \
    --repo "${ORG}/${repo}" \
    --state open \
    --author app/dependabot \
    --json number,title,headRefName,isDraft,author \
    --limit "${BATCH_SIZE}" 2>/dev/null) || {
      echo "  [skip] gh pr list failed for ${repo} (auth or repo missing?)"
      return 0
    }

  local count
  count=$(echo "$prs" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
  echo "  Found ${count} dependabot PR(s) (max ${BATCH_SIZE}/run)"

  if [ "$count" = "0" ]; then
    return 0
  fi

  # Merge each, with checks gated on CI status
  echo "$prs" | python3 -c "
import json, sys
for pr in json.load(sys.stdin):
    if pr.get('isDraft'):
        print(f\"  [skip-draft] PR #{pr['number']}: {pr['title']}\")
        continue
    print(f\"  {pr['number']}  {pr['title']}\")
" | while read -r line; do
    pr_num=$(echo "$line" | awk '{print $1}')
    [ -z "$pr_num" ] && continue
    if [ "$DRY_RUN" = "true" ]; then
      echo "    [dry-run] would merge PR #${pr_num}"
    else
      # --auto waits for required checks; --squash flattens to 1 commit
      gh pr merge "${pr_num}" \
        --repo "${ORG}/${repo}" \
        --squash --auto \
        --delete-branch 2>&1 | sed 's/^/    /'
    fi
  done
}

if [ -n "$TARGET_REPO" ]; then
  merge_repo "$TARGET_REPO"
else
  for repo in "${REPOS[@]}"; do
    merge_repo "$repo"
  done
fi

echo
echo "Done. Re-run with --dry-run to preview."
