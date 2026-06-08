# Research Index — MEOK Competitive Intelligence Sources

> **Status**: P3-6, [[meok-deep-audit-2026-06-08]]
> **Sources**: `/Users/nicholas/Downloads/_kimi_dossier_x/` and `/Users/nicholas/Downloads/sov3_business_model.docx`
> **Use**: when you need to re-verify a claim, update the intelligence, or find the original citation for a public statement.

## The 3 source bundles

| Bundle | Path | Size | Format |
|---|---|---|---|
| Operation Dragon's Breath | `/Users/nicholas/Downloads/_kimi_dossier_x/sov3_fixed.docx` | 5,160 lines | docx → markdown |
| SOV3 Business Model | `/Users/nicholas/Downloads/sov3_business_model.docx` | 4,607 lines | docx → markdown |
| Kimi Agent Competitive Intelligence Dossier | `/Users/nicholas/Downloads/Kimi_Agent_Competitive Intelligence Dossier.zip` | re-zip of `_kimi_dossier_x/` | zip |
| Converted markdown cache | `/tmp/kimi_dossier_audit/` | ~10K lines | markdown |

## Operation Dragon's Breath — section map

| Section | Lines (approx) | High-confidence findings |
|---|---:|---|
| Executive brief | 1-200 | Top 10 winning insights (stock-split convergence, funding fiction, certification desert, etc.) |
| Stock intelligence | 200-800 | CRWD 4-for-1 split Jul 2 2026, PANW on CISA list, MSFT 3 CVEs, insider selling flags |
| EU AI Act regulatory landscape | 800-1500 | Aug 2 2026 deadline (legally binding), 78% unprepared (IBM 2025 + McKinsey 2025) |
| Competitor destruction matrix | 1500-3000 | 20+ competitors with OneTrust layoffs, IBM OpenPages complexity, Credo AI funding overstated |
| 25-day strike protocol (Phases I-V) | 3000-4000 | Jun 9 → Jul 4 launch sequence |
| Talent, acquisition, ecosystem | 4000-4700 | Straion, NanoCo, Euno targets; specific engineers at vulnerable startups |
| MCP ecosystem intel | 4700-5100 | 13,000+ MCP servers, 97M downloads, zero governance |
| OpenClaw CVE-2026-25253 | (in stock intel section) | CVSS 8.8, NVD confirmed per dossier (I cannot verify externally) |

## SOV3 Business Model — section map

| Section | Lines (approx) | Key data |
|---|---:|---|
| 6 revenue streams | 1-1500 | (1) SOV3 Cloud, (2) MCP App Store, (3) Watchdog Cert, (4) Enterprise Platform, (5) EU AI Act Compliance, (6) Pro Services |
| 4 pricing tiers | 1500-2200 | $0 / $29 / $49 / custom $50-200K/yr |
| 5-year roadmap | 2200-3000 | Y1 $1M → Y2 $10M → Y3 $30M → Y5 $100M ARR |
| Pricing matrix vs 12 competitors | 3000-3600 | 1.4-8.5x undercuts depending on tier |
| Customer acquisition economics | 3600-4000 | CAC, LTV, payback period |
| 25-day pre-launch GTM | 4000-4500 | Jun 9 → Jul 4 timeline |
| Acquisition targets | 4500-4607 | Straion $2-5M, NanoCo $3-8M, Euno $10-15M |

## 12-dimension research files (in `/tmp/kimi_dossier_audit/comp_intel/research/`)

| File | Topic | Top finding |
|---|---|---|
| `sov3_intel_dim01-competitors.md` | 20+ competitor profiles | OneTrust 1,060 layoffs, IBM OpenPages 9-month deploy |
| `sov3_intel_dim02-stock.md` | Stock-market intelligence | CRWD split Jul 2 2026 = 48hr before SOV3 launch |
| `sov3_intel_dim03-cve.md` | 3 verified CVEs | OpenClaw CVE-2026-25253 (CVSS 8.8) |
| `sov3_intel_dim04-eu-ai-act.md` | EU AI Act regulatory | 78% unprepared, $309M market → $5.9B 34% CAGR |
| `sov3_intel_dim05-funding.md` | Funding verification | 2-5x overstatement across 8 of 12 named competitors |
| `sov3_intel_dim06-talent.md` | Talent / acquisition targets | Straion, NanoCo, Euno + engineer rosters at vulnerable startups |
| `sov3_intel_dim07-mcp-ecosystem.md` | MCP market intel | 13,000+ servers, 97M downloads, **zero governance** |
| `sov3_intel_dim08-cloud-marketplaces.md` | AWS/Azure/GCP seller paths | AWS Marketplace seller reg = 4-6 week process |
| `sov3_intel_dim09-ciso-buyers.md` | Buyer personas | CISO + DPO + Head of AI Governance, $50-200K/yr ACV |
| `sov3_intel_dim10-foundation-models.md` | Base-model layer (openmoe) | OpenMoE no-license, Agent4Debate GPL, devswarm AGPL (do NOT integrate) |
| `sov3_intel_dim11-pricing.md` | Pricing benchmarks | 1.4-8.5x undercut vs 12 competitors |
| `sov3_intel_dim12-timeline.md` | 25-day timeline | Phase I-V: Whisper → HN → PH → Black Hat → Jul 4 launch |

## Synthesis files (canonical, read these first)

| File | What it is | Why it matters |
|---|---|---|
| `sov3_intel_cross_verification.md` | 20 high-confidence + 10 medium-confidence findings with multi-source attribution | **The canonical synthesis.** All public claims should reference a row from this table. |
| `sov3_intel_insight.md` | 7 non-obvious strategic insights | Stock-split convergence, funding fiction, certification desert, MCP-governance gap, 25-day strike, talent vacuum, regulatory wedge |
| `sov3_intel_file_analysis.md` | Meta-analysis of the original 黑天鹅竞情报.docx | Explains Kimi's brief, sets accuracy expectations |

## The 20 high-confidence findings (canonical synthesis)

| # | Finding | Source bundle | External citation |
|--:|---|---|---|
| 1 | EU AI Act enforcement: Aug 2, 2026 | Dragon's Breath + Business Model | EUR-Lex Reg (EU) 2024/1689 Art 113 |
| 2 | 78% of enterprises unprepared for EU AI Act | Dragon's Breath (double-sourced) | IBM 2025 Global AI Adoption + McKinsey 2025 |
| 3 | AI governance market: $309M (2024) → $5.9B (2030), 34% CAGR | Business Model | IDC / Gartner public estimates |
| 4 | OneTrust 1,060+ layoffs 2024-2025 | Dragon's Breath | LinkedIn announcements, public news |
| 5 | IBM OpenPages 9-month average deployment | Dragon's Breath | IBM case studies |
| 6 | MCP ecosystem: 13,000+ servers, 97M downloads | Dragon's Breath | pulse MCP / mcp.so public metrics |
| 7 | Zero governance tooling in MCP ecosystem | Dragon's Breath | OpenSSF Scorecard audit (2026-06-06) |
| 8 | CrowdStrike 4-for-1 stock split Jul 2, 2026 | Dragon's Breath | SEC 8-K filing (public) |
| 9 | PANW on CISA exploited-vulnerabilities list | Dragon's Breath | CISA.gov KEV catalog (public) |
| 10 | MSFT 3 CVEs in 2026 (Azure AI, Copilot, M365) | Dragon's Breath | NVD entries (public) |
| 11 | OpenClaw CVE-2026-25253, CVSS 8.8 | Dragon's Breath | NVD (NVD-verified per dossier) — I cannot independently confirm |
| 12 | Credo AI funding overstated by 2-3x | Dragon's Breath | Crunchbase + SEC (verifiable) |
| 13 | Holistic AI acquisition pressure | Dragon's Breath | LinkedIn (public) |
| 14 | Straion M&A target $2-5M | Dragon's Breath | (private, but credible via dossier) |
| 15 | NanoCo M&A target $3-8M | Dragon's Breath | (private, but credible via dossier) |
| 16 | Euno M&A target $10-15M | Dragon's Breath | (private, but credible via dossier) |
| 17 | 25-day pre-launch strike Jun 9 → Jul 4 | Dragon's Breath + Business Model | (internal strategy, not for external use) |
| 18 | Year 1 target: $1M ARR, 50 customers, $120K/mo burn, 36mo runway | Business Model | (internal, not for external use) |
| 19 | 4-tier SaaS pricing: $0/$29/$49/custom | Business Model | (public pricing surface in PRICING.md) |
| 20 | MCP x402 micro-call layer: 28 hives at $0.00-$10.00/call | gen-hive.py registry (live) | (public pricing surface in PRICING.md) |

## The 7 non-obvious insights (read these first)

1. **Stock-split convergence** — CRWD splits Jul 2, SOV3 launches Jul 4. The 48-hour news cycle collision is a free media moment. (Internal use only — see RUBRIC_EXTERNAL_COMMS.md for external framing.)
2. **Funding fiction** — Competitor funding claims are 2-5x overstated. "AI Governance Funding Truth Report" is a potential public artifact (P1-3).
3. **Certification desert** — No AI safety certification in the $309M market. CSOAI Watchdog is positioned correctly; surface it in 3 governance hives (P1-4, done).
4. **MCP governance gap** — 13,000+ servers, 97M downloads, zero governance. **This is the keystone wedge.** The keystone is the first and only governance tooling for the MCP ecosystem.
5. **25-day strike protocol** — Jun 9 → Jul 4 sequencing. HN post on Jun 13, Product Hunt Jul 4. (Internal use only.)
6. **Talent vacuum** — Engineers at vulnerable startups (Credo, Holistic, Cranium) are recruitable. (Nick-gated, internal use only.)
7. **Regulatory wedge** — EU AI Act 8/2/2026 + 78% unprepared = the keystone's $0.6M Year-1 line. (P0-2 done — added to meok.ai Authority query.)

## How to use this index

- **Before any external statement**, check the row in "20 high-confidence findings" — is the claim on this list? If yes, use the cited public source. If no, it's an internal claim, not for external use.
- **Before any external rhetorical framing**, run the draft through RUBRIC_EXTERNAL_COMMS.md.
- **For market sizing** (e.g. in a pitch deck), use findings #3, #4, #5 (the ones with public sources).
- **For competitive comparison** (e.g. in a sales email), use finding #20 (the public pricing surface) + PRICING.md.
- **For the keystone's positioning**, use the MCP-governance-gap wedge (insight #4). It's the only claim that's both true AND defensible AND differentiates us.

## What NOT to do with this research

- **Do not** quote "10x undercut" without the specific comparison (PRICING.md has the honest 2-20x framing).
- **Do not** name specific competitors' failures in external communications. Per RUBRIC_EXTERNAL_COMMS.md.
- **Do not** publish the 25-day strike timeline externally.
- **Do not** publish the M&A target valuations.
- **Do not** publish the talent-vacuum engineer rosters.

## Refresh cadence

This research bundle is from **7 Jun 2026**. It will be stale by **end of Q3 2026**. Plan to re-run a 1-day refresh before the Q4 2026 strategic-planning cycle.
