"""Tamper-evident audit trail for every agent-to-agent interaction."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Any


def _now() -> str:
    return f"{time.time():.6f}"


def _canonical(obj: Any) -> str:
    """Deterministic JSON canonicalisation for hashing."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)


@dataclass
class AuditEntry:
    entry_id: str           # UUIDv4
    timestamp: str          # Unix epoch with micros
    protocol: str           # "a2a" | "mcp" | "anp"
    source_agent: str       # did or url
    target_agent: str       # did or url
    action: str             # tool name / task id / message type
    payload_hash: str       # SHA-256 of canonicalised payload
    compliance_checks: list[str] = field(default_factory=list)
    result: str = "pending"  # "pass" | "fail" | "pending"
    parent_hash: str = ""   # previous entry hash for chain integrity
    signature: str = ""     # placeholder for future Ed25519 sig

    def compute_hash(self) -> str:
        """Return SHA-256 of this entry (excluding its own hash field)."""
        blob = _canonical(asdict(self))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class AuditTrail:
    """In-memory append-only audit log with hash chaining.
    Production should swap this for an immutable store (IPFS, Arweave, S3+WORM).
    """

    def __init__(self) -> None:
        self._chain: list[AuditEntry] = []
        self._last_hash: str = "0" * 64

    def append(self, entry: AuditEntry) -> str:
        entry.timestamp = _now()
        entry.parent_hash = self._last_hash
        entry_hash = entry.compute_hash()
        self._chain.append(entry)
        self._last_hash = entry_hash
        return entry_hash

    def verify(self) -> list[str]:
        """Return list of entry IDs whose hash chain is broken."""
        broken: list[str] = []
        prev = "0" * 64
        for e in self._chain:
            if e.parent_hash != prev:
                broken.append(e.entry_id)
            recomputed = e.compute_hash()
            # In a real chain we'd store the hash separately; here we re-verify continuity
            prev = recomputed
        return broken

    def to_json(self) -> str:
        return json.dumps([asdict(e) for e in self._chain], indent=2, default=str)

    def __len__(self) -> int:
        return len(self._chain)
