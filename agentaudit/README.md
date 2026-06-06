# AgentAudit — A2A Compliance & Audit Proxy

> **Status:** Alpha — interfaces may change until v1.0.  
> **Empire Alignment:** OpenMoE-BFT Empire Layer 3 (OpenScore Safety Experts), Layer 8 (Compliance Gateway), Layer 9 (Audit & Receipts), Layer 10 (x402 Paywall), Layer 11 (A2A + MCP Interop).

AgentAudit is the regulatory-compliance conscience layer for AI-agent protocols. It maps the **EU AI Act**, **DORA**, **NIS2**, and **CRA** onto A2A Agent Card fields, maintains **tamper-evident audit trails** with **Signet Ed25519 signing**, scores agents via the **OpenScore 14-expert algorithm**, and can shadow-scan estates for unregistered agents.

## Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run the MCP server (stdio)
python -m agentaudit.server

# 3. Or run the streamable-HTTP gateway
python http_server.py        # listens on 0.0.0.0:8000
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
| `score_agent` | Free | OpenScore an A2A Agent Card (14 experts + optional BFT). |
| `create_audit_trail` | Free | Init a Signet-signed, hash-chained audit log. |
| `append_audit_event` | Free | Log an interaction with optional BFT + blockchain anchor. |
| `verify_audit_trail` | Free | Verify chain integrity + Signet signatures. |
| `dump_audit_trail` | Free | Export trail as JSON. |
| `generate_signet_receipt` | Free | Create a standalone Ed25519 receipt for any hash. |
| `cast_bft_vote` | Free | Vote in a 2f+1 BFT consensus round. |
| `get_bft_status` | Free | Query BFT consensus state. |
| `register_expert` | Free | Register an MCP server as a safety expert candidate. |
| `scan_shadow_agents` | **$0.10** | Probe URLs for rogue A2A agents. |

*Paid tools require `X402_ENABLED=1` and a valid `_meta["x402/payment"]` token.*

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
| `X402_ENABLED` | `0` | Enable x402 paywall |
| `X402_PAY_TO` | — | EVM settlement address |
| `X402_PRICE` | `$0.10` | Default tool price |
| `SIGNET_SEED` | — | Ed25519 signing key seed (hex) |
| `SIGNET_DID` | `did:web:agentaudit.meok.ai` | Signet signer DID |

## License

MIT — see top-level `LICENSE`.
