# Horus — the Oversight Plane (internal spec v0.1)

> **Status**: design spec, not built. Keystone for the sector-pack expansion
> (`SECTOR_PACKS_ENERGY_COMMERCE_MEDIA.md`).
> **Codename discipline**: "Horus" is an **internal codename only**. Externally
> it ships as **"the Oversight Plane" / "Article 14 Continuous-Oversight engine."**
> No Egyptian-theology framing in any public artifact — see
> [[meok-deep-audit-2026-06-08]] (scrub war-dossier/mythic rhetoric before
> external publication).

## 1. One-liner

Horus is the **cross-hive oversight plane**: the single all-seeing layer that
watches every agent action across all 28 hives, aggregates their tamper-evident
audit trails and trust scores, and emits signed *oversight attestations* that map
directly onto EU AI Act Articles 14, 12 and 72. It is the thing that turns a pile
of independent vertical hives into **one governable fabric you can sell as a
platform.**

## 2. Why it exists — the three-layer philosophy

This is the alignment Nick asked for. Ubuntu, BFT and Horus are not three
mascots competing for the same job — they are three layers of one governance
stack, and we already half-built each:

| Layer | Concept | Answers | Already in the repo |
|---|---|---|---|
| **Ubuntu** — *"a person is a person through other persons"* (Nguni/Bantu communal ethic; ancient root, codified 20th C) | The **ethic / topology** | *Why peer hives, no central brain?* | The 25-hive **A2A peer-to-peer, no-central-brain** architecture ([[meok-hive-architecture-2026-06-07]]) **is** Ubuntu — truth emerges relationally from the mesh, not from a king. |
| **BFT** — Byzantine Fault Tolerance | The **mechanism** | *How does collective truth survive liars/faulty nodes?* | `councilof.ai`, `proofof.ai` — the headline differentiator (`KEY_DIFFERENTIATORS.md`). |
| **Horus** — the Eye (oversight, protection, accountability of the sovereign) | The **oversight plane** | *Who watches the watchers? Where is the immutable record?* | Scattered today: AgentAudit (tamper-evident trails, trust scoring, shadow scanner), `safetyof.ai` (monitoring), `accountabilityof.ai` (incident + audit), `transparencyof.ai` (explainability). **Never named or unified.** |

**The gap Horus fills:** oversight currently exists as four disconnected hives.
There is no single plane that sees *across* them. Horus is that plane. It is **not
a new hive** — it is the aggregation/oversight tier that the governance hives feed
into and that the vertical packs (Energy/Commerce/Media) hang off.

## 3. Regulatory anchors (why buyers pay for it)

Horus is not a metaphor looking for a market. It is the literal implementation
surface of three obligations that go live for EU high-risk AI on **2 Aug 2026**:

| Obligation | What it requires | Horus function |
|---|---|---|
| **EU AI Act Art. 14 — Human Oversight** | *Meaningful* (not symbolic) human review: who reviewed, when, outcome, reasoning. | `oversight.queue()` — routes high-stakes agent actions to a human, captures who/when/outcome/why, signs the record. |
| **EU AI Act Art. 12 — Record-keeping / logging** | Automatic, tamper-evident logs over the system lifecycle. | Aggregates every hive's AgentAudit trail into one immutable, HMAC-chained ledger. |
| **EU AI Act Art. 72 — Post-market monitoring** | Continuous monitoring of deployed high-risk systems + incident reporting. | `oversight.monitor()` — continuous trust-score drift detection across the mesh; feeds `accountabilityof.ai` incident flow. |

Adjacent duties it also discharges: **NIS2** continuous-monitoring + incident
reporting for essential entities (energy, finance), **DORA** operational-resilience
logging. This is why the Energy and Commerce packs need Horus underneath them.

## 4. Architecture

```
        Ubuntu topology: 28 peer hives, A2A, no central brain
   ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐   ...
   │meok  │  │proof │  │energy│  │comm- │  │media │
   │      │  │of    │  │pack  │  │erce  │  │pack  │
   └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘
      │ emits   │ emits   │ emits   │ emits   │ emits
      │ AgentAudit trail + trust score (A2A events)
      ▼         ▼         ▼         ▼         ▼
   ╔══════════════════════════════════════════════════╗
   ║   HORUS — the Oversight Plane (this spec)          ║
   ║   • ledger:  HMAC-chained aggregate of all trails  ║  ← Art. 12
   ║   • monitor: trust-score drift across the mesh     ║  ← Art. 72
   ║   • queue:   human-oversight routing + capture     ║  ← Art. 14
   ║   • attest:  signs oversight attestations          ║  → proofof.ai
   ╚══════════════════════╤═══════════════════════════╝
                          │ BFT consensus on contested/high-stakes events
                          ▼
                  councilof.ai (the math)
```

- **Consumes** (does not re-implement): AgentAudit's tamper-evident trails +
  trust scores + shadow-scanner findings, emitted as A2A events by each hive.
- **Adds** (the genuinely new code): cross-hive aggregation, drift/anomaly
  detection over the *fleet* of trust scores, the human-oversight queue, and the
  oversight-attestation signer.
- **Delegates**: contested or high-stakes events go to `councilof.ai` for BFT
  adjudication; resulting attestations are verifiable at `proofof.ai/v/<id>`.

**Reuse, don't rebuild:** ~70% of Horus already exists as AgentAudit + the four
governance hives. Horus is the thin, valuable plane that *unifies* them. Estimated
net-new surface: the aggregation ledger, the drift monitor, and the Art. 14 queue.

## 5. MCP tool surface (proposed)

| Tool | Input | Output | Article | Price |
|---|---|---|---|---|
| `oversight.ledger_append` | `event: AgentAuditEvent` | `LedgerReceipt` (chain position + HMAC) | Art. 12 | metered |
| `oversight.queue` | `action: HighStakesAction` | `ReviewTicket` (who/when/outcome/reasoning) | Art. 14 | per review |
| `oversight.monitor` | `hive_id`, `window` | `DriftReport` (trust-score deltas + anomalies) | Art. 72 | subscription |
| `oversight.attest` | `decision_id` | `OversightAttestation` (signed; verifiable at proofof.ai) | 14+12 | per attestation |
| `oversight.fleet_view` | — (free, the wedge) | live mesh-wide oversight dashboard | — | FREE |

`oversight.fleet_view` is the FREE wedge — same play as `agent-mcp-router` in
`INDUSTRY_PACKS_2027_Q1.md`: every install becomes a paid-attestation buyer.

## 6. Dependencies & gating

Horus ships **behind the same gate as everything else** — no new external surface
until the rail earns:

1. Gateway public flip (G4) + Stripe/wallet live (G3) — per `FIVE_FLYWHEEL_STATUS_2026-06-08.md`.
2. AgentAudit merged + published (PR #20 — **CI currently RED**, missing
   `pip install x402` in `.github/workflows/agentaudit-ci.yml`; see
   [[agentaudit-paywire-tests]]). Horus consumes AgentAudit, so this lands first.
3. `councilof.ai` deployed (BFT adjudication endpoint).

Build order: **(2) → Horus ledger+monitor → (3) → Horus attest+queue.** Do not
open a `horus.ai` hive — Horus is a plane, not a vertical.

## 7. Cross-references
- `SECTOR_PACKS_ENERGY_COMMERCE_MEDIA.md` — the three sector packs that ride on Horus
- `INDUSTRY_PACKS_2027_Q1.md` — the existing 7-pack structure + FREE-router wedge pattern
- `EU_AI_ACT_DEADLINE_INTEL.md` — Art. 14 oversight definition (line 30)
- `KEY_DIFFERENTIATORS.md` — BFT consensus as the headline moat
- [[meok-hive-architecture-2026-06-07]] · [[agentaudit-server]] · [[meok-deep-audit-2026-06-08]]
