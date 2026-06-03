# MEOK Fleet — 30-Day Action Plan

> Generated 2026-06-03 by the 5-phase fleet research workflow.
> Companion to `/tmp/final_report.md` (the full 12-section synthesis).
> Full data: `/tmp/cohort_assignments.json` + 13 × `/tmp/flagship_profiles/*.md` + `/tmp/wheel_audit.md` + `/tmp/long_tail_table.md` + `/tmp/axis[1-4]_*.md`.
> Cross-references: `/tmp/x402_full_report.md` (the parallel x402/OpenRouter competitive map).

---

## Day 0 (this week) — Ship the $0.001 x402 call

**Per the parallel x402 research (the Monday-morning action), the highest-leverage single move is to ship one billable call.** Everything else in this 30-day plan is scaffolding for that.

1. Set up a Coinbase CDP wallet (`MEOK_X402_RECEIVER`).
2. Wire `meok_x402.py` to a public endpoint with a `0.0001 USDC` paywall on the cheapest tool in the fleet (suggest `eu-ai-act-compliance-mcp:enforcement_status` or `meok-mcp-injection-scan-mcp:quick_scan`).
3. POST to it from a test MCP client, capture the onchain transaction hash.
4. Publish a 1-page memo: **"MEOK charges 0.0001 USDC — here's the proof"** — names every competitor and current pricing. Post to GitHub Discussions + a 5-line blog entry on the keystone repo.

**Why this is Day 0:** the consumer-discovery funnel leaks at the x402 conversion stage. Zero of the 13 flagships ship a working paywall today. Until one does, no flagship earns per-call USDC revenue, regardless of how many Smithery installs or PyPI downloads it has. The x402 facilitator fee on Base is $0.005 per wallet operation; on Solana it's $0 (facilitator sponsors gas). The theoretical minimum per-call price is $0.001.

---

## Week 1 — Fleet-wide engineering (the 5 features, in priority order)

| Day | Feature | Files touched | Effort | What it unlocks |
|-----|---------|---------------|--------|-----------------|
| 1-2 | **F3 — Pinned `requirements.txt`** (mcp==1.27.2 + uvicorn[standard]==0.48.0) | 13 × `requirements.txt` | ~1h | Reproducible builds; pre-positions 2026-07-28 spec freeze |
| 3-4 | **F4 — Real e2e CI step** (copy from gateway `tests/e2e_smoke.py`) | 13 × `.github/workflows/test.yml` | ~3h | Lifts fleet from "we hope it boots" to "CI proves it serves /mcp" |
| 5-7 | **F2 — Streamable-HTTP shim + canonical Dockerfile** (copy from keystone `http_server.py` + `Dockerfile`) | 10 missing flagships × 2 files | ~4h | Cloud Run, AWS AgentCore, Docker MCP Catalog listings become possible |

---

## Week 2 — Revenue + distribution

| Day | Action | Files touched | Effort |
|-----|--------|---------------|--------|
| 8-10 | **F1 — `meok_x402` paywall** on 3-4 high-value tools per flagship + `COST WARNING:` docstring prefix + `requirements-x402.txt`. Start with `eu-ai-act-compliance-mcp:audit_report` and `cra-compliance-mcp:sign_cra_attestation`. | 11 × `server.py` | ~5h |
| 11-12 | **F5a — Smithery/Glama `runtime: container` manifests** + `displayName`/`icon`/`tags` for the 7 broken flagships (legacy stdio schema) | 7 × `smithery.yaml` | ~2h |
| 13-14 | **F5b — `## Comparison vs <competitor>` README sections** for the 6 EU flagships (SEO wedge) | 6 × `README.md` | ~1h |

---

## Week 3 — Deprecation + cleanup

- Archive the 6 empty shells: `vulnerability-scanner`, `red-team-ops`, `threat-intelligence`, `policy-engine`, `incident-response`, `cloud-security`.
- **Fix or formally deprecate `hipaa-compliance-mcp`** (the `~/clawd/` import bug breaks every fresh install).
- **Fix the `instructions=` lie in `meok-governance-engine-mcp`** — currently claims "59 compliance tools" but ships 6. LLMs that read it during `initialize` plan for 59 and fail mid-task. Rewrite or archive.
- Yank the 3 broken shell+wheel repos from PyPI: `meok-cra-art14-reporter-mcp`, `meok-nis2-nl-register-mcp`, `meok-eu-ai-act-art-9-rms-mcp`.
- Fix the broken entry point in `iso-42001-ai-mcp` (`pyproject.toml` `[project.scripts]` points to a non-existent `server:main`).
- Fix the `api_key` positional-arg leak in 12 tools of `csoai-governance-crosswalk-mcp` (move to Context-based auth).

---

## Week 4 — Distribution + partner pitches

- **Submit to AWS AgentCore Marketplace (EU regions):** `eu-ai-act-compliance-mcp`, `cra-compliance-mcp`, `gdpr-compliance-ai-mcp`, `meok-mcp-injection-scan-mcp`.
- **Pitch Composio** for `csoai-governance-crosswalk-mcp` + `dora-compliance-mcp` toolkit partnerships.
- **Open Smithery issues** on the 19-pending flagships (per keystone `LISTING.md`: 19 submitted, 0 published since 2026-05-14).
- **Begin the 2026-07-28 spec-freeze pin bump.** Bump `mcp` in lockstep across `requirements-gateway.txt` + `constraints.txt` + every flagship's `requirements.txt`. Test against the keystone gateway's `tests/e2e_smoke.py`. Cutover by 2026-07-14.

---

## The 2 repos to PROMOTE (do first)

- **`eu-ai-act-compliance-mcp`** — 16 tools, 1.8 MB `data/regulations.db`, mature, only flagship that passes the keystone gateway's e2e smoke test. The EU AI Act SERP is fragmenting; OneTrust owns it but is enterprise-priced. SMB / self-serve DPO is wide open. Promote via Smithery + x402 Bazaar + AWS AgentCore.
- **`cra-compliance-mcp`** — 7 tools including the HMAC-signed `sign_cra_attestation`, the only MCP-native CRA tool. SERP is thin; the regulation only fully applies in Sep 2026 — we have ~14 months of uncontested window. Promote via x402 Bazaar at $1.00/call on `sign_cra_attestation`.

## The 3 repos to ABANDON this week

- **`soc2-compliance-ai-mcp`** — Vanta owns the SOC 2 SERP (15k+ customers, 300+ integrations, $7.5k-$12k/yr). Cannot rank. Stop investing in marketplace listings; keep on PyPI for direct "MCP SOC 2" searchers.
- **`hipaa-compliance-mcp`** — Vanta/Drata/Secureframe ship HIPAA as a checkbox add-on. Also has a hidden `~/clawd/meok-labs-engine/shared` import bug that breaks every fresh install. Fix the import or formally deprecate.
- **`meok-governance-engine-mcp`** — currently undeployable (lying `instructions=` + broken `~/clawd/` import + the `api_key` leaks already fixed in crosswalk). Rewrite before any other work, or archive.

---

## Per-flagship x402 paywall targets (Week 2, F1)

| Flagship | Tool to paywall | Price | Why |
|----------|-----------------|-------|-----|
| `eu-ai-act-compliance-mcp` | `audit_report` | $1.00 | Replaces a $5k+ consultant day |
| `cra-compliance-mcp` | `sign_cra_attestation` | $1.00 | Auditors will pay for a signed artifact |
| `csoai-governance-crosswalk-mcp` | `crosswalk_bridge` | $0.25 | 30-framework lookup is the wedge |
| `dora-compliance-mcp` | `get_dora_certificate` | $0.25 | Financial-entity WTP is high |
| `nis2-compliance-mcp` | `audit_article_21` | $0.50 | 72h breach notification is the billable event |
| `csrd-compliance-mcp` | `double_materiality_assessment` | $0.50 | Replaces a consultant day |
| `iso-42001-ai-mcp` | `audit_management_system` | $0.50 | Cert audit prep |
| `meok-mcp-injection-scan-mcp` | `signed_safety_report` | $1.50 | Higher than `sign_cra_attestation` because auditors pay for signed certs |
| `bias-detection-mcp` | `regulatory_check` | $0.50 | EU AI Act Art 10 lookup |
| `soc2-compliance-ai-mcp` | (abandoned) | — | Vanta owns SERP |
| `hipaa-compliance-mcp` | (abandoned) | — | Vanta/Drata own SERP |
| `gdpr-compliance-ai-mcp` | `dpia_generator` | $0.50 | EDPB-aligned DPIA is the billable event |
| `meok-governance-engine-mcp` | (rewrite or archive) | — | Currently undeployable |

Keep the cheapest tool in each flagship free (`quick_scan`, `classify_*`, `enforcement_status`) as the top-of-funnel wedge.

---

## The compounding bet

The 6 EU regulatory flagships (EU AI Act, GDPR, NIS2, DORA, CRA, CSRD) collectively cover a SERP set that Vanta/Drata/OneTrust have not yet consolidated. We have **~14 weeks** before the 2026-07-28 MCP spec freeze. Ship the 5 features above across the 6 EU flagships by 2026-07-14, then push to marketplace listings in parallel before the spec cutoff.

**The single line item in this plan that the x402 report identifies as the keystone is Day 0. Everything else is scaffolding for that one call.**
