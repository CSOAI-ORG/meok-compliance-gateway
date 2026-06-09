# China AI Anthropomorphic MCP — Spec

> **Authored**: 2026-06-08
> **Purpose**: spec for `china-ai-anthropomorphic-mcp` — the compliance layer for **China's Interim Measures for the Management of Generative AI Services** (effective **15 July 2026**, T-37 from today). This is one of 4 P0 MCPs in the regulatory roadmap; the others are `eu-ai-act-high-risk-classifier-mcp` (T-55), `etsi-cabca-continuous-conformity-mcp` (T-90+), and `colorado-admt-compliance-mcp` (T-207).
> **Source**: `REGULATORY_CALENDAR_2026-2027.md` (the calendar) + `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec09.md` (threats, regulatory complexity) + `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec17.md` (China's 15th Five-Year Plan on "full AI lifecycle risk management") + `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec16.md` (Singapore/China algorithmic recommendation regulations) + the 76-server MCP master audit (this MCP is one of the 4 P0-builds).
> **Rubric**: factual comparative, no war language per `RUBRIC_EXTERNAL_COMMS.md`. Banned vocabulary in § 11.

## 1. The opportunity

- **The deadline**: **15 July 2026** — T-37 from today (2026-06-08) and T-19 from the planned July 4 launch. **The keystone's 28-hive GEO content already advertises "EU AI Act August 2" deadlines; we need a parallel "China Generative AI July 15" wedge to capture both calendar waves.**
- **The market gap**: per `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec16.md`, China's algorithmic recommendation regulations and deep-synthesis provisions already impose governance requirements. Per the 76-server MCP master audit, **none of the 15 named GRC competitors (OneTrust, Credo AI, Holistic AI, Vanta, Drata, Secureframe, Tugboat Logic, Laika, Compyl, AuditBoard, Diligent, Galvanize, Pathlock, Netwrix, Sumo Logic, AppOmni) has a China-specific MCP**. **This is the SOV3-Only capability with the shortest replication time** — about 3 months if a competitor started today, but they aren't.
- **The Chinese regulatory stack** (per `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec17.md`):
  - **Interim Measures for the Management of Generative AI Services** (effective 15 Aug 2023; **synthetic-content labeling enforcement tightens 15 July 2026** per the calendar)
  - **Provisions on the Administration of Deep Synthesis of Internet Information Services** (effective 10 Jan 2023)
  - **Provisions on Algorithm Recommendation Management** (effective 1 March 2022)
  - **Measures for the Security Assessment of Internet Information Services with Public Opinion or Social Mobilization Attributes** (effective 15 March 2018, but the 2026 revision extends to GenAI)
  - China's 15th Five-Year Plan (2026-2030) explicitly incorporates "full AI lifecycle risk management" alongside AGI development pathways
- **The keystone's existing 13-framework engine** (Key Differentiator #1) covers EU AI Act + GDPR + HIPAA + DORA + NIS2 + CRA + CSRD + ESG + ISO 42001 + ISO 27001 + SOC 2 + NIST AI RMF + supply-chain. **None of the 13 cover China Generative AI Services specifically.** This MCP closes that gap.
- **The ICP licensing barrier** (per `/Users/nicholas/meok-compliance-gateway/docs/seo-global-report/seo_global_report_sec07.md`): a commercial ICP license for Chinese-hosted sites takes 60-90 working days. Foreign companies must establish a Chinese entity (WFOE/JV) or partner with a licensed local company. The MCP-server model side-steps this: a remote MCP server hosted in HK/Singapore can serve Chinese-domiciled customers without the ICP bottleneck, as long as it doesn't host Chinese-domestic user data. (The MCP is compliance-advice-as-a-service, not user-data-hosting.)
- **Revenue angle**: per `PRICING.md`, the x402 micro-call layer can bill per attestation lookup, per classification call, per watermark verification. Estimated: 200 Chinese-domiciled customers × 50K calls/year × $0.05 = $500K Y1 (Stream 5 wedge for APAC).

## 2. The 5 obligations under the Interim Measures

| # | Obligation | What it requires | What MEOK's MCP does |
|---:|---|---|---|
| 1 | **Synthetic content labeling** (Art. 4, 7, 12) | All AI-generated text, image, audio, video, virtual-scene output must be **explicitly labeled as such** to the end user | `label_synthetic_content` MCP tool — produces a C2PA-style signed manifest embedded in the output metadata |
| 2 | **Service provider filing** (Art. 17) | Generative AI services offered to the Chinese public must be **filed with the Cyberspace Administration of China (CAC)** and the local cyberspace department | `filing_checklist` MCP tool — generates the 12-section filing document from the customer's AI system inventory |
| 3 | **Training data lawfulness** (Art. 7) | Training data must be sourced lawfully, must not infringe IP, must comply with China's Personal Information Protection Law (PIPL) | `audit_training_data` MCP tool — cross-references training corpora against PIPL + the Interim Measures' IP blacklist (the 12 categories of prohibited content) |
| 4 | **Content moderation** (Art. 4, 14) | Generated content must not produce 12 categories of prohibited content (per Article 4) | `moderate_output` MCP tool — applies the 12-category classifier to LLM outputs; integrates with both US-hosted (OpenAI, Anthropic) and China-hosted (ERNIE, Qwen, DeepSeek) models |
| 5 | **User complaint handling + log retention** (Art. 15) | Service providers must handle user complaints within a defined SLA, retain content logs for at least 6 months | `user_complaint_log` + `audit_log_retention` MCP tools — integrate with the keystone's HMAC-SHA256 attestation chain for tamper-evidence |

## 3. The 6 MCP tools (per the spec template from `SHADOW_AI_DETECTION_MCP_SPEC.md`)

| # | Tool | Input | Output | Interim Measures article | Pricing |
|---:|---|---|---|---|---|
| 1 | `label_synthetic_content` | `content: bytes` + `media_type: str` + `model_id: str` | `LabeledContent` (signed manifest + sidecar) | Art. 4, 7, 12 (synthetic labeling) | $0.001 per item labeled |
| 2 | `filing_checklist` | `service_description: ServiceDescription` (name, model, deployment, data flow) | `FilingDocument` (12 sections, ready for CAC submission) | Art. 17 (service filing) | $50 per filing (one-time) |
| 3 | `audit_training_data` | `corpus_manifest: CorpusManifest` (source list, license, content types) | `ComplianceReport` (12-category classifier result, PIPL cross-ref, IP risk flags) | Art. 7 (training data) | $0.10 per 1K corpus items |
| 4 | `moderate_output` | `output: str` + `model_id: str` + `jurisdiction: str` | `ModerationResult` (allowed / flagged / blocked + reason codes) | Art. 4, 14 (content moderation) | $0.01 per call (free, drives the wider funnel) |
| 5 | `user_complaint_log` | `complaint: Complaint` (user_id, content_ref, complaint_type) | `ComplaintRecord` (HMAC-signed, 6-month retention check) | Art. 15 (complaint handling) | $0.05 per complaint logged |
| 6 | `audit_log_retention` | `service_id: str` + `window_days: int` | `RetentionReport` (which logs are due, which need extension) | Art. 15 (log retention) | $0.10 per 1K log entries scanned |

All tools are `@paywalled` per the keystone's x402 pattern. Free tier = 100 calls/month (drives the freemium funnel for Chinese AI operators). Team tier = 10K calls/month. Business tier = unlimited.

## 4. The 5 customer archetypes (Chinese GenAI service providers)

| # | Archetype | Example companies | Primary tool used | x402 spend/month (est.) |
|---:|---|---|---|---|
| 1 | **Baidu/ERNIE ecosystem** | Baidu (ERNIE Bot, Ernie 4.5), iFlytek (Spark), Zhipu (GLM), Moonshot (Kimi) | `label_synthetic_content` + `audit_log_retention` | $5K-$20K |
| 2 | **Vertical GenAI providers** | 01.AI (Yi), DeepSeek (R1/V3), Stepfun, MiniMax, ModelBest, SandAI | `moderate_output` + `label_synthetic_content` | $2K-$10K |
| 3 | **Cross-border SaaS** | Microsoft (Copilot in China), Google (Gemini via partnership), OpenAI (API only) | `filing_checklist` + `audit_training_data` | $10K-$50K (enterprise) |
| 4 | **Content platforms** | WeChat (Tencent), Weibo, Douyin (TikTok China), Xiaohongshu | `moderate_output` at scale + `user_complaint_log` | $20K-$100K |
| 5 | **Open-source operators** | Alibaba (Qwen), DeepSeek, 01.AI (open-weight models) | `audit_training_data` + `filing_checklist` | $1K-$5K |

**Total addressable:** 500+ Chinese GenAI service providers × $5K average monthly spend = $2.5M MRR. (Sourced from the 76-server MCP master audit's China vertical sizing, footnote-anchored to CAC's public GenAI service registry.)

## 5. The 12 prohibited content categories (Article 4)

The Interim Measures Article 4 prohibits services from generating content that:

1. **Subverts state power** — opposes the PRC's fundamental political system, endangers national security
2. **Undermines national unity** — promotes separatism, undermines territorial integrity
3. **Incitement to subversion, separatism, or terrorism**
4. **Ethnic hatred or discrimination** — content that denigrates ethnic groups
5. **Violence, obscenity, pornography, or false information** — content that is obscene, violent, or spreads rumors
6. **Disrupts economic or social order** — pyramid schemes, illegal fundraising, market manipulation
7. **Encourages or depicts substance abuse, gambling, or crime**
8. **Excessively glorifies inappropriate values** — content that the CAC judges to be morally harmful
9. **Infringes on others' IP, privacy, or other rights**
10. **Spreading rumors or false information** that disrupts financial markets or public order
11. **Content that the CAC judges endangers cybersecurity**
12. **Content that violates other Chinese laws and regulations** (catch-all)

The MCP's `moderate_output` tool (Tool #4) implements all 12 categories as a deterministic classifier, integrated with the keystone's existing EU AI Act risk classification engine. **The two regulatory regimes share the same input (LLM output) but different category taxonomies — the MCP normalizes both.**

## 6. The 3 deployment modes

| # | Mode | Architecture | ICP required? | Latency |
|---:|---|---|---|---|
| 1 | **Remote SaaS (HK/SG)** | MEOK-hosted MCP server in HK or Singapore; customer calls via x402 | No (advice-only, not user-data-hosting) | 50-200ms |
| 2 | **On-prem (China-domiciled)** | Docker image in customer's Chinese VPC; no egress | Yes (customer's ICP covers it) | 5-20ms |
| 3 | **Hybrid (control plane in HK + scanner in China)** | MEOK control plane outside Great Firewall; scanner inside | Yes (scanner side) | 20-50ms |

For initial launch, **Mode 1 (Remote SaaS)** is the only viable option — Modes 2/3 require ICP + Chinese entity, which is a Q3-Q4 2026 capability. The remote mode can serve the freemium funnel immediately.

## 7. The CRITICAL Fix compliance (per `CRITICAL_FIXES_2026-06-08.md`)

- **Fix #1 (Drop root in Docker)**: Dockerfile uses `USER app` with `uid 10001` (per keystone pattern). For Mode 1 (Remote SaaS), the MCP server image is built with the same template.
- **Fix #2 (API key permission lockdown)**: customer's PIPL-relevant API keys are read via `meok_secrets.get_api_key()` (stdlib keyring + chmod 600 fallback).
- **Fix #3 (`MEOK_ATTESTATION_KEY` secret manager)**: the synthetic-content labels (Tool #1) and the audit log retention (Tool #6) are HMAC-SHA256 signed via `meok_x402.py:_resolve_attestation_key()`. The CAC filing checklist (Tool #2) includes a `signed_at` field referencing the attestation key.

## 8. Integration with the keystone's 35,000+ MCP server ecosystem

- **Cross-link to `csoai.org`**: 14-framework governance (was 13, now 14 with China Generative AI Services)
- **Cross-link to `meok.ai`**: Business tier ($49/user/mo) for full filing + moderation
- **Cross-link to `councilof.ai`**: BFT attestation for the moderation decisions
- **Cross-link to `proofof.ai`**: HMAC-signed proof that a synthetic-content label was issued
- **Cross-link to `transparencyof.ai`**: public dashboard showing the customer's compliance status (per Flywheel 5)

## 9. Engineering build schedule (T-37 = 15 July 2026)

| Week | Phase | Output | Owner |
|---|---|---|---|
| **W1 (Jun 8-14)** | Spec finalization + corpus sourcing | This spec (done 8 Jun) + 12-category classifier training data sourced from CAC public rulings | Eng lead |
| **W2 (Jun 15-21)** | Tool scaffolding + keystone integration | 6 MCP tools wired into the gateway + 14th framework entry | Eng lead |
| **W3 (Jun 22-28)** | Pilot customer validation | 2-3 Chinese GenAI providers using it in beta (Baidu ecosystem or 01.AI/DeepSeek) | Sales/CS |
| **W4 (Jun 29 - Jul 5)** | Public launch at Jul 4 | china-ai-anthropomorphic-mcp on GHCR, PyPI, Smithery, x402 | Eng + Nick |
| **W5 (Jul 6-12)** | Final hardening + 1.0.0 release | Stable release, OpenSSF Scorecard pass, AWS Marketplace listing | Eng + Nick |
| **W6 (Jul 13-15)** | **GO LIVE** | Service available in production for 15 Jul enforcement | All |

**Tight but achievable.** The keystone's existing 13-framework engine provides the substrate; the China work is content + classification logic, not new infrastructure.

## 10. What this is NOT

- **Not** a comprehensive Chinese legal-compliance product. The MCP is a **server-side classification + labeling + filing-assistance tool**, not a substitute for Chinese legal counsel. For sensitive cases, customers should engage qualified Chinese counsel.
- **Not** a host of Chinese-domiciled user data. Mode 1 (Remote SaaS) processes only the customer's AI system description and (in `moderate_output` tool) the LLM output text — both of which the customer can choose to truncate, hash, or pre-redact.
- **Not** a replacement for the customer's own CAC filing. The `filing_checklist` tool generates the 12-section document, but the customer is the filer. MEOK's role is to reduce the 60-90 day ICP/filing burden to 5-10 days, not to file on the customer's behalf.

## 11. Cross-references

- `REGULATORY_CALENDAR_2026-2027.md` — the 4 P0 deadlines (this is #2 of 4)
- `MASTER_AUDIT_INGESTION.md` — the 4 P0 builds identified
- `EU_AI_ACT_FREE_SCANNER_SPEC.md` — sister spec (the EU AI Act freemium gate, T-55)
- `SHADOW_AI_DETECTION_MCP_SPEC.md` — sister spec (template for this one)
- `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` — sister spec (the certification track)
- `PRICING.md` — the 4 SaaS tiers + 28 x402 call prices
- `CRITICAL_FIXES_2026-06-08.md` — the 3 security fixes (Docker root, API key perms, attestation key)
- `KEY_DIFFERENTIATORS.md` — differentiator #1 (13 frameworks → will become 14 with this)
- `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec09.md` — threats, regulatory complexity
- `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec17.md` — China's 15th Five-Year Plan, AGI governance
- `/tmp/kimi_extract/nicholas_templeman_ai_portfolio_sec16.md` — Asia-Pacific regulatory sizing
- `/Users/nicholas/meok-compliance-gateway/docs/seo-global-report/seo_global_report_sec07.md` — China ICP licensing details
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — Phase 1 (Jun 15-20) covers the China content angle

---

*Generated 2026-06-08 by Claude (Opus 4.8 session on `claude/review-changes-mkbcvckpl5ix3r03-MkKCu`). Sources: `sov3_mcp_master_audit.md` + Kimi research corpus + the keystone's existing MCP spec templates. All Chinese regulatory references should be verified by qualified Chinese counsel before the Jul 4 public launch — this is a specification document, not legal advice.*
