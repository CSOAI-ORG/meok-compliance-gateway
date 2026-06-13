# 7 Industry Packs — Briefs (Q1 2027 EXPAND phase)

> **Source**: `sov3_mcp_master_audit.docx` § "Industry Pack Bundles" (8 Jun 2026)
> **Quarter**: Q1 2027 (per master audit 18-month roadmap: EXPAND phase)
> **Total MCPs in packs**: 62 (post-merge, across 7 packs)
> **Combined ARR target**: $170K-$1.38M per pack
> **Cross-cutting**: `agent-mcp-router` (FREE, "Governance OS Kernel") fronts all 7 packs

## Pack coverage map

| Pack | MCPs | Primary Buyer | Secondary Buyer | ARR Range |
|---|---:|---|---|---|
| `finserv-pack` | 11 | CRO / CCO | CISO | $50K-$500K |
| `healthcare-pack` | 8 | CMIO | Compliance | $30K-$200K |
| `mfg-logistics-pack` | 8 | Operations Director | Compliance | $20K-$100K |
| `ai-gov-essentials-pack` | 11 | Chief AI Officer / Legal | CISO | $15K-$150K |
| `agent-infra-pack` | 12 | VP Eng / CTO | Platform Eng | $40K-$300K |
| `trust-pack` | 5 | CISO | Compliance | $10K-$80K |
| `dev-productivity-pack` | 7 | VP Eng | DevOps Lead | $5K-$50K |

## Pack 1: Financial Services Compliance Pack (`finserv-pack`)

**MCPs (11 post-merge)**: `dora-complete`, `nis2-complete`, `cra-complete`, `basel-ai-overlay`, `aml-ai`, `gdpr`, `iso-27001`, `risk-assessment`, `soc2`, `meok-dpia-edpb`, `regulatory-crosswalk-engine`

**Target users**: Banks, insurance companies, fintechs, payment processors, investment funds

**Value prop**: Complete regulatory coverage for EU financial institutions — DORA (operational resilience), NIS2 (cybersec), CRA (product safety), Basel (risk), AML (financial crime), GDPR (data), ISO 27001 + SOC2 (InfoSec), plus automated risk assessment and cross-regulatory mapping.

**Why this bundle**: Financial services face the densest regulatory overlap of any industry. A mid-size bank may be subject to DORA + NIS2 + CRA + GDPR + Basel + AML simultaneously. Currently they must install and integrate 11+ separate MCPs. This pack provides one integrated solution.

**Key integrations**: DORA-NIS2 crosswalk (built-in), AML-risk assessment pipeline, GDPR-DPIA automation, Basel-risk model overlay

**ARR target**: $50K-$500K (based on institution size and transaction volume)

**Sales motion**: Direct enterprise sales with proof-of-concept on one regulation, expansion to full pack

## Pack 2: Healthcare AI Governance Pack (`healthcare-pack`)

**MCPs (8 post-merge)**: `healthcare-ai-suite`, `hipaa`, `gdpr`, `iso-42001`, `eu-ai-act-complete`, `ai-bom`, `bias-detection`, `ai-self-audit`

**Target users**: Hospitals, medtech vendors, health AI startups, pharmaceutical companies, clinical research organizations

**Value prop**: End-to-end AI governance for healthcare — clinical data (FHIR), patient privacy (HIPAA/GDPR), AI quality management (ISO 42001), EU AI Act high-risk compliance, and AI transparency (BOM, bias detection, self-audit).

**Why this bundle**: Healthcare AI sits at the intersection of medical device regulation, data protection (HIPAA + GDPR), AI Act (high-risk classification), and quality management (ISO 42001). A medtech startup needs all of these to go to market.

**Key integrations**: FHIR-governance bridge, HIPAA-GDPR dual compliance mode, EU AI Act-ISO 42001 QMS alignment, bias detection-BOM transparency

**ARR target**: $30K-$200K

**Sales motion**: Medtech-focused sales, regulatory consultant partnerships, HIMSS/conference presence

## Pack 3: Manufacturing & Logistics Pack (`mfg-logistics-pack`)

**MCPs (8 post-merge)**: `transport-compliance-suite`, `drone-airspace-suite`, `crane-hire-cpcs`, `agriculture-robotics`, `cra-complete`, `iso-27001`, `ai-bom`, `sbom-cyclonedx`

**Target users**: Logistics companies, construction firms, drone operators, agtech companies, manufacturers

**Value prop**: Regulatory coverage for industrial operations — transport compliance, drone airspace, construction safety (CPCS), agri-robotics, product safety (CRA), cybersecurity (ISO 27001), and full supply chain transparency (SBOM + AI BOM).

**Why this bundle**: Industrial AI faces a unique mix: sector-specific (transport hours, drone flight rules, crane certifications), product safety (CRA for connected devices), and cybersecurity (ISO 27001). The SBOM + AI-BOM combination is critical for supply chain transparency in manufacturing.

**Key integrations**: Transport-drone multi-modal logistics, CRA-SBOM product safety pipeline, agriculture-robotics field compliance

**ARR target**: $20K-$100K

**Sales motion**: Industry association partnerships (FTA for logistics, CAA for drones), trade show presence

## Pack 4: AI Governance Essentials Pack (`ai-gov-essentials-pack`)

**MCPs (11 post-merge)**: `eu-ai-act-complete`, `nist-rmf`, `iso-42001`, `iso-42005-impact`, `bias-detection`, `ai-bom`, `meok-governance-engine`, `ai-watermarking-suite`, `ai-self-audit`, `risk-assessment`, `llm-compliance-comparison`

**Target users**: **ANY** organization building or deploying AI — tech companies, enterprises, startups, government agencies

**Value prop**: Foundational AI governance covering the three major frameworks (EU AI Act, NIST RMF, ISO 42001), technical safeguards (watermarking, bias detection), and operational tools (BOM, audit, risk assessment, LLM comparison).

**Why this bundle**: This is the "must-have" pack for any AI-using organization. It bundles the three dominant AI governance frameworks with the technical controls needed to implement them. The `meok-governance-engine` orchestrates across all frameworks automatically.

**Key integrations**: Governance engine → all framework MCPs for unified orchestration; EU AI Act ↔ NIST RMF ↔ ISO 42001 crosswalk (automated); watermarking ↔ BOM for content provenance

**ARR target**: $15K-$150K

**Sales motion**: Self-serve trial (land) with enterprise expansion (expand). Freemium entry via `ai-self-audit`. **This is the Q3 LAUNCH wedge** — every other pack inherits its buyers from this one.

## Pack 5: Agent Infrastructure Pack (`agent-infra-pack`)

**MCPs (12 post-merge)**: `agent-mcp-router`, `agent-orchestrator-pro`, `agent-identity-trust`, `agent-policy-enforcement`, `agent-prompt-injection-firewall`, `agent-audit-logger`, `agent-rate-limiter`, `agent-data-residency`, `agent-replay-debugger`, `agent-finops-manager`, `a2a-governance-bridge`, `bft-progress-council`

**Target users**: Organizations building multi-agent systems — AI platforms, enterprise IT, agent framework vendors

**Value prop**: Complete infrastructure for governed, secure, observable agent systems — routing, orchestration, identity, security, audit, cost management, and cross-agent governance.

**Why this bundle**: Multi-agent deployments require infrastructure-layer governance: who can call what, how costs are tracked, how policies are enforced, how security is maintained. This pack is the "agent operating system."

**Key integrations**: Router → all agent MCPs for discovery; policy enforcement → identity for authorization; audit logger → all for observability; FinOps → rate limiter for cost control

**ARR target**: $40K-$300K

**Sales motion**: Platform partnerships (Anthropic, OpenAI, Google), enterprise architecture teams, agent framework vendors

## Pack 6: Trust & Verification Pack (`trust-pack`)

**MCPs (5 post-merge)**: `blockchain-trust-layer`, `meok-mcp-injection-scan`, `ai-self-audit`, `accessibility-ai`, `meok-attestation-verify`

**Target users**: Security teams, compliance officers, AI quality assurance, auditors

**Value prop**: Technical trust layer — security scanning, blockchain verification, attestation, self-audit, and accessibility compliance.

**Why this bundle**: Trust and verification are cross-cutting concerns. This pack bundles security (injection scanning), cryptographic verification (blockchain), quality (accessibility), and audit (self-audit, attestation) into a unified trust layer.

**Key integrations**: Blockchain trust ↔ AI-BOM for verifiable bills of materials; injection scan ↔ prompt firewall for defense in depth

**ARR target**: $10K-$80K

**Sales motion**: Security-focused sales, CISO engagement, compliance audit partnerships

## Pack 7: Developer Productivity Pack (`dev-productivity-pack`)

**MCPs (7)**: `api-devtools-suite`, `sql-builder-ai`, `meok-mcp-test`, `document-comparison`, `ai-gateway`, `backup-ai`, `compression-ai`

**Target users**: Software developers, DevOps engineers, AI engineers, platform teams

**Value prop**: Developer tools for building, testing, and operating AI-powered applications.

**Why this bundle**: Horizontal developer tools that don't fit compliance/governance packs but provide productivity value. Bundling creates a natural developer tooling tier at an accessible price point.

**Key integrations**: API devtools ↔ AI gateway; MCP test ↔ agent router for testing

**ARR target**: $5K-$50K

**Sales motion**: Self-serve, developer-led adoption, GitHub Marketplace, IDE plugin integrations

## Cross-pack architecture

```
                ┌─────────────────────────────┐
                │  agent-mcp-router (FREE)    │
                │  Governance OS Kernel        │
                └──────────────┬──────────────┘
                               │
       ┌───────────┬───────────┼───────────┬───────────┐
       │           │           │           │           │
   ┌───▼───┐  ┌────▼───┐  ┌────▼───┐  ┌────▼───┐  ┌────▼───┐
   │finserv│  │health- │  │  mfg-  │  │ai-gov- │  │agent-  │
   │ -pack │  │ care   │  │logistic│  │essent- │  │ infra  │
   │       │  │ -pack  │  │  -pack │  │ ials   │  │ -pack  │
   │  $$$  │  │        │  │        │  │ -pack  │  │        │
   └───┬───┘  └────┬───┘  └────┬───┘  └────┬───┘  └────┬───┘
       │           │           │           │           │
       │      ┌────▼────┐  ┌───▼────┐
       │      │ trust   │  │ dev-   │
       │      │ -pack   │  │prod-   │
       │      └─────────┘  │uctivity│
       │                   └────────┘
       │
   shared EU AI Act
   complete + governance
   engine (the keystone
   orchestration layer)
```

The **FREE** `agent-mcp-router` is the wedge — every install of the router becomes a future pack buyer.

## Phasing (per the 18-month roadmap)

| Pack | Q3 2026 LAUNCH | Q4 2026 SCALE | Q1 2027 EXPAND | Q2 2027 DOMINATE |
|---|:---:|:---:|:---:|:---:|
| `ai-gov-essentials` | ✅ MVP | Full | ✅ | ✅ |
| `finserv` | Pilot (1 bank) | General | ✅ | ✅ |
| `healthcare` | Pilot (1 medtech) | General | ✅ | ✅ |
| `agent-infra` | MVP (router only) | + 4 MCPs | ✅ | ✅ |
| `mfg-logistics` | — | MVP | ✅ | ✅ |
| `trust` | MVP | Full | ✅ | ✅ |
| `dev-productivity` | MVP | Full | ✅ | ✅ |

## Cross-references

- `sov3-mcp-master-audit-2026-06-08.md` (memory) — the audit that defines these 7 packs
- `MERGE_PLAN_2026_Q4.md` — the 15-merge refactor that produces the post-merge MCP names
- `KIMI_COMPETITOR_VISUAL_AUDIT_BRIEF_v2.md` — the 13/15 GRC competitors with zero MCP context
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — the 25-day strike that launches `ai-gov-essentials` first
- [[sov3-mcp-master-audit-2026-06-08]]
