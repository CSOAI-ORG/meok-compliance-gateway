"""Unit tests for AgentAudit / OpenMoE-BFT Empire aligned modules."""

from __future__ import annotations

import json

from agentaudit.compliance_matrix import MATRIX, by_regulation, by_risk, by_expert, Regulation, RiskLevel
from agentaudit.safety_experts import EXPERTS, by_id, by_domain, ExpertDomain
from agentaudit.audit_trail import AuditTrail, AuditEntry
from agentaudit.signet import SignetKey, sign_entry, verify_receipt
from agentaudit.bft import BFTConsensus
from agentaudit.openscore import openscore
from agentaudit.server import (
    get_compliance_matrix, score_agent, create_audit_trail,
    get_safety_experts, generate_signet_receipt, cast_bft_vote,
    get_bft_status, register_expert, finalize_bft_round, x402_spending_report,
    compliance_gap_analyser, expert_quorum_consult,
    audit_trail_export_anchored, threat_intel_lookup,
)


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
    _ = json.loads(out2)
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


# ── Paid tools (smoke, X402_ENABLED unset → transparent) ───────


def test_finalize_bft_round_consensus() -> None:
    """finalize_bft_round tallies votes, mints a Signet receipt for the majority hash."""
    sid = "session-finalize-1"
    cast_bft_vote(sid, "n1", "hashW", total_nodes=5)
    cast_bft_vote(sid, "n2", "hashW")
    cast_bft_vote(sid, "n3", "hashW")  # quorum = 3 for 5 nodes
    out = finalize_bft_round(sid)
    data = json.loads(out)
    assert data["consensus_reached"] is True
    assert data["majority_hash"] == "hashW"
    assert "signet_receipt" in data
    assert data["signet_receipt"]["entry_hash"] == f"bft:{sid}:hashW"
    assert "signature" in data["signet_receipt"]


def test_finalize_bft_round_no_consensus() -> None:
    """Without quorum, finalize still runs and surfaces a Signet receipt for the leading hash."""
    sid = "session-finalize-split"
    cast_bft_vote(sid, "n1", "hashX", total_nodes=5)
    cast_bft_vote(sid, "n2", "hashY", total_nodes=5)
    out = finalize_bft_round(sid)
    data = json.loads(out)
    assert data["consensus_reached"] is False
    # Leading hash is still attested so the buyer can show "what we had at round-end".
    assert "signet_receipt" in data


def test_finalize_bft_round_no_session() -> None:
    out = finalize_bft_round("nope-no-such-session")
    data = json.loads(out)
    assert "error" in data


def test_x402_spending_report_empty() -> None:
    out = x402_spending_report()
    data = json.loads(out)
    assert "total_calls" in data
    assert "by_tool" in data
    assert "recent" in data
    # The report itself is free and doesn't count as a paid call.
    assert data["total_calls"] == 0


def test_x402_spending_report_records_paid_call(x402_enabled, monkeypatch) -> None:
    """A verified paid call must show up in the spending report."""
    from agentaudit import x402 as xm
    from tests.test_x402 import _FakeResourceServer, _FakeVerify, _ctx_with_meta  # type: ignore[import-not-found]

    fake = _FakeResourceServer(verify=_FakeVerify(is_valid=True))
    monkeypatch.setattr(xm, "_resource_server", lambda: fake)

    def tool(x, ctx):
        return x

    wrapped = xm.paywalled(price="$0.10", tool_name="spending_test_tool")(tool)
    ctx = _ctx_with_meta(meta={xm.PAYMENT_META_KEY: {
        "payload": {"authorization": {"from": "0x1234567890abcdef1234567890abcdef12345678"}}
    }})
    wrapped("hi", ctx=ctx)

    out = x402_spending_report()
    data = json.loads(out)
    assert data["total_calls"] >= 1
    assert "spending_test_tool" in data["by_tool"]
    # Payer should be the truncated address, not the full one.
    assert any("0x12345678" in r["payer"] for r in data["recent"])


def test_x402_spending_report_records_score_agent(x402_enabled, monkeypatch) -> None:
    """The real score_agent tool, when re-wrapped with @paywalled (the same way FastMCP
    registers it), must populate the spending report on a verified call.

    Mirrors the existing pattern in tests/test_x402.py — FastMCP's @mcp.tool wrapper
    doesn't expose the inner paywalled function, so the test re-wraps explicitly to
    exercise the @paywalled → server.score_agent → spending-log path end-to-end.
    """
    from agentaudit import x402 as xm
    from tests.test_x402 import _FakeResourceServer, _FakeVerify, _ctx_with_meta  # type: ignore[import-not-found]

    fake = _FakeResourceServer(verify=_FakeVerify(is_valid=True))
    monkeypatch.setattr(xm, "_resource_server", lambda: fake)

    # Re-wrap the imported score_agent — same shape as server.py's @mcp.tool(@paywalled(score_agent))
    paywalled_score = xm.paywalled(price="$0.10", tool_name="score_agent")(score_agent)
    card = {"documentationUrl": "https://example.com/docs"}
    ctx = _ctx_with_meta(meta={xm.PAYMENT_META_KEY: {
        "payload": {"authorization": {"from": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}
    }})
    out = paywalled_score("did:web:example.com", json.dumps(card), None, ctx=ctx)
    data = json.loads(out)
    assert "overall" in data  # the tool body ran — verify+settle succeeded

    report = json.loads(x402_spending_report())
    assert "score_agent" in report["by_tool"]
    assert any("0xaaaa" in r["payer"] for r in report["recent"])
    assert any(r["price"] == "$0.10" for r in report["recent"] if r["tool"] == "score_agent")


# ── Paid compliance + audit tools (smoke) ─────────────────────


def test_compliance_gap_analyser_finds_missing_fields() -> None:
    """An empty card must surface every applicable check as a gap."""
    out = compliance_gap_analyser(json.dumps({}))
    data = json.loads(out)
    assert data["missing_count"] >= 10       # the matrix has many required fields
    assert data["compliance_pct"] == 0.0
    assert "gaps" in data
    sample = data["gaps"][0]
    assert {"check_id", "regulation", "article", "missing_field", "risk_level"} <= sample.keys()


def test_compliance_gap_analyser_filled_card() -> None:
    """A fully-filled card must report 0 gaps and 100% compliance."""
    full_card = {
        "id": "did:web:example.com",
        "metadata": {
            "riskAssessment": "done",
            "trainingDataProvenance": "done",
            "humanOversightContact": "done",
            "contentOriginTag": "done",
            "forbiddenUseCases": [],
            "ictRiskFramework": "done",
            "resilienceTestReport": "done",
            "supplyChainAudit": "done",
            "lastIncidentReport": "done",
            "vulnerabilityDisclosure": "done",
            "updatePolicy": "done",
        },
        "documentationUrl": "https://example.com/docs",
    }
    out = compliance_gap_analyser(json.dumps(full_card))
    data = json.loads(out)
    assert data["missing_count"] == 0
    assert data["compliance_pct"] == 100.0


def test_compliance_gap_analyser_regulation_filter() -> None:
    """`regulation=eu_ai_act` must restrict the matrix to that regulation's checks."""
    out = compliance_gap_analyser(json.dumps({}), regulation="eu_ai_act")
    data = json.loads(out)
    assert all(g["regulation"] == "eu_ai_act" for g in data["gaps"])


def test_compliance_gap_analyser_invalid_json() -> None:
    out = compliance_gap_analyser("not json")
    data = json.loads(out)
    assert "error" in data


def test_expert_quorum_consult() -> None:
    out = expert_quorum_consult("How do we prove EU AI Act Art 9 compliance?", n_experts=3)
    data = json.loads(out)
    assert data["experts_consulted"] == 3
    assert len(data["digest"]) == 3
    assert all(d["expert_id"] in (1, 2, 3) for d in data["digest"])
    assert "quorum_receipt" in data
    assert data["quorum_receipt"]["scheme"] in ("ed25519", "hmac-sha256")


def test_expert_quorum_consult_clamps_n() -> None:
    """n_experts must clamp to [1, 14] regardless of the caller's value."""
    out = expert_quorum_consult("test", n_experts=999)
    data = json.loads(out)
    assert data["experts_consulted"] == 14
    out2 = expert_quorum_consult("test", n_experts=0)
    data2 = json.loads(out2)
    assert data2["experts_consulted"] == 1


def test_audit_trail_export_anchored_no_session() -> None:
    out = audit_trail_export_anchored("does-not-exist")
    data = json.loads(out)
    assert "error" in data


def test_audit_trail_export_anchored_ok() -> None:
    sid = "export-session-test"
    create_audit_trail(sid)
    # Use append_audit_event through the server path
    from agentaudit.server import append_audit_event
    append_audit_event(sid, "a2a", "src", "tgt", "act", json.dumps({"k": "v"}))
    out = audit_trail_export_anchored(sid)
    data = json.loads(out)
    assert data["entries"] >= 1
    assert data["anchor"].startswith("sha256:")
    assert data["integrity_ok"] is True
    assert "signet_receipt" in data
    assert "trail" in data
    assert isinstance(data["trail"], list) and len(data["trail"]) >= 1


def test_threat_intel_lookup_deterministic() -> None:
    """Same indicator → same score (deterministic placeholder)."""
    a = json.loads(threat_intel_lookup("evil.example.com"))
    b = json.loads(threat_intel_lookup("evil.example.com"))
    assert a["score"] == b["score"]
    assert a["severity"] == b["severity"]
    assert 0 <= a["score"] <= 100
    assert a["severity"] in ("low", "medium", "high", "critical")


def test_threat_intel_lookup_empty_indicator() -> None:
    out = threat_intel_lookup("")
    data = json.loads(out)
    assert "error" in data


def test_threat_intel_lookup_bad_type() -> None:
    out = threat_intel_lookup("evil.example.com", indicator_type="email")
    data = json.loads(out)
    assert "error" in data


def test_threat_intel_lookup_includes_signet_receipt() -> None:
    data = json.loads(threat_intel_lookup("1.2.3.4", indicator_type="ip"))
    assert data["indicator_type"] == "ip"
    assert "signet_receipt" in data
    assert data["signet_receipt"]["entry_hash"].startswith("ti:ip:1.2.3.4")

