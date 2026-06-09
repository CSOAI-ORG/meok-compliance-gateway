# The Crown — Root-Key Hardening Spec (v0.1)

> **Status**: design spec, not built. Implements prerequisite #2 of
> `DEFONOS_SOVEREIGN_ARCHITECTURE.md` — turning `MEOK_ATTESTATION_KEY` into the
> rotatable, council-revocable **root-of-trust** ("the crown").
> **No gate, no SOV3 auth required to build** — this is the one critical-path item
> that's unblocked today. (Issuing the live root key + naming council quorum members
> are operational steps that come later.)

## 0. The finding that drives everything

`meok_x402.py:66` resolves a **symmetric HMAC-SHA256** key. The secret *resolution*
is already hardened (AWS Secrets Manager → meok_secrets → env-dev-only → fail-closed;
CRITICAL Fix #3 — done). But:

> **A symmetric HMAC key cannot be a root-of-trust.** With HMAC, whoever can *verify*
> a signature holds the same secret that *creates* it. So either (a) hives can't
> verify the sovereign's attestations, or (b) every hive that can verify can also
> **forge** — and public verification at `proofof.ai/v/<id>` would mean publishing
> the forging key. Both break the chain-of-trust the DEFONOS sovereign depends on.

The crown therefore needs **asymmetric** signing. This is the central change; rotation
and revocation are built on top of it.

## 1. Two-tier key model

Don't rip out HMAC — split responsibilities by what each primitive is good at:

| Tier | Primitive | Used for | Signer = Verifier? | Where |
|---|---|---|---|---|
| **Local receipts** | HMAC-SHA256 (keep as-is) | x402 paywall receipts, internal integrity where the gateway verifies its own output | Yes | `meok_x402.py` (unchanged) |
| **Sovereign attestations** | **Ed25519** (new) | Compliance attestations that hives + the public verify; the chain-of-trust to the crown | **No** — private signs, public verifies | new `meok_crown.py` |

Ed25519: 32-byte keys, fast, no parameter-choice footguns, stdlib-adjacent via
`cryptography`. The root holds the private seed (the crown); the public key is
published so anyone can verify and no one can forge.

## 2. Chain-of-trust (how hives chain to the crown)

```
   SOV3 root keypair (the crown)               kid=root-v1, Ed25519
        │  signs each hive's cert
        ▼
   Hive cert: {hive_id, hive_pubkey, valid_from/to, kid=root-v1, sig_by_root}
        │  hive signs its own attestations with hive_privkey
        ▼
   Attestation: {claim, ts, kid=hive:meok-v1, sig_by_hive}
        │  verifier walks: attestation → hive cert → root pubkey
        ▼
   proofof.ai/v/<id>  → "valid, chains to crown root-v1, not revoked"
```

A hive never holds the root private key. The root only ever signs **certs**, never
day-to-day attestations — so the crown is used rarely and can live in deep storage
(HSM / AWS KMS), shrinking its attack surface.

## 2a. The sigil — the seal on every message

The signed envelope is called the **sigil**: the sovereign's mark that stamps a
message so any hive (or the public) can prove it came from the holder of a given key
and chains to the crown. **Rule: every SOV3↔MEOK message is sigil-sealed** — not just
compliance attestations, but enrollment requests, oversight feeds, and revocations.
This makes the entire channel tamper-evident end to end; an unsigiled message on the
sovereign channel is rejected.

```jsonc
// the sigil
{
  "kid": "hive:meok-v1",        // which key sealed it (root or hive)
  "payload": { ... },           // the actual message
  "ts": "2026-08-01T12:00:00Z",
  "sig": "<Ed25519 signature over (kid || payload || ts)>"
}
```

`kid` = which key sealed it · `sig` = the seal (forgeable by no one, verifiable by
anyone) · chain-walk (sigil → hive cert → root) = proof of lineage to SOV3. HMAC
receipts (x402) are *not* sigils — sigils are the asymmetric, publicly-verifiable
seal; HMAC is internal-only.

## 3. Key registry (the data structure rotation + revocation hang off)

Every key — root and hive — is an entry in a signed, published registry:

```jsonc
{
  "kid": "root-v2",                 // unique, versioned key id
  "alg": "Ed25519",
  "public_key": "<base64>",
  "role": "root" | "hive",
  "status": "active" | "retiring" | "revoked",
  "valid_from": "2026-08-01T00:00:00Z",
  "valid_to":   "2027-08-01T00:00:00Z",
  "supersedes": "root-v1",          // rotation lineage
  "revocation": null | { "effective": "...", "reason": "...", "quorum_sig": "..." }
}
```

Every signature carries its `kid`. Verifiers resolve `kid` → registry entry, check
status + validity window covering the attestation's `ts`, then verify the signature.
**Adding `kid` to the signed envelope is the one change that makes both rotation and
revocation possible** — without it you can't tell which key signed what.

## 4. Rotation protocol (overlap, never a hard cutover)

1. Generate `root-vN+1`; publish its registry entry as `active`, set `valid_from` =
   now + grace.
2. Mark `root-vN` as `retiring` (still valid for verification, no longer signs new
   certs).
3. **Sign-new / verify-old**: new certs signed by `vN+1`; attestations signed under
   `vN` stay verifiable until their `valid_to`. No attestation is orphaned.
4. After the overlap window (≥ longest cert lifetime), `vN` → `expired`.

Drives cleanly off **AWS KMS / Secrets Manager automatic rotation** — the resolver in
`meok_x402.py` already prefers AWS SM, so the storage layer is in place; what's new is
the *versioned registry* + verify-against-keyring logic.

## 5. Council revocation (what makes the crown *constitutional*)

A single operator must **not** be able to revoke/rotate the root unilaterally — that
would just relocate the single point of failure. Revocation requires a **BFT quorum
from councilof.ai** (m-of-n, e.g. 3-of-5 council signers):

```jsonc
"revocation": {
  "kid": "root-v2",
  "effective": "2026-09-15T12:00:00Z",
  "reason": "suspected key compromise",
  "quorum_sig": "<aggregated m-of-n council signatures over the revocation record>"
}
```

- Verifiers reject any attestation whose `kid` is revoked **with `ts ≥ effective`**
  for routine rotation, or **all `ts`** (retroactive) for confirmed compromise — the
  `reason` field drives which policy applies.
- The revocation record itself is only valid if the council quorum signature verifies.
  **No quorum → no revocation.** This is the deposition path from
  `DEFONOS_SOVEREIGN_ARCHITECTURE.md` §3, expressed in keys.

## 6. Migration from today's code (backward-compatible)

1. **Add `kid` to the signed envelope** in `meok_x402.py` (default `hmac-v1` for
   existing HMAC receipts) — non-breaking, old verifiers ignore unknown fields.
2. **New module `meok_crown.py`**: Ed25519 sign/verify + the key registry loader
   (reuses `_resolve_attestation_key`'s store chain, now resolving a private seed).
3. **New `meok_registry.py`**: load/validate the published key registry; expose
   `verify_chain(attestation) -> Verdict`.
4. **Keep HMAC** for x402 receipts; route *compliance attestations* through the crown.
5. Tests: rotation overlap (old sig still verifies after new key active), revocation
   (revoked kid rejected per policy), forgery (hive key can't sign as root).

## 7. Threat model — what each layer defends

| Threat | Defense |
|---|---|
| Operator reads the key, forges attestations | Asymmetric: reading the *public* key forges nothing; the private root lives in KMS/HSM, used only to sign certs |
| Key compromise discovered later | Council-quorum retroactive revocation invalidates everything that kid signed |
| Rogue operator tries to revoke/rotate alone | Revocation needs BFT quorum sig — single actor can't |
| Old attestations break after rotation | Overlap window + verify-against-keyring keeps them valid to `valid_to` |
| Hive tries to impersonate the sovereign | Hive key can only sign under its own cert; chain walk to root fails |

## 8. Cross-references
- `DEFONOS_SOVEREIGN_ARCHITECTURE.md` — the crown is prereq #2 there
- `HORUS_OVERSIGHT_PLANE_SPEC.md` — oversight attestations ride this chain
- `CRITICAL_FIXES_2026-06-08.md` — Fix #3 (secret resolution, the part already done)
- `meok_x402.py:51-124` — current HMAC resolver this builds on
- [[sov3-mcp-master-audit-2026-06-08]] (CRITICAL #3) · [[horus-ubuntu-bft-alignment-2026-06-09]]
