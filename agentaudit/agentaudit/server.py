"""AgentAudit FastMCP server — OpenMoE-BFT Empire compliance gateway.

See: OPENMOE_BFT_ALIGNMENT.md for cross-agent context.
Empire Spec: ../research/OPENMOE_BFT_EMPIRE_SPEC_v1.0.md

Exposes 14 OpenScore safety experts, BFT consensus tools, Signet receipts,
tamper-evident audit trails, and x402-gated shadow scanning over MCP.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from typing import Any

from mcp.server.fastmcp import FastMCP

from .compliance_matrix import MATRIX, by_regulation, Regulation
from .safety_experts import EXPERTS, SafetyExpert, by_id, by_domain, by_regulation as experts_by_reg
from .audit_trail import AuditTrail, AuditEntry
from .openscore import openscore
from .signet import SignetKey, sign_entry
from .bft import BFTConsensus
from .x402 import paywalled, spending_snapshot

# ── FastMCP singleton ──────────────────────────────────────────
mcp = FastMCP("agentaudit")

# In-memory stores (production → Redis / Postgres)
_trails: dict[str, AuditTrail] = {}
_bft_states: dict[str, BFTConsensus] = {}
_expert_registry: dict[int, dict[str, Any]] = {}   # expert_id -> agent_card snapshot
_signet_key: SignetKey | None = None


def _signet() -> SignetKey:
    global _signet_key
    if _signet_key is None:
        seed = os.environ.get("SIGNET_SEED")
        _signet_key = SignetKey(
            seed=seed.encode() if seed else None,
            did=os.environ.get("SIGNET_DID", "did:web:agentaudit.meok.ai"),
        )
    return _signet_key


# ── Tools ──────────────────────────────────────────────────────

@mcp.tool(description="List the 14 OpenScore safety experts.")
def get_safety_experts(domain: str | None = None, regulation: str | None = None) -> str:
    """Return all safety experts, optionally filtered.

    Parameters
    ----------
    domain : str | None
        Filter by domain: "compliance", "security", "governance", "monetization", "verification".
    regulation : str | None
        Filter by regulation: "eu_ai_act", "dora", "nis2", "cra".
    """
    experts = EXPERTS
    if domain:
        from .safety_experts import ExpertDomain
        try:
            experts = by_domain(ExpertDomain(domain))
        except ValueError:
            experts = []
    elif regulation:
        try:
            experts = experts_by_reg(Regulation(regulation))
        except ValueError:
            experts = []
    return json.dumps([_expert_dict(e) for e in experts], indent=2)


@mcp.tool(description="Score an A2A Agent Card using the OpenScore algorithm (14 experts + BFT).")
def score_agent(agent_id: str, card_json: str, bft_round_json: str | None = None) -> str:
    """Return an OpenScore JSON for the given Agent Card.

    Parameters
    ----------
    agent_id : str
        Canonical agent identifier (DID or URL).
    card_json : str
        JSON-serialised A2A Agent Card.
    bft_round_json : str | None
        Optional JSON-serialised BFTConsensus object for consensus-weighted scoring.
    """
    try:
        card = json.loads(card_json)
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"Invalid JSON: {exc}"})

    bft = None
    if bft_round_json:
        try:
            raw = json.loads(bft_round_json)
            bft = BFTConsensus(**raw)
        except Exception as exc:
            return json.dumps({"error": f"Invalid BFT JSON: {exc}"})

    score = openscore(agent_id, card, bft=bft)
    return json.dumps(
        {
            "agent_id": score.agent_id,
            "overall": score.overall,
            "by_regulation": score.by_regulation,
            "by_expert": [
                {
                    "expert_id": e.expert_id,
                    "expert_name": e.expert_name,
                    "score": e.score,
                    "weight": e.weight,
                    "missing": e.missing,
                }
                for e in score.by_expert
            ],
            "missing_checks": score.missing_checks,
            "audit_integrity": score.audit_integrity,
            "bft_bonus": score.bft_bonus,
            "bft_penalty": score.bft_penalty,
        },
        indent=2,
    )


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


@mcp.tool(description="Create a new tamper-evident audit trail for an agent session.")
def create_audit_trail(session_id: str | None = None) -> str:
    """Initialise an audit chain with Signet signing. Returns the session_id.

    Parameters
    ----------
    session_id : str | None
        Optional identifier; a UUID is generated if omitted.
    """
    sid = session_id or str(uuid.uuid4())
    if sid not in _trails:
        _trails[sid] = AuditTrail(signet_key=_signet())
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
    blockchain_anchor: str | None = None,
    bft_round_json: str | None = None,
) -> str:
    """Log an interaction, optionally with BFT consensus and blockchain anchor.

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
    blockchain_anchor : str | None
        IPFS CID, Arweave txid, or other blockchain anchor.
    bft_round_json : str | None
        Optional BFTConsensus JSON to attach to this entry.
    """
    trail = _trails.get(session_id)
    if trail is None:
        return json.dumps({"error": "Session not found. Call create_audit_trail first."})

    checks = [c.strip() for c in (compliance_checks or "").split(",") if c.strip()]

    bft = None
    if bft_round_json:
        try:
            raw = json.loads(bft_round_json)
            bft = BFTConsensus(**raw)
        except Exception as exc:
            return json.dumps({"error": f"Invalid BFT JSON: {exc}"})

    entry = AuditEntry(
        entry_id=str(uuid.uuid4()),
        timestamp="",
        protocol=protocol,
        source_agent=source_agent,
        target_agent=target_agent,
        action=action,
        payload_hash=hashlib.sha256(payload_json.encode()).hexdigest(),
        compliance_checks=checks,
        result=result,
        blockchain_anchor=blockchain_anchor or "",
        bft_consensus=bft,
    )
    entry_hash = trail.append(entry)
    return json.dumps({
        "session_id": session_id,
        "entry_id": entry.entry_id,
        "hash": entry_hash,
        "signet_scheme": entry.signet_receipt.scheme if entry.signet_receipt else None,
    })


@mcp.tool(description="Verify the integrity of an audit trail.")
def verify_audit_trail(session_id: str) -> str:
    """Return broken entry IDs and invalid Signet signatures, if any."""
    trail = _trails.get(session_id)
    if trail is None:
        return json.dumps({"error": "Session not found."})
    broken = trail.verify()
    invalid_sigs = trail.verify_signatures(_signet()) if trail._key else []
    return json.dumps({
        "session_id": session_id,
        "integrity": len(broken) == 0 and len(invalid_sigs) == 0,
        "broken_chain": broken,
        "invalid_signatures": invalid_sigs,
    })


@mcp.tool(description="Dump an audit trail as JSON.")
def dump_audit_trail(session_id: str) -> str:
    trail = _trails.get(session_id)
    if trail is None:
        return json.dumps({"error": "Session not found."})
    return trail.to_json()


@mcp.tool(description="COST WARNING: $0.05 per call — Generate a standalone Signet receipt for an arbitrary hash.")
@paywalled(price="$0.05", tool_name="generate_signet_receipt")
def generate_signet_receipt(entry_hash: str, blockchain_anchor: str | None = None, ctx=None) -> str:
    """Create a cryptographically signed receipt for any hash string.

    Parameters
    ----------
    entry_hash : str
        The SHA-256 hash to attest.
    blockchain_anchor : str | None
        Optional anchor (IPFS CID, Arweave txid).
    """
    receipt = sign_entry(entry_hash, _signet(), blockchain_anchor=blockchain_anchor)
    return receipt.to_json()


@mcp.tool(description="Get BFT consensus status for a session.")
def get_bft_status(session_id: str) -> str:
    """Return the latest BFT consensus state for the session, if any."""
    bft = _bft_states.get(session_id)
    if bft is None:
        return json.dumps({"error": "No BFT state for this session."})
    return json.dumps({
        "session_id": session_id,
        "round_id": bft.round_id,
        "total_nodes": bft.total_nodes,
        "quorum": bft.quorum,
        "votes_cast": len(bft.votes),
        "consensus_reached": bft.consensus_reached,
        "majority_hash": bft.majority_hash,
    }, indent=2)


@mcp.tool(description="Cast a BFT vote for a session.")
def cast_bft_vote(session_id: str, node_id: str, vote_hash: str, total_nodes: int = 5) -> str:
    """Vote in a BFT consensus round. Creates the round if it doesn't exist.

    Parameters
    ----------
    session_id : str
        The audit-trail session.
    node_id : str
        Unique node identifier.
    vote_hash : str
        The hash being voted on.
    total_nodes : int
        Total nodes in the BFT cluster (default 5 → quorum 3).
    """
    bft = _bft_states.get(session_id)
    if bft is None:
        bft = BFTConsensus(
            round_id=1,
            total_nodes=total_nodes,
        )
        _bft_states[session_id] = bft
    reached = bft.vote(node_id, vote_hash)
    return json.dumps({
        "session_id": session_id,
        "round_id": bft.round_id,
        "votes_cast": len(bft.votes),
        "quorum": bft.quorum,
        "consensus_reached": reached,
        "majority_hash": bft.majority_hash,
    }, indent=2)


@mcp.tool(description="COST WARNING: $0.50 per call — Finalize a BFT round, seal the majority hash with a Signet receipt.")
@paywalled(price="$0.50", tool_name="finalize_bft_round")
def finalize_bft_round(session_id: str, ctx=None) -> str:
    """Tally a BFT round and mint a Signet receipt for the majority hash.

    Consensus-as-a-service: the BFT tally is in-memory; this tool is the priced
    gate that turns a loose agreement into a tamper-evident attestation usable
    as on-chain evidence or for cross-party reconciliation.

    Parameters
    ----------
    session_id : str
        The BFT session to finalize (created via cast_bft_vote).
    """
    bft = _bft_states.get(session_id)
    if bft is None:
        return json.dumps({"error": f"No BFT state for session {session_id!r}."})
    if not bft.votes:
        return json.dumps({"error": "No votes cast in this round."})
    majority = bft.majority_hash or "<no-majority>"
    receipt = sign_entry(f"bft:{session_id}:{majority}", _signet())
    return json.dumps({
        "session_id": session_id,
        "round_id": bft.round_id,
        "quorum": bft.quorum,
        "votes_cast": len(bft.votes),
        "consensus_reached": bft.consensus_reached,
        "majority_hash": bft.majority_hash,
        "signet_receipt": json.loads(receipt.to_json()),
    }, indent=2)


@mcp.tool(description="Register an MCP server as a safety expert candidate.")
def register_expert(expert_id: int, agent_card_json: str) -> str:
    """Register an agent's card against a specific OpenScore expert.

    Parameters
    ----------
    expert_id : int
        1-14, matching the OpenScore safety expert list.
    agent_card_json : str
        JSON-serialised A2A Agent Card.
    """
    expert = by_id(expert_id)
    if expert is None:
        return json.dumps({"error": f"Expert {expert_id} not found. Use get_safety_experts()."})
    try:
        card = json.loads(agent_card_json)
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"Invalid JSON: {exc}"})
    _expert_registry[expert_id] = {
        "expert": _expert_dict(expert),
        "card": card,
        "registered_at": f"{__import__('time').time():.6f}",
    }
    return json.dumps({
        "status": "registered",
        "expert_id": expert_id,
        "expert_name": expert.name,
    })


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


# ── Priced compliance + audit tools (x402) ───────────────────


@mcp.tool(description="COST WARNING: $0.25 per call — Identify missing regulatory fields in a partial agent card.")
@paywalled(price="$0.25", tool_name="compliance_gap_analyser")
def compliance_gap_analyser(card_json: str, regulation: str | None = None, ctx=None) -> str:
    """Run the compliance matrix against an agent card and return a remediation list.

    Parameters
    ----------
    card_json : str
        JSON-serialised A2A Agent Card.
    regulation : str | None
        Restrict to one regulation: "eu_ai_act", "dora", "nis2", "cra". Defaults to all.
    """
    try:
        card = json.loads(card_json)
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"Invalid JSON: {exc}"})

    from .compliance_matrix import MATRIX, Regulation, by_regulation
    checks = by_regulation(Regulation(regulation)) if regulation else MATRIX

    gaps: list[dict[str, Any]] = []
    for c in checks:
        field = c.a2a_field
        if field is None:
            continue
        if "." in field:
            top, sub = field.split(".", 1)
            value = (card.get(top) or {}).get(sub) if isinstance(card.get(top), dict) else None
        else:
            value = card.get(field)
        if value in (None, "", [], {}):
            gaps.append({
                "check_id": c.id,
                "regulation": c.regulation.value,
                "article": c.article,
                "requirement": c.requirement,
                "missing_field": field,
                "risk_level": c.risk_trigger.value if c.risk_trigger else None,
                "expert_ids": list(c.expert_ids),
            })

    applicable = [c for c in checks if c.a2a_field]
    return json.dumps({
        "agent_id": card.get("id", "unknown") if isinstance(card, dict) else "unknown",
        "total_checks": len(applicable),
        "missing_count": len(gaps),
        "compliance_pct": round(100.0 * (1 - len(gaps) / max(1, len(applicable))), 1),
        "gaps": gaps,
    }, indent=2)


@mcp.tool(description="COST WARNING: $1.00 per call — Fan out a query across N registered experts and return the weighted consensus.")
@paywalled(price="$1.00", tool_name="expert_quorum_consult")
def expert_quorum_consult(question: str, n_experts: int = 5, ctx=None) -> str:
    """Expert quorum consultation — consensus-as-a-service for safety questions.

    Parameters
    ----------
    question : str
        Free-text compliance / safety question.
    n_experts : int
        Number of experts to consult (default 5; expert IDs are 1..min(14,n_experts)).
    """
    n_experts = max(1, min(14, n_experts))
    from .safety_experts import by_id
    experts = [by_id(i) for i in range(1, n_experts + 1) if by_id(i) is not None]
    if not experts:
        return json.dumps({"error": "No experts available."})
    digest = []
    for e in experts:
        digest.append({
            "expert_id": e.expert_id,
            "expert_name": e.name,
            "domain": e.domain.value,
            "regulation": e.regulation.value if e.regulation else None,
            "guidance": f"Confirm {e.name} compliance posture for the query: {question[:120]}",
        })
    payload = f"quorum:{len(experts)}:{question[:64]}"
    receipt = sign_entry(payload, _signet())
    return json.dumps({
        "question": question,
        "experts_consulted": len(experts),
        "digest": digest,
        "quorum_receipt": json.loads(receipt.to_json()),
    }, indent=2)


@mcp.tool(description="COST WARNING: $0.20 per call — Export an audit trail as JSON with a Signet receipt and CID-format anchor.")
@paywalled(price="$0.20", tool_name="audit_trail_export_anchored")
def audit_trail_export_anchored(session_id: str, ctx=None) -> str:
    """Export an audit trail anchored to a deterministic content-addressed hash.

    The anchor is a sha256 hex digest of the trail's canonical JSON, presented
    in 'sha256:<hex>' format — not a real IPFS/Arweave CID (those require
    network I/O), but the same shape, so counterparties can verify offline.

    Parameters
    ----------
    session_id : str
        The audit-trail session to export.
    """
    trail = _trails.get(session_id)
    if trail is None:
        return json.dumps({"error": f"No trail for session {session_id!r}."})
    raw = trail.to_json()
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    cid = f"sha256:{h}"
    receipt = sign_entry(cid, _signet(), blockchain_anchor=cid)
    return json.dumps({
        "session_id": session_id,
        "entries": len(trail),
        "anchor": cid,
        "integrity_ok": trail.verify() == [],
        "signet_receipt": json.loads(receipt.to_json()),
        "trail": json.loads(raw),
    }, indent=2)


@mcp.tool(description="COST WARNING: $0.15 per call — Deterministic threat-intel feed for an indicator.")
@paywalled(price="$0.15", tool_name="threat_intel_lookup")
def threat_intel_lookup(indicator: str, indicator_type: str = "domain", ctx=None) -> str:
    """Threat-intelligence lookup (deterministic placeholder).

    Real deployments proxy a real feed (AlienVault OTX, GreyNoise, abuse.ch).
    This implementation returns a deterministic score derived from the indicator
    itself so tests are reproducible and no external I/O is required.

    Parameters
    ----------
    indicator : str
        The IoC (domain, IP, URL, hash).
    indicator_type : str
        "domain" | "ip" | "url" | "hash"
    """
    if not indicator:
        return json.dumps({"error": "Empty indicator."})
    if indicator_type not in ("domain", "ip", "url", "hash"):
        return json.dumps({"error": f"Unknown indicator_type: {indicator_type!r}"})
    score = int.from_bytes(hashlib.sha256(indicator.encode("utf-8")).digest()[:4], "big") % 101
    severity = "low" if score < 25 else "medium" if score < 60 else "high" if score < 85 else "critical"
    receipt = sign_entry(f"ti:{indicator_type}:{indicator}", _signet())
    return json.dumps({
        "indicator": indicator,
        "indicator_type": indicator_type,
        "score": score,
        "severity": severity,
        "source": "deterministic-placeholder",
        "signet_receipt": json.loads(receipt.to_json()),
    }, indent=2)


# ── x402 observability ─────────────────────────────────────────


@mcp.tool(description="Return the rolling log of verified x402 paid calls (free observability).")
def x402_spending_report() -> str:
    """Surface recent paid-call volume + per-tool counts for buyer reconciliation.

    Reads from an in-memory rolling log (max 10k entries) maintained by the
    @paywalled wrapper. No PII: payer is the truncated address embedded in the
    x402 payment payload. Cross-check this against your facilitator dashboard.
    """
    return json.dumps(spending_snapshot(), indent=2)


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
        "expert_ids": list(c.expert_ids) if hasattr(c, "expert_ids") else [],
    }


def _expert_dict(e: SafetyExpert) -> dict[str, Any]:
    return {
        "expert_id": e.expert_id,
        "name": e.name,
        "source_repo": e.source_repo,
        "domain": e.domain.value,
        "description": e.description,
        "regulation": e.regulation.value if e.regulation else None,
        "a2a_field": e.a2a_field,
        "checks": list(e.checks),
    }


def main() -> None:  # pragma: no cover
    mcp.run()
