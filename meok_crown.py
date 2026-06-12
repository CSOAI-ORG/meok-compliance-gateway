"""meok_crown.py — the Crown: Ed25519 root-of-trust + sigil seal.

Implements the buildable slice of CROWN_ROOT_KEY_HARDENING_SPEC.md:

  * The **sigil** — the signed seal on every SOV3↔MEOK message:
        { "kid", "payload", "ts", "sig" }   (sig = Ed25519 over canonical bytes)
  * **Asymmetric** signing (Ed25519), because a symmetric HMAC key CANNOT be a
    root-of-trust: with HMAC whoever verifies can also forge. HMAC stays in
    meok_x402.py for x402 *receipts* (signer == verifier); sigils are the
    publicly-verifiable seal.
  * A versioned **key registry** (kid → pubkey + status + validity window) so
    rotation and council revocation are possible.
  * **Chain-of-trust**: the root signs hive *certs*; a hive signs its own
    attestations; a verifier walks attestation → hive cert → root.
  * **Council revocation**: revoking/rotating the root needs a BFT quorum of the
    33-seat council (per MEOK_EMPIRE_EXPANSION.md) — no single operator can.

The MEOK-SOV-* Sovereign Token (SSO, per MEOK_EMPIRE_EXPANSION.md) is a DIFFERENT
layer: it authenticates a *user/session*; the sigil authenticates a *message's
origin + lineage to the crown*. `is_sov_token()` / `bind_sov_token()` keep them
complementary, never conflated.

Pure stdlib + `cryptography`. No network, no global mutable singletons.
"""
from __future__ import annotations

import base64
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

log = logging.getLogger("meok.crown")

# Distinct from meok_x402's "attestation-key" (the HMAC receipt key) — the crown
# root is a separate, asymmetric secret with its own rotation lifecycle.
_ROOT_SEED_KEYRING_USER = "crown-root-seed"
_ROOT_SEED_AWS_SECRET_ID = "meok/crown-root-seed"

_SOV_TOKEN_PREFIX = "MEOK-SOV-"


# ── canonicalisation ────────────────────────────────────────────────────────
def _canonical(obj) -> bytes:
    """Deterministic bytes for signing: sorted keys, no whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _signing_bytes(kid: str, payload, ts: str) -> bytes:
    return _canonical({"kid": kid, "payload": payload, "ts": ts})


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse(ts: str) -> datetime:
    dt = datetime.fromisoformat(ts)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


# ── key material ──────────────────────────────────────────────────────────────
def gen_keypair() -> tuple[bytes, bytes]:
    """(seed_32b, public_32b) for a fresh Ed25519 key. Seed is the private secret."""
    priv = Ed25519PrivateKey.generate()
    seed = priv.private_bytes_raw()
    pub = priv.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return seed, pub


def public_from_seed(seed: bytes) -> bytes:
    return Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes(
        Encoding.Raw, PublicFormat.Raw
    )


def _resolve_root_seed() -> bytes:
    """Resolve the 32-byte crown root seed. Mirrors meok_x402._resolve_attestation_key:
    AWS Secrets Manager → meok_secrets → env (dev only, warns) → fail closed."""
    # 1. AWS Secrets Manager (production)
    try:
        import boto3  # type: ignore

        resp = boto3.client("secretsmanager").get_secret_value(SecretId=_ROOT_SEED_AWS_SECRET_ID)
        if resp.get("SecretString"):
            return base64.b64decode(resp["SecretString"])
    except ImportError:
        pass
    except Exception as exc:  # noqa: BLE001
        log.debug("AWS Secrets Manager crown lookup failed (trying meok_secrets): %r", exc)

    # 2. meok_secrets (keyring → chmod-600 file)
    try:
        from meok_secrets import get_secret

        val = get_secret(_ROOT_SEED_KEYRING_USER)
        if val:
            return base64.b64decode(val)
    except ImportError:
        pass
    except Exception as exc:  # noqa: BLE001
        log.debug("meok_secrets crown lookup failed (trying env): %r", exc)

    # 3. env (dev/test ONLY), rejected in production
    val = os.environ.get("MEOK_CROWN_ROOT_SEED")
    if val:
        if os.environ.get("MEOK_ENV", "development").lower() == "production":
            raise RuntimeError(
                "MEOK_CROWN_ROOT_SEED set in env but MEOK_ENV=production. The crown root "
                f"seed must come from AWS Secrets Manager ({_ROOT_SEED_AWS_SECRET_ID!r}) or "
                f"meok_secrets ({_ROOT_SEED_KEYRING_USER!r}), never an env var in prod."
            )
        log.warning("MEOK_CROWN_ROOT_SEED read from env (dev only). Move to a secret store before prod.")
        return base64.b64decode(val)

    raise RuntimeError(
        "Crown root seed not found in AWS Secrets Manager, meok_secrets, or env. "
        "Refusing to sign — a missing crown must fail closed, never default."
    )


# ── key registry (rotation + revocation hang off this) ───────────────────────
@dataclass
class KeyEntry:
    kid: str
    public_key: bytes              # raw 32 bytes
    role: str                      # "root" | "hive"
    status: str = "active"         # "active" | "retiring" | "revoked" | "expired"
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    supersedes: Optional[str] = None
    revocation: Optional[dict] = None   # {effective, reason, quorum_sig} once revoked


@dataclass
class KeyRegistry:
    _by_kid: dict = field(default_factory=dict)

    def register(self, entry: KeyEntry) -> None:
        self._by_kid[entry.kid] = entry

    def lookup(self, kid: str) -> Optional[KeyEntry]:
        return self._by_kid.get(kid)

    def usable_at(self, kid: str, ts: str) -> tuple[bool, str]:
        """Is `kid` valid to verify a signature stamped at `ts`?"""
        e = self._by_kid.get(kid)
        if e is None:
            return False, f"unknown kid {kid!r}"
        when = _parse(ts)
        if e.valid_from and when < _parse(e.valid_from):
            return False, "before valid_from"
        if e.valid_to and when > _parse(e.valid_to):
            return False, "after valid_to"
        if e.status == "revoked" and e.revocation:
            eff = e.revocation.get("effective")
            reason = (e.revocation.get("reason") or "").lower()
            # confirmed compromise → retroactive; routine rotation → prospective only
            if "compromise" in reason or (eff and when >= _parse(eff)):
                return False, f"revoked ({e.revocation.get('reason')})"
        return True, "ok"


# ── sigil: seal + verify ──────────────────────────────────────────────────────
@dataclass
class Verdict:
    valid: bool
    reason: str
    kid: Optional[str] = None
    role: Optional[str] = None


def seal(payload, *, seed: bytes, kid: str, ts: Optional[str] = None) -> dict:
    """Create a sigil: the Ed25519-signed seal on a message."""
    ts = ts or _now_iso()
    sig = Ed25519PrivateKey.from_private_bytes(seed).sign(_signing_bytes(kid, payload, ts))
    return {"kid": kid, "payload": payload, "ts": ts, "sig": base64.b64encode(sig).decode()}


def verify_sigil(sigil: dict, registry: KeyRegistry) -> Verdict:
    """Verify a sigil against the key registry (validity window + revocation + signature)."""
    for k in ("kid", "payload", "ts", "sig"):
        if k not in sigil:
            return Verdict(False, f"malformed sigil: missing {k!r}")
    kid, ts = sigil["kid"], sigil["ts"]
    ok, why = registry.usable_at(kid, ts)
    if not ok:
        return Verdict(False, why, kid=kid)
    entry = registry.lookup(kid)
    try:
        Ed25519PublicKey.from_public_bytes(entry.public_key).verify(
            base64.b64decode(sigil["sig"]), _signing_bytes(kid, sigil["payload"], ts)
        )
    except InvalidSignature:
        return Verdict(False, "bad signature (tampered or wrong key)", kid=kid, role=entry.role)
    return Verdict(True, "ok", kid=kid, role=entry.role)


def verify_chain(attestation: dict, hive_cert: dict, registry: KeyRegistry) -> Verdict:
    """Walk attestation → hive cert → root. Proves the attestation chains to the crown.

    `hive_cert` is itself a sigil whose payload = {hive_kid, hive_public_key(b64), ...},
    sealed by a ROOT key. The attestation must be sealed by that hive_kid.
    """
    cert_v = verify_sigil(hive_cert, registry)
    if not cert_v.valid:
        return Verdict(False, f"hive cert invalid: {cert_v.reason}")
    if cert_v.role != "root":
        return Verdict(False, "hive cert not sealed by a root key (no lineage to crown)")

    cert_payload = hive_cert["payload"]
    hive_kid = cert_payload.get("hive_kid")
    if attestation.get("kid") != hive_kid:
        return Verdict(False, "attestation kid does not match the certified hive")

    # Register the certified hive key on the fly so verify_sigil can check it.
    if registry.lookup(hive_kid) is None:
        registry.register(
            KeyEntry(
                kid=hive_kid,
                public_key=base64.b64decode(cert_payload["hive_public_key"]),
                role="hive",
                valid_from=cert_payload.get("valid_from"),
                valid_to=cert_payload.get("valid_to"),
            )
        )
    att_v = verify_sigil(attestation, registry)
    if not att_v.valid:
        return Verdict(False, f"attestation invalid: {att_v.reason}", kid=hive_kid, role="hive")
    return Verdict(True, "chains to crown", kid=hive_kid, role="hive")


# ── council revocation (the constitutional check) ─────────────────────────────
def bft_quorum(n: int) -> int:
    """BFT quorum 2f+1 for n=3f+1 seats. n=33 → f=10 → quorum=21."""
    f = (n - 1) // 3
    return 2 * f + 1


def verify_revocation(record: dict, council: dict, *, seats: int = 33) -> bool:
    """A revocation is valid only if >= bft_quorum(seats) distinct council members
    signed it. `council` maps member_id → raw public key. `record["signatures"]`
    maps member_id → base64 Ed25519 signature over the canonical record body."""
    body = {k: record[k] for k in ("kid", "effective", "reason") if k in record}
    msg = _canonical(body)
    good = set()
    for member_id, sig_b64 in (record.get("signatures") or {}).items():
        pub = council.get(member_id)
        if not pub:
            continue
        try:
            Ed25519PublicKey.from_public_bytes(pub).verify(base64.b64decode(sig_b64), msg)
            good.add(member_id)
        except InvalidSignature:
            continue
    return len(good) >= bft_quorum(seats)


# ── MEOK-SOV token interop (separate layer; never conflated with the sigil) ───
def is_sov_token(value: Optional[str]) -> bool:
    """True for a `MEOK-SOV-*` Sovereign Token (with or without a Bearer prefix)."""
    if not value:
        return False
    v = value.strip()
    if v.lower().startswith("bearer "):
        v = v[7:].strip()
    return v.startswith(_SOV_TOKEN_PREFIX)


def bind_sov_token(payload: dict, sov_token: str) -> dict:
    """Bind a sigil's payload to the session that produced it, WITHOUT embedding the
    token (which is a bearer credential). Stores only a SHA-256 of the token so a
    verifier can confirm 'same session' without holding the secret."""
    import hashlib

    bound = dict(payload)
    bound["sov_token_sha256"] = hashlib.sha256(sov_token.encode()).hexdigest()
    return bound
