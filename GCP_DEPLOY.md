# Deploy MEOK Compliance MCP to Google Cloud Run

Cloud Run > a raw VM: container-native, public HTTPS, scales to zero (near-free idle),
no server to manage. Each flagship = one deploy. **Run from a terminal where gcloud auth works**
(this build box's sandbox blocks oauth2.googleapis.com, so the deploy runs on your machine).

## One-time setup
```bash
gcloud config set project meok-498012
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

## Path A — deploy from source (simplest; no registry/visibility hassle)
```bash
git clone https://github.com/CSOAI-ORG/meok-compliance-gateway && cd meok-compliance-gateway
gcloud run deploy eu-ai-act-mcp --source . \
  --port 8000 --allow-unauthenticated --region europe-west2
# Cloud Build builds the default PKG=eu-ai-act image and deploys. ~3 min.
```
For other flagships, rebuild with a build-arg via Cloud Build, or use Path B images.

## Path B — deploy the prebuilt GHCR images (fastest)
Images already pushed: `ghcr.io/csoai-org/{eu-ai-act,dora,nis2,cra}-mcp:latest`
First make each GHCR package **public** (GitHub → your packages → package → settings → change visibility → Public), then:
```bash
for s in eu-ai-act dora nis2 cra; do
  gcloud run deploy $s-mcp \
    --image ghcr.io/csoai-org/$s-mcp:latest \
    --port 8000 --allow-unauthenticated --region europe-west2 --project meok-498012
done
```

## Result
Each gives a public endpoint: `https://<svc>-<hash>.europe-west2.run.app/mcp` (streamable-HTTP, verified HTTP 200).

## Then → money
1. **List on AWS Marketplace / Smithery** using the same image (billable enterprise).
2. **x402 wrap** the Cloud Run URL + your Coinbase wallet → per-call revenue + auto-lists in x402 Bazaar.
3. Point the meok.ai/csoai.org checkout + in-tool upsell at the hosted endpoint.

MEOK AI Labs · CSOAI LTD (UK CH 16939677) · MIT.
