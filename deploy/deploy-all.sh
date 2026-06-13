#!/usr/bin/env bash
# Deploy all 4 flagship MCPs to Google Cloud Run.
# Uses pre-built GHCR images. Run from meok-compliance-gateway/.
#
# Prerequisites:
#   gcloud auth login
#   gcloud config set project meok-498012
#   gcloud services enable run.googleapis.com
#   GHCR images must be public (GitHub → Packages → Settings → Public)
#
# Usage:
#   ./deploy/deploy-all.sh

set -euo pipefail

PROJECT_ID="meok-498012"
REGION="europe-west2"
MAX_INSTANCES=10
MEMORY="1Gi"
CPU="1"
PORT=8000

SERVICES=(
  "eu-ai-act-mcp:ghcr.io/csoai-org/eu-ai-act-mcp:latest"
  "dora-mcp:ghcr.io/csoai-org/dora-mcp:latest"
  "nis2-mcp:ghcr.io/csoai-org/nis2-mcp:latest"
  "cra-mcp:ghcr.io/csoai-org/cra-mcp:latest"
)

echo "=== MEOK Compliance Gateway — Cloud Run Deploy ==="
echo "Project: $PROJECT_ID"
echo "Region:  $REGION"
echo ""

for entry in "${SERVICES[@]}"; do
  svc="${entry%%:*}"
  img="${entry#*:}"
  echo ">>> Deploying $svc from $img ..."
  gcloud run deploy "$svc" \
    --image "$img" \
    --region "$REGION" \
    --project "$PROJECT_ID" \
    --platform managed \
    --allow-unauthenticated \
    --max-instances "$MAX_INSTANCES" \
    --memory "$MEMORY" \
    --cpu "$CPU" \
    --port "$PORT" \
    --set-env-vars "PORT=$PORT,PYTHONUNBUFFERED=1" \
    --no-cpu-throttling \
    --quiet
  echo "    ✅ $svc deployed"
  echo ""
done

echo "=== All 4 flagships deployed ==="
echo ""
echo "Endpoints:"
for entry in "${SERVICES[@]}"; do
  svc="${entry%%:*}"
  url=$(gcloud run services describe "$svc" --region "$REGION" --project "$PROJECT_ID" --format 'value(status.url)' 2>/dev/null || echo "pending")
  echo "  $svc -> $url/mcp"
done

echo ""
echo "Next: configure x402 wallet secret"
echo "  gcloud secrets create x402-wallet --data-file=- <<< '{\"pay-to\":\"0xYOUR_ADDRESS\"}'"
