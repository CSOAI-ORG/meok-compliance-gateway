"""AgentAudit FastMCP server — compliance tools exposed over MCP."""

from __future__ import annotations

import json
import os
import uuid
from typing import Any

from mcp.server.fastmcp import FastMCP

from .compliance_matrix import MATRIX, by_regulation, by_risk, Regulation, RiskLevel
from .audit_trail import AuditTrail, AuditEntry
from .bridge import score_agent_card, TrustScore
from .x402 import paywalled

# ── FastMCP singleton ──────────────────────────────────────────
mcp = FastMCP("agentaudit")

# In-memory stores (production → Redis / Postgres)
_trails: dict[str, AuditTrail] = {}


# ── Helpers ────────────────────────────────────────────────────
def _enabled() -> bool:
    return os.environ.get("X402_ENABLED", "").strip() == "1"


# ── Tools ──────────────────────────────────────────────────────

@mcp.tool(description="Return the full compliance matrix (EU AI Act, DORA, NIS2, CRA).")
def get_compliance_matrix(regulation: str | None = None) -> str:
    """List every compliance check.

    Parameters
    ----------
    regulation : str | None
        Filter by regulation name: "eu_ai_act", "dora", "nis2", "cra".
    """
    if regulation:
        try:
            reg = Regulation(regulation)
            checks = by_regulation(reg)
        except ValueError:
            checks = []
    else:
        checks = MATRIX
    return json.dumps([_check_dict(c) for c in checks], indent=2)


@mcp.tool(description="Score an A2A Agent Card against the compliance matrix.")
def score_agent(agent_id: str, card_json: str) -> str:
    """Return a TrustScore JSON for the given Agent Card.

    Parameters
    ----------
    agent_id : str
        Canonical agent identifier (DID or URL).
    card_json : str
        JSON-serialised A2A Agent Card.
    """
    try:
        card = json.loads(card_json)
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"Invalid JSON: {exc}"})

    score = score_agent_card(agent_id, card)
    return json.dumps(
        {
            "agent_id": score.agent_id,
            "overall": score.overall,
            "by_regulation": score.by_regulation,
            "missing_checks": score.missing_checks,
            "audit_integrity": score.audit_integrity,
        },
        indent=2,
    )


@mcp.tool(description="Create a new tamper-evident audit trail for an agent session.")
def create_audit_trail(session_id: str | None = None) -> str:
    """Initialise an audit chain. Returns the session_id.

    Parameters
    ----------
    session_id : str | None
        Optional identifier; a UUID is generated if omitted.
    """
    sid = session_id or str(uuid.uuid4())
    if sid not in _trails:
        _trails[sid] = AuditTrail()
    return json.dumps({"session_id": sid, "status": "created"})


@mcp.tool(description="Append an event to an existing audit trail.")
def append_audit_event(
    session_id: str,
    protocol: str,
    source_agent: str,
    target_agent: str,
    action: str,
    payload_json: str,
    compliance_checks: str | None = None,
    result: str = "pending",
) -> str:
    """Log an interaction and return the entry hash.

    Parameters
    ----------
    session_id : str
        Trail identifier returned by create_audit_trail.
    protocol : str
        "a2a", "mcp", "anp".
    source_agent, target_agent : str
        Agent identifiers.
    action : str
        Tool name / task id / message type.
    payload_json : str
        JSON blob of the interaction payload.
    compliance_checks : str | None
        Comma-separated list of check IDs that were evaluated.
    result : str
        "pass", "fail", or "pending".
    """
    trail = _trails.get(session_id)
    if trail is None:
        return json.dumps({"error": "Session not found. Call create_audit_trail first."})

    checks = [c.strip() for c in (compliance_checks or "").split(",") if c.strip()]
    payload_hash = AuditEntry.compute_hash  # placeholder until we compute real hash

    entry = AuditEntry(
        entry_id=str(uuid.uuid4()),
        timestamp="",
        protocol=protocol,
        source_agent=source_agent,
        target_agent=target_agent,
        action=action,
        payload_hash="",  # computed inside append
        compliance_checks=checks,
        result=result,
    )
    entry_hash = trail.append(entry)
    return json.dumps({"session_id": session_id, "entry_id": entry.entry_id, "hash": entry_hash})


@mcp.tool(description="Verify the integrity of an audit trail.")
def verify_audit_trail(session_id: str) -> str:
    """Return broken entry IDs, if any."""
    trail = _trails.get(session_id)
    if trail is None:
        return json.dumps({"error": "Session not found."})
    broken = trail.verify()
    return json.dumps({"session_id": session_id, "integrity": len(broken) == 0, "broken": broken})


@mcp.tool(description="Dump an audit trail as JSON.")
def dump_audit_trail(session_id: str) -> str:
    trail = _trails.get(session_id)
    if trail is None:
        return json.dumps({"error": "Session not found."})
    return trail.to_json()


@mcp.tool(description="COST WARNING: $0.10 per call — Run a shadow scan for unregistered agents.")
@paywalled(price="$0.10", tool_name="scan_shadow_agents")
def scan_shadow_agents(candidate_urls: str, ctx=None) -> str:
    """Probe candidate URLs for A2A Agent Cards.

    Parameters
    ----------
    candidate_urls : str
        Newline-separated list of URLs to scan.
    """
    urls = [u.strip() for u in candidate_urls.splitlines() if u.strip()]
    if not urls:
        return json.dumps({"error": "No URLs provided."})

    # Synchronous scan for MCP tool compatibility
    from .shadow_scanner import ShadowScanner, DiscoveredAgent
    scanner = ShadowScanner()
    import asyncio

    async def _run() -> list[DiscoveredAgent]:
        return await scanner.scan(urls)

    try:
        results = asyncio.run(_run())
    except RuntimeError as exc:
        return json.dumps({"error": str(exc)})

    out = []
    for r in results:
        out.append(
            {
                "url": r.url,
                "status": r.status,
                "fingerprints": r.fingerprints,
                "card_present": r.agent_card is not None,
            }
        )
    return json.dumps(out, indent=2)


# ── Internal helpers ───────────────────────────────────────────
def _check_dict(c: Any) -> dict[str, Any]:
    return {
        "id": c.id,
        "regulation": c.regulation.value,
        "article": c.article,
        "requirement": c.requirement,
        "a2a_field": c.a2a_field,
        "mandatory": c.mandatory,
        "risk_trigger": c.risk_trigger.value if c.risk_trigger else None,
    }


def main() -> None:  # pragma: no cover
    mcp.run()
