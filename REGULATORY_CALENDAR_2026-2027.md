# MEOK Regulatory Calendar — P0 Deadlines (2026-2027)

> **Source**: `sov3-mcp-master-audit-2026-06-08.md` + `sov3_state_of_empire.agent.final.md` + `sov3_july4_playbook.md`.
> **Scope**: 4 P0 regulatory deadlines that drive MEOK engineering priorities.
> **Days to EU AI Act from 2026-06-08**: T-58.

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
- [[sov3-mcp-master-audit-2026-06-08]] — the master audit memory
- [[mcp-2026-07-28-stateless-spec]] — MCP 2026-07-28 spec migration affects how these 4 new MCPs will be built
