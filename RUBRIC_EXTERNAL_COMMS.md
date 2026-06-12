# External-Communications Rhetoric-Scrubbing Rubric

> **Status**: P0-1, [[meok-deep-audit-2026-06-08]]
> **Owner**: Nick + LinkedIn/PR contractor
> **Audit cadence**: before any external publication, run this rubric
> **Sources to audit**: `clawd/mcp-marketplace/` (100+ PRs, 50 LinkedIn templates), future blog posts, press releases, conference talks

## Why this exists

The "Operation Dragon's Breath" competitive-intelligence dossier (5,160 lines, 7 Jun 2026) uses internal war-planning language. That language is fine for an internal strategy document but **fatal for external publication**. A small UK company that publishes "kill shot," "nuclear arsenal," "coup de grâce," "talent raids," "seeding doubt," or "depletion campaign" will be:

- **FCA/SEC scrutiny** — UK regulator + US regulator both view coordinated "kill" rhetoric as evidence of market manipulation.
- **Cloud marketplace delisting** — AWS Marketplace, Azure Marketplace, GCP Marketplace all have content policies that prohibit "unfair competitive practices."
- **Permanent reputation damage** — once "kill shot" appears in a press release, every future customer remembers it.
- **PBN / SEO penalty** — Google de-indexes sites with "thin competitive-attack press releases."

## The replacement vocabulary

| ❌ BANNED (war language) | ✅ REPLACEMENT (factual comparative) |
|---|---|
| Kill shot | "differentiator", "10x advantage", "feature comparison" |
| Nuclear arsenal | "comprehensive feature set", "full coverage of EU AI Act articles" |
| Coup de grâce | "complete solution", "single pane of glass" |
| Talent raid | "hiring from", "recruiting engineers with experience in" |
| Seeding doubt | "case study of", "evidence that", "documented in" |
| Depletion campaign | "competitive analysis", "comparison report" |
| Strike while | "launch in coordination with", "release alongside" |
| Vulnerability window | "market opportunity", "regulatory deadline" |
| Stock-split convergence play | "launch aligned with industry events" (NEVER reference stock splits) |
| CrowdStrike BSOD legacy | "Lessons from past industry incidents" (NEVER name specific companies' failures) |
| CISA exploited-vuln list | "Industry-wide vulnerability disclosures" (NEVER name the company) |
| Insider selling | (NEVER mention insider trading data) |
| Funding fiction / overstated | "Independent verification of funding claims" (FACTUAL, no attack framing) |
| Acquisition target | "potential strategic partner" (NEVER say "target" about a company you want to buy) |

## The 3-Question Test (run before publishing)

For every external paragraph, ask:

1. **Could a regulator read this as market manipulation?** If yes → rephrase.
2. **Could a competitor sue for defamation?** If yes → rephrase with citation requirement.
3. **Could this be screenshot-tweeted as "look how toxic this company is"?** If yes → rephrase.

If any answer is "yes," the paragraph is not ready for publication.

## Numbers, not adjectives

Where the dossier says "10x undercut," the public statement must be:

- **CORRECT framing (recommended)**:
  - "CSOAI's per-attestation cost is $10, vs. typical governance platforms charging $120-500K/year for equivalent coverage"
  - "Sovereign AI infrastructure deploys in 48 hours, vs. 2.5-9 months for legacy GRC rollouts"
  - "78% of enterprises are unprepared for EU AI Act August 2026 enforcement (IBM 2025, McKinsey 2025)"

- **WRONG framing (banned)**:
  - "10x cheaper than the competition" (not specific enough; "10x of what?")
  - "Crushing the OneTrust 1,060-layoff narrative" (named-company attack)
  - "Kill their business model" (war language)

## Factual claims — citation required

Every external claim must cite a public source. Internal dossier is NOT a citable source for external publication.

| Dossier claim | External citation |
|---|---|
| "78% of enterprises unprepared for EU AI Act" | IBM 2025 Global AI Adoption + McKinsey "State of AI 2025" |
| "EU AI Act deadline August 2, 2026" | EUR-Lex Reg (EU) 2024/1689, Article 113 |
| "OneTrust layoffs" | LinkedIn announcements + Reuters/Bloomberg if available |
| "13,000+ MCP servers, 97M downloads" | pulse MCP / mcp.so public metrics |
| "MCP governance gap" | Self-citation: OpenSSF Scorecard + keystone's `SECREVIEW.md` |

## Templates to audit (priority order)

1. **50 LinkedIn cold-email templates** in `clawd/mcp-marketplace/` — these are sent individually so are highest-risk for screenshot-tweets.
2. **100+ PR templates** in `clawd/mcp-marketplace/` — bulk-publish candidates, high-volume risk.
3. **Hacker News post (Jun 13)** — see [[hn-post-mcp-governance]] (drafting in progress).
4. **EU AI Act countdown blog post** — draft due Jul 4 launch.
5. **Press release (US launch, Jul 4)** — highest regulatory exposure.

## What to keep (not all dossier language is banned)

- Factual comparative language ("10x," "1000x," specific deltas) — fine.
- Technical architecture descriptions ("Byzantine fault tolerant," "cryptographic attestation") — fine.
- Regulatory dates + names ("EU AI Act 8/2/2026") — fine.
- Market size numbers with sources — fine.
- Customer testimonials (with permission) — fine.

## Process

1. **Before publishing**, paste the draft into a "rubric check" session.
2. Run the 3-question test on every paragraph.
3. Apply the vocabulary table.
4. Verify every factual claim has a citable public source.
5. If the rubric passes, publish. If not, revise.

## See also

- [[meok-deep-audit-2026-06-08]] P0-1 (the original audit item)
- [[meok-geo-strategy-2026-06-07]] "James Castle lesson" (the cautionary tale of fabricated authority)
- [[meok-fleet-monetization-blockers]] (regulatory exposure magnifies if revenue is going through FCA/SEC regulated channels)
