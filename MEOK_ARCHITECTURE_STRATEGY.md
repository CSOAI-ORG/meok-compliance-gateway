# MEOK Architecture Strategy — 10-Platform Deep-Dive Synthesis

> **Authored**: 2026-06-08
> **Purpose**: architectural strategy for the MEOK Compliance Gateway, synthesised from `/tmp/kimi_dossier_v2/research/deepdive_tech_docs.md` (982 lines, 15 platform/framework deep-dives + Key Architecture Insights). This is the **structural** companion to `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` — where the capabilities matrix says "MEOK has X", this doc says "here's what the 15 competitors tried, what worked, what failed, and the architectural gap MEOK fills."
> **Source**: `/tmp/kimi_dossier_v2/research/deepdive_tech_docs.md` § 1-15 (per-platform architecture) + § "Key Architecture Insights" (9 patterns that work, 9 patterns that fail, 6 unified gaps, 7 SOV3 moats) + 43 source citations.
> **Rubric**: factual comparative, no war language per `RUBRIC_EXTERNAL_COMMS.md`. Banned vocabulary in § 10.

## 1. The 15 platforms deep-dived

| # | Platform | Architecture pattern | Source doc § |
|---:|---|---|---|
| 1 | **CrowdStrike Falcon** | Cloud-native microservices, single 25MB agent, Threat Graph (2T+ events/week) | § 1 |
| 2 | **Microsoft Responsible AI Standard v2** | Internal process framework (Office of Responsible AI → Council → Digital RAI) | § 2 |
| 3 | **OneTrust AI Governance** | Modular bolt-on to legacy GRC; dense UI; 14K+ customers | § 3 |
| 4 | **Credo AI** | Governance Graph (frameworks/risks/controls as objects); radar trust chart; SDK-documented | § 4 |
| 5 | **Holistic AI** | Full-lifecycle + 50+ point-to-point integrations; dual runtime+governance layer | § 5 |
| 6 | **Cranium AI** | AI Bill of Materials (AIBOM); exposure management; Congressional testimony | § 6 |
| 7 | **WitnessAI** | Network-level agentless deployment; behavioral intent analysis; 4-quadrant view | § 7 |
| 8 | **Zenity** | Microsoft/ChatGPT/Salesforce/Agentforce focus; device agent; Forrester-recognized | § 8 |
| 9 | **Palo Alto Prisma AIRS** | Runtime security (no governance layer); API-documented at `pan.dev/airs` | § 9 |
| 10 | **ServiceNow IRM** | Bolt-on AI features to enterprise GRC; consultant-required deployment | § 10 |
| 11 | **Gartner AI TRiSM 2025** | 4-layer framework (Governance / Runtime / Information / Infrastructure) | § 11 |
| 12 | **Forrester AI Governance Landscape Q2 2025** | Market segmentation + vendor positioning | § 12 |
| 13 | **EU AI Act technical compliance** | 10 requirements (Art 6-51), conformity assessment, declaration | § 13 |
| 14 | **NIST AI RMF 1.0** | 4 functions (Govern / Map / Measure / Manage) as continuous loop | § 14 |
| 15 | **Modulos AI Governance** | Governance Graph + Scout deep-agent + ISO 42001 product conformity | § 15 |

## 2. The Gartner AI TRiSM 4-layer framework (industry reference model)

| # | Layer | Function | Example vendor |
|---:|---|---|---|
| 1 | **AI Governance** | Visibility, traceability, accountability (AI catalogs, continuous assurances) | Credo AI, Holistic AI, Modulos |
| 2 | **AI Runtime Inspection & Enforcement** | Real-time monitoring, anomaly detection, policy enforcement | Palo Alto Prisma AIRS, WitnessAI, CrowdStrike |
| 3 | **Information Governance** | Data access controls, classification, permission management | OneTrust, ServiceNow |
| 4 | **Infrastructure & Stack** | Traditional security controls for AI workloads | CrowdStrike, Palo Alto |

**Gartner market finding**: no single vendor addresses all 4 layers. Market is fragmented. 80% of AI failures are internal misuse / oversharing / unintended outputs (NOT external attacks). Market is consolidating: governance + runtime vendors merging.

## 3. The 9 patterns that work (per dossier)

| # | Pattern | Vendor exemplar | Why it works |
|---:|---|---|---|
| 1 | Cloud-native microservices | CrowdStrike, Palo Alto | Rapid scaling + deployment |
| 2 | Single lightweight agent | CrowdStrike (25MB) | Reduces deployment friction |
| 3 | Behavioral intent analysis | WitnessAI | More effective than keyword rules |
| 4 | Governance Knowledge Graph | Credo AI, Modulos | Connecting regulations, risks, controls |
| 5 | Network-level deployment | WitnessAI | Agentless architecture reduces friction |
| 6 | Continuous governance loop | Credo AI, Modulos | Not point-in-time compliance |
| 7 | Runtime + Governance dual layer | Holistic AI | The "winning architecture pattern" per the dossier |
| 8 | AI Bill of Materials (AIBOM) | Cranium | Comprehensive inventory approach |
| 9 | Four-layer AI TRiSM (Gartner) | (Framework, not vendor) | Industry reference model |

## 4. The 9 patterns that fail (per dossier)

| # | Pattern | Vendor exemplar | Why it fails |
|---:|---|---|---|
| 1 | Bolt-on AI features | OneTrust, ServiceNow | Legacy GRC tools cannot adapt to AI governance |
| 2 | Pure documentation layers | Credo AI | Governance without enforcement = no teeth |
| 3 | Platform-specific limitations | Zenity (Microsoft only) | Enterprises use multiple platforms |
| 4 | Point-to-point integrations | Holistic AI (50+ sources) | Unmaintainable at scale |
| 5 | Agent-heavy deployment | Zenity device agent | Creates deployment friction |
| 6 | No runtime enforcement | Credo AI, OneTrust | Governance without teeth |
| 7 | Pure security without governance | Palo Alto, CrowdStrike | Missing compliance layer |
| 8 | Internal process frameworks | Microsoft RAI | Not productizable or scalable |
| 9 | Fragmented market | All vendors | Gartner confirms no vendor covers all 4 layers |

## 5. The 6 unified-architecture gaps (MEOK's wedge)

**No vendor currently provides:**

1. **AI model/agent registry + runtime enforcement + compliance documentation + risk assessment** in one platform
2. **Platform-agnostic coverage** (across Microsoft, AWS, GCP, custom frameworks)
3. **Continuous governance** (not point-in-time audits)
4. **Unified API layer** (instead of 50+ point-to-point integrations)
5. **Agentless + agent-based hybrid deployment** options
6. **Behavioral intent analysis + policy enforcement + audit trails** end-to-end

## 6. The 7 SOV3 technical moats (dossier-validated)

| # | Moat | Defended by | Maps to keystone |
|---:|---|---|---|
| 1 | **Unified Governance + Runtime** | First platform to combine governance (registry, compliance, risk) with runtime enforcement (security, monitoring, blocking) | `meok-compliance-gateway` (governance) + `meok-mcp-injection-scan-mcp` (runtime) |
| 2 | **Platform-Agnostic Design** | Unified abstraction layer across Microsoft, AWS, GCP, custom | 13 frameworks, multi-cloud deploys |
| 3 | **Continuous Compliance** | Operationalize EU AI Act 10-yr retention, NIST RMF continuous loop, ISO 42001 — as operating processes not documentation | Article 12 auto-logging (6-mo+ retention), BFT governance loop |
| 4 | **Hybrid Deployment** | Both agentless (network-level, like WitnessAI) and agent-based (endpoint) | MCP server (agentless) + optional agent (keystone) |
| 5 | **Knowledge Graph Foundation** | Extend Credo's governance graph to include runtime behavior data | The keystone's inventory + attestation graph (per `meok_x402.py:66-126`) |
| 6 | **API-First Architecture** | Single unified API for all governance and security operations | REST + GraphQL + gRPC + WebSocket (per `MEOK_API_STRATEGY.md`) |
| 7 | **Agentic AI Governance** | Use AI to govern AI — autonomous governance agents | `agentaudit` A2A agent inventory + `openmoe-bft-mcp` BFT consensus |

## 7. The 4 vendor categories (competitive positioning)

| # | Category | Vendors | MEOK counter-position |
|---:|---|---|---|
| 1 | **Security-focused** | HiddenLayer, AIShield, Mindgard | MEOK adds governance layer (they don't have it) |
| 2 | **Governance-focused** | Credo AI, Holistic AI, OneTrust | MEOK adds runtime enforcement (they don't have it) |
| 3 | **Runtime-focused** | Palo Alto Prisma AIRS, WitnessAI | MEOK adds governance + compliance (they don't have it) |
| 4 | **Platform-native** | Microsoft, Google, AWS | MEOK is platform-agnostic (they're not) |

**MEOK positioning**: spans all 4 categories by combining governance + runtime + platform-agnostic + multi-cloud, addressing the unified-architecture gap (the dossier's central finding).

## 8. The 4 EU AI Act technical-compliance requirements (from § 13)

| # | Requirement | MEOK implementation |
|---:|---|---|
| 1 | **Risk classification** (Art 6) | `eu-ai-act-compliance-mcp` `risk.classify()` — prohibited / high-risk / limited / minimal |
| 2 | **Conformity assessment** (Art 43) | `conformity.generate()` — Annex VI internal control, 80-200 pages |
| 3 | **Technical documentation** (Art 11 + Annex IV) | `techdocs.generate()` — 15 categories, 4-8 wk human time → <2h |
| 4 | **EU database registration** (Art 71) | `eu_database.register()` — direct submission via EU API |

## 9. The NIST AI RMF 4-function implementation (from § 14)

| # | Function | What it does | MEOK implementation |
|---:|---|---|---|
| 1 | **GOVERN** | Establish AI risk management policies, culture, roles | `policy.create()` + `roles.assign()` — keystone core |
| 2 | **MAP** | Identify risks and their context | `risk.register.create()` + `system.catalog()` |
| 3 | **MEASURE** | Implement metrics and testing | `model.accuracy.test()` + `adversarial.probe()` + `bias.detect()` |
| 4 | **MANAGE** | Implement controls and monitor | `policy.enforce()` + `incident.respond()` + `audit.export()` |

**Key insight** (per dossier § 14): most orgs fail because they treat NIST RMF as a documentation exercise, not an operating model. MEOK operationalizes it as a continuous automated process — the keystone's BFT governance loop runs all 4 functions continuously, not on a project basis.

## 10. The 4 "do NOT do" rules

1. **Do NOT name-and-shame specific competitors for their architectural failures.** The dossier's "patterns that fail" table is the factual research — cite it without turning it into an attack. Use the pattern (e.g. "bolt-on AI features") not the vendor's reputation.
2. **Do NOT use war vocabulary.** Banned per `RUBRIC_EXTERNAL_COMMS.md` § 8: "kill shot", "nuclear arsenal", "coup de grâce", "talent raid", "seeding doubt", "depletion campaign", "strike while", "vulnerability window", "acquisition target", "funding fiction".
3. **Do NOT claim vendor architectures that aren't public.** The dossier's architecture summaries are based on white papers + documentation + platform pages. Do not speculate about internals (e.g. "CrowdStrike's backend is written in C++" — the dossier says "Likely C++" which is the honest hedge).
4. **Do NOT overclaim "first" status for capabilities that are partially implemented elsewhere.** The 7 SOV3 moats all build on partial work from other vendors (e.g. Modulos's governance graph, WitnessAI's behavioral intent, Cranium's AIBOM). The accurate claim is "first to unify all 4 Gartner TRiSM layers in one platform" — not "first to do any of these things."

## 11. Cross-references

- `/Users/nicholas/meok-compliance-gateway/SOV3_UNIQUE_CAPABILITIES_MATRIX.md` — the 10 SOV3-exclusive capabilities (the "what" — this doc is the "why and how").
- `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` — the 8 differentiators (different framing, same evidence base).
- `/Users/nicholas/meok-compliance-gateway/COMPARE_MATRIX_15_COMPETITORS.md` — 15-competitor feature matrix (the "what they have" — this doc is "how they built it").
- `/Users/nicholas/meok-compliance-gateway/EU_AI_ACT_DEADLINE_INTEL.md` — the 9 high-risk requirements (this doc § 8 is the architectural mapping).
- `/Users/nicholas/meok-compliance-gateway/MEOK_API_STRATEGY.md` — API-first as one of the 7 moats.
- `/Users/nicholas/meok-compliance-gateway/MCP_MARKETPLACE_STRATEGY.md` — multi-protocol deployment (moat #4 hybrid).
- `/Users/nicholas/meok-compliance-gateway/SHADOW_AI_DETECTION_MCP_SPEC.md` — runtime enforcement (moat #1).
- `/Users/nicholas/meok-compliance-gateway/WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` — continuous governance (moat #3).
- `/Users/nicholas/meok-compliance-gateway/SOV3_FINANCIAL_MODEL_2026-2028.md` — Stream 1 (Cloud) revenue supports the runtime + governance moat (INTERNAL ONLY).
- `/Users/nicholas/meok-compliance-gateway/MEOK_UX_STRATEGY.md` — UX wedge supports the API-first moat (Wiz-style single-pane-of-glass).
- `/Users/nicholas/meok-compliance-gateway/sov3_tech_blueprint.agent.final.md` (in `/tmp/kimi_dossier_v2/`) — the canonical technical-blueprint source for the keystone's actual architecture.
- [[sov3-mcp-master-audit-2026-06-08]] — the 76-server audit that documents the MCP-side architectural surface.
- [[eat-execute-july4-plan-2026-06-08]] — Lane E (keystone docs), this is one of the docs in that lane.

## 12. Source pointers

- `/tmp/kimi_dossier_v2/research/deepdive_tech_docs.md` (full file, 982 lines, 43 source citations).
- CrowdStrike: `crowdstrike.com/en-us/platform/` + 2 white papers + 2 deep-dive analyses.
- Microsoft: `microsoft.com/insidetrack/blog/responsible-ai/` + VerifyWise Responsible AI Standard v2.
- OneTrust: Wikipedia + Digital Marketplace G-Cloud service profile.
- Credo AI: `credo.ai/` + `credo.ai/product` + `docs.sdk.credo.ai/`.
- Holistic AI: `holisticai.com/` + UK Gov assessment + Modulos comparison.
- Cranium: Azure Marketplace listing + 2 press releases + Congressional testimony.
- WitnessAI: CheckThat.ai profile + $58M funding press.
- Zenity: 2 press releases (ChatGPT Enterprise + Forrester recognition) + Salt Security comparison.
- Palo Alto: `docs.paloaltonetworks.com/ai-runtime-security` + `pan.dev/airs/` + juaraits Medium guide.
- ServiceNow: Devoteam expert view + XenonStack GRC analysis.
- Gartner AI TRiSM 2025: Mindgard blog + AIShield recognition.
- Forrester AI Governance Landscape Q2 2025: Forrester report `RES182336`.
- EU AI Act: SureCloud compliance guide + ISACA white paper + FPF conformity assessment + Fraunhofer IKS white paper.
- NIST AI RMF 1.0: `nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf` + Modulos implementation + Elevate roadmap.
- Modulos: `modulos.ai/modulos-vs-holistic-ai/`.
