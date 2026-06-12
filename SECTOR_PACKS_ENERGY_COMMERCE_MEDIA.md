# Sector Packs — Energy · Commerce · Media (briefs)

> **Companion to** `INDUSTRY_PACKS_2027_Q1.md` (Packs 1–7). These are Packs 8–10,
> the answer to "ENERGY / SHOPPING / MEDIA / NEWS — wide-open gaps we can fill and
> synthesize with what we already have?" (2026-06-09).
> **All three ride on the Oversight Plane** (`HORUS_OVERSIGHT_PLANE_SPEC.md`) and the
> existing 13-framework engine — they are **packs, not new hives.**
> **NEWS is deliberately absent**: it's weak as a product and strong as our
> AEO/credibility channel — keep it in `gen-geo.py` + `REGULATORY_CALENDAR`, don't
> productize it. See §4.

## Coverage map

| Pack | Net-new MCPs | Reuses (already built) | Primary Buyer | Reg. anchor | ARR range |
|---|---:|---|---|---|---|
| `energy-critical-infra-pack` | 2 | BFT (councilof), proofof, transparencyof, nis2-complete, oversight plane | TSO/ISO Ops Director, Utility CISO | EU AI Act **Annex III** (critical infra) + **NIS2** | $40K–$400K |
| `agentic-commerce-pack` | 2 | **x402 rail** (shipped), proofof, oversight queue/audit | Head of Payments / Trust & Safety | DSA + EU AI Act Art. 50 + consumer/dark-pattern rules | $20K–$250K |
| `media-provenance-pack` | 1 | **`label_synthetic_content`** (built, CHINA spec), HMAC signer, ai-watermarking-suite | Head of Content / Ad-network Compliance | EU AI Act **Art. 50 / Art. 4** (synthetic disclosure) + C2PA | $15K–$150K |

The "reuses" column is the point: each pack is mostly **assembly of assets we
already shipped**, not greenfield. Sequence by synthesis cost: **Commerce → Media
→ Energy.**

---

## Pack 8: Energy & Critical-Infrastructure Pack (`energy-critical-infra-pack`)

**MCPs**: `nis2-complete`, `cra-complete`, `iso-27001`, `eu-ai-act-complete`,
`regulatory-crosswalk-engine`, + **net-new** `grid-decision-attestor`,
`critical-infra-classifier`.

**Target users**: Transmission/distribution operators (TSO/DSO), ISOs, utilities,
oil & gas majors running AI ops, energy traders, grid-balancing/demand-forecast
vendors.

**Value prop**: The compliance + oversight layer for AI that manages energy
critical infrastructure. Classify the system as high-risk, attest every
grid/dispatch/load-shed decision with a signed, immutable, BFT-adjudicated record,
and discharge NIS2 continuous-monitoring + incident duties — all from one pack.

**Why this bundle / why now**: EU AI Act **Annex III** explicitly names AI used in
the *"management and operation of critical infrastructure (gas, electricity, water,
traffic)"* as **high-risk** (cf. `EU_AI_ACT_FREE_SCANNER_SPEC.md` line 34). Energy
operators are also **essential entities under NIS2** (continuous monitoring +
incident reporting). **No competitor ships an MCP for energy-sector AI compliance**
— this is the widest-open lane.

**Why it's our strongest BFT story**: Grid dispatch and automated load-shedding are
the textbook Byzantine-fault case — a single rogue/faulty node mis-dispatching is
exactly what `councilof.ai`'s BFT consensus prevents, and exactly what a regulator
wants an immutable record of. The energy pitch sells the BFT moat better than any
governance abstraction.

**Key integrations**: `critical-infra-classifier` → EU AI Act high-risk
determination; `grid-decision-attestor` → councilof BFT sign-off → proofof
verifiable receipt; transparencyof explains the load-shed ("*why* did the AI shed
this feeder?"); Horus ledger holds the Art. 12 record + NIS2 monitoring feed.

**ARR target**: $40K–$400K (by operator size / regulated asset base).

**Sales motion**: Direct enterprise; industry-body channels (ENTSO-E, national grid
operators); pilot on one dispatch model → expand to fleet.

---

## Pack 9: Agentic-Commerce Pack (`agentic-commerce-pack`)

**MCPs**: `gdpr`, `eu-ai-act-complete`, `bias-detection` (pricing
non-discrimination), `meok-attestation-verify`, + **net-new** `agent-spend-control`,
`purchase-attestor`.

**Target users**: Marketplaces, retailers, PSPs, and anyone exposing an AI shopping
agent — plus the agent-platform side (Visa Intelligent Commerce, Mastercard Agent
Pay, Coinbase x402 ecosystems).

**Value prop**: The trust + attestation layer for AI agents that *transact*. Who
authorized this agent to spend, against what limit, was the price non-discriminatory,
and where is the signed receipt for chargeback/audit/DSA. Every agent purchase gets
a signed attestation; spend limits are enforced and immutably logged.

**Why this bundle / why now**: Agentic commerce is the current wave (Visa, Mastercard,
Coinbase **x402**) and the **governance layer for agent-driven purchases is wide
open** — nobody is attesting *who authorized the spend* or *whether the recommendation
was explainable*. Stacked obligations: **DSA** (marketplace transparency / dark
patterns), **EU AI Act Art. 50** (interacting-with-AI disclosure), consumer-protection
law on dynamic pricing.

**Why it's our best synthesis (least new code)**: We already shipped the **x402 rail
+ paywall** ([[x402-rollout-state]], [[Revenue rail testnet — 9 Jun]]). This pack is
that rail turned outward — `purchase-attestor` signs the x402 settlement as a
compliance receipt; `agent-spend-control` is the spend snapshot we already track in
AgentAudit (`_PAID_LOG` + `spending_snapshot`). Half-built today.

**Key integrations**: x402 settlement → `purchase-attestor` → proofof receipt;
`agent-spend-control` → Horus Art. 14 queue for over-limit human sign-off;
bias-detection → pricing-fairness check; oversight ledger → DSA audit export.

**ARR target**: $20K–$250K (by GMV / transaction volume).

**Sales motion**: Land via the FREE x402 receipt tool (developer-led), expand to
enterprise Trust & Safety; agent-platform partnerships.

---

## Pack 10: Media & Content-Provenance Pack (`media-provenance-pack`)

**MCPs**: `ai-watermarking-suite`, `label_synthetic_content` (the China-spec tool),
`meok-attestation-verify`, `eu-ai-act-complete`, + **net-new** `c2pa-provenance-signer`.

**Target users**: Media companies, publishers, ad networks, agencies, stock/UGC
platforms, brands shipping AI-generated creative.

**Value prop**: Provenance-as-a-service. Sign and attest media at creation
(C2PA-compatible), disclose AI generation per EU AI Act Art. 50/Art. 4, and hold a
verifiable provenance record — so a publisher or ad network can prove what was AI-made
and when.

**Why this bundle / why now**: EU AI Act **Art. 50** (synthetic-content transparency)
and **Art. 4** (literacy/labeling) bite on **2 Aug 2026**; C2PA provenance is becoming
table stakes for publishers and ad networks.

**Why it's high-fit / low-effort**: We **already built `label_synthetic_content`**
(signed manifest + sidecar) in `CHINA_AI_ANTHROPOMORPHIC_MCP_SPEC.md`, and we already
have the HMAC signing infra. This pack is that tool **generalized to C2PA** plus our
existing watermarking suite — the smallest net-new build of the three.

**Key integrations**: `c2pa-provenance-signer` ⇄ HMAC signer ⇄ ai-watermarking-suite
for dual hard/soft provenance; `label_synthetic_content` → proofof verifiable
manifest; oversight ledger holds the Art. 50 disclosure record.

**ARR target**: $15K–$150K.

**Sales motion**: Self-serve for the provenance signer (developer/creator-led),
enterprise expansion to publishers + ad networks; partner with C2PA / content-auth
coalitions.

---

## 4. Why NEWS is not a pack

NEWS is **weak as a product** for us (we have no newsroom asset and the regulated
surface is thin) but **strong as a channel**: it's our AEO/credibility engine. The
lane is to be **the cited authority** that AI answer-engines quote on EU AI Act
questions — which we already operate via `gen-geo.py`, `REGULATORY_CALENDAR_2026-2027.md`,
`CVE_INTEL_BRIEF_2026-06-08.md`, and the `28_DAY_BLOG_CALENDAR.md`. Action: keep
running it as top-of-funnel that feeds councilof/meok; **do not build a news hive.**

## 5. Build discipline (the council's recommendation)

1. **No new domains.** 28 hives exist, most unpushed, revenue is $0, and the real
   blockers are 5 manual Nick tasks (Stripe/Vercel/DNS/wallet). These three are
   **packs on the Oversight Plane**, not new companies.
2. **Sequence by synthesis cost**: Commerce (x402 done) → Media (labeling tool done)
   → Energy (most new code, but best check size + best BFT narrative).
3. **Everything stays behind the gate**: gateway public (G4) + Stripe/wallet (G3) +
   AgentAudit merged (PR #20 CI is RED — fix `pip install x402` in the workflow) +
   Horus ledger live. No new external surface until the rail earns first dollar.

## 6. Cross-references
- `HORUS_OVERSIGHT_PLANE_SPEC.md` — the plane all three packs ride on
- `INDUSTRY_PACKS_2027_Q1.md` — Packs 1–7 + the FREE-wedge pattern
- `EU_AI_ACT_FREE_SCANNER_SPEC.md` (line 34) — Annex III critical-infra naming
- `CHINA_AI_ANTHROPOMORPHIC_MCP_SPEC.md` — the `label_synthetic_content` tool we reuse
- [[x402-rollout-state]] · [[Revenue rail testnet — 9 Jun]] · [[agentaudit-paywire-tests]]
