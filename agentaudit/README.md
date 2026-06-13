# AgentAudit — A2A Compliance & Audit Proxy

> **Status:** Alpha — interfaces may change until v1.0.  
> **Empire Alignment:** OpenMoE-BFT Empire Layer 3 (OpenScore Safety Experts), Layer 8 (Compliance Gateway), Layer 9 (Audit & Receipts), Layer 10 (x402 Paywall), Layer 11 (A2A + MCP Interop).

AgentAudit is the regulatory-compliance conscience layer for AI-agent protocols. It maps the **EU AI Act**, **DORA**, **NIS2**, and **CRA** onto A2A Agent Card fields, maintains **tamper-evident audit trails** with **Signet Ed25519 signing**, scores agents via the **OpenScore 14-expert algorithm**, and can shadow-scan estates for unregistered agents.

## Quick Start

```bash
# 1. Install (free / MIT)
pip install -r requirements.txt

# 2. Run the MCP server (stdio)
python -m agentaudit.server

# 3. Or run the streamable-HTTP gateway
python http_server.py        # listens on 0.0.0.0:8000

# 4. Opt in to per-call monetization (priced tools)
pip install 'agentaudit[x402]'
X402_ENABLED=1 X402_PAY_TO=0xYourBaseWallet python -m agentaudit.server

# 5. Dev / fuzz install (hypothesis property tests)
pip install 'agentaudit[dev]'    # includes hypothesis
python -m pytest agentaudit/tests/ agentaudit/fuzz/ -v
```

## OpenScore Safety Experts (14)

| # | Expert | Domain | Source Repo |
|---|--------|--------|-------------|
| 1 | EU AI Act Compliance | Compliance | AIR Blackbox |
| 2 | NIST RMF Risk Scoring | Compliance | DeepTeam |
| 3 | DORA / NIS2 Incident Taxonomy | Compliance | DORA ROI Validator |
| 4 | Neurorights (GDPR Art 9) | Governance | Custom |
| 5 | x402 Payment Validation | Monetization | AgentMint + Signet |
| 6 | MCP Tool Attestation | Security | Agent Security Harness |
| 7 | Blockchain Verification | Verification | liboqs |
| 8 | Human-in-the-Loop Gate | Governance | LangGraph Approval Hub |
| 9 | Red Team Automation | Security | RedAmon + PyRIT |
| 10 | Blue Team Defense | Security | Agent Security Harness |
| 11 | Continuous Monitoring | Security | DeepTeam |
| 12 | Fuzzing / Mutation | Security | FuzzyAI |
| 13 | Autonomous Auditor | Verification | UI-TARS Desktop |
| 14 | Web Crawler / Extractor | Verification | Firecrawl |

## MCP Tools

| Tool | Cost | Description |
|------|------|-------------|
| `get_safety_experts` | Free | List all 14 OpenScore experts. |
| `get_compliance_matrix` | Free | List regulation checks with expert mapping. |
| `score_agent` | **$0.10** | OpenScore an A2A Agent Card (14 experts + optional BFT). |
| `create_audit_trail` | Free | Init a Signet-signed, hash-chained audit log. |
| `append_audit_event` | Free | Log an interaction with optional BFT + blockchain anchor. |
| `verify_audit_trail` | Free | Verify chain integrity + Signet signatures. |
| `dump_audit_trail` | Free | Export trail as JSON. |
| `generate_signet_receipt` | **$0.05** | Create a standalone Ed25519 receipt for any hash. |
| `cast_bft_vote` | Free | Vote in a 2f+1 BFT consensus round. |
| `get_bft_status` | Free | Query BFT consensus state. |
| `register_expert` | Free | Register an MCP server as a safety expert candidate. |
| `scan_shadow_agents` | **$0.10** | Probe URLs for rogue A2A agents. |
| `compliance_gap_analyser` | **$0.25** | Run the EU/DORA/NIS2/CRA matrix against a partial card; return a remediation list. |
| `finalize_bft_round` | **$0.50** | Tally a BFT round + mint a Signet receipt for the majority hash (consensus-as-a-service). |
| `expert_quorum_consult` | **$1.00** | Fan out across N experts, return a Signet-receipted digest. |
| `audit_trail_export_anchored` | **$0.20** | Export a trail with a `sha256:` CID-format anchor + Signet receipt. |
| `threat_intel_lookup` | **$0.15** | Deterministic threat-intel score for an IoC (placeholder feed; swap for OTX/GreyNoise). |
| `x402_spending_report` | Free | Rolling log of verified paid calls + per-tool counts (cross-check vs your facilitator dashboard). |

*Paid tools require `X402_ENABLED=1` and a valid `_meta["x402/payment"]` token. They are **off by default** — free self-host and existing builds are unaffected.*

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AgentAudit MCP Server                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ OpenScore   │  │ Signet      │  │ BFT         │         │
│  │ (14 experts)│  │ Ed25519     │  │ 2f+1        │         │
│  │ Algorithm   │  │ Receipts    │  │ Consensus   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                          │                                   │
│                   ┌──────┴──────┐                           │
│                   │ AuditTrail  │                           │
│                   │ Hash chain  │                           │
│                   └──────┬──────┘                           │
│                          │                                   │
│  ┌─────────────┐  ┌──────┴──────┐  ┌─────────────┐         │
│  │ Compliance  │  │ x402        │  │ Shadow      │         │
│  │ Matrix      │  │ Paywall     │  │ Scanner     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Docker

```bash
docker build -t agentaudit .
docker run -p 8000:8000 agentaudit
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | HTTP listener port |
| `SIGNET_SEED` | — | Ed25519 signing key seed (hex) |
| `SIGNET_DID` | `did:web:agentaudit.meok.ai` | Signet signer DID |
| `X402_ENABLED` | `0` | Enable x402 paywall on the priced tools below. **Off by default** — free self-host is unaffected. |
| `X402_PAY_TO` | — | EVM settlement address (Coinbase CDP receiving wallet) |
| `X402_NETWORK` | `eip155:8453` | Base mainnet (`eip155:84532` for Base Sepolia) |
| `X402_PRICE` | `$0.10` | Default tool price (per-tool overrides win) |
| `X402_ASSET` | USDC for network | Token contract; defaults to canonical USDC for the network |
| `X402_FACILITATOR_URL` | `https://x402.org/facilitator` | Override the x402 facilitator endpoint |
| `X402_TIMEOUT` | `300` | Payment-required timeout (seconds) |

## Per-call monetization (x402)

Eight tools are priced for autonomous-agent callers:

| Tool | Price | Use it for |
|------|-------|-----------|
| `generate_signet_receipt` | $0.05 | Issue a tamper-evident Ed25519 receipt for any hash |
| `score_agent` | $0.10 | OpenScore an A2A Agent Card against the 14-expert algorithm + optional BFT |
| `scan_shadow_agents` | $0.10 | Discover rogue A2A agents on candidate URLs |
| `threat_intel_lookup` | $0.15 | Score an IoC (deterministic placeholder; swap for OTX/GreyNoise) |
| `audit_trail_export_anchored` | $0.20 | Export a trail with a `sha256:` CID-format anchor + receipt |
| `compliance_gap_analyser` | $0.25 | Run the EU/DORA/NIS2/CRA matrix; get a remediation list |
| `finalize_bft_round` | $0.50 | Tally a BFT round and mint a Signet attestation |
| `expert_quorum_consult` | $1.00 | Fan out across N experts; Signet-receipted consensus digest |

All other tools are free and stay free. Payment travels in MCP request `_meta["x402/payment"]`
(spec-correct x402-over-MCP, **not** HTTP 402 — MCP clients can't read HTTP status).
The challenge comes back as a `ToolError` whose JSON text contains the
`x402/payment-response` envelope with `accepts[0].amount` in atomic USDC (6dp).

Use `x402_spending_report` (free) to audit your call volume — cross-check the
truncated payer addresses against your facilitator dashboard.

## License

MIT — see top-level `LICENSE`.
