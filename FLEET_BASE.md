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
README.md                       # Install, env, one curl example, license badge
LICENSE                        # Apache-2.0 (or MIT, your choice — keep consistent)
pyproject.toml                  # declares the PKG name + entry point + deps
Dockerfile.glama                # python:3.14-slim + uv, runs mcp-wrapper.py
smithery.yaml                   # declarative tool list (no `runtime:` block)
server.py                       # imports mcp from mcp.server.fastmcp; @mcp.tool() decorators
mcp-wrapper.py                  # streamable-HTTP shim importing server.mcp
auth_middleware.py              # tier check, audit log
.github/workflows/test.yml      # py_compile + pytest on Python 3.10/3.11
.github/workflows/ci.yml        # py_compile + pytest + ruff on Python 3.11/3.12
.github/workflows/mcp-smithery-publish.yml  # on release: published → nicholastempleman/<repo>
SECURITY.md                     # vulnerability disclosure + signed commits
```

### Recommended files
```
.well-known/mcp/server-card.json # Smithery discovery card
package.json                    # MCP registry metadata
glama.json                      # Glama discovery metadata
server.json                     # MCP server schema (modelcontextprotocol.io)
```

**Note:** `requirements.txt` is **not** required — gold-standards declare all deps in `pyproject.toml`.
A separate `requirements-gateway.txt` lives only in the gateway repo, where it pins the gateway's
exact `mcp==1.27.2` so the in-process `from server import mcp` resolves deterministically. Flagships
pin loose (`mcp>=1.0.0`); pip's exact-pin-takes-precedence resolves any conflict at the gateway's
`pip install -r requirements-gateway.txt "${PKG}"` boundary.

## Canonical Dockerfile (use Dockerfile.glama — matches the gateway + all 4 reference flagships)
```dockerfile
# python:3.14-slim; uv for fast pip; runs mcp-wrapper.py which exposes
# the FastMCP server over streamable-HTTP on PORT (default 8000).
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy

# uv (https://github.com/astral-sh/uv) is ~10× faster than pip for cold installs
RUN pip install --no-cache-dir uv

WORKDIR /app

# Install PKG from PyPI (a meta-package that pulls the flagship + its deps)
ARG PKG
RUN uv pip install --system "${PKG}"

# Ship the wrapper so Smithery/Cloud Run can launch it directly
COPY mcp-wrapper.py /app/mcp-wrapper.py
COPY .well-known /app/.well-known

# Unprivileged user (Cloud Run / AgentCore / Docker MCP Catalog requirement)
RUN useradd --create-home --uid 10001 app && chown -R app:app /app
USER app

ENV PORT=8000
EXPOSE 8000

# /healthz is wired in mcp-wrapper.py
CMD ["python", "mcp-wrapper.py"]
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

## Canonical mcp-wrapper.py (streamable-HTTP shim)
```python
import os
from server import mcp as mcp_server

SERVICE_NAME = os.path.basename(os.getcwd())

@mcp_server.custom_route("/.well-known/mcp/server-card.json", methods=["GET"])
async def server_card(_request):  # noqa: ANN001
    import json
    with open("/app/.well-known/mcp/server-card.json") as f:
        return json.load(f)

@mcp_server.custom_route("/health", methods=["GET"])
async def health(_request):  # noqa: ANN001
    return {"status": "ok", "service": SERVICE_NAME}

if __name__ == "__main__":
    mcp_server.settings.host = "0.0.0.0"
    mcp_server.settings.port = int(os.environ.get("PORT", "8000"))
    mcp_server.run(transport="streamable-http")
```

## Canonical .github/workflows/test.yml
```yaml
name: Test MCP Server
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11"]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with: {python-version: ${{ matrix.python-version }}}
      - name: Install dependencies
        run: pip install mcp>=1.0.0 pytest
      - name: Syntax check
        run: python -c "import py_compile; py_compile.compile('server.py', doraise=True)"
      - name: Run tests
        run: pytest tests/ -v --tb=short 2>/dev/null || echo "No tests found"
```

## Canonical smithery.yaml (declarative — no `runtime:` block)
```yaml
name: <pypi-flagship-name>
description: MCP server for <purpose>. From MEOK AI Labs.
version: 0.1.0
license: Apache-2.0
author: MEOK AI Labs
homepage: https://github.com/CSOAI-ORG/<repo>
repository: https://github.com/CSOAI-ORG/<repo>
tools:
  - name: tool_one
    description: ...
    parameters:
      - name: foo
        type: string
        required: true
  - name: tool_two
    description: ...
    parameters:
      - name: bar
        type: number
        required: false
```

> The old `runtime: container / startCommand: type: http` form is deprecated; Smithery now picks
> up the declarative form and resolves the container automatically.

## 2026-07-28 migration checklist
For every flagship, before July 14, 2026:
- [ ] Bump the loose `mcp>=1.0.0` (in `pyproject.toml`) to the next stable that ships 2026-07-28 spec support; bump the gateway's exact `mcp==1.27.2` (in `requirements-gateway.txt`) to the same version
- [ ] Update `mcp-wrapper.py` to validate `Mcp-Method` / `Mcp-Name` headers
- [ ] Remove reliance on `initialize` / `initialized` handshake in any tests
- [ ] Add `MCP-Protocol-Version: 2026-07-28` to all curl examples in README
- [ ] Re-push image and re-test on AWS AgentCore / Smithery

## Audit script (run from a clean clone of one flagship)
```bash
for f in README.md LICENSE pyproject.toml Dockerfile.glama smithery.yaml mcp-wrapper.py server.py auth_middleware.py \
         .github/workflows/test.yml .github/workflows/ci.yml \
         .github/workflows/mcp-smithery-publish.yml SECURITY.md \
         .well-known/mcp/server-card.json; do
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
- `eu-ai-act-compliance-mcp` — gold-standard compliance flagship (server.py + tests + smithery + Dockerfile.glama)
- `soc2-compliance-ai-mcp` — gold-standard compliance flagship (auth_middleware.py + MEOK Compliance PDCA workflow)
- `threat-intelligence-mcp` — security flagship (NVD/OSV/GHSA, pure-Python)
- `vulnerability-scanner-mcp` — security flagship (pyjadx + ILSpy-MCP subprocess + secret regex)
- `red-team-ops-mcp` — security flagship (pyjadx + androguard, mobile)
- `policy-engine-mcp` — security flagship (cedarpy in-process + opa subprocess fallback)
