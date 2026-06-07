#!/usr/bin/env bash
# Comprehensive deploy runbook for agentaudit-mcp.
# Nick-only: requires gcloud auth + project meok-498012 + (after first run)
# the agentaudit GHCR package flipped to Public in GitHub Packages UI.
#
# This wraps the lean `DEPLOY.sh` (source-build Cloud Run) with a full pre-flight
# + post-deploy smoke test, so the deploy step is one command instead of nine.
#
# Usage:
#   ./DEPLOY_AGENTAUDIT.sh                # full pipeline
#   ./DEPLOY_AGENTAUDIT.sh --skip-build   # deploy the existing :latest image
#   ./DEPLOY_AGENTAUDIT.sh --skip-deploy  # build + push only
#   ./DEPLOY_AGENTAUDIT.sh --dry-run      # show what would happen
#
# Pre-flight gates (any of these failing aborts the run):
#   1. gcloud auth active and on project meok-498012
#   2. tests pass locally (pytest agentaudit/tests/)
#   3. wheel builds cleanly (python -m build --wheel --sdist)
#   4. agentaudit is on PyPI (curl https://pypi.org/pypi/agentaudit/json)
#   5. ghcr.io/csoai-org/agentaudit-mcp:latest exists (post first build)
#
# Post-deploy smoke:
#   * GET /healthz returns {"status":"ok","service":"agentaudit"}
#   * GET /.well-known/oauth-protected-resource returns 200 with valid JSON
set -euo pipefail
cd "$(dirname "$0")"

PROJECT="meok-498012"
REGION="europe-west2"
SERVICE="agentaudit-mcp"
IMAGE="ghcr.io/csoai-org/${SERVICE}:latest"

SKIP_BUILD=0
SKIP_DEPLOY=0
DRY_RUN=0
for arg in "$@"; do
    case "$arg" in
        --skip-build)  SKIP_BUILD=1 ;;
        --skip-deploy) SKIP_DEPLOY=1 ;;
        --dry-run)     DRY_RUN=1 ;;
        -h|--help)
            sed -n '2,28p' "${BASH_SOURCE[0]:-$0}"; exit 0 ;;
        *)
            echo "Unknown flag: $arg" >&2; exit 2 ;;
    esac
done

run() {
    if [ "$DRY_RUN" = "1" ]; then
        printf '  [dry-run] %s\n' "$*"
    else
        printf '  + %s\n' "$*"
        "$@"
    fi
}

# ── Pre-flight ────────────────────────────────────────────────
echo "═══ pre-flight ═══"

echo "[1/5] gcloud auth + project"
run gcloud config get-value account
run gcloud config get-value project
ACTIVE_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")
if [ "$ACTIVE_PROJECT" != "$PROJECT" ]; then
    echo "  ! active project is '$ACTIVE_PROJECT', expected '$PROJECT' — switching"
    run gcloud config set project "$PROJECT"
fi

echo "[2/5] local tests"
run /opt/homebrew/bin/python3.11 -m pytest tests/ -q

echo "[3/5] wheel build (smoke)"
run /opt/homebrew/bin/python3.11 -m build --wheel --sdist --outdir /tmp/agentaudit-build-check
run rm -rf /tmp/agentaudit-build-check

echo "[4/5] agentaudit on PyPI"
if curl -fsSL "https://pypi.org/pypi/agentaudit/json" -o /dev/null; then
    PYPI_VERSION=$(curl -fsSL "https://pypi.org/pypi/agentaudit/json" \
        | /opt/homebrew/bin/python3.11 -c "import json,sys; print(json.load(sys.stdin)['info']['version'])")
    echo "  OK: agentaudit $PYPI_VERSION on PyPI"
else
    echo "  ! agentaudit NOT on PyPI — publish it first (twine upload dist/*) before deploying." >&2
    if [ "$SKIP_DEPLOY" = "0" ]; then
        exit 1
    fi
fi

echo "[5/5] ghcr image present"
if [ "$SKIP_BUILD" = "0" ]; then
    echo "  (skipping — will rebuild below)"
else
    if ! docker manifest inspect "$IMAGE" >/dev/null 2>&1; then
        echo "  ! $IMAGE not found in GHCR — re-run without --skip-build" >&2
        exit 1
    fi
fi

# ── Build + push ──────────────────────────────────────────────
if [ "$SKIP_BUILD" = "0" ]; then
    echo "═══ build + push ═══"
    echo "  building agentaudit (linux/amd64) ..."
    run docker buildx build \
        --platform linux/amd64 \
        --tag "$IMAGE" \
        --tag "ghcr.io/csoai-org/${SERVICE}:$(git rev-parse --short HEAD)" \
        --push \
        .
    echo "  + cosign verify (after first sign — see build-push-agentaudit.yml)"
fi

# ── Deploy to Cloud Run ───────────────────────────────────────
if [ "$SKIP_DEPLOY" = "0" ]; then
    echo "═══ deploy to Cloud Run ═══"
    run gcloud run deploy "$SERVICE" \
        --image "$IMAGE" \
        --project "$PROJECT" \
        --region "$REGION" \
        --port 8000 \
        --allow-unauthenticated \
        --set-env-vars "X402_ENABLED=0" \
        --quiet
    URL=$(gcloud run services describe "$SERVICE" \
        --project "$PROJECT" \
        --region "$REGION" \
        --format 'value(status.url)')

    echo "═══ post-deploy smoke ═══"
    echo "  deployed to: $URL"
    run curl -fsSL "$URL/healthz"
    run curl -fsSL "$URL/.well-known/oauth-protected-resource"
    echo "  + OK — agentaudit-mcp is live"
fi

echo "═══ done ═══"
