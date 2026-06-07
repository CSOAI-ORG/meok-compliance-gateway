#!/bin/bash
# Phase C verification: byte-identical diffs across all 14 repos for fixes #1 + #2.
#
# Branch-agnostic: uses `git show <branch>:<path>` so the working tree can be
# on any branch during verification. Verifies the file at the named branch.

set -uo pipefail

CLONES=/Users/nicholas/fleet-clones
KEYSTONE=/Users/nicholas/meok-worktrees/ci-hardening
PASS=0
FAIL=0

check_branch_file() {
  # check_branch_file <name> <branch> <repo-relative-path> <reference-file>
  local name=$1 branch=$2 relpath=$3 ref=$4
  local target
  target=$(git -C "$CLONES/$name" show "$branch:$relpath" 2>/dev/null) || {
    echo "FAIL $name: $branch:$relpath not present"
    FAIL=$((FAIL+1)); return
  }
  local want
  want=$(cat "$ref")
  if [ "$target" = "$want" ]; then
    echo "PASS $name: $branch:$relpath byte-identical"
    PASS=$((PASS+1))
  else
    echo "FAIL $name: $branch:$relpath divergent"
    FAIL=$((FAIL+1))
  fi
}

# Pull the keystone canonical files.
# Keystone's dependabot/codeql is on chore/ci-hardening branch.
KEYSTONE_BRANCH=chore/ci-hardening
mkdir -p /tmp/verify-dep
git -C "$KEYSTONE" show "$KEYSTONE_BRANCH:.github/dependabot.yml" > /tmp/verify-dep/dependabot.yml
git -C "$KEYSTONE" show "$KEYSTONE_BRANCH:.github/workflows/codeql.yml" > /tmp/verify-dep/codeql.yml

echo "=== Fix #1: dependabot.yml on chore/scorecard-dependabot ==="
for repo in $CLONES/*/; do
  name=$(basename "$repo")
  check_branch_file "$name" "chore/scorecard-dependabot" ".github/dependabot.yml" /tmp/verify-dep/dependabot.yml
done

echo
echo "=== Fix #2: codeql.yml on chore/scorecard-codeql ==="
for repo in $CLONES/*/; do
  name=$(basename "$repo")
  check_branch_file "$name" "chore/scorecard-codeql" ".github/workflows/codeql.yml" /tmp/verify-dep/codeql.yml
done

echo
echo "=== Summary: $PASS pass, $FAIL fail ==="
exit $FAIL
