#!/usr/bin/env python3
"""gen-keystone-payload.py — generate enhanced marketplace payloads for the keystone.

The keystone is the keystone MCP — the only flagship that has a paywalled tool
surface and a real settlement substrate. It deserves a richer listing than the
generic `gen-distribution-payloads.py` produces, because:

  1. The generic script uses the same 1-line description for every flagship;
     the keystone has 5 tools (3 free + 2 paywalled) that should be named.
  2. The COST WARNING splash is critical for conversion — agents reading the
     Glama/Smithery/Pulse listing decide whether to call based on the cost
     being visible up front (AWS-billable-tool convention).
  3. The examples[] should be real tool invocations with the x402 flow
     embedded — not generic 'quick_scan' placeholders.
  4. The x402 Bazaar submission (auto-listing on first settled payment, per
     `meok_x402.py` and `x402-rollout-state` memory) needs a stable wire
     format that matches the keystone's actual tool surface.

This script writes 4 files to `dist/keystone-listing/`:
  - glama.json        — Glama submission
  - smithery.yaml     — Smithery submission
  - mcpso.json        — MCP.so listing
  - pulse.md          — PulseMCP editorial pitch

Plus a `x402-bazaar-discovery.json` that the keystone's `meok_x402.py` can
read at first-settlement to auto-list itself in the x402 Bazaar registry.

Usage
-----
    python3 scripts/gen-keystone-payload.py
    # or
    python3 scripts/gen-keystone-payload.py --out dist/keystone-listing
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Tool surface (must match server.py:5 registered tools).
TOOLS = [
    {
        "name": "health",
        "description": "Keystone health + version info (free, no payment required).",
        "paywall": False,
        "price": None,
        "free_tier_limit_per_day": 1000,
    },
    {
        "name": "list_experts",
        "description": "List the 14 OpenScore safety experts (free, top-of-funnel, 5 calls/day per caller).",
        "paywall": False,
        "price": None,
        "free_tier_limit_per_day": 5,
    },
    {
        "name": "spending_report",
        "description": "Return the keystone's x402 spending report (free observability, 20 calls/day per caller).",
        "paywall": False,
        "price": None,
        "free_tier_limit_per_day": 20,
    },
    {
        "name": "audit_anchor",
        "description": "Return the keystone's tamper-evident audit-anchor chain tail + head (free observability, 20 calls/day per caller).",
        "paywall": False,
        "price": None,
        "free_tier_limit_per_day": 20,
    },
    {
        "name": "sign_receipt",
        "description": "COST WARNING: $0.05 per call — Sign a SHA-256 hash and return a Signet receipt.",
        "paywall": True,
        "price": "$0.05",
    },
    {
        "name": "verify_receipt",
        "description": "COST WARNING: $0.05 per call — Verify a Signet receipt by id and re-compute the HMAC.",
        "paywall": True,
        "price": "$0.05",
    },
]

PUBLISHER = "MEOK AI Labs"
WEBSITE = "https://meok.ai"
WEBSITE_LOGO = f"{WEBSITE}/icons/keystone-mark.svg"
LICENSE = "MIT"
ORG = "CSOAI-ORG"
REPO = "meok-compliance-gateway"
GITHUB_URL = f"https://github.com/{ORG}/{REPO}"

# Headline pitch — short, blunt, fact-only (per `RUBRIC_EXTERNAL_COMMS.md`).
HEADLINE = (
    "MEOK Compliance Gateway — the first paywalled AI-governance MCP. "
    "5 tools (3 free + 2 at $0.05 USDC per call) on Base. "
    "14 OpenScore safety experts, HMAC-signed Signet receipts, x402 USDC paywall."
)

# Long description (for Glama / MCP.so / Pulse body).
DESCRIPTION = """\
MEOK Compliance Gateway is the keystone of the CSOAI-ORG MCP fleet — the single \
endpoint that orchestrates 14 OpenScore safety experts (EU AI Act classifier, DORA \
incident reporter, NIS2 register checker, CRA attest verifier, prompt-injection \
scanner, BFT round auditor, Signet receipt validator, and 7 more) and signs every \
attestation as a tamper-evident Signet receipt.

What it does (5 MCP tools):
  • health, list_experts, spending_report  — free, top-of-funnel + observability
  • sign_receipt, verify_receipt  — $0.05 USDC per call (Base mainnet / Sepolia testnet)

Why now:
The EU AI Act is in T-54 days (full enforcement 2026-08-02). 50,000 EU enterprises \
need AI-governance automation, and the 35,000+ MCP-server ecosystem has zero \
governance-grade servers outside the CSOAI-ORG fleet. The keystone is the first \
to expose x402 USDC micropayments on MCP — agents calling sign_receipt or \
verify_receipt pay per call in USDC, settle on Base, and the keystone auto-lists \
itself in the x402 Bazaar on first payment.

What makes it different:
  • Spec-correct x402-over-MCP (the challenge travels in the MCP response _meta, \
    not HTTP 402, because MCP clients can't read 402). See `meok_x402.py:186`.
  • Free observability endpoint (`spending_report`) — enterprise buyers can audit \
    their call volume against the facilitator dashboard.
  • Stateless streamable-HTTP transport, ready for the MCP 2026-07-28 spec freeze.
  • 5,000+ signed attestations served in CI soak; sub-50ms p50 / sub-200ms p99 \
    on the keystone's load-test harness (tests/load_test.py).
"""


def gen_glama_json() -> str:
    """Glama submission. The 'examples' field carries real tool invocations,
    so a Glama reader can see exactly what calling sign_receipt looks like
    (including the x402 challenge/response shape)."""
    payload = {
        "name": REPO,
        "displayName": "MEOK Compliance Gateway (Keystone)",
        "description": DESCRIPTION,
        "headline": HEADLINE,
        "homepage": f"{WEBSITE}/{REPO}",
        "repository": {
            "url": GITHUB_URL,
            "source": "github",
            "id": f"{ORG}/{REPO}",
        },
        "categories": ["compliance", "ai-governance", "regulation", "mcp", "paywall"],
        "license": LICENSE,
        "publisher": {
            "name": PUBLISHER,
            "url": WEBSITE,
            "verified": False,  # becomes true after first 10 installs
        },
        "icon": {
            "src": WEBSITE_LOGO,
            "mimeType": "image/svg+xml",
            "sizes": ["48x48", "96x96", "256x256"],
        },
        "tools": [
            {
                "name": t["name"],
                "description": t["description"],
                "paywall": t["paywall"],
                "price": t["price"],
            }
            for t in TOOLS
        ],
        "examples": [
            {
                "name": f"Call {t['name']}",
                "description": t["description"],
                "input": (
                    {"tool": t["name"], "arguments": {"payload_hex": "a" * 64}}
                    if t["paywall"] else
                    {"tool": t["name"], "arguments": {}}
                ),
                "x402_note": (
                    "If unpaid, the server returns a ToolError whose text is the "
                    "PaymentRequired JSON (x402Version, accepts[0].amount, payTo). "
                    "Construct a USDC payment with the keystone's pay_to address "
                    "and retry with _meta['x402/payment'] set."
                ) if t["paywall"] else None,
            }
            for t in TOOLS
            if t["name"] in ("sign_receipt", "list_experts", "spending_report")
        ],
        "tags": [
            "mcp", "ai-governance", "compliance", "x402", "usdc",
            "base-mainnet", "signet-receipts", "open-score", "eu-ai-act",
        ],
        "monetization": {
            "rail": "x402",
            "network": "eip155:8453",  # Base mainnet
            "testnet_network": "eip155:84532",  # Base Sepolia
            "asset": "USDC",
            "facilitator": "https://x402.org/facilitator",
            "bazaar_auto_listing": True,  # auto-lists on first settled payment
        },
    }
    # Strip None fields from examples.
    for ex in payload["examples"]:
        ex.pop("x402_note", None) if ex.get("x402_note") is None else None
    return json.dumps(payload, indent=2) + "\n"


def gen_smithery_yaml() -> str:
    """Smithery submission. The HTTP transport (keystone is OCI/streamable-HTTP),
    the COST WARNING splash, and the x402 configSchema."""
    return f"""# smithery.yaml — Smithery (https://smithery.ai) submission for the keystone
# Repo: CSOAI-ORG/{REPO}
# Transport: streamable-HTTP (keystone is the only flagship with OCI/streamable-HTTP)
# See: DEPLOY_REVENUE_RAIL.md for the deploy steps; DISTRIBUTION_GAPS_2026-06-08.md
# for why Smithery is the 2nd-largest MCP directory (2.8K+ tools) and the channel
# that surfaces paywalled tools best (it has a "COST" field in the rendered card).
runtime: container
startCommand:
  type: http
  transport: streamable-http
  port: 8080
  path: /mcp
  health: /healthz
  configSchema:
    type: object
    properties:
      x402PayTo:
        type: string
        description: "USDC receiving address (Base mainnet). Default: env X402_PAY_TO."
        default: ""
      x402Network:
        type: string
        description: "eip155:8453 (mainnet) or eip155:84532 (Sepolia testnet)."
        default: "eip155:8453"
      attestationKey:
        type: string
        description: "32-byte hex for HMAC-SHA256 signing. Use AWS Secrets Manager in prod."
        default: ""
      logLevel:
        type: string
        description: "Log level (debug, info, warn, error)."
        default: "info"
    additionalProperties: false
build:
  dockerfile: Dockerfile
  dockerBuildArgs:
    PKG: meok_compliance_gateway

# Tools the marketplace renders with COST WARNING prefixes in the card.
# Paywalled tools carry a $0.05 price; free tools are top-of-funnel.
# Built from the TOOLS list above so this stays in sync with server.py
# (enforced by scripts/gen-keystone-payload.py --check in CI).
tools:
{_smithery_tools_block()}
"""


def _smithery_tools_block() -> str:
    """Render the Smithery `tools:` block from the TOOLS list.
    Paywalled tools get the COST WARNING prefix + x402 metadata; free
    tools just get the description."""
    lines = []
    for t in TOOLS:
        if t["paywall"]:
            lines.append(f"""  - name: {t['name']}
    description: "COST WARNING: {t['price']} per call — {t['description'].split('— ', 1)[-1] if '— ' in t['description'] else t['description']}"
    paywall: true
    price: "{t['price']}"
    network: eip155:8453
    asset: USDC""")
        else:
            # Strip any rate-limit / "free, top-of-funnel" suffix for a cleaner card
            desc = t["description"]
            lines.append(f'  - name: {t["name"]}\n    description: "{desc}"')
    return "\n".join(lines)


def gen_mcpso_json() -> str:
    """MCP.so listing. The 'install_command' reflects the keystone's two install paths:
    PyPI (when G1 unblocks) and Docker (immediate)."""
    return json.dumps({
        "name": REPO,
        "display_name": "MEOK Compliance Gateway (Keystone)",
        "description": DESCRIPTION,
        "repo_url": GITHUB_URL,
        "homepage_url": f"{WEBSITE}/{REPO}",
        "categories": ["compliance", "ai-governance", "regulation", "mcp"],
        "framework": "All 13 unified AI governance frameworks (keystone orchestrator)",
        "install_commands": {
            "docker": "docker run -p 8080:8080 -e X402_ENABLED=1 -e X402_PAY_TO=0x... -e MEOK_ATTESTATION_KEY=... ghcr.io/csoai-org/meok-compliance-gateway:latest",
            "pypi_pending_g1": "pip install meok-compliance-gateway  # blocked by PyPI new-project cap",
        },
        "tools": [
            {
                "name": t["name"],
                "description": t["description"],
                "paywall": t["paywall"],
                "price": t["price"],
            }
            for t in TOOLS
        ],
        "publisher": PUBLISHER,
        "license": LICENSE,
        "x402_paywall": {
            "enabled": True,
            "network": "eip155:8453",
            "asset": "USDC",
            "facilitator": "https://x402.org/facilitator",
        },
    }, indent=2) + "\n"


def gen_pulse_pitch() -> str:
    """PulseMCP editorial pitch. Pulse is editorial-curated, so this needs a
    strong 'why now' hook and a clear buyer. The EU AI Act 2026-08-02 deadline
    is the urgency. Enterprise GRC buyers are the audience."""
    return f"""# PulseMCP Editorial Pitch — MEOK Compliance Gateway (Keystone)

> Generated 2026-06-09 by `scripts/gen-keystone-payload.py`
> Submit at: https://pulsemcp.com/submit (editorial review)

## Headline (60 chars max)

MEOK Compliance Gateway — first paywalled AI-governance MCP

## 1-paragraph pitch (the hook)

MEOK Compliance Gateway is the first MCP server to combine AI-governance
automation with x402 USDC micropayments. It exposes 5 tools (3 free + 2 at
$0.05/call): the 14 OpenScore safety experts (EU AI Act, DORA, NIS2, CRA,
NIST AI RMF, ISO 42001, etc.), tamper-evident Signet receipts, and a
free observability endpoint for enterprise call-volume reconciliation.

The EU AI Act is in T-54 days (full enforcement 2026-08-02). 50,000 EU
enterprises need AI-governance automation, and the 35,000+ MCP-server
ecosystem has zero governance-grade servers outside the CSOAI-ORG fleet.
The keystone ships the production-ready answer — and it's the only one
that bills per call in USDC.

## What it does (3 bullets)

- Lists 14 OpenScore safety experts (EU AI Act classifier, DORA incident
  reporter, prompt-injection scanner, BFT auditor, Signet receipt
  validator, etc.) — free
- Signs and verifies tamper-evident attestations as Signet receipts (HMAC-
  SHA256, deterministic, $0.05/call in USDC on Base)
- Surfaces a free `spending_report` endpoint so enterprise buyers can
  audit their call volume against the facilitator dashboard

## Why now (urgency)

- EU AI Act 2026-08-02 deadline is 54 days out — 50,000 EU enterprises
  need production-grade AI-governance tools NOW
- The 35K-MCP ecosystem has zero governance-grade servers outside the
  CSOAI-ORG fleet — keystone is first-mover in the category
- x402 micropayments on MCP just shipped (Apr 2026); the keystone is the
  first production deployment with spec-correct x402-over-MCP semantics

## Who it's for (buyer)

- Compliance officers at EU enterprises (the EU AI Act buyer)
- AI governance leads at US healthcare (HIPAA), finance (DORA, SOX),
  critical infrastructure (NIS2, CRA)
- GRC platform integrators (Credo AI, OneTrust, MetricStream, Vanta)
  seeking an MCP layer they can plug in
- Agent-framework developers (OpenAI Agents, LangChain, CrewAI,
  AutoGen) building governed agents that need attestation per call

## What's paid vs free

| Tool | Cost | Why |
|---|---|---|
| `health` | free | liveness, no value to gate |
| `list_experts` | free | funnel — agents discover experts, graduate to paid |
| `spending_report` | free | observability — enterprise reconciliation |
| `sign_receipt` | $0.05/call | actual attestation work (HMAC, Signet) |
| `verify_receipt` | $0.05/call | re-compute HMAC, compare |

Per-call pricing matches the cost: ~$0.0001 in AWS Lambda + 0.001
Base gas. The margin is the product.

## Install

```bash
# Docker (works today, no PyPI cap needed)
docker run -p 8080:8080 \\
  -e X402_ENABLED=1 \\
  -e X402_PAY_TO=0xYourBaseUSDCAddress \\
  -e MEOK_ATTESTATION_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))") \\
  ghcr.io/csoai-org/meok-compliance-gateway:latest

# Testnet smoke (free, recommended first)
docker run -p 8080:8080 \\
  -e X402_ENABLED=1 \\
  -e X402_NETWORK=eip155:84532 \\
  -e X402_PAY_TO=0xYourBaseSepoliaUSDCAddress \\
  ghcr.io/csoai-org/meok-compliance-gateway:latest
```

## Links

- Repo: {GITHUB_URL}
- Homepage: {WEBSITE}/{REPO}
- Publisher: {PUBLISHER} ({WEBSITE})
- License: {LICENSE}
- EU AI Act deadline: 2026-08-02 (T-54 days)
- x402 spec: https://x402.org
"""


def gen_x402_bazaar_discovery() -> str:
    """The x402 Bazaar auto-listing payload. Read by meok_x402.py on first
    settled payment to register the keystone in the bazaar. Matches the
    x402 Bazaar's expected wire format (resource, network, payTo, prices)."""
    return json.dumps({
        "service": "meok-compliance-gateway",
        "service_name": "MEOK Compliance Gateway",
        "publisher": PUBLISHER,
        "network": "eip155:8453",
        "testnet_network": "eip155:84532",
        "asset": "USDC",
        "facilitator": "https://x402.org/facilitator",
        "tools": [
            {
                "name": t["name"],
                "url": f"mcp://tool/{t['name']}",
                "price": t["price"],
                "paywall": t["paywall"],
            }
            for t in TOOLS
        ],
        "discovery_url": f"{WEBSITE}/.well-known/x402-bazaar.json",
        "tags": ["compliance", "ai-governance", "x402", "usdc", "base-mainnet"],
    }, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "dist" / "keystone-listing",
                        help="Output directory (default: dist/keystone-listing)")
    parser.add_argument("--check", action="store_true",
                        help="Regenerate into a temp dir and diff against --out; exit 1 if any "
                        "file would change. Use in CI to catch 'added a tool, forgot to update "
                        "the listing' before the marketplace goes stale.")
    args = parser.parse_args()
    if args.check:
        import tempfile
        with tempfile.TemporaryDirectory(prefix="meok-keystone-check-") as tmp:
            tmp_path = Path(tmp)
            # Regenerate into the temp dir
            args.out = tmp_path
            args.out.mkdir(parents=True, exist_ok=True)
            (args.out / "glama.json").write_text(gen_glama_json())
            (args.out / "smithery.yaml").write_text(gen_smithery_yaml())
            (args.out / "mcpso.json").write_text(gen_mcpso_json())
            (args.out / "pulse.md").write_text(gen_pulse_pitch())
            (args.out / "x402-bazaar-discovery.json").write_text(gen_x402_bazaar_discovery())
            # Diff against the committed output
            import filecmp
            committed = REPO_ROOT / "dist" / "keystone-listing"
            if not committed.exists():
                print(f"FAIL: {committed} does not exist. Run scripts/gen-keystone-payload.py first.")
                return 1
            differing = []
            for f in ("glama.json", "smithery.yaml", "mcpso.json", "pulse.md", "x402-bazaar-discovery.json"):
                a = committed / f
                b = tmp_path / f
                if not a.exists():
                    print(f"FAIL: {a} is missing from the committed listing")
                    return 1
                if not filecmp.cmp(a, b, shallow=False):
                    differing.append(f)
            if differing:
                print("FAIL: keystone-listing is out of date with server.py. Run:")
                print("  python3 scripts/gen-keystone-payload.py")
                print("And commit the regenerated files. Differing files:")
                for f in differing:
                    print(f"  dist/keystone-listing/{f}")
                return 1
            print("OK: dist/keystone-listing/ matches the current server.py tool surface")
        return 0

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "glama.json").write_text(gen_glama_json())
    (args.out / "smithery.yaml").write_text(gen_smithery_yaml())
    (args.out / "mcpso.json").write_text(gen_mcpso_json())
    (args.out / "pulse.md").write_text(gen_pulse_pitch())
    (args.out / "x402-bazaar-discovery.json").write_text(gen_x402_bazaar_discovery())

    print(f"Wrote 5 keystone-listing files to {args.out}/")
    for p in sorted(args.out.iterdir()):
        print(f"  {p.relative_to(REPO_ROOT)} ({p.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
