# AgentAudit ←→ OpenMoE-BFT Empire Alignment

> This document exists so that every AI agent (Kimi, Opus, MiniMax, or future)
> working on this repo can see at a glance how AgentAudit maps to the Empire spec.
> **Source of truth:** `../research/OPENMOE_BFT_EMPIRE_SPEC_v1.0.md` (or the latest
> version in the project root / shared drive).

## Empire Layer Mapping

| Empire Layer | Layer Name | AgentAudit Module(s) | Status |
|---|---|---|---|
| 3 | OpenScore Safety Experts (14) | `safety_experts.py`, `openscore.py` | ✅ Live |
| 8 | Compliance Gateway (MEOK) | `compliance_matrix.py`, `server.py` | ✅ Live |
| 9 | Audit & Receipts (OpenScore) | `audit_trail.py`, `signet.py` | ✅ Live |
| 10 | Payment & Monetization (x402) | `x402.py`, `@paywalled` | ✅ Live |
| 11 | Interoperability (A2A + MCP) | `server.py`, `http_server.py`, `shadow_scanner.py` | ✅ Live |
| 2 | BFT Consensus Engine | `bft.py`, `cast_bft_vote`, `get_bft_status` | ✅ Live |

## The 14 Safety Experts

See `safety_experts.py::EXPERTS` for the canonical list.  Each expert has:
- `expert_id` (1-14)
- `name` — human-readable
- `source_repo` — upstream project we fork / integrate
- `domain` — compliance | security | governance | monetization | verification
- `regulation` — which regulation this expert enforces (if any)
- `a2a_field` — the A2A Agent Card field that carries evidence
- `checks` — compliance check IDs from `compliance_matrix.py`

### Quick Reference

| ID | Name | Domain | Regulation | A2A Field |
|---|---|---|---|---|
| 1 | EU AI Act Compliance | compliance | EU_AI_ACT | `metadata.riskAssessment` |
| 2 | NIST RMF Risk Scoring | compliance | — | `metadata.nistRmfScore` |
| 3 | DORA / NIS2 Incident Taxonomy | compliance | DORA | `metadata.ictRiskFramework` |
| 4 | Neurorights (GDPR Art 9) | governance | — | `metadata.neurorightsPolicy` |
| 5 | x402 Payment Validation | monetization | — | `metadata.x402Receipt` |
| 6 | MCP Tool Attestation | security | — | `metadata.mcpAttestation` |
| 7 | Blockchain Verification | verification | — | `metadata.blockchainAnchor` |
| 8 | Human-in-the-Loop Gate | governance | — | `metadata.hitlContact` |
| 9 | Red Team Automation | security | — | `metadata.redTeamReport` |
| 10 | Blue Team Defense | security | — | `metadata.blueTeamStatus` |
| 11 | Continuous Monitoring | security | — | `metadata.continuousMonitoring` |
| 12 | Fuzzing / Mutation | security | — | `metadata.fuzzingReport` |
| 13 | Autonomous Auditor | verification | — | `metadata.autonomousAudit` |
| 14 | Web Crawler / Extractor | verification | — | `metadata.webExtractionPolicy` |

## OpenScore Algorithm

Implemented in `openscore.py::openscore()`.

1. For each of the 14 experts, compute a 0.0–1.0 score:
   - Regulation-backed experts (1, 3) score by evidence presence on their `checks`.
   - Non-regulation experts (2, 4-14) score by evidence presence on their `a2a_field`.
2. Weighted average across all experts (regulation experts weight 1.0, others 0.5).
3. BFT adjustment:
   - If `bft.consensus_reached`: +0.1 bonus (capped at 1.0)
   - If BFT exists but no consensus: −0.2 penalty
4. Audit integrity: broken chain → overall × 0.5

## Signet Receipts

Implemented in `signet.py`.

- Ed25519 via `pynacl` (falls back to HMAC-SHA256 if unavailable)
- Every `AuditEntry` is signed on `append()` if a `SignetKey` is present
- Bilateral co-sign supported (pass `co_key` to `AuditTrail.append()`)
- Blockchain anchor field on every receipt (IPFS CID, Arweave txid, etc.)
- Offline verification: `verify_receipt(receipt, key)` → `bool`

## BFT Consensus

Implemented in `bft.py`.

- 2f+1 quorum where f = floor((n-1)/3)
- `cast_bft_vote(session_id, node_id, vote_hash)` creates or extends a round
- Consensus reached when ≥ quorum nodes vote for the same hash
- AI-enhanced leader election flag reserved for future use

## Cross-Agent Collaboration Notes

**If you are Kimi (architecture / long-context reasoning):**
- Reference this file + the Empire spec for any stack-design decisions
- The 14-expert model is the canonical governance layer
- BFT consensus wraps audit-trail entries, not the full agent protocol

**If you are Opus (implementation / coding):**
- Reference `safety_experts.py::EXPERTS` when adding new checks
- `openscore()` is the single scoring function — extend it, don't duplicate
- Signet uses lazy `pynacl` import; don't add heavy crypto deps at module load
- All new tools must be smoke-tested in `tests/test_agentaudit.py`

**If you are MiniMax (narrative / marketing):**
- Reference the README.md expert table for public-facing docs
- The keiretsu architecture is in the Empire spec Part 8
- Domain portfolio: openmoe.ai, councilof.ai, openscore.ai, meok.ai, proofof.ai

## Environment Variables for Agents

| Var | Purpose |
|---|---|
| `X402_ENABLED=1` | Turn on x402 paywall |
| `X402_PAY_TO` | EVM settlement address |
| `SIGNET_SEED` | Hex seed for deterministic Ed25519 key |
| `SIGNET_DID` | DID string for Signet receipts |

## How to Extend

1. **Add a new regulation** → append to `compliance_matrix.py::MATRIX`, map to existing expert(s)
2. **Add a new expert** → append to `safety_experts.py::EXPERTS`, assign next `expert_id`
3. **Add a new tool** → add `@mcp.tool()` in `server.py`, test in `tests/test_agentaudit.py`
4. **Add x402 to a tool** → `@paywalled(price="$0.10", tool_name="...")` + `ctx` param

## Tests

Run: `python -m pytest tests/test_agentaudit.py -v`

Current: **37 passing** (compliance matrix, 14 experts, Signet, BFT, audit trail,
OpenScore empty/partial/full cards, BFT bonus/penalty, all server tools).
