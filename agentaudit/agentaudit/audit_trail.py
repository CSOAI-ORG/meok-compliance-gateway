"""Tamper-evident audit trail for every agent-to-agent interaction.

Aligned with OpenMoE-BFT Empire Layer 9 (Audit & Receipts):
- Hash chaining (Merkle-style continuity)
- Signet Ed25519 signatures per entry
- BFT consensus metadata per entry
- Blockchain anchoring hash
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from typing import Any

from .signet import SignetKey, SignetReceipt, sign_entry
from .bft import BFTConsensus


def _now() -> str:
    return f"{time.time():.6f}"


def _canonical(obj: Any) -> str:
    """Deterministic JSON canonicalisation for hashing."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)


@dataclass
class AuditEntry:
    """A single audit entry with Signet signing and BFT consensus."""
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
    signet_receipt: SignetReceipt | None = None
    bft_consensus: BFTConsensus | None = None
    blockchain_anchor: str = ""   # e.g. IPFS CID or Arweave txid

    def compute_hash(self) -> str:
        """Return SHA-256 of this entry (excluding its own hash field)."""
        blob = _canonical(asdict(self))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class AuditTrail:
    """In-memory append-only audit log with hash chaining, Signet signatures,
    and optional BFT consensus metadata.
    Production should swap this for an immutable store (IPFS, Arweave, S3+WORM).
    """

    def __init__(self, signet_key: SignetKey | None = None) -> None:
        self._chain: list[AuditEntry] = []
        self._last_hash: str = "0" * 64
        self._key = signet_key

    def append(
        self,
        entry: AuditEntry,
        co_key: SignetKey | None = None,
    ) -> str:
        entry.timestamp = _now()
        entry.parent_hash = self._last_hash
        entry_hash = entry.compute_hash()

        # Signet signature
        if self._key is not None:
            entry.signet_receipt = sign_entry(
                entry_hash, self._key, co_key=co_key,
                blockchain_anchor=entry.blockchain_anchor or None,
            )

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
            prev = recomputed
        return broken

    def verify_signatures(self, key: SignetKey) -> list[str]:
        """Return list of entry IDs with invalid Signet receipts."""
        invalid: list[str] = []
        for e in self._chain:
            if e.signet_receipt is None:
                continue
            from .signet import verify_receipt
            if not verify_receipt(e.signet_receipt, key):
                invalid.append(e.entry_id)
        return invalid

    def to_json(self) -> str:
        return json.dumps([asdict(e) for e in self._chain], indent=2, default=str)

    def __len__(self) -> int:
        return len(self._chain)
