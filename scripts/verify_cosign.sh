#!/bin/bash
# Phase C verification: structural check on cosign step in each fix-#3 branch.
# Branch-agnostic: uses `git show <branch>:<path>` to inspect the branch tip.

set -uo pipefail

CLONES=/Users/nicholas/fleet-clones
PASS=0
FAIL=0

check_cosign() {
  # check_cosign <name> <branch> <workflow-path>
  local name=$1 branch=$2 wfpath=$3
  local content
  content=$(git -C "$CLONES/$name" show "$branch:$wfpath" 2>/dev/null) || {
    echo "FAIL $name: $branch:$wfpath not present"
    FAIL=$((FAIL+1)); return
  }
  local has_installer has_sign
  has_installer=$(echo "$content" | grep -c "cosign-installer" || true)
  has_sign=$(echo "$content" | grep -c "cosign sign" || true)
  if [ "$has_installer" -ge 1 ] && [ "$has_sign" -ge 1 ]; then
    echo "PASS $name: $branch:$wfpath has cosign-installer + cosign sign"
    PASS=$((PASS+1))
  else
    echo "FAIL $name: $branch:$wfpath cosign-installer=$has_installer cosign-sign=$has_sign"
    FAIL=$((FAIL+1))
  fi
}

echo "=== Fix #3: cosign step in release-publishing workflow ==="
for repo in $CLONES/*/; do
  name=$(basename "$repo")
  # Most flagships use mcp-smithery-publish.yml
  check_cosign "$name" "chore/scorecard-cosign" ".github/workflows/mcp-smithery-publish.yml"
done

echo
echo "=== Special case: meok-mcp-injection-scan-mcp also touches mcp-registry-publish.yml ==="
check_cosign meok-mcp-injection-scan-mcp "chore/scorecard-cosign" ".github/workflows/mcp-registry-publish.yml"

echo
echo "=== Summary: $PASS pass, $FAIL fail ==="
exit $FAIL
