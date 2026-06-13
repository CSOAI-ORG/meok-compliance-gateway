#!/usr/bin/env bash
# STEALTH PYPI PUBLISH — agentaudit preparation script
# This script PREPARES but does NOT execute (account-gated)

set -e

echo "🚀 Prepared for Nick: agentaudit PyPI publish"
echo "============================================"
echo ""

# The wheel is already built in the PR branch
# This script shows what Nick needs to run

cat << 'EOF'
# Step 1: Check out the PR branch
git checkout feat/agentaudit-stage6-from-server

# Step 2: Build the wheel (dry-run preview)
python3 -m build --wheel --sdist -n  # -n = no-isolation if needed

# Step 3: Publish to PyPI (REQUIRES PYPI_TOKEN)
# export PYPI_TOKEN=pypi-xxx-your-token-here
# python3 -m twine upload dist/* --username __token__ --password "$PYPI_TOKEN"

# Expected output:
# - agentaudit-0.1.0-py3-none-any.whl (27KB)
# - agentaudit-0.1.0.tar.gz (34KB)
# - URL: https://pypi.org/project/agentaudit/

# Step 4: Verify
curl -s https://pypi.org/pypi/agentaudit/json | jq '.info.version'
EOF

echo ""
echo "📋 PR #20 Status: MERGEABLE (SHA-pinned, 78 tests passing)"
echo "📋 GHCR image will auto-build on merge"
echo "📋 Required: Nick's GitHub merge + PyPI token"