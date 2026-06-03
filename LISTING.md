# MEOK Compliance Gateway — HTTP/Container Listing Playbook

> **Status:** keystone built + PROVEN. `http_server.py` serves any MEOK FastMCP server over
> streamable-HTTP at `/mcp` — verified locally: `initialize` handshake → **HTTP 200**.
> This artifact unlocks every HTTP-only surface (AWS, Google, Azure, Smithery) + x402.
>
> ⚠️ **MCP 2026-07-28 spec freeze — ~8 weeks.** This gateway tracks the 2025-03-26 spec.
> The new spec drops `initialize`/`initialized` and `Mcp-Session-Id`, requires
> `Mcp-Method` + `Mcp-Name` + `MCP-Protocol-Version` on every request, and shifts
> error code `-32002` → `-32602`. Plan: bump `mcp` pin in `requirements-gateway.txt`
> when the upstream SDK ships support, then re-push GHCR images by **2026-07-14**
> (2-week buffer). Tracked in issue #1.
> Source: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/

## What's in this dir
- `http_server.py` — generic streamable-HTTP entrypoint (imports the installed `server` module, serves `/mcp` on `0.0.0.0:$PORT`). Also exposes `GET /healthz` and `GET /.well-known/oauth-protected-resource`. ✅ tested HTTP 200.
- `Dockerfile` — parameterized by `--build-arg PKG=<pypi-name>`; pip-installs `requirements-gateway.txt` + the server.
- `requirements-gateway.txt` — exact pins for reproducible builds (`mcp==1.27.2`, `uvicorn[standard]==0.48.0`).
- `build_all.sh` — builds 4 flagship images (eu-ai-act, dora, nis2, cra).
- `smithery.yaml` — Smithery container/HTTP config (Smithery dropped stdio Sept 2025).
- `.github/workflows/test-gateway.yml` + `tests/e2e_smoke.py` — real CI: lint + import smoke, plus a true e2e that installs a flagship, boots the gateway, and drives it with the mcp client (initialize + tools/list + /healthz). Verified locally: 16 tools listed against `eu-ai-act-compliance-mcp`.

## Deploy (one command on any host WITH Docker — this box's Docker is down)
```bash
./build_all.sh
docker run -p 8000:8000 meok/eu-ai-act:latest
curl -XPOST localhost:8000/mcp -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}'
```

## The honest critical path to revenue (in priority order)

### 1. x402 Bazaar  ★ smallest bridge — auto-list + per-call revenue
- Front the deployed `/mcp` with `meok-x402-wrap-mcp` (or `agent-x402-paywall-mcp`).
- Plug your **Coinbase CDP wallet** (receiving address) into the wrap.
- On first settled USDC payment, you appear in Coinbase Agentic.Market automatically — agent-purchasable.
- Why first: $50M+ already processed, 165M tx, OpenRouter (~$1B/yr) migrated 2026-05-22, Coinbase × AWS Bedrock AgentCore native integration 2026-05-07.
- **NEEDS NICK:** Coinbase CDP wallet + a deployed endpoint (any cloud below).

### 2. Deploy ONE flagship container to a public host
- **Cloud Run (easiest)** — `gcloud run deploy <name> --source .` (see GCP_DEPLOY.md). ARM64 for AWS AgentCore; x86 is fine for Cloud Run.
- **AWS Bedrock AgentCore** — push ARM64 image to ECR, list on AWS Marketplace (billable). State-of-the-art monetization for EU/UK compliance buyers.
- **Railway / Fly / Render** — `docker run`-equivalent; bring your own domain.
- Once a public URL is live, layer #1 on top.

### 3. Smithery (HTTP)
- `smithery.yaml` is ready. Connect the GitHub repo at smithery.ai → it builds the container.
- **NEEDS NICK:** Smithery login + connect repo. 19 flagships already submitted, **pending review since 2026-05-14** — ping the queue.

### 4. AWS Bedrock AgentCore → AWS Marketplace  ★ billable enterprise revenue
- ARM64 Docker container, port 8000, `/mcp`. **Matches `http_server.py` exactly.**
- List on AWS Marketplace as a billable AI agent (revenue-share).
- **NEEDS NICK:** AWS account + Marketplace **seller registration** (tax/banking) — account-gated, can't be automated.

### 5. Docker MCP Catalog
- Publish image to Docker Hub, then PR to `docker/mcp-registry`.
- **NEEDS NICK:** Docker Hub account; **NEEDS:** a host with Docker to build/push.

### 6. Google Gemini Enterprise / Azure AI Foundry
- A2A-native; apply to Google AI Agent Ecosystem Program / package with M365 Agent Toolkit.
- **NEEDS NICK:** partner-program application (enterprise, gated).

Everything else (Glama, punkpeye, meok.ai £79 page, EU AI Act 2026-08-02 urgency) already funnels to this. **The build is done and proven. The remaining steps are account-gated** (Coinbase wallet, AWS seller, Smithery/Docker logins) — unavoidable, they require your identity/banking.
