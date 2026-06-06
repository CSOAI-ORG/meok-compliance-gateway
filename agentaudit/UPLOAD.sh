#!/usr/bin/env bash
# Staged upload for agentaudit to PyPI.
# Nick-only: requires PYPI_API_TOKEN env var.
set -euo pipefail
cd "$(dirname "$0")"

WHEEL="dist/agentaudit-0.1.0-py3-none-any.whl"
if [[ ! -f "$WHEEL" ]]; then
    echo "Wheel not found. Building..."
    python -m build --wheel
fi

echo "Uploading $WHEEL to PyPI..."
python -m twine upload \
    --repository pypi \
    --username __token__ \
    --password "${PYPI_API_TOKEN:?PYPI_API_TOKEN required}" \
    "$WHEEL"

echo "Done. agentaudit is live on PyPI."
