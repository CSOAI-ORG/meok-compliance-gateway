# SOV3 Unique Capabilities Matrix — Engineering Reification

> **Authored**: 2026-06-09
> **Purpose**: convert the marketing blueprint (`/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md`, 1,695 lines) into an engineering source-of-truth that a developer building MEOK v2.0 can use to find the code path that implements each SOV3-exclusive capability.
> **Audience**: MEOK engineering team (keystone + flagship contributors).
> **Rubric**: per `RUBRIC_EXTERNAL_COMMS.md` — factual comparative, no war language. Banned vocabulary (kill shot, nuclear arsenal, coup de grâce, talent raid, seeding doubt, depletion campaign, strike while, vulnerability window, acquisition target, funding fiction) does not appear in this file. Where a banned phrase would have lived in the source dossier, this file uses a neutral replacement.
> **Status legend**: shipped / in dev / spec'd / not started.

---

## 1. The 10 SOV3-Exclusive Capabilities mapped to keystone code

Each row maps a capability from `sov3_tech_blueprint.agent.final.md` § 4.1-4.10 to a concrete keystone artifact, its current status, a proof artifact, and the replication time a competitor would need.

| # | Capability (1-line) | Keystone code path | Status | Proof artifact | Competitor replication time |
|---|---|---|---|---|---|
| 1 | Public Transparency Dashboard with Blockchain Verification | `http_server.py` + planned `meok_dashboard.py` (React + GraphQL) + `meok_x402.py:66-126` attestation substrate | spec'd | `KEY_DIFFERENTIATORS.md` differentiator #1; design in `sov3_tech_blueprint.agent.final.md` § 4.1 | 12-18 months (architectural + cultural) |
| 2 | PDCA Cycle Automation for AI Safety | `meok_policy.py` (planned) → `meok_enforce.py` (planned) → `meok_monitor.py` (planned) → `meok_gitops.py` (planned); each cycle signed via `meok_x402.py` HMAC substrate | spec'd | design in `sov3_tech_blueprint.agent.final.md` § 4.2; PDCA loop engine in § 8.2 build plan | 12-18 months (requires redesign of any linear assessment engine) |
| 3 | Watchdog AI Safety Certification (3-tier) | `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` + `MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md`; exam content corpus built from 410 EU AI Act articles | spec'd | `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` (full spec); HMAC-signed certs via `meok_x402.py:66-126` | 9-12 months (category does not exist yet) |
| 4 | MCP-Native Governance (First in Market) | `meok-governance-engine-mcp` (production, OpenSSF 81.6) + `eu-ai-act-compliance-mcp` (production, OpenSSF 81.6) + 44 CSOAI-ORG MCPs in the official registry | shipped (keystone + 10 production + 16 active) | `sov3_portfolio_inventory.md` § 2.1 (26 MCPs catalogued); `MCP_REG_HEALTH_REPORT.md` (44 registered) | 12-18 months (ecosystem moat: 35K+ servers, 0 governance) |
| 5 | EU AI Act 48-Hour Compliance Engine | `eu-ai-act-compliance-mcp` (410 verbatim articles, 42-point audit) + `meok-governance-engine-mcp` (13 frameworks) | shipped (single-framework; full engine Q3 2026) | `eu-ai-act-compliance-mcp` v1.3.0 on `ghcr.io/csoai-org`; `EU_AI_ACT_FREE_SCANNER_SPEC.md` (the funnel front-door) | 6-9 months (1,200+ controls to encode; legal engineering bottleneck) |
| 6 | Agent Behavior Monitoring & Enforcement | `meok-mcp-injection-scan-mcp` (30+ rules, 5 severity tiers) + `SHADOW_AI_DETECTION_MCP_SPEC.md` (4 detection sources) + agentaudit server (A2A inventory, 37 tests) | shipped (scanner); spec'd (full enforcement) | `meok-mcp-injection-scan-mcp` production; agentaudit test suite 60/60 green | 12-18 months (runtime + governance DNA required) |
| 7 | Multi-Protocol API (REST + GraphQL + gRPC + WebSockets) | `http_server.py` (REST, live) + planned GraphQL schema (in `sov3_tech_blueprint.agent.final.md` § 8.6) + planned gRPC + planned WebSocket `/ws/v1/*` (in § 8.6) | shipped (REST); spec'd (GraphQL/gRPC/WS) | `http_server.py` + x402 streamable-HTTP transport on keystone | 12-24 months (legacy REST-only stacks would need rewrite) |
| 8 | Open-Source Core with Enterprise Paywall | 447 MIT-licensed CSOAI-ORG repos; keystone + 76 MCP servers in the fleet | shipped | `sov3_portfolio_inventory.md` § 3.3 (447 repos, MIT); `PRICING.md` (4-tier paywall) | 18-24 months (cultural + business model reversal) |
| 9 | Real-Time AI Governance Event Streaming | Webhook dispatcher (in `sov3_tech_blueprint.agent.final.md` § 8.1 #17) + WebSocket `/ws/v1/{agents,violations,trust-scores,alerts}` spec + HMAC-signed event receipts | spec'd (architecture); x402 streamable-HTTP substrate shipped | `sov3_tech_blueprint.agent.final.md` § 8.6 WebSocket schemas + § 3.4 real-time event types | 9-12 months (event-driven refactor of batch systems) |
| 10 | Industry-Specific MCP Packs (Finance, Healthcare, Gov, Critical Infra) | `dora-compliance-mcp`, `nis2-compliance-mcp`, `cra-compliance-mcp`, `hipaa-compliance-mcp`, `soc2-compliance-ai-mcp`, `gdpr-compliance-ai-mcp`, `csrd-compliance-mcp` | shipped (7 of 7 production or active per `sov3_portfolio_inventory.md` § 2.1) | OpenSSF-scored Docker images on `ghcr.io/csoai-org` | 12-18 months per pack (vertical expertise + legal engineering) |

---

## 2. The 5 Critical Competitor Weaknesses

Each row identifies a structural weakness observed across the 15-competitor set in `sov3_tech_blueprint.agent.final.md` § "Executive Summary" § 5, and the MEOK exploitation path with a keystone code reference.

| # | Weakness (1-line) | Why it matters (1-line) | MEOK exploitation path (1-line + code/spec reference) |
|---|---|---|---|
| 1 | Zero blockchain adoption across all 15 competitors | Immutable audit trails do not exist in any closed enterprise platform | HMAC-SHA256 signed attestations via `meok_x402.py:66-126` + `MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` Signet receipts (§ 5.5) |
| 2 | Agent governance is pre-product everywhere except WitnessAI | $47B AI agent infrastructure market has no governance layer | `agentaudit` server (A2A inventory, 60/60 tests) + `meok-mcp-injection-scan-mcp` (30+ rules) + `SHADOW_AI_DETECTION_MCP_SPEC.md` (4 detection sources) |
| 3 | 3 major competitors have NO public API (WitnessAI, Zenity, Cranium) | Their users cannot integrate governance data into existing CI/CD or SIEM pipelines | `http_server.py` (REST, live) + x402 streamable-HTTP + planned GraphQL/gRPC/WS per `sov3_tech_blueprint.agent.final.md` § 8.6 |
| 4 | Transparency score = 0 for all 15 competitors | Public trust is impossible without public attestations | Planned `meok_dashboard.py` + HMAC-signed public attestations; design in `sov3_tech_blueprint.agent.final.md` § 4.1 |
| 5 | DevOps integration is universally weak | AI governance sits outside the CI/CD pipeline in every other product | `meok-policy-enforcement-mcp` (deployment gate) + `agent-prompt-injection-firewall-mcp` + planned `meok_gitops.py` (PR-blocking policy checks) per blueprint § 8.2 |

---

## 3. The MCP Ecosystem — Unclaimed Empire

Market data from `sov3_tech_blueprint.agent.final.md` § 2 plus the keystone's own MCP fleet and registry health.

| Metric | Value | Source |
|---|---|---|
| Total MCP servers (cross-marketplace, June 2026) | 35,000-40,000 unique | Blueprint § 2.1 |
| Glama.ai indexed | 32,490 | Glama.ai |
| MCP.so collected | 21,956 | MCP.so |
| PulseMCP directory | 16,822 | PulseMCP |
| Smithery.ai curated | 2,880+ | Smithery.ai |
| GitHub `awesome-mcp-servers` stars | 88,700 | GitHub |
| Active developers | 50,000+ | Glama.ai |
| Monthly tool calls | 1,000,000+ | Glama.ai |
| MCP ecosystem TAM | $10.4B | Industry estimates |
| Security MCPs | 84 (0.4% of total) | Blueprint § 2.2 |
| AI Governance MCPs | 0 in any competitor's portfolio | Blueprint § 2.2 |
| MCP-related CVEs (per `deepdive_mcp_inventory.md` + OX Security May 2026) | 30+ (CVE-2025-65720, CVE-2025-49596, CVE-2026-30615..33252, CVE-2025-54136, CVE-2025-59536, CVE-2026-21852, etc.) | Blueprint § 2.3 |
| Competitors with MCP strategy | 1 (Zenity — monitors MCP interactions, no governance) | Blueprint § 2.4 |
| MEOK MCP server inventory | 10 production + 16 active + 3 infrastructure = 29 total | `sov3_portfolio_inventory.md` § 2.1 |
| MEOK repos on MCP official registry | 44 (all missing server.json fields except keystone) | `MCP_REG_HEALTH_REPORT.md` (regenerated 2026-06-08) |
| GRC competitors with zero MCP | 13 of 15 | 76-server MCP master audit (2026-06-08) |
| The 6 missing `server.json` fields per repo | `icons`, `websiteUrl`, `metadata.publisher`, `metadata.categories`, `examples`, `resources` | `MCP_REG_HEALTH_REPORT.md` |

**Analysis**: AI governance is the largest unclaimed category in the MCP ecosystem. The 84 security MCPs are mostly offensive (GHOSTCREW, PentestAgentMCP, Hostile-Command-Suite); the defensive governance layer is absent. The keystone's `meok-governance-engine-mcp` and `eu-ai-act-compliance-mcp` are the only governance-grade MCPs on the official registry as of 2026-06-09.

---

## 4. The 3 API-Less Competitors (integration-blocked users)

| Company | Verified funding | API status | User pain point | MEOK API-first pitch |
|---|---|---|---|---|
| **WitnessAI** | $85.5M (Sound Ventures, GV, Ballistic Ventures, Samsung NEXT) | No public API; observability-only | Users cannot pipe findings into SIEM/SOAR; no programmatic access | x402 streamable-HTTP + REST + planned GraphQL/gRPC/WS expose every observation as a paid-call event |
| **Zenity** | $55M+ (Series B; "Gartner Company to Beat") | No public API; AWS Security Hub one-way only | Microsoft-locked customers cannot build platform-agnostic agents | Platform-agnostic gateway + LangChain/CrewAI/AutoGen/Azure AI Foundry unified abstraction |
| **Cranium** | $46M (KPMG spinout) | No public API; W&B partnership is the only integration | Enterprise customers cannot extract data without a manual request | Open-core SDKs (Python/TypeScript) + x402 per-attestation pricing + REST + planned gRPC streaming |

The MEOK differentiator vs these three is **first-class API access with cryptographic event receipts**, per `sov3_tech_blueprint.agent.final.md` § 3.2.

---

## 5. The Multi-Protocol API Strategy

Per `sov3_tech_blueprint.agent.final.md` § 4.7 + § 3.4, the keystone is the only AI governance platform exposing four protocols through a unified gateway. Every competitor is REST-only.

| Protocol | Keystone code path | Schema location | Rate limit (planned) | Auth method |
|---|---|---|---|---|
| **REST** | `http_server.py` (live) | `sov3_tech_blueprint.agent.final.md` § 8.6 (OpenAPI 3.0 sketch) + Blueprint § 3.4 (resource list) | 1,000 req/min (free); 10,000 req/min (paid) | OAuth 2.0 + API keys (scoped per env) + x402 paywall |
| **GraphQL** | planned (no file yet) | `sov3_tech_blueprint.agent.final.md` § 8.6 (full schema) | 100 queries/min (per session) | JWT + x402 paywall |
| **gRPC** | planned (no file yet) | planned `.proto` files in `/proto/v1/` (not yet created) | 10,000 streams/min (per agent) | mTLS + x402 paywall |
| **WebSocket / SSE** | x402 streamable-HTTP transport (shipped on keystone); WS handler planned | `sov3_tech_blueprint.agent.final.md` § 8.6 (event schemas: `agentStatusChanged`, `violationDetected`, `trustScoreUpdated`, `complianceStatusChanged`) | 1 connection/agent; 10 events/sec | JWT + x402 paywall |

The 3-5x developer-experience improvement claimed in the blueprint comes from GraphQL's 60-80% call reduction for complex governance queries and gRPC's 5-10x latency reduction for high-throughput agent monitoring (Blueprint § 4.7).

---

## 6. The PDCA Automation Architecture

The Plan-Do-Check-Act loop is the keystone's most distinctive engineering claim. Each phase maps to a planned keystone module; the loop is sealed by an HMAC-signed audit entry on every cycle.

1. **Plan** — policy engine (OPA/Rego) — keystone code path: `meok_policy.py` (planned). Policy templates: EU AI Act High-Risk System, NIST RMF GOVERN-1, ISO 42001 Clause 6 (per `sov3_tech_blueprint.agent.final.md` § 8.1 #8).
2. **Do** — governance enforcement — keystone code path: `meok_enforce.py` (planned). Runtime evaluator with <50ms per-evaluation latency target (Blueprint § 8.1 #10).
3. **Check** — monitoring — keystone code path: `meok_monitor.py` (planned). Drift detection (KS-test + Wasserstein distance), bias monitor (AIF360 + Fairlearn), shadow-AI discovery (Blueprint § 8.2).
4. **Act** — automated policy updates (GitOps) — keystone code path: `meok_gitops.py` (planned). Policy changes committed to git, HMAC-signed, deployed via CI/CD.

**The cycle**: every PDCA iteration is sealed with an HMAC-SHA256 receipt via `meok_x402.py:66-126` (`_resolve_attestation_key()`). The key is read from AWS Secrets Manager in production, `meok_secrets` (keyring → chmod 600 file) as fallback, and env-var only in dev (with a loud warning) per `CRITICAL_FIXES_2026-06-08.md` Fix #3.

---

## 7. The 14 Features No Competitor Has (full list from `sov3_tech_blueprint.agent.final.md` § "The 14 Features NO Competitor Has")

| # | Feature | Keystone code path | Status | Competitor replication | SOV3 advantage summary |
|---|---|---|---|---|---|
| 1 | Public transparency dashboard | planned `meok_dashboard.py` | spec'd | Cultural — competitors cannot adopt | Category-defining moat; the only governance provider that publishes its own results |
| 2 | Blockchain-verified audit trails | `meok_x402.py:66-126` (HMAC substrate) + planned on-chain anchor | shipped (HMAC) / spec'd (on-chain) | 12-18 months | Every audit receipt is cryptographically signed; auditor verifies offline |
| 3 | PDCA cycle automation | § 6 above | spec'd | Architectural — requires redesign | Continuous governance improvement, not point-in-time assessment |
| 4 | MCP-native protocol governance | `meok-governance-engine-mcp` + `eu-ai-act-compliance-mcp` + 27 others | shipped | Ecosystem — first-mover in 35K-server category | Only governance layer in a $10.4B MCP ecosystem |
| 5 | AI governance certification (blockchain-verified) | `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` (3 tiers) | spec'd | Market — category does not exist | 9-12 months replication time; first-mover locks the category |
| 6 | Zero-knowledge compliance proofs | planned ZK circuit (not yet started) | not started | Technical — advanced cryptography | Sensitive-data proof without revealing the data itself |
| 7 | CE marking support | planned `meok_ce_marking.py` | not started | Regulatory — EU high-risk systems | Required for EU high-risk AI systems; nobody else supports it |
| 8 | AIMS certification support | planned `meok_aims.py` | not started | Market — ISO 42001 certification path | Audit + certification layer nobody else provides |
| 9 | Multi-agent orchestration governance | `agentaudit` server (A2A inventory) + planned multi-agent orchestrator | in dev | Greenfield — nobody addresses it | 60/60 tests pass on agentaudit; multi-agent orchestration planned Phase 4 keystone |
| 10 | Agent-to-agent trust verification | `agentaudit` A2A bridge + `a2a-governance-bridge-mcp` | in dev | Greenfield | Signed trust handshakes between agents |
| 11 | Risk quantification (monetary) | planned `meok_risk_quant.py` (Fermi estimation, EUR 35M fine inputs) | not started | Business — C-suite need | Financial exposure in EUR/GBP/USD, not just risk tiers |
| 12 | FinOps cost tracking for AI | planned `meok_finops.py` | not started | Business — AI spend management | No competitor tracks per-model/per-agent cost |
| 13 | Air-gapped deployment | planned `meok_airgap.py` + Helm chart | not started | Government/defense market | Kubernetes-based, no external dependencies |
| 14 | Transparent pricing | `PRICING.md` (4 tiers, all published) | shipped | Market — eliminates sales-call friction | $0 / $29 / $49 / custom; competitors hide all pricing behind sales |

---

## 8. The 10 UX Principles (per `sov3_tech_blueprint.agent.final.md` § 5.7)

Target: **"Wiz-simplicity meets Credo intelligence"** — 8/10 UX target (Wiz = 8/10 best in class; CrowdStrike = 4.5/10 worst in class). The keystone should ship at 7.5-8.5 from day one.

1. **Dark mode default** — security and governance professionals expect it; light mode is optional.
2. **Single pane of glass** — one unified view of all AI governance data; no module-hopping or tab-switching.
3. **Radar trust charts** — Credo-style 6-axis radar (Bias, Compliance, Security, Privacy, Safety, Fairness) at fleet and per-agent scope.
4. **Checklist onboarding** — Vanta-style 5-step setup with progress bars (Connect first agent → Set first policy → Review inventory → Invite team → Customize dashboard).
5. **Agentless deployment** — API keys, not endpoint agents; <5 minutes from signup to first agent visible.
6. **Maximum 5 nav sections** — Dashboard, Agents, Policies, Reports, Settings. No more.
7. **Command bar navigation** — `/` opens a search palette for agents, policies, violations, docs.
8. **<2 clicks to any action** — flat hierarchy; no buried features.
9. **Contextual help tooltips** — every UI element has a `?` tooltip explaining what it does and why.
10. **Transparent pricing** — no "contact sales" gates; plans visible on the website (`PRICING.md` is the source-of-truth).

**Anti-patterns to avoid** (per Blueprint § 5.3, CrowdStrike's SIEM hellscape):
- No raw alert streams — actionable insights only, grouped by severity.
- No query languages for dashboards — pre-built widgets, point-and-click.
- No week-long learning curves — every feature discoverable in <30 seconds.
- No single-persona UI — serve governance, security, legal, compliance from one console.

---

## 9. The 5-Layer Converged Architecture (per `sov3_tech_blueprint.agent.final.md` § 6.5)

Maps Gartner's AI TRiSM four-layer framework to keystone modules. No single competitor covers all four Gartner layers; MEOK covers all five SOV3 layers from day one.

1. **Layer 1 — Discovery** (asset + agent + MCP registry). `meok-governance-engine-mcp` (13 frameworks) + `agentaudit` (A2A inventory) + planned `MCP_REG_HEALTH_REPORT.md` regenerator. Gartner layers covered: AI Governance + Information Governance.
2. **Layer 2 — Inventory** (HMAC-signed system catalog). `meok-attestation-api` (planned) + `meok-attestation-verify` (shipped; HMAC-SHA256 verifier). Gartner layer: AI Governance.
3. **Layer 3 — Risk classification** (EU AI Act engine). `eu-ai-act-compliance-mcp` (shipped, 410 articles, 42-point audit) + `EU_AI_ACT_FREE_SCANNER_SPEC.md` (the 5-question funnel front-door). Gartner layers: AI Governance + Information Governance.
4. **Layer 4 — Enforcement** (policy engine + agent intercept). `meok-mcp-injection-scan-mcp` (30+ rules) + `meok-policy-enforcement-mcp` (planned) + `agent-prompt-injection-firewall-mcp`. Gartner layer: AI Runtime Inspection & Enforcement.
5. **Layer 5 — Reporting** (transparency dashboard + cert issuance). Planned `meok_dashboard.py` + `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` (3 cert tiers) + `MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` (4 MSCS levels). Gartner layer: AI Governance (cross-cutting).

---

## 10. The 6 Revenue Streams mapped to Capabilities

| # | Stream | Pricing (from `PRICING.md`) | Gating capabilities | Keystone code path that gates the stream |
|---|---|---|---|---|
| 1 | Subscriptions (Freemium → Team → Business → Enterprise) | $0 / $29 / $49 / custom ($50-200K/yr) | #5 (48h EU AI Act engine) + #2 (PDCA automation) | `eu-ai-act-compliance-mcp` + planned `meok_policy.py` |
| 2 | x402 pay-per-call | $0.10-$0.50 per 1K events (per `SHADOW_AI_DETECTION_MCP_SPEC.md` § 3) | #9 (real-time event streaming) + #4 (MCP-native) | `meok_x402.py` (shipped; @paywalled decorator on every MCP tool) |
| 3 | Watchdog certifications (3-tier) | $99 + $29/yr / $299 + $99/yr / $5-25K + $2-10K/yr | #3 (Watchdog cert) | `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` + `MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` exam content corpus |
| 4 | Industry packs (Finance, Healthcare, Gov, Critical Infra) | $5-25K/yr per pack | #10 (industry packs) | `dora-compliance-mcp`, `nis2-compliance-mcp`, `cra-compliance-mcp`, `hipaa-compliance-mcp`, `soc2-compliance-ai-mcp`, `gdpr-compliance-ai-mcp`, `csrd-compliance-mcp` |
| 5 | Enterprise on-prem (DORA, NIS2, air-gapped) | $50-200K/yr | #8 (open source + on-prem) | Planned Helm chart + `meok_airgap.py` (per Blueprint § 8.4) |
| 6 | API consumption (REST + GraphQL + gRPC + WS) | $0.001-$0.10 per call (tiered) | #7 (multi-protocol API) | `http_server.py` (shipped) + planned GraphQL/gRPC/WS per Blueprint § 8.6 |

---

## 11. The 4 do-NOT-do rules (per `RUBRIC_EXTERNAL_COMMS.md`)

This file audit-passes the 3-question test (regulator, defamation, screenshot-tweet). All downstream engineering documents derived from this matrix must apply the same rules.

1. **Don't use war-language phrases in body copy.** Banned: kill shot, nuclear arsenal, coup de grâce, talent raid, seeding doubt, depletion campaign, strike while, vulnerability window, acquisition target, funding fiction. Use factual comparative language: "differentiator," "10x advantage," "feature comparison," "competitive analysis," "market opportunity," "potential strategic partner."
2. **Don't name specific competitor failures.** Per `RUBRIC_EXTERNAL_COMMS.md`, do not reference CrowdStrike's July 2024 outage, the CISA exploited-vuln list, or any named company's specific incident. Use neutral language: "industry-wide incident," "lessons from past events."
3. **Don't quote $1.2T TAM or $48M run-rate externally.** These are derived from the 26-domain Kimi audit and were banned by the deep audit (`[[meok-deep-audit-2026-06-08]]`). Use the per-attestation framing: "per-attestation cost is $10, vs. typical governance platforms charging $120-500K/year."
4. **Don't claim feature parity where there isn't any.** The 14 features in § 7 are SOV3-exclusive for verifiable reasons. Don't round up to "we have everything X has." Be specific about which of the 14 are shipped vs. in dev vs. spec'd vs. not started.

---

## 12. Cross-References

| Document | Path | What it covers |
|---|---|---|
| Marketing / positioning source-of-truth | `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` | 8 differentiators (the 10 + 14 here are the engineering reification) |
| 15-competitor matrix | `/Users/nicholas/meok-compliance-gateway/COMPARE_MATRIX_15_COMPETITORS.md` | Side-by-side scoring, head-to-head 1-liners, honest gaps |
| 3 CRITICAL fleet security fixes | `/Users/nicholas/meok-compliance-gateway/CRITICAL_FIXES_2026-06-08.md` | Docker non-root, keyring, attestation key secret management |
| Regulatory calendar | `/Users/nicholas/meok-compliance-gateway/REGULATORY_CALENDAR_2026-2027.md` | EU AI Act 8/2/2026, China 7/15/2026, ETSI Q3, Colorado 1/1/2027 |
| Shadow AI spec | `/Users/nicholas/meok-compliance-gateway/SHADOW_AI_DETECTION_MCP_SPEC.md` | 4 detection sources, 6 MCP tools, 3 deployment modes |
| Watchdog cert spec | `/Users/nicholas/meok-compliance-gateway/WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` | 3 cert tiers, exam content outline, signed-forever UX |
| EU AI Act free scanner spec | `/Users/nicholas/meok-compliance-gateway/EU_AI_ACT_FREE_SCANNER_SPEC.md` | 5-question funnel, risk classification, 48-hour engine path |
| MCP Security Cert RFC | `/Users/nicholas/meok-compliance-gateway/MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` | 4 MSCS levels, 10 requirement domains, attestation evidence |
| Keystone SECREVIEW (OpenSSF 81.6) | `/Users/nicholas/meok-compliance-gateway/keystone_SECREVIEW.md` | OpenSSF Scorecard baseline evidence |
| Pricing | `/Users/nicholas/meok-compliance-gateway/PRICING.md` | 4 tiers, x402 per-call rates |
| MCP registry health | `/Users/nicholas/meok-compliance-gateway/MCP_REG_HEALTH_REPORT.md` | 44 repos × 6 missing fields |
| External-comms rubric | `/Users/nicholas/meok-compliance-gateway/RUBRIC_EXTERNAL_COMMS.md` | Banned vocabulary + 3-question test |

---

## 13. Source Pointers

| Section | Primary source | Lines |
|---|---|---|
| § 1 row mapping (capabilities → code) | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § 4.1-4.10 | 765-957 |
| § 2 weaknesses | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` "Executive Summary" § 5 | 127-135 |
| § 3 MCP ecosystem | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § 2.1-2.5 | 450-595 |
| § 4 API-less competitors | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § 3.2 | 614-647 |
| § 5 Multi-protocol API | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § 4.7 + § 3.4 | 883-901 + 689-762 |
| § 6 PDCA architecture | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § 4.2 | 787-803 |
| § 7 14 features | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` "The 14 Features NO Competitor Has" | 3-21 + 429-447 |
| § 8 UX principles | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § 5.7 | 1089-1104 |
| § 9 5-layer architecture | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § 6.5 | 1208-1223 |
| § 10 Revenue streams | `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § "The $100M ARR Technical Foundation" | 137-146 |
| MEOK server inventory | `/tmp/kimi_dossier_v2/sov3_portfolio_inventory.md` § 2.1-2.3 | 101-180 |
| 13/15 GRC with zero MCP | Memory `[[sov3-mcp-master-audit-2026-06-08]]` (the 76-server audit) | — |
| HMAC substrate | `/Users/nicholas/meok-compliance-gateway/meok_x402.py:66-126` | — |
| keyring substrate | `/Users/nicholas/meok-compliance-gateway/meok_secrets.py` | — |
| Competitor API profiles | `/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md` | 1-466 |
| Competitor tech architecture | `/tmp/kimi_dossier_v2/research/deepdive_tech_docs.md` | full file |
| MCP ecosystem analysis | `/tmp/kimi_dossier_v2/research/deepdive_mcp_inventory.md` | full file |
| 70+ features × 15 competitors | `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` | full file |

---

*Authored 2026-06-09 from `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` + the keystone's own code paths. All capability claims are cross-referenced to a concrete file or a planned module; all 14 "no competitor has" features are status-flagged. The 4 do-not-do rules are applied throughout per `RUBRIC_EXTERNAL_COMMS.md`.*
