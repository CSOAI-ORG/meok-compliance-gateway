# MEOK Compliance Gateway

<!-- OpenSSF + hygiene badges (auto-inserted by add_openssf_badge.py) -->
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/CSOAI-ORG/meok-compliance-gateway/badge)](https://scorecard.dev/viewer/?uri=github.com/CSOAI-ORG/meok-compliance-gateway)
[![License](https://img.shields.io/github/license/CSOAI-ORG/meok-compliance-gateway)](https://github.com/CSOAI-ORG/meok-compliance-gateway/blob/main/LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/CSOAI-ORG/meok-compliance-gateway)](https://github.com/CSOAI-ORG/meok-compliance-gateway/commits/main)

Streamable-HTTP / containerized builds of MEOK AI Labs compliance MCP servers —
the HTTP transport that cloud marketplaces (AWS Bedrock AgentCore, Google, Azure,
Smithery) and x402 monetization require.

`http_server.py` serves any MEOK FastMCP server over streamable-HTTP at `/mcp`
(verified: `initialize` → HTTP 200). One container image per flagship via the
`PKG` build arg. See **LISTING.md** for the full deploy + marketplace playbook.

```bash
docker build --build-arg PKG=eu-ai-act-compliance-mcp -t meok/eu-ai-act .
docker run -p 8000:8000 meok/eu-ai-act    # → POST /mcp
```

Flagships: eu-ai-act · dora · nis2 · cra (+ any of the 290 MEOK MCP servers).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> ⚠️ **2026-07-28 MCP spec freeze in ~8 weeks** — this gateway tracks the 2025-03-26 spec. Migration plan: see [LISTING.md § MCP Spec Freeze](./LISTING.md#-mcp-2026-07-28-spec-freeze-8-weeks).

MIT-licensed. MEOK AI Labs (CSOAI LTD, UK CH 16939677).
