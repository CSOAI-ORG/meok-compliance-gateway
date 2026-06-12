# Show HN: A stateless MCP-to-streamable-HTTP gateway with x402 paywall, deployed for 28 production hives

**TL;DR**: We built a production-ready streamable-HTTP gateway (`meok-compliance-gateway`) that wraps any MEOK FastMCP server for AWS Bedrock AgentCore, Google Cloud Run, Azure, Smithery, and x402 monetization. It includes a built-in x402 paywall (OFF by default), RFC 9728 OAuth metadata, health checks, and an AgentAudit compliance layer (14-expert OpenScore, BFT consensus, Signet receipts, tamper-evident audit trails). 4 flagship compliance MCPs (EU AI Act, DORA, NIS2, CRA) + 24 vertical hives deployed via 28-hive mesh architecture.

---

## The Problem

The Model Context Protocol (MCP) spec (2025-03-26) uses stdio transport — great for local dev, unusable for cloud marketplaces. AWS Bedrock AgentCore, Google Cloud Run, Azure AI Foundry, and Smithery all require **streamable-HTTP** at `/mcp`.

Meanwhile, **monetization is broken**: Stripe subscriptions don't work for agent-to-agent calls. Autonomous agents need per-call, USDC-settled micropayments — enter **x402** (Coinbase).

No existing solution combines:
1. Stateless streamable-HTTP transport (cloud-ready)
2. Correct x402-over-MCP semantics (payment in `_meta["x402/payment"]`)
3. Regulatory compliance baked in (EU AI Act, DORA, NIS2, CRA)
4. Audit-grade agent cards (OpenScore 14-expert, BFT, Signet receipts)

---

## The Solution: `meok-compliance-gateway`

### 1. Streamable-HTTP Gateway (`http_server.py`)

```python
# Serves ANY MEOK FastMCP server over /mcp on 0.0.0.0:$PORT
import os
import server
from mcp.server.transport_security import TransportSecuritySettings

mcp = server.mcp
mcp.settings.host = "0.0.0.0"
mcp.settings.port = int(os.environ.get("PORT", "8000"))
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,  # platform controls ingress
)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

**Verified**: `POST /mcp` with `initialize` → **HTTP 200**.

**Cloud deployments** (one command each):
```bash
# Google Cloud Run (Path A — from source)
gcloud run deploy eu-ai-act-mcp --source . --port 8000 --allow-unauthenticated --region europe-west2

# AWS Bedrock AgentCore (Path B — prebuilt GHCR image)
gcloud run deploy eu-ai-act-mcp --image ghcr.io/csoai-org/eu-ai-act-mcp:latest --port 8000 --allow-unauthenticated
```

### 2. x402 Paywall (OFF by default)

```python
# Correct MCP-over-x402: payment in _meta["x402/payment"], challenge via ToolError
from meok_x402 import paywalled

@mcp.tool()
@paywalled(price="$0.10")  # COST WARNING in description (AWS convention)
def audit_report(system: str, ctx: Context) -> dict:
    ...
```

**Key design decisions**:
- **Opt-in only**: `X402_ENABLED=1` + `X402_PAY_TO=0xYourWallet` activates it. Default: transparent passthrough (free self-host unaffected).
- **Payment in MCP meta**: `_meta["x402/payment"]` — NOT HTTP 402 (MCP clients can't read it).
- **Fail-open**: facilitator outage never blocks paying customers.
- **Settle best-effort**: verification gates the call; settlement is async + logged.

### 3. AgentAudit Compliance Layer (28-hive mesh)

Every hive in the 28-hive mesh can import AgentAudit for:

| Component | What it does |
|-----------|--------------|
| **OpenScore** | 14 safety experts score A2A Agent Cards 0.0–1.0 (EU AI Act, NIST RMF, DORA, NIS2, CRA, neurorights, x402, MCP attestation, blockchain, HITL, red/blue team, continuous monitoring, fuzzing, autonomous audit, web extraction) |
| **BFT Consensus** | 2f+1 Byzantine Fault Tolerant rounds on audit entries; quorum certificates |
| **Signet Receipts** | Ed25519 (or HMAC-SHA256 fallback) signed receipts per entry; bilateral co-signing |
| **Audit Trails** | Hash-chained (Merkle-style), blockchain-anchorable, exportable with integrity verification |
| **Shadow Scanner** | Probes `/.well-known/agent-card.json` for unregistered agents in your estate |

```python
from agentaudit.openscore import openscore
from agentaudit.audit_trail import AuditTrail, AuditEntry
from agentaudit.signet import SignetKey, sign_entry
from agentaudit.bft import BFTConsensus

# Score an agent with audit-trail integrity + BFT consensus
score = openscore(agent_id, card, audit=trail, bft=bft)
# score.overall: 0.0–1.0, score.by_regulation, score.by_expert, score.missing_checks
```

### 4. 28-Hive Mesh Architecture

Each `.ai` domain runs an autonomous 7-layer hive:

```
L7  PRESENTATION    Open Design (Vercel/Cloudflare Pages)
L6  ORCHESTRATION   Hermes sub-context (Kimi K2.6 / DeepSeek V3.5 / local)
L5  DOMAIN MCP      FastMCP + streamable-HTTP + x402
L4  AGENT MEMORY    agentmemory (95.2% R@5 LongMemEval-S)
L3  KNOWLEDGE GRAPH Cognee subgraph (Neo4j streams gossip)
L2  VERSIONED HIST  Memoria (Git-for-memory, namespace per hive)
L1  DRIFT DETECTION mex (fail on score < 90, CI gate)
```

**Peer-to-peer via A2A** — no central brain. 25 customer hives + 3 infra hives = 28.

**Flagships**: `meok.ai` (compliance portal), `csoai.org` (governance FAA-for-AI), `proofof.ai` (attestations), `cobolbridge.ai` (COBOL→modern for banks)

**Governance bundle (9)**: accountabilityof, agisafe, asisecurity, biasdetectionof, dataprivacyof, ethicalgovernanceof, safetyof, transparencyof, councilof

**Verticals**: UK construction (4), legal (1), aquatics (2), flip candidates (5), infra (3)

---

## Two Orthogonal Pricing Axes

| | x402 micro-call | SaaS subscription |
|---|---|---|
| **Use case** | Agent-to-agent, pay-per-call | Human dashboard, many seats |
| **Pricing unit** | $0.01–$10.00/call | $29–$49/user/mo, custom $50–200K/yr |
| **Payment rail** | x402 / Coinbase CDP | Stripe |
| **Examples** | "Run bias check once" | "Compliance dashboard for 50 risk officers" |

**4 SaaS tiers**: Freemium ($0), Team ($29), Business ($49), Enterprise (custom)

**10–20x undercut** vs Vanta/Drata/OneTrust at enterprise tier; **1000–10000x** for low-volume agent calls.

---

## EU AI Act: The Forcing Function

**August 2, 2026** — enforcement begins. **78% of enterprises unprepared** (IBM/McKinsey 2025).

Our turnkey package maps directly:
- **Article 10** (bias) → `biasdetectionof.ai` ($0.10/call or $299/mo)
- **Article 12** (incidents) → `accountabilityof.ai` ($0.50/call)
- **Article 13** (transparency) → `transparencyof.ai` ($0.75/call)
- **Article 30** (records) → `dataprivacyof.ai` ($0.20/call)
- **Certification** → `councilof.ai` Watchdog AI Safety Certification ($1.00/call)

---

## Open Source & Verifiable

- **MIT licensed** — all 28 hives, gateway, AgentAudit
- **447 public repos** in CSOAI-ORG (every framework, MCP, integration auditable)
- **OpenSSF Scorecard 7.0+** fleet mean (52/52 verifiers passing)
- **SBOM** (CycloneDX 1.6 + SPDX 2.3) per flagship
- **Sigstore cosign** keyless image signing on GHCR

---

## What's Next (MCP 2026-07-28 Spec Freeze)

The MCP spec freezes **July 28, 2026** (~8 weeks). New spec drops `initialize`/`initialized` handshake, requires `Mcp-Method` + `Mcp-Name` + `MCP-Protocol-Version` headers.

**Our migration target**: re-push GHCR images by **July 14, 2026** (2-week buffer). Tracked in issue #1.

---

## Links

- **Gateway repo**: `github.com/CSOAI-ORG/meok-compliance-gateway`
- **AgentAudit**: `github.com/CSOAI-ORG/agentaudit` (on `feat/agentaudit-server`)
- **28 hive configs**: `github.com/CSOAI-ORG/*-hive` (auto-generated via `gen-hive.py` + `gen-geo.py`)
- **Deploy playbook**: `LISTING.md` (Cloud Run, AWS, Smithery, x402 wrap)
- **Pricing**: `PRICING.md` (two SKUs, 4 tiers, 28-hive table)
- **RFC**: `MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` (10 domains, 4 levels, crosswalk matrix)

---

## Ask HN

1. **x402-over-MCP**: Is the `_meta["x402/payment"]` convention the right long-term pattern, or should MCP native a payment field?
2. **Stateless vs stateful**: We disabled DNS-rebinding protection because the platform terminates TLS. Is there a cleaner pattern for Cloud Run / AgentCore?
3. **BFT for governance**: `councilof.ai` runs multi-agent BFT deliberation for certification decisions. Has anyone seen production BFT in agent orchestration?
4. **Compliance as code**: 410 verbatim EU AI Act articles ingested as parseable source. Who else is doing regulation-as-structured-data?

---

*Built by MEOK AI Labs (CSOAI LTD, UK CH 16939677). MIT licensed. Co-authored by the 28-hive mesh.*