# 6-Channel Distribution Gap Matrix — CSOAI-ORG MCP Fleet

> **Source**: `sov3_mcp_master_audit.docx` Part 7 "Distribution Channel Audit" + Appendix C "Distribution Channel Priorities" (8 Jun 2026)
> **Scope**: 11 distribution channels audited, 318 GitHub MCP repos, 76 officially registered MCP servers
> **Headline**: "CSOAI-ORG's MCP servers have minimal presence on third-party distribution channels" — 1 of 76 on Glama, 0 on Smithery, 0 on Pulse MCP, 0 on MCP.so, 0 on Docker MCP Catalog, 0 on AWS Marketplace, 0 on Claude Desktop Extensions

## Tier 1: Must-Be-Present (All 6)

| Marketplace | Current Status | Target | Priority Actions | What Blocks It |
|---|---|---|---|---|
| **Smithery.ai** (2,800+ tools) | **Not listed** | 20+ MCPs | CLI installer config, `smithery.yaml` for each | `gh` is Nick-gated |
| **Glama.ai** (32,634+ servers) | **1 of 76** (`a2a-governance-bridge-mcp` only) | 20+ MCPs | Registry submission, quality score optimization | `gh` is Nick-gated |
| **MCP.so** (21,969+ servers) | **Partial** | 20+ MCPs | Full directory listing, featured placement | Submit-only (low effort) |
| **PulseMCP** (14,310+ servers) | **Not listed** | 20+ MCPs | Daily-updated directory submission (editorial curation) | Need to pitch editorial |
| **Cursor Directory** | **Not listed** | 10+ MCPs | Cursor-specific plugin packaging | Submit-only (low effort) |
| **GitHub (awesome-mcp-servers)** | **PR submitted** | Listed | Maintain PR, add governance category | Maintain in-flight |

## Tier 2: Strategic Growth (3 emerging)

| Marketplace | Why Target | Timeline | What Blocks It |
|---|---|---|---|
| **AWS Marketplace** | Enterprise procurement path | Q4 2026 | AWS seller registration (account work) |
| **Google Cloud Marketplace** | GCP customer access | Q1 2027 | GCP seller registration (account work) |
| **Azure Marketplace** | Microsoft ecosystem access | Q1 2027 | Azure seller registration (account work) |

## Tier 3: Future (2 nascent)

| Marketplace | Why Target | Timeline | What Blocks It |
|---|---|---|---|
| **Docker Hub (verified)** | Container distribution | Q2 2027 | Per-repo Docker publishing (engineering) |
| **npm registry** | Developer-native install | Q3 2027 | Per-repo npm packaging (engineering) |

## Channel-by-channel fix plan (what Claude can do without Nick)

| Action | Channel | Effort | Owner | Status |
|---|---|---|---|---|
| Generate per-repo `smithery.yaml` (already part of the MCP-reg schema) | Smithery | 1 PR/15min × 20 = 5h | Claude | Script-ready, not run |
| Generate per-repo Glama submission payload | Glama | 1 PR/15min × 20 = 5h | Claude | Script-ready, not run |
| Fill out PulseMCP editorial pitch (security, EU AI Act, councilof.ai positioning) | PulseMCP | 1 editorial form | Nick | Not started |
| Submit MCP.so listings (20 forms) | MCP.so | 1 PR/15min × 20 = 5h | Claude | Not started |
| Build `.mcpb` bundles for the 6 flagships (keystone + 5) | Claude Desktop | 1 PR × 6 = 1 day | Claude | Not started |
| Build per-repo Docker images with USER/cap-drop | Docker Hub | 1 PR × 76 = 2 weeks | Claude (templates), Nick (publish) | Templates only |
| Update awesome-mcp-servers PR with governance category | GitHub | 1 PR | Claude | In-flight |

## 5 highest-ROI channel moves (Nick's checklist)

In order of cost-per-impression:

1. **Glama (32K+ servers)** — single submission, biggest audience. Generate the payloads here first.
2. **Smithery (2.8K+ tools)** — CLI-driven, lowest-friction submission. `smithery.yaml` is already in our `server.json` schema.
3. **MCP.so (22K+ servers)** — community-driven, easiest to seed via cross-posts.
4. **PulseMCP (14K+ servers)** — editorial curation; the EU AI Act Aug 2 2026 angle is a hook.
5. **Claude Desktop `.mcpb`** — one-click install, highest per-user conversion (developers).

## Why this matters (the audit's framing)

> "Critical Finding: CSOAI-ORG's MCP servers have minimal presence on third-party distribution channels. While PyPI coverage is strong (~35 packages), the organization is effectively invisible on Smithery, Pulse MCP, and MCP.so — the three largest MCP directories after Glama."

PyPI is the only channel with real traction (2,687 downloads/mo for `eu-ai-act-compliance-mcp`). The 5 missing channels (Smithery, Glama, MCP.so, PulseMCP, Cursor Directory) collectively reach 72,000+ MCP listings and most of the agent-developer audience. **The fix is mostly Claude-side (generate the submission payloads) plus 1-2 hours of Nick time (Glama/Smithery/MCP.so account creation).**

## Cross-references

- `sov3-mcp-master-audit-2026-06-08.md` (memory) — durable summary
- `MASTER_AUDIT_INGESTION.md` — 1-page digest (internal-only)
- `MCP_REG_HEALTH_REPORT.md` — the 6-field server.json patch list (the foundation for the Smithery/Glama schemas)
- `SOV3_CLOUD_1_PAGER.md` — the SOV3 Cloud tier where these channels become the funnel
- [[meok-cross-post]] — the cross-post CLI (`meok-cross-post --smithery --glama --mcpso --pulse`) that can be extended to cover all 6
- [[meok-hive-architecture-2026-06-07]] — the 28-hive mesh that gives each `.ai` domain a per-channel landing surface
