"""Signet — Ed25519 cryptographic receipts for audit trails.

Aligned with OpenMoE-BFT Empire Layer 9 (Audit & Receipts).
Provides hash-chained, bilaterally co-signed receipts that can be
verified offline and anchored to a blockchain.

Lazy import of pynacl: if unavailable the module falls back to
HMAC-SHA256 (still tamper-evident, but not Signet-spec compliant).
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from typing import Any


def _has_nacl() -> bool:
    try:
        import nacl.signing  # type: ignore[import-untyped]
        return True
    except Exception:
        return False


@dataclass
class SignetReceipt:
    """A cryptographic receipt for a single audit entry."""
    entry_hash: str
    signer_did: str
    signature_hex: str
    scheme: str          # "ed25519" or "hmac-sha256"
    co_signer_did: str | None = None
    co_signature_hex: str | None = None
    blockchain_anchor: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_hash": self.entry_hash,
            "signer_did": self.signer_did,
            "signature": self.signature_hex,
            "scheme": self.scheme,
            "co_signer": self.co_signer_did,
            "co_signature": self.co_signature_hex,
            "blockchain_anchor": self.blockchain_anchor,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class SignetKey:
    """Signing key for Signet receipts."""

    def __init__(self, seed: bytes | None = None, did: str = "did:web:agentaudit.meok.ai") -> None:
        self.did = did
        if _has_nacl():
            import nacl.signing  # type: ignore[import-untyped]
            if seed:
                self._sk = nacl.signing.SigningKey(seed)
            else:
                self._sk = nacl.signing.SigningKey.generate()
            self._vk = self._sk.verify_key
            self.scheme = "ed25519"
        else:
            # Fallback: HMAC-SHA256 with env secret
            self._secret = seed or os.urandom(32)
            self.scheme = "hmac-sha256"

    def sign(self, message: bytes) -> bytes:
        if self.scheme == "ed25519":
            return self._sk.sign(message).signature
        return hmac.new(self._secret, message, hashlib.sha256).digest()

    def verify(self, message: bytes, signature: bytes) -> bool:
        if self.scheme == "ed25519":
            try:
                self._vk.verify(message, signature)
                return True
            except Exception:
                return False
        expected = hmac.new(self._secret, message, hashlib.sha256).digest()
        return hmac.compare_digest(expected, signature)

    @property
    def public_key_hex(self) -> str:
        if self.scheme == "ed25519":
            return self._vk.encode().hex()
        return hashlib.sha256(self._secret).hexdigest()


def sign_entry(
    entry_hash: str,
    key: SignetKey,
    co_key: SignetKey | None = None,
    blockchain_anchor: str | None = None,
) -> SignetReceipt:
    """Create a Signet receipt for an audit entry hash."""
    msg = entry_hash.encode("utf-8")
    sig = key.sign(msg)
    co_sig = None
    if co_key is not None:
        co_sig = co_key.sign(msg)
    return SignetReceipt(
        entry_hash=entry_hash,
        signer_did=key.did,
        signature_hex=sig.hex(),
        scheme=key.scheme,
        co_signer_did=co_key.did if co_key else None,
        co_signature_hex=co_sig.hex() if co_sig else None,
        blockchain_anchor=blockchain_anchor,
    )


def verify_receipt(receipt: SignetReceipt, key: SignetKey) -> bool:
    """Verify a Signet receipt against a public key."""
    msg = receipt.entry_hash.encode("utf-8")
    sig = bytes.fromhex(receipt.signature_hex)
    return key.verify(msg, sig)
