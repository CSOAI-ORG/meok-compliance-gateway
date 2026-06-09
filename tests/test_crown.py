"""Tests for meok_crown.py — the sigil seal + Ed25519 root-of-trust.

Run: python3.11 -m pytest tests/test_crown.py -q
Covers: round-trip, tamper, wrong-key, validity window, revocation policy,
chain-of-trust (incl. forgery attempt), BFT quorum math, MEOK-SOV token interop.
"""
import base64
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import meok_crown as crown  # noqa: E402

T0 = "2026-08-01T12:00:00+00:00"


def _root_registry():
    seed, pub = crown.gen_keypair()
    reg = crown.KeyRegistry()
    reg.register(crown.KeyEntry(kid="root-v1", public_key=pub, role="root"))
    return seed, pub, reg


# ── basic seal/verify ─────────────────────────────────────────────────────────
def test_seal_verify_roundtrip():
    seed, _, reg = _root_registry()
    sigil = crown.seal({"claim": "high-risk-ok"}, seed=seed, kid="root-v1", ts=T0)
    v = crown.verify_sigil(sigil, reg)
    assert v.valid and v.role == "root", v.reason


def test_tampered_payload_rejected():
    seed, _, reg = _root_registry()
    sigil = crown.seal({"claim": "ok"}, seed=seed, kid="root-v1", ts=T0)
    sigil["payload"]["claim"] = "tampered"
    assert not crown.verify_sigil(sigil, reg).valid


def test_wrong_key_rejected():
    seed, _, reg = _root_registry()
    other_seed, _ = crown.gen_keypair()
    sigil = crown.seal({"claim": "ok"}, seed=other_seed, kid="root-v1", ts=T0)
    assert not crown.verify_sigil(sigil, reg).valid  # kid says root-v1, signed by other


def test_unknown_kid_rejected():
    seed, _, reg = _root_registry()
    sigil = crown.seal({"x": 1}, seed=seed, kid="ghost-v9", ts=T0)
    v = crown.verify_sigil(sigil, reg)
    assert not v.valid and "unknown kid" in v.reason


# ── rotation / validity windows ───────────────────────────────────────────────
def test_validity_window():
    seed, pub = crown.gen_keypair()
    reg = crown.KeyRegistry()
    reg.register(crown.KeyEntry(
        kid="root-v2", public_key=pub, role="root",
        valid_from="2026-08-01T00:00:00+00:00", valid_to="2027-08-01T00:00:00+00:00",
    ))
    inside = crown.seal({"x": 1}, seed=seed, kid="root-v2", ts=T0)
    before = crown.seal({"x": 1}, seed=seed, kid="root-v2", ts="2026-07-01T00:00:00+00:00")
    after = crown.seal({"x": 1}, seed=seed, kid="root-v2", ts="2027-09-01T00:00:00+00:00")
    assert crown.verify_sigil(inside, reg).valid
    assert not crown.verify_sigil(before, reg).valid
    assert not crown.verify_sigil(after, reg).valid


# ── revocation policy: compromise = retroactive, rotation = prospective ───────
def test_revocation_compromise_is_retroactive():
    seed, pub = crown.gen_keypair()
    reg = crown.KeyRegistry()
    reg.register(crown.KeyEntry(
        kid="root-v1", public_key=pub, role="root", status="revoked",
        revocation={"effective": "2026-09-01T00:00:00+00:00", "reason": "suspected key compromise"},
    ))
    # signed BEFORE the effective date but compromise → still rejected
    sigil = crown.seal({"x": 1}, seed=seed, kid="root-v1", ts=T0)
    assert not crown.verify_sigil(sigil, reg).valid


def test_revocation_rotation_is_prospective():
    seed, pub = crown.gen_keypair()
    reg = crown.KeyRegistry()
    reg.register(crown.KeyEntry(
        kid="root-v1", public_key=pub, role="root", status="revoked",
        revocation={"effective": "2026-09-01T00:00:00+00:00", "reason": "routine rotation"},
    ))
    pre = crown.seal({"x": 1}, seed=seed, kid="root-v1", ts=T0)            # before effective
    post = crown.seal({"x": 1}, seed=seed, kid="root-v1", ts="2026-10-01T00:00:00+00:00")
    assert crown.verify_sigil(pre, reg).valid       # old attestations still valid
    assert not crown.verify_sigil(post, reg).valid  # nothing new after rotation


# ── chain-of-trust ────────────────────────────────────────────────────────────
def test_chain_walks_to_crown():
    root_seed, _, reg = _root_registry()
    hive_seed, hive_pub = crown.gen_keypair()
    cert = crown.seal(
        {"hive_kid": "hive:meok-v1", "hive_public_key": base64.b64encode(hive_pub).decode()},
        seed=root_seed, kid="root-v1", ts=T0,
    )
    attestation = crown.seal({"claim": "audit-passed"}, seed=hive_seed, kid="hive:meok-v1", ts=T0)
    v = crown.verify_chain(attestation, cert, reg)
    assert v.valid and v.role == "hive", v.reason


def test_hive_cannot_forge_root():
    """A hive cert NOT sealed by a root key must not grant lineage."""
    root_seed, _, reg = _root_registry()
    rogue_seed, rogue_pub = crown.gen_keypair()
    # rogue self-signs a "cert" with its own (non-root) key
    reg.register(crown.KeyEntry(kid="hive:rogue", public_key=rogue_pub, role="hive"))
    fake_cert = crown.seal(
        {"hive_kid": "hive:rogue", "hive_public_key": base64.b64encode(rogue_pub).decode()},
        seed=rogue_seed, kid="hive:rogue", ts=T0,
    )
    att = crown.seal({"claim": "x"}, seed=rogue_seed, kid="hive:rogue", ts=T0)
    v = crown.verify_chain(att, fake_cert, reg)
    assert not v.valid and "not sealed by a root" in v.reason


# ── council revocation (BFT quorum) ───────────────────────────────────────────
def test_bft_quorum_math():
    assert crown.bft_quorum(33) == 21   # f=10
    assert crown.bft_quorum(4) == 3     # f=1
    assert crown.bft_quorum(1) == 1


def test_revocation_needs_quorum():
    seats = 33
    members = {f"c{i}": crown.gen_keypair() for i in range(seats)}
    council = {mid: pub for mid, (seed, pub) in members.items()}
    body = {"kid": "root-v1", "effective": T0, "reason": "suspected key compromise"}
    msg = crown._canonical(body)

    def signed_by(n):
        rec = dict(body)
        rec["signatures"] = {
            mid: base64.b64encode(
                crown.Ed25519PrivateKey.from_private_bytes(seed).sign(msg)
            ).decode()
            for mid, (seed, pub) in list(members.items())[:n]
        }
        return rec

    assert not crown.verify_revocation(signed_by(20), council, seats=seats)  # below 21
    assert crown.verify_revocation(signed_by(21), council, seats=seats)      # quorum met


def test_revocation_rejects_forged_signature():
    seats = 4
    members = {f"c{i}": crown.gen_keypair() for i in range(seats)}
    council = {mid: pub for mid, (seed, pub) in members.items()}
    rec = {"kid": "root-v1", "effective": T0, "reason": "compromise",
           "signatures": {mid: base64.b64encode(b"\x00" * 64).decode() for mid in council}}
    assert not crown.verify_revocation(rec, council, seats=seats)  # all sigs bogus


# ── MEOK-SOV token interop (separate layer) ───────────────────────────────────
def test_is_sov_token():
    assert crown.is_sov_token("MEOK-SOV-abc123")
    assert crown.is_sov_token("Bearer MEOK-SOV-abc123")
    assert not crown.is_sov_token("Bearer eyJhbGci...")
    assert not crown.is_sov_token(None)


def test_bind_sov_token_hashes_not_embeds():
    bound = crown.bind_sov_token({"claim": "x"}, "MEOK-SOV-secret")
    assert "MEOK-SOV-secret" not in str(bound)         # raw token never embedded
    assert len(bound["sov_token_sha256"]) == 64        # just its hash
