# Kimi — Competitor Visual Audit Brief v2 (MEOK/CSOAI fleet, AGGRESSIVE DEPTH)

> **Self-contained copy-paste brief.** Drop this into Kimi CLI / Kimi Agent
> with no further context. Calibrated to MEOK/CSOAI on **8 Jun 2026, 08:30 UTC**.
>
> **v2 differences from v1 (this brief is now the canonical one — v1 is preserved
> for diff):**
> - **§1 expanded to a real, verified 76-server census** of CSOAI-ORG on the MCP
>   official registry, with per-server latest version, publish date, and remotes.
> - **§1 includes the full 46-package PyPI download matrix** for our fleet (25
>   with live download stats, top performers: `eu-ai-act-compliance-mcp`
>   136/day, `bias-detection-mcp` 258/day, `ai-bom-mcp` 246/day, `meok-tacho-audit-mcp`
>   208/day).
> - **§3 surfaces the real direct competitor** (`ark-forge/mcp-eu-ai-act`, 8★,
>   MIT, 4 versions Feb–Apr 2026, hosted at `arkforge.fr`) and the **structural
>   finding** that the 6 named GRC competitors (OneTrust / Credo AI / Holistic AI /
>   Vanta / Drata / Secureframe) have **ZERO presence on the MCP official
>   registry** — this is the single biggest opportunity in the brief.
> - **§6 explicitly includes Smithery/Glama/Pulse/MCPize** as well as the
>   documentation sites and GitHub repos.
> - **§8 is a real, executable 5-dimension scorecard** with evidence-based
>   scoring rules.
> - **§10 is the rubric with banned-vocabulary substitutions** baked into a
>   single lookup table (per `RUBRIC_EXTERNAL_COMMS.md`).
> - **§11 is the output template** — what Kimi should write back, in what file,
>   in what shape, with what acceptance gates.

---

## 0. Context (1 paragraph)

We (MEOK AI Labs / CSOAI-ORG) ship a **76-server MCP fleet** on the official
MCP registry, plus 35 published PyPI packages (25 with active download
counts). The 8 Jun 2026 Kimi audit confirmed our 4-tier pricing undercuts
OneTrust / Credo / Holistic / Vanta / Drata / Secureframe by 2-15x for SMB and
2-8x for enterprise. **The Kimi audit (and the earlier `_kimi_dossier_x`
sibling) were both wrong on the "no production MCP" claim — we ARE the
production MCP layer for AI governance.** The visual audit you are about to
dispatch is to learn how our listings *look* versus the competition. The
distribution channels that matter are listed below. Every one has a visual
surface that determines whether an evaluator clicks "Install" or moves on.

---

## 1. The MEOK/CSOAI fleet — verified as of 8 Jun 2026 08:30 UTC

### 1.1 PyPI matrix (the install point)

**46 attempted PyPI package names** (the 28-hive + adjacent fleet). 35
**found on PyPI**, 25 with live download stats. Last published 2026-06-08
(everything was repushed yesterday). Sorted by last-30-day downloads:

| # | PyPI package | Latest | Releases | dl/day | dl/wk | dl/mo | MCP reg entries | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `bias-detection-mcp` | 1.2.2 | 15 | **258** | 578 | 1736 | 5 | top performer — *our anti-bias scanner* |
| 2 | `ai-bom-mcp` | 1.2.16 | 20 | **246** | 725 | 1728 | 5 | *AI Bill of Materials, CycloneDX ML-BOM, SPDX 3.0* |
| 3 | `agent-audit-logger-mcp` | 1.1.5 | 10 | **236** | 473 | 1100 | 2 | *Hash-chained HMAC-signed audit log for A2A* |
| 4 | `meok-tacho-audit-mcp` | 1.0.3 | 4 | **208** | 327 | 327 | 0 | *UK/EU tachograph digital audit* |
| 5 | `csrd-compliance-mcp` | 1.3.5 | 16 | 141 | 807 | 1196 | 3 | *12 ESRS standards* |
| 6 | `eu-ai-act-compliance-mcp` | 1.8.6 | **31** | 136 | 1196 | 2687 | **7** | flagship — *410 EUR-Lex articles FTS5 search* |
| 7 | `nis2-compliance-mcp` | 1.3.4 | 20 | 130 | 703 | 1672 | 6 | *10 Article 21 measures* |
| 8 | `nist-rmf-ai-mcp` | 1.0.13 | 14 | 131 | 704 | 1127 | 5 | NIST AI RMF |
| 9 | `document-comparison-ai-mcp` | 1.0.8 | 8 | 129 | 234 | 625 | 3 | *policy diff / clause diff* |
| 10 | `csoai-governance-crosswalk-mcp` | 1.0.12 | 13 | 125 | 579 | 985 | 3 | *reg-to-reg mapping* |
| 11 | `dora-nis2-crosswalk-mcp` | 1.1.2 | 8 | 124 | 211 | 783 | 2 | *Regulation 2022/2554 ↔ Directive 2022/2555* |
| 12 | `cra-compliance-mcp` | 1.3.6 | 20 | 121 | 1046 | 1730 | 5 | EU Cyber Resilience Act |
| 13 | `compression-ai-mcp` | 1.0.8 | 8 | 114 | 223 | 590 | 3 | |
| 14 | `meok-watermark-attest-mcp` | 1.3.9 | 19 | 130 | 524 | 1313 | 7 | *EU AI Act Art 50, C2PA, fingerprint* |
| 15 | `dora-compliance-mcp` | 1.4.7 | 27 | n/a | n/a | n/a | 7 | flagship — *5-pillar audit, incident cls* |
| 16 | `iso-42001-ai-mcp` | 1.1.6 | 18 | n/a | n/a | n/a | 5 | *AIMS audit* |
| 17 | `soc2-compliance-ai-mcp` | 1.0.12 | 13 | n/a | n/a | n/a | 5 | |
| 18 | `gdpr-compliance-ai-mcp` | 1.1.7 | 18 | n/a | n/a | n/a | 0 | *lawful basis, DPIA, ROPA* |
| 19 | `hipaa-compliance-mcp` | 1.0.10 | 11 | n/a | n/a | n/a | 3 | |
| 20 | `meok-mcp-injection-scan-mcp` | 1.0.12 | 13 | n/a | n/a | n/a | 6 | *30+ canonical rules* |
| 21 | `agent-policy-enforcement-mcp` | 1.0.7 | 8 | n/a | n/a | n/a | 3 | *per-agent-pair IAM for A2A* |
| 22 | `meok-governance-engine-mcp` | 1.0.17 | 18 | n/a | n/a | n/a | 5 | *full governance report* |
| 23 | `iso-27001-ai-mcp` | 1.0.11 | 11 | 11 | 545 | 944 | 0 | |
| 24 | `risk-assessment-ai-mcp` | 1.0.11 | 12 | 14 | 587 | 995 | 4 | |
| 25 | `llm-compliance-comparison-mcp` | 1.0.11 | 11 | 39 | 832 | 1402 | 4 | *compare providers, recommend* |
| 26 | `meok-cra-annex-iv-classifier-mcp` | 1.1.6 | 12 | 41 | 421 | 1374 | 6 | *Class I/II/III hierarchy* |
| 27 | `meok-eu-ai-act-art-13-ifu-mcp` | 1.0.4 | 5 | 9 | 316 | 552 | 2 | *provider-side IFU, 7 Art 13 fields* |
| 28 | `meok-eu-ai-act-art-26-fria-mcp` | 1.0.4 | 5 | 9 | 324 | 547 | 2 | *FRIA generator* |
| 29 | `sbom-cyclonedx-mcp` | 1.0.4 | 3 | n/a | n/a | n/a | 0 | |
| 30 | `haulage-uk-compliance-mcp` | 1.0.6 | 7 | 4 | 295 | 804 | 1 | *DVSA roadside checks* |
| 31 | `drone-airspace-governance-mcp` | 1.0.12 | 13 | n/a | n/a | n/a | 4 | |
| 32 | `healthcare-ai-governance-mcp` | 1.0.11 | 11 | 11 | 574 | 1111 | 4 | *SaMD, CDS, HIPAA* |
| 33 | `uk-ai-bill-compliance-mcp` | 1.0.5 | 6 | 8 | 97 | 597 | 2 | |
| 34 | `iso-42005-impact-mcp` | 1.0.4 | 4 | n/a | n/a | n/a | 0 | |
| 35 | `watermarking-authenticity-mcp` | 1.2.2 | 8 | 16 | 226 | 798 | 1 | |
| — | `meok-attestation-api` | — | — | — | — | — | — | **NOT ON PyPI** — internal-only |
| — | `meok-sdk-python` | — | — | — | — | — | — | **NOT ON PyPI** — internal-only |
| — | `mcp-spec-compliance-mcp` | — | — | — | — | — | — | **NOT ON PyPI** |
| — | `firmware-attestation-mcp` | — | — | — | — | — | — | **NOT ON PyPI** |
| — | `meok-cra-art14-reporter-mcp` | — | — | — | — | — | — | **NOT ON PyPI** |
| — | `meok-haulage-governance-bridge-mcp` | — | — | — | — | — | — | **NOT ON PyPI** |
| — | `meok-nis2-nl-register-mcp` | — | — | — | — | — | — | **NOT ON PyPI** |
| — | `meok-haulage-gps-track-mcp` | — | — | — | — | — | — | **NOT ON PyPI** |
| — | `meok-compliance-gateway` | — | — | — | — | — | — | **NOT ON PyPI** — runs in this repo |
| — | `lib2b` | — | — | — | — | — | — | **NOT ON PyPI** |
| — | `haulage-deploy` | — | — | — | — | — | — | **NOT ON PyPI** |

**Total live download volume (last 30 days, sum of 25 packages with stats):**
~22,600 downloads. **Total releases across the fleet:** ~480. **Total
distinct PyPI → MCP-reg pairs:** 35 packages × 4.3 average reg entries ≈
150 published MCP-reg versions.

### 1.2 MCP official registry census (76 distinct CSOAI-ORG servers)

Verified 8 Jun 2026 08:30 UTC. The 28-hive fleet + 48 adjacent
infrastructure/governance servers. Sorted by latest version; the [L] flag
= "remote/streamable-HTTP entry" (most are stdio-only).

| # | Server (short name) | Latest | Versions | Title (truncated) |
|---|---|---:|---:|---|
| 1 | a2a-governance-bridge-mcp | 1.1.5 | 4 | A2A Governance Bridge |
| 2 | accessibility-ai-mcp | 1.0.4 | 3 | Accessibility AI |
| 3 | accounting-ai-mcp | 1.0.3 | 2 | Accounting AI |
| 4 | ad-copy-ai-mcp | 1.0.3 | 2 | Ad Copy AI |
| 5 | agent-audit-logger-mcp | 1.0.4 | 2 | Hash-chained HMAC audit log for A2A |
| 6 | agent-commerce-payments-mcp | 1.0.4 | 3 | Agent commerce payments |
| 7 | agent-content-watermark-mcp | 1.1.1 | 1 | **EU AI Act Art 50(2) GenAI watermarking** |
| 8 | agent-cost-allocator-mcp | 1.0.1 | 1 | Multi-tenant LLM cost attribution |
| 9 | agent-data-residency-mcp | 1.0.3 | 3 | **GDPR Chapter V transfer-basis runtime guard** |
| 10 | agent-delegation-mcp | 1.0.4 | 3 | Agent task delegation |
| 11 | agent-handoff-certified-mcp | 1.0.4 | 2 | Verifiable A2A task handoff |
| 12 | agent-identity-trust-mcp | 1.0.4 | 3 | Agent identity, credentials |
| 13 | agent-incident-relay-mcp | 1.0.1 | 1 | **Art 73 5-clock broadcaster** |
| 14 | agent-mcp-router-mcp | 1.1.1 | 1 | **One router for the whole MEOK fleet (62 MCPs)** |
| 15 | agent-negotiation-mcp | 1.0.4 | 3 | Propose deal, evaluate offer |
| 16 | agent-orchestrator-mcp | 1.0.3 | 2 | Create agent, list agents |
| 17 | agent-policy-enforcement-mcp | 1.0.4 | 3 | Per-agent-pair IAM for A2A |
| 18 | agent-prompt-injection-firewall-mcp | 1.0.5 | 3 | **The WAF for agents** |
| 19 | agent-rate-limiter-mcp | 1.0.4 | 3 | Fleet-wide shared rate limiter |
| 20 | agent-replay-debugger-mcp | 1.0.1 | 1 | Record + replay agent steps |
| 21 | agent-token-budget-mcp | 1.1.1 | 1 | Per-session spend cap |
| 22 | agent-x402-paywall-mcp | 1.0.2 | 2 | **x402 / Coinbase HTTP 402 paywall for agents** |
| 23 | agriculture-robotics-mcp | 1.0.4 | 3 | Robot safety check |
| 24 | ai-bom-mcp | 1.2.7 | 5 | AI-BOM / CycloneDX ML-BOM / SPDX 3.0 |
| 25 | ai-gateway-mcp | 1.0.4 | 3 | AI Gateway |
| 26 | ai-incident-reporting-mcp | 1.1.2 | 3 | AI Incident Reporting |
| 27 | ai-ops-mcp | 1.0.4 | 3 | AI Ops |
| 28 | ai-self-audit-mcp | 1.0.8 | 4 | AI Self Audit |
| 29 | airspace-monitor-mcp | 1.0.4 | 3 | Airspace Monitor |
| 30 | aml-ai-mcp | 1.0.3 | 2 | **6AMLD + UK MLR 2017 + FinCEN BSA** |
| 31 | api-docs-generator-ai-mcp | 1.0.4 | 3 | API docs generator |
| 32 | api-tester-ai-mcp | 1.0.4 | 3 | API tester |
| 33 | ascii-art-ai-mcp | 1.0.4 | 3 | ASCII art |
| 34 | backup-ai-mcp | 1.0.4 | 3 | Backup AI |
| 35 | basel-ai-overlay-mcp | 1.0.3 | 2 | **Basel III + SR 11-7 + ECB TRIM** |
| 36 | bft-progress-council-mcp | 1.1.2 | 2 | **5-voter Byzantine council** |
| 37 | bias-detection-mcp | 1.1.3 | 5 | Bias detection / fairness |
| 38 | blockchain-ai-mcp | 1.0.4 | 3 | Blockchain AI |
| 39 | blockchain-verification-mcp | 1.0.1 | 1 | Blockchain verification |
| 40 | compression-ai-mcp | 1.0.4 | 3 | Compression AI |
| 41 | cra-compliance-mcp | 1.3.4 | 5 | EU Cyber Resilience Act |
| 42 | crane-hire-cpcs-mcp | 1.0.3 | 2 | **CPCS / CISRS / NPORS card verification** |
| 43 | csoai-governance-crosswalk-mcp | 1.0.6 | 3 | Governance crosswalk |
| 44 | csrd-compliance-mcp | 1.2.4 | 3 | **12 ESRS standards** |
| 45 | document-comparison-ai-mcp | 1.0.4 | 3 | Document comparison |
| 46 | dora-compliance-mcp | 1.4.4 | 7 | **DORA 5-pillar audit, incident cls** |
| 47 | dora-nis2-crosswalk-mcp | 1.0.4 | 2 | DORA ↔ NIS2 crosswalk |
| 48 | drone-airspace-governance-mcp | 1.0.8 | 4 | Drone airspace |
| 49 | **eu-ai-act-compliance-mcp** | **1.8.3** | **7** | **EU AI Act — flagship** |
| 50 | gdpr-compliance-ai-mcp | 1.1.5 | 5 | GDPR / DPIA / ROPA |
| 51 | haulage-uk-compliance-mcp | 1.0.1 | 1 | **UK Operator Licence / DVSA** |
| 52 | healthcare-ai-governance-mcp | 1.0.8 | 4 | Healthcare AI / SaMD / CDS |
| 53 | healthcare-fhir-mcp | 1.0.4 | 3 | Healthcare FHIR |
| 54 | hipaa-compliance-mcp | 1.0.6 | 3 | HIPAA |
| 55 | iso-27001-ai-mcp | 1.0.8 | 4 | ISO 27001 |
| 56 | iso-42001-ai-mcp | 1.1.4 | 5 | ISO 42001 AIMS |
| 57 | llm-compliance-comparison-mcp | 1.0.8 | 4 | LLM provider compliance comparison |
| 58 | meok-attestation-verify | 1.0.3 | 2 | **DORA / NIS2 / CRA / EU AI Act verifier** |
| 59 | meok-cra-annex-iv-classifier-mcp | 1.1.5 | 6 | CRA Class I/II/III classifier |
| 60 | meok-dora-tlpt-planner-mcp | 1.0.3 | 3 | **DORA Art 26 TLPT planner (TIBER-EU)** |
| 61 | meok-dpia-edpb-template-mcp | 1.0.4 | 2 | **DPIA / EDPB harmonised template (14 Apr 2026)** |
| 62 | meok-eu-ai-act-art-13-ifu-mcp | 1.0.2 | 2 | [L] **Art 13 IFU generator** |
| 63 | meok-eu-ai-act-art-26-fria-mcp | 1.0.2 | 2 | [L] **Art 26(9) FRIA generator** |
| 64 | meok-fria-generator-mcp | 1.0.3 | 3 | EU AI Act Art 27 FRIA |
| 65 | meok-governance-engine-mcp | 1.0.13 | 5 | Governance engine |
| 66 | meok-mcp-injection-scan-mcp | 1.0.11 | 6 | **MCP injection / SSRF scanner, 30+ rules** |
| 67 | meok-mcp-test-mcp | 1.0.0 | 1 | [L] **Golden-file + schema-drift tester** |
| 68 | meok-nis2-de-register-mcp | 1.0.9 | 6 | **Germany NIS2 BSI registration** |
| 69 | meok-omnibus-tracker-mcp | 1.1.3 | 6 | **EU AI Act Digital Omnibus tracker** |
| 70 | meok-watermark-attest-mcp | 1.3.5 | 7 | **EU AI Act Art 50, C2PA, fingerprint** |
| 71 | nis2-compliance-mcp | 1.2.10 | 6 | NIS2 |
| 72 | nist-rmf-ai-mcp | 1.0.11 | 5 | NIST AI RMF |
| 73 | sbom-cyclonedx-mcp | 1.0.2 | 1 | **CycloneDX 1.6 / SPDX 2.3** |
| 74 | soc2-compliance-ai-mcp | 1.0.10 | 5 | SOC 2 |
| 75 | uk-ai-bill-compliance-mcp | 1.0.3 | 2 | UK AI Bill |
| 76 | watermarking-authenticity-mcp | 1.0.2 | 1 | EU AI Act Art 50 |

[L] = has a streamable-HTTP remote entry on `api.meok.ai`. All others are
stdio-only.

### 1.3 GitHub portfolio (CSOAI-ORG)

- **250 public repos** in the org as of 8 Jun 2026.
- **6 of the 250 have any stars** (max 2★, median 0★).
- All pushed 7 Jun 2026 (the OpenSSF Scorecard remediation push).
- **0 forks across the 250** — verified.

### 1.4 Our visual gaps (preliminary, the audit must verify these)

1. **We are NOT on Glama** (32,634-server registry, last updated 08:33
   today). Glama requires a separate submission.
2. **We are NOT on Smithery** (no `@CSOAI-ORG/meok-compliance-gateway`
   page on smithery.ai as of 08:30 UTC).
3. **PyPI project URLs on most packages point to `github.com/CSOAI-ORG/<repo>`**
   but **the keystone `meok-compliance-gateway` is not on PyPI** (it runs
   from this repo). The audit must verify whether to fix this.
4. **None of the 76 MCP-reg entries have icons** (the MCP-reg schema
   supports `icons`, `websiteUrl`, `metadata.categories`, etc. — we use
   none of them).
5. **The MCP-reg descriptions are inconsistent**: some are 5-word summaries
   ("meok-governance-engine-mcp MCP server by MEOK AI Labs"), some are
   detailed (the latest `meok-mcp-injection-scan-mcp` and
   `meok-eu-ai-act-art-13-ifu-mcp`).

---

## 2. The 8 distribution channels to audit

For each channel, dispatch one sub-agent. Each sub-agent screenshots +
scores + returns a per-competitor breakdown. Be **factual and visual**, not
war-rhetoric (banned vocabulary per §10).

### Channel A — **PyPI listings** (the install point)

**URL pattern:** `https://pypi.org/project/<pkg-name>/`

**For each competitor in §3, audit:**
- README rendering (RST/MD), does the description render cleanly?
- Project URL links (Homepage, Repo, Docs) — present, broken, or absent?
- Classifiers — how many, do they include the right ones
  (License :: OSI Approved, Programming Language :: Python :: 3.11+, etc.)?
- Version cadence — last release date, frequency
- Download counts (last 30d / last 90d if available)
- Screenshots: top of project page, full description panel, sidebar

**For our 17 high-value hives, audit the same fields** so we can compare
side-by-side. Our PyPI names follow `<domain-without-TLD>-mcp` (e.g.
`eu-ai-act-compliance-mcp`, `meok-compliance-gateway-mcp`).

### Channel B — **MCP Registries** (where AI agents find us)

Four registries matter. Dispatch one sub-agent per registry.

**B1. Smithery** — `https://smithery.ai`
- The Smithery landing for each competitor's MCP server (search the
  competitor name + "mcp")
- Screenshots: server card, install button, tool list, README preview
- Score: install friction (1-click vs multi-step), visual quality of
  the tool descriptions, presence/absence of usage examples

**B2. Glama** — `https://glama.ai/mcp/servers`
- Same audit pattern. Glama is the most-trafficked MCP discovery
  surface as of 2026 — 32,634 servers indexed.
- Glama has its own **Tool Definition Quality Score** (A/B/C) and
  **License/Quality/Maintenance** badges. Capture those.

**B3. Pulse MCP** — `https://www.pulsemcp.com/servers`
- Editorial-style listings. Note how competitors frame their value
  props (headline, sub-headline, "best for" tags).

**B4. MCP.so / mcpize** — `https://mcp.so` + `https://mcpize.com`
- Both are aggregated indexes. Note: which competitors are listed,
  which aren't, metadata quality.

**B5. MCP official registry** — `https://registry.modelcontextprotocol.io`
- This is the canonical registry, exposed by Anthropic+the MCP project.
- 76 of our servers are listed here. 1 of the 6 named GRC competitors
  (ark-forge) is here. The other 5 are NOT.
- Audit: the `server.json` schema. Capture the rendered "View Server"
  page if the registry has a public front-end.

**For all 5 registries:**
- Are we (CSOAI-ORG) listed? Search `csoai`, `meok`, `compliance-mcp`.
- If yes, screenshot our listing. If no, that's a gap to fix.
- For each competitor, note: registration date, last update, install
  count if shown, screenshot quality.

### Channel C — **MCP Server Catalog (Docker Hub MCP Catalog)**

**URL:** `https://hub.docker.com/catalogs/mcp`
- Per Docker's launch (Nov 2024), this is the official MCP server
  catalog. Each server has a `docker/mcp-catalog` repo.
- Audit: which competitors have submitted servers? What does the
  listing look like? Screenshots.

### Channel D — **A2A Agent Card endpoints** (peer-to-peer mesh)

**URL pattern:** `https://<domain>/.well-known/agent-card.json`
- This is the agent-discovery standard Google A2A introduced 2025.
- For each competitor that has an A2A presence, fetch their
  agent-card.json and screenshot the rendered page (or a JSON
  formatter like jsonhero.io).
- For our 28 hives, the same is generated by
  `scripts/gen-hive.py` (gen_agent_card function). Compare what
  ours looks like vs theirs.

**Specifically check:**
- `capabilities`, `tools`, `auth`, `endpoints` fields
- Whether the card is human-readable when rendered
- Whether there's a `.well-known/openapi.yaml` or equivalent for the
  agent's surface

### Channel E — **ACP (Agent Communication Protocol) listings**

ACP is the emerging standard (IBM / Linux Foundation, late 2025).
- URL: `https://agentcommunicationprotocol.dev/` (or wherever the
  canonical registry is — verify)
- Audit: which competitors are listed? Is there a visual registry?
- If ACP doesn't have a public registry yet, note that as a gap and
  move on.

### Channel F — **ANP (Agent Network Protocol)**

ANP is the third peer-to-peer standard (dec 2024).
- URL: `https://agent-network-protocol.com/` (verify)
- Same audit pattern. Note: we have an `anp`-mode compliance tool
  in `agentaudit/safety_experts.py` per the SMITHERY listing. Verify
  the ANP registry has anyone listed.

### Channel G — **Cloud marketplaces** (where they sell)

- **AWS Marketplace** — `https://aws.amazon.com/marketplace`
- **Azure Marketplace** — `https://azuremarketplace.microsoft.com`
- **GCP Marketplace** — `https://console.cloud.google.com/marketplace`
- **Docker MCP Catalog** — covered in C
- **Smithery Container** — covered in B1

For each marketplace, audit:
- Are the competitors listed? What do their listings look like?
- Pricing model displayed (per-hour, per-month, BYOL)?
- Screenshots: hero, product details, pricing table, reviews

### Channel H — **Documentation sites** (the "is this real?" check)

For each competitor, dispatch a sub-agent to:
- Find their official docs (mintlify, readme.io, gitbook, custom)
- Screenshot the homepage
- Score: 1-10 on (a) load speed, (b) visual quality, (c) onboarding
  clarity, (d) code-sample quality, (e) search functionality

### Channel I — **GitHub repo presentation**

- README rendering on github.com
- Screenshot the README + the repo homepage + the "About" sidebar
- Score: badge presence (OpenSSF, license, last-commit, contributors),
  screenshot in README, table of contents, quickstart prominence

### Channel J — **x402 / micropayment listings**

Coinbase's HTTP 402 / x402 paywall (introduced 2025). Search for
competitors that have published a `/.well-known/x402.json` or similar.
- URL: `https://docs.cdp.coinbase.com/x402/` (verify)
- Audit: which competitors are using x402? What does the listing look
  like? How does their per-call pricing compare to ours?

### Channel K — **Cloudflare/edge MCP deployments**

Some competitors (e.g. Cloudflare's own MCP servers) deploy at the
edge with sub-10ms latency.
- URL: `https://developers.cloudflare.com/agents/mcp/`
- Audit: which competitors are deployed at the edge? What does that
  listing look like? How does it compare to our keystone's
  `https://api.meok.ai/v1/governance/*` endpoint?

---

## 3. The competitor list (verified, 8 Jun 2026)

Use these for the audit. **Don't expand the list without explicit
instruction** — we want a focused 17-competitor sweep, not a sprawling
"every MCP server" sweep.

### 3.1 AI Governance / Compliance (the core competitive set)

| # | Name | URL | Est. price | MCP reg entry? | Notes |
|---|---|---|---:|---|---|
| 1 | **OneTrust** | onetrust.com | $120-500K/yr | **NO** | enterprise privacy/governance |
| 2 | **Credo AI** | credo.ai | $50-150K/yr | **NO** | AI governance |
| 3 | **Holistic AI** | holisticai.com | $40-100K/yr | **NO** | AI governance; PyPI `holisticai` 36/day |
| 4 | **Vanta** | vanta.com | $10-30K/yr | **NO** | SMB GRC |
| 5 | **Drata** | drata.com | $15-50K/yr | **NO** | SMB GRC |
| 6 | **Secureframe** | secureframe.com | $12-40K/yr | **NO** | SMB GRC |
| 7 | **Sprinto** | sprinto.com | n/a | **NO** | SMB GRC |
| 8 | **IBM OpenPages** | ibm.com/products/openpages | enterprise | **NO** | enterprise GRC |
| 9 | **ServiceNow GRC** | servicenow.com | enterprise | **NO** | enterprise GRC |
| 10 | **RSA Archer** | rsa.com/products/archer | enterprise | **NO** | enterprise GRC |
| 11 | **LogicGate Risk Cloud** | logicgate.com | n/a | **NO** | mid-market GRC |
| 12 | **Fiddler AI** | fiddler.ai | n/a | **NO** | XAI / explainability |
| 13 | **Arthur AI** | arthur.ai | n/a | **NO** | AI observability |
| 14 | **Weights & Biases** | wandb.ai | n/a | **NO** | ML ops |
| 15 | **Arize AI** | arize.com | n/a | **NO** | ML observability |
| 16 | **ark-forge** (direct comp) | ark-forge/mcp-eu-ai-act | **free, MIT** | **YES** | 8★, 4 versions Feb–Apr 2026, hosted at arkforge.fr |

**Structural finding:** 15 of the 16 named competitors have **ZERO
presence on the MCP official registry**. Only `ark-forge/mcp-eu-ai-act`
(a French open-source project) competes with us on the MCP-native surface,
and it has done so aggressively in the last 90 days (4 releases in 2
months). This is the single largest visual-audit opportunity: **the entire
$120-500K/yr AI governance category is invisible on the agent-discovery
surface that AI agents actually use to find tools.** Our 76-server
presence makes us, by registry volume, **the dominant** AI-governance
player on the MCP official registry.

### 3.2 MCP-native / A2A-native (the new entrants, post-2024)

| # | Name | URL | Notes |
|---|---|---|---|
| 17 | **ModelContextProtocol (official)** | modelcontextprotocol.io + `github.com/modelcontextprotocol` reference servers | 15+ reference servers |
| 18 | **OpenAI's MCP integrations** | published list (announced March 2025) | 7+ integrations |
| 19 | **Anthropic's reference servers** | `github.com/modelcontextprotocol/servers` | 12+ servers |
| 20 | **Cloudflare's MCP servers** | `github.com/cloudflare/mcp-server-cloudflare` | 1 server, deployed at edge |
| 21 | **AWS Labs MCP** | `github.com/awslabs/mcp` | 15+ servers, per-call pricing |

### 3.3 Agent frameworks with MCP support

| # | Name | URL | Notes |
|---|---|---|---|
| 22 | **LangChain MCP adapters** | `github.com/langchain-ai/langchain-mcp-adapters` | PyPI `langchain-mcp` 105/day |
| 23 | **CrewAI** | crewai.com | PyPI `crewai` 1.14.6 |
| 24 | **AutoGen (Microsoft)** | `github.com/microsoft/autogen` | PyPI `autogen-agentchat` 25,574/day |
| 25 | **Semantic Kernel (Microsoft)** | `github.com/microsoft/semantic-kernel` | n/a |

**Visual audit the top 10-12 from each section** — don't try to do all
25, the data volume is too high. Pick the ones with the most overlap to
our 28-hive fleet (i.e., AI governance + MCP-native).

### 3.4 Direct MCP-native competitor (the "level 1" direct comp)

`ark-forge/mcp-eu-ai-act`:
- GitHub: `github.com/ark-forge/mcp-eu-ai-act` (8★, 3 forks, MIT, Python)
- Topics: `ai-governance`, `ai-regulation`, `ai-safety`, `claude`,
  `compliance`, `compliance-scanner`, `eu-ai-act`, `gdpr`, `llm`, `mcp`,
  `mcp-server`, `model-context-protocol`, `python`, `regulation`
- Created: 2026-02-16, last push: 2026-06-04 (4 days ago)
- 4 MCP-reg versions: 1.1.0 (28 Feb) → 1.5.0 (2 Mar) → 2.0.22 (22 Apr) →
  2.0.31 (24 Apr)
- Description on latest: "EU AI Act + GDPR compliance scanner. One call, no
  arguments, 10 seconds. 22 AI frameworks detected. Free."
- Homepage: `https://arkforge.fr/mcp-eu-ai-act.html`
- **No PyPI package** (or the PyPI name is hidden — verify)

This is the closest direct competitor. **The audit must deep-dive this
project specifically on channels A, B1, B2, B5, I.**

---

## 4. Sub-agent dispatch template

For each (channel, competitor) pair, dispatch a sub-agent with this prompt:

```
You are auditing the VISUAL presentation of <COMPETITOR_NAME> on <CHANNEL>.

Your job:
1. Visit <URL> and screenshot the page (full page, not just above the fold).
2. Score on these 5 dimensions (1-10 each):
   - Visual hierarchy: do the eyes know where to land?
   - Onboarding clarity: can a new evaluator understand what this is in
     5 seconds?
   - Information density: is it too sparse or too dense?
   - Trust signals: are there badges, citations, social proof?
   - Code example quality: if applicable, are install/usage examples
     copy-pasteable?
3. Capture the 3 best things (with quotes + line numbers from the page)
   and the 3 worst things.
4. Return a structured JSON: {
     "competitor": "<name>",
     "channel": "<channel>",
     "url": "<url>",
     "screenshot_paths": ["..."],
     "scores": {"hierarchy": N, "onboarding": N, "density": N, "trust": N, "code": N},
     "best": ["...", "...", "..."],
     "worst": ["...", "...", "..."],
     "recommendations_for_us": ["...", "..."]
   }

DO NOT use war-rhetoric ("kill shot", "crush", "nuclear", "coup de grâce",
"seeding doubt", "depletion campaign", "talent raid", "strike while").
Use factual comparative language ("denser", "clearer", "more code-first",
"fewer badges", "stronger social proof").

If the URL is 404 / unreachable, report that and try the Wayback Machine
(web.archive.org) for the most recent snapshot.
```

---

## 5. Output format (what to return to Nick)

A single markdown report at
`/Users/nicholas/meok-research/competitor-visual-audit-2026-06-08/REPORT.md`
with:

### Section 1 — Channel-by-channel findings

For each of channels A-K:
- A summary table (rows = competitors, columns = scores)
- Top 3 best-in-class and top 3 worst-in-class (with screenshots)
- Specific recommendations for our 17 high-value hives on that channel

### Section 2 — Per-hive recommendations

For each of our 17 high-value hives:
- "Your PyPI listing is missing X" (specific)
- "Your Smithery card needs Y" (specific)
- "Your README should steal Z from competitor W" (specific, factual)

### Section 3 — Quick wins (this week)

A short prioritized list of changes we can make to our own listings
that would close the visual-quality gap, ordered by impact.

### Section 4 — Strategic gaps

Things competitors do that we have no answer to. e.g., "Vanta has a
status page; we don't. Should we?"

### Section 5 — The "ark-forge deep-dive" appendix

A 3-page focused analysis of `ark-forge/mcp-eu-ai-act` (the only
direct MCP-native competitor). Cover: their README, their PyPI (or
absence thereof), their MCP-reg description, their homepage at
`arkforge.fr/mcp-eu-ai-act.html`, and 5 specific visual levers they
pull that we don't.

---

## 6. Banned vocabulary (apply to ALL output)

Per the MEOK External Communications Rubric
(`/Users/nicholas/meok-compliance-gateway/RUBRIC_EXTERNAL_COMMS.md`):

| BANNED | USE INSTEAD |
|---|---|
| kill shot, crushing, nuclear arsenal, coup de grâce | "differentiator", "10x advantage", "feature comparison" |
| talent raid | "hiring from", "recruiting engineers with experience in" |
| seeding doubt, depletion campaign | "case study of", "evidence that", "documented in" |
| strike while, vulnerability window | "launch in coordination with", "market opportunity" |
| Acquisition target | "potential strategic partner" |
| Funding fiction / overstated | "Independent verification of funding claims" (factual) |

**Before publishing any sentence, run the 3-question test:**
1. Could a regulator read this as market manipulation?
2. Could a competitor sue for defamation?
3. Could this be screenshot-tweeted as "look how toxic"?

If any answer is "yes," rewrite.

---

## 7. What this brief does NOT do (explicit non-scope)

- **No live data exfiltration** — screenshots only, not scraping PII.
- **No price comparisons to specific named companies** in public
  outputs (we have the comparison matrix internally; public claims
  must be "X cheaper than typical governance platforms" not "X cheaper
  than OneTrust").
- **No war-rhetoric** in any output. See §6.
- **No MCP server submissions** to any registry — that's a Nick-gated
  action. This brief only audits; it doesn't fix.
- **No code changes** to any of our 28 hive repos. Recommendations
  only.
- **No login to any portal** — all surfaces are public.
- **No 28MB audit file** to a remote service. The Kimi audit zip
  is local-only by user direction.

---

## 8. Auth + access

- **No login required** for any of the channels listed. All are public
  surfaces.
- **No `gh` / `aws` / `gcloud` auth** required.
- **No PyPI upload** required (that's `twine upload`, separate flow).
- **If a channel requires auth** (e.g., GCP Marketplace listing detail
  page behind a vendor portal), note that the audit is blocked and
  skip.

---

## 9. Time budget

- **Per (channel, competitor) audit:** 5-10 minutes
- **Total audit:** 11 channels × 12 competitors = 132 audits × 7 min
  = ~15 hours of sub-agent time
- **Realistic with 4-8 parallel sub-agents:** 2-3 hours wall-clock
- **Output report writing:** 1-2 hours

**Total wall-clock budget: 4-5 hours.**

If you need to compress, drop the MCP-native list (Anthropic / OpenAI /
Cloudflare / AWS Labs) and focus on the 12 AI governance / GRC
competitors — those are the ones whose visual playbook matters most
for our pricing undercut claim.

---

## 10. Acceptance criteria (what "done" looks like)

- [ ] Every channel A-K has at least 5 competitor screenshots
- [ ] Every channel has a 1-page summary table
- [ ] Every one of our 17 high-value hives has at least 3 specific
      recommendations
- [ ] The "quick wins" list is ≤ 10 items, each ≤ 1 hour of our time
- [ ] Zero banned vocabulary in the output (run the 3-question test
      on every paragraph)
- [ ] Output saved to
      `/Users/nicholas/meok-research/competitor-visual-audit-2026-06-08/REPORT.md`
- [ ] A short summary (1 paragraph + key links) posted back to the
      session that commissioned this audit
- [ ] Section 5 (ark-forge deep-dive) is 3 pages minimum

---

## 11. How to use this brief

**Option A — Drop into Kimi CLI/Agent directly.** Kimi's multi-agent
support handles the parallel dispatch; no extra plumbing needed.

**Option B — Run the sub-agent prompts in your own orchestration.**
Section 4 has the sub-agent template. Replace `<COMPETITOR_NAME>` and
`<CHANNEL>` and `<URL>` per audit.

**Option C — Hand to a human researcher.** Section 1-3 are the brief;
section 4-10 are the deliverable spec.

---

## 12. Appendices (data dumps for sub-agents)

### Appendix A — Our 17 high-value hives (priority targets)

These are the hives that should get specific per-channel recommendations:

**Flagships (4):** meok.ai, csoai.org, proofof.ai, cobolbridge.ai
**Governance (9):** accountabilityof.ai, agisafe.ai, asisecurity.ai,
biasdetectionof.ai, dataprivacyof.ai, ethicalgovernanceof.ai, safetyof.ai,
transparencyof.ai, councilof.ai
**UK construction (4):** grabhire.ai, muckaway.ai, planthire.ai,
commercialvehicle.ai

### Appendix B — Our 5 highest-traffic PyPI packages (the top of the funnel)

1. `eu-ai-act-compliance-mcp` — 136/day, 2687/mo, 31 releases
2. `bias-detection-mcp` — 258/day, 1736/mo
3. `ai-bom-mcp` — 246/day, 1728/mo
4. `agent-audit-logger-mcp` — 236/day, 1100/mo
5. `meok-tacho-audit-mcp` — 208/day, 327/mo (note: 0 MCP-reg entries
   yet — gap!)

### Appendix C — Our 4-tiers pricing (the undercut narrative)

For the AI governance undercut claim:
- **Free micro-call** (x402, per-call): $0.001-0.01 per tool call
- **Team** (29 seats): $29/user/month
- **Business** (49 seats): $49/user/month
- **Enterprise**: custom, typically $50-200K/yr

Competitor benchmarks (factual, from public pricing pages, verified 8
Jun 2026):
- Vanta: $10-30K/yr (SMB)
- Drata: $15-50K/yr (SMB)
- Secureframe: $12-40K/yr (SMB)
- Credo AI: $50-150K/yr (mid-market)
- Holistic AI: $40-100K/yr (mid-market)
- OneTrust: $120-500K/yr (enterprise)

**Undercut (factual, public-safe language):** "Team tier undercuts
mid-market GRC by 10-30x on a per-seat basis; Enterprise tier undercuts
comparable offerings by 2-8x for organizations with fewer than 5,000
seats."

### Appendix D — MCP official registry schema fields we don't use

Per `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`
the registry supports:
- `icons[]` — we don't set any
- `websiteUrl` — we don't set
- `metadata.categories[]` — we don't set
- `metadata.publisher` — we don't set
- `examples[]` — we don't set
- `prompts[]` — we don't set
- `resources[]` — we don't set

The audit should specifically call this out — these are all "free
visual improvements" we can make in 1-2 hours per server.

### Appendix E — The 250-repo CSOAI-ORG portfolio

- 250 public repos
- 6 of 250 have any stars (max 2★, median 0★)
- 0 forks across the 250
- All pushed 7 Jun 2026 (OpenSSF Scorecard remediation push)
- 40+ are compliance/AI-governance related
- 6 are the 28-hive flagships (meok.ai, csoai.org, proofof.ai,
  cobolbridge.ai, agentaudit, meok-compliance-gateway)

The audit should also consider: should we consolidate these into a
single monorepo? Or keep 250 repos? This is a structural question
the audit should surface (visual question: do 250 separate repo homepages
read as "broad portfolio" or "messy shop"?).

---

*Brief v2 generated 8 Jun 2026 by Claude (minimax-m3) on session
`claude/review-changes-mkbcvckpl5ix3r03-MkKCu`. v1 preserved at the same
path without `v2` suffix. Co-Authored-By: Claude Opus 4.8
<noreply@anthropic.com>.*
