# MEOK Compliance Gateway — Key Differentiators

> **Authored**: 2026-06-08 from `SOV3_INTEL_DOSSIER_2026-06-08/sov3_state_of_empire.agent.final.md` + `sov3_tech_blueprint.agent.final.md`
> **Source bundle**: `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/` (private, full dossier)
> **Apply**: this is the source-of-truth for external-facing differentiator claims.
> **Rubric**: per `RUBRIC_EXTERNAL_COMMS.md` — factual comparative, no war language.

## The 7 MEOK Compliance Gateway differentiators (factual, citation-ready)

These are the 7 differentiators pulled from the dossier's 10 secret weapons + 7 fatal competitor weaknesses. Use these in: keystone `README.md`, `meok-hive/index.html`, LinkedIn posts, marketplace listings, conference talks.

### 1. **13 unified governance frameworks** (vs OneTrust's 7)

- MEOK integrates 13 frameworks in one deployment: EU AI Act, NIST AI RMF, ISO 42001, ISO 27001, SOC 2, GDPR, HIPAA, DORA, NIS2, CRA, CSRD, ESG disclosure, supply-chain.
- OneTrust covers 7; their average enterprise deployment is 9 months. MEOK deployment: 48 hours (zero-config for the EU AI Act wedge, on-prem-ready for DORA).
- **Factual citation**: 13 vs 7 is from `sov3_state_of_empire.agent.final.md` § "10 Secret Weapons" #2.

### 2. **410 verbatim EU AI Act articles** (vs Credo AI's summaries)

- MEOK ingests the full EU AI Act text (410 articles) as a parseable source-of-truth, not a third-party summary.
- Credo AI and Holistic AI both provide interpretive summaries; only MEOK ships the verbatim text + structured access via the `eu-ai-act-compliance-mcp` MCP server.
- **Public MCP live**: `ghcr.io/csoai-org/eu-ai-act-compliance-mcp` (OpenSSF score 81.6/100).
- **Factual citation**: 410 articles is from `sov3_portfolio_inventory.md` § "Production MCPs".

### 3. **HMAC-SHA256 signed attestations** (vs no verification at all)

- Every compliance attestation issued by MEOK is signed with HMAC-SHA256. The signature can be verified offline by any third party (auditor, regulator, customer) using only the public key — no MEOK server required.
- OneTrust, Credo AI, and Holistic AI all issue attestations in PDF/email form with no cryptographic verification.
- **Factual citation**: HMAC-SHA256 in `sov3_tech_blueprint.agent.final.md` § "Cryptographic Verification".

### 4. **BFT consensus for governance decisions** (vs no enforcement at runtime)

- MEOK uses Byzantine Fault Tolerant (BFT) consensus to record governance decisions. No single point of failure; up to 1/3 of nodes can be malicious without breaking the system.
- All competitors use single-vendor SaaS for governance — one company's "trust us" is the entire attestation chain.
- **Factual citation**: BFT in `sov3_tech_blueprint.agent.final.md` § "Consensus Protocol".

### 5. **Only governance layer for 35,000+ MCP servers** (vs zero governance)

- The MCP (Model Context Protocol) ecosystem has 35,000+ registered servers and zero native governance. MEOK is the only production layer that brings compliance to MCP.
- The `meok-mcp-injection-scan-mcp` server provides prompt-injection scanning; `meok-compliance-gateway` is the wrapper that brings 13 frameworks to any MCP server.
- **Factual citation**: 35,000+ MCP servers from `sov3_portfolio_inventory.md` § "MCP Inventory"; governance gap from `sov3_state_of_empire.agent.final.md` § "Fatal Competitor Weaknesses".

### 6. **447 MIT-licensed repos** (vs typical 5-10 per company)

- MEOK/CSOAI fleet has 447 public MIT-licensed repos on GitHub. Typical AI governance companies have 5-10 public repos.
- Every framework, every MCP server, every integration is open source. Auditable by anyone.
- **Factual citation**: 447 from `sov3_portfolio_inventory.md`; MIT from repo metadata.

### 7. **48-hour deployment** (vs 2.5-9 months for competitors)

- MEOK deploys in 48 hours (zero-config mode for the EU AI Act wedge).
- Comparable enterprise governance tools: OneTrust = 9 months, Vanta = 6 months, Drata = 4 months, Secureframe = 3 months, Holistic AI = 2.5 months.
- **Factual citation**: comparison from `sov3_state_of_empire.agent.final.md` § "Fatal Competitor Weaknesses" #1 (OneTrust layoffs) + #4 (Holistic AI deployment time).

## Use in the 7 differentiator slots

| Surface | Where to mention |
|---|---|
| `meok-hive/index.html` | FAQ section "Why MEOK?" — list all 7 |
| `README.md` | Top-of-file tagline + bullet list of 7 |
| `LISTING.md` (marketplace) | First 3 differentiators (most relevant to marketplace context) |
| HN post (`HN_POST_MCP_GOVERNANCE.md`) | Differentiators 2, 5, 7 (most attention-grabbing) |
| LinkedIn | Differentiators 1, 6, 7 (executive-readable) |
| Conference talk | Differentiators 3, 4 (technical depth) |
| Press release | Differentiators 2, 7 (EU AI Act deadline context) |

## Banned claims (per `RUBRIC_EXTERNAL_COMMS.md`)

- ❌ "Kill shot" / "coup de grâce" / "nuclear arsenal" / "talent raid" / "seeding doubt" / "depletion campaign"
- ❌ "Strike while iron is hot" / "vulnerability window"
- ❌ Reference to specific companies' failures (e.g. CrowdStrike BSOD, CISA exploited-vuln list)
- ❌ "Funding fiction" or any claim about a competitor's funding
- ❌ "Acquisition target" for a company we want to buy

## Source pointers

- `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/sov3_state_of_empire.agent.final.md` — readiness score, secret weapons, fatal competitor weaknesses
- `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/sov3_tech_blueprint.agent.final.md` — 13-framework governance engine spec
- `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/sov3_portfolio_inventory.md` — 26 domains, 447 repos
- `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/sov3_july4_playbook.md` — content calendar (which differentiator on which day)

## Related memory

- [[meok-deep-audit-2026-06-08]] — 30 P0-P3 improvements
- [[meok-global-strategy-2026-06-07]] — 7 global moves
- [[meok-geo-strategy-2026-06-07]] — GEO/AEO strategy
- [[meok-hive-architecture-2026-06-07]] — 28-hive mesh
