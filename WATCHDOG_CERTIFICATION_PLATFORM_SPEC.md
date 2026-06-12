# Watchdog Certification Platform — Spec

> **Authored**: 2026-06-08
> **Purpose**: spec for the Watchdog certification platform. Gap #14 from `sov3_state_of_empire.agent.final.md` § 5.1 "Medium Gaps" (post-launch acceptable) BUT per the feature matrix "Nobody Has This" table, **AI Governance Certification is a SOV3-Only capability with 9-12 month replication time** — so we should accelerate it into Phase 2 of the launch.
> **Source**: `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` Category 4 (Certification & Training, lines 531-620) + `/tmp/kimi_dossier_v2/sov3_state_of_empire.agent.final.md` § 4.1 Tier 1+2 (Cranium, Holistic AI).
> **Upstream**: `/Users/nicholas/meok-compliance-gateway/MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` (the RFC for certifying MCP servers — this is the content corpus for the Watchdog exam).

## 1. The opportunity

- **The market**: per the feature matrix, 0/15 competitors have AI Governance Certification as a product. Cranium = best at 4/15 (training certs only, not product certs). Every other competitor = 0/15.
- **The moat**: SOV3 unique advantage #5 (per `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` "SOV3 Unique Advantages" table) — 9-12 month replication time. First-mover locks the category.
- **The substrate**: the keystone already has HMAC-SHA256 signed attestations (see `CRITICAL_FIXES_2026-06-08.md` Fix #3 + `meok_x402.py:66-126` attestation key resolution). The Watchdog certs are the natural extension.
- **The content corpus**: the keystone's 410 verbatim EU AI Act articles (`KEY_DIFFERENTIATORS.md` differentiator #2) + the MCP Security Certification Standard RFC = the exam content.
- **The 3 cert tiers**:
  1. **AI Governance Foundations** (individual, $99 exam + $29/yr renewal) — entry-level.
  2. **AI Governance Professional** (individual, $299 exam + $99/yr renewal) — practitioner.
  3. **AI Governance System Certification** (product/MCP, $5K-$25K) — system-level.

## 2. The 3 cert tiers — detailed

| Tier | Name | Audience | Format | Pass mark | Cost | Renewal |
|---:|---|---|---|---|---|---|
| 1 | **AI Governance Foundations** | Compliance analysts, GRC practitioners, AI ethics officers | 60-min online, 50-question MCQ | 70% | $99 exam | $29/yr (10-question refresher) |
| 2 | **AI Governance Professional** | Senior compliance officers, AI risk managers, MCP server operators | 2-hour proctored, 80 questions (60% MCQ + 40% short essay) | 75% | $299 exam | $99/yr (30-question refresher + 1 case study) |
| 3 | **AI Governance System Certification** | MCP server products, AI products, governance platforms | 4-6 week audit + 1-year validity | Pass = no Critical / ≤ 3 High findings | $5K (single MCP) / $25K (multi-component product) | Annual re-cert ($2K-$10K) |

## 3. Exam content outline (Tier 1 + Tier 2)

### Tier 1 — AI Governance Foundations (50 questions, 60 min)

| Domain | # questions | Source corpus | Sample question topic |
|---|---:|---|---|
| EU AI Act basics | 15 | 410 verbatim articles (Key Differentiator #2) | "Which article defines high-risk classification?" |
| NIST AI RMF | 8 | NIST AI RMF 1.0 (GOVERN / MAP / MEASURE / MANAGE) | "Which function covers AI system decommissioning?" |
| ISO 42001 | 7 | ISO/IEC 42001:2023 | "What is the role of the AI management system owner?" |
| GDPR + dataprivacy | 6 | dataprivacyof.ai hive content | "When is DPIA mandatory under GDPR Article 35?" |
| MCP Security | 5 | MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md | "What is the minimum OpenSSF Scorecard for Tier-1 MCP?" |
| HMAC attestations | 4 | CRITICAL_FIXES_2026-06-08.md | "What is the purpose of HMAC-SHA256 in compliance attestations?" |
| BFT consensus | 3 | sov3_tech_blueprint.agent.final.md | "What does Byzantine Fault Tolerance guarantee?" |
| x402 micropayments | 2 | mcp-x402-bazaar-micropayments memory | "What is the role of x402 in MCP governance?" |

### Tier 2 — AI Governance Professional (80 questions, 2 hours, proctored)

Inherits all of Tier 1's content plus:

| Domain | # questions | Format | Source corpus |
|---|---:|---|---|
| EU AI Act deep-dive (Articles 6, 10, 12, 13, 30, 50) | 20 | 14 MCQ + 6 short essay | 410 verbatim articles |
| MCP server security audit | 10 | 6 MCQ + 4 short essay | MCP Security Cert RFC + OpenSSF Scorecard 18 checks |
| Risk classification (high-risk / limited / prohibited) | 8 | All MCQ | EU AI Act + EU_AI_ACT_FREE_SCANNER_SPEC |
| HMAC attestation implementation | 6 | 3 MCQ + 3 short essay | meok_x402.py:66-126 + meok_secrets.py |
| BFT consensus design | 4 | 2 MCQ + 2 short essay | sov3_tech_blueprint § "Consensus Protocol" |
| Industry-specific applications (financial, healthcare, transport) | 10 | All MCQ | 7 industry packs (per sov3_state_of_empire § 6 W9) |
| Incident response + revocation | 6 | 3 MCQ + 3 short essay | Watchdog platform design (this spec) |
| Audit + cert lifecycle management | 6 | All MCQ | Watchdog platform design (this spec) |
| Cross-framework harmonization | 4 | All MCQ | 13-framework engine spec |
| Watchdog-specific policies + rubric | 6 | All MCQ | Watchdog policies (this spec) |

## 4. The "verified forever" UX

Every cert has a public URL: `meok.ai/verify/<cert_id>`.

The page shows:
- Holder name (for individual Tier 1/2) or product name (for Tier 3 system)
- Tier (1 / 2 / 3)
- Issue date
- Expiry date
- HMAC-SHA256 signature (truncated for display, full in the JSON payload)
- The signed JSON payload (downloadable)

**Verifier flow** (third-party auditor, regulator, customer):
1. Visit `meok.ai/verify/<cert_id>`.
2. Download the JSON payload.
3. Verify the HMAC-SHA256 signature against MEOK's published public key.
4. Confirm: ✓ Authentic, ✓ Not expired, ✓ Holder matches.

Verification is fully offline. No MEOK server required. The HMAC public key is published at `meok.ai/keys/public.pem` and pinned via DNS SEC where registrars support it.

This is the same HMAC-SHA256 substrate as the compliance attestations (`CRITICAL_FIXES_2026-06-08.md` Fix #3) — shared infrastructure, no new signing service needed.

## 5. The proctoring + anti-cheat story

| Tier | Proctoring | ID check | Anti-cheat |
|---|---|---|---|
| 1 — Foundations | None (low-stakes) | Email verification only | Time limit + randomization |
| 2 — Professional | Webcam + ID upload (Proctorio-style) | Government-issued ID | Webcam monitoring + tab-switch detection + behavioral analysis |
| 3 — System Cert | Third-party auditor (CPA, ex-Big-4 compliance consultant) | Auditor's professional credentials | Manual audit of submitted artifacts |

**Cheating consequences**:
- Cert revocation (HMAC-signed public revocation list at `meok.ai/revocations`).
- 5-year ban from re-taking.
- The ban + revocation are HMAC-signed → verifiable by third parties.

## 6. The MCP cert pipeline (Tier 3) — 7 steps

1. **Step 1**: Submit the MCP server's `server.json` + Dockerfile + repo URL + CI logs + OpenSSF Scorecard badge.
2. **Step 2**: Auto-scan for 18 OpenSSF Scorecard checks (run the keystone's scorecard workflow). Must score ≥ 7.0/10.
3. **Step 3**: Static analysis: dependency tree (no known-vulnerable deps), license check (MIT/Apache-2.0 only), no-root container (Dockerfile: USER app), file permissions audit (no world-writable files), no `printenv` of secrets (per `CRITICAL_FIXES_2026-06-08.md`).
4. **Step 4**: Manual review by a Watchdog auditor (Senior tier or above). 1-2 weeks turnaround. Auditor uses the keystone's MCP Security Cert RFC rubric.
5. **Step 5**: Issue a 1-year cert with public verify URL + HMAC signature. Publish to `meok.ai/registry/certified-mcps`.
6. **Step 6**: Quarterly re-check (automated). Auto-revoke if any Critical finding appears (e.g., dependency CVE published, OpenSSF score drops below 7.0).
7. **Step 7**: Annual recertification (manual review). New HMAC-signed cert issued, prior cert moved to `meok.ai/registry/expired-mcps`.

## 7. The auditor network

**Recruit 20-50 Watchdog auditors globally** (CPAs, compliance consultants, ex-Big-4).

**Revenue split**: 70% to auditor, 30% to MEOK. Auditors set their own rates; MEOK caps at $10K per Tier-3 cert to keep market prices down.

**Auditor onboarding**:
1. Pass Tier 2 Watchdog cert (proctored).
2. Complete 1-day MCP-specific training (free, online).
3. Sign the Watchdog auditor code of conduct (HMAC-signed).
4. Pass a 5-question calibration test (peer-reviewed by 2 existing auditors).

**Auditor tiers**:
- **Junior** ($200/hr): reviews Tier 1 challenges (Tier 1 cert takers who appeal a fail).
- **Senior** ($350/hr): reviews Tier 2 challenges + Tier 3 MCP cert audits.
- **Principal** ($500/hr): reviews Senior-tier escalations + signs off on Tier 3 system certs.

**Year-2 ramp**: 50 auditors × $200K each (1,000 hours/year at avg $200/hr) = $10M through-flow, 30% to MEOK = $3M ARR from auditor network alone.

## 8. Build order (2 weeks)

**Week 1**:
- Day 1-2: Exam content (Tier 1 + Tier 2) — pull from § 3 sources.
- Day 3-4: Cert signing infrastructure — wire to `meok_x402.py:66-126` attestation key resolution.
- Day 5: Public verify URL + JSON payload schema + revocation list.

**Week 2**:
- Day 6-7: Tier 3 MCP cert pipeline (the 7 steps in § 6).
- Day 8-9: Auditor onboarding flow + 5-10 pilot auditors.
- Day 10: 5-10 pilot certs (mix of Tier 1 individuals + Tier 3 MCPs).

**Stretch (post-week 2)**:
- Stripe integration for cert purchase.
- Pearson VUE / Prometric partnership for proctored Tier 2.
- Watchdog-branded LinkedIn / X / YouTube presence.

## 9. The 5-lever revenue impact

| Lever | Math | Year-2 potential |
|---|---|---:|
| Tier 1 exam revenue | 10,000 exams/yr × $99 | $990K |
| Tier 1 renewals | 10,000 × 50% renewal × $29 | $145K |
| Tier 2 exam revenue | 2,000 exams/yr × $299 | $600K |
| Tier 2 renewals | 2,000 × 50% renewal × $99 | $99K |
| Tier 3 system certs | 200 systems/yr × $15K avg | $3,000K |
| Tier 3 renewals | 200 × 80% renewal × $5K avg | $800K |
| Auditor network through-flow | 50 auditors × $200K each × 30% | $3,000K |
| Training courses (companion) | 500 enrollments/yr × $499 | $250K |
| **Total Year-2 potential** | | **~$8.9M** |

This is a category, not a product.

## 10. The 4 risks + mitigations

| Risk | Mitigation |
|---|---|
| 1. Slow cert exam delivery (we don't have a Pearson VUE partnership) | Phase 1: in-house proctoring via webcam. Phase 2: Pearson VUE partnership for Tier 2 by Q4 2026. |
| 2. Auditor quality variance | Calibration tests + peer review + 5-question per-audit random audit. |
| 3. Competitor fast-follow (Cranium expands training certs) | First-mover advantage (9-12 months per the SOV3 unique advantage analysis) + open-source the Watchdog rubric (defensive). |
| 4. Customer reluctance to pay (preference for "free" governance) | Tier 1 = $99 entry barrier is low; Tier 3 system cert = $5K+ barrier is justified by the audit depth. Both are competitive with the market. |

## 11. Cross-references

- `/Users/nicholas/meok-compliance-gateway/MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` — the upstream RFC for MCP server certification.
- `/Users/nicholas/meok-compliance-gateway/CRITICAL_FIXES_2026-06-08.md` — HMAC-SHA256 signing infrastructure (the cert substrate).
- `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` — differentiator #2 (410 EU AI Act articles = exam corpus).
- `/Users/nicholas/meok-compliance-gateway/PRICING.md` — the subscription model that should bundle with cert.
- `/Users/nicholas/meok-compliance-gateway/REGULATORY_CALENDAR_2026-2027.md` — 4 P0 deadlines = exam urgency.
- `/Users/nicholas/meok-compliance-gateway/EU_AI_ACT_FREE_SCANNER_SPEC.md` — the free scanner is the funnel into Tier 1 certs.
- `/Users/nicholas/meok-compliance-gateway/SHADOW_AI_DETECTION_MCP_SPEC.md` — Shadow AI MCP should default to "Watchdog-certified" after launch.

## 12. Source pointers

- `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` § 4.1-4.6 (certification category).
- `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` "SOV3 Unique Advantages" #5 (9-12 month replication).
- `/tmp/kimi_dossier_v2/sov3_state_of_empire.agent.final.md` § 4.1 Tier 1+2 (Cranium, Holistic AI profiles).
- `/tmp/kimi_dossier_v2/sov3_state_of_empire.agent.final.md` § 5.1 gap #14 (build effort estimate).
- `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` (HMAC + BFT substrate).
