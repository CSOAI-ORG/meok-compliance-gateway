# Colorado ADMT Compliance MCP — Spec

> **Authored**: 2026-06-08
> **Purpose**: spec for `colorado-admt-compliance-mcp` — the MCP that operationalizes **Colorado SB 24-205** ("Colorado AI Act"), specifically the **Algorithmic Decision-Making Tool (ADMT) consumer protection provisions** (Colorado Revised Statutes §6-1-1701 et seq., as amended by SB 24-205). **T-207 from today (2026-06-08) to 1 January 2027 enforcement**; build order #4 per `REGULATORY_CALENDAR_2026-2027.md`.
> **Companion asset**: `EU_AI_ACT_HIGH_RISK_CLASSIFIER_MCP_SPEC.md` (Aug 2), `CHINA_AI_ANTHROPOMORPHIC_MCP_SPEC.md` (Jul 15), `ETSI_CABCA_CONTINUOUS_CONFORMITY_MCP_SPEC.md` (Q3 2026).
> **Source**: `REGULATORY_CALENDAR_2026-2027.md` + `MASTER_AUDIT_INGESTION.md` + `/tmp/kimi_extract/nicholas_templeman_26domain_portfolio.agent.final.md` § "US State AI Laws" + `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec09.md` (US AI safety governance) + the keystone's existing MCP spec templates.
> **Rubric**: factual comparative, no war language per `RUBRIC_EXTERNAL_COMMS.md`. Banned vocabulary in § 11.

## 1. The opportunity

- **The deadline**: **1 January 2027** — T-207 from today (2026-06-08) and the LAST of the 4 P0 regulatory deadlines. Colorado SB 24-205 was signed into law in May 2024; the ADMT provisions (C.R.S. §6-1-1701 et seq.) take effect **February 1, 2026** for the developer/deployer notification program and **January 1, 2027** for the full impact-assessment + consumer-rights regime. The keystone has a 7-month runway, but the impact-assessment templates need to ship *before* the law takes effect for the early-adopter cohort.
- **Why this matters**: Colorado is the **first US state to enact a comprehensive AI law** with risk-based accountability obligations. The law's structure (impact assessments, consumer notification, opt-out, appeal rights, AG enforcement) is a **template that 15+ other US states are actively copying** (per `/tmp/kimi_extract/nicholas_templeman_26domain_portfolio.agent.final.md` § "US State AI Laws"). California, Illinois, New York, and Texas all have active bills referencing the Colorado framework. The MCP that wins in Colorado in 2027 wins the **US state-by-state cascade** in 2027-2028.
- **The market gap**: per `/tmp/kimi_extract/sov3_mcp_master_audit.md`, **none of the 15 named GRC competitors has a Colorado-ADMT-specific MCP.** OneTrust has the privacy templates (CCPA/CPRA), not ADMT. Holistic AI has a "policy alignment engine" but no US-state-ADMT-specific tooling. The closest is **BABL AI** (a small consultancy doing one-off ADMT assessments at $30-80K) and **Parity** (a startup with an ADMT-impact-assessment product at $15-30K/yr). Neither is a tool an LLM agent can call in 200ms with HMAC attestation.
- **The "1000-developer" inflection**: Colorado's ADMT regime requires **all developers and deployers** of "consequential decision-making" AI to (a) file an impact assessment with the AG, (b) notify consumers they are interacting with AI, (c) provide an opt-out or human-review process, and (d) maintain a public anti-discrimination policy. With ~5,000 enterprises operating ADMTs that affect Colorado consumers (employment, housing, credit, insurance, education, healthcare, government services), the addressable market is **larger than the EU AI Act high-risk set** but **less mature** in tooling. Capturing 1% = 50 customers × $10K average monthly spend = **$500K MRR Y1** (Stream 5 wedge for US, complementing EU + China + ETSI).
- **The keystone's existing 13-framework engine** is the substrate. This MCP adds 4 new tool surfaces (ADMT classification + impact-assessment generation + consumer-rights workflow + AG-report filing) on top of the existing `eu-ai-act-high-risk-classifier-mcp` Annex III engine and the keystone's HMAC-SHA256 attestation chain, without re-architecting.
- **Revenue angle**: per `PRICING.md`, the x402 micro-call layer can bill per ADMT classification, per impact-assessment generation, per consumer-rights API call, per AG-report filing. Estimated: 50 US customers × 50K calls/year × $0.05 = $125K Y1 (conservative); the $500K figure assumes enterprise tier (5 customers × $100K/yr).

## 2. The 6 MCP tools (per the spec template from `SHADOW_AI_DETECTION_MCP_SPEC.md`)

| # | Tool | Input | Output | Colorado SB 24-205 / C.R.S. §6-1-1701 et seq. | Pricing |
|---:|---|---|---|---|---|
| 1 | `classify_admt` | `system_description: SystemDescription` (purpose, sector, decision type, consumer impact) | `ADMTClassification` (in-scope / out-of-scope, sector, consequential-decision flag) | C.R.S. §6-1-1702(1) (ADMT definition) | $0.50 per classification |
| 2 | `generate_impact_assessment` | `system_id: str` + `adverse_impact_audit: AdverseImpactAudit` (demographic parity, equalized odds, disparate impact) | `ImpactAssessment` (16-section, AG-filing-ready) | C.R.S. §6-1-1703 (impact assessment) | $50 per assessment (one-time per assessment cycle, valid 24 months) |
| 3 | `register_consumer_rights_workflow` | `system_id: str` + `rights_config: RightsConfig` (notification, opt-out, appeal, human-review) | `ConsumerRightsWorkflow` (consumer-facing endpoints + audit log) | C.R.S. §6-1-1704 (consumer rights) | $5.00 per workflow registration |
| 4 | `consumer_rights_request` | `request: ConsumerRightsRequest` (consumer_id, request_type, system_id) | `ConsumerRightsResponse` (response, status, escalation path) | C.R.S. §6-1-1704(2)(c) (consumer right to appeal) | $0.50 per request |
| 5 | `file_ag_report` | `incident: Incident` (type, severity, consumer_impact, remediation) | `AGReport` (signed, ready for Colorado AG submission) | C.R.S. §6-1-1706 (AG enforcement, incident disclosure) | $20.00 per report |
| 6 | `admt_compliance_ledger` | `system_id: str` + `time_range: TimeRange` | `ComplianceLedger` (HMAC-chained log of classifications, assessments, rights-requests, AG-reports) | C.R.S. §6-1-1705 (record-keeping, 5-year retention) | $0.50 per query |

All tools are `@paywalled` per the keystone's x402 pattern. Free tier = 100 calls/month (drives the freemium funnel — `classify_admt` is the entry point). Team tier = 10K calls/month. Business tier = unlimited + auto-scheduled impact-assessment renewals.

## 3. The 8 ADMT sectors (C.R.S. §6-1-1702(1))

Colorado's ADMT regime covers AI systems that **make or substantially influence "consequential decisions"** in 8 sectors:

| # | Sector | Examples | Consequential decisions |
|---:|---|---|---|
| 1 | **Education** | K-12 and higher-ed admissions, grading, disciplinary, financial aid | Acceptance, grade, suspension, aid award |
| 2 | **Employment** | Hiring, firing, promotion, task assignment, performance evaluation | Hire/no-hire, promote/terminate, raise/bonus |
| 3 | **Essential government services** | Public benefits, law enforcement, immigration, voting | Eligibility, response, status, access |
| 4 | **Healthcare** | Diagnosis, treatment, insurance eligibility, triage | Care plan, coverage, priority |
| 5 | **Housing** | Tenant screening, lease approval, mortgage underwriting, property valuation | Approval, terms, occupancy |
| 6 | **Insurance** | Underwriting, pricing, claims, fraud detection | Coverage, premium, payout |
| 7 | **Financial services / lending** | Credit decisions, account closure, fraud detection | Approval, terms, account action |
| 8 | **Legal services** | Brief research, contract review, case-outcome prediction | Strategy, document handling, prediction |

`classify_admt` returns an `ADMTClassification` with the matched sector(s) (a system can be in multiple), the consequential-decision flag, and a confidence score. The 8 sectors **overlap substantially with the EU AI Act Annex III categories** (employment, education, credit, law enforcement, etc.), so the MCP can reuse the Annex III classification engine from `eu-ai-act-high-risk-classifier-mcp` and re-taxonomy it for Colorado's 8 sectors.

## 4. The 16-section impact assessment (C.R.S. §6-1-1703)

The MCP's `generate_impact_assessment` tool (Tool #2) generates a 16-section assessment per the statute:

| # | Section | What it requires | What the MCP fills in |
|---:|---|---|---|
| 1 | **System description** | Purpose, intended use, deployment context | Auto from `SystemDescription` |
| 2 | **Decision type** | What consequential decision it makes or influences | Auto from `ADMTClassification` |
| 3 | **Sector** | Which of the 8 sectors | Auto from classification |
| 4 | **Data sources** | Training/operational data sources, provenance | Auto from `DataManifest` |
| 5 | **Data minimization** | Whether personal data is minimized; anonymization/pseudonymization | Auto + manual confirmation |
| 6 | **Outputs and interpretation** | What the system outputs, how deployers interpret them | Manual |
| 7 | **Consumer population** | Demographics of affected consumers | Manual + auto from data |
| 8 | **Known disparities** | Pre-deployment disparate impact analysis | Auto from `AdverseImpactAudit` |
| 9 | **Bias mitigation** | Steps taken to mitigate identified biases | Manual |
| 10 | **Consumer notification** | How consumers are informed they're interacting with AI | Manual + linked to `consumer_rights_workflow` |
| 11 | **Opt-out / human review** | How consumers can opt out or request human review | Manual + linked to workflow |
| 12 | **Appeal process** | How consumers can appeal ADMT decisions | Manual + linked to `consumer_rights_request` |
| 13 | **Accuracy metrics** | Model performance metrics, broken down by demographic | Auto from model card |
| 14 | **Known limitations** | Known failure modes, edge cases, distribution shift risks | Manual |
| 15 | **Periodic review** | Schedule for re-assessment (at least every 24 months) | Auto-generated schedule |
| 16 | **AG filing acknowledgment** | Statement that the assessment will be filed with the CO AG on request | Auto-generated |

The MCP fills in 9 of 16 sections automatically from existing system metadata; the other 7 require manual input from the customer's compliance team. The output is a single PDF + structured JSON, signed with HMAC-SHA256, and ready for AG submission.

## 5. The consumer-rights workflow (C.R.S. §6-1-1704)

The MCP's `register_consumer_rights_workflow` tool (Tool #3) operationalizes the 4 consumer rights under Colorado law:

| Right | What it requires | MCP implementation |
|---|---|---|
| **Notification** | Deployer must notify consumers they're interacting with AI before the consequential decision | Generates a consumer-facing disclosure snippet + embeddable JS widget |
| **Opt-out** | Consumer can opt out of the ADMT and request human review | Generates an opt-out endpoint + human-review escalation path |
| **Correction** | Consumer can correct inaccurate data used by the ADMT | Generates a data-correction endpoint that re-runs the ADMT |
| **Appeal** | Consumer can appeal the ADMT decision, with human reviewer | Generates an appeal endpoint with SLA tracking (15-day response) |

The MCP does NOT host the consumer-facing endpoints (those are the customer's website). It **generates the workflow definition** (URLs, snippets, escalation paths) and **monitors the audit log** of consumer interactions via the keystone's HMAC-SHA256 attestation chain.

## 6. The 4 customer archetypes (US ADMT deployers + developers)

| # | Archetype | Example companies | Primary tool used | x402 spend/month (est.) |
|---:|---|---|---|---|
| 1 | **US enterprises with CO consumers** (banks, insurers, employers, schools, hospitals) | Wells Fargo, Allstate, Geico, Kaiser Permanente, Kaiser, Ascension, large US employers | `classify_admt` + `generate_impact_assessment` + `register_consumer_rights_workflow` (full cycle) | $10K-$50K |
| 2 | **AI vendors serving US enterprises** (HR tech, edtech, lending tech) | Workday, ServiceNow, Eightfold, HireVue, Upstart, Zest AI, Olive AI | `classify_admt` (per product, at scale) + `generate_impact_assessment` (per deployment) | $5K-$30K |
| 3 | **US state + local government agencies** (public benefits, law enforcement, healthcare) | State unemployment agencies, state housing authorities, city police departments, state Medicaid | `generate_impact_assessment` + `register_consumer_rights_workflow` (public-sector procurement cycles) | $20K-$200K |
| 4 | **AI compliance consultants serving US ADMT clients** (the channel) | Big 4, US boutique AI consultancies | All 6 tools at volume; assessment generation for client deliverables | $10K-$100K |

**Total addressable:** ~5,000 US enterprises with CO consumer footprint × 1% capture = 50 customers × $10K average monthly spend = $500K MRR Y1. The $500K figure assumes enterprise tier (5 customers × $100K/yr); the lower-bound is 50 customers × $25K/yr = $1.25M ARR. **The revenue inflection is when Colorado issues its first AG enforcement action** (expected H2 2027), at which point demand spikes 5-10x.

## 7. The 3 deployment modes (per the China + EU AI Act + ETSI specs, the same pattern)

| # | Mode | Architecture | CCPA/CPRA data-residency impact | Latency |
|---:|---|---|---|---|
| 1 | **Remote SaaS (US region)** | MEOK-hosted MCP server in us-east-1 / us-west-2; customer calls via x402 | None (no personal data processed, only system metadata + classifier result) | 50-200ms |
| 2 | **On-prem (customer US VPC)** | Docker image in customer's AWS/GCP/Azure US region; no egress | None (data stays in customer VPC) | 5-20ms |
| 3 | **Hybrid (control plane EU + scanner US)** | MEOK control plane in eu-west-1; ledger storage in customer's US VPC | Data minimization: only aggregated metrics cross the border | 20-50ms |

For initial launch, **Mode 1 (Remote SaaS in US region)** is the only viable option — Modes 2/3 require customer's infra team involvement. The remote mode can serve the freemium funnel immediately and is CCPA/CPRA-compliant because no personal data is processed.

## 8. The CRITICAL Fix compliance (per `CRITICAL_FIXES_2026-06-08.md`)

- **Fix #1 (Drop root in Docker)**: Dockerfile uses `USER app` with `uid 10001` (per keystone pattern). The MCP server image is built with the same template.
- **Fix #2 (API key permission lockdown)**: customer's impact-assessment data and AG-report drafts are stored in customer's own S3/GCS bucket; MEOK's API keys are read via `meok_secrets.get_api_key()` (stdlib keyring + chmod 600 fallback).
- **Fix #3 (`MEOK_ATTESTATION_KEY` secret manager)**: the impact assessments (Tool #2) and the AG reports (Tool #5) are HMAC-SHA256 signed via `meok_x402.py:_resolve_attestation_key()`. The compliance ledger (Tool #6) is the keystone's flagship attestation-chain product, and the AG-filing use case is the highest-stakes deployment.

## 9. Integration with the keystone's 35,000+ MCP server ecosystem

- **Cross-link to `csoai.org`**: 14-framework governance (was 13, now 14 with Colorado ADMT; will become 15-19 with the other 15+ state ADMT laws expected 2027-2028)
- **Cross-link to `meok.ai`**: Business tier ($49/user/mo) for the full ADMT workspace
- **Cross-link to `councilof.ai`**: BFT attestation that the impact assessment was performed by a qualified reviewer (BFT prevents the customer from rubber-stamping assessments to "look compliant")
- **Cross-link to `proofof.ai`**: HMAC-signed proof that an impact assessment was generated + filed with the AG on request
- **Cross-link to `transparencyof.ai`**: public dashboard showing the customer's ADMT classification + last-assessment date + consumer-rights workflow status (per Flywheel 5)
- **Cross-link to `eu-ai-act-high-risk-classifier-mcp`**: Tool #1 (`classify_admt`) reuses the Annex III classification engine from the EU AI Act MCP, re-taxonomy'd for Colorado's 8 sectors. The two MCPs share the same back-end ML classifier.
- **Cross-link to `eu-ai-act-compliance-mcp` flagship**: reads the 410 verbatim EU AI Act articles for the legal-text cross-references (the EU AI Act and Colorado ADMT share many concepts)

## 10. Engineering build schedule (T-207 = 1 January 2027)

| Week | Phase | Output | Owner |
|---|---|---|---|
| **W1-W2 (Jul 6 - Jul 19)** | Spec finalization + corpus sourcing | This spec (done 8 Jun) + Colorado ADMT statute text + 50+ public ADMT impact assessments from early-adopter cohort | Eng lead |
| **W3-W4 (Jul 20 - Aug 2)** | Tool scaffolding + keystone integration | 6 MCP tools wired into the gateway + integration with `eu-ai-act-high-risk-classifier-mcp` for the shared classifier | Eng lead |
| **W5-W6 (Aug 3 - Aug 16)** | Pilot customer validation | 2-3 US ADMT deployers (1 bank, 1 insurer, 1 employer) using it in beta | Sales/CS |
| **W7-W8 (Aug 17 - Aug 30)** | Pre-Q3 marketing + waitlist | `colorado-admt-compliance-mcp` on GHCR, PyPI, Smithery, x402; ADMT waitlist launch; 28-hive cross-link to ADMT Authority query | Eng + Nick |
| **W9-W20 (Aug 31 - Nov 15)** | Pre-Jan-1 hardening | 1.0.0 release, OpenSSF Scorecard pass, AWS Marketplace listing, 50+ customer onboarding | Eng + Nick |
| **W21-W26 (Nov 16 - Dec 31)** | Final pre-deadline push | "January 1 → ADMT-ready" marketing; 1,000 free classifications/week; impact-assessment push to existing Business-tier customers | Sales/Marketing |
| **W27 (Jan 1, 2027)** | **GO LIVE** | Service available in production for 1 Jan enforcement; first 50 customers onboarded | All |

**Tight but achievable.** The keystone's existing 13-framework engine provides the substrate; the Colorado work is sector-taxonomy + impact-assessment-template + consumer-rights-workflow logic, not new infrastructure. The 7-month runway (vs 5-6 weeks for the other 3 P0 builds) is the buffer for state-by-state expansion in 2027-2028.

## 11. What this is NOT

- **Not** a substitute for qualified legal counsel. Colorado ADMT is a new statute with limited case law; the MCP's `confidence` field is a signal, not a verdict. Edge cases (e.g., is a recommendation system in a job portal "substantially influencing" a hiring decision if a human makes the final call?) require qualified legal counsel.
- **Not** an AG-relationship tool. The MCP generates AG-filing-ready documents (Tool #5), but the actual filing is the customer's responsibility. MEOK's role is to make the filing 1-hour instead of 1-week, not to file on the customer's behalf.
- **Not** a guarantee of non-discrimination. The MCP's `AdverseImpactAudit` computes demographic parity, equalized odds, and disparate impact ratios, but the legal determination of whether a system "discriminates" under Colorado law remains with the regulator and the courts.
- **Not** a CCPA/CPRA substitute. Colorado ADMT is an AI-specific law; the underlying personal-data processing is still governed by CCPA/CPRA (California), CPA (Colorado), and the other state privacy laws. The MCP does NOT replicate privacy-rights request handling; it complements existing privacy tooling.

## 12. Cross-references

- `REGULATORY_CALENDAR_2026-2027.md` — the 4 P0 deadlines (this is #4, the Jan 1 2027 deadline)
- `MASTER_AUDIT_INGESTION.md` — the 4 P0 builds identified
- `EU_AI_ACT_HIGH_RISK_CLASSIFIER_MCP_SPEC.md` — sister spec (the Aug 2 deadline, the shared classifier)
- `CHINA_AI_ANTHROPOMORPHIC_MCP_SPEC.md` — sister spec (the Jul 15 deadline)
- `ETSI_CABCA_CONTINUOUS_CONFORMITY_MCP_SPEC.md` — sister spec (the Q3 2026 deadline)
- `SHADOW_AI_DETECTION_MCP_SPEC.md` — sister spec (template)
- `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` — sister spec (the cert track)
- `PRICING.md` — the 4 SaaS tiers + 28 x402 call prices
- `CRITICAL_FIXES_2026-06-08.md` — the 3 security fixes (Docker root, API key perms, attestation key)
- `KEY_DIFFERENTIATORS.md` — differentiator #3 (HMAC-SHA256 attestation chain, the substrate for the compliance ledger)
- `/tmp/kimi_extract/nicholas_templeman_26domain_portfolio.agent.final.md` § "US State AI Laws" — Colorado SB 24-205 + the 15+ state cascade
- `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec09.md` — US AI safety governance, NIST AI RMF, EEOC algorithmic accountability
- `/tmp/kimi_extract/sov3_mcp_master_audit.md` — 76-server audit, 13-framework engine, the 4 P0 builds
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — Phase 3 (Jun 28 - Jul 3) covers Colorado ADMT pre-announce

---

*Generated 2026-06-08 by Claude (Opus 4.8 session on `claude/review-changes-mkbcvckpl5ix3r03-MkKCu`). Sources: `sov3_mcp_master_audit.md` + Kimi research corpus + the keystone's existing MCP spec templates. Colorado SB 24-205 (2024) and C.R.S. §6-1-1701 et seq. are referenced as published in the Colorado Revised Statutes; the impact-assessment requirements should be verified against the Colorado Department of Law's final implementing regulations when published — this is a specification document anticipating the statute, not a definitive legal reading.*
