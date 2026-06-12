# MEOK Regulatory Calendar — P0 Deadlines (2026-2027)

> **Source**: `sov3-mcp-master-audit-2026-06-08.md` + `sov3_mcp_master_audit.docx` Parts 1, 14, 15 + `sov3_state_of_empire.agent.final.md` + `sov3_july4_playbook.md`.
> **Scope**: 4 P0 regulatory deadlines that drive MEOK engineering priorities. **17 total deadlines ranked by urgency** in the master audit (4 P0 + 5 P1 + 8 P2).
> **Days to EU AI Act from 2026-06-08**: T-58.
> **Audit Part 1 reference**: `sov3_mcp_master_audit.docx` Part 1 "Regulatory Timeline at a Glance" (17 deadlines in critical-path timeline) + Part 14 "Emerging Standards" (ETSI TS 104 008 detail) + Part 15 "MCP Build Priority Matrix" (P0/P1/P2 definitions).

## The 4 P0 deadlines

| Date | Days from 2026-06-08 | Regulation | What it requires | MEOK coverage | Gap |
|---|---:|---|---|---|---|
| **2026-07-15** | T-37 | China Generative AI (interim measures) | Anthropomorphic / synthetic content labeling | None | Need `china-ai-anthropomorphic-mcp` |
| **2026-08-02** | T-55 | EU AI Act (high-risk obligations) | 78% of EU enterprises unprepared per Commission; Article 10 (data governance), Article 12 (logging), Article 13 (transparency), Article 30 (post-market monitoring) | keystone + `eu-ai-act-compliance-mcp` cover ~73% of Article 10 | 27% Article 10 gap; need `eu-ai-act-high-risk-classifier-mcp` |
| **2026-Q3** | T-90+ | ETSI TS 104 008 (EU consumer-grade AI) | Continuous conformity assessment for consumer AI products | None | Need `etsi-cabca-continuous-conformity-mcp` |
| **2027-01-01** | T-207 | Colorado ADMT (algorithmic decision-making tools) | Consumer-facing algorithmic decisions: impact assessments, disclosure, opt-out | None | Need `colorado-admt-compliance-mcp` |

## Engineering backlog (P0 builds)

| # | MCP server | Deadline | Effort | Build order |
|---|---|---|---|---|
| 1 | `eu-ai-act-high-risk-classifier-mcp` | Aug 2 (T-55) | ~2 weeks | NOW (Jun 8 - Jun 21) |
| 2 | `china-ai-anthropomorphic-mcp` | Jul 15 (T-37) | ~2 weeks | Parallel (Jun 8 - Jun 21) |
| 3 | `etsi-cabca-continuous-conformity-mcp` | Q3 (T-90+) | ~2 weeks | Wave 2 (Jun 22 - Jul 5) |
| 4 | `colorado-admt-compliance-mcp` | Jan 1 2027 (T-207) | ~2 weeks | Wave 3 (Jul 6 - Jul 19) |

Total engineering: ~8 weeks across 4 MCPs. Tight but achievable with the July 4 launch as the kickoff.

## 18-month revenue roadmap (per `sov3_state_of_empire.agent.final.md` § "18-Month Forecast")

| Quarter | Milestone | MRR target | P0 deadline coverage |
|---|---|---:|---|
| Q3 2026 | LAUNCH (4 P0 MCPs + x402 + 6-channel dist) | $10K → $200K | EU AI Act (Aug 2), China (Jul 15), ETSI (Q3) |
| Q4 2026 | SCALE (6→3 merge + ETSI + China) | $500K | All 3 Q3 deadlines |
| Q1 2027 | EXPAND (Colorado ADMT + 7 industry packs) | $1.2M | Colorado (Jan 1) |
| Q2 2027 | DOMINATE | $2.5M | Year-1 cumulative: $4.2M ARR |
| Q3 2027 | ENTERPRISE | $3.5M | All P0 deadlines shipped |
| Q4 2027 | STANDARD | $4M | Year-2 ARR run-rate: $48M |

## How this intersects the July 4 playbook

- **Phase 0 (Jun 8-14)**: EU AI Act infrastructure lockdown. The Aug 2 deadline is THE urgency engine for the launch.
- **Phase 1 (Jun 15-20)**: China Anthropomorphic content angles (any Llama derivative needs watermarking).
- **Phase 2 (Jun 21-27)**: EU AI Act high-risk classifier tool drop (free scanner).
- **Phase 3 (Jun 28-Jul 3)**: ETSI pre-announce; Colorado ADMT pre-announce.
- **Day 0 (Jul 4)**: 4 P0 MCPs in various build states. EU AI Act = shipped, China = shipped, ETSI = in QA, Colorado = in dev.

## Cross-references

- `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/sov3_july4_playbook.md` — Phase 0/1/2/3 actions tied to deadlines
- `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/sov3_state_of_empire.agent.final.md` — readiness score 63.7% → 91%
- `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/sov3_mcp_master_audit.md` — 4 P0 build specs
- `meok-compliance-gateway/MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — daily calendar
- `P0_BUILD_MCPS_2026-06-08.md` — the 4 P0-build MCPs (engineering briefs extracted from docx)
- `ROADMAP_18_MONTH_2026-2027.md` — the 18-month quarterly plan (this calendar is the urgency engine)
- `DISTRIBUTION_GAPS_2026-06-08.md` — the 6 channels these 4 P0s distribute through
- [[sov3-mcp-master-audit-2026-06-08]] — the master audit memory
- [[mcp-2026-07-28-stateless-spec]] — MCP 2026-07-28 spec migration affects how these 4 new MCPs will be built

---

## APPENDIX: All 17 deadlines ranked (from docx Part 1 critical-path timeline)

The master audit identifies 17 distinct regulatory deadlines in the 18-month horizon. The 4 P0s above are the highest-priority engineering targets. The remaining 13 are P1 (5) or P2 (8) and ship in Q3 2026 → Q2 2027 per `P0_BUILD_MCPS_2026-06-08.md`.

| # | Deadline | Days from 2026-06-08 | Priority | Confidence | MCP Coverage |
|---:|---|---:|---|---|---|
| 1 | **China AI Anthropomorphic** (effective) | 37 | **P0** | HIGH | None — must build (MCP-003) |
| 2 | **EU AI Act Annex III high-risk** (full app) | 55 | **P0** | HIGH (Omnibus may extend) | Partial — must build classifier (MCP-001) |
| 3 | EU CRA: Vulnerability/incident reporting | 95 | P1 | HIGH | Partial (CRA MCP exists) |
| 4 | EU AI Act Article 50 (deepfake/watermark) | ~150 | P1 | HIGH | Partial (watermarking MCPs exist) |
| 5 | EU CRA: Notified bodies operational | 186 | P2 | HIGH | Partial |
| 6 | **Colorado SB 26-189** (ADMT) | 207 | **P0** | HIGH (signed into law) | None — must build (MCP-002) |
| 7 | EU AI Act Article 6(1) Annex I (per Omnibus) | 420 | P1 | HIGH (Digital Omnibus) | None |
| 8 | EU AI Act: pre-Aug-2026 systems compliant | ~420 | P1 | HIGH | Partial |
| 9 | **ETSI TS 104 008 CABCA** (ongoing) | ongoing | **P0** | HIGH (enables 6-month lead) | None — must build (MCP-004) |
| 10 | SEC AI enforcement | ongoing | P1 | HIGH (active) | None — must build (MCP-005) |
| 11 | Australia mandatory guardrails (early 2026) | ongoing | P1 | MEDIUM (consultation phase) | None — must build (MCP-006) |
| 12 | Japan HAIP reporting (Hiroshima) | ongoing | P2 | HIGH (voluntary) | None |
| 13 | Automotive AI / UNECE type approval | ~420 | P1 | HIGH (multi-regulator) | None — must build (MCP-007) |
| 14 | UK AI Bill (Private Member's Bill) | ~540 | P2 | MEDIUM (govt taking different approach) | Partial (UK AI Bill MCP) |
| 15 | EU CRA FULL COMPLIANCE (CE marking) | 551 | P2 | HIGH | Partial |
| 16 | EU AI Act deferred Annex III (Omnibus) | ~560 | P2 | MEDIUM | Partial |
| 17 | EU: Commission guidelines on high-risk (extended) | ~240 | P1 | HIGH (extended) | Partial |

## APPENDIX: 4 P0 MCPs cross-reference

The 4 P0 deadlines map to 4 P0-build MCPs (per `P0_BUILD_MCPS_2026-06-08.md`):

| P0 Deadline | P0 MCP | Build start | MVP target | Effort |
|---|---|---|---|---|
| China AI (Jul 15) | `china-ai-anthropomorphic-compliance-mcp` (MCP-003) | Now | 1 Jul 2026 | 3 weeks |
| EU AI Act (Aug 2) | `eu-ai-act-high-risk-classifier-mcp` (MCP-001) | Now | 15 Jul 2026 | 4 weeks |
| ETSI CABCA (ongoing) | `etsi-cabca-continuous-conformity-mcp` (MCP-004) | Now | 1 Aug 2026 | 4 weeks |
| Colorado ADMT (Jan 1 2027) | `colorado-admt-compliance-mcp` (MCP-002) | 1 Jul 2026 | 1 Oct 2026 | 4 weeks |

**Total engineering**: ~15 weeks (parallelizable to ~8 weeks with 2 engs).

## APPENDIX: Why this calendar is the urgency engine for the launch

The 4 P0 deadlines (37 / 55 / ongoing / 207 days) are the **demand spikes** that drive:
- 5,000 free EU AI Act scanner completions (Q3 O3 target)
- $50K MRR from MCP-driven subscriptions (Q3 O4 target)
- 50,000 EU enterprises with high-risk AI use cases (TAM)
- $35M or 7% global turnover penalty = existential risk (the pain)
- Free EU AI Act risk scanner at meok.ai/scan = top-of-funnel (the wedge)

The 5 manual monetization blockers (Stripe, Vercel, DNS, Resend, LinkedIn per memory) gate the **distribution** of these 4 P0s, not the **build** of them. The builds can ship to PyPI + the 6 distribution channels (per `DISTRIBUTION_GAPS_2026-06-08.md`) on Nick's existing token.
