"""meok_horus.py — the Oversight Plane ledger (HORUS), buildable slice.

Implements `oversight.ledger_append` from HORUS_OVERSIGHT_PLANE_SPEC.md — the
EU AI Act **Article 12** record-keeping function — wiring meok_crown.seal()
into a real attestation path. Each oversight event is:

  1. **hash-chained** to the previous entry (tamper-evident: change any past
     entry and every subsequent entry_hash breaks), AND
  2. **sigil-sealed** by the crown (origin is provable and chains to the root;
     a forged entry fails Ed25519 verification).

Hash chain alone proves *integrity of order*; the sigil proves *who wrote it*.
Together they are the Article-12 immutable log the realm's hives feed into.

Pure stdlib + meok_crown. No network. Append-only; persistence is JSONL.
"""
from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import meok_crown as crown

GENESIS_PREV = "0" * 64


def _canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _entry_hash(seq: int, prev_hash: str, event, ts: str) -> str:
    """sha256 over the chained tuple — the link that makes tampering detectable."""
    h = hashlib.sha256()
    h.update(_canonical({"seq": seq, "prev_hash": prev_hash, "event": event, "ts": ts}))
    return h.hexdigest()


@dataclass
class LedgerEntry:
    seq: int
    prev_hash: str
    event: dict
    ts: str
    entry_hash: str
    sigil: dict                 # crown.seal() over {seq, prev_hash, event, entry_hash}

    def to_dict(self) -> dict:
        return {
            "seq": self.seq, "prev_hash": self.prev_hash, "event": self.event,
            "ts": self.ts, "entry_hash": self.entry_hash, "sigil": self.sigil,
        }


@dataclass
class VerifyResult:
    valid: bool
    reason: str
    checked: int = 0
    broken_at: Optional[int] = None


@dataclass
class Ledger:
    """Append-only, hash-chained, sigil-sealed oversight ledger (HORUS Art. 12)."""

    entries: list = field(default_factory=list)

    @property
    def head_hash(self) -> str:
        return self.entries[-1].entry_hash if self.entries else GENESIS_PREV

    def append(self, event: dict, *, seed: bytes, kid: str, ts: Optional[str] = None) -> LedgerEntry:
        """Append an oversight event: chain it, then seal the chained entry."""
        seq = len(self.entries)
        prev = self.head_hash
        ts = ts or _now_iso()
        eh = _entry_hash(seq, prev, event, ts)
        sigil = crown.seal(
            {"seq": seq, "prev_hash": prev, "event": event, "entry_hash": eh},
            seed=seed, kid=kid, ts=ts,
        )
        entry = LedgerEntry(seq=seq, prev_hash=prev, event=event, ts=ts, entry_hash=eh, sigil=sigil)
        self.entries.append(entry)
        return entry

    def verify(self, registry: "crown.KeyRegistry") -> VerifyResult:
        """Walk the whole chain: every link must hold AND every sigil must verify."""
        prev = GENESIS_PREV
        for i, e in enumerate(self.entries):
            if e.seq != i:
                return VerifyResult(False, f"seq out of order at {i}", checked=i, broken_at=i)
            if e.prev_hash != prev:
                return VerifyResult(False, f"chain break: prev_hash mismatch at {i}", checked=i, broken_at=i)
            if _entry_hash(e.seq, e.prev_hash, e.event, e.ts) != e.entry_hash:
                return VerifyResult(False, f"tampered entry at {i} (hash mismatch)", checked=i, broken_at=i)
            v = crown.verify_sigil(e.sigil, registry)
            if not v.valid:
                return VerifyResult(False, f"bad sigil at {i}: {v.reason}", checked=i, broken_at=i)
            # the sigil must seal THIS entry, not some other one
            p = e.sigil["payload"]
            if p.get("entry_hash") != e.entry_hash or p.get("seq") != e.seq:
                return VerifyResult(False, f"sigil/entry mismatch at {i}", checked=i, broken_at=i)
            prev = e.entry_hash
        return VerifyResult(True, "ledger intact", checked=len(self.entries))

    # ── persistence (append-only JSONL) ──────────────────────────────────────
    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(e.to_dict(), sort_keys=True) for e in self.entries)

    @classmethod
    def from_jsonl(cls, text: str) -> "Ledger":
        ledger = cls()
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            ledger.entries.append(LedgerEntry(
                seq=d["seq"], prev_hash=d["prev_hash"], event=d["event"],
                ts=d["ts"], entry_hash=d["entry_hash"], sigil=d["sigil"],
            ))
        return ledger
