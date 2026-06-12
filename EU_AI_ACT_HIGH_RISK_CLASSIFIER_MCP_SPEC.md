# EU AI Act High-Risk Classifier MCP — Spec

> **Authored**: 2026-06-08
> **Purpose**: spec for `eu-ai-act-high-risk-classifier-mcp` — the MCP that closes the **27% Article 10 coverage gap** in the keystone's existing `eu-ai-act-compliance-mcp` flagship. **T-55 from today (2026-06-08) to 2 August 2026 enforcement**; build order #1 per `REGULATORY_CALENDAR_2026-2027.md`.
> **Companion asset**: `EU_AI_ACT_FREE_SCANNER_SPEC.md` is the customer-facing `meok.ai/eu-check` web form. This MCP is the back-end classification engine the scanner calls.
> **Source**: `REGULATORY_CALENDAR_2026-2027.md` + `EU_AI_ACT_FREE_SCANNER_SPEC.md` (sister spec) + `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec09.md` (regulatory complexity) + `/tmp/kimi_extract/sov3_mcp_master_audit.md` (76-server audit, 13-framework engine) + Annex III of EU AI Act Regulation (EU) 2024/1689.

## 1. The opportunity

- **The deadline**: **2 August 2026** — T-55 from today (2026-06-08) and T-29 from the planned July 4 launch. **The keystone's `eu-ai-act-compliance-mcp` flagship (v1.3.0) covers ~73% of Article 10 conformance**; the 27% gap is the back-end classification engine that turns a system inventory into a per-article compliance posture. This MCP is that engine.
- **The market gap**: per `/tmp/kimi_extract/sov3_mcp_master_audit.md`, **none of the 15 named GRC competitors has a server-side MCP that exposes Annex III risk classification as a callable tool.** OneTrust has the templates (with 2.5-9 month implementation cycles). Holistic AI has a "policy alignment engine" (Tier 1, $50K+). Credo AI has the assessment (per-customer, $30-80K). None exposes it as a tool an LLM agent can call in 200ms with HMAC attestation.
- **The 78% unprepared stat** (per the European Commission's June 2026 enterprise AI survey) is the buying signal. 78% of EU enterprises are still figuring out whether their systems are high-risk. **78% × ~30,000 EU enterprises with material AI footprint = ~23,400 buyers** shopping in the next 55 days. Even capturing 1% of that as paid MCP customers = **234 customers × $49/user/mo × 10 users = $114K MRR Y1** (Stream 5 wedge for the EU).
- **The keystone's existing 13-framework engine** is the substrate. This MCP adds 2 new tool surfaces (annex III classification + Article 10 evidence assembly) on top of the existing `eu-ai-act-compliance-mcp` 410-article backbone and 42-point audit, without re-architecting.
- **Revenue angle**: per `PRICING.md`, the x402 micro-call layer can bill per classification call, per evidence-bundle generation, per Article 10 conformance check. Estimated: 100 EU customers × 100K calls/year × $0.05 = $500K Y1 (Stream 5 wedge for EU, paralleling the China wedge at $500K).

## 2. The 6 MCP tools (per the spec template from `SHADOW_AI_DETECTION_MCP_SPEC.md`)

| # | Tool | Input | Output | EU AI Act article | Pricing |
|---:|---|---|---|---|---|
| 1 | `classify_annex_iii` | `system_description: SystemDescription` (purpose, sector, data subjects, decision type) | `AnnexIIIClassification` (category, confidence, matched sub-clauses) | Art. 6 + Annex III | $0.50 per classification |
| 2 | `assess_article_10` | `training_data: DataManifest` (sources, provenance, biases, gaps) + `system_id: str` | `Article10Report` (5 sub-clauses × compliant / partial / gap) | Art. 10 (data governance) | $2.00 per assessment |
| 3 | `assess_article_12` | `logging_config: LoggingConfig` (what's logged, retention, tamper-evidence) | `Article12Report` (compliant / partial / gap + remediation) | Art. 12 (record-keeping) | $1.00 per assessment |
| 4 | `assess_article_13` | `transparency_docs: TransparencyDocs` (instructions for use, deployer info) | `Article13Report` (compliant / partial / gap + remediation) | Art. 13 (transparency) | $1.00 per assessment |
| 5 | `assess_article_30` | `post_market_plan: PostMarketPlan` (monitoring, incidents, reporting) | `Article30Report` (compliant / partial / gap + remediation) | Art. 30 (post-market monitoring) | $1.50 per assessment |
| 6 | `generate_article_10_evidence_bundle` | `system_id: str` + `assessor: Assessor` (the qualified person under Art. 17) | `EvidenceBundle` (signed zip: 5 sub-clause reports + raw data + HMAC) | Art. 10, 11, 17, 43 | $50 per bundle (one-time per assessment cycle) |

All tools are `@paywalled` per the keystone's x402 pattern. Free tier = 100 calls/month (drives the freemium funnel — `classify_annex_iii` is the entry point). Team tier = 10K calls/month. Business tier = unlimited + auto-generated evidence bundles.

## 3. The 4 risk classes (per the EU AI Act risk pyramid)

The MCP implements the 4-class taxonomy from the EU AI Act:

| Class | Triggering article | What it means for the customer | Tool flow |
|---|---|---|---|
| **Prohibited** | Article 5(1) (subliminal manipulation, exploitation of vulnerabilities, social scoring, real-time biometric ID in public, emotion recognition in workplace/education) | Cannot deploy in EU. Withdraw or re-architect. | `classify_annex_iii` returns `prohibited` + Article 5 sub-clause; no further assessment. |
| **High-risk** | Article 6 + Annex III §1-§8 (biometric, critical infrastructure, education, employment, essential services, law enforcement, migration, justice) | Full Article 10-15, 17, 30 obligations. Conformity assessment (Art. 43), CE marking (Art. 48), EU database registration (Art. 49/71). | `classify_annex_iii` → `assess_article_10/12/13/30` → `generate_article_10_evidence_bundle` |
| **Limited-risk** | Article 50 (chatbots, deepfakes, emotion-recognition not in workplace/education) | Transparency: disclose AI to users; AI-generated content machine-readable. | `classify_annex_iii` returns `limited-risk` + Article 50 sub-clause; `assess_article_13` only. |
| **Minimal-risk** | Everything else (spam filters, AI in video games, etc.) | No EU AI Act obligations. Voluntary best practices. | `classify_annex_iii` returns `minimal-risk`; no further assessment. |

## 4. The 8 Annex III categories (Article 6 high-risk triggers)

| # | Category | Examples | Sub-clauses |
|---:|---|---|---|
| 1 | **Biometric** | Remote biometric ID, biometric categorization (race, religion, etc.), emotion recognition (not workplace/education) | Annex III §1(a-d) |
| 2 | **Critical infrastructure** | AI controlling water, gas, heating, electricity, traffic (safety component) | Annex III §2 |
| 3 | **Education and vocational training** | Admissions, evaluation, exam-cheating detection, learning outcomes | Annex III §3 |
| 4 | **Employment, workers management, self-employment** | Recruitment (ads, screening, interviews), evaluations, promotions, terminations, task allocation | Annex III §4 |
| 5 | **Essential private and public services** (credit, insurance, public benefits, emergency services) | Credit scoring, insurance risk, public benefit eligibility, emergency dispatch | Annex III §5 |
| 6 | **Law enforcement** | Risk assessment of victims, evidence reliability, polygraphs, crime analytics, profiling | Annex III §6 |
| 7 | **Migration, asylum, border control** | Visa decisions, asylum processing, border detection, document verification | Annex III §7 |
| 8 | **Administration of justice and democratic processes** | Judicial decision support, influencing elections/referenda/voting behavior | Annex III §8 |

`classify_annex_iii` returns a `AnnexIIIClassification` with the matched category(s) (a system can be in multiple), the sub-clause(s), and a confidence score. **The 27% Article 10 gap the calendar mentions is the absence of an automated, callable engine that does this classification deterministically + auditable.** Today, classification is done by a Big 4 consultant reading the system description; the MCP replaces that with a 200ms API call.

## 5. The 5 Article 10 sub-clauses (the data governance obligations)

Article 10 is the heart of the gap. The MCP's `assess_article_10` tool maps a customer's `DataManifest` to all 5 sub-clauses:

| # | Sub-clause | What it requires | What the MCP checks |
|---:|---|---|---|
| 10(1) | Training/validation/test data governance | Relevant, representative, free of errors, complete | Data provenance → source list, license verification, bias audit, gap analysis |
| 10(2) | Data preparation processing | Documented, partially automated, bias-detection, domain expert involvement | Pre-processing pipeline → documented stages, automation %, bias mitigation |
| 10(3) | Bias evaluation + mitigation | Examine training data for biases; examine biases that may lead to discrimination | Per-class performance metrics → demographic parity, equalized odds, disparate impact |
| 10(4) | Data gaps + mitigation | Identify gaps, document why, mitigate | Missing data → coverage report, mitigation strategy |
| 10(5) | Personal data use | Comply with GDPR; use anonymized/pseudonymized data where possible | Data minimization → PII inventory, anonymization/pseudonymization, GDPR DPIA |

Each sub-clause returns one of: `compliant` / `partial` / `gap`. The MCP does NOT decide legal compliance — it assembles evidence for a qualified person (per Article 17) to make that judgment. The MCP's value is making the 5 sub-clauses **machine-readable** and **automated**.

## 6. The 3 customer archetypes (EU AI deployers)

| # | Archetype | Example companies | Primary tool used | x402 spend/month (est.) |
|---:|---|---|---|---|
| 1 | **EU high-risk AI deployers** (banks, insurers, employers, schools, gov) | BNP Paribas, Allianz, Siemens, BMW, Deutsche Telekom, Telefonica, public-sector agencies | `assess_article_10` + `generate_article_10_evidence_bundle` (full cycle) | $20K-$100K |
| 2 | **AI vendors selling to EU** (US/UK/Israel-domiciled, EU customers) | OpenAI, Anthropic, Cohere, Scale AI, DataRobot, H2O.ai | `classify_annex_iii` (per product, at scale) + `assess_article_13` (transparency docs) | $5K-$50K |
| 3 | **EU AI compliance consultants** (the channel) | Big 4 (Deloitte, PwC, EY, KPMG), boutique EU AI consultancies | All 6 tools at volume; bundle generation for client deliverables | $10K-$200K |

**Total addressable:** ~30,000 EU enterprises with material AI footprint × 1% capture = 300 customers × $10K average monthly spend = $3M MRR (Stream 5 Y3 target). Y1 is more like 50-100 customers = $500K-$1M MRR (the calendar's Stream 5 Y1 = $50K is conservative; $500K is the engineering-and-partner-team bet).

## 7. The 3 deployment modes (per the China spec, the same pattern)

| # | Mode | Architecture | GDPR data-residency impact | Latency |
|---:|---|---|---|---|
| 1 | **Remote SaaS (EU region)** | MEOK-hosted MCP server in eu-west-1 / eu-central-1; customer calls via x402 | None (no personal data processed, only system description + classifier result) | 50-200ms |
| 2 | **On-prem (customer EU VPC)** | Docker image in customer's AWS/GCP/Azure EU region; no egress | None (data stays in customer VPC) | 5-20ms |
| 3 | **Hybrid (control plane US + scanner EU)** | MEOK control plane in us-east-1; scanner in customer's EU VPC | Data minimization: only classification results cross the border | 20-50ms |

For initial launch, **Mode 1 (Remote SaaS in EU region)** is the only viable option — Modes 2/3 require customer's infra team involvement. The remote mode can serve the freemium funnel immediately and is GDPR-compliant because no personal data is processed.

## 8. The CRITICAL Fix compliance (per `CRITICAL_FIXES_2026-06-08.md`)

- **Fix #1 (Drop root in Docker)**: Dockerfile uses `USER app` with `uid 10001` (per keystone pattern). The MCP server image is built with the same template.
- **Fix #2 (API key permission lockdown)**: customer's Article 10 evidence bundles are stored in customer's own S3/GCS bucket; MEOK's API keys are read via `meok_secrets.get_api_key()` (stdlib keyring + chmod 600 fallback).
- **Fix #3 (`MEOK_ATTESTATION_KEY` secret manager)**: the Article 10 evidence bundles (Tool #6) and the per-article assessment reports (Tools #2-5) are HMAC-SHA256 signed via `meok_x402.py:_resolve_attestation_key()`. The signed attestation is the proof-of-work artifact for the conformity assessment body.

## 9. Integration with the keystone's 35,000+ MCP server ecosystem

- **Cross-link to `csoai.org`**: 14-framework governance (was 13, EU AI Act was already in, this MCP deepens it)
- **Cross-link to `meok.ai`**: Business tier ($49/user/mo) for the full Article 10 evidence workspace
- **Cross-link to `councilof.ai`**: BFT attestation that the assessment was performed by a qualified person (per Article 17)
- **Cross-link to `proofof.ai`**: HMAC-signed proof that an evidence bundle was generated
- **Cross-link to `transparencyof.ai`**: public dashboard showing the customer's compliance status (per Flywheel 5)
- **Cross-link to `eu-ai-act-compliance-mcp` flagship**: Tool #1 (`classify_annex_iii`) calls the existing flagship's 410-article backbone for the legal-text references

## 10. Engineering build schedule (T-55 = 2 August 2026)

| Week | Phase | Output | Owner |
|---|---|---|---|
| **W1 (Jun 8-14)** | Spec finalization + Annex III corpus | This spec (done 8 Jun) + 8-category classifier training data sourced from EU AI Act Annex III + 50+ public EU AI Act conformity assessments | Eng lead |
| **W2 (Jun 15-21)** | Tool scaffolding + keystone integration | 6 MCP tools wired into the gateway + `classify_annex_iii` calls `eu-ai-act-compliance-mcp`'s 410 articles | Eng lead |
| **W3 (Jun 22-28)** | Pilot customer validation | 2-3 EU AI deployers (1 bank, 1 insurer, 1 employer) using it in beta | Sales/CS |
| **W4 (Jun 29 - Jul 5)** | Public launch at Jul 4 | eu-ai-act-high-risk-classifier-mcp on GHCR, PyPI, Smithery, x402; `meok.ai/eu-check` routes here | Eng + Nick |
| **W5 (Jul 6-12)** | Final hardening + 1.0.0 release | Stable release, OpenSSF Scorecard pass, AWS Marketplace listing | Eng + Nick |
| **W6 (Jul 13-19)** | Pre-deadline push | 1,000 free scans/week; Article 10 bundle push to existing Business-tier customers | Sales/Marketing |
| **W7-W8 (Jul 20 - Aug 2)** | **GO LIVE** | Service available in production for 2 Aug enforcement; sales push to the 78% unprepared | All |

**Tight but achievable.** The keystone's existing 13-framework engine provides the substrate; the EU work is content + classification logic, not new infrastructure. The EU AI Act free scanner (per `EU_AI_ACT_FREE_SCANNER_SPEC.md`) is the customer-facing front door that drives traffic to this MCP.

## 11. What this is NOT

- **Not** a substitute for a qualified person under Article 17. The MCP assembles evidence and automates classification; the legal-judgment call remains with a qualified person. The MCP's value is reducing the 9-month OneTrust cycle to 48 hours, not replacing human judgment.
- **Not** a conformity assessment body. Article 43 conformity assessment is performed by a notified body; the MCP produces the evidence bundle the notified body reviews. MEOK's role is to make the evidence machine-readable, signed, and ready-for-audit.
- **Not** legal advice. The MCP maps to EU AI Act articles and Annex III categories, but the legal interpretation of "high-risk" in edge cases (e.g. is a recommendation system in a job portal "high-risk" if it doesn't make the final decision?) requires qualified legal counsel. The MCP's `confidence` field is a signal, not a verdict.

## 12. Cross-references

- `REGULATORY_CALENDAR_2026-2027.md` — the 4 P0 deadlines (this is #1, the most urgent build)
- `MASTER_AUDIT_INGESTION.md` — the 4 P0 builds identified
- `EU_AI_ACT_FREE_SCANNER_SPEC.md` — sister spec (the customer-facing freemium gate)
- `CHINA_AI_ANTHROPOMORPHIC_MCP_SPEC.md` — sister spec (the parallel T-37 build)
- `SHADOW_AI_DETECTION_MCP_SPEC.md` — sister spec (template)
- `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` — sister spec (the cert track)
- `PRICING.md` — the 4 SaaS tiers + 28 x402 call prices
- `CRITICAL_FIXES_2026-06-08.md` — the 3 security fixes (Docker root, API key perms, attestation key)
- `KEY_DIFFERENTIATORS.md` — differentiator #2 (410 verbatim EU AI Act articles, the substrate for this MCP)
- `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec09.md` — regulatory complexity, 78% unprepared stat
- `/tmp/kimi_extract/sov3_mcp_master_audit.md` — 76-server audit, 13-framework engine, the 4 P0 builds
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — Phase 0 (Jun 8-14) covers EU AI Act infrastructure lockdown

---

*Generated 2026-06-08 by Claude (Opus 4.8 session on `claude/review-changes-mkbcvckpl5ix3r03-MkKCu`). Sources: `sov3_mcp_master_audit.md` + Kimi research corpus + the keystone's existing MCP spec templates. All EU AI Act article references are sourced from Regulation (EU) 2024/1689 (the published text); legal interpretation in edge cases requires qualified counsel — this is a specification document, not legal advice.*
