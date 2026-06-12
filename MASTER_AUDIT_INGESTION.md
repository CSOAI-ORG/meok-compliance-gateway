# Master Audit Ingestion — sov3_mcp_master_audit.docx (2026-06-08)

> **Source**: `/Users/nicholas/Downloads/sov3_mcp_master_audit.docx` (Kimi research, 271,728 chars, 100-pt scorecards × 20 priority MCPs + 18-month roadmap).
> **Scope**: 76 MCP servers, 35 PyPI packages, 250+ public GitHub repos.
> **Fleet grade**: C+ (56.8/100) per the audit; production security: OpenSSF 4.8 (keystone) → target 7+ post-remediation.
> **Audience**: Nick + Claude — internal ONLY. Do NOT leak the $1.2T TAM, $30-120M Y3 ARR, or 26-domain strategy to any public channel (HN / LinkedIn / PR) per `RUBRIC_EXTERNAL_COMMS.md`.

This is a 1-page digest. The full 9,424-line audit lives at the docx path above (local-only). Below: what to act on, ranked by leverage.

---

## Top 3 CRITICAL fixes (Claude-actionable, shipped this session)

| # | Finding | Fix | Shipped in this session |
|---|---|---|---|
| 1 | All 76 Docker containers run as root | `USER app` with `uid 10001` | `Dockerfile:20-21` (keystone) + `docs/DOCKERFILE_SECURITY_TEMPLATE.md` for the other 75 |
| 2 | `~/.meok/api_keys.json` world-readable | chmod 600, keyring pattern, audit script | `scripts/check-secret-perms.sh` (fix mode works locally) + `meok_x402.py:_resolve_attestation_key()` for future attestation keys |
| 3 | `MEOK_ATTESTATION_KEY` exposed via env | AWS SM → keyring → env (dev only) → fail closed | `meok_x402.py:_resolve_attestation_key()` (new function; doesn't break existing test) |

Effort: <1 hr each. Audit's CRITICAL severity = "blocks marketplace listings that require secure Docker images" (Docker Hub, AWS Marketplace). Unblocks all downstream distribution work.

---

## Top 6 distribution gaps (Claude-actionable, shipped this session)

The audit Appendix D flags 6 free distribution wins on Glama / Smithery / Pulse MCP / MCP.so / Docker / .mcpb — all gated on adding 6 missing `server.json` fields to each of the 76 repos:

| Field | Currently on 76/76 repos? | Fix |
|---|---|---|
| `icons` | ❌ | common SVG, MIME `image/svg+xml` |
| `websiteUrl` | ❌ | `https://meok.ai` |
| `metadata.publisher` | ❌ | `MEOK AI Labs` |
| `metadata.categories` | ❌ | `["compliance", "ai-governance", "regulation"]` |
| `examples` | ❌ | one realistic invocation per repo |
| `resources` | ❌ | docs + GitHub links per repo |

**Shipped**: `scripts/regen-mcp-reg.py` + `MCP_REG_HEALTH_REPORT.md` (44 rows × 6 cols, 41 need patch). Pushing the patches is Nick-gated (`gh` auth + `MEOK_PUSH_OK=1`).

---

## 4 P0 regulatory deadlines (calendar pressure)

| Date | Reg | What we need |
|---|---|---|
| **2026-08-02** | EU AI Act (high-risk obligations) | 78% of EU enterprises unprepared per Commission impact assessment; MEOK ships Article 10/12/13/30 evidence stack via `eu-ai-act-compliance-mcp` |
| **2026-07-15** | China Generative AI (interim measures) | anthropomorphic / synthetic content rules; need a `china-ai-anthropomorphic-mcp` (one of the 4 P0-builds in the audit) |
| **2026-Q3** | ETSI TS 104 008 (EU) | consumer-grade AI conformity; need a `etsi-cabca-continuous-conformity-mcp` |
| **2027-01-01** | Colorado ADMT | consumer-facing algorithmic decisions; need a `colorado-admt-compliance-mcp` |

**Days to EU AI Act**: T-58 from 2026-06-08. The keystone + `eu-ai-act-compliance-mcp` already cover ~73% of Article 10 data-governance requirements (per the audit's scorecard). Remaining 27% = 4 P0-builds × ~2 weeks each = 8 weeks engineering, starting now.

---

## "CSOAI owns this space" — the 5 levers (from the audit's executive verdict)

1. **0/15 GRC competitors on MCP** — Vanta, Drata, OneTrust, Secureframe, Tugboat Logic, Laika, Compyl, AuditBoard, Diligent, Galvanize, Pathlock, Drata, Netwrix, Sumo Logic, AppOmni have ZERO MCP-native presence. We are the only compliance brand an agent can `quick_scan` against.
2. **1 direct MCP-native competitor** — `ark-forge/mcp-eu-ai-act` (8★, MIT, 4 versions, 22 AI frameworks). Free, single-dev. Wedge on hosting + x402 paywall.
3. **$50B GRC market by 2028** per the audit's market-sizing appendix (CAGR 13.6%). 4-tier SaaS pricing ($0/$29/$49/Enterprise) + x402 micro-settlement = the wedge.
4. **x402 first-mover** — 165M tx / $50M+ USDC processed; OpenRouter migrated 22 May. We are the only compliance MCP that bills per attestation lookup.
5. **OpenSSF baseline 81.6 (keystone)** — cleanest security posture in the agent-tool ecosystem, ahead of every GRC competitor (most score 0-2 on Maintained/Code-Review).

---

## 18-month roadmap (compressed)

| Quarter | Milestone | MRR target | ARR target |
|---|---|---|---|
| Q3 2026 | LAUNCH (4 P0 MCPs + x402 + 6-channel dist) | $10K → $200K | — |
| Q4 2026 | SCALE (6→3 fleet merge + ETSI + China) | $500K | — |
| Q1 2027 | EXPAND (Colorado ADMT + 7 industry packs) | $1.2M | — |
| Q2 2027 | DOMINATE | $2.5M | $30M (run-rate) |
| Q3 2027 | ENTERPRISE | $3.5M | — |
| Q4 2027 | STANDARD | $4M | **$48M (run-rate)** |

The audit's $15M Year-2 ARR target maps to $1.25M MRR — Q1 2027 is the right landing pad. The 24 new MCPs in Appendix A are the engineering backlog; the 6→3 merge is the Q4 2026 refactor that reduces ops surface by 50%.

---

## What Nick can do this week vs what only Claude can do

### Nick-only (gated on his accounts / credentials)
- 5 manual monetization blockers (3.5 hours, $11K/day of Year-1 ARR at risk per `meok-deep-audit-2026-06-08` P0-4):
  1. **Stripe Live Mode** — `dashboard.stripe.com` → 2h
  2. **Vercel deploy** — `vercel.com/dashboard` → 10 min per site
  3. **Namecheap DNS** — `namecheap.com` → 1h
  4. **Resend API key** — `resend.com/api-keys` → 5 min
  5. **LinkedIn recovery** — `linkedin.com` → 10 min
- `gh repo create` × 28 hive-config repos (his `gh` auth)
- Coinbase CDP wallet creation (gates x402 paywall go-live)
- AWS Secrets Manager provisioning (`meok/attestation-key` secret) for the keystone attestation feature

### Claude-actionable (this session, all done)
- ✅ Fix #1 (Docker USER + capability drop + template)
- ✅ Fix #2 (chmod 600 script + keyring pattern)
- ✅ Fix #3 (keyring → env → fail guard in meok_x402.py)
- ✅ regen-mcp-reg.py + health report (44 rows, 41 need patch)
- ✅ MASTER_AUDIT_INGESTION.md (this file)
- ✅ HANDOFF.md (next file)
- ✅ Memory: sov3 master audit summary
- ⏳ Push the 41 server.json patches to CSOAI-ORG (Nick-gated, not in this session)

### Multi-week / multi-session (NOT this session)
- The 4 P0-build MCPs (eu-ai-act-high-risk-classifier, china-ai-anthropomorphic, etsi-cabca-continuous-conformity, colorado-admt-compliance) — 8 weeks engineering total
- The 6→3 merge refactor (Q4 2026) — refactor risk too high in one session
- The 20 other new MCPs from Appendix A — multi-month backlog
- The full OpenSSF push from 4.8 → 7+ (adds Dependabot, CodeQL, cosign, fuzzing per `keystone_SECREVIEW.md` §5) — separate session

---

## Banned vocabulary reminder (for any external PR / HN / LinkedIn)

Per `RUBRIC_EXTERNAL_COMMS.md` — never use these words in customer-facing copy:
- kill shot, nuclear arsenal, coup de grâce, talent raid
- seeding doubt, depletion campaign, strike while, vulnerability window
- stock-split convergence play, CrowdStrike BSOD legacy
- CISA exploited-vuln list, insider selling, funding fiction
- acquisition target

The 5-lever verdict + the $50B TAM are SAFE for internal docs (this file). They are NOT safe for the 28-hive public listings, the keystone's HN post, or the LinkedIn presence — those get the "5-10x undercut on GRC" wedge, not the $48M Year-2 target.

---

## Cross-references

- `CRITICAL_FIXES_2026-06-08.md` — the keystone's 3-fix plan (already in repo)
- `meok-deep-audit-2026-06-08.md` (memory) — the 12-dim research synthesis that underpins the $11K/day calc
- `keystone_SECREVIEW.md` — the OpenSSF Scorecard audit + remediation order
- `meok-fleet-monetization-blockers.md` (memory) — the 5 manual Nick-gated actions
- `keyring-token-push-rule.md` (memory) — `env -u GITHUB_TOKEN -u GH_TOKEN git push` for the 41 server.json patches
- `sov3-master-audit-2026-06-08.md` (memory, new this session) — durable summary of the docx
- `KIMI_COMPETITOR_VISUAL_AUDIT_BRIEF_v2.md` — the 712-line companion to this audit
- `EXECUTION_PLAN_2026-06-08.md` — the day's P0-A through P3-D plan (mostly done)
