#!/usr/bin/env bash
# ============================================================================
# Cloud Run Deploy — NO DOCKER NEEDED
# Uses Google Cloud Build to build images in the cloud
# ============================================================================
# This script submits builds to Cloud Build (GCP's CI/CD) which builds
# containers in Google's infrastructure — no local Docker required!
#
# Prerequisites:
#   - gcloud installed and authenticated (✅ you have this)
#   - Project set to meok-498012 (✅ already done)
#
# Usage:
#   bash deploy/cloudbuild-deploy.sh
# ============================================================================

set -euo pipefail

PROJECT_ID="meok-498012"
REGION="europe-west2"

echo "=== CSOAI Cloud Run Deploy (Cloud Build — No Docker) ==="
echo "Project: $PROJECT_ID"
echo "Region:  $REGION"
echo ""

# Verify gcloud
gcloud config get-value project | grep -q "meok-498012" || {
    echo "❌ Project not set. Run: gcloud config set project meok-498012"
    exit 1
}

echo "✅ gcloud configured"
echo ""

# Enable required APIs
echo "🔧 Enabling APIs..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com --quiet

# Submit Cloud Build for each flagship
flagships=(
  "eu-ai-act:eu-ai-act-compliance-mcp"
  "dora:dora-compliance-mcp"
  "nis2:nis2-compliance-mcp"
  "cra:cra-compliance-mcp"
)

for entry in "${flagships[@]}"; do
    flagship="${entry%%:*}"
    pkg="${entry#*:}"
    svc_name="${flagship}-mcp"
    
    echo ""
    echo ">>> Deploying $flagship ($pkg)"
    echo ""
    
    # Submit Cloud Build
    gcloud builds submit --config="deploy/cloudbuild-${flagship}.yaml" \
        --substitutions="_PKG=${pkg},_SERVICE=${svc_name},_REGION=${REGION}" \
        --project="${PROJECT_ID}" \
        --quiet || {
        echo "⚠️  Cloud Build failed for $flagship, trying direct deploy..."
        
        # Fallback: deploy using source-based Cloud Run deploy
        gcloud run deploy "$svc_name" \
            --source . \
            --region "$REGION" \
            --project "$PROJECT_ID" \
            --platform managed \
            --allow-unauthenticated \
            --max-instances 10 \
            --memory "1Gi" \
            --cpu "1" \
            --port 8000 \
            --set-env-vars "PORT=8000,PYTHONUNBUFFERED=1,PKG=${pkg}" \
            --no-cpu-throttling \
            --timeout 300 \
            --concurrency 100 \
            --quiet
    }
    
    echo "✅ $flagship deployed!"
done

echo ""
echo "=== ALL FLAGSHIPS DEPLOYED ==="
echo ""

# Show URLs
for entry in "${flagships[@]}"; do
    flagship="${entry%%:*}"
    svc_name="${flagship}-mcp"
    url=$(gcloud run services describe "$svc_name" \
        --region "$REGION" \
        --project "$PROJECT_ID" \
        --format 'value(status.url)' 2>/dev/null || echo "pending")
    echo "  $flagship: $url"
done

echo ""
echo "Test with:"
echo "  curl -XPOST <url>/mcp -H 'content-type: application/json' \\"
echo "    -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\"...}'"
echo ""
