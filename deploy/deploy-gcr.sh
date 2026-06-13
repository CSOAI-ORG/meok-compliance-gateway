#!/usr/bin/env bash
# ============================================================================
# Cloud Run Deploy Fix — Build Local → GCR → Cloud Run
# ============================================================================
# Cloud Run only accepts images from GCR, Artifact Registry, or Docker Hub.
# GHCR images need to be mirrored to GCR first.
#
# PREREQUISITE: Start Docker Desktop or OrbStack first!
#   open -a "Docker Desktop"  # or  open -a OrbStack
#
# Then run this script.
# ============================================================================

set -euo pipefail

PROJECT_ID="meok-498012"
REGION="europe-west2"
GCR_HOST="gcr.io"

# Flagships: name : pypi_package
flagships=(
  "eu-ai-act:eu-ai-act-compliance-mcp"
  "dora:dora-compliance-mcp"
  "nis2:nis2-compliance-mcp"
  "cra:cra-compliance-mcp"
)

echo "=== CSOAI Cloud Run Deploy (GCR Mirror) ==="
echo "Project: $PROJECT_ID"
echo "Region:  $REGION"
echo ""

# Check Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo ""
    echo "Start Docker first:"
    echo "  open -a \"Docker Desktop\""
    echo "  # or"
    echo "  open -a OrbStack"
    echo ""
    echo "Then re-run this script."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Configure gcloud docker auth
echo "🔐 Configuring Docker auth for GCR..."
gcloud auth configure-docker gcr.io --quiet

# Build, tag, push, deploy each flagship
for entry in "${flagships[@]}"; do
    flagship="${entry%%:*}"
    pkg="${entry#*:}"
    
    local_img="csoai-org/${flagship}-mcp:latest"
    gcr_img="${GCR_HOST}/${PROJECT_ID}/${flagship}-mcp:latest"
    svc_name="${flagship}-mcp"
    
    echo ""
    echo ">>> Processing $flagship ($pkg)"
    echo "    Local:  $local_img"
    echo "    GCR:    $gcr_img"
    echo "    Service: $svc_name"
    echo ""
    
    # Build
    echo "🔨 Building..."
    docker build --build-arg PKG="$pkg" -t "$local_img" .
    
    # Tag for GCR
    echo "🏷️  Tagging for GCR..."
    docker tag "$local_img" "$gcr_img"
    
    # Push to GCR
    echo "📤 Pushing to GCR..."
    docker push "$gcr_img"
    
    # Deploy to Cloud Run
    echo "🚀 Deploying to Cloud Run..."
    gcloud run deploy "$svc_name" \
        --image "$gcr_img" \
        --region "$REGION" \
        --project "$PROJECT_ID" \
        --platform managed \
        --allow-unauthenticated \
        --max-instances 10 \
        --memory "1Gi" \
        --cpu "1" \
        --port 8000 \
        --set-env-vars "PORT=8000,PYTHONUNBUFFERED=1" \
        --no-cpu-throttling \
        --timeout 300 \
        --concurrency 100
    
    echo ""
    echo "✅ $flagship deployed!"
    echo ""
done

echo ""
echo "=== ALL FLAGSHIPS DEPLOYED ==="
echo ""
echo "Endpoints:"
for entry in "${flagships[@]}"; do
    flagship="${entry%%:*}"
    svc_name="${flagship}-mcp"
    url=$(gcloud run services describe "$svc_name" --region "$REGION" --project "$PROJECT_ID" --format 'value(status.url)' 2>/dev/null || echo "pending")
    echo "  $flagship: $url"
done

echo ""
echo "Test with:"
echo "  curl -XPOST <url>/mcp -H 'content-type: application/json' \\"
echo "    -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\"...}'"
echo ""
