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

## Why MEOK?

- **13 unified governance frameworks** in one deployment (EU AI Act, NIST AI RMF, ISO 42001, ISO 27001, SOC 2, GDPR, HIPAA, DORA, NIS2, CRA, CSRD, ESG, supply-chain).
- **410 verbatim EU AI Act articles** as a parseable source-of-truth (not a third-party summary).
- **HMAC-SHA256 signed attestations** + **BFT consensus** for governance decisions — every audit trail is offline-verifiable, no single point of failure.
- **48-hour zero-config deployment** for the EU AI Act wedge (vs 2.5–9 months for OneTrust, Vanta, Drata, Holistic AI).
- **First governance layer for the 35,000+ MCP server ecosystem** — 13 of 15 GRC competitors have zero MCP presence.

Full source-of-truth + per-surface copy: [KEY_DIFFERENTIATORS.md](./KEY_DIFFERENTIATORS.md). External-comms rubric: [RUBRIC_EXTERNAL_COMMS.md](./RUBRIC_EXTERNAL_COMMS.md).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> ⚠️ **2026-07-28 MCP spec freeze in ~8 weeks** — this gateway tracks the 2025-03-26 spec. Migration plan: see [LISTING.md § MCP Spec Freeze](./LISTING.md#-mcp-2026-07-28-spec-freeze-8-weeks).

MIT-licensed. MEOK AI Labs (CSOAI LTD, UK CH 16939677).
