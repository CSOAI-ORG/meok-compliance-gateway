# Kimi — Competitor Visual Audit Brief (MEOK/CSOAI fleet)

> **Self-contained copy-paste brief.** Drop this into Kimi CLI / Kimi Agent
> with no further context. The brief is calibrated to the MEOK/CSOAI 28-hive
> MCP fleet on 8 Jun 2026.
>
> **Goal:** dispatch sub-agents to perform a *visual* audit of competitors
> across every MCP/A2A/ACP/PyPI distribution channel — what's on the page,
> what the page looks like, what works visually, what doesn't. Output: a
> structured comparison matrix + screenshots + recommendations for each
> flagship's listing/landing.

---

## 0. Context (1 paragraph)

We (MEOK AI Labs / CSOAI-ORG) ship a **28-hive MCP fleet** — 25 customer
flagships + 3 infrastructure hives — all open-source under MIT, all on PyPI,
all targeting cloud marketplaces + MCP registries. The Kimi audit (8 Jun 2026,
28MB, 247 footnotes) confirms our 4-tier pricing undercuts
OneTrust/Credo/Holistic/Vanta/Drata/Secureframe by 2-15x for SMB and 2-8x for
enterprise. But **we have not done a visual audit** of how our listings
*look* versus the competition. This brief commissions that audit. The
distribution channels that matter are listed below — every one has a visual
surface that determines whether an evaluator clicks "Install" or moves on.

---

## 1. The MEOK/CSOAI fleet (target baseline)

**28 hives** (25 customer + 3 infra). For visual audit purposes, focus on
the 4 flagship + 9 governance + 4 UK construction = **17 high-value hives**.
Skip the 5 flip/expire + 3 infra for the visual audit (they have different
go-to-market needs).

### Flagships (4)
| # | Hive | Domain | PyPI pkg | Repo |
|---|------|--------|----------|------|
| 1 | **meok.ai** | meok.ai | (private compliance portal) | CSOAI-ORG/meok-hive |
| 2 | **csoai.org** | csoai.org | (governance crosswalk) | CSOAI-ORG/csoai-hive |
| 3 | **proofof.ai** | proofof.ai | (attestation verifier) | CSOAI-ORG/proofof-hive |
| 4 | **cobolbridge.ai** | cobolbridge.ai | (COBOL→modern translator) | CSOAI-ORG/cobolbridge-hive |

### Governance (9)
accountabilityof.ai, agisafe.ai, asisecurity.ai, biasdetectionof.ai,
dataprivacyof.ai, ethicalgovernanceof.ai, safetyof.ai, transparencyof.ai,
councilof.ai

### UK construction (4)
grabhire.ai, muckaway.ai, planthire.ai, commercialvehicle.ai

### Vertical SaaS (3)
landlaw.ai, fishkeeper.ai, koikeeper.ai

### Flip/expire (5 — skip for visual audit)
diyhelp.ai, pokerhud.ai, loopfactory.ai, optimobile.ai,
socialmediamananger.ai (typo, let expire)

### Infra (3 — skip)
openmoe.ai, openMCP, meok-compliance-gateway

---

## 2. Distribution channels to audit (the visual surface)

For each channel, dispatch one sub-agent. Each sub-agent screenshots +
scores + returns a per-competitor breakdown. Be **factual and visual**, not
war-rhetoric (banned vocabulary per the rubric below).

### Channel A — **PyPI listings** (the install point)

**URL pattern:** `https://pypi.org/project/<pkg-name>/`

**For each competitor in section 3, audit:**
- README rendering (RST/MD), does the description render cleanly?
- Project URL links (Homepage, Repo, Docs) — present, broken, or absent?
- Classifiers — how many, do they include the right ones
  (License :: OSI Approved, Programming Language :: Python :: 3.11+, etc.)?
- Version cadence — last release date, frequency
- Download counts (last 30d / last 90d if available)
- Screenshots: top of project page, full description panel, sidebar

**For our 17 hives, audit the same fields** so we can compare side-by-side.
Our PyPI names follow `<domain-without-TLD>-mcp` (e.g.
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
  surface as of 2026.

**B3. Pulse MCP** — `https://www.pulsemcp.com/servers`
- Editorial-style listings. Note how competitors frame their value
  props (headline, sub-headline, "best for" tags).

**B4. MCP.so / mcpize** — `https://mcp.so` + `https://mcpize.com`
- Both are aggregated indexes. Note: which competitors are listed,
  which aren't, metadata quality.

**For all 4 registries:**
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

---

## 3. The competitor list (verified, from our 8 Jun deep audit)

Use these for the audit. **Don't expand the list without explicit
instruction** — we want a focused 17-competitor sweep, not a sprawling
"every MCP server" sweep.

### AI Governance / Compliance (the core competitive set)
1. **OneTrust** — `onetrust.com` — enterprise privacy/governance, $120-500K/yr
2. **Credo AI** — `credo.ai` — AI governance, $50-150K/yr
3. **Holistic AI** — `holisticai.com` — AI governance, $40-100K/yr
4. **Vanta** — `vanta.com` — SMB GRC, $10-30K/yr
5. **Drata** — `drata.com` — SMB GRC, $15-50K/yr
6. **Secureframe** — `secureframe.com` — SMB GRC, $12-40K/yr
7. **Sprinto** — `sprinto.com` — SMB GRC
8. **IBM OpenPages** — `ibm.com/products/openpages` — enterprise GRC
9. **ServiceNow GRC** — `servicenow.com/products/governance-risk-compliance`
10. **RSA Archer** — `rsa.com/products/archer` — enterprise GRC
11. **LogicGate Risk Cloud** — `logicgate.com`
12. **Fiddler AI** — `fiddler.ai` — XAI / explainability
13. **Arthur AI** — `arthur.ai` — AI observability
14. **Weights & Biases** — `wandb.ai` — ML ops
15. **Arize AI** — `arize.com` — ML observability

### MCP-native / A2A-native (the new entrants, post-2024)
16. **ModelContextProtocol (official)** — `modelcontextprotocol.io` + the
    `github.com/modelcontextprotocol` reference servers
17. **OpenAI's MCP integrations** — check OpenAI's published MCP server
    list (announced March 2025)
18. **Anthropic's reference servers** — `github.com/modelcontextprotocol/servers`
19. **Cloudflare's MCP servers** — `github.com/cloudflare/mcp-server-cloudflare`
20. **AWS Labs MCP** — `github.com/awslabs/mcp`

### Agent frameworks with MCP support
21. **LangChain MCP adapters** — `github.com/langchain-ai/langchain-mcp-adapters`
22. **CrewAI** — `crewai.com`
23. **AutoGen (Microsoft)** — `github.com/microsoft/autogen`
24. **Semantic Kernel (Microsoft)** — `github.com/microsoft/semantic-kernel`

**Visual audit the top 10-12 from each section** — don't try to do all
24, the data volume is too high. Pick the ones with the most overlap to
our 28-hive fleet (i.e., AI governance + MCP-native).

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
For each of channels A-I:
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
- **No war-rhetoric** in any output. See section 6.
- **No MCP server submissions** to any registry — that's a Nick-gated
  action. This brief only audits; it doesn't fix.
- **No code changes** to any of our 28 hive repos. Recommendations
  only.

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
- **Total audit:** 12 channels × 12 competitors = 144 audits × 7 min
  = ~17 hours of sub-agent time
- **Realistic with 4-8 parallel sub-agents:** 2-3 hours wall-clock
- **Output report writing:** 1-2 hours

**Total wall-clock budget: 4-5 hours.**

If you need to compress, drop the MCP-native list (Anthropic / OpenAI /
Cloudflare / AWS Labs) and focus on the 12 AI governance / GRC
competitors — those are the ones whose visual playbook matters most
for our pricing undercut claim.

---

## 10. Acceptance criteria (what "done" looks like)

- [ ] Every channel A-I has at least 5 competitor screenshots
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

*Brief generated 8 Jun 2026 by Claude (minimax-m3) on session
`claude/review-changes-mkbcvckpl5ix3r03-MkKCu`. Co-Authored-By: Claude
Opus 4.8 <noreply@anthropic.com>.*
