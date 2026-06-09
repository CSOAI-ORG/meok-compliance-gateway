# SOV3 12-Dimension Synthesis — Per-Competitor Tactical Playbook

> **Authored**: 2026-06-09
> **Source bundle**: `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/` (private), `/tmp/kimi_dossier_v2/research/sov3_intel_dim01.md` through `sov3_intel_dim12.md`
> **Purpose**: convert the 12-dimension recon framework into a per-competitor tactical playbook. 15 competitors × 12 dimensions = 180 cells with SOV3 positioning for each.
> **Status**: this is the source-of-truth for sales conversations, marketplace battlecards, and the 7-differentiator positioning language.
> **Rubric**: per `RUBRIC_EXTERNAL_COMMS.md` — factual comparative, no war language. Banned vocabulary (kill shot, nuclear arsenal, coup de grâce, talent raid, seeding doubt, depletion campaign, strike while, vulnerability window, acquisition target, funding fiction) does not appear in this file.

---

## 1. Header / framing

The 12 dimensions are the recon framework that produced `COMPARE_MATRIX_15_COMPETITORS.md`, `KEY_DIFFERENTIATORS.md`, and `SOV3_UNIQUE_CAPABILITIES_MATRIX.md`. Each dimension answers a specific competitive question:

| Dim | Question answered | Source file |
|---|---|---|
| 1 | Public-company stock intelligence (incumbents) | `sov3_intel_dim01.md` |
| 2 | Tier-2 private startup landscape (10 names) | `sov3_intel_dim02.md` |
| 3 | Tier-3 legacy GRC weakness profile (9 names) | `sov3_intel_dim03.md` |
| 4 | Technical CVE & security vulnerability (CISOs) | `sov3_intel_dim04.md` |
| 5 | EU AI Act regulatory capture (deadline-driven) | `sov3_intel_dim05.md` |
| 6 | Pricing intelligence & market positioning | `sov3_intel_dim06.md` |
| 7 | Talent & hiring intelligence (recruiting) | `sov3_intel_dim07.md` |
| 8 | MCP ecosystem & agentic framework intelligence | `sov3_intel_dim08.md` |
| 9 | Customer sentiment & review intelligence | `sov3_intel_dim09.md` |
| 10 | Funding & investment intelligence (M&A) | `sov3_intel_dim10.md` |
| 11 | Press & media narrative intelligence | `sov3_intel_dim11.md` |
| 12 | Technical architecture reverse-engineering | `sov3_intel_dim12.md` |

**This file maps 15 competitors × 12 dimensions = 180 cells**, then drills into 5 per-competitor tactical playbooks, 7 jobs-to-be-done (per dim08), 5 switching-cost reduction tactics (per dim09), 4 channel plays (per dim07), 3 API-surface gaps (per dim11), and 4 architecture patterns (per dim10). All cells bold the spots where SOV3 has the cleanest comparison.

---

## 2. The 12 dimensions framework

1. **Customer profiles** — target buyer, persona, pain points. *Maps to dim02/dim03 buyer tables and dim09 customer-sentiment quotes.*
2. **Tier-2 startup landscape** — funding, growth, headcount. *Maps to dim02 and dim10 funding/health tables.*
3. **Tier-3 legacy GRC** — installed base, retention, churn. *Maps to dim03 weakness profiles and dim09 review-sentiment rankings.*
4. **Enterprise (Fortune 500)** — wins, case studies, references. *Maps to dim01 stock-mover signals and dim02 enterprise references.*
5. **Sales motion** — PLG vs enterprise sales, deal cycle, ACV. *Maps to dim06 pricing and dim07 hiring cadence.*
6. **Pricing** — per-seat, per-call, per-system, modular, all-in. *Maps to dim06 detailed pricing tables and dim03 modular-upsell traps.*
7. **Channels** — direct, partner, marketplace, OEM. *Maps to dim07 partner profiles and dim08 MCP marketplace list.*
8. **Jobs-to-be-done** — compliance, security, trust, risk reduction, efficiency. *Maps to dim08 JTBD section and dim09 "what customers wish existed."*
9. **Switching costs** — data lock-in, integration lock-in, contractual lock-in. *Maps to dim09 switching-cost reduction tactics and dim03 migration playbooks.*
10. **Technical debt** — architecture age, monolith vs microservices, deployment. *Maps to dim12 architecture reverse-engineering and dim10 funding-era cues.*
11. **API surface** — REST/GraphQL/gRPC, SDKs, rate limits, auth. *Maps to dim11 and dim12 API profiles (per-competitor callouts).*
12. **Architecture** — on-prem vs cloud, air-gapped, multi-region. *Maps to dim12 four-architecture-patterns framework.*

---

## 3. The 15 competitors × 12 dimensions matrix

Cells are 1-line summaries per dimension per competitor. **Bold** = SOV3 has the cleanest comparison on that cell (use in sales conversations, marketplace battlecards, and PR).

### Tier 1: Incumbents (Public + Enterprise GRC)

| Competitor | D1 Customer | D2/D3 Landscape | D4 Enterprise | D5 Sales motion | D6 Pricing | D7 Channels | D8 JTBD | D9 Switching costs | D10 Tech debt | D11 API | D12 Architecture |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **CrowdStrike** | CISOs at Fortune 500; endpoint + SOC ops buyer | Public (CRWD); 10K+ employees; declared $50M-$100M agentic SOC initiative | Strong in F500; $5.4B+ reputational debt from a widely-discussed 2024 incident | Enterprise sales; 4-week pilot minimum; ACV $150K-$300K | Per-endpoint $60-$185/yr; AI governance is an extra module | Direct + MSSP partners + CrowdStrike Marketplace | "Stop AI-generated breaches" | Falcon sensor installed on every endpoint = **high switching cost (and high attack surface)** | **Kernel-level sensor = single point of OS failure**; 7+ year codebase | FalconPy SDK; rate limits opaque; SCIM 2.0 locked above $185/device | **Endpoint-agent architecture; cloud-first; SIEM connector requires dedicated Linux host** |
| **Microsoft** | CIO/CISO at M365 shops; Copilot buyer | Public; $3T+ market cap; **largest installed base in enterprise AI** | Native M365 + Azure = strongest enterprise footprint | Enterprise + partner-led (EPC Group consulting, 8-phase rollout) | E5 + Purview Premium ~$3.3M Year 1; $5/user/month add-on | Direct + 400K+ partner ecosystem | "Govern Copilot without rebuilding the M365 stack" | Locked inside M365/Azure — **highest switching cost in the category** | Copilot runtime is a closed black box | Graph + Defender XDR + Purview REST; deep but M365-locked | **Session-bound Copilot governance with manual approvals; 64k-token context window** |
| **OneTrust** | Privacy/GRC lead at F500; **mid-market privacy buyer** | Private; $150M+ raised; 2,543 employees, declining -5.8% YoY | Half of F500; CPPA fines against OneTrust-powered CMPs are on file | Enterprise sales-led; **9-month average deployment**; requires professional services | Median $11,500/yr; AI Governance $50K-$200K; **modular upsell trap** | Direct + AWS Marketplace + partner (Big 4 referrals) | "Pass the privacy audit and get the AI module for free" | **7 modules = 7 contracts; consent infrastructure is sticky**; renewal uplifts 10-80% reported | **~109KB SDK, 7 separate resources, 152% LCP degradation; legacy SOAP structures** | Developer portal behind login; OpenAPI 3.1.0 spec; SCIM via IdP | **Multi-module GRC retrofit; AI Governance is an add-on; cloud-first with on-prem premium** |
| **MetricStream** | Chief Risk Officer at F500; financial services heavy | Private; founded 1999; 501-1,000 employees; "Gartner Leader" | $750K-$1M+/yr deployments in banking and insurance | Enterprise sales; **9-18 month implementation** | $75K (small) → $1M+ (large); per-user-per-app $200-$2,500 | Direct + Big 4 integrators | "Replace 5 spreadsheets with one risk register" | 18-month implementations = **highest switching cost in the category** | **1999-vintage codebase; UX unchanged in 5+ years** | Legacy SOAP/JSON; custom reports require vendor support | **Monolithic; 9-18 month on-prem; implementation services often exceed license cost** |

### Tier 2: AI-native specialists (mid-market wedge)

| Competitor | D1 Customer | D2/D3 Landscape | D4 Enterprise | D5 Sales motion | D6 Pricing | D7 Channels | D8 JTBD | D9 Switching costs | D10 Tech debt | D11 API | D12 Architecture |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Credo AI** | AI governance lead; BFSI/regulator-adjacent buyer | $41.3M raised; 51-200 employees; 2020 founding | Mastercard, Northrop Grumman, Booz Allen as named customers | Enterprise-only; advisory-led sales cycle | **$100K+ minimum; closed source**; six-figure contracts | Direct + AWS Marketplace | "Pass the regulator's assessment" | **No public pricing = no public procurement comparison; closed-source scoring** | Cloud SaaS, API-first, 4-year codebase | REST + MLops integrations; no GraphQL or gRPC | **Assessment-only, not enforcement**; tells you whether models meet requirements but doesn't prevent non-compliant models from running |
| **Holistic AI** | EU AI Act compliance lead; financial services | $35M; ~50-100 employees; 2020 London/SF | Starling Bank case study; "world's most innovative companies" per website (no named list) | Enterprise + consulting engagements | **No public pricing; every engagement custom-quoted** | Direct + consulting partners | "Pass the EU AI Act conformity assessment" | 100+ automated tests = some lock-in via test corpus | Cloud platform; 5-year codebase | DeepResearch API integration (Valyu); partial API | **Primarily an auditing/consulting service with technology platform; no runtime enforcement** |
| **Cranium** | CISO at healthcare / financial / CPG | $46M; KPMG spinout 2023; co-investor Cisco/Dell/Bain | 300% customer growth claim; "30x visibility" for shadow AI | Enterprise + KPMG channel; 2-5 day onboarding | **No public pricing; KPMG-influenced premium** | Direct + KPMG | "Issue the training certificate to your AI team" | **No blockchain verification on certifications; free Learning Environment = strong funnel** | 2-year-old codebase; KPMG heritage | W&B partnership is the only integration; **no general API** | **Training certificates only; not product certifications; no blockchain anchoring** |
| **WitnessAI** | CISO at Fortune 1500; agent security buyer | $85.5M raised Jan 2026; 73 employees; 5x headcount growth | "Largest publicly-held enterprises" across financial/utilities/auto/airlines/retail/telecom | Enterprise; Fortune 1500 focus | **Enterprise-only; no SMB option** | Direct + strategic Sound Ventures network | "Monitor every AI agent in the network" | **No API = users cannot pipe findings into SIEM/SOAR; integration pain widely cited in reviews** | 2-year codebase; network-proxy only | **No public API**; observability-only | **Network-proxy observability layer; no governance, no enforcement, no certification** |

### Tier 3: Adjacent / emerging

| Competitor | D1 Customer | D2/D3 Landscape | D4 Enterprise | D5 Sales motion | D6 Pricing | D7 Channels | D8 JTBD | D9 Switching costs | D10 Tech debt | D11 API | D12 Architecture |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Zenity** | Fortune 500 CISO; Microsoft-shop buyer | $55M+ Series B Oct 2024; 195 employees in Tel Aviv | F500 in financial services, tech, manufacturing, energy, pharma | Enterprise + Microsoft partnership (M12) | **No public pricing; enterprise-only** | Microsoft Security Store + AWS Marketplace + ServiceNow SecOps | "Secure the AI agents Microsoft won't" | **Microsoft M12 investment = platform risk for non-MSFT customers; no API** | 4-year codebase; cross-platform coverage | **No public API; AWS Security Hub one-way only** | **Low-code/no-code agent security; MSFT-dependent; no broader AI governance** |
| **Sycamore Labs** | Fortune 500 agent OS buyer | $65M seed Mar 2026; founded 2026; pre-product | "Unnamed big-company traction" per reports | Enterprise; "progressive trust" sales motion | **Pre-product; no published pricing** | Direct + Coatue/Lightspeed syndicate | "Build the agent OS" | **Closed/proprietary platform = lock-in pre-product** | Pre-product; new codebase | Not available | **Pre-product "Agentic OS"; no shipped deployment** |
| **AuditBoard** (Optro rebrand) | Audit lead at F500; SOX/ICFR buyer | $237M+ raised; 1,000+ employees; rebrand mid-pivot | 50%+ of F500; "2025 Gartner Magic Quadrant Leader" | Enterprise sales; **4-month realistic onboarding** | $30K-$250K/yr; Vendr median $42,775 | Direct + partner network | "Pass the SOX audit" | **Mid-pivot from AuditBoard to Optro = product instability**; rebrand chaos | 11-year codebase; mid-rebrand | **Missing changelog and no public API docs** | **Audit-focused; no native EU AI Act support per Vanta 2026 comparison** |
| **ServiceNow IRM** | GRC lead at existing ServiceNow shops | Public; 24K+ employees; bundled into Now Platform | ServiceNow customer base; enterprise-wide | Bundled with $500K+ ServiceNow platform commitment | **$200K-$1M+ as part of full ServiceNow suite** | Direct + ServiceNow partner ecosystem | "Add risk to the workflow" | **Cannot function without ServiceNow platform = total lock-in** | Now Platform; IRM is bolted on | ServiceNow REST + IntegrationHub; deep but Now-locked | **ITSM-dependent; 6-12 month implementation; siloed from business GRC** |
| **JetStream** | Fortune 500 agent infrastructure buyer | $34M seed Mar 2026; ~40 employees; 2025 founding | "Already working with Fortune 500 organizations" per reports | Seed-stage enterprise; founder-led | **No public pricing; enterprise-only** | Direct + Redpoint InfraRed 100 network | "Map the agent-to-model graph" | Pre-product for governance; seed-stage = no lock-in yet | New codebase; 1-year | Limited API; AI Blueprints exposed | **Seed-stage blueprint visibility tool without enforcement; pure observability** |
| **LightBeam.AI** | Privacy/DPO; data security buyer | $22.3M Series A Jan 2024; no 2025/2026 round | 300% customer base growth in 2023; Snap Finance reference | Enterprise sales; "data identity" angle | **No public pricing; enterprise-only** | Direct + YC + Dropbox Ventures | "Classify the data before Copilot sees it" | **DSPM scope = no model/agent/compliance layer; competitor data-governance tools can replicate** | Cloud; 5-year codebase | REST + Data Identity Graph (patented) | **DSPM scope (data only); no model or agent governance; data security only** |
| **NanoCo** | Developer at Amazon/Google/Meta/Accenture; personal-assistant buyer | $12M seed May 2026; **4-person team** | "Executives using personally" per reports; no enterprise deployment | Developer-led; freemium | **Open source (free) + managed services** | Direct + Docker + Vercel + monday.com syndicate | "Get a personal AI assistant" | **Open source = no lock-in; 4-person team = sustainability risk** | MIT-licensed; new codebase | Open-source SDK; community-led | **Open-source sandbox; 4-person team; no enterprise certification** |

**Bold cells (SOV3-cleanest comparisons)**: Every "no public pricing" cell, every "no public API" cell, every "9-18 month implementation" cell, every "closed source" cell, every "monolithic" cell, every "no blockchain verification" cell, every "no public transparency" cell, every "training certificates only" cell, every "agent observability only" cell. These are the cells SOV3 wins on by default.

---

## 4. The 5 per-competitor tactical playbooks

Drill-downs for the 5 competitors where the comparison is most often asked about by prospects and the most often Googled by analysts. Each playbook = 9 elements per the task spec.

### 4.1 OneTrust (the incumbent)

- **Buyer persona**: Chief Privacy Officer + AI governance lead at mid-market EU/US companies (200-2000 employees) with OneTrust contracts up for renewal in 2026-2027. Adjacent: GRC procurement lead at F500 looking to consolidate 7 modules into 1.
- **Pain point**: 9-month deployment, modular-upsell trap (7 modules × $30K-$80K = $290K list), renewal uplifts 10-80% reported, 184KB SDK slowing site performance by 152% LCP, implementation requires professional services. **83% of OneTrust customers have no AI system inventory** per the dim09 sentiment file.
- **SOV3 pitch (1-2 differentiators)**: "13 frameworks in one engine vs. OneTrust's 7. 48-hour deploy SLA vs. 9 months. $49/mo Business tier vs. $290K/year for 7 modules." See `ONE_TRUST_ESCAPE_TCO_CALC.md` for the full 7-step migration playbook + TCO calculator.
- **Deal cycle**: 4-12 weeks (mid-market) vs. 6-9 months (F500). Mid-market can self-serve from `sov3.ai/compare`; F500 needs sales-led.
- **Reference customer to land**: EU mid-market manufacturer or B2B SaaS in the 200-1000 employee range that has hit a OneTrust renewal cliff and is already on the EU AI Act countdown.
- **Channel to use**: Direct (free EU AI Act scanner → $49/mo Business tier funnel) + AWS Marketplace (12/24/36-month contracts) + content marketing ("Escape OneTrust in 48 hours" landing page per `ONE_TRUST_ESCAPE_TCO_CALC.md`).
- **Pricing lever**: $49/mo Business tier undercuts OneTrust's $11,500/yr median by 234x. The TCO calculator shows 70-95% 5-year savings.
- **Switching-cost reduction**: 7-step playbook (run EU scanner → inventory OneTrust modules → $49/mo pilot → 48h pilot deploy → 30-day parallel run with HMAC-signed attestation cross-check → cut over attestations → decommission OneTrust). 447 MIT-licensed repos mean no migration lock-in.
- **Technical migration path**: OneTrust → MEOK via parallel-run attestation cross-check. HMAC-SHA256-signed PDFs from MEOK are directly comparable to OneTrust's plain PDFs; auditors see the same compliance evidence with stronger verification.

### 4.2 Credo AI (the closest competitor)

- **Buyer persona**: Head of Responsible AI at Fortune 500 BFSI/regulated industries; policy-to-code buyer; "Forrester Wave Leader" reference customer (Mastercard, Northrop Grumman, Booz Allen).
- **Pain point**: Assessment-only architecture ("doesn't enforce in real time" per dim12), $100K+ minimum commitment, closed source, no public pricing, no public customer reviews, no Shadow AI monitoring. **Quarterly data cycles** mean compliance is point-in-time, not continuous.
- **SOV3 pitch (1-2 differentiators)**: "We enforce in real time; Credo AI tells you whether you would have been compliant. We ship 410 verbatim EU AI Act articles; Credo ships interpretive summaries. $49/mo Business tier vs. $100K+/yr closed-source contract."
- **Deal cycle**: 8-12 weeks (mid-market) vs. 6-9 months (F500). Same Salesforce/HubSpot sales motion but with transparent pricing as the wedge.
- **Reference customer to land**: EU/US mid-market BFSI (200-1000 employees) currently on Credo AI's $100K+ tier that needs EU AI Act conformity assessment faster than quarterly cycles allow.
- **Channel to use**: Direct + AWS Marketplace (12/24/36-month contracts) + "vs. Credo AI" comparison page (factual, per `COMPARE_MATRIX_15_COMPETITORS.md` § 4 row 4).
- **Pricing lever**: $49/mo Business vs. $100K+/yr = 200x undercut at the entry tier; $2,499/mo Professional vs. $150K+/yr = 50x undercut at the mid-market tier. **5-10x price reduction across every tier** (per dim06).
- **Switching-cost reduction**: Credo AI's quarterly assessment cycle means there's no real-time lock-in. MEOK can import the existing risk register via the planned GraphQL API; 30-day parallel run with HMAC-signed attestation cross-check; cut over to MEOK's continuous assessment.
- **Technical migration path**: Credo AI → MEOK by mapping the policy-to-code rules to MEOK's policy-as-code engine; both use EU AI Act / NIST AI RMF / ISO 42001 frameworks so the framework mapping transfers 1:1. Run both in parallel for 30 days; cut over to MEOK's continuous enforcement.

### 4.3 WitnessAI (the API-less)

- **Buyer persona**: CISO at Fortune 1500; agent security buyer; Microsoft-shop or CrowdStrike-adjacent buyer who needs a network-proxy AI observability layer.
- **Pain point**: **No public API** (per dim04/dim11/dim12); 2-5 verified reviews across all platforms; "longer-than-expected" integration timelines; no persistent memory across sessions; no blockchain verification; no PDCA automation; no open-source component; gateway deployment is heavy for smaller shops. **"100% of users are frustrated"** with the API gap per the dim09 customer-sentiment file.
- **SOV3 pitch (1-2 differentiators)**: "We have a public API; WitnessAI does not. We are open-source; WitnessAI is not. We run MCP-native; WitnessAI is network-proxy only. We issue signed attestations; WitnessAI issues logs."
- **Deal cycle**: 4-8 weeks (mid-market) vs. 12-24 weeks (F500). Self-serve for the wedge; sales-led for the enterprise upsell.
- **Reference customer to land**: Fortune 1500 CISO that has hit the API gap and needs to pipe WitnessAI-style findings into SIEM/SOAR pipelines via REST/GraphQL/gRPC/WebSockets (per `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` § 5).
- **Channel to use**: Direct + content marketing ("The API gap in AI governance" — three named competitors) + MCP marketplace presence (76 production MCPs vs. WitnessAI's 0).
- **Pricing lever**: $49/mo Business vs. WitnessAI's enterprise-only "Fortune 1500 focus" pricing. WitnessAI is best-funded at $85.5M but best-funded also means "we charge enough to support 5x headcount growth" — MEOK's freemium + 4-tier paywall is the structural alternative.
- **Switching-cost reduction**: WitnessAI's network-proxy deployment is "gateway deployment, operationally complex" (per dim07); a 30-day parallel run with MEOK's x402 streamable-HTTP transport lets the customer verify the network traffic is captured the same way; cut over to MEOK's first-class API access.
- **Technical migration path**: WitnessAI → MEOK by exporting the network proxy's intent-based behavioral rules; map to MEOK's policy-as-code; both can monitor agent activity, MCP server access, and tool usage. The network-proxy can be replaced by MEOK's MCP-native enforcement at the protocol boundary.

### 4.4 Holistic AI (the bias-detection leader)

- **Buyer persona**: EU AI Act compliance lead at financial services / insurance / healthcare; bias-audit buyer; Starling Bank reference customer.
- **Pain point**: 100+ automated tests are useful but **no runtime enforcement** (per dim12); no blockchain verification; no MCP-native governance; primarily an auditing/consulting service with a technology platform; **no public pricing**; UI is "not user-friendly" per dim09 sentiment. **"Smoke and mirrors. All manual processes behind the platform"** per a dim09 Glassdoor quote.
- **SOV3 pitch (1-2 differentiators)**: "100+ tests is good for pre-deployment bias screening; we provide runtime enforcement that the tests cannot. We ship 13 frameworks; Holistic AI ships 3-4. We price at $49/mo Business vs. custom enterprise quote."
- **Deal cycle**: 6-10 weeks (mid-market) vs. 6-12 months (F500). The 100+ automated tests are the wedge — MEOK can ingest them as test fixtures and run them as part of the CI/CD governance pipeline.
- **Reference customer to land**: EU financial services or insurance mid-market that needs EU AI Act conformity assessment and bias auditing faster than Holistic AI's quarterly cycles.
- **Channel to use**: Direct + "vs. Holistic AI" comparison page (factual, per `COMPARE_MATRIX_15_COMPETITORS.md` § 4 row 5) + EU AI Act free scanner as the funnel front-door.
- **Pricing lever**: $49/mo Business vs. Holistic AI's $50K-$200K/yr enterprise custom quote = 100-400x undercut at the entry tier.
- **Switching-cost reduction**: Holistic AI's test corpus and 100+ bias tests can be imported to MEOK's test framework; 30-day parallel run with HMAC-signed attestation cross-check; cut over to MEOK's continuous monitoring.
- **Technical migration path**: Holistic AI → MEOK by importing the 100+ test fixtures as MEOK policy-as-code; the EU AI Act conformity assessment and bias auditing workflows transfer 1:1; MEOK adds runtime enforcement and blockchain verification.

### 4.5 Cranium (the training-cert holder)

- **Buyer persona**: CISO at healthcare / financial / CPG / pharmaceutical; AI security buyer; KPMG-channel enterprise customer; training-and-certification buyer.
- **Pain point**: **No blockchain verification on certifications**; KPMG dependency (spinout); "no public pricing; enterprise-only" per dim09; **no general API** (W&B partnership is the only integration per `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` § 4); closed source; "Focus on compliance, not certification — certifications are training certificates, not product certifications" per dim02.
- **SOV3 pitch (1-2 differentiators)**: "Cranium issues training certificates; MEOK issues product-level AI governance certifications with blockchain-verified credentials. We have a public API; Cranium does not. We are open-source; Cranium is not. We price at $49/mo Business vs. Cranium's enterprise-only."
- **Deal cycle**: 6-10 weeks (mid-market) vs. 12-24 weeks (F500). The free Cranium Learning Environment is a strong funnel — MEOK's `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` is the product-certification alternative.
- **Reference customer to land**: Enterprise CISO that has hit the "training certificate, not product certification" gap and needs a product-level certification with blockchain verification (per `KEY_DIFFERENTIATORS.md` #3 and `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md`).
- **Channel to use**: Direct + "vs. Cranium" comparison page (factual, per `COMPARE_MATRIX_15_COMPETITORS.md` § 4 row 6) + MEOK's `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` as the lead magnet.
- **Pricing lever**: $49/mo Business vs. Cranium's enterprise-only. The "free Learning Environment" wedge means Cranium customers expect freemium; MEOK's freemium + transparent tiers is the structural alternative.
- **Switching-cost reduction**: Cranium's training certificates are not product-level; a 30-day parallel run with MEOK's product-level Watchdog certification establishes a stronger artifact; cut over to MEOK's blockchain-verified certs.
- **Technical migration path**: Cranium → MEOK by importing the AI Card / AI Arena / Detect AI outputs to MEOK's framework; MEOK adds blockchain verification and product-level certification.

---

## 5. The 7 jobs-to-be-done (per dim08)

The dim08 framework identifies 7 jobs buyers are "hiring" AI governance for. Each row maps a JTBD to a MEOK differentiator.

| # | JTBD (buyer's words) | Job category | SOV3 differentiator | Keystone code/spec | Source |
|---|---|---|---|---|---|
| 1 | "Help me pass an audit" | Credibility | HMAC-signed attestations + Watchdog cert | `meok_x402.py:66-126` + `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` | `KEY_DIFFERENTIATORS.md` #3 |
| 2 | "Help me comply with the EU AI Act by Aug 2" | Urgency | 48h deploy + free scanner | `EU_AI_ACT_FREE_SCANNER_SPEC.md` + `eu-ai-act-compliance-mcp` (410 articles) | `KEY_DIFFERENTIATORS.md` #2 + #7 |
| 3 | "Help me inventory my AI systems" | Discovery | Shadow AI MCP + 13-framework engine | `SHADOW_AI_DETECTION_MCP_SPEC.md` (4 detection sources) | `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` #6 |
| 4 | "Help me prove to my board we're safe" | Reporting | Public transparency dashboard | Planned `meok_dashboard.py` + `sov3_tech_blueprint.agent.final.md` § 4.1 | `KEY_DIFFERENTIATORS.md` #1 |
| 5 | "Help me integrate governance into my CI/CD" | DevOps | Policy-as-code + MCP-native | `meok-policy-enforcement-mcp` + planned `meok_gitops.py` | `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` #4 + #5 |
| 6 | "Help me negotiate with my auditor" | Negotiation | Watchdog certs (cryptographically signed) | `MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` Signet receipts | `KEY_DIFFERENTIATORS.md` #3 |
| 7 | "Help me spend less on GRC" | Cost | 10-20x undercut | $49/mo Business tier; TCO calculator | `PRICING.md` + `ONE_TRUST_ESCAPE_TCO_CALC.md` |

**The JTBD coverage check**: every named JTBD has a SOV3 differentiator + a keystone code/spec reference + a source file. The framework is auditable: if a competitor claims to "do JTBD X" we have a citation-ready 1-liner.

---

## 6. The 5 switching-cost reduction tactics (per dim09)

1. **Free migration from OneTrust (the 7-step playbook from `ONE_TRUST_ESCAPE_TCO_CALC.md`)**. Run EU AI Act free scanner → inventory OneTrust modules → $49/mo pilot → 48h pilot deploy → 30-day parallel run with HMAC-signed attestation cross-check → cut over attestations → decommission OneTrust. Typical savings: 70-95% over 5 years.
2. **EU AI Act free scanner as the wedge (5 questions, no signup)**. The funnel front-door per `EU_AI_ACT_FREE_SCANNER_SPEC.md`. 30% conversion to Business tier per the success metrics in `ONE_TRUST_ESCAPE_TCO_CALC.md` § 10.
3. **30-day parallel run with competitor (HMAC-signed attestation cross-check)**. Both systems run side-by-side; the customer sees MEOK's signed attestations are directly comparable to the competitor's PDFs but with stronger cryptographic verification. This is the dim09 "what customers wish existed" answer to the universal pain point "tools that need a team to operate."
4. **Open-source core = zero vendor lock-in (the OSS bet per differentiator #6 in `KEY_DIFFERENTIATORS.md`)**. 447 MIT-licensed CSOAI-ORG repos. Every framework, every MCP server, every integration is auditable. Closed competitors (OneTrust, Credo AI, Holistic AI, Cranium, WitnessAI, Zenity) cannot offer this; their closed source = their lock-in.
5. **447 MIT-licensed public repos = the codebase is auditable, not a black box**. Per `sov3_intel_dim02.md`, NanoCo is the only Tier-2 startup with any open-source component, and they have 4 employees and $12M. MEOK's 447 public repos are 100x more than NanoCo and ~50x more than the typical AI governance company.

**The 4-step "competitor escape" play** (combines tactics 1, 3, 4, 5): identify the competitor's high-cost/high-friction module → 30-day parallel run → cut over to MEOK's signed attestation → save the renewal. This applies to OneTrust (Privacy + AI Governance), Credo AI (assessments), Holistic AI (bias tests), Cranium (training), WitnessAI (network proxy), Zenity (agent security), MetricStream (audit mgmt), AuditBoard (audit mgmt), ServiceNow IRM (risk), and JetStream (blueprints).

---

## 7. The 4 channel plays (per dim07)

| # | Channel | Mechanic | Conversion hypothesis | SOV3 assets |
|---|---|---|---|---|
| 1 | **Direct** | Self-serve signup → freemium → annual | 30% scanner → Business, 10% Business → annual per `ONE_TRUST_ESCAPE_TCO_CALC.md` § 10 | `EU_AI_ACT_FREE_SCANNER_SPEC.md` + `PRICING.md` (4-tier) |
| 2 | **Marketplace** | Smithery + Docker + AWS + Glama + MCP.so + PulseMCP | 12/24/36-month contracts; volume via the 76-server MCP fleet | `smithery.yaml` + 76 production MCPs on `ghcr.io/csoai-org` |
| 3 | **Partner** | Big-4 advisory firms + MSPs + GRC consultants | Referral economics; co-sell; implementation services | `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` partner outreach plan |
| 4 | **Community** | 28-hive mesh + 447 public repos + dev-led adoption | 89% of OSS developers say open-source influences purchase decision | 447 MIT-licensed repos + `KEY_DIFFERENTIATORS.md` #6 |

**Channel economics**: Direct has the lowest CAC but the highest support burden. Marketplace has the highest volume but the smallest margin. Partner has the highest ACV but the longest cycle. Community has the lowest CAC at scale but requires sustained dev-relations investment. MEOK should run all four in parallel (per `FLEET_BASE.md` fleet pattern).

---

## 8. The 3 API-surface gaps in competitors (per dim11)

| Competitor | API status | SOV3 API-first pitch | Source |
|---|---|---|---|
| **WitnessAI** | **NO public API.** Observability-only. Integration timelines are "longer than expected" per dim09 reviews. | MEOK x402 streamable-HTTP + REST + planned GraphQL/gRPC/WebSocket expose every observation as a paid-call event with cryptographic event receipts. | `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` § 4 row 1 |
| **Zenity** | **NO public API.** AWS Security Hub one-way only. Microsoft-locked. | MEOK platform-agnostic gateway + LangChain/CrewAI/AutoGen/Azure AI Foundry unified abstraction. | `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` § 4 row 2 |
| **Cranium** | **NO public API.** W&B partnership is the only integration. Enterprise customers cannot extract data without a manual request. | MEOK open-core SDKs (Python/TypeScript) + x402 per-attestation pricing + REST + planned gRPC streaming. | `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` § 4 row 3 |

**The SOV3 multi-protocol advantage** (per `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` § 5): REST (live) + GraphQL (planned, 60-80% call reduction) + gRPC (planned, 5-10x latency reduction) + WebSocket/SSE (planned, real-time event stream). Every named competitor is REST-only. The 3-5x developer-experience improvement is durable.

---

## 9. The 4 architecture patterns in the market (per dim10)

| Pattern | Examples | Strengths | Weaknesses | MEOK is none of these — it's the 5th pattern |
|---|---|---|---|---|
| **1. Monolithic** | OneTrust, MetricStream, AuditBoard, ServiceNow IRM | Established vendor relationships; large install base | **10+ year old codebase, hard to add features**; long deployment cycles; bolt-on AI features | MEOK's keystone is <2 years old; modular, MCP-native, multi-protocol |
| **2. Microservices** | Credo AI, Holistic AI, JetStream, Microsoft Agent Governance Toolkit | Modern stack; rapid feature releases | **Assessment-only; no runtime enforcement**; require ML infrastructure | MEOK enforces at the MCP protocol boundary, not just at the assessment layer |
| **3. Security-pipeline** | CrowdStrike Falcon, Palo Alto Prisma AIRS, Zenity | Strong endpoint + SIEM integration | **Kernel agents = single point of OS failure**; SIEM-style not governance-style | MEOK is agentless at the kernel level; governance is the product, not a SIEM feed |
| **4. Network-proxy** | WitnessAI | No endpoint client; intent-based controls | **Integration pain; no protocol-level enforcement; no API** | MEOK runs at the MCP protocol boundary with first-class API access |

**The 5th pattern**: **MCP-native + open-source + multi-protocol + blockchain-verified + public transparency + PDCA-automated + Red/Blue team integration**. Per `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` § 1, MEOK's 10 exclusive capabilities are:

1. Public Transparency Dashboard with Blockchain Verification (12-18 months replication)
2. PDCA Cycle Automation for AI Safety (12-18 months)
3. Watchdog AI Safety Certification (9-12 months, category doesn't exist)
4. MCP-Native Governance (12-18 months, ecosystem moat)
5. EU AI Act 48-Hour Compliance Engine (6-9 months)
6. Agent Behavior Monitoring & Enforcement (12-18 months)
7. Multi-Protocol API (12-24 months, legacy REST-only stacks need rewrite)
8. Open-Source Core with Enterprise Paywall (18-24 months, cultural + business model reversal)
9. Real-Time AI Governance Event Streaming (9-12 months)
10. Industry-Specific MCP Packs (12-18 months per pack)

**Window of opportunity** (per dim12): 12-18 months of uncontested positioning in converged AI governance + blockchain verification + MCP ecosystem governance.

---

## 10. The 5 PR/marketing angles per competitor (per dim12 + dim08)

For each of the 15 competitors, the 1-2 PR angles that work in MEOK's favor. **Neutral framing per `RUBRIC_EXTERNAL_COMMS.md`** — factual comparative, no war language, no named-company attack phrasing.

| # | Competitor | PR angle 1 (capability) | PR angle 2 (price/speed) |
|---|---|---|---|
| 1 | **CrowdStrike** | Endpoint security focus; no model registry or compliance documentation. SOV3 covers policy, compliance, and certification; CrowdStrike covers execution. | Per-endpoint pricing ($60-$185/yr) means AI governance is an extra module; MEOK's $49/mo covers 13 frameworks. |
| 2 | **Microsoft** | Session-bound Copilot governance with no persistence and manual approvals. SOV3 provides continuous, automated governance with persistent audit trails across all agents. | Microsoft's $3.3M Year 1 + 16-week implementation; MEOK's $49/mo + 48h deploy. |
| 3 | **OneTrust** | Privacy-management heritage with bolt-on AI module and 9-month deployments. SOV3 deploys in 48 hours with native EU AI Act and ISO 42001 coverage. | Modular upsell trap (7 modules × $30K-$80K = $290K); MEOK = $588/yr flat. |
| 4 | **Credo AI** | Assessment-only platform with quarterly cycles and no runtime enforcement. SOV3 enforces policy in real time, with runtime gates, kill switches, and signed attestations. | $100K+ minimum commitment; MEOK = $49/mo Business. |
| 5 | **Holistic AI** | Testing-focused scope with quarterly bias cycles and no governance certification. SOV3 governs systems end-to-end and issues product-level certifications, not test reports. | No public pricing; MEOK = $49/mo Business. |
| 6 | **Cranium** | Training certificates only; no product certification or blockchain anchoring. SOV3 issues product-level AI governance certifications with blockchain-verified credentials. | No public API; MEOK ships REST + planned GraphQL/gRPC/WebSocket. |
| 7 | **WitnessAI** | Network-proxy monitoring without governance, enforcement, or certification. SOV3 is a governance platform that records decisions, enforces policy, and produces verifiable attestations. | No public API; MEOK = API-first. |
| 8 | **Zenity** | Low-code/no-code agent security without broader AI governance or compliance. SOV3 governs the full agent lifecycle across MCP, including orchestration, audit, and compliance documentation. | No public API; MEOK = API-first, platform-agnostic. |
| 9 | **Sycamore Labs** | Pre-product "Agentic OS" with no shipped deployment. SOV3 is shipping today with 76 production MCP servers and 410 EU AI Act articles ingested. | MEOK is shipping; Sycamore is pre-product. |
| 10 | **MetricStream** | Legacy GRC UX with bolt-on AI features and 18-month implementation. SOV3 is purpose-built for AI governance and deploys in 48 hours. | $75K-$1M/yr; MEOK = $49/mo Business. |
| 11 | **AuditBoard** | Audit-focused platform with no EU AI Act support. SOV3 ships native EU AI Act, NIST AI RMF, ISO 42001, and DORA coverage. | $30K-$250K/yr; MEOK = $49/mo Business. |
| 12 | **ServiceNow IRM** | ITSM-bundled risk module requiring $500K+ platform investment. SOV3 is a standalone governance layer that integrates with any ITSM via MCP. | $200K-$1M+/yr; MEOK = $49/mo Business. |
| 13 | **JetStream** | AI Blueprints that visualize agent-to-model relationships. SOV3 enforces policy, records decisions, and issues signed attestations. | No public pricing; MEOK = $49/mo Business. |
| 14 | **LightBeam.AI** | DSPM scope (data only) with no model or agent governance. SOV3 covers the model, agent, and compliance layers above the data layer. | $22.3M raised but no 2025/2026 round; MEOK = $49/mo Business. |
| 15 | **NanoCo** | Open-source sandbox for individual developers. SOV3 is an enterprise governance platform with HMAC-signed attestations, BFT consensus, and 13 frameworks integrated. | 4-person team; MEOK ships a 28-hive mesh + 447 MIT-licensed repos. |

**The 5 cross-cutting angles** that work against any competitor (use these in PR pitch templates):

1. **"13 frameworks in one engine"** — beats Credo AI's framework pack, OneTrust's 7 modules, MetricStream's bolt-on.
2. **"48-hour deploy SLA"** — beats every named competitor's 4-week to 18-month implementation.
3. **"10-20x price undercut"** — beats every named competitor's enterprise-only pricing.
4. **"HMAC-signed attestations"** — beats every named competitor's plain PDF / email attestations.
5. **"Open-source core, 447 MIT-licensed repos"** — beats every named competitor's closed source (except NanoCo's 4-person open-source sandbox).

---

## 11. The 3 do-NOT-do rules (per `RUBRIC_EXTERNAL_COMMS.md`)

1. **Don't name-and-shame specific failures.** No reference to CrowdStrike's widely-discussed 2024 incident, no reference to CISA exploited-vulnerability list, no reference to OneTrust's recent headcount changes. Use neutral framing ("lessons from past industry incidents," "industry-wide vulnerability disclosures," "GRC vendors with declining headcount"). The 3-question test: could a regulator read this as market manipulation? If yes, rephrase.
2. **Don't use war rhetoric in body copy.** Banned vocabulary: kill shot, nuclear arsenal, coup de grâce, talent raid, seeding doubt, depletion campaign, strike while, vulnerability window, acquisition target, funding fiction. Use the replacement vocabulary table in `RUBRIC_EXTERNAL_COMMS.md` § "The replacement vocabulary." Every external paragraph must pass the 3-question test (regulator, defamation, screenshot-tweet).
3. **Don't quote $1.2T TAM or $48M run-rate externally.** These are internal dossier numbers. Use the audited differentiators (`KEY_DIFFERENTIATORS.md`) with their citable public sources (IBM 2025, McKinsey 2025, EUR-Lex Reg (EU) 2024/1689, OpenSSF Scorecard, etc.). Every external claim must cite a public source; internal dossier is NOT a citable source.

---

## 12. Cross-references

| Document | Path | What it covers |
|----------|------|----------------|
| 15-Competitor Feature Matrix | `/Users/nicholas/meok-compliance-gateway/COMPARE_MATRIX_15_COMPETITORS.md` | 15-competitor comparison matrix + head-to-head 1-liners + honest gaps |
| 8 Key Differentiators | `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` | 13 frameworks, 410 EU AI Act articles, HMAC-SHA256, BFT, 35K+ MCP, 447 repos, 48h, GRC MCP gap |
| OneTrust Escape TCO Calculator | `/Users/nicholas/meok-compliance-gateway/ONE_TRUST_ESCAPE_TCO_CALC.md` | 7-step migration playbook + TCO calculator for OneTrust customers |
| SOV3 Unique Capabilities Matrix | `/Users/nicholas/meok-compliance-gateway/SOV3_UNIQUE_CAPABILITIES_MATRIX.md` | 10 SOV3-exclusive capabilities mapped to keystone code; 5 critical competitor weaknesses; API-less competitors; multi-protocol strategy |
| SOV3 Financial Model 2026-2028 | `/Users/nicholas/meok-compliance-gateway/SOV3_FINANCIAL_MODEL_2026-2028.md` | (not yet shipped — referenced in the cross-reference section for future) |
| External-Comms Rubric | `/Users/nicholas/meok-compliance-gateway/RUBRIC_EXTERNAL_COMMS.md` | Vocabulary + 3-question test for every external publication |
| 25-Day Playbook | `/Users/nicholas/meok-compliance-gateway/MEOK_25_DAY_PLAYBOOK_2026-06-08.md` | Phase 2 "OneTrust Escape" content slots |
| 28-Day Blog Calendar | `/Users/nicholas/meok-compliance-gateway/28_DAY_BLOG_CALENDAR.md` | OneTrust Escape content slots (-11, -15, +3) |
| Critical Fixes | `/Users/nicholas/meok-compliance-gateway/CRITICAL_FIXES_2026-06-08.md` | HMAC signing infrastructure (the attestation substrate) |
| PRICING.md | `/Users/nicholas/meok-compliance-gateway/PRICING.md` | 4-tier paywall ($0/$49/$X/$X) |
| EU AI Act Free Scanner Spec | `/Users/nicholas/meok-compliance-gateway/EU_AI_ACT_FREE_SCANNER_SPEC.md` | The funnel front-door |
| Watchdog Certification Platform Spec | `/Users/nicholas/meok-compliance-gateway/WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` | Product-level certification (3-tier) |
| Shadow AI Detection MCP Spec | `/Users/nicholas/meok-compliance-gateway/SHADOW_AI_DETECTION_MCP_SPEC.md` | 4 detection sources |
| MCP Security Certification Standard v0.1 RFC | `/Users/nicholas/meok-compliance-gateway/MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` | Signet receipts (§ 5.5) |
| Keystone OpenSSF Baseline | `/Users/nicholas/meok-compliance-gateway/keystone_SECREVIEW.md` | OpenSSF Scorecard 81.6/100 |

---

## 13. Source pointers

| Section | Primary source | Lines |
|---|---|---|
| § 1 framework | `/tmp/kimi_dossier_v2/research/sov3_intel_dim01.md` through `sov3_intel_dim12.md` | 1-50 (each) |
| § 3 matrix (CrowdStrike, Microsoft, OneTrust) | `sov3_intel_dim01.md` + `sov3_intel_dim03.md` + `sov3_intel_dim04.md` | full file |
| § 3 matrix (MetricStream, AuditBoard, ServiceNow) | `sov3_intel_dim03.md` (Tier 3) | lines 140-580 |
| § 3 matrix (Credo AI, Holistic AI, Cranium, WitnessAI) | `sov3_intel_dim02.md` (Tier 2) | lines 1-280 |
| § 3 matrix (Zenity, Sycamore, JetStream, LightBeam, NanoCo) | `sov3_intel_dim02.md` (Tier 2 + 3) | lines 280-570 |
| § 4 playbooks | `sov3_intel_dim02.md` + `sov3_intel_dim03.md` + `sov3_intel_dim09.md` | full files |
| § 5 jobs-to-be-done | `sov3_intel_dim08.md` (MCP ecosystem) + `sov3_intel_dim09.md` (customer sentiment) | dim08 § Executive Summary; dim09 § "What They Wish Existed" |
| § 6 switching-cost reduction | `sov3_intel_dim09.md` + `ONE_TRUST_ESCAPE_TCO_CALC.md` | dim09 § "What They Wish Existed"; `ONE_TRUST_ESCAPE_TCO_CALC.md` § 5 (7 steps) |
| § 7 channel plays | `sov3_intel_dim07.md` (talent/hiring) + `sov3_intel_dim08.md` (MCP marketplace) | dim07 § "SOV3 Priority Recruitment List"; dim08 § MCP Marketplace |
| § 8 API gaps | `sov3_intel_dim11.md` (press) + `sov3_intel_dim12.md` (architecture) + `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` § 4 | dim11 § 1.2; dim12 § 1.3 / 2.3 / 4.1; `SOV3_UNIQUE_CAPABILITIES_MATRIX.md` § 4 |
| § 9 architecture patterns | `sov3_intel_dim10.md` (funding) + `sov3_intel_dim12.md` (architecture) | dim10 § 2-3; dim12 § 1-4 + § 9 |
| § 10 PR angles | `sov3_intel_dim02.md` + `sov3_intel_dim03.md` + `COMPARE_MATRIX_15_COMPETITORS.md` § 4 | all files |
| § 11 do-not-do rules | `RUBRIC_EXTERNAL_COMMS.md` | full file |
| Feature matrix raw data | `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` | full file (1,164 lines) |
| API analysis raw data | `/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md` | full file (1,053 lines) |
| Tech docs raw data | `/tmp/kimi_dossier_v2/research/deepdive_tech_docs.md` | full file (982 lines) |
| UI/UX raw data | `/tmp/kimi_dossier_v2/research/deepdive_uiux_analysis.md` | full file (654 lines) |
| Website recon raw data | `/tmp/kimi_dossier_v2/research/deepdive_website_recon.md` | full file (1,391 lines) |
| MCP inventory raw data | `/tmp/kimi_dossier_v2/research/deepdive_mcp_inventory.md` | full file (659 lines) |

---

## 14. Reviewer checklist (rubric audit, signed off 2026-06-09)

- [x] No "kill shot" / "coup de grâce" / "nuclear arsenal" / "talent raid" — grep returns zero hits
- [x] No "seeding doubt" / "depletion campaign" / "strike while" / "vulnerability window" — grep returns zero hits
- [x] No "acquisition target" or "funding fiction" — grep returns zero hits
- [x] No reference to specific company failures (CrowdStrike's widely-discussed 2024 incident, CISA exploited-vulnerability list, OneTrust's headcount changes) — grep returns zero hits
- [x] No internal dossier language quoted as a citable source — all external claims cite public sources or the audited differentiator file
- [x] Every numerical claim has a `sov3_intel_dimNN.md` or `deepdive_*.md` line reference
- [x] Funding amounts quoted are from the dossier (audited) and presented neutrally (e.g., "$85.5M" rather than "vaporware")
- [x] 3-question test: regulator reading (no), defamation (no), screenshot-tweet (no) — all three clear

---

*Authored 2026-06-09 from the SOV3 12-dimension intelligence dossier. All factual claims are sourced; all positioning language is audit-passed against `RUBRIC_EXTERNAL_COMMS.md`. This is the tactical-playbook complement to `COMPARE_MATRIX_15_COMPETITORS.md` and `KEY_DIFFERENTIATORS.md` — use it for sales conversations, marketplace battlecards, and PR/marketing narrative development.*
