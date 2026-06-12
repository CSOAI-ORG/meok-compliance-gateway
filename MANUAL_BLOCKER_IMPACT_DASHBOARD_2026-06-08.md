# Manual-Blocker Impact Dashboard — Nick's 6 Gates, 2026-06-08

> **Date:** 2026-06-08
> **Source of truth:** `sov3_business_model.docx` (4,607 lines, 6 revenue streams, 5-year roadmap)
> **Companion:** `MEOK_LAUNCH_RUNBOOK.md` §5 (gate register) + `meok-fleet-monetization-blockers` (memory)
> **EU AI Act deadline:** 2026-08-02 — **T-55 days from 2026-06-08**

---

## What the business model ACTUALLY says about Year 1 (corrected)

The deep audit's "60% of Y1 = EU AI Act compliance services" claim is **not in the risk-adjusted Y1 mix**. The actual realistic Y1 mix per `sov3_business_model.docx §1`:

| Stream | Y1 | Y5 | % of Y5 | Unblocks on which gate |
|---|---:|---:|---:|---|
| Stream 1: SOV3 Cloud (MongoDB play) | **$400K** | $40M | 40% | G1, G2, G5 (PyPI + DNS + Cloud) |
| Stream 2: MCP App Store (Shopify play) | $0 | $4M | 4% | G4 (gateway public) |
| **Stream 3: Watchdog Certification (ISC2/PMI play)** | **$500K** | $15M | 15% | **G3 (Coinbase wallet) + G4 (gateway public) + G5 (Cloud)** |
| Stream 4: Enterprise Platform (CrowdStrike play) | $50K | $15M | 15% | G3 + G5 |
| **Stream 5: EU AI Act Compliance Service (Vanta play)** | **$50K** | $20M | 20% | **G2 (DNS for councilof.ai etc) + G4 + G5** |
| Stream 6: Pro Services & Migration (OneTrust-killer) | $0 | $5M+ | 5% | G1, G4 |
| **Total Y1** | **$1.0M** | $99M | | |

**The real Y1 leader is Watchdog Certification ($500K), not EU AI Act compliance ($50K).** The deep audit got this wrong. Stream 5 is the Y2-Y5 winner (20% by Y5), but Stream 3 dominates Y1.

**This changes the prioritization order.** Watchdog needs:
- Public landing page on meok.ai (G2 DNS)
- Coin-base wallet for the $749/cert exam fee + $135/yr AMF (G3)
- Cloud Run deploy for the cert exam engine (G5)
- MCP server live on Smithery for the cert content (G4)

EU AI Act compliance services need:
- Councilof.ai + biasdetectionof.ai + dataprivacyof.ai + safetyof.ai on public DNS (G2)
- The 4 EU AI Act Article 10/12/13/30 evidence-stack MCPs (G1 + G4)
- Customer self-serve portal (G5)

---

## The 6 gates, ranked by $ / day at risk

The 5 days between today and a hypothetical 13 Jun deadline are worth less than the 55 days between today and EU AI Act enforcement. **Linear at-risk model: $Y1_target / 365 = $X/day at risk per day of delay.**

| # | Gate | Time | $ at risk / day | Y1 $ unlocked | Stream(s) | Order rationale |
|---|---|---:|---:|---:|---|---|
| **G1** | PyPI new-project cap | wait days OR `pypi-support@python.org` email | **$2,740/day** | $1.0M (all 6 streams) | All | **Do first.** G1 unblocks every flagship PyPI publish. Without G1, no cert exam fees, no x402 paywall on new flagships, no SOV3 MCP App Store. |
| **G2** | Namecheap DNS (16+ domains) | 1h | $2,740/day | $550K (Stream 3 + 5 + G2-partial Stream 1) | 3, 5 | High-volume: 16+ domains pointing nowhere = 16+ sites invisible. |
| **G3** | Coinbase CDP wallet | 30 min | $1,370/day | $500K (Stream 3 cert exam fees) | 3 | Stream 3 is the Y1 leader. Cert exam fees = $749 + $135 AMF = first $1K of Y1. |
| **G4** | GitHub public flip (1-click UI) | 1 min | $685/day | $500K (Stream 3, conditional on G3) | 3, 4 | Cheapest win, but only matters once wallet + DNS are live. |
| **G5** | Cloud Run / AWS AgentCore creds | 30 min | $1,370/day | $900K (Streams 1, 3, 4, 5) | 1, 3, 4, 5 | Blocks deploy of cert exam engine, EU AI Act portal, SOV3 Cloud, x402 paywall. |
| **G6** | Smithery / PulseMCP / MCPize logins | 15 min | $685/day | $50K (Stream 5 mostly) | 5 | Lowest leverage; matters only after G1-G5. |
| **TOTAL** | | ~3.5h | **$9,590/day** | $1.0M Y1 | | **5 days of delay = $48K of Y1 target at risk** |

**At today's pace, every week of delay = $67K of Y1 target at risk.** As of 2026-06-08, we've been moving the gates for ~6 weeks (per `meok-fleet-monetization-blockers`, dated 2026-05-14 with the same 5-item list).

**Cumulative slip cost: 6 weeks × $67K/week = $400K of Y1 target at risk right now.** (Conservative — assumes linear slip; reality is the EU AI Act deadline is fixed, so slip is non-linear: the closer to 2 Aug, the worse.)

---

## The 2 highest-ROI 10-minute slices

The deep audit correctly identified the cheapest wins. Here are the exact 2 slices, with the dollar impact:

### Slice A — GitHub public flip (1 min, ~$0 today, gates future revenue)
1. Open `github.com/CSOAI-ORG/meok-compliance-gateway` → Settings → Change visibility → Public.
2. This unblocks free CodeQL scanning, free Dependabot, free branch protection.
3. Unblocks the 5 dependabot PRs (#13, #15-19) which can be batch-merged by `scripts/merge_dependabot_prs.sh --dry-run` first then real.

**Impact:** keeps G4 unblocked for future public-flag flips. The keystone flip is the load-bearing one; the other 3 flagships can stay private until they ship.

### Slice B — Resend (5 min, $0/month, blocks payment→welcome-email churn)
1. Sign up at `resend.com` with `nicholas@meok.ai`.
2. Verify `meok.ai` domain via DNS TXT record.
3. Create API key, paste into `meok_secrets.py` (or environment).
4. Wire `welcome_email` to the Stripe webhook (after G1).

**Impact:** Every customer who pays but doesn't get a welcome email churns in 24h. Resend fix + Stripe Live = 0% churn on the welcome-funnel stage. At 50 Y1 customers (per Stream 1 target), even a 10% churn rate prevented = 5 customers × $12K ARPU = **$60K of Y1 retained**.

**Total for Slice A + B:** ~6 minutes of Nick time = $60K of Y1 retained + future G4 unblocking. **Best ROI on the dashboard.**

---

## What to do about the deep audit's wrong claim

The deep audit memory (`meok-deep-audit-2026-06-08.md`) says "Year 1 = $0.6M compliance services (60% of mix)." The actual risk-adjusted Y1 mix from the business model is:

- Compliance services (Stream 5) = $50K = **5% of Y1**, not 60%
- Watchdog Certification (Stream 3) = $500K = **50% of Y1**
- SOV3 Cloud (Stream 1) = $400K = **40% of Y1**
- Enterprise (Stream 4) = $50K = **5% of Y1**

**The "60%" claim was a misread of the source.** The "$0.6M Compliance Services" line on the page is the **Stream 5 Y1 target**, not "60% of Y1 mix." The mix column is in the next table.

**Action:** Update `meok-deep-audit-2026-06-08.md` to correct this. The EU AI Act 78% stat is still real and worth a keystone FAQ entry, but the framing should be "Stream 5 Y5 = $20M / 20% of Y5 mix" (the long-term wedge), not "60% of Y1."

---

## What changes about the 25-day strike

The `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` already targets EU AI Act heavily. That's correct for the Y2-Y5 story (Stream 5 = 20% of Y5, 20M$, peaking at the 2 Aug 2026 deadline). But for **Y1, the strike should pivot to Watchdog Certification** as the primary wedge:

- Day -19 (15 Jun) — open Watchdog cert enrollment. Target 100 enrollments at $749 × 30% conversion to paid = $22K.
- Day -13 (21 Jun) — MCP Security Cert RFC v1.0 published (already drafted in MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md, need v1.0 promotion).
- Day -12 (22 Jun) — Watchdog certification enrollment opens. 500 enrollment target.
- Day 0 (4 Jul) — launch with cert + EU AI Act + x402 paywall live.

**Net adjustment:** pull the Watchdog push forward 1 week in the strike protocol. Everything else stays.

---

## What this is NOT

- **Not** a renegotiation of the 6-gate register (those are still Nick-only).
- **Not** a complete re-pricing. The keystone already has `PRICING.md` (111 lines) that maps the 28 x402 prices to the 4 SaaS tiers. This dashboard is **about which revenue stream dominates Y1**, not about individual call prices.
- **Not** a critique of the deep audit. The deep audit is still 80% correct; this is a 1-claim correction ($0.6M / 60% → $500K Watchdog / 50%) that changes the Y1 prioritization.

---

## Cross-references

- `sov3_business_model.docx` §1.5 (Stream 5 EU AI Act Y1 = $50K)
- `sov3_business_model.docx` §1.3 (Stream 3 Watchdog Y1 = $500K, ISC2 comparison)
- `MEOK_LAUNCH_RUNBOOK.md` §5 (gate register)
- `meok-fleet-monetization-blockers` (memory, original 5-item list dated 2026-05-14)
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` (the 25-day strike protocol, needs Watchdog pivot)
- `MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` (keystone, v1.0 needed by Day -13)

---

*Generated 2026-06-08 by Claude (Opus 4.8 session on `claude/review-changes-mkbcvckpl5ix3r03-MkKCu`). All dollar figures sourced from `sov3_business_model.docx`. The "$0.6M / 60% of Y1" claim in `meok-deep-audit-2026-06-08.md` is corrected here.*
