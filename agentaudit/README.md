# AgentAudit — A2A Compliance & Audit Proxy

> **Status:** Alpha — interfaces may change until v1.0.

AgentAudit is a regulatory-compliance layer for AI-agent protocols. It maps the
**EU AI Act**, **DORA**, **NIS2**, and **CRA** onto A2A Agent Card fields,
exposes trust-scoring tools, maintains tamper-evident audit trails, and can
shadow-scan estates for unregistered agents.

## Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Run the MCP server (stdio)
python -m agentaudit.server

# 3. Or run the streamable-HTTP gateway
python http_server.py        # listens on 0.0.0.0:8000
```

## MCP Tools

| Tool | Cost | Description |
|------|------|-------------|
| `get_compliance_matrix` | Free | List all regulation checks. |
| `score_agent` | Free | Score an A2A Agent Card against the matrix. |
| `create_audit_trail` | Free | Initialise a tamper-evident audit chain. |
| `append_audit_event` | Free | Log an interaction to a trail. |
| `verify_audit_trail` | Free | Verify chain integrity. |
| `dump_audit_trail` | Free | Export a trail as JSON. |
| `scan_shadow_agents` | **$0.10** | Probe URLs for rogue A2A agents. |

*Paid tools require `X402_ENABLED=1` and a valid `_meta["x402/payment"]` token.*

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  A2A Agent Card │────▶│  AgentAudit MCP  │────▶│  Trust Score    │
│  (agent.json)   │     │  compliance_matrix│     │  (0.0 – 1.0)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  AuditTrail      │
                       │  (hash-chained)  │
                       └──────────────────┘
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

## License

MIT — see top-level `LICENSE`.
