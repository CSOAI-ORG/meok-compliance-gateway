# 20-MCP Scorecards — Structured (extracted from sov3_mcp_master_audit.docx)

> **Source**: `~/Downloads/sov3_mcp_master_audit.docx` § "INDIVIDUAL SERVER SCORECARDS" (8 Jun 2026)
> **Method**: extracted via Python zipfile + regex, the docx is local-only per [[sov3-mcp-master-audit-2026-06-08]]
> **Scope**: 20 priority MCPs (1 per flagship category); the full 76-server audit is in the docx
> **Fleet grade**: 56.8/100 (C+). Top: `eu-ai-act-compliance-mcp` 73/100. Bottom: `llm-compliance-comparison-mcp` 42/100.

## The 20 scorecards (ranked by score, descending)

| # | Rank | Score | Grade | Server | Category | Top Strength | Top Improvement |
|---:|---:|---:|---|---|---|---|---|
| 1 | 1/20 | **73** | B+ | `eu-ai-act-compliance-mcp` | FLAGSHIP (EU AI Act) | HMAC-SHA256 signing, auth_middleware, rate limiting, SECURITY.md, CODEOWNERS | Add OpenSSF Scorecard badge; add SBOM |
| 2 | 2/20 | **67** | B | `meok-governance-engine-mcp` | UNIFIED ENGINE (multi-jurisdiction) | Cross-jurisdiction reasoning, 119 commits, 11 branches | Run third-party security audit or OpenSSF scorecard |
| 3 | 3/20 | **65** | B- | `meok-watermark-attest-mcp` | ART 50 COMPLIANCE (EU AI Act) | Watermarking per Art 50, tamper-evident | Community building — case studies, blog posts |
| 4 | 4/20 | **64** | B- | `dora-compliance-mcp` | FINANCIAL (DORA) | DORA ICT risk + incident reporting, FinServ vertical | Engagement — finance sector conferences |
| 5 | 5/20 | **63** | C+ | `meok-mcp-injection-scan-mcp` | SECURITY (prompt-injection firewall) | Prompt-injection detection, MCP-aware scanner | Security research/blog posts to build authority |
| 6 | 6/20 | **62** | C+ | `meok-cra-annex-iv-classifier-mcp` | CRA (Annex IV) | CRA Annex IV technical-doc classifier, EU CRA | Visual classification flowchart for users |
| 7 | 7/20 | **61** | C+ | `nis2-compliance-mcp` | NIS2 (cybersec) | NIS2 incident reporting, ENISA alignment | Sector-specific compliance templates |
| 8 | 8/20 | **61** | C+ | `cra-compliance-mcp` | CRA (general) | CRA vulnerability handling, SBOM, due-diligence | Integration with CVE databases |
| 9 | 9/20 | **61** | C+ | `gdpr-compliance-ai-mcp` | GDPR | DSR (data subject rights) workflow, 78% GDPR coverage | Integration with popular CRMs (Salesforce, HubSpot) |
| 10 | 10/20 | **60** | C | `csrd-compliance-mcp` | CSRD (sustainability) | ESRS data points, sustainability disclosure | Integration with carbon accounting platforms |
| 11 | 11/20 | **62** | C+ | `meok-compliance-gateway` | GATEWAY (keystone) | Single compliance MCP for the cloud-marketplace | Templates; registry presence weaker than individual MCPs |
| 12 | 12/20 | **57** | C | `bias-detection-mcp` | AI BIAS | Bias detection across LLM outputs, top traffic (258/day PyPI) | Open-source competitors; case studies showing real results |
| 13 | 13/20 | **57** | C | `ai-bom-mcp` | AI BOM | AI Bill of Materials, software supply chain | Vulnerability scanning of BOM components |
| 14 | 14/20 | **54** | C | `agent-audit-logger-mcp` | AUDIT (tamper-evident) | Tamper-evident audit trail (HMAC chain) | Export to common audit formats (XBRL, CSV) |
| 15 | 15/20 | **50** | C- | `agent-mcp-router-mcp` | INFRA (Router, 62 MCPs) | Single aggregator for 62 MCPs | Performance benchmarks under load |
| 16 | 16/20 | **54** | C | `meok-x402-wrap-mcp` | PAYWALL (x402) | **Best monetization in fleet**: x402 USDC paywall, 1-line integration | Add fiat on-ramp (most users don't have USDC) |
| 17 | 16/20† | **54** | C | `meok-attestation-verify` | ATTESTATION (HMAC verify) | Zero-dependency HMAC-SHA256 verifier, no third-party data | Documentation; multi-language SDK (Go, Rust) |
| 18 | 18/20 | **46** | D+ | `bft-progress-council-mcp` | GOV (BFT consensus) | Multi-agent BFT deliberation for board-grade consensus | Integration with Jira/ServiceNow for compliance workflows |
| 19 | 19/20 | **47** | D+ | `healthcare-ai-governance-mcp` | HEALTHCARE (HIPAA) | HIPAA-aligned AI governance, SaMD-aware | Clarify relationship to other governance MCPs |
| 20 | 20/20 | **42** | D | `llm-compliance-comparison-mcp` | LLM COMPLIANCE | Cross-LLM compliance comparison | FDA SaMD classification tools needed |

† #17 is tied at rank 16/20 with #16 (meok-x402-wrap-mcp).

## Score distribution

```
Score  Count  Servers
-----  -----  -------
73      1     eu-ai-act-compliance-mcp
67      1     meok-governance-engine-mcp
65      1     meok-watermark-attest-mcp
64      1     dora-compliance-mcp
63      1     meok-mcp-injection-scan-mcp
62      2     meok-cra-annex-iv-classifier-mcp, meok-compliance-gateway
61      3     nis2-compliance-mcp, cra-compliance-mcp, gdpr-compliance-ai-mcp
60      1     csrd-compliance-mcp
57      2     bias-detection-mcp, ai-bom-mcp
54      3     agent-audit-logger-mcp, meok-x402-wrap-mcp, meok-attestation-verify
50      1     agent-mcp-router-mcp
47      1     healthcare-ai-governance-mcp
46      1     bft-progress-council-mcp
42      1     llm-compliance-comparison-mcp
```

Mean: 57.5/100. Median: 60/100. Range: 42-73 (31 points).

## Grade distribution (n=20)

- **B+ (70-79)**: 1
- **B  (60-69)**: 9
- **B- (50-59)**: 0 (no pure B-)
- **C+ (60-69)**: 5 (counted in B column; no B-/C+ split in source)
- **C  (50-59)**: 3
- **C- (40-49)**: 0
- **D+ (40-49)**: 2
- **D  (30-39)**: 1

(NB: the docx grade table merges some ranges; the column above maps by score.)

## Category breakdown

| Category | Count | Mean Score | Top Performer |
|---|---:|---:|---|
| Compliance (frameworks) | 8 | 60.4 | eu-ai-act-compliance-mcp (73) |
| Infra / Gateway / Router | 4 | 53.0 | meok-compliance-gateway (62) |
| AI-specific (bias, BOM, watermark) | 3 | 59.0 | meok-watermark-attest-mcp (65) |
| Security (audit log, prompt-inj, BFT) | 3 | 54.3 | meok-mcp-injection-scan-mcp (63) |
| Paywall (x402) | 1 | 54.0 | meok-x402-wrap-mcp (54) |
| Cross-LLM | 1 | 42.0 | llm-compliance-comparison-mcp (42) |

## Top 3 cross-cutting issues (the audit's "fix first" list)

These appeared in 8+ of the 20 scorecards' "Top 3 Improvement Areas":

1. **No OpenSSF Scorecard badges** (mentioned 9×) — fix with `scripts/add_openssf_badge.py`
2. **No community / case studies** (mentioned 7×) — fix with Q3 2026 content push
3. **No integration with major platforms** (Salesforce, Jira, ServiceNow, carbon accounting, CVE databases — mentioned 6×) — fix per-flagship PRs

## How this intersects the keystone's work

The keystone (`meok-compliance-gateway`) scores 62/100, ranked 11/20. Per the audit's commentary, the keystone's biggest gaps are:

- **Templates**: each flagship ships a self-contained service; the keystone is the integration layer but its templates for downstream callers are sparse.
- **Registry presence**: the keystone is on the MCP official registry but with thinner metadata than individual flagships (the `MCP_REG_HEALTH_REPORT.md` shows this — keystone is in the "3 need server.json" tier).

The keystone's **monetization** (x402 paywall) is the keystone's only 9/10 dimension across the whole 20-server panel. That score lives in `meok-x402-wrap-mcp` (54/100 overall, but 9/10 on Monetization). The keystone inherits this strength but doesn't get the audit credit because the keystone's "monetization" dimension measures the SaaS subscription path (Stripe + Vercel), not the per-call x402 path.

## Cross-references

- `sov3-mcp-master-audit-2026-06-08.md` (memory) — durable summary
- `MASTER_AUDIT_INGESTION.md` — 1-page digest (internal-only)
- `MCP_REG_HEALTH_REPORT.md` — the 6-field server.json patch list (44 repos, 41 need patch)
- `KIMI_COMPETITOR_VISUAL_AUDIT_BRIEF_v2.md` — competitive framing
- `keystone_SECREVIEW.md` — the keystone's per-check OpenSSF audit
- [[sov3-mcp-master-audit-2026-06-08]] — the master audit memory
