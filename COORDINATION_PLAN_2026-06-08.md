# MEOK Multi-TUI Coordination Plan — 2026-06-08

> **Purpose**: Single source of truth for 4 concurrent agent TUIs working the same repo.
> **Updated**: Each session start — check `git worktree list` + `git branch --show-current`
> **Owner**: Nick (human gatekeeper for account-gated actions)

---

## 🎯 Current Worktree Map (4 Active)

| # | Worktree Path | Branch | Status | Owner/Session | Primary Mission |
|---|---|---|---|---|---|
| **1** | `/Users/nicholas/meok-compliance-gateway` | `claude/review-changes-mkbcvckpl5ix3r03-MkKCu` | **THIS SESSION** — keystone gateway + GEO/AEO + pricing + RFC | Main Claude | Gateway hardening, GEO/AEO gen, pricing, MCP Security Cert RFC |
| **2** | `/private/tmp/agentaudit-cherry-test` | `feat/agentaudit-stage6-from-server` | AgentAudit post-Stage-6 delta (from crashed session) | Agent 2 | Recover crashed paywire tests (stash `241a5a3`), complete x402 test coverage |
| **3** | `/private/tmp/agentaudit-rescaffold-2026-06-08` | `agentaudit-rescaffold-2026-06-08` | Re-scaffold delta (8 Jun 05:51) | Agent 3 | Diff vs Stage 6, cherry-pick non-duplicate changes to Agent 2's worktree |
| **4** | `/Users/nicholas/meok-worktrees/ci-hardening` | `chore/ci-hardening` | Phase C verification scripts (OpenSSF, fuzz, scoreboard) | Agent 4 | Scorecard verification, fuzz tests, fleet scoreboard, CODEOWNERS/cosign |

---

## 📋 Branch Ownership & Merge Graph

```
gateway/main (58c9a38) ←── upstream source of truth
    │
    ├── feat/agentaudit-server (1931a30) ←── Stage 6 shipped, PRs #1-5 open
    │       │
    │       ├── feat/agentaudit-stage6-from-server (Agent 2) ←── paywire test recovery
    │       │
    │       └── agentaudit-rescaffold-2026-06-08 (Agent 3) ←── re-scaffold diff
    │
    ├── chore/ci-hardening (b4159af) ←── Agent 4, Phase C
    │
    └── claude/review-changes-mkbcvckpl5ix3r03-MkKCu (THIS, e0fbd73) ←── 7 unpushed commits + Phase 1-3 edits
```

**Merge sequence (Nick-gated)**:
1. `feat/agentaudit-server` → `gateway/main` (via PR #6, already merged per log)
2. `chore/ci-hardening` → `gateway/main` (Agent 4 completes Phase C)
3. `claude/review-changes-...` → `gateway/main` (THIS session, after Agent 2/3 resolved)
4. `feat/agentaudit-stage6-from-server` → `feat/agentaudit-server` (Agent 2 paywire tests)

---

## 🔒 Hard Coordination Rules (Non-Negotiable)

### Before ANY Edit
```bash
git branch --show-current
git status
# If branch ≠ expected, another session moved it → re-checkout your branch
```

### File Claim Protocol
| File Pattern | Owner | Claim Method |
|---|---|---|
| `scripts/gen-geo.py`, `scripts/gen-hive.py` | **THIS session** | Already editing — check MEMORY.md |
| `agentaudit/agentaudit/*.py` | Agent 2 (cherry-test) | Claim in Agent 2's MEMORY.md |
| `.github/workflows/scorecard.yml`, `fuzz/*` | Agent 4 (ci-hardening) | Claim in Agent 4's MEMORY.md |
| `meok_x402.py`, `http_server.py` | Shared (gateway core) | **Never edit same file concurrently** — claim in MEMORY.md |
| `FLEET_BASE.md`, `LISTING.md` | THIS session | Template authority |

### Memory Claim (One Line Per Session)
```bash
# Each session writes to ~/.claude/projects/-Users-nicholas-meok-compliance-gateway/memory/MEMORY.md
# Format: - [Session X] <branch> — <task> — <files touched>
```

### Account-Gated Actions (NICK ONLY)
| Action | Gate | Nick Time |
|---|---|---|
| Merge PRs (gateway #5, #6, 52 OpenSSF, 5 agentaudit) | GitHub UI | 15 min |
| PyPI publish (agentaudit) | `twine` + 2FA | 5 min |
| GHCR package visibility flip (4 flagships + agentaudit) | GitHub Packages UI | 10 min |
| Coinbase CDP wallet setup (X402_PAY_TO) | Coinbase dashboard | 30 min |
| Vercel deploy (28 hives) | Vercel dashboard | 30 min |
| Namecheap DNS (28 domains) | Namecheap dashboard | 45 min |
| Resend (email) | Resend dashboard | 10 min |
| LinkedIn auth (scheduled posts) | LinkedIn developer | 15 min |

---

## 📅 Session-by-Session Execution Plan

### **SESSION 1: THIS (Keystone Gateway + GEO/AEO + Pricing + RFC)**
**Branch**: `claude/review-changes-mkbcvckpl5ix3r03-MkKCu`
**Worktree**: `/Users/nicholas/meok-compliance-gateway`
**Status**: ✅ Phase 0-3 COMPLETE (see EXECUTION_PLAN_2026-06-08.md)

| Phase | Task | Status |
|---|---|---|
| 0 | Kimi bundle move, working tree clean, agentaudit→worktree, merge gateway/main, pre-push verify | ✅ DONE |
| 1-A | 10-20x undercut FAQ (meok.ai, csoai.org, transparencyof, councilof) | ✅ DONE |
| 1-C | EU AI Act 78% unprepared stat (meok.ai) | ✅ DONE |
| 1-D | pricing_tier wiring verify | ✅ DONE |
| 2-A | Re-price 4 calls (proofof $10, councilof $5, csoai $3, safetyof $5) | ✅ DONE |
| 2-B | Certification Authority queries (councilof, biasdetectionof, transparencyof) | ✅ DONE |
| 2-C | Valuation/asking_price on 5 flip candidates | ✅ DONE (already in registry) |
| 2-D | Keystone GEO query (meok-compliance-gateway) | ✅ DONE |
| 3-A | MCP Security Cert Standard v0.1 RFC stub | ✅ DONE |
| 3-C | OpenSSF badges on keystone + 5 flagships | ✅ DONE |

**Remaining for THIS session**:
- [ ] Push 7 unpushed commits (G1 — Nick go)
- [ ] Stage agentaudit/ deletion commit (clean working tree)
- [ ] Verify gen-geo.py output for all 28 hives has new FAQs/differentiators

---

### **SESSION 2: Agent 2 — AgentAudit Paywire Test Recovery**
**Branch**: `feat/agentaudit-stage6-from-server`
**Worktree**: `/private/tmp/agentaudit-cherry-test`
**Mission**: Complete x402 paywire test coverage (crashed 6 Jun 13:54)

| Task | Source | Status |
|---|---|---|
| Recover `conftest.py` from stash parent `241a5a3` | Stash | 🔄 PENDING |
| Recover `test_x402.py` from stash parent `241a5a3` | Stash | 🔄 PENDING |
| Add 2 more paid tools (compliance_gap_analyser, expert_quorum_consult) | New | 🔄 PENDING |
| Add spending report test (x402_spending_report) | New | 🔄 PENDING |
| Run full test suite (81 tests) | Validate | 🔄 PENDING |
| Push to `feat/agentaudit-server` as new commits | Sync | 🔄 PENDING |

**Dependencies**: None (isolated worktree)
**Nick gate**: Merge resulting PR to `feat/agentaudit-server`

---

### **SESSION 3: Agent 3 — Re-scaffold Diff & Cherry-pick**
**Branch**: `agentaudit-rescaffold-2026-06-08`
**Worktree**: `/private/tmp/agentaudit-rescaffold-2026-06-08`
**Mission**: Diff re-scaffold vs Stage 6, move non-duplicate changes to Agent 2

| Task | Detail | Status |
|---|---|---|
| `diff agentaudit/` vs `/private/tmp/agentaudit-cherry-test/agentaudit/` | File-by-file | 🔄 PENDING |
| Identify non-duplicate changes (signet.py +60b, shadow_scanner.py +5b, server.py +223b, AGENTS.md new, README.md +730b) | Compare SHAs | 🔄 PENDING |
| Cherry-pick non-duplicate changes to Agent 2's worktree | `git cherry-pick` or manual apply | 🔄 PENDING |
| Discard re-scaffold worktree after sync | Cleanup | 🔄 PENDING |

**Dependencies**: Agent 2's worktree must be ready to receive cherry-picks
**Nick gate**: None (internal sync)

---

### **SESSION 4: Agent 4 — CI Hardening Phase C**
**Branch**: `chore/ci-hardening`
**Worktree**: `/Users/nicholas/meok-worktrees/ci-hardening`
**Mission**: Complete OpenSSF Scorecard Phase C + fuzz tests + fleet scoreboard

| Task | Detail | Status |
|---|---|---|
| Add hypothesis fuzz tests for gateway parsers | `fuzz/test_gateway_parsers.py` | 🔄 PENDING (started at f763885) |
| Phase C verification scripts | `scripts/verify_scorecard.py` | 🔄 PENDING (started at b4159af) |
| Fleet scoreboard generation | `FLEET_SCORE.md` update | 🔄 PENDING |
| CODEOWNERS + cosign keyless image signing | `.github/CODEOWNERS` + workflow | 🔄 PENDING |
| x402 property tests | `tests/test_x402_properties.py` | 🔄 PENDING |
| Push branch, open PR to gateway/main | Sync | 🔄 PENDING |

**Dependencies**: None (isolated worktree)
**Nick gate**: Merge PR to `gateway/main` → triggers fleet propagation

---

## 🚀 Critical Path to Revenue (Priority Order)

| # | Blocker | Session | Nick Action | Impact |
|---|---|---|---|---|
| **1** | **Stripe Live Mode** | — | Dashboard toggle | Enables real payments on all 28 hives |
| **2** | **Vercel deploy 28 hives** | Agent 1 (gen-geo output) | Vercel import + deploy | Live sites for Smithery/AWS/x402 |
| **3** | **Namecheap DNS 28 domains** | — | DNS records → Vercel/GCP | `https://<hive>.ai` serving |
| **4** | **Coinbase CDP wallet (X402_PAY_TO)** | Agent 2 (paywire tests ready) | Coinbase dashboard | x402 revenue + Bazaar auto-list |
| **5** | **Merge gateway #5 (x402 + hardening)** | Agent 4 (Phase C done) | GitHub UI merge | x402 paywall active on flagships |
| **6** | **Merge 5 agentaudit PRs** | Agent 2 (paywire done) | GitHub UI merge | AgentAudit x402 live |
| **7** | **Merge 52 OpenSSF PRs** | Agent 4 (Phase C done) | GitHub UI merge | Fleet 7.0+ scorecard |
| **8** | **GHCR visibility flip (5 packages)** | — | GitHub Packages UI | Public marketplace images |

**Daily ARR cost of delay**: ~$11K/day (per meok-deep-audit-2026-06-08 P0-4)

---

## 🔄 Daily Sync Protocol (Run at Session Start)

```bash
# 1. Check worktree status
git worktree list

# 2. Check branch status
git -C /Users/nicholas/meok-compliance-gateway branch --show-current
git -C /private/tmp/agentaudit-cherry-test branch --show-current
git -C /private/tmp/agentaudit-rescaffold-2026-06-08 branch --show-current
git -C /Users/nicholas/meok-worktrees/ci-hardening branch --show-current

# 3. Check for uncommitted changes on other worktrees
git -C /private/tmp/agentaudit-cherry-test status --short
git -C /private/tmp/agentaudit-rescaffold-2026-06-08 status --short
git -C /Users/nicholas/meok-worktrees/ci-hardening status --short

# 4. Read other sessions' MEMORY.md claims
cat ~/.claude/projects/-Users-nicholas-meok-compliance-gateway/memory/MEMORY.md

# 5. Update THIS session's claim
echo "- [Session 1] claude/review-changes-... — Phase 3 polish + push prep — gen-geo.py, gen-hive.py, README.md" >> ~/.claude/projects/-Users-nicholas-meok-compliance-gateway/memory/MEMORY.md
```

---

## 📁 File Ownership Matrix (Prevent Conflicts)

| File/Directory | Primary Owner | Can Edit | Notes |
|---|---|---|---|
| `scripts/gen-geo.py` | Session 1 | Session 1 only | GEO/AEO generator |
| `scripts/gen-hive.py` | Session 1 | Session 1 only | 28-hive registry |
| `scripts/add_openssf_badge.py` | Session 1 | Session 1 + Agent 4 | Agent 4 may extend |
| `http_server.py` | Session 1 | Session 1 + Agent 4 | Gateway core — claim first |
| `meok_x402.py` | Session 1 | Session 1 + Agent 2 | x402 logic — Agent 2 tests it |
| `agentaudit/agentaudit/*.py` | Agent 2 | Agent 2 only | AgentAudit core |
| `agentaudit/tests/*.py` | Agent 2 | Agent 2 only | AgentAudit tests |
| `.github/workflows/scorecard.yml` | Agent 4 | Agent 4 only | Scorecard CI |
| `.github/workflows/codeql.yml` | Agent 4 | Agent 4 only | CodeQL CI |
| `.github/workflows/fleet-e2e.yml` | Agent 4 | Agent 4 only | Fleet E2E CI |
| `fuzz/*` | Agent 4 | Agent 4 only | Hypothesis fuzz tests |
| `FLEET_BASE.md` | Session 1 | Session 1 only | Template authority |
| `LISTING.md` | Session 1 | Session 1 only | Deploy playbook |
| `PRICING.md` | Session 1 | Session 1 only | Public pricing |
| `MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` | Session 1 | Session 1 only | New RFC |
| `AGENTS.md` | All | All (append only) | Coordination board |

---

## 🚨 Conflict Resolution Escalation

1. **File collision detected** (write fails "modified since read")
   - STOP → `git status` → identify other session's worktree
   - Coordinate via this plan or direct message
   - Never force-write (`git checkout --ours` etc.)

2. **Branch switched under you**
   - `git branch --show-current` shows wrong branch
   - Another session ran `git checkout` on shared checkout
   - **Fix**: `git checkout <your-branch>` — never assume tree state

3. **Duplicate work discovered**
   - Two sessions editing same logical component
   - Compare outputs → merge best parts → one session owns going forward
   - Update this plan's ownership matrix

4. **Test failures from other session's changes**
   - Run tests in YOUR worktree only
   - Don't assume other worktrees are green
   - Report cross-worktree breakage in MEMORY.md

---

## 📌 Next Session Handoff Checklist

### For Session 1 (THIS → Next)
- [ ] Push 7 unpushed commits (after Nick G1 go)
- [ ] Stage agentaudit/ deletion as separate commit
- [ ] Verify all 28 hives regenerate cleanly with new FAQs
- [ ] Update MEMORY.md with final state

### For Session 2 (Agent 2 → Next)
- [ ] All paywire tests passing (81 total)
- [ ] Pushed to `feat/agentaudit-server` branch
- [ ] PR opened for Nick review

### For Session 3 (Agent 3 → Next)
- [ ] Diff complete, non-duplicate changes identified
- [ ] Changes cherry-picked to Agent 2's worktree
- [ ] Re-scaffold worktree deleted

### For Session 4 (Agent 4 → Next)
- [ ] Phase C scripts complete + tested
- [ ] Fuzz tests passing
- [ ] PR opened to `gateway/main`

---

## 📞 Communication Channels

| Channel | Purpose | Participants |
|---|---|---|
| This document (`COORDINATION_PLAN_2026-06-08.md`) | Master plan, source of truth | All sessions + Nick |
| `~/.claude/projects/-Users-nicholas-meok-compliance-gateway/memory/MEMORY.md` | Session claims, live status | All sessions |
| `AGENTS.md` (in each worktree) | Coordination rules, open work board | All sessions |
| Nick direct | Account-gated decisions, merges, spend | Nick only |

---

## 🎯 Success Criteria (All Sessions Green)

- [ ] **Session 1**: 7 commits pushed, agentaudit/ cleaned, gen-geo/gen-hive verified, RFC published
- [ ] **Session 2**: 81 AgentAudit tests passing, paywire coverage complete, PR to feat/agentaudit-server
- [ ] **Session 3**: Re-scaffold diff complete, non-duplicate changes merged to Agent 2, worktree deleted
- [ ] **Session 4**: Phase C complete, PR to gateway/main, fleet scoreboard updated
- [ ] **Nick**: 5 manual blockers done, 58 PRs merged, 5 GHCR packages public, 28 Vercel deploys live

---

*Generated 2026-06-08 by Session 1 (claude/review-changes-mkbcvckpl5ix3r03-MkKCu). Update at each session start.*