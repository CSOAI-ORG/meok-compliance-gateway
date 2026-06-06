"""MCP attestation → A2A Agent Card trust-score bridge."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .compliance_matrix import Check, Regulation, RiskLevel, by_regulation
from .audit_trail import AuditTrail, AuditEntry


@dataclass
class TrustScore:
    agent_id: str
    overall: float                 # 0.0 – 1.0
    by_regulation: dict[str, float] = field(default_factory=dict)
    missing_checks: list[str] = field(default_factory=list)
    audit_integrity: bool = True   # chain verified?


def score_agent_card(
    agent_id: str,
    card: dict[str, Any],
    audit: AuditTrail | None = None,
) -> TrustScore:
    """Score an A2A Agent Card against the full compliance matrix.

    Parameters
    ----------
    agent_id: canonical identifier (DID or URL)
    card: parsed Agent Card JSON (e.g. from `/.well-known/agent.json`)
    audit: optional AuditTrail to verify integrity before scoring
    """
    if audit is not None:
        broken = audit.verify()
        integrity = len(broken) == 0
    else:
        integrity = True

    scores: dict[str, float] = {}
    missing: list[str] = []
    total_weight = 0.0
    accrued = 0.0

    for check in by_regulation(Regulation.EU_AI_ACT):
        weight = 1.0 if check.mandatory else 0.5
        total_weight += weight
        if _has_evidence(card, check.a2a_field):
            accrued += weight
        else:
            missing.append(check.id)

    for check in by_regulation(Regulation.DORA):
        weight = 1.0 if check.mandatory else 0.5
        total_weight += weight
        if _has_evidence(card, check.a2a_field):
            accrued += weight
        else:
            missing.append(check.id)

    for check in by_regulation(Regulation.NIS2):
        weight = 1.0 if check.mandatory else 0.5
        total_weight += weight
        if _has_evidence(card, check.a2a_field):
            accrued += weight
        else:
            missing.append(check.id)

    for check in by_regulation(Regulation.CRA):
        weight = 1.0 if check.mandatory else 0.5
        total_weight += weight
        if _has_evidence(card, check.a2a_field):
            accrued += weight
        else:
            missing.append(check.id)

    overall = accrued / total_weight if total_weight > 0 else 0.0
    if not integrity:
        overall *= 0.5  # severe penalty for broken chain

    scores["eu_ai_act"] = _reg_score(Regulation.EU_AI_ACT, card)
    scores["dora"] = _reg_score(Regulation.DORA, card)
    scores["nis2"] = _reg_score(Regulation.NIS2, card)
    scores["cra"] = _reg_score(Regulation.CRA, card)

    return TrustScore(
        agent_id=agent_id,
        overall=round(overall, 4),
        by_regulation=scores,
        missing_checks=missing,
        audit_integrity=integrity,
    )


def _has_evidence(card: dict[str, Any], field: str | None) -> bool:
    if field is None:
        return True
    parts = field.split(".")
    node = card
    for p in parts:
        if isinstance(node, dict) and p in node:
            node = node[p]
        else:
            return False
    return node not in (None, "", [], {})


def _reg_score(reg: Regulation, card: dict[str, Any]) -> float:
    checks = by_regulation(reg)
    total = 0.0
    got = 0.0
    for c in checks:
        w = 1.0 if c.mandatory else 0.5
        total += w
        if _has_evidence(card, c.a2a_field):
            got += w
    return round(got / total, 4) if total > 0 else 0.0
