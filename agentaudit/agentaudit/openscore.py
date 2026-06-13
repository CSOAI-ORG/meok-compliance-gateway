"""OpenScore — Trust scoring algorithm for the OpenMoE-BFT Empire (Layer 3).

Maps MCP attestations + A2A Agent Cards to a 0.0–1.0 trust score,
broken down by each of the 14 safety experts and by regulation.
Incorporates BFT consensus weighting: entries with verified consensus
receive a bonus; broken consensus applies a penalty.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .compliance_matrix import Regulation, by_regulation
from .safety_experts import EXPERTS
from .audit_trail import AuditTrail
from .bft import BFTConsensus


@dataclass
class ExpertScore:
    expert_id: int
    expert_name: str
    score: float           # 0.0 – 1.0
    weight: float          # contribution to overall score
    missing: list[str]     # check IDs missing evidence


@dataclass
class OpenScoreResult:
    agent_id: str
    overall: float                 # 0.0 – 1.0
    by_regulation: dict[str, float]
    by_expert: list[ExpertScore]
    missing_checks: list[str]
    audit_integrity: bool
    bft_bonus: float = 0.0         # +0.1 for verified consensus
    bft_penalty: float = 0.0       # -0.2 for broken consensus


def openscore(
    agent_id: str,
    card: dict[str, Any],
    audit: AuditTrail | None = None,
    bft: BFTConsensus | None = None,
) -> OpenScoreResult:
    """Score an A2A Agent Card using the OpenScore algorithm.

    Parameters
    ----------
    agent_id: canonical identifier (DID or URL)
    card: parsed Agent Card JSON
    audit: optional AuditTrail for integrity verification
    bft: optional BFTConsensus for consensus-weighted scoring
    """
    if audit is not None:
        broken = audit.verify()
        integrity = len(broken) == 0
    else:
        integrity = True

    by_expert: list[ExpertScore] = []
    missing: list[str] = []
    total_weight = 0.0
    accrued = 0.0

    for expert in EXPERTS:
        w = 1.0 if expert.regulation else 0.5
        total_weight += w

        if expert.checks:
            # Regulation-backed expert: score by check evidence
            got = 0.0
            subtotal = 0.0
            expert_missing: list[str] = []
            for check_id in expert.checks:
                # Find the matching Check in MATRIX
                from .compliance_matrix import MATRIX
                check = next((c for c in MATRIX if c.id == check_id), None)
                if check is None:
                    continue
                cw = 1.0 if check.mandatory else 0.5
                subtotal += cw
                if _has_evidence(card, check.a2a_field):
                    got += cw
                else:
                    expert_missing.append(check_id)
                    missing.append(check_id)
            score = got / subtotal if subtotal > 0 else 0.0
        else:
            # Non-regulation expert: score by dedicated a2a_field
            score = 1.0 if _has_evidence(card, expert.a2a_field) else 0.0
            expert_missing = []
            if score < 1.0:
                missing.append(f"expert-{expert.expert_id}")

        accrued += score * w
        by_expert.append(ExpertScore(
            expert_id=expert.expert_id,
            expert_name=expert.name,
            score=round(score, 4),
            weight=w,
            missing=expert_missing,
        ))

    overall = accrued / total_weight if total_weight > 0 else 0.0

    # BFT consensus adjustments
    bft_bonus = 0.0
    bft_penalty = 0.0
    if bft is not None:
        if bft.consensus_reached:
            bft_bonus = 0.1
            overall = min(1.0, overall + bft_bonus)
        else:
            bft_penalty = 0.2
            overall = max(0.0, overall - bft_penalty)

    if not integrity:
        overall *= 0.5

    by_reg: dict[str, float] = {}
    for reg in (Regulation.EU_AI_ACT, Regulation.DORA, Regulation.NIS2, Regulation.CRA):
        by_reg[reg.value] = _reg_score(reg, card)

    return OpenScoreResult(
        agent_id=agent_id,
        overall=round(overall, 4),
        by_regulation=by_reg,
        by_expert=by_expert,
        missing_checks=missing,
        audit_integrity=integrity,
        bft_bonus=bft_bonus,
        bft_penalty=bft_penalty,
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


# Backward-compatible alias for bridge.py consumers
score_agent_card = openscore
TrustScore = OpenScoreResult
