# MEOK Fleet MCP Base — Template

> **The base every MEOK flagship MCP server should be a thin wrapper around.**
> Born from the 2026-06-03 audit. Each flagship repo should contain only:
> 1. The flagship's specific tools/prompts (the "what")
> 2. A copy of this template's infra (the "how")
>
> Goal: when the **MCP 2026-07-28 spec** freezes, one PR to this base repo
> (or a coordinated fleet-sync) upgrades all 290 flagships in lockstep.

## What every flagship repo must contain

### Required files
```
README.md            # Install, env, one curl example, license badge
LICENSE              # MIT
pyproject.toml       # declares the PKG name + entry point
Dockerfile           # from this template
smithery.yaml        # Smithery container/HTTP config (runtime: container)
requirements.txt     # mcp==<gateway pin>, uvicorn[standard]==<gateway pin>
server.py            # imports mcp from mcp.server.fastmcp; @mcp.tool() decorators
.github/workflows/test.yml  # lint + import + real e2e (install PKG, boot, initialize + tools/list)
SECURITY.md          # vulnerability disclosure + signed commits
```

### Recommended files
```
http_server.py       # streamable-HTTP shim (only if you want marketplace deployment)
AGENTS.md            # distribution snippet for LLM agents
Dockerfile.glama     # if you also want Glama distribution
```

## Canonical Dockerfile (matches meok-compliance-gateway)
```dockerfile
# Pinned by digest for reproducible builds (tag kept for readability).
# Re-resolve with:  docker buildx imagetools inspect python:3.11-slim
FROM python:3.11-slim@sha256:a3ab0b966bc4e91546a033e22093cb840908979487a9fc0e6e38295747e49ac0
ARG PKG=<pypi-flagship-name>
ENV PORT=8000 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt "${PKG}"
COPY server.py /app/server.py
COPY http_server.py /app/http_server.py  # if applicable
# Run unprivileged — required by Docker MCP Catalog / AWS Marketplace review.
RUN useradd --create-home --uid 10001 app && chown -R app:app /app
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import os,sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:%s/healthz' % os.environ.get('PORT','8000'), timeout=2).status==200 else 1)"
CMD ["python", "http_server.py"]
```

## Canonical requirements.txt
```
mcp==1.27.2
uvicorn[standard]==0.48.0
```

## Canonical server.py
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("<flagship-name>")

@mcp.tool()
def ping() -> str:
    """Health check — returns 'pong'."""
    return "pong"
```

## Canonical http_server.py (adds /healthz + RFC 9728)
See `/Users/nicholas/meok-compliance-gateway/http_server.py` for the production version.

## Canonical .github/workflows/test.yml
```yaml
name: test
on: [push, pull_request]
jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - uses: actions/setup-node@v4
        with: {node-version: '20'}
      - run: pip install -r requirements.txt "<pypi-flagship-name>"
      - run: python -m py_compile server.py http_server.py
      # Real e2e — boot the actual gateway, drive it with the mcp client:
      - run: |
          PORT=8000 python http_server.py & echo $! > /tmp/gw.pid
          for i in $(seq 1 30); do curl -fsS localhost:8000/healthz >/dev/null 2>&1 && break; sleep 1; done
          python - <<'PY'
          import anyio
          from mcp import ClientSession
          from mcp.client.streamable_http import streamablehttp_client
          async def main():
              async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (r, w, _):
                  async with ClientSession(r, w) as s:
                      await s.initialize()
                      assert (await s.list_tools()).tools, "no tools"
                      print("e2e OK")
          anyio.run(main)
          PY
          kill "$(cat /tmp/gw.pid)" 2>/dev/null || true
```
> The gateway repo's `tests/e2e_smoke.py` is the reference implementation of this step
> (verified: 16 tools listed against `eu-ai-act-compliance-mcp`).

## Canonical smithery.yaml
```yaml
runtime: container
startCommand:
  type: http
  configSchema: {}
build:
  dockerfile: Dockerfile
  dockerBuildArgs:
    PKG: <pypi-flagship-name>
```

## 2026-07-28 migration checklist
For every flagship, before July 14, 2026:
- [ ] Bump `mcp==1.27.2` → the next stable that ships 2026-07-28 spec support
- [ ] Update `http_server.py` to validate `Mcp-Method` / `Mcp-Name` headers
- [ ] Remove reliance on `initialize` / `initialized` handshake in any tests
- [ ] Add `MCP-Protocol-Version: 2026-07-28` to all curl examples in README
- [ ] Re-push image and re-test on AWS AgentCore / Smithery

## Audit script (run from a clean clone of one flagship)
```bash
for f in README.md LICENSE pyproject.toml Dockerfile smithery.yaml requirements.txt server.py .github/workflows/test.yml SECURITY.md; do
  [ -f "$f" ] && echo "✓ $f" || echo "✗ MISSING: $f"
done
```

## Per-call monetization (x402) — a second revenue rail
Stripe subscriptions bill **humans**; x402 bills **autonomous agents** per call in USDC,
and on first settled payment auto-lists the endpoint in the x402 Bazaar / AWS AgentCore.
Both run at once. Use `meok_x402.paywalled` (in `meok-compliance-gateway`) on **high-value**
tools only — keep `quick_scan` / `deadline_check` FREE as top-of-funnel.

```python
from meok_x402 import paywalled
from mcp.server.fastmcp import Context

@mcp.tool()
@paywalled(price="$0.25")          # OFF unless X402_ENABLED — free self-host is unaffected
def audit_report(system: str, ctx: Context) -> dict:   # declare ctx so FastMCP injects it
    """COST WARNING: $0.25/call. Full 42-point EU AI Act audit. ..."""   # AWS billable-tool convention
    ...
```
Enable per-deployment with env: `X402_ENABLED=1`, `X402_PAY_TO=<Coinbase CDP wallet>`,
`X402_PRICE`, `X402_NETWORK` (Base mainnet `eip155:8453`). Add `requirements-x402.txt`
(`x402[evm]`) to the image. Tools that take payment must put **`COST WARNING:`** in their
description (AWS Marketplace / AgentCore requirement so agents know before calling).
Rollout: wallet + apply `@paywalled` to the 4–5 highest-value tools per flagship.

## Reference implementations
- `meok-compliance-gateway` — the gateway shim + `meok_x402.py` (this template's source of truth)
- `eu-ai-act-compliance-mcp` — the gold-standard flagship (server.py + tests + smithery + Dockerfile.glama)
- `soc2-compliance-ai-mcp` — second gold-standard flagship (auth_middleware.py + MEOK Compliance PDCA workflow)
