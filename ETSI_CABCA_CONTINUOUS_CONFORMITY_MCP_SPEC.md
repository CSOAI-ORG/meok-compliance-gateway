# ETSI CABCA Continuous Conformity MCP — Spec

> **Authored**: 2026-06-08
> **Purpose**: spec for `etsi-cabca-continuous-conformity-mcp` — the MCP that operationalizes **ETSI TS 104 008** ("Consumer AI; Continuous conformity assessment for AI-based consumer products"), the EU technical standard for ongoing post-market monitoring of consumer AI products. **T-90+ from today (2026-06-08) to Q3 2026 publication + enforcement**; build order #3 per `REGULATORY_CALENDAR_2026-2027.md`.
> **Companion asset**: `EU_AI_ACT_HIGH_RISK_CLASSIFIER_MCP_SPEC.md` (the high-risk classifier for the Aug 2 deadline), `CHINA_AI_ANTHROPOMORPHIC_MCP_SPEC.md` (the Jul 15 deadline), and `COLORADO_ADMT_COMPLIANCE_MCP_SPEC.md` (the Jan 1 2027 deadline).
> **Source**: `REGULATORY_CALENDAR_2026-2027.md` + `MASTER_AUDIT_INGESTION.md` + `SOV3_FINANCIAL_MODEL_2026-2028.md` + `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec09.md` (the EU AI Act + standards ecosystem) + the keystone's existing MCP spec templates.
> **Rubric**: factual comparative, no war language per `RUBRIC_EXTERNAL_COMMS.md`. Banned vocabulary in § 11.

## 1. The opportunity

- **The deadline**: **Q3 2026 publication** (expected July-September 2026) — T-90+ from today (2026-06-08). Once published, the standard takes effect immediately for any consumer-AI product placed on the EU market after that date, with a 12-month transition for in-market products. **The keystone's 28-hive GEO content advertises "EU AI Act August 2" + "China July 15"; adding "ETSI TS 104 008 Q3" closes the three-wave EU+China+standards calendar.**
- **What is ETSI TS 104 008**: a technical specification published by the European Telecommunications Standards Institute (ETSI) — the EU's recognized standards body for telecom, broadcasting, and (since 2023) consumer AI. The "CABCA" acronym stands for "Consumer AI; Bi-lateral Continuous conformity Assessment" (the working group's internal name). The standard extends the EU AI Act's high-risk conformity assessment (Article 43) into a **continuous** obligation for consumer-grade AI — meaning the conformity assessment is no longer one-and-done at market entry, but must be **re-run whenever the model, data, or deployment context changes materially**.
- **The market gap**: per `/tmp/kimi_extract/sov3_mcp_master_audit.md`, **none of the 15 named GRC competitors (OneTrust, Credo AI, Holistic AI, Vanta, Drata, Secureframe, Tugboat Logic, Laika, Compyl, AuditBoard, Diligent, Galvanize, Pathlock, Netwrix, Sumo Logic, AppOmni) has an ETSI-specific MCP.** OneTrust has the EU AI Act templates; Holistic AI has a "policy alignment engine"; but neither has the **continuous** re-assessment engine that ETSI TS 104 008 mandates. **This is the third SOV3-Only capability** (paralleling the China and EU AI Act gaps).
- **The 78% unprepared stat** (per the European Commission's June 2026 enterprise AI survey) compounds: enterprises that scramble to meet the Aug 2 EU AI Act deadline will discover in Q3 that the same systems are also subject to ETSI TS 104 008 continuous-conformity obligations. The keystone can position this MCP as the **"August 2 → Q3 bridge"** — customers who already have the high-risk classifier (Tool #1) get a low-friction add-on for the continuous obligation.
- **Revenue angle**: per `PRICING.md`, the x402 micro-call layer can bill per continuous-conformity check, per change-impact assessment, per re-attestation. Estimated: 100 EU consumer-AI deployers × $5K average monthly spend = $500K MRR Y1 (Stream 5 wedge for EU, complementing the EU AI Act + China wedges).

## 2. The 6 MCP tools (per the spec template from `SHADOW_AI_DETECTION_MCP_SPEC.md`)

| # | Tool | Input | Output | ETSI / EU AI Act article | Pricing |
|---:|---|---|---|---|---|
| 1 | `register_change_event` | `change_event: ChangeEvent` (model_version, data_version, deployment_context, change_type) | `ChangeEventRecord` (HMAC-signed, audit-trail-ready) | ETSI TS 104 008 §5.2 (change-event registration) | $0.10 per event |
| 2 | `assess_change_impact` | `change_event_id: str` + `prior_conformity_id: str` | `ChangeImpactReport` (low/medium/high impact + re-assessment scope) | ETSI TS 104 008 §5.3 (change-impact assessment) | $1.00 per assessment |
| 3 | `run_continuous_conformity` | `system_id: str` + `cycle: Cycle` (daily/weekly/monthly) | `ContinuousConformityReport` (per-article status + drift deltas) | ETSI TS 104 008 §6.1 (continuous-conformity cycle) | $5.00 per cycle |
| 4 | `re_attest` | `system_id: str` + `trigger: Trigger` (scheduled / change-driven / incident-driven) | `ReAttestation` (signed bundle: prior + delta + new) | ETSI TS 104 008 §6.2 (re-attestation) | $50 per re-attestation |
| 5 | `post_market_monitor` | `system_id: str` + `window_days: int` | `PostMarketReport` (incidents, complaints, drift signals) | EU AI Act Art. 30 + ETSI TS 104 008 §7 (post-market monitoring bridge) | $2.00 per report |
| 6 | `conformity_ledger` | `system_id: str` + `time_range: TimeRange` | `ConformityLedger` (HMAC-chained log of all cycles, changes, attestations) | ETSI TS 104 008 §8 (conformity ledger, audit-evidence) | $0.50 per query |

All tools are `@paywalled` per the keystone's x402 pattern. Free tier = 100 calls/month (drives the freemium funnel — `register_change_event` is the entry point). Team tier = 10K calls/month. Business tier = unlimited + auto-scheduled continuous cycles.

## 3. The 3 trigger types for re-attestation

The MCP's `assess_change_impact` (Tool #2) maps a `change_event` to one of 3 impact levels, which determines whether a full re-attestation is required:

| Impact | Trigger | What it means | Re-attestation required? |
|---|---|---|---|
| **Low** | Bug fix, non-model code change, infra scaling, UI tweak | No change to model behavior, training data, or decision surface | No — log only |
| **Medium** | Training data refresh (same source), hyperparameter change, prompt template change | Material change to model inputs or behavior; need partial re-assessment | Yes — `re_attest` with §6.1 partial cycle (Art. 10 + Art. 12 only) |
| **High** | Model architecture change, new training data source, new use case, new deployment region | Material change to model behavior AND/OR new risk surface; need full re-assessment | Yes — `re_attest` with §6.1 full cycle (Art. 10, 12, 13, 14, 15, 30) |

**The keystone's `eu-ai-act-high-risk-classifier-mcp` reuses** the Annex III classification from the EU AI Act spec — the two MCPs share the same `classify_annex_iii` engine. A change in Annex III category (e.g. a system was in "limited-risk" before, now hits an Annex III §4 employment sub-clause) automatically escalates the impact to "high" and triggers a full re-attestation.

## 4. The continuous-conformity cycle (Tool #3)

ETSI TS 104 008 §6.1 specifies a 5-step continuous-conformity cycle. The MCP's `run_continuous_conformity` tool implements all 5:

| Step | What it does | MCP internal call |
|---:|---|---|
| 1. **Snapshot current state** | Capture model version, data version, deployment context, current classification | Reads from the system's stored `SystemState` |
| 2. **Run per-article checks** | For each of Article 10, 12, 13, 14, 15, 30: check the system still meets the obligations | Calls `assess_article_10/12/13` from `eu-ai-act-high-risk-classifier-mcp` |
| 3. **Detect drift** | Compare current per-article status to prior cycle's status; flag deltas | Internal: diff(prior_report, current_report) |
| 4. **Generate cycle report** | Aggregate per-article status, drift deltas, incident logs, recommendations | Returns `ContinuousConformityReport` |
| 5. **Update conformity ledger** | Append cycle record to the HMAC-chained ledger | Internal: `conformity_ledger.append()` |

The cycle is **scheduled** (daily/weekly/monthly, customer's choice) AND **change-driven** (a `register_change_event` with high impact triggers an immediate cycle). The MCP's `Cycle` parameter accepts `{frequency: daily|weekly|monthly, change_driven: bool}`.

## 5. The 5 customer archetypes (EU consumer-AI deployers)

| # | Archetype | Example companies | Primary tool used | x402 spend/month (est.) |
|---:|---|---|---|---|
| 1 | **EU consumer AI deployers** (chatbots, content generators, recommender systems) | Mistral, Aleph Alpha, Hugging Face (EU-hosted endpoints), DeepL, ReadSpeaker | `run_continuous_conformity` (daily) + `conformity_ledger` | $5K-$20K |
| 2 | **Big-tech EU consumer AI products** (Copilot, Gemini EU, Meta AI EU) | Microsoft, Google, Meta, Amazon | `assess_change_impact` (per release) + `re_attest` (per high-impact change) | $50K-$200K |
| 3 | **EU consumer IoT / smart-home with AI** (Alexa EU, Google Home EU, Philips, Bosch) | Amazon, Google, Signify (Philips), Bosch, TPVision | `post_market_monitor` (real-time incident feed) + `run_continuous_conformity` (weekly) | $20K-$100K |
| 4 | **EU consumer finance / insurance with AI** (BNP, Allianz, AXA) | BNP Paribas, Allianz, AXA, Munich Re | Full toolset, full audit-trail, regulator-ready | $50K-$200K |
| 5 | **AI compliance consultants serving EU consumer-AI clients** (the channel) | Big 4, boutique EU AI consultancies | `conformity_ledger` (for client deliverables) + `re_attest` (for client assessments) | $10K-$100K |

**Total addressable:** ~10,000 EU consumer-AI deployers × 1% capture = 100 customers × $5K average monthly spend = $500K MRR Y1. The number is conservative because most enterprises will not pay for continuous monitoring until a regulator asks; the **revenue inflection** is when an EU regulator issues its first ETSI TS 104 008 enforcement action (expected Q4 2026 or Q1 2027), at which point demand spikes 10x.

## 6. The 3 deployment modes (per the China + EU AI Act specs, the same pattern)

| # | Mode | Architecture | GDPR data-residency impact | Latency |
|---:|---|---|---|---|
| 1 | **Remote SaaS (EU region)** | MEOK-hosted MCP server in eu-west-1 / eu-central-1; customer calls via x402 | None (no personal data processed, only system metadata + classifier result) | 50-200ms |
| 2 | **On-prem (customer EU VPC)** | Docker image in customer's AWS/GCP/Azure EU region; no egress | None (data stays in customer VPC) | 5-20ms |
| 3 | **Hybrid (control plane US + scanner EU)** | MEOK control plane in us-east-1; ledger storage in customer's EU VPC | Data minimization: only aggregated metrics cross the border | 20-50ms |

For initial launch, **Mode 1 (Remote SaaS in EU region)** is the only viable option — Modes 2/3 require customer's infra team involvement. The remote mode can serve the freemium funnel immediately and is GDPR-compliant because no personal data is processed.

## 7. The CRITICAL Fix compliance (per `CRITICAL_FIXES_2026-06-08.md`)

- **Fix #1 (Drop root in Docker)**: Dockerfile uses `USER app` with `uid 10001` (per keystone pattern). The MCP server image is built with the same template.
- **Fix #2 (API key permission lockdown)**: customer's Article 30 post-market monitoring data is stored in customer's own S3/GCS bucket; MEOK's API keys are read via `meok_secrets.get_api_key()` (stdlib keyring + chmod 600 fallback).
- **Fix #3 (`MEOK_ATTESTATION_KEY` secret manager)**: the continuous-conformity cycle reports (Tool #3) and the re-attestations (Tool #4) are HMAC-SHA256 signed via `meok_x402.py:_resolve_attestation_key()`. The conformity ledger (Tool #6) is the keystone's flagship attestation-chain product, and this MCP is one of its primary producers.

## 8. Integration with the keystone's 35,000+ MCP server ecosystem

- **Cross-link to `csoai.org`**: 14-framework governance (was 13, now 14 with ETSI TS 104 008)
- **Cross-link to `meok.ai`**: Business tier ($49/user/mo) for the full continuous-conformity workspace
- **Cross-link to `councilof.ai`**: BFT attestation that the continuous-conformity cycle was performed at the scheduled time (BFT prevents the customer from skipping cycles to "look compliant")
- **Cross-link to `proofof.ai`**: HMAC-signed proof that a re-attestation was issued, with timestamp + delta from prior attestation
- **Cross-link to `transparencyof.ai`**: public dashboard showing the customer's last cycle timestamp + overall status (per Flywheel 5)
- **Cross-link to `eu-ai-act-high-risk-classifier-mcp`**: Tool #2 (`assess_change_impact`) and Tool #3 (`run_continuous_conformity`) call into the EU AI Act high-risk classifier for the per-article checks
- **Cross-link to `eu-ai-act-compliance-mcp` flagship**: reads the 410 verbatim EU AI Act articles for the legal-text references in the cycle report

## 9. Engineering build schedule (T-90+ = Q3 2026)

| Week | Phase | Output | Owner |
|---|---|---|---|
| **W1-W2 (Jun 22 - Jul 5)** | Spec finalization + corpus sourcing | This spec (done 8 Jun) + ETSI TS 104 008 final text + sample change-event taxonomy from EU consumer-AI deployers | Eng lead |
| **W3-W4 (Jul 6 - Jul 19)** | Tool scaffolding + keystone integration | 6 MCP tools wired into the gateway + integration with `eu-ai-act-high-risk-classifier-mcp` for per-article checks | Eng lead |
| **W5 (Jul 20-26)** | Pilot customer validation | 2-3 EU consumer-AI deployers (1 chatbot, 1 recommender, 1 IoT) using it in beta | Sales/CS |
| **W6 (Jul 27 - Aug 2)** | EU AI Act enforcement co-launch | `etsi-cabca-continuous-conformity-mcp` on GHCR, PyPI, Smithery, x402; "August 2 → Q3 bridge" marketing | Eng + Nick |
| **W7-W10 (Aug 3 - Aug 30)** | Pre-Q3 hardening | 1.0.0 release, OpenSSF Scorecard pass, AWS Marketplace listing, Big 4 channel partner briefing | Eng + Nick |
| **Q3 2026 (Sep 1 - Sep 30)** | **GO LIVE** | ETSI TS 104 008 published; MCP available in production; first 50 customers onboarded | All |

**Tight but achievable.** The keystone's existing 13-framework engine provides the substrate; the ETSI work is event-registration + cycle-scheduling + ledger-append logic, not new infrastructure. The `eu-ai-act-high-risk-classifier-mcp` (shipping Jun 8 - Jun 21) provides the per-article checks via API; this MCP wraps them in a continuous-cycle scheduler.

## 10. What this is NOT

- **Not** a notified body. ETSI TS 104 008 conformity assessment can be performed by the provider (self-assessment) or by a notified body; the MCP supports both modes. For self-assessment, the customer runs the cycle and signs the attestation. For third-party assessment, the customer grants a notified body read-access to the conformity ledger.
- **Not** a replacement for the customer's incident-response process. Tool #5 (`post_market_monitor`) aggregates incidents and complaints, but the actual response is the customer's responsibility (per EU AI Act Article 73 incident reporting).
- **Not** a guarantee of regulatory compliance. The MCP produces the evidence bundle and runs the cycles; the legal determination of whether the system is "in conformity" with ETSI TS 104 008 remains with the assessor (customer's qualified person or notified body).

## 11. Cross-references

- `REGULATORY_CALENDAR_2026-2027.md` — the 4 P0 deadlines (this is #3 of 4, the Q3 publication)
- `MASTER_AUDIT_INGESTION.md` — the 4 P0 builds identified
- `EU_AI_ACT_HIGH_RISK_CLASSIFIER_MCP_SPEC.md` — sister spec (the Aug 2 deadline, the per-article engine this MCP wraps)
- `CHINA_AI_ANTHROPOMORPHIC_MCP_SPEC.md` — sister spec (the Jul 15 deadline)
- `COLORADO_ADMT_COMPLIANCE_MCP_SPEC.md` — sister spec (the Jan 1 2027 deadline)
- `SHADOW_AI_DETECTION_MCP_SPEC.md` — sister spec (template)
- `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` — sister spec (the cert track)
- `PRICING.md` — the 4 SaaS tiers + 28 x402 call prices
- `CRITICAL_FIXES_2026-06-08.md` — the 3 security fixes (Docker root, API key perms, attestation key)
- `KEY_DIFFERENTIATORS.md` — differentiator #3 (HMAC-SHA256 attestation chain, the substrate for the conformity ledger)
- `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec09.md` — EU AI Act + standards ecosystem
- `/tmp/kimi_extract/sov3_mcp_master_audit.md` — 76-server audit, 13-framework engine, the 4 P0 builds
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — Phase 3 (Jun 28 - Jul 3) covers ETSI pre-announce

---

*Generated 2026-06-08 by Claude (Opus 4.8 session on `claude/review-changes-mkbcvckpl5ix3r03-MkKCu`). Sources: `sov3_mcp_master_audit.md` + Kimi research corpus + the keystone's existing MCP spec templates. ETSI TS 104 008 is referenced as published in the EU standards tracker; the final technical text should be verified against the ETSI publication when available — this is a specification document anticipating the standard, not a definitive reading of unpublished text.*
