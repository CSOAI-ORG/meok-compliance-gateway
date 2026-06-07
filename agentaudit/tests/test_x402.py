"""Tests for agentaudit.x402 — runnable without a wallet/chain.

    pip install x402 && python -m pytest tests/test_x402.py -v

Covers the deterministic, money-free paths:
  - DISABLED  → @paywalled is a transparent no-op (free self-host unaffected)
  - ENABLED   → correct x402 challenge JSON + unpaid calls are gated before the tool runs
  - ENABLED + paid (mocked facilitator) → tool body runs, _paid_call contextvar flips
  - Settle failure does not break the paid call (best-effort log, return result)
  - is_paid_call() contextvar is scoped (resets between calls)
  - Decorator idempotency: stacking @paywalled twice is safe (passthrough when disabled)

The verify/settle path that touches a real facilitator needs a funded wallet and is
exercised in staging, not here.
"""
from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

import pytest


# ── DISABLED path ───────────────────────────────────────────────


def test_disabled_is_noop(x402_disabled) -> None:
    """@paywalled must be a transparent passthrough when X402_ENABLED is unset."""
    def my_tool(x):
        return {"ok": x}

    wrapped = x402_disabled.paywalled(price="$0.25")(my_tool)
    assert wrapped is my_tool, "disabled must return the original function unchanged"
    assert wrapped("hello") == {"ok": "hello"}


def test_disabled_is_paid_call_false(x402_disabled) -> None:
    assert x402_disabled.is_paid_call() is False


# ── ENABLED challenge shape + price math ────────────────────────


def test_challenge_shape_and_price_math(x402_enabled) -> None:
    m = x402_enabled
    ch = m.build_challenge("scan_shadow_agents", "$0.10")
    acc = ch["accepts"][0]
    assert ch["x402Version"] == 1
    assert ch["resource"]["url"] == "mcp://tool/scan_shadow_agents"
    assert acc["scheme"] == "exact" and acc["network"] == "eip155:8453"
    assert acc["amount"] == "100000", acc["amount"]            # $0.10 → 100000 atomic USDC (6dp)
    assert acc["payTo"].endswith("dEaD")
    assert acc["asset"].lower().startswith("0x833589fc")        # USDC on Base mainnet
    # Price-math edge cases
    assert m._price_to_atomic("$1") == "1000000"
    assert m._price_to_atomic("0.005") == "5000"
    assert m._price_to_atomic("$0.001") == "1000"


def test_challenge_invalid_price_raises(x402_enabled) -> None:
    m = x402_enabled
    with pytest.raises(ValueError, match="dollar amount"):
        m._price_to_atomic("not-a-number")


# ── ENABLED unpaid call is gated ────────────────────────────────


class _FakeMeta(SimpleNamespace):
    pass


class _FakeParams(SimpleNamespace):
    pass


class _FakeRequest(SimpleNamespace):
    pass


class _FakeRequestContext(SimpleNamespace):
    pass


def _ctx_with_meta(meta: dict[str, Any] | None = None):
    """Build a duck-typed FastMCP Context whose _meta is `meta` (or empty)."""
    params = _FakeParams(meta=meta or {})
    request = _FakeRequest(params=params)
    rc = _FakeRequestContext(request=request)
    return SimpleNamespace(request_context=rc)


def test_unpaid_call_is_gated(x402_enabled) -> None:
    """No _meta['x402/payment'] → tool body must NOT run, must raise ToolError with the challenge."""
    from mcp.server.fastmcp.exceptions import ToolError

    m = x402_enabled
    ran = {"v": False}

    def scan_shadow_agents(candidate_urls, ctx):
        ran["v"] = True
        return {"ran": True}

    wrapped = m.paywalled(price="$0.10", tool_name="scan_shadow_agents")(scan_shadow_agents)

    ctx = _ctx_with_meta(meta={})  # no payment
    with pytest.raises(ToolError) as ei:
        wrapped("https://example.com\nhttps://other.com", ctx=ctx)
    envelope = json.loads(str(ei.value))
    assert m.PAYMENT_RESPONSE_META_KEY in envelope
    assert envelope[m.PAYMENT_RESPONSE_META_KEY]["accepts"][0]["amount"] == "100000"
    assert ran["v"] is False, "tool body must NOT run when unpaid"
    assert m.is_paid_call() is False


def test_unpaid_call_without_ctx(x402_enabled) -> None:
    """If FastMCP somehow didn't inject ctx, the tool must still raise (not silently run)."""
    from mcp.server.fastmcp.exceptions import ToolError

    m = x402_enabled

    def tool():
        return "ran"

    wrapped = m.paywalled(price="$0.10", tool_name="t")(tool)
    with pytest.raises(ToolError):
        wrapped()


# ── ENABLED + paid path (mocked facilitator) ───────────────────


class _FakeVerify:
    def __init__(self, is_valid: bool, reason: str | None = None):
        self.is_valid = is_valid
        self.invalid_reason = reason


class _FakeResourceServer:
    """Mock x402ResourceServerSync — no chain calls, no web3 import."""

    def __init__(self, *, verify: _FakeVerify, settle_raises: bool = False):
        self._verify = verify
        self._settle_raises = settle_raises
        self.settle_calls: list[Any] = []
        self.verify_calls = 0

    def find_matching_requirements(self, accepts, payment):  # noqa: ARG002
        return accepts  # any payment matches

    def verify_payment(self, payment, reqs):  # noqa: ARG002
        self.verify_calls += 1
        return self._verify

    def settle_payment(self, payment, reqs):  # noqa: ARG002
        self.settle_calls.append((payment, reqs))
        if self._settle_raises:
            raise RuntimeError("simulated settle failure")


def test_paid_call_runs_body_and_flips_contextvar(x402_enabled, monkeypatch) -> None:
    """Valid payment → tool body runs, is_paid_call()=True during the call, then resets."""
    m = x402_enabled
    fake = _FakeResourceServer(verify=_FakeVerify(is_valid=True))
    monkeypatch.setattr(m, "_resource_server", lambda: fake)

    observed: list[bool] = []

    def audit_report(system, ctx):
        observed.append(m.is_paid_call())
        return {"ok": True, "system": system}

    wrapped = m.paywalled(price="$0.10", tool_name="audit_report")(audit_report)
    ctx = _ctx_with_meta(meta={m.PAYMENT_META_KEY: {"fake": "signed-payment"}})

    result = wrapped("acme", ctx=ctx)
    assert result == {"ok": True, "system": "acme"}
    assert fake.verify_calls == 1
    assert len(fake.settle_calls) == 1, "settle must be called once for a verified paid call"
    assert observed == [True], "is_paid_call() must be True while the tool body runs"
    assert m.is_paid_call() is False, "contextvar must reset after the call"


def test_settle_failure_does_not_break_call(x402_enabled, monkeypatch) -> None:
    """Settle errors are logged + swallowed (best-effort) — the call must still return the body result."""
    m = x402_enabled
    fake = _FakeResourceServer(verify=_FakeVerify(is_valid=True), settle_raises=True)
    monkeypatch.setattr(m, "_resource_server", lambda: fake)

    def tool(system, ctx):
        return {"ok": True, "system": system}

    wrapped = m.paywalled(price="$0.10", tool_name="tool")(tool)
    ctx = _ctx_with_meta(meta={m.PAYMENT_META_KEY: {"fake": "signed"}})
    # Should NOT raise — the call still returns.
    result = wrapped("x", ctx=ctx)
    assert result == {"ok": True, "system": "x"}


def test_invalid_payment_is_gated(x402_enabled, monkeypatch) -> None:
    """Verifier says is_valid=False → re-issue the challenge (don't run the body, don't call settle)."""
    from mcp.server.fastmcp.exceptions import ToolError

    m = x402_enabled
    fake = _FakeResourceServer(verify=_FakeVerify(is_valid=False, reason="bad signature"))
    monkeypatch.setattr(m, "_resource_server", lambda: fake)

    ran = {"v": False}

    def tool(system, ctx):
        ran["v"] = True
        return {"ok": True}

    wrapped = m.paywalled(price="$0.10", tool_name="tool")(tool)
    ctx = _ctx_with_meta(meta={m.PAYMENT_META_KEY: {"fake": "tampered"}})
    with pytest.raises(ToolError):
        wrapped("x", ctx=ctx)
    assert ran["v"] is False
    assert fake.settle_calls == [], "settle must NOT run for an invalid payment"


def test_billing_path_failure_fails_open(x402_enabled, monkeypatch) -> None:
    """If the x402 machinery itself errors (e.g. facilitator down), call still runs (fail-open).

    This is the safety property: a billing outage must not lock paying customers out of
    the actual tool. (Free self-host is unaffected because X402_ENABLED is unset.)
    """
    m = x402_enabled

    def boom():
        raise RuntimeError("facilitator unreachable")

    monkeypatch.setattr(m, "_resource_server", boom)

    def tool(system, ctx):
        return {"ran": True, "system": system}

    wrapped = m.paywalled(price="$0.10", tool_name="tool")(tool)
    ctx = _ctx_with_meta(meta={m.PAYMENT_META_KEY: {"fake": "x"}})
    result = wrapped("x", ctx=ctx)
    assert result == {"ran": True, "system": "x"}


# ── Decorator metadata / idempotency ────────────────────────────


def test_decorator_preserves_name_and_doc(x402_enabled) -> None:
    m = x402_enabled

    def scan_shadow_agents(candidate_urls, ctx):
        """Probe URLs."""
        return []

    wrapped = m.paywalled(price="$0.10", tool_name="scan_shadow_agents")(scan_shadow_agents)
    assert wrapped.__name__ == "scan_shadow_agents"
    assert wrapped.__doc__ == "Probe URLs."


def test_decorator_disabled_idempotent(x402_disabled) -> None:
    """Stacking @paywalled twice when disabled is safe (both layers are no-ops)."""
    m = x402_disabled

    def t(x, ctx=None):
        return x * 2

    once = m.paywalled(price="$0.10")(t)
    twice = m.paywalled(price="$0.10")(once)
    # When disabled, the OUTER decorator returns its argument unchanged — so twice is `once`.
    assert twice is once
    assert twice("hi") == "hihi"


# ── ctx extraction robustness ───────────────────────────────────


def test_ctx_can_be_positional(x402_enabled, monkeypatch) -> None:
    """@paywalled should find the FastMCP ctx whether passed by kwarg or position."""

    m = x402_enabled
    fake = _FakeResourceServer(verify=_FakeVerify(is_valid=True))
    monkeypatch.setattr(m, "_resource_server", lambda: fake)

    called = {"v": False}

    def tool(system, ctx):
        called["v"] = True
        return {"ok": True}

    wrapped = m.paywalled(price="$0.10", tool_name="tool")(tool)
    ctx = _ctx_with_meta(meta={m.PAYMENT_META_KEY: {"fake": "x"}})
    # Positional ctx
    result = wrapped("acme", ctx)
    assert result == {"ok": True}
    assert called["v"] is True


# ── META key constants (spec pin) ──────────────────────────────


def test_meta_keys_are_spec_correct(x402_disabled) -> None:
    """Pin the on-the-wire meta keys so we don't drift from the x402-over-MCP convention."""
    m = x402_disabled
    assert m.PAYMENT_META_KEY == "x402/payment"
    assert m.PAYMENT_RESPONSE_META_KEY == "x402/payment-response"
