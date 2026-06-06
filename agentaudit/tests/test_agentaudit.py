"""Unit tests for AgentAudit / OpenMoE-BFT Empire aligned modules."""

from __future__ import annotations

import json
import pytest

from agentaudit.compliance_matrix import MATRIX, by_regulation, by_risk, by_expert, Regulation, RiskLevel
from agentaudit.safety_experts import EXPERTS, by_id, by_domain, ExpertDomain
from agentaudit.audit_trail import AuditTrail, AuditEntry
from agentaudit.signet import SignetKey, sign_entry, verify_receipt
from agentaudit.bft import BFTConsensus
from agentaudit.openscore import openscore, OpenScoreResult, ExpertScore


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


def test_by_expert_mapping() -> None:
    # Expert #1 (EU AI Act) should have checks mapped
    checks = by_expert(1)
    assert len(checks) > 0
    assert all(1 in c.expert_ids for c in checks)


# ── Safety Experts ─────────────────────────────────────────────

def test_14_experts() -> None:
    assert len(EXPERTS) == 14


def test_expert_ids_unique() -> None:
    ids = [e.expert_id for e in EXPERTS]
    assert len(ids) == len(set(ids))
    assert sorted(ids) == list(range(1, 15))


def test_by_id_found() -> None:
    e = by_id(1)
    assert e is not None
    assert e.name == "EU AI Act Compliance"


def test_by_id_missing() -> None:
    assert by_id(99) is None


def test_by_domain_filter() -> None:
    sec = by_domain(ExpertDomain.SECURITY)
    assert all(e.domain == ExpertDomain.SECURITY for e in sec)
    assert len(sec) > 0


# ── Signet ─────────────────────────────────────────────────────

def test_signet_sign_verify() -> None:
    key = SignetKey(did="did:web:test")
    msg = b"hello world"
    sig = key.sign(msg)
    assert key.verify(msg, sig)
    assert not key.verify(msg + b"x", sig)


def test_signet_receipt_roundtrip() -> None:
    key = SignetKey(did="did:web:test")
    receipt = sign_entry("abc123", key)
    assert receipt.entry_hash == "abc123"
    assert receipt.signer_did == "did:web:test"
    assert verify_receipt(receipt, key)


def test_signet_co_sign() -> None:
    key_a = SignetKey(did="did:web:a")
    key_b = SignetKey(did="did:web:b")
    receipt = sign_entry("hash", key_a, co_key=key_b)
    assert receipt.co_signer_did == "did:web:b"
    assert receipt.co_signature_hex is not None


# ── BFT Consensus ──────────────────────────────────────────────

def test_bft_quorum_5_nodes() -> None:
    bft = BFTConsensus(round_id=1, total_nodes=5)
    assert bft.quorum == 3


def test_bft_quorum_7_nodes() -> None:
    bft = BFTConsensus(round_id=1, total_nodes=7)
    assert bft.quorum == 5


def test_bft_consensus_reached() -> None:
    bft = BFTConsensus(round_id=1, total_nodes=5)
    assert not bft.consensus_reached
    bft.vote("node1", "hashA")
    bft.vote("node2", "hashA")
    assert not bft.consensus_reached
    reached = bft.vote("node3", "hashA")
    assert reached
    assert bft.consensus_reached
    assert bft.majority_hash == "hashA"


def test_bft_consensus_split() -> None:
    bft = BFTConsensus(round_id=1, total_nodes=5)
    bft.vote("node1", "hashA")
    bft.vote("node2", "hashA")
    bft.vote("node3", "hashB")
    assert not bft.consensus_reached


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


def test_audit_chain_with_signet() -> None:
    key = SignetKey(did="did:web:test")
    trail = AuditTrail(signet_key=key)
    e = AuditEntry(
        entry_id="e1",
        timestamp="1.0",
        protocol="a2a",
        source_agent="a",
        target_agent="b",
        action="test",
        payload_hash="abc",
    )
    trail.append(e)
    assert e.signet_receipt is not None
    assert e.signet_receipt.signer_did == "did:web:test"

    invalid = trail.verify_signatures(key)
    assert invalid == []


def test_audit_chain_with_bft() -> None:
    trail = AuditTrail()
    bft = BFTConsensus(round_id=1, total_nodes=5)
    bft.vote("n1", "hashX")
    bft.vote("n2", "hashX")
    bft.vote("n3", "hashX")
    e = AuditEntry(
        entry_id="e1",
        timestamp="1.0",
        protocol="a2a",
        source_agent="a",
        target_agent="b",
        action="test",
        payload_hash="abc",
        bft_consensus=bft,
    )
    trail.append(e)
    assert e.bft_consensus is not None
    assert e.bft_consensus.consensus_reached


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


# ── OpenScore ──────────────────────────────────────────────────

def test_openscore_empty_card() -> None:
    score = openscore("did:web:example.com", {})
    assert score.overall == 0.0
    assert len(score.by_expert) == 14
    assert score.missing_checks
    assert score.audit_integrity is True


def test_openscore_full_card() -> None:
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
            "nistRmfScore": 0.95,
            "neurorightsPolicy": "strict",
            "x402Receipt": "valid",
            "mcpAttestation": "signed",
            "blockchainAnchor": "ipfs://Qmabc",
            "hitlContact": "human@example.com",
            "redTeamReport": "passed",
            "blueTeamStatus": "active",
            "continuousMonitoring": "enabled",
            "fuzzingReport": "clean",
            "autonomousAudit": "complete",
            "webExtractionPolicy": "gdpr_compliant",
        },
        "documentationUrl": "https://example.com/docs",
    }
    score = openscore("did:web:example.com", card)
    assert score.overall == 1.0
    assert score.missing_checks == []
    # Per-expert breakdown
    for es in score.by_expert:
        assert es.score == 1.0


def test_openscore_partial_card() -> None:
    card = {
        "metadata": {
            "riskAssessment": "done",
        },
        "documentationUrl": "https://example.com/docs",
    }
    score = openscore("did:web:example.com", card)
    assert 0.0 < score.overall < 1.0
    assert any("eu-ai-act" in m for m in score.missing_checks)


def test_openscore_bft_bonus() -> None:
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
            "nistRmfScore": 0.95,
            "neurorightsPolicy": "strict",
            "x402Receipt": "valid",
            "mcpAttestation": "signed",
            "blockchainAnchor": "ipfs://Qmabc",
            "hitlContact": "human@example.com",
            "redTeamReport": "passed",
            "blueTeamStatus": "active",
            "continuousMonitoring": "enabled",
            "fuzzingReport": "clean",
            "autonomousAudit": "complete",
            "webExtractionPolicy": "gdpr_compliant",
        },
        "documentationUrl": "https://example.com/docs",
    }
    bft = BFTConsensus(round_id=1, total_nodes=5)
    bft.vote("n1", "hashX")
    bft.vote("n2", "hashX")
    bft.vote("n3", "hashX")
    score = openscore("did:web:example.com", card, bft=bft)
    assert score.bft_bonus == 0.1
    assert score.overall == 1.0  # capped at 1.0


def test_openscore_bft_penalty() -> None:
    card = {
        "metadata": {
            "riskAssessment": "done",
        },
        "documentationUrl": "https://example.com/docs",
    }
    bft = BFTConsensus(round_id=1, total_nodes=5)
    bft.vote("n1", "hashA")
    bft.vote("n2", "hashB")
    bft.vote("n3", "hashC")
    score = openscore("did:web:example.com", card, bft=bft)
    assert score.bft_penalty == 0.2


# ── Server Tools (smoke) ───────────────────────────────────────

from agentaudit.server import (
    get_compliance_matrix, score_agent, create_audit_trail,
    get_safety_experts, generate_signet_receipt, cast_bft_vote,
    get_bft_status, register_expert,
)


def test_get_safety_experts() -> None:
    out = get_safety_experts()
    data = json.loads(out)
    assert isinstance(data, list)
    assert len(data) == 14


def test_get_safety_experts_filtered() -> None:
    out = get_safety_experts(domain="security")
    data = json.loads(out)
    assert all(d["domain"] == "security" for d in data)


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
    assert "by_expert" in data
    assert data["overall"] < 1.0


def test_score_agent_with_bft() -> None:
    card = {"documentationUrl": "https://example.com/docs"}
    bft_json = json.dumps({"round_id": 1, "total_nodes": 5, "votes": {"n1": "h", "n2": "h", "n3": "h"}})
    out = score_agent("did:web:example.com", json.dumps(card), bft_json)
    data = json.loads(out)
    assert "bft_bonus" in data


def test_create_audit_trail() -> None:
    out = create_audit_trail()
    data = json.loads(out)
    assert data["status"] == "created"
    assert "session_id" in data


def test_generate_signet_receipt() -> None:
    out = generate_signet_receipt("abc123")
    data = json.loads(out)
    assert data["entry_hash"] == "abc123"
    assert "signature" in data


def test_cast_bft_vote() -> None:
    out = cast_bft_vote("session-x", "node1", "hashA", total_nodes=5)
    data = json.loads(out)
    assert data["votes_cast"] == 1
    assert not data["consensus_reached"]

    out2 = cast_bft_vote("session-x", "node2", "hashA")
    data2 = json.loads(out2)
    out3 = cast_bft_vote("session-x", "node3", "hashA")
    data3 = json.loads(out3)
    assert data3["consensus_reached"]


def test_get_bft_status() -> None:
    cast_bft_vote("session-bft", "n1", "hashZ", total_nodes=5)
    out = get_bft_status("session-bft")
    data = json.loads(out)
    assert data["round_id"] == 1


def test_register_expert() -> None:
    card = {"name": "Test Agent"}
    out = register_expert(1, json.dumps(card))
    data = json.loads(out)
    assert data["status"] == "registered"
    assert data["expert_id"] == 1


def test_register_expert_invalid() -> None:
    out = register_expert(99, "{}")
    data = json.loads(out)
    assert "error" in data
