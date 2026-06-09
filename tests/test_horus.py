"""Tests for meok_horus.py — the HORUS Art. 12 ledger (hash-chained + sigil-sealed).

Run: python3.11 -m pytest tests/test_horus.py -q
Proves: append/verify round-trip, tamper detection (event + hash + sigil),
order/forgery rejection, JSONL persistence round-trip, empty-ledger validity.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import meok_crown as crown   # noqa: E402
import meok_horus as horus   # noqa: E402

T0 = "2026-08-01T12:00:00+00:00"


def _setup():
    seed, pub = crown.gen_keypair()
    reg = crown.KeyRegistry()
    reg.register(crown.KeyEntry(kid="root-v1", public_key=pub, role="root"))
    return seed, reg


def _filled(seed, n=3):
    lg = horus.Ledger()
    for i in range(n):
        lg.append({"event": "agent_action", "i": i}, seed=seed, kid="root-v1", ts=T0)
    return lg


def test_append_and_verify():
    seed, reg = _setup()
    lg = _filled(seed, 3)
    r = lg.verify(reg)
    assert r.valid and r.checked == 3, r.reason


def test_chain_links():
    seed, _ = _setup()
    lg = _filled(seed, 3)
    assert lg.entries[0].prev_hash == horus.GENESIS_PREV
    assert lg.entries[1].prev_hash == lg.entries[0].entry_hash
    assert lg.entries[2].prev_hash == lg.entries[1].entry_hash


def test_empty_ledger_is_valid():
    _, reg = _setup()
    assert horus.Ledger().verify(reg).valid


def test_tampered_event_detected():
    seed, reg = _setup()
    lg = _filled(seed, 3)
    lg.entries[1].event["i"] = 999          # mutate a past entry
    r = lg.verify(reg)
    assert not r.valid and r.broken_at == 1


def test_tampered_hash_detected():
    seed, reg = _setup()
    lg = _filled(seed, 3)
    lg.entries[0].entry_hash = "f" * 64     # break the first link
    r = lg.verify(reg)
    assert not r.valid and r.broken_at in (0, 1)


def test_forged_sigil_detected():
    seed, reg = _setup()
    other_seed, _ = crown.gen_keypair()
    lg = _filled(seed, 2)
    # re-seal entry 1 with a non-crown key but keep kid=root-v1
    e = lg.entries[1]
    e.sigil = crown.seal(
        {"seq": e.seq, "prev_hash": e.prev_hash, "event": e.event, "entry_hash": e.entry_hash},
        seed=other_seed, kid="root-v1", ts=e.ts,
    )
    r = lg.verify(reg)
    assert not r.valid and r.broken_at == 1


def test_sigil_relocation_detected():
    """A valid sigil from a DIFFERENT entry can't be pasted in (entry_hash binds it)."""
    seed, reg = _setup()
    lg = _filled(seed, 3)
    lg.entries[2].sigil = lg.entries[1].sigil   # paste entry 1's (valid) sigil onto entry 2
    r = lg.verify(reg)
    assert not r.valid and r.broken_at == 2


def test_jsonl_roundtrip():
    seed, reg = _setup()
    lg = _filled(seed, 4)
    restored = horus.Ledger.from_jsonl(lg.to_jsonl())
    assert restored.verify(reg).valid
    assert restored.head_hash == lg.head_hash
