#!/usr/bin/env bash
# Staged Cloud Run deploy for agentaudit-mcp.
# Nick-only: requires gcloud auth + project meok-498012.
set -euo pipefail
cd "$(dirname "$0")"

PROJECT="meok-498012"
REGION="europe-west2"
SERVICE="agentaudit-mcp"

echo "Building + deploying $SERVICE to Cloud Run..."
gcloud run deploy "$SERVICE" \
    --source . \
    --project "$PROJECT" \
    --region "$REGION" \
    --port 8000 \
    --allow-unauthenticated \
    --set-env-vars "X402_ENABLED=0" \
    --quiet

echo "Deployed. Endpoint:"
gcloud run services describe "$SERVICE" \
    --project "$PROJECT" \
    --region "$REGION" \
    --format 'value(status.url)'
