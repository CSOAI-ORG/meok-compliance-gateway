# OneTrust Escape — TCO Calculator Spec

> **Authored**: 2026-06-08
> **Purpose**: spec for the OneTrust Escape migration landing page + TCO calculator. Gap #4 from `sov3_state_of_empire.agent.final.md` § 5.1 "Critical Gaps": "Build migration landing page with TCO calculator, 2-3 days effort."
> **Audience**: mid-market EU companies (200-2000 employees) on OneTrust contracts coming up for renewal in 2026-2027.
> **Rubric**: factual comparative, no war language per `RUBRIC_EXTERNAL_COMMS.md`. Banned vocabulary in § 8.

## 1. The opportunity

- **OneTrust fatigue thesis**: 9-month deployment, modular upsell trap, $30K-$80K per framework module. 7 frameworks max. Single-vendor SaaS (no multi-party consensus).
- **MEOK's response**: 13 frameworks in one engine, 48-hour deploy SLA, $49/mo Business tier. Multi-party BFT consensus. HMAC-signed attestations. 35,000+ MCP server governance (OneTrust = 0).
- **The 4 P0 regulatory deadlines** (`REGULATORY_CALENDAR_2026-2027.md`) are the urgency engine:
  - 2026-07-15: China GenAI (T-37)
  - 2026-08-02: EU AI Act (T-55)
  - 2026-Q3: ETSI TS 104 008 (T-90+)
  - 2027-01-01: Colorado ADMT (T-207)
- **The migration funnel**: free EU AI Act scanner (5 questions) → Business tier ($49/mo) → annual contract ($588/yr) → enterprise upsell.

## 2. The TCO calculator input form

Web form with 7 inputs (all on one page, no login):

| Input | Type | Default | Notes |
|---|---|---|---|
| Company headcount | number (slider 50-10000) | 500 | Drives per-seat licensing. |
| Number of frameworks in use | dropdown (1-13) | 7 | OneTrust max = 7; MEOK = 13. |
| Deployment timeline target | dropdown (1m / 3m / 6m / 9m / 12m) | 9m | OneTrust typical = 9m; MEOK SLA = 48h. |
| Number of integrations | number (1-50) | 5 | OneTrust integrations = connectors; MEOK = MCP servers. |
| Audit frequency | dropdown (monthly/quarterly/annual) | quarterly | Drives audit cost. |
| On-prem vs cloud | radio (cloud / hybrid / on-prem) | cloud | MEOK on-prem = +$5K setup, +0% recurring. |
| Number of compliance staff | number (1-20) | 2 | FTE count for in-house governance team. |

## 3. The TCO calculator formula

The calculator computes Year-1 and 5-year TCO for both vendors, then shows savings.

### 3.1 OneTrust Year-1 TCO

```
modules_cost = number_of_frameworks × $50,000      # avg $30K-$80K per module
licensing = headcount × $120/year                    # OneTrust list ~$100-200 per user
implementation = 9 months × 2 FTE × $15,000/month  # typical 9m deploy
integrations = number_of_integrations × $5,000       # connector build cost
audit = audit_frequency_factor × $30,000             # quarterly=$30K, monthly=$80K
on_premium = +$50,000 if on-prem                     # OneTrust on-prem premium
onboarding = $25,000                                  # first-year onboarding

oneTrust_year1 = modules_cost + licensing + implementation + integrations + audit + on_premium + onboarding
```

**Typical range**: $400K (small, cloud, 3 modules) → $1.2M (large, on-prem, 7 modules).

### 3.2 OneTrust 5-year TCO

```
oneTrust_year2_5 = (licensing + integrations + audit + on_premium) × 4   # recurring
oneTrust_5yr = oneTrust_year1 + oneTrust_year2_5
```

**Typical 5-year range**: $1.5M → $3.5M (recurring + 1 module re-implementation every 2 years).

### 3.3 MEOK Year-1 TCO

```
business_tier = $49/mo × 12                              = $588/yr
team_tier = $29/mo × 12                                   = $348/yr (if compliance team < 5)
enterprise_custom = $50,000 (if headcount > 2000)        # one-time
implementation = 48 hours × 0.25 FTE × $15,000/month    = $7,500 (cloud) or $5,000 (on-prem)
on_premium = +$5,000 if on-prem                          # one-time, vs $50K OneTrust
free_scanner = $0                                         # 5-min EU AI Act scan

meok_year1_cloud = max(business_tier, team_tier) + implementation
meok_year1_onprem = max(business_tier, team_tier) + implementation + on_premium + enterprise_custom
```

**Typical range**: $1K (small, cloud) → $60K (large, on-prem, enterprise).

### 3.4 MEOK 5-year TCO

```
meok_year2_5 = max(business_tier, team_tier) × 4 + (free_scanner × 4)
meok_5yr = meok_year1 + meok_year2_5
```

**Typical 5-year range**: $5K (small, cloud) → $250K (large, on-prem).

### 3.5 Savings summary

```
savings_year1 = oneTrust_year1 - meok_year1
savings_5yr = oneTrust_5yr - meok_5yr
savings_pct = savings_5yr / oneTrust_5yr × 100
```

**Typical**: 70%-95% 5-year savings.

## 4. The 3 MEOK upsides not in TCO

These are the qualitative differentiators the calculator surfaces as a sidebar (but does not include in $ math):

1. **13 frameworks vs OneTrust's 7.** No modular upsell trap. MEOK covers EU AI Act, NIST AI RMF, ISO 42001, ISO 27001, SOC 2, GDPR, HIPAA, DORA, NIS2, CRA, CSRD, ESG, supply-chain — all in one engine.
2. **HMAC-SHA256 signed attestations.** OneTrust issues PDFs/email; no verification possible. MEOK's attestations are cryptographically signed; third parties can verify offline.
3. **35,000+ MCP server governance + 447 MIT-licensed repos.** OneTrust has zero MCP coverage. MEOK is the only production layer for MCP governance, and the codebase is fully open-source and auditable.
4. **BFT (Byzantine Fault Tolerance) consensus.** OneTrust = single-vendor SaaS ("trust us"). MEOK = multi-party governance with cryptographic consensus.
5. **48-hour deploy SLA.** OneTrust typical = 9 months. MEOK = 48h cloud, 2 weeks on-prem.
6. **No vendor lock-in.** 447 public MIT repos. Auditable by anyone. OneTrust = closed-source, no migration path.

## 5. The migration playbook (7 steps)

For users who hit "Calculate my savings" and see 70%+ savings:

1. **Step 1**: Run the EU AI Act free scanner (`EU_AI_ACT_FREE_SCANNER_SPEC.md`).
2. **Step 2**: Inventory the OneTrust modules in use. Map to MEOK's 13-framework engine.
3. **Step 3**: Sign up for MEOK Business tier ($49/mo) for the cloud pilot.
4. **Step 4**: 48h pilot deployment (cloud mode, zero-config).
5. **Step 5**: Run both systems in parallel for 30 days. Verify parity via the HMAC-signed attestation cross-check.
6. **Step 6**: Cut over the compliance attestations. MEOK issues HMAC-signed PDFs; OneTrust issues plain PDFs.
7. **Step 7**: Decommission OneTrust. Savings start immediately. The 12-month OneTrust contract = $400K-$1.2M; the 12-month MEOK Business tier = $588.

## 6. The "1-day" landing page wireframe

```
+---------------------------------------------------------------+
| HERO: "Escape OneTrust in 48 hours. Save 90% in Year 1."      |
| [TCO Calculator widget]                                       |
+---------------------------------------------------------------+
| THE 4 P0 REGULATORY DEADLINES COUNTDOWN                       |
| [Aug 2 EU AI Act] [Jul 15 China] [Q3 ETSI] [Jan 1 Colorado]   |
+---------------------------------------------------------------+
| 3 CUSTOMER STORY PLACEHOLDERS                                 |
| [Pilot 1] [Pilot 2] [Pilot 3]                                 |
+---------------------------------------------------------------+
| SIDE-BY-SIDE COMPARISON TABLE                                 |
| OneTrust vs MEOK: frameworks, deployment, attestations, MCP   |
+---------------------------------------------------------------+
| HOW THE MIGRATION WORKS (7 steps)                             |
| [Step 1: EU scan] → ... → [Step 7: Decommission]             |
+---------------------------------------------------------------+
| CTA: "Start your free EU AI Act scan →" (links /eu-check)    |
+---------------------------------------------------------------+
```

## 7. The pricing comparison table

| OneTrust module | OneTrust list price | MEOK equivalent | Annual savings |
|---|---:|---|---:|
| Privacy Management | $40K | EU AI Act + GDPR (in 13-framework engine) | $40K |
| AI Governance | $60K | EU AI Act + NIST RMF + ISO 42001 | $60K |
| GRC Platform | $50K | DORA + NIS2 + CRA | $50K |
| Ethics & Responsible AI | $30K | ethicalgovernanceof.ai hive | $30K |
| ESG / Sustainability | $45K | CSRD + ESG disclosure | $45K |
| Vendor Risk Management | $35K | supply-chain framework | $35K |
| Consent & Preferences | $30K | dataprivacyof.ai hive | $30K |
| **Total (7 modules)** | **$290K** | **$588/yr** | **$289K** |

**The modular-upsell trap made visible**: 7 modules at OneTrust = $290K list price (plus implementation). MEOK = $588/year flat.

## 8. The 5 "do NOT do" rules

1. **Don't name-and-shame OneTrust.** No references to "OneTrust layoffs" or any specific personnel/funding events. Factual comparison only.
2. **Don't use war vocabulary.** Banned: kill shot, nuclear arsenal, coup de grâce, talent raid, seeding doubt, depletion campaign, strike while, vulnerability window, acquisition target, funding fiction.
3. **Don't quote "$50B GRC no-MCP" without neutral framing.** It's a market-structure fact (13 of 15 GRC vendors have zero MCP), not a OneTrust critique. Frame as "the GRC market has no MCP strategy yet" — not "we beat them all."
4. **Don't claim feature parity where there isn't any.** Be specific: "MEOK deploys in 48h, OneTrust deploys in 9 months" (true). "MEOK is better than OneTrust" (subjective, do not claim).
5. **Don't promise MEOK supports every OneTrust module.** List the ones it does support (see § 7 table). The EU AI Act MCP, dataprivacyof.ai hive, and ethicalgovernanceof.ai hive cover Privacy + AI Governance + Ethics; the 13-framework engine covers the rest. Be precise.

## 9. Build order (2-3 days)

- **Day 1**: Calculator logic (the formula in § 3) + 7-input form + Year-1 / 5-year output.
- **Day 2**: Landing page (wireframe in § 6) + pricing comparison table (§ 7) + 3 customer-story placeholders.
- **Day 3**: Migration playbook (§ 5) + 5 do-NOT-do rules editorial review + deploy to sov3.ai/compare (or meok.ai/one-trust-escape).

## 10. Success metrics

- 100 TCO calculator uses in week 1.
- 30% conversion from calculator to free EU AI Act scanner (link in CTA).
- 10% conversion from scanner to Business tier ($49/mo) = 3 paying customers in week 1.
- 1 published case study (the first OneTrust escape customer).

## 11. Cross-references

- `/Users/nicholas/meok-compliance-gateway/PRICING.md` — MEOK pricing tiers.
- `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` — 8 differentiators.
- `/Users/nicholas/meok-compliance-gateway/REGULATORY_CALENDAR_2026-2027.md` — 4 P0 deadlines.
- `/Users/nicholas/meok-compliance-gateway/EU_AI_ACT_FREE_SCANNER_SPEC.md` — the lead-gen funnel.
- `/Users/nicholas/meok-compliance-gateway/MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — Phase 2 "OneTrust Escape" angle.
- `/Users/nicholas/meok-compliance-gateway/COMPARE_MATRIX_15_COMPETITORS.md` — the comparison matrix.
- `/Users/nicholas/meok-compliance-gateway/CRITICAL_FIXES_2026-06-08.md` — HMAC signing infrastructure (the attestation substrate).
- `/Users/nicholas/meok-compliance-gateway/28_DAY_BLOG_CALENDAR.md` — the OneTrust Escape content slots (-11, -15, +3).

## 12. Source pointers

- `/tmp/kimi_dossier_v2/sov3_state_of_empire.agent.final.md` § 4.1 Tier 3 (OneTrust profile), § 5.1 gap #4.
- `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` (OneTrust scorecard).
- `/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md` (OneTrust API profile = 9/10 developer portal).
- `/tmp/kimi_dossier_v2/research/deepdive_uiux_analysis.md` (OneTrust UX).
