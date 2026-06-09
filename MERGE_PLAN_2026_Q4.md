# 15-Merge Consolidation Plan — Q4 2026

> **Source**: `sov3_mcp_master_audit.docx` § "Synergy Analysis" + § "Merge Candidates" (8 Jun 2026)
> **Quarter**: Q4 2026 (per master audit 18-month roadmap: SCALE phase)
> **Net reduction**: 82 MCPs → 59 MCPs (-28%, 23 eliminated across 15 merges)
> **Fleet refactor cost**: ~8 weeks engineering (1-2 engineers)
> **Prerequisite**: All 4 P0-build MCPs shipped (eu-ai-act-high-risk-classifier, china-ai-anthropomorphic, etsi-cabca-continuous-conformity, colorado-admt-compliance) per `REGULATORY_CALENDAR_2026-2027.md`

## Why merge (audit rationale, verbatim)

> "These five merges eliminate 9 redundant MCPs and address the most fragmented areas. The EU AI Act alone has 4 separate MCPs for what is one regulation. DORA has 3. Watermarking has 3. These are clear cases of horizontal fragmentation that confuse users and complicate maintenance."

The audit's 3 merge principles:
1. **Functional Overlap > 70%** — if two MCPs address the same regulation / workflow / technical concern, merge.
2. **Sub-tool Preservation** — merged MCPs expose original capabilities as sub-tools, not sub-MCPs. No functionality lost.
3. **Naming Convention** — descriptive compound names (`eu-ai-act-complete` vs `meok-eu-ai-act-art-13-ifu`).

## The 15 merges (by priority)

### HIGH priority — execute weeks 1-4 (5 merges, 9 MCPs eliminated)

| # | Merge Group | MCPs to merge | Result | Eliminated |
|---:|---|---|---|---:|
| 1 | EU AI Act Consolidation | `eu-ai-act` + `meok-eu-ai-act-art-13-ifu` + `meok-eu-ai-act-art-26-fria` + `meok-fria-generator` | `eu-ai-act-complete` | 3 |
| 2 | DORA Comprehensive | `dora` + `meok-dora-tlpt` + `dora-nis2-crosswalk` | `dora-complete` | 2 |
| 3 | CRA Consolidated | `cra` + `meok-cra-annex-iv` | `cra-complete` | 1 |
| 4 | NIS2 Consolidated | `nis2` + `meok-nis2-de-register` | `nis2-complete` | 1 |
| 5 | Watermarking Unified | `meok-watermark-attest` + `watermarking-authenticity` + `agent-content-watermark` | `ai-watermarking-suite` | 2 |

**Subtotal**: 5 merged, 9 eliminated. **Cumulative remaining: 73.**

### MEDIUM priority — execute weeks 3-6 (8 merges, 12 MCPs eliminated)

| # | Merge Group | MCPs to merge | Result | Eliminated |
|---:|---|---|---|---:|
| 6 | Agent Orchestration | `agent-orchestrator` + `agent-delegation` + `agent-handoff-certified` | `agent-orchestrator-pro` | 2 |
| 7 | Agent Commerce | `agent-commerce-payments` + `agent-negotiation` + `agent-x402-paywall` | `agent-commerce-suite` | 2 |
| 8 | Agent FinOps | `agent-cost-allocator` + `agent-token-budget` | `agent-finops-manager` | 1 |
| 9 | Blockchain Trust | `blockchain-ai` + `blockchain-verification` + `meok-attestation-verify` | `blockchain-trust-layer` | 2 |
| 10 | Healthcare Suite | `healthcare-ai-governance` + `healthcare-fhir` | `healthcare-ai-suite` | 1 |
| 11 | Aviation / Airspace | `drone-airspace-governance` + `airspace-monitor` | `drone-airspace-suite` | 1 |
| 12 | Transport / Tachograph | `haulage-uk-compliance` + `meok-tacho-audit` | `transport-compliance-suite` | 1 |
| 13 | AI Operations Center | `ai-ops` + `ai-incident-reporting` + `agent-incident-relay` | `ai-ops-center` | 2 |

**Subtotal**: 8 merged, 12 eliminated. **Cumulative remaining: 61.**

### LOW priority — execute weeks 5-6 (2 merges, 2 MCPs eliminated)

| # | Merge Group | MCPs to merge | Result | Eliminated |
|---:|---|---|---|---:|
| 14 | API DevTools | `api-docs-generator` + `api-tester` | `api-devtools-suite` | 1 |
| 15 | Crosswalk Engine | `dora-nis2-crosswalk`* + `csoai-governance-crosswalk` | `regulatory-crosswalk-engine` | 1 |

*NB: `dora-nis2-crosswalk` is already consumed into `dora-complete` in merge #2. The Crosswalk Engine merge re-evaluates whether to use the already-merged version or `csoai-governance-crosswalk` standalone.

**Subtotal**: 2 merged, 2 eliminated. **Cumulative remaining: 59.**

## Phasing & dependencies

```
Weeks 1-2: HIGH merges (1-5)         — 5 deliverables, 9 MCPs killed
Weeks 3-4: MEDIUM merges (6-13)      — 8 deliverables, 12 MCPs killed
Weeks 5-6: LOW merges (14-15)         — 2 deliverables, 2 MCPs killed
Weeks 7-8: Integration / regression  — 59-MCP fleet verified
```

**Dependencies**:
- **HIGH #1 (eu-ai-act-complete)** is the dependency for 2 industry packs (Healthcare, AI Gov Essentials) and the EU AI Act compliance P0-build. Cannot start until `eu-ai-act-high-risk-classifier-mcp` ships (Aug 2 deadline first).
- **HIGH #5 (ai-watermarking-suite)** is the dependency for `china-ai-anthropomorphic-mcp` (Jul 15 deadline first).
- **MEDIUM #7 (agent-commerce-suite)** includes `agent-x402-paywall` — coordinate with the keystone's x402 rollout (PR #5 + 4 flagship PRs already open). Cannot break the existing paywall path.

## Sub-tool migration pattern

Every merged MCP exposes the original tool surface as a sub-tool, prefixed with the source MCP name. Example for `eu-ai-act-complete`:

```python
# Before merge: 4 separate MCPs each exposing a different tool
eu-ai-act.quick_scan(system)
meok-eu-ai-act-art-13-ifu.generate_ifu(art13_data)
meok-eu-ai-act-art-26-fria.run_fria(system)
meok-fria-generator.build_fria_doc(...)

# After merge: 1 MCP with 4 sub-tools, same call shape
eu-ai-act-complete.quick_scan(system)
eu-ai-act-complete.generate_ifu(art13_data)
eu-ai-act-complete.run_fria(system)
eu-ai-act-complete.build_fria_doc(...)
```

The legacy package name is kept as a **deprecation alias** for 90 days (`meok-eu-ai-act-art-13-ifu` → `eu-ai-act-complete.generate_ifu`). After 90 days, the alias package is unpublished from PyPI; existing installs get a `DeprecationWarning` at import.

## Verification gate (week 8)

- All 59 surviving MCPs build + test green (per `scripts/regen-mcp-reg.py` health check).
- 15 deprecated aliases emit `DeprecationWarning` on import.
- OpenSSF Scorecard: 59 repos all ≥ 7/10 (current fleet mean = 4.04 per the audit, target = 7+).
- 6-channel distribution (Smithery, Glama, Pulse, MCP.so, Docker, .mcpb): all 59 repos listed with the 6 patched fields (per `MCP_REG_HEALTH_REPORT.md`).
- 7 industry packs pass integration tests (per the audit's Pack 1-7 definitions).

## Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Sub-tool breaking change for existing users | High | Medium | 90-day deprecation alias + migration guide per merge |
| Industry pack dependencies on merges not yet done | Medium | High | Phase HIGH merges first; pack framework ships after |
| OpenSSF Scorecard regression from 7+ → 4 in some repos | Medium | Medium | Per-merge OpenSSF gate; abort merge if score drops |
| `eu-ai-act-complete` collides with external `eu-ai-act-compliance-mcp` (the flagship) | Low | High | The flagship is the canonical one; rename merge result to `eu-ai-act-mcp-bundle` instead if collision |
| Loss of niche features during sub-tool migration | Medium | Low | Functional Overlap > 70% is the gate; preserve outliers as separate |

## Cross-references

- `sov3-mcp-master-audit-2026-06-08.md` (memory) — the 18-month roadmap + this merge plan
- `MASTER_AUDIT_INGESTION.md` — 1-page digest (internal-only)
- `REGULATORY_CALENDAR_2026-2027.md` — the 4 P0-build MCPs that must ship BEFORE Q4 merge execution
- `KIMI_COMPETITOR_VISUAL_AUDIT_BRIEF_v2.md` — the 13/15 GRC competitors with zero MCP context
- `MCP_REG_HEALTH_REPORT.md` — the 6-field server.json patch list (this merge should re-emit it for the 59 surviving repos)
- [[meok-hive-architecture-2026-06-07]] — the 28-hive mesh context
