"""Tests for the keystone server.py — the module http_server.py imports.

These cover the tool surface the keystone exposes: registration, free
tools (health, list_experts, spending_report), paywalled tools
(sign_receipt, verify_receipt) in their disabled-mode passthrough
(default X402_ENABLED=0, so @paywalled is a no-op — the test runs the
undecorated function body).

For the enabled-mode (X402_ENABLED=1) tests, see
`scripts/test_x402_settlement.py` which is the integration smoke.

Why a separate test file (not in tests/test_x402.py):
- test_x402.py covers the meok_x402.py substrate in isolation
- this file covers the server.py tool surface in isolation
- test_x402_settlement.py covers the end-to-end settlement flow

Together: substrate + surface + settlement = full revenue-rail coverage.
"""
from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

import pytest

# Repo root on path (same trick tests/test_x402.py uses)
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture
def fresh_server():
    """Import server.py fresh, with a clean X402_ENABLED (disabled = no-op).
    Sets MEOK_ATTESTATION_KEY to a stable value so sign + verify agree.
    Clears the in-process free-tier counter so cap tests are isolated."""
    os.environ.pop("X402_ENABLED", None)
    os.environ.pop("X402_PAY_TO", None)
    os.environ.pop("X402_NETWORK", None)
    # 64 hex chars = 32 bytes (HMAC-SHA256 key length). Stable across the
    # test run so sign_receipt + verify_receipt use the same key.
    os.environ["MEOK_ATTESTATION_KEY"] = "deadbeef" * 8
    if "server" in sys.modules:
        del sys.modules["server"]
    # Clear the rate-limit counters — they live in the meok_rate_limit module,
    # which is process-global. If we don't clear between tests, the cap tests
    # bleed into each other (one test's 5 list_experts calls exhaust the next
    # test's budget). This is the in-memory equivalent of a TRUNCATE.
    if "meok_rate_limit" in sys.modules:
        import meok_rate_limit
        with meok_rate_limit._LOCK:
            meok_rate_limit._COUNTS.clear()
    return importlib.import_module("server")


# ── Tool registration ───────────────────────────────────────────────


def test_all_expected_tools_registered(fresh_server):
    tools = fresh_server.mcp._tool_manager._tools
    names = set(tools.keys())
    expected_free = {"health", "list_experts", "spending_report", "audit_anchor"}
    expected_paid = {"sign_receipt", "verify_receipt"}
    assert expected_free <= names, f"missing free tools: {expected_free - names}"
    assert expected_paid <= names, f"missing paid tools: {expected_paid - names}"


def test_paywalled_tools_carry_cost_warning(fresh_server):
    """AWS-billable-tool convention: any paywalled tool's description must
    start with 'COST WARNING: $X per call' so agents see the cost up front."""
    tools = fresh_server.mcp._tool_manager._tools
    for name in ("sign_receipt", "verify_receipt"):
        desc = tools[name].description
        assert "COST WARNING" in desc, f"{name} missing COST WARNING: {desc!r}"
        assert "$0.05" in desc, f"{name} missing $0.05 price: {desc!r}"


def test_free_tools_have_no_cost_warning(fresh_server):
    tools = fresh_server.mcp._tool_manager._tools
    for name in ("health", "list_experts", "spending_report", "audit_anchor"):
        assert "COST WARNING" not in tools[name].description, \
            f"{name} (free) has COST WARNING — it shouldn't"


# ── Free tools (no payment, no env) ────────────────────────────────


def test_health_returns_ok(fresh_server):
    tools = fresh_server.mcp._tool_manager._tools
    out = tools["health"].fn()
    data = json.loads(out)
    assert data["status"] == "ok"
    assert data["server"] == "meok-compliance-gateway"
    # x402_enabled is False (default) — should reflect that
    assert data["x402_enabled"] is False
    # x402_pay_to is unset (default) — should reflect that
    assert data["x402_pay_to_set"] is False


def test_list_experts_returns_14(fresh_server):
    tools = fresh_server.mcp._tool_manager._tools
    out = tools["list_experts"].fn()
    data = json.loads(out)
    assert data["count"] == 14
    domains = {e["domain"] for e in data["experts"]}
    # All 5 expected domains are present
    assert {"compliance", "security", "governance", "monetization", "verification"} <= domains


def test_list_experts_filter_by_domain(fresh_server):
    tools = fresh_server.mcp._tool_manager._tools
    out = tools["list_experts"].fn(domain="compliance")
    data = json.loads(out)
    assert all(e["domain"] == "compliance" for e in data["experts"])
    assert data["count"] >= 1


def test_spending_report_empty_by_default(fresh_server):
    tools = fresh_server.mcp._tool_manager._tools
    out = tools["spending_report"].fn()
    data = json.loads(out)
    assert data["total_calls"] == 0
    assert data["by_tool"] == {}
    assert data["recent"] == []


# ── Paywalled tools: disabled mode is a transparent no-op ──────────


def test_sign_receipt_passthrough_when_disabled(fresh_server):
    """With X402_ENABLED unset, @paywalled is a no-op: sign_receipt runs
    as if undecorated. Returns a valid Signet receipt."""
    import hashlib
    tools = fresh_server.mcp._tool_manager._tools
    payload_hex = hashlib.sha256(b"test-passthrough").hexdigest()
    out = tools["sign_receipt"].fn(payload_hex=payload_hex)
    data = json.loads(out)
    assert "attestation_id" in data
    assert data["payload_sha256"] == payload_hex
    assert len(data["hmac_sha256"]) == 64  # hex SHA-256


def test_sign_receipt_rejects_bad_hex(fresh_server):
    tools = fresh_server.mcp._tool_manager._tools
    out = tools["sign_receipt"].fn(payload_hex="not-hex")
    data = json.loads(out)
    assert "error" in data


def test_verify_receipt_passthrough_when_disabled(fresh_server):
    """With X402_ENABLED unset, verify_receipt also runs as no-op.
    The 'unknown id' path is reachable (no payment gating in front)."""
    import hashlib
    tools = fresh_server.mcp._tool_manager._tools
    payload_hex = hashlib.sha256(b"verify-test").hexdigest()
    signed = json.loads(tools["sign_receipt"].fn(payload_hex=payload_hex))
    out = tools["verify_receipt"].fn(attestation_id=signed["attestation_id"])
    data = json.loads(out)
    assert data["valid"] is True
    assert data["attestation_id"] == signed["attestation_id"]


def test_verify_receipt_unknown_id(fresh_server):
    tools = fresh_server.mcp._tool_manager._tools
    out = tools["verify_receipt"].fn(attestation_id="does-not-exist")
    data = json.loads(out)
    assert "error" in data


# ── Spending log + receipt store are process-scoped (not test-polluting) ─


def test_spending_log_independent_per_import(monkeypatch):
    """Each fresh import of meok_x402 resets the rolling log — this is
    critical so CI doesn't carry state across runs. The smoke is the
    one that *uses* the log; the unit tests just assert the shape."""
    monkeypatch.delenv("X402_ENABLED", raising=False)
    if "meok_x402" in sys.modules:
        del sys.modules["meok_x402"]
    m1 = importlib.import_module("meok_x402")
    snap1 = m1.spending_snapshot()
    assert snap1["total_calls"] == 0
    # Manually record
    m1._record_paid_call("test_tool", "$0.05", "0xabcd…1234")
    snap2 = m1.spending_snapshot()
    assert snap2["total_calls"] == 1
    assert "test_tool" in snap2["by_tool"]


def test_payer_hint_handles_v1_layout():
    """The v1 PaymentPayload has the payer under payload.authorization.from.
    The keystone's _payer_hint must extract it for the spending log."""
    from meok_x402 import _payer_hint
    payment = {
        "x402Version": 1,
        "scheme": "exact",
        "network": "eip155:84532",
        "payload": {
            "authorization": {
                "from": "0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf",
                "to": "0x1111111111111111111111111111111111111111",
                "value": "50000",
            },
            "signature": "0xdeadbeef",
        },
    }
    hint = _payer_hint(payment)
    # 0x7E5F4552…5Bdf → "0x7E5F4552…5Bdf" (10 chars + ellipsis + 4 chars)
    assert hint.startswith("0x7E5F4552")
    assert hint.endswith("5Bdf")
    assert "…" in hint


def test_payer_hint_handles_legacy_layout():
    """Legacy PaymentPayload (v0) sometimes nests the address under 'from'."""
    from meok_x402 import _payer_hint
    payment = {"from": "0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf"}
    hint = _payer_hint(payment)
    assert hint.startswith("0x7E5F4552")
    assert hint.endswith("5Bdf")


# ── Free-tier rate limit (funnel-to-paid) ──────────────────────────


def test_free_tier_allows_under_limit():
    from meok_rate_limit import free_tier_check
    # 5 calls is the cap; do 5, all should pass
    for i in range(5):
        err = free_tier_check("list_experts", ctx=None, limit=5)
        assert err is None, f"call {i} should have been allowed: {err}"


def test_free_tier_blocks_at_cap():
    from meok_rate_limit import free_tier_check
    cap = 3
    for i in range(cap):
        assert free_tier_check("spending_report", ctx=None, limit=cap) is None
    err = free_tier_check("spending_report", ctx=None, limit=cap)
    assert err is not None
    assert err["code"] == 429
    assert err["limit"] == cap
    assert "reset_at_seconds" in err
    # Reset is in the future, within ~24h
    assert 0 < err["reset_at_seconds"] <= 86400


def test_paid_calls_bypass_free_tier(monkeypatch):
    """If is_paid_call() returns True (we're inside a @paywalled wrapper body),
    the rate limit should NOT trigger even at >cap usage."""
    from meok_rate_limit import free_tier_check
    # Patch is_paid_call to return True
    import meok_x402
    monkeypatch.setattr(meok_x402, "is_paid_call", lambda: True)
    # Hit the cap 10 times — all should be allowed
    for i in range(10):
        err = free_tier_check("list_experts", ctx=None, limit=2)
        assert err is None, f"paid call {i} should bypass cap: {err}"


def test_list_experts_rate_limited_at_5(fresh_server):
    """End-to-end: the wired-up @ratelimited decorator on list_experts
    actually blocks the 6th call. This is the funnel-to-paid gate."""
    tools = fresh_server.mcp._tool_manager._tools
    fn = tools["list_experts"].fn
    # 5 succeed
    for i in range(5):
        out = fn()
        data = json.loads(out)
        assert "error" not in data, f"call {i} unexpectedly blocked: {data}"
        assert data["count"] == 14
    # 6th returns 429-shaped JSON
    out = fn()
    data = json.loads(out)
    assert data["code"] == 429
    assert data["limit"] == 5
    assert "sign_receipt" in data["hint"] or "verify_receipt" in data["hint"]


def test_spending_report_has_higher_limit(fresh_server):
    """spending_report gets 20/day (observability), not 5 — agents
    auditing call volume shouldn't hit the cap on a single dashboard view."""
    tools = fresh_server.mcp._tool_manager._tools
    fn = tools["spending_report"].fn
    for i in range(20):
        out = fn()
        data = json.loads(out)
        assert "error" not in data, f"call {i} blocked at spending_report cap: {data}"
    # 21st should be blocked
    out = fn()
    data = json.loads(out)
    assert data["code"] == 429
    assert data["limit"] == 20


def test_health_effectively_unlimited(fresh_server):
    """Health is liveness — set the cap high (1000) so monitoring doesn't
    trigger rate-limit errors during a deploy / outage."""
    tools = fresh_server.mcp._tool_manager._tools
    fn = tools["health"].fn
    # 50 calls is well under the 1000/day cap
    for i in range(50):
        out = fn()
        data = json.loads(out)
        assert data["status"] == "ok", f"call {i} blocked: {data}"


def test_free_tier_snapshot_no_pii():
    """The snapshot exposed by the keystone (and via observability tools
    downstream) must not leak raw API keys — only truncated hashes."""
    from meok_rate_limit import free_tier_check, free_tier_snapshot
    free_tier_check("list_experts", ctx=None, limit=5)
    snap = free_tier_snapshot()
    # Walk every counter; none should look like an API key
    import re
    for tool, callers in snap["by_tool"].items():
        for caller in callers:
            # Real API keys are 20+ chars of high-entropy base64/hex
            assert not re.match(r"^[A-Za-z0-9_-]{32,}$", caller), \
                f"caller id {caller[:8]}… looks like an API key"
            # All we expect: 'anon' or 'auth:<16-hex>'
            assert caller == "anon" or caller.startswith("auth:")


# ── Audit anchor (tamper-evident chained hash) ──────────────────────


def test_anchor_record_emits_chain_row():
    """A single _anchor_record call returns a row with seq, prev, hash."""
    from meok_x402 import _anchor_record
    row = _anchor_record("sign_receipt", "$0.05", "0x7E5F…5Bdf")
    assert row["seq"] >= 0
    assert len(row["hash"]) == 64  # SHA-256 hex
    assert len(row["prev"]) == 64


def test_anchor_chains_via_prev_hash():
    """Two consecutive calls: row2.prev == row1.hash. The chain advances."""
    from meok_x402 import _anchor_record
    r1 = _anchor_record("sign_receipt", "$0.05", "0xA1…A1")
    r2 = _anchor_record("verify_receipt", "$0.05", "0xB2…B2")
    assert r2["prev"] == r1["hash"]
    assert r1["hash"] != r2["hash"]


def test_anchor_snapshot_exposes_head_and_tail():
    from meok_x402 import _anchor_record, audit_anchor_snapshot
    _anchor_record("sign_receipt", "$0.05", "0xA1…A1")
    snap = audit_anchor_snapshot(limit=5)
    assert "head" in snap
    assert snap["length"] >= 1
    assert isinstance(snap["tail"], list)
    # The head should match the last row's hash
    assert snap["head"] == snap["tail"][-1]["hash"]


def test_anchor_verify_round_trip():
    """Push 3 rows through, snapshot the chain, verify it. Then mutate
    one row in the snapshot — verify should fail. This is the property
    auditors care about: any tamper breaks the chain."""
    from meok_x402 import _anchor_record, audit_anchor_snapshot, audit_anchor_verify
    _anchor_record("sign_receipt", "$0.05", "0xA1…A1")
    _anchor_record("verify_receipt", "$0.05", "0xB2…B2")
    _anchor_record("sign_receipt", "$0.05", "0xC3…C3")
    snap = audit_anchor_snapshot(limit=10)
    assert audit_anchor_verify(snap["tail"]) is True
    # Tamper: change the price on row 1
    snap["tail"][1]["price"] = "$99.00"
    assert audit_anchor_verify(snap["tail"]) is False


def test_anchor_head_publishable_to_buyer():
    """A buyer can take a row and the keystone's current head and
    verify the row was anchored (a one-row check is trivial, but the
    keystone should be able to tell you the head without the chain)."""
    from meok_x402 import _anchor_record, audit_anchor_snapshot
    row = _anchor_record("sign_receipt", "$0.05", "0xA1…A1")
    snap = audit_anchor_snapshot(limit=1)
    # A one-row tail re-derives the same hash if and only if its prev is the
    # genesis anchor. This is the property: a buyer with just the keystone's
    # head and their own copy of the row can confirm anchoring.
    assert snap["tail"][-1]["hash"] == row["hash"]
    assert snap["head"] == row["hash"]


def test_audit_anchor_tool_registered(fresh_server):
    """The new free audit-anchor tool shows up in the registry."""
    tools = fresh_server.mcp._tool_manager._tools
    assert "audit_anchor" in tools
    assert "audit-anchor" in tools["audit_anchor"].description.lower() or \
           "tamper-evident" in tools["audit_anchor"].description.lower()
    # Free, not paywalled
    assert "COST WARNING" not in tools["audit_anchor"].description


def test_audit_anchor_tool_returns_chain(fresh_server):
    tools = fresh_server.mcp._tool_manager._tools
    out = tools["audit_anchor"].fn()
    data = json.loads(out)
    assert "head" in data
    assert "length" in data
    assert "tail" in data
    # Fresh process: chain starts at genesis
    assert data["head"] == "0" * 64 or len(data["head"]) == 64
