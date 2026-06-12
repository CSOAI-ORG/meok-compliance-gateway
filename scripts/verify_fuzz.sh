#!/bin/bash
# Phase C verification: tests/test_fuzz.py exists at feat/scorecard-fuzz and
# the test file is well-formed. Branch-agnostic.

set -uo pipefail

CLONES=/Users/nicholas/fleet-clones
PASS=0
FAIL=0

echo "=== Fix #4: tests/test_fuzz.py at feat/scorecard-fuzz ==="
for repo in $CLONES/*/; do
  name=$(basename "$repo")
  test_file_content=$(git -C "$repo" show "feat/scorecard-fuzz:tests/test_fuzz.py" 2>/dev/null) || {
    echo "FAIL $name: feat/scorecard-fuzz:tests/test_fuzz.py not present"
    FAIL=$((FAIL+1))
    continue
  }
  if [ -z "$test_file_content" ]; then
    echo "FAIL $name: empty fuzz test file"
    FAIL=$((FAIL+1))
    continue
  fi
  has_hypothesis=$(echo "$test_file_content" | grep -c "from hypothesis" || true)
  has_given=$(echo "$test_file_content" | grep -c "@given" || true)
  has_test=$(echo "$test_file_content" | grep -c "def test_" || true)
  if [ "$has_hypothesis" -ge 1 ] && [ "$has_given" -ge 1 ] && [ "$has_test" -ge 1 ]; then
    echo "PASS $name: hypothesis + @given + test function present"
    PASS=$((PASS+1))
  else
    echo "FAIL $name: hypothesis=$has_hypothesis given=$has_given test=$has_test"
    FAIL=$((FAIL+1))
  fi
done

echo
echo "=== Summary: $PASS pass, $FAIL fail ==="
exit $FAIL
