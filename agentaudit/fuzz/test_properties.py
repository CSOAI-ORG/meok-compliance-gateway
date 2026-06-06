"""Hypothesis property tests for agentaudit.

Sister to the gateway's tests/test_x402_properties.py. Covers the pure
parsing/encoding surface (no chain, no I/O) so the Fuzzing scorecard check
gets a real signal without needing a wallet.

Run:
    pip install 'agentaudit[dev]' hypothesis
    python -m pytest agentaudit/fuzz -v

CI budget: ~30s on GitHub-hosted runners (settings.max_examples=30).
"""
from __future__ import annotations

import string
from collections import Counter

from hypothesis import HealthCheck, given, settings, strategies as st

from agentaudit.bft import BFTConsensus
from agentaudit.audit_trail import AuditEntry, AuditTrail
from agentaudit.signet import SignetKey, sign_entry, verify_receipt
from agentaudit.x402 import (
    PAYMENT_META_KEY,
    PAYMENT_RESPONSE_META_KEY,
    _price_to_atomic,
    build_challenge,
    enabled,
)


# ── x402 price + challenge surface ────────────────────────────


@given(st.decimals(min_value=0, max_value=1_000_000, allow_nan=False, places=6))
def test_price_to_atomic_is_finite(price) -> None:
    """Any decimal string in the supported range must parse to a finite atomic USDC integer."""
    s = str(price)
    out = _price_to_atomic(s)
    assert out.isdigit() or (out.startswith("-") and out[1:].isdigit())
    back = int(out) / (10 ** 6)
    assert abs(float(s) - back) < 1e-6 or float(s) == back


@given(st.text(alphabet=string.ascii_letters + string.digits, min_size=1, max_size=64))
def test_build_challenge_handles_arbitrary_tool_names(tool: str) -> None:
    """Arbitrary tool names must produce a well-formed x402 challenge with the name in the resource URL."""
    import os
    # build_challenge needs X402_PAY_TO; set a placeholder so it doesn't KeyError.
    # The exact pay_to value is asserted separately in test_x402.py.
    os.environ["X402_PAY_TO"] = "0xtest"
    ch = build_challenge(tool, "$0.10")
    assert ch["x402Version"] == 1
    assert ch["resource"]["url"] == f"mcp://tool/{tool}"
    acc = ch["accepts"][0]
    assert acc["amount"] == "100000"            # $0.10 → 100000 atomic
    assert acc["scheme"] == "exact"
    assert isinstance(acc["network"], str) and acc["network"].startswith("eip155:")
    assert acc["payTo"] == "0xtest"


@given(st.sampled_from(["1", "true", "yes", "on", "TRUE", "Yes", "0", "", "false", "no", "off", "nope", " "]))
def test_enabled_truthy_set_is_exact(value: str) -> None:
    """`enabled()` must accept exactly the truthy set documented in x402.py."""
    import os
    os.environ["X402_ENABLED"] = value
    expected = value.strip().lower() in ("1", "true", "yes", "on")
    assert enabled() is expected


@given(st.dictionaries(keys=st.sampled_from([PAYMENT_META_KEY, PAYMENT_RESPONSE_META_KEY, "unrelated"]),
                       values=st.text(max_size=64), max_size=3))
def test_meta_keys_are_documented_constants(meta: dict) -> None:
    """The on-the-wire meta keys must NOT drift across releases."""
    assert PAYMENT_META_KEY == "x402/payment"
    assert PAYMENT_RESPONSE_META_KEY == "x402/payment-response"
    assert isinstance(meta, dict)


# ── BFT tally invariants ─────────────────────────────────────


@given(st.lists(st.tuples(st.text(min_size=1, max_size=8), st.text(min_size=1, max_size=16)),
                min_size=1, max_size=20),
       st.integers(min_value=1, max_value=11))
def test_bft_quorum_is_correct(votes, total_nodes: int) -> None:
    """quorum = 2f+1 where f = floor((n-1)/3). consensus_reached ↔ #top-hash ≥ quorum."""
    bft = BFTConsensus(round_id=1, total_nodes=total_nodes)
    expected_quorum = 2 * ((total_nodes - 1) // 3) + 1
    assert bft.quorum == expected_quorum

    for node_id, h in votes:
        bft.vote(node_id, h)

    # BFT tracks node_id → vote_hash, so each node can only vote once.
    # Count votes by hash, mirroring the production `consensus_reached` / `majority_hash` logic.
    tallies = Counter(bft.votes.values())
    if tallies:
        top_hash, top_count = tallies.most_common(1)[0]
        if top_count >= expected_quorum:
            assert bft.consensus_reached is True
            assert bft.majority_hash == top_hash
        else:
            assert bft.consensus_reached is False


# ── Signet Ed25519 / HMAC round-trip ──────────────────────────


@given(st.text(min_size=1, max_size=128))
def test_signet_sign_verify_roundtrip(message: str) -> None:
    """Sign-then-verify must succeed for any non-empty message; a flipped byte must fail."""
    key = SignetKey()
    msg = message.encode("utf-8")
    sig = key.sign(msg)
    assert key.verify(msg, sig) is True
    # A flipped byte must fail verification.
    tampered = msg[:-1] + (b"x" if msg[-1:] != b"x" else b"y") + msg[-1:]
    assert key.verify(tampered, sig) is False


@given(st.text(min_size=1, max_size=64),
       st.text(min_size=1, max_size=64))
def test_signet_receipt_roundtrip(entry_hash: str, did: str) -> None:
    """sign_entry → verify_receipt must round-trip, with entry_hash recoverable from the wire format."""
    key = SignetKey(did=did)
    receipt = sign_entry(entry_hash, key)
    assert receipt.entry_hash == entry_hash
    assert receipt.signer_did == did
    assert verify_receipt(receipt, key) is True
    # The wire JSON escapes non-printable chars (e.g. \x1f → ), so the
    # raw entry_hash won't appear verbatim. Decode and compare structurally.
    import json as _json
    payload = _json.loads(receipt.to_json())
    assert payload["entry_hash"] == entry_hash


# ── Audit trail integrity (parent_hash chain) ────────────────


@given(st.lists(st.tuples(st.text(min_size=1, max_size=8), st.text(min_size=1, max_size=8), st.text(min_size=1, max_size=16)),
                min_size=1, max_size=8))
def test_audit_trail_chain_intact_after_random_appends(entries) -> None:
    """A fresh audit trail with N appended entries in order must verify as intact."""
    trail = AuditTrail()
    for i, (src, tgt, action) in enumerate(entries):
        e = AuditEntry(
            entry_id=f"e{i}",
            timestamp="",
            protocol="a2a",
            source_agent=src,
            target_agent=tgt,
            action=action,
            payload_hash=f"hash{i}",
        )
        trail.append(e)
    assert len(trail) == len(entries)
    assert trail.verify() == [], "freshly-built trail must verify clean"


@given(st.lists(st.text(min_size=1, max_size=8), min_size=2, max_size=8),
       st.integers(min_value=0, max_value=6))
def test_audit_trail_tamper_detection(actions, tamper_index: int) -> None:
    """Mutating any non-last entry must break the next entry's parent_hash, which verify() detects.

    The last entry has no successor, so chain-only verify cannot detect tampering
    on it (a real-world deployment pairs the chain with a Signet signature on each
    entry; that's covered by `test_audit_chain_with_signet` in test_agentaudit.py).
    """
    trail = AuditTrail()
    for i, action in enumerate(actions):
        e = AuditEntry(
            entry_id=f"e{i}",
            timestamp="",
            protocol="a2a",
            source_agent="a",
            target_agent="b",
            action=action,
            payload_hash=f"hash{i}",
        )
        trail.append(e)
    # Tamper with any non-last entry; the next entry's parent_hash will mismatch.
    idx = tamper_index % (len(trail._chain) - 1)
    trail._chain[idx].action = "tampered"
    broken = trail.verify()
    assert len(broken) >= 1, "tamper must be detected via broken parent_hash"


# ── Hypothesis profile for CI ────────────────────────────────


settings.register_profile(
    "ci",
    max_examples=30,
    deadline=2_000,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.data_too_large],
)
settings.load_profile("ci")
