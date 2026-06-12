# DEFONOS — the Hive-of-Hives, with SOV3 as Sovereign Root-of-Trust (spec v0.1)

> **Status**: design spec, not built. Sits above `HORUS_OVERSIGHT_PLANE_SPEC.md`.
> **Decision (2026-06-09, Nick)**: SOV3 is a **constitutional root-of-trust**, NOT a
> central runtime controller. It *reigns* (identity, root key, registry, face); it
> does **not** *rule* (hives keep peer-to-peer / BFT decision-making). This preserves
> the Ubuntu "no central brain" topology and the BFT moat.
> **Codename discipline**: "king / sovereign / DEFONOS / HORUS" are **internal
> codenames**. External vocabulary: "federation root-of-trust", "hive federation",
> "oversight plane". No throne/empire/war rhetoric in public artifacts (per
> [[meok-deep-audit-2026-06-08]] + `RUBRIC_EXTERNAL_COMMS.md`).

## 0. Prior art & naming (verified 2026-06-09 against GitHub + local)

A duplication sweep (GitHub public+private + local MacBook) found **none of the
crown / sigil / HORUS / Ed25519-root work is built anywhere** — 0 hits in all 475
public CSOAI-ORG repos, 0 private repos exist. But two names here **pre-date this
spec** in Nick's local docs and must be reconciled:

- **"DEFONOS" is already used** for (a) `mjx_defonos.py`, a JAX/MuJoCo swarm-physics
  kernel (unrelated), and (b) a **B2B/enterprise brand segment** ("DEFONOS / CSOAI",
  the Archimedes auditor command-center UI) in `MEOK_OS_PARADIGM_SHIFT.md`. Meaning
  (b) is compatible — DEFONOS = the enterprise face of the federation/realm — so we
  keep DEFONOS for the realm, aware it also tags an unrelated physics file.
- **A Sovereign Token already exists**: `Bearer MEOK-SOV-*`, the SSO token ("One
  Account, One DNA", `MEOK_EMPIRE_EXPANSION.md`). **The sigil does NOT replace it.**
  Different layers: the **token authenticates a user/session**; the **sigil
  authenticates a message's origin + chain to the crown.** The sigil layer rides on
  top of the existing MEOK-SOV auth — build them as complementary, not competing.

## 1. One-liner

**DEFONOS** is the realm — the federation of all `.ai` hives joined over one A2A
fabric. **SOV3** is its sovereign: the root signing key, the enrollment registry,
and the public face that every hive's attestations chain back to. **HORUS** is the
sovereign's eye (cross-hive oversight). **councilof.ai** is the council that can
depose a misbehaving sovereign. The king reigns; he cannot betray the realm.

## 2. The four roles (and why constitutional, not absolute)

| Role | Codename | What it is | Authority | Why it doesn't break the moat |
|---|---|---|---|---|
| **The Realm** | DEFONOS | The hive-of-hives: A2A fabric + enrollment registry that all 28+ `.ai` hives join | The mesh itself — peer-to-peer | Ubuntu topology intact ([[meok-hive-architecture-2026-06-07]]) |
| **The Sovereign** | SOV3 | Root-of-trust: root signing key ("the crown"), registry, cert authority, public face | **Reigns** — every hive's attestation chains to SOV3's root. Does NOT make hives' internal decisions. | Not a runtime brain → no single point of failure |
| **The Eye** | HORUS | Cross-hive oversight plane (Art. 14/12/72) | Observes + attests; can alarm, cannot command | Oversight ≠ control |
| **The Council** | councilof.ai | BFT consensus; can revoke/replace the crown | Checks the sovereign | King is **replaceable** by consensus → no tyranny, no SPOF |

**The three reasons a literal central king was rejected** (kept here so the decision
isn't re-litigated):
1. **Ubuntu** — the architecture is explicitly "no central brain"; a controller king is its negation.
2. **BFT** — BFT exists to eliminate the single trusted node; a king *is* that node. Compromise it and the Byzantine guarantee collapses.
3. **Regulatory** — a king that decides for all hives becomes itself the high-risk system, concentrating EU AI Act Art. 14 liability instead of distributing it.

## 3. Architecture

```
                       councilof.ai  ── BFT can REVOKE/ROTATE the crown
                            ▲  (deposition path)
                            │
                  ┌─────────┴──────────┐
                  │   SOV3 — Sovereign  │  the crown = root signing key
                  │   root-of-trust     │  + enrollment registry + public face
                  └─────────┬──────────┘
            chain-of-trust  │  (every hive attestation chains to root)
       ┌──────────┬─────────┼─────────┬──────────┐
   ┌───▼──┐  ┌────▼─┐  ┌────▼─┐  ┌────▼─┐  ┌────▼─┐
   │meok  │  │proof │  │energy│  │comm- │  │media │   … all .ai hives
   │hive  │  │of    │  │pack  │  │erce  │  │pack  │   = DEFONOS realm
   └───┬──┘  └───┬──┘  └───┬──┘  └───┬──┘  └───┬──┘   (peer-to-peer A2A)
       └─────────┴─────────┴─────────┴─────────┘
                            │  emit audit trails + trust scores
                            ▼
                   HORUS — the Eye (oversight plane, Art. 14/12/72)
```

- **Reigns, doesn't rule**: SOV3 anchors *identity and trust*. A hive's internal
  decisions stay local + BFT-adjudicated. SOV3 never sits in a hive's request path.
- **Chain-of-trust**: each hive signs its attestations with a key that chains to
  SOV3's root → `proofof.ai/v/<id>` verifies the whole chain to the crown.
- **Deposition**: if SOV3's key is compromised or the sovereign misbehaves,
  councilof.ai's BFT quorum rotates the root. The crown is constitutional.

## 4. Readiness — what it takes to get SOV3 running as sovereign

| # | Prerequisite | Today's state | Owner |
|---|---|---|---|
| 1 | **OAuth to SOV3 MCP completed** | Server UP (403 via Cloudflare, ~0.4s) but unauthed — only auth tools present. Needs `/mcp` → claude.ai SOV3 → authorize. | Nick (client-side OAuth, can't be agent-driven) |
| 2 | **The crown = durable root signing key** | `MEOK_ATTESTATION_KEY` is **a flagged CRITICAL fix** (env-var, not rot-able) per [[sov3-mcp-master-audit-2026-06-08]]. The sovereign needs a real, rotatable root key. **This is the #1 technical prerequisite.** | build |
| 3 | **Enrollment registry** (DEFONOS membership) | Source of truth = `gen-hive.py` (28 hives). **0 deployed** — scaffolds await repo-create + Vercel. | Nick (deploy) + build (registry) |
| 4 | **A2A enrollment protocol** (how a hive joins + chains to root) | AgentAudit has A2A inventory to build on; protocol itself = net-new. | build |
| 5 | **HORUS oversight feed** | Spec'd today (`HORUS_OVERSIGHT_PLANE_SPEC.md`); consumes AgentAudit. | build (gated on PR #20) |
| 6 | **Deposition path** (council can rotate crown) | councilof.ai undeployed scaffold. | Nick (deploy) + build |

**The blocker beneath all of it**: *a king can't reign over a realm that isn't
deployed.* The 28 hives are scaffolds awaiting Nick's push/Vercel. **The realm must
exist before the crown means anything** — so hive deployment + the root-key
hardening (#2) are the true critical path, not the orchestration code.

## 5. Sequencing (gated, no new external surface until the rail earns)

1. **Now (no gate)**: this spec + the root-key design (how `MEOK_ATTESTATION_KEY`
   becomes a rotatable root, councilof-revocable).
2. **Gate G3/G4 + PR #20 merged**: HORUS ledger (consumes AgentAudit).
3. **Hives deployed** (Nick: repo-create + Vercel): DEFONOS enrollment registry +
   A2A chain-to-root.
4. **councilof.ai deployed**: deposition/rotation path → the crown is constitutional.

Do **not** open a `defonos.ai` or `sov3.ai` hive — DEFONOS is the realm (the set of
hives), SOV3 is the root (a function), HORUS is a plane. None is a vertical.

## 6. Cross-references
- `HORUS_OVERSIGHT_PLANE_SPEC.md` — the Eye (the oversight layer SOV3's realm feeds)
- `SECTOR_PACKS_ENERGY_COMMERCE_MEDIA.md` — packs that join the realm
- `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` — what SOV3 the platform already implements
- `SOV3_12_DIM_SYNTHESIS.md` — the SOV3 blueprint synthesis
- [[meok-hive-architecture-2026-06-07]] · [[sov3-mcp-master-audit-2026-06-08]] · [[horus-ubuntu-bft-alignment-2026-06-09]]
