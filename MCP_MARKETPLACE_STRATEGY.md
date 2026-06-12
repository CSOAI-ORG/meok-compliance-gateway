# MCP Marketplace Strategy — 2026-06-08

> **Authored**: 2026-06-08
> **Purpose**: source-of-truth for MEOK's marketplace rollout across the 6 major MCP marketplaces, mapped to the keystone's 6-shipped / 4-specced MCP servers, the Watchdog Certification platform, and the 76-server master audit findings. This is the launch sequencing substrate for the dossier's "Phase 1: Tool Drop" (Jun 12 / Jun 16).
> **Source**: `/tmp/kimi_dossier_v2/research/deepdive_mcp_inventory.md` (659 lines, 7 parts: marketplace inventory, server count analysis, category matrix, competitor MCP analysis, CVE database, governance gap analysis, SOV3 strategy).
> **Rubric**: factual comparative, no war language per `RUBRIC_EXTERNAL_COMMS.md`. Banned vocabulary in § 10.

## 1. The 6-marketplace landscape

| Marketplace | URL | Server count | Differentiator | Listed? |
|---|---|---:|---|---|
| **MCP.so** | mcp.so | 21,956 | Broadest community collection | Planned |
| **Glama.ai** | glama.ai/mcp | 32,490 + 4,962 connectors (37,452 total) | Largest single registry, MCP Inspector sandbox | Planned |
| **PulseMCP** | pulsemcp.com | 16,822 | Daily-updated directory | Planned |
| **Smithery.ai** | smithery.ai | 2,880 | Curated, CLI-installable (`npx smithery mcp add`) | Planned |
| **Cursor Directory** | cursor.directory | ~500+ | MCP-related plugins for Cursor IDE | Planned |
| **awesome-mcp-servers** (GitHub) | github.com/topics/mcp | (community list) | GitHub discoverability, MIT-licensed | Planned |

**Total unique (post-dedup)**: 35,000-40,000 MCP servers. **Total tools indexed** (Glama): 228,120. **Active developers**: 50,000+. **Daily tool calls**: 18,000-1,000,000 depending on marketplace.

## 2. The 6-shipped MEOK MCP servers (ready to publish)

| # | Server | Category | Marketplace readiness |
|---:|---|---|---|
| 1 | **`meok-compliance-gateway`** (the keystone itself, as MCP) | AI Governance | Production-ready, HMAC-signed, x402 paywalled |
| 2 | **`eu-ai-act-compliance-mcp`** | EU AI Act compliance | Production-ready, 410 articles indexed, 42-point audit |
| 3 | **`meok-mcp-injection-scan-mcp`** | MCP security scanner | Production-ready, 30+ CVEs catalogued |
| 4 | **`agentaudit`** | A2A agent inventory | Production-ready (per [[agentaudit-stage6-shipped]]), 37 tests passing |
| 5 | **`proofof-ai-mcp`** | AI provenance / attestation | Production-ready (HMAC-signed) |
| 6 | **`openmoe-bft-mcp`** | BFT consensus for governance | Research-grade (per [[openmoe-ai-project]]) |

## 3. The 4-specced MEOK MCP servers (in design phase)

| # | Server | Category | Source spec | ETA |
|---:|---|---|---|---|
| 7 | **`meok-shadow-ai-discovery-mcp`** | Shadow AI detection (6 tools) | `SHADOW_AI_DETECTION_MCP_SPEC.md` | ~2 weeks build |
| 8 | **`watchdog-certification-mcp`** | 3-tier AI safety cert (Foundation/Professional/System) | `WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` | ~3 weeks build |
| 9 | **`mcp-security-audit-mcp`** | 42-point MCP audit standard | `MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` | ~1 week build |
| 10 | **`api-gateway-mcp`** (multi-protocol) | REST + GraphQL + gRPC + WebSockets bridge | `MEOK_API_STRATEGY.md` § 2 Phase 2 | ~6 weeks build |

## 4. The 7-step marketplace submission pattern (per-server)

For each of the 10 MEOK MCP servers, the submission workflow is:

1. **Pre-submission**:
   - `server.json` with the 6 required metadata fields (icons, websiteUrl, publisher, categories, examples, resources) per the keystone's `regen-mcp-reg.py` validation.
   - README with: 5-line description, 3-line install, 1-line value prop, badges (OpenSSF Scorecard, MIT, MCP-native).
   - `smithery.yaml` (for Smithery) with: command, args, env, secrets (API keys, x402 wallet), build config.
   - HMAC-signed attestation in the compliance ledger (per `meok_x402.py:66-126`).
2. **Smithery submission** (Smithery has the strictest CI):
   - `smithery deploy` from CLI.
   - Health check must pass (`smithery mcp inspect <server>`).
   - OAuth credential handling via `agent.pw` (or HMAC for x402).
3. **Glama.ai submission**:
   - Submit via `glama.ai/mcp/servers/new`.
   - Quality + safety scoring (Glama's algorithm).
   - Maintainer verification (one-time email + GitHub auth).
4. **MCP.so submission**:
   - Submit via `mcp.so/submit`.
   - Category assignment (auto + manual review).
   - Featured consideration (requires 1,000+ installs).
5. **PulseMCP submission**:
   - Submit via `pulsemcp.com/submit`.
   - Daily-updated directory (no manual review for valid submissions).
6. **Cursor Directory submission**:
   - Submit via `cursor.directory/submit`.
   - Requires Cursor compatibility test (`cursor mcp test`).
7. **Post-submission**:
   - 30-day KPI tracking (installs, GitHub stars, marketplace position).
   - Monthly README refresh (per the keystone's OpenSSF Scorecard workflow).
   - Quarterly CVE refresh (per the dossier's 30+ CVE database).

## 5. The 6 marketplace-priority matrix (where to publish first)

| # | Marketplace | Rationale | Priority | Submission date |
|---:|---|---|---|---|
| 1 | **Smithery.ai** | Strictest CI = strongest trust signal, OAuth + CLI install = developer-friendly | P0 | 2026-06-12 (Day -22) |
| 2 | **MCP.so** | Broadest community collection = highest install ceiling | P0 | 2026-06-12 (Day -22) |
| 3 | **Glama.ai** | Largest single registry + quality scoring = SEO authority | P0 | 2026-06-12 (Day -22) |
| 4 | **PulseMCP** | Daily-updated = freshness signal | P1 | 2026-06-16 (Day -18) |
| 5 | **awesome-mcp-servers** (GitHub) | GitHub discoverability + MIT-licensed credibility | P1 | 2026-06-16 (Day -18) |
| 6 | **Cursor Directory** | Niche but high-LTV audience (Cursor IDE users) | P2 | 2026-06-19 (Day -15) |

**Day -22 (Jun 12) launch**: ship the 6-shipped MCPs to the 3 P0 marketplaces. Target: 50 installs per server, 300 total on Day 1.

**Day -18 (Jun 16) launch**: extend to P1 marketplaces. Target: 200 installs per server, 1,200 total.

**Day -15 (Jun 19) launch**: extend to P2 + first Specced MCP (`meok-shadow-ai-discovery-mcp` v0.1). Target: 500 installs per server, 5,000+ total.

## 6. The 5 competitor MCP presence scores (factual)

| # | Competitor | MCP server? | Category | SOV3 opportunity |
|---:|---|---|---|---|
| 1 | **OneTrust** | No | n/a | Direct opportunity (AI governance customer base) |
| 2 | **Credo AI** | No | n/a | Direct opportunity (Forrester Wave Leader, no MCP exposure) |
| 3 | **Cranium** | No | n/a | Direct opportunity (AI security customer base) |
| 4 | **Holistic AI** | Partial | Network-level discovery (not MCP-native) | Partial opportunity (claim) |
| 5 | **WitnessAI** | Partial | Network-level gateway (not MCP-native) | Partial opportunity (claim) |
| 6 | **CrowdStrike** | Yes | `crowdstrike-falcon` (detections, incidents, threat intel) | Watch + learn (high MCP maturity = potential fast-follow) |
| 7 | **Holistics** | Yes | Full MCP server (Streamable HTTP, OAuth) | Watch + learn |
| 8 | **IBM** | No | n/a | Direct opportunity |
| 9 | **Microsoft** | No direct (but uses MCP internally) | n/a | Indirect (Azure AI Foundry = competitor runtime) |
| 10 | **Zenity** | MCP-aware | Monitors MCP interactions, doesn't provide MCP servers | Partial opportunity (position as governance layer) |

**Per [[sov3-mcp-master-audit-2026-06-08]]**: 13/15 GRC vendors have zero MCP presence. The 2 with presence (CrowdStrike, Holistics) are not governance-focused. **The governance-MCP category is empty.**

## 7. The 10-launch-productization opportunities (from gap analysis)

| # | Gap | MEOK server | First-mover status |
|---:|---|---|---|
| 1 | No unified AI governance MCP | `meok-compliance-gateway` (shipped) | **First** |
| 2 | No NIST AI RMF MCP | `meok-compliance-gateway` (covers 13 frameworks including NIST AI RMF) | **First** |
| 3 | No EU AI Act MCP | `eu-ai-act-compliance-mcp` (shipped, 410 articles) | **First** |
| 4 | No model card governance MCP | `meok-compliance-gateway` (model registry tool) | **First** |
| 5 | No bias detection MCP | `meok-mcp-injection-scan-mcp` (covers LLM03) | **First** |
| 6 | No drift detection MCP | Future (`model.drift.detect` is in the watch list) | **First** when shipped |
| 7 | No explainability MCP | Future (planned Q4 2026) | **First** when shipped |
| 8 | No multi-framework compliance | `meok-compliance-gateway` (13 frameworks) | **First** |
| 9 | No governance scoring | `meok-compliance-gateway` (trust scoring per `agentaudit`) | **First** |
| 10 | No supply chain governance | `meok-mcp-injection-scan-mcp` (CWE-829 + SBOM checking) | **First** |

**The pattern**: 9 of 10 governance-MCP categories are empty. MEOK fills 6 (shipped) + 1 (shadow AI) + 1 (watchdog cert) + 1 (MCP audit) = 9 of 10 first-mover positions.

## 8. The 4-marketplace-side revenue flow (per the dossier's projection)

| Marketplace | Free tier (1K calls/mo) | Team tier (100K calls/mo, $29/mo) | Business tier (unlimited, $49/mo) | Enterprise (custom) |
|---|---|---|---|---|
| MCP.so | Default | Self-serve upgrade | Self-serve upgrade | Sales-led |
| Glama.ai | Default (quality-score-gated) | Self-serve upgrade | Self-serve upgrade | Sales-led |
| Smithery.ai | Default (CLI-installed) | Self-serve upgrade | Self-serve upgrade | Sales-led |
| PulseMCP | Default (featured slot = paid) | Self-serve upgrade | Self-serve upgrade | Sales-led |

**Per-call revenue (x402 paywall, per `meok_x402.py:66-126` substrate)**: $0.10/1K logs, $0.50/repo, $0.01/classification. **Year-1 projection** (per `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` Stream 6): ~$10K loss-leader marketing spend, primarily to drive installs of the free tier.

## 9. The 4 launch-content assets (rubric-pass, marketplace-anchored)

| # | Asset | Channel | Lead metric | Banned-phrase audit |
|---:|---|---|---|---|
| 1 | "MCP Security Crisis: 35,000 Servers, Zero Governance" | meok.ai blog (Day -23, Jun 11) | 100 GitHub stars on the audit standard | Rubric-pass |
| 2 | "SOV3 MCP Server Audit Standard v1.0" | GitHub (the 447th repo) | 50 installs Day 1 | Rubric-pass |
| 3 | Submission of `meok-compliance-gateway` to all 6 marketplaces | Smithery + MCP.so + Glama + PulseMCP + Cursor + GitHub (Day -22, Jun 12) | 50 installs per server | Rubric-pass |
| 4 | X thread: "MCP is the fastest-growing AI protocol ever. It has zero security standards. We're fixing that." | X (Day -23, Jun 11) | 10K impressions | Rubric-pass |

## 10. The 4 "do NOT do" rules

1. **Do NOT claim the marketplace counts are "real-time" or "verified."** The dossier's counts are point-in-time (June 8, 2026) and depend on each marketplace's deduplication. Re-verify before any external publication.
2. **Do NOT name-and-shame specific competitors for missing MCP presence.** The factual statement "13/15 GRC vendors have zero MCP presence" IS external-safe (factual market-structure fact). The adversarial framing "X is irrelevant" is NOT.
3. **Do NOT use war vocabulary.** Banned per `RUBRIC_EXTERNAL_COMMS.md` § 8: "kill shot", "nuclear arsenal", "coup de grâce", "talent raid", "seeding doubt", "depletion campaign", "strike while", "vulnerability window", "acquisition target", "funding fiction".
4. **Do NOT overclaim "first" status for MCP categories that are partially filled.** The 6 partial-fills (CrowdStrike, Holistics, Zenity, Holistic AI, WitnessAI, plus the OpenClaw / LangChain etc. CVE-affected servers) are all noted in the gap analysis. The accurate claim is "first unified AI governance MCP" — not "first MCP server."

## 11. Cross-references

- `/Users/nicholas/meok-compliance-gateway/SHADOW_AI_DETECTION_MCP_SPEC.md` — server #7 in § 3 above.
- `/Users/nicholas/meok-compliance-gateway/WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` — server #8 in § 3 above.
- `/Users/nicholas/meok-compliance-gateway/MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` — server #9 in § 3 above, also the source for the 42-point audit.
- `/Users/nicholas/meok-compliance-gateway/MEOK_API_STRATEGY.md` — server #10 in § 3 above (multi-protocol).
- `/Users/nicholas/meok-compliance-gateway/CRITICAL_FIXES_2026-06-08.md` — the 3 CRITICAL fixes every MEOK MCP server must follow (root Docker, API key storage, HMAC env-var).
- `/Users/nicholas/meok-compliance-gateway/CVE_INTEL_BRIEF_2026-06-08.md` — the 30+ MCP CVE database that powers the MCP security scanner's CVE refresh cycle.
- `/Users/nicholas/meok-compliance-gateway/SOV3_UNIQUE_CAPABILITIES_MATRIX.md` — capability #7 (Multi-Protocol API), capability #8 (MCP-native) reference this strategy.
- `/Users/nicholas/meok-compliance-gateway/SOV3_FINANCIAL_MODEL_2026-2028.md` — Stream 6 (MCP App Store revenue) = $1.5M-$4M Year-1, references this strategy.
- `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` — differentiator #5 (35,000+ MCP servers) is the headline stat for this strategy.
- `/Users/nicholas/meok-compliance-gateway/28_DAY_BLOG_CALENDAR.md` — Day -23 (Jun 11), Day -22 (Jun 12), Day -18 (Jun 16), Day -15 (Jun 19) all reference this strategy.
- [[sov3-mcp-master-audit-2026-06-08]] — the audit memory, 76 MCPs catalogued, 13/15 GRC no-MCP finding.

## 12. Source pointers

- `/tmp/kimi_dossier_v2/research/deepdive_mcp_inventory.md` (full file, 659 lines).
- MCP.so server count = 21,956 (per the dossier's June 8, 2026 snapshot).
- Glama.ai server count = 32,490 + 4,962 connectors = 37,452 total.
- PulseMCP server count = 16,822.
- Smithery.ai server count = 2,880.
- 30+ MCP CVEs documented in the dossier's Part 5 (CVE database).
- OWASP Agentic Top 10 (2026) for the 617-finding distribution.
- Cloud Security Alliance's `mcpserver-audit` project (active in the gap analysis).
- The keystone's `meok-compliance-gateway` OpenSSF Scorecard workflow (monthly README refresh + quarterly CVE refresh).
