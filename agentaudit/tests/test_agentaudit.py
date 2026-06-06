"""Unit tests for AgentAudit core modules."""

from __future__ import annotations

import json
import pytest

from agentaudit.compliance_matrix import MATRIX, by_regulation, by_risk, Regulation, RiskLevel
from agentaudit.audit_trail import AuditTrail, AuditEntry
from agentaudit.bridge import score_agent_card, TrustScore


# ── Compliance Matrix ──────────────────────────────────────────

def test_matrix_not_empty() -> None:
    assert len(MATRIX) > 0


def test_by_regulation_filter() -> None:
    eu = by_regulation(Regulation.EU_AI_ACT)
    assert all(c.regulation == Regulation.EU_AI_ACT for c in eu)
    assert len(eu) < len(MATRIX)


def test_by_risk_filter() -> None:
    high = by_risk(RiskLevel.HIGH)
    assert all(c.risk_trigger == RiskLevel.HIGH for c in high)


# ── Audit Trail ────────────────────────────────────────────────

def test_audit_chain_integrity() -> None:
    trail = AuditTrail()
    e1 = AuditEntry(
        entry_id="e1",
        timestamp="1.0",
        protocol="a2a",
        source_agent="a",
        target_agent="b",
        action="test",
        payload_hash="abc",
    )
    h1 = trail.append(e1)
    assert len(trail) == 1

    e2 = AuditEntry(
        entry_id="e2",
        timestamp="2.0",
        protocol="a2a",
        source_agent="b",
        target_agent="c",
        action="test",
        payload_hash="def",
    )
    h2 = trail.append(e2)
    assert len(trail) == 2
    assert h1 != h2

    broken = trail.verify()
    assert broken == []


def test_audit_chain_tamper_detection() -> None:
    trail = AuditTrail()
    e1 = AuditEntry(
        entry_id="e1",
        timestamp="1.0",
        protocol="a2a",
        source_agent="a",
        target_agent="b",
        action="test",
        payload_hash="abc",
    )
    trail.append(e1)
    # Tamper by mutating the stored entry directly (protected by frozen dataclass,
    # but in a mutable trail we can't freeze the list item; so we check via private)
    # Actually AuditEntry is NOT frozen; let's check.
    assert not getattr(e1, "__dataclass_params__", None) or not e1.__dataclass_params__.frozen
    # We intentionally don't freeze AuditEntry to allow compute_hash
    # Tamper detection works on parent_hash mismatch across appended entries.
    # Let's simulate a break by appending an entry with wrong parent_hash.
    e2 = AuditEntry(
        entry_id="e2",
        timestamp="2.0",
        protocol="a2a",
        source_agent="b",
        target_agent="c",
        action="test",
        payload_hash="def",
        parent_hash="wrong",
    )
    trail._chain.append(e2)
    broken = trail.verify()
    assert "e2" in broken


# ── Bridge / Trust Score ───────────────────────────────────────

def test_score_empty_card() -> None:
    score = score_agent_card("did:web:example.com", {})
    assert score.overall == 0.0
    assert score.missing_checks
    assert score.audit_integrity is True


def test_score_full_card() -> None:
    card = {
        "metadata": {
            "riskAssessment": "done",
            "trainingDataProvenance": "done",
            "humanOversightContact": "done",
            "contentOriginTag": "done",
            "forbiddenUseCases": ["social_scoring_public_authorities"],
            "ictRiskFramework": "done",
            "resilienceTestReport": "done",
            "supplyChainAudit": "done",
            "lastIncidentReport": "done",
            "vulnerabilityDisclosure": "done",
            "updatePolicy": "done",
        },
        "documentationUrl": "https://example.com/docs",
    }
    score = score_agent_card("did:web:example.com", card)
    assert score.overall == 1.0
    assert score.missing_checks == []


def test_score_partial_card() -> None:
    card = {
        "metadata": {
            "riskAssessment": "done",
        },
        "documentationUrl": "https://example.com/docs",
    }
    score = score_agent_card("did:web:example.com", card)
    assert 0.0 < score.overall < 1.0
    assert any("eu-ai-act" in m for m in score.missing_checks)


# ── Server Tools (smoke) ───────────────────────────────────────

from agentaudit.server import get_compliance_matrix, score_agent, create_audit_trail


def test_get_compliance_matrix() -> None:
    out = get_compliance_matrix()
    data = json.loads(out)
    assert isinstance(data, list)
    assert len(data) == len(MATRIX)


def test_get_compliance_matrix_filtered() -> None:
    out = get_compliance_matrix("eu_ai_act")
    data = json.loads(out)
    assert all(d["regulation"] == "eu_ai_act" for d in data)


def test_score_agent_tool() -> None:
    card = {"documentationUrl": "https://example.com/docs"}
    out = score_agent("did:web:example.com", json.dumps(card))
    data = json.loads(out)
    assert "overall" in data
    assert data["overall"] < 1.0


def test_create_audit_trail() -> None:
    out = create_audit_trail()
    data = json.loads(out)
    assert data["status"] == "created"
    assert "session_id" in data
