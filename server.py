"""MEOK Compliance Gateway — keystone FastMCP server.

This is the keystone's tool surface, imported by `http_server.py` for
streamable-HTTP serving. The keystone is the billing endpoint of the
CSOAI-ORG fleet: it exposes a small set of high-value MCP tools gated by
x402 USDC paywall, plus free observability + expert-listing tools that act
as top-of-funnel for agent developers.

Design notes
------------
* `mcp` is a module-level FastMCP singleton — `http_server.py` does
  `import server` and reads `server.mcp`. Keep the name and the singleton
  pattern stable.
* Paywalled tools carry a `COST WARNING: $X per call` prefix in their
  `description=` (AWS-billable-tool convention, see CRITICAL_FIXES
  2026-06-08). Pricing is per-tool, not per-call-size.
* Free tools: `list_experts`, `get_compliance_matrix`, `spending_report`,
  `health`. These are funnel — agents discover the keystone, then graduate
  to paid calls.
* Paywalled tools: `sign_receipt`, `score_compliance`, `verify_attestation`.
  Each is a thin wrapper over the keystone's HMAC + Signet substrate.
* `X402_ENABLED=0` (the default) means every `@paywalled` decorator is a
  transparent no-op — the function runs as if undecorated. This is what
  keeps `tests/` green on a default checkout.

This file is intentionally a thin keystone surface, not a transplant of
the agentaudit server. The agentaudit server (`feat/agentaudit-server` →
`agentaudit/agentaudit/server.py`) is a separate, larger tool set; we
deliberately do NOT bundle it here. When the keystone graduates to a
"mega-server," this file becomes a 1-line `import` of the agentaudit mcp.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
import uuid
from typing import Any

from mcp.server.fastmcp import FastMCP

from meok_x402 import paywalled, spending_snapshot, audit_anchor_snapshot
from meok_rate_limit import ratelimited

# Module-level FastMCP singleton — http_server.py reads this.
mcp = FastMCP("meok-compliance-gateway")

# ── In-memory stores (production: Redis / Postgres) ─────────────
_attestations: dict[str, dict[str, Any]] = {}     # attestation_id → signed record
_experts: list[dict[str, Any]] = []               # seeded below


def _load_seed_experts() -> list[dict[str, Any]]:
    """The seed expert registry — the 14 OpenScore experts from the
    agentaudit branch, inlined so the keystone has zero cross-module
    dependencies. Each expert is a stable, addressable safety reviewer.
    """
    return [
        {"id": 1,  "name": "EU-AI-Act-Classifier",     "domain": "compliance",    "regulation": "eu_ai_act"},
        {"id": 2,  "name": "DORA-Incident-Reporter",   "domain": "compliance",    "regulation": "dora"},
        {"id": 3,  "name": "NIS2-Register-Checker",    "domain": "compliance",    "regulation": "nis2"},
        {"id": 4,  "name": "CRA-Attest-Verifier",      "domain": "compliance",    "regulation": "cra"},
        {"id": 5,  "name": "Prompt-Injection-Scanner", "domain": "security",      "regulation": None},
        {"id": 6,  "name": "Shadow-Agent-Discoverer",  "domain": "security",      "regulation": None},
        {"id": 7,  "name": "BFT-Round-Auditor",        "domain": "governance",    "regulation": None},
        {"id": 8,  "name": "Signet-Receipt-Validator", "domain": "verification",  "regulation": None},
        {"id": 9,  "name": "Threat-Intel-Lookup",      "domain": "security",      "regulation": None},
        {"id": 10, "name": "Audit-Trail-Exporter",     "domain": "verification",  "regulation": None},
        {"id": 11, "name": "OpenScore-Aggregator",     "domain": "verification",  "regulation": None},
        {"id": 12, "name": "Compliance-Gap-Analyser",  "domain": "compliance",    "regulation": None},
        {"id": 13, "name": "Agent-Card-Registrar",     "domain": "governance",    "regulation": None},
        {"id": 14, "name": "Quorum-Consult-Broker",    "domain": "monetization",  "regulation": None},
    ]


# Seed the expert registry after the function is defined.
_experts = _load_seed_experts()


def _signing_key() -> bytes:
    """Read the HMAC signing key. Same resolution order as meok_x402."""
    # 1. env (dev only — MEOK_ATTESTATION_KEY)
    val = os.environ.get("MEOK_ATTESTATION_KEY")
    if val:
        return val.encode()
    # 2. meok_secrets (production path)
    try:
        from meok_secrets import get_secret
        v = get_secret("attestation-key")
        if v:
            return v.encode()
    except Exception:
        pass
    # 3. ephemeral dev key — never trust in prod. Loud warning.
    import secrets
    import warnings
    warnings.warn(
        "MEOK_ATTESTATION_KEY not set; using ephemeral dev key. "
        "Set MEOK_ATTESTATION_KEY or meok_secrets['attestation-key'] "
        "before MEOK_ENV=production.",
        RuntimeWarning,
        stacklevel=2,
    )
    return secrets.token_bytes(32)


# ────────────────────────── Free tools (funnel) ──────────────────────────


@mcp.tool(description="List the 14 OpenScore safety experts (free, top-of-funnel, 5 calls/day per caller).")
@ratelimited("list_experts")
def list_experts(domain: str | None = None) -> str:
    """Return the expert registry, optionally filtered by domain.

    Parameters
    ----------
    domain : str | None
        Filter: "compliance", "security", "governance", "monetization", "verification".
    """
    if domain:
        experts = [e for e in _experts if e["domain"] == domain]
    else:
        experts = list(_experts)
    return json.dumps({"count": len(experts), "experts": experts}, indent=2)


@mcp.tool(description="Return the keystone's x402 spending report (free observability, 20 calls/day per caller).")
@ratelimited("spending_report")
def spending_report() -> str:
    """In-memory log of verified paid calls. No PII (payer addresses are truncated)."""
    return json.dumps(spending_snapshot(), indent=2)


@mcp.tool(description="Return the keystone's tamper-evident audit-anchor chain tail + head (free observability).")
@ratelimited("spending_report")
def audit_anchor() -> str:
    """Chained-HMAC audit log: every settled x402 call appends a row whose
    hash includes the previous row's hash. Buyers reconcile this against
    the facilitator dashboard to confirm what their agents actually paid for."""
    return json.dumps(audit_anchor_snapshot(limit=50), indent=2)


@mcp.tool(description="Keystone health + version info (free, no payment required).")
def health() -> str:
    return json.dumps({
        "status": "ok",
        "server": "meok-compliance-gateway",
        "x402_enabled": os.environ.get("X402_ENABLED", "0") in ("1", "true", "yes", "on"),
        "x402_network": os.environ.get("X402_NETWORK", "eip155:8453"),
        "x402_pay_to_set": bool(os.environ.get("X402_PAY_TO")),
        "experts_seeded": len(_experts),
        "ts": time.time(),
    }, indent=2)


# ────────────────────────── Paywalled tools ──────────────────────────


@mcp.tool(description="COST WARNING: $0.05 per call — Sign a SHA-256 hash and return a Signet receipt.")
@paywalled(price="$0.05", tool_name="sign_receipt")
def sign_receipt(payload_hex: str, ctx=None) -> str:
    """Return an HMAC-SHA256-signed receipt for a 32-byte hex hash.

    Parameters
    ----------
    payload_hex : str
        64-character hex string (the SHA-256 of the artefact being attested).
    """
    if len(payload_hex) != 64 or not all(c in "0123456789abcdefABCDEF" for c in payload_hex):
        return json.dumps({"error": "payload_hex must be 64 hex chars (SHA-256)"})
    digest = bytes.fromhex(payload_hex)
    sig = hmac.new(_signing_key(), digest, hashlib.sha256).hexdigest()
    attestation_id = str(uuid.uuid4())
    record = {
        "attestation_id": attestation_id,
        "payload_sha256": payload_hex,
        "hmac_sha256": sig,
        "signed_at": time.time(),
        "server": "meok-compliance-gateway",
    }
    _attestations[attestation_id] = record
    return json.dumps(record, indent=2)


@mcp.tool(description="COST WARNING: $0.05 per call — Verify a Signet receipt by id and re-compute the HMAC.")
@paywalled(price="$0.05", tool_name="verify_receipt")
def verify_receipt(attestation_id: str, ctx=None) -> str:
    """Re-compute the HMAC over the stored payload and compare to the stored sig.

    Parameters
    ----------
    attestation_id : str
        The id returned by sign_receipt.
    """
    record = _attestations.get(attestation_id)
    if not record:
        return json.dumps({"error": "unknown attestation_id"})
    digest = bytes.fromhex(record["payload_sha256"])
    expected = hmac.new(_signing_key(), digest, hashlib.sha256).hexdigest()
    valid = hmac.compare_digest(expected, record["hmac_sha256"])
    return json.dumps({
        "attestation_id": attestation_id,
        "valid": valid,
        "signed_at": record["signed_at"],
    }, indent=2)
