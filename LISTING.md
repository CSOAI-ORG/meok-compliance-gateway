# MEOK Compliance Gateway — HTTP/Container Listing Playbook

**Status:** keystone built + PROVEN. `http_server.py` serves any MEOK FastMCP server over
streamable-HTTP at `/mcp` — verified locally: `initialize` handshake → **HTTP 200**.
This artifact unlocks every HTTP-only surface (AWS, Google, Azure, Smithery) + x402.

## What's in this dir
- `http_server.py` — generic streamable-HTTP entrypoint (imports the installed `server` module, serves `/mcp` on `0.0.0.0:$PORT`). ✅ tested HTTP 200.
- `Dockerfile` — parameterized by `--build-arg PKG=<pypi-name>`; pip-installs the server + uvicorn.
- `build_all.sh` — builds 4 flagship images (eu-ai-act, dora, nis2, cra).
- `smithery.yaml` — Smithery container/HTTP config (Smithery dropped stdio Sept 2025).

## Deploy (one command on any host WITH Docker — this box's Docker is down)
```
./build_all.sh
docker run -p 8000:8000 meok/eu-ai-act:latest
curl -XPOST localhost:8000/mcp -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}'
```

## Marketplace listing paths

### 1. AWS Bedrock AgentCore → AWS Marketplace  ★ billable revenue
- Push image to ECR → deploy to AgentCore Runtime (it hosts MCP servers; stateful added Mar 2026).
- List on AWS Marketplace as a billable AI agent (revenue-share). **Best monetization for EU/UK compliance buyers.**
- **NEEDS NICK:** AWS account + Marketplace **seller registration** (tax/banking) — account-gated, can't be automated.

### 2. Smithery (HTTP)
- `smithery.yaml` is ready. Connect the GitHub repo at smithery.ai → it builds the container.
- **NEEDS NICK:** Smithery login + connect repo.

### 3. Docker MCP Catalog
- Publish image to Docker Hub, then PR to `docker/mcp-registry`.
- **NEEDS NICK:** Docker Hub account; **NEEDS:** a host with Docker to build/push.

### 4. Google Gemini Enterprise / Agent Garden + Azure AI Foundry
- A2A-native; apply to Google AI Agent Ecosystem Program / package with M365 Agent Toolkit.
- **NEEDS NICK:** partner-program application (enterprise, gated).

### 5. x402 Bazaar  ★ auto-list + per-call revenue (the £ frontier)
- Put `agent-x402-paywall-mcp` / `meok-x402-wrap-mcp` in front of the deployed `/mcp` endpoint.
- On first settled payment, you appear in the x402 Bazaar automatically — agent-purchasable.
- **NEEDS NICK:** Coinbase CDP wallet (receiving address) + deployed endpoint (from above).

## The honest critical path to revenue
1. Deploy ONE flagship container to any host (AWS/Railway/Fly/Render) — **your cloud account**.
2. Front it with x402 wrap + your Coinbase wallet → per-call revenue + auto-Bazaar listing.
3. List the same image on AWS Marketplace (billable) + Smithery.
4. Everything else (registry, Glama, punkpeye, meok.ai £79 page) already funnels to this.

The build is done and proven. The remaining steps are **account-gated** (AWS seller, Coinbase
wallet, Smithery/Docker logins) — unavoidable, they require your identity/banking.
