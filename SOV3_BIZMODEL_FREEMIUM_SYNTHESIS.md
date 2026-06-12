# Freemium-to-Enterprise Conversion Playbook — MEOK Synthesis

> **Source**: `docs/seo-global-report/research/sov3_bizmodel/sov3_bizmodel_freemium.md` (Kimi, 743 lines, 7 benchmark companies: Figma, Notion, Linear, Vercel, GitHub, Supabase, Cloudflare)
> **Maps to revenue streams**: **Stream 1 (SOV3 Cloud) + Stream 2 (MCP App Store) — the conversion-funnel wedge**
> **Purpose**: extract the 7 freemium-mechanic patterns (free-tier limitations, conversion triggers, viral loops, enterprise upgrade paths) into keystone-specific pricing + funnel actions.
> **Companion**: `PRICING.md` (the 4-tier model); `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` (the strike protocol)
> **Rubric**: factual comparative, no war language. Banned vocabulary per `RUBRIC_EXTERNAL_COMMS.md`.

## 1. The 7 freemium benchmarks — keystone-applicable patterns

| Company | Free → Paid conversion | Enterprise penetration | **Keystone-applicable pattern** |
|---|--:|--:|---|
| **Figma** | 4% free→paid | 95% Fortune 500 | 3-file + 2-editor + 30-day version-history cap = the "second project triggers upgrade" lever. 88% gross margin. **Apply to:** SOV3's 100-calls/month free tier = the "second project" lever. |
| **Notion** | 5% free→paid | 80%+ of unicorns | "Block uploads >5MB on free" = the storage-as-paywall. **Apply to:** SOV3's HMAC-attestation count + log-retention days as the paywall. |
| **Linear** | 8% free→paid | 60% of YC startups | "Unlimited issues, but team >10 = paid" = the team-size cap. **Apply to:** SOV3's Team tier ($29/user/mo) triggers at team-size >5. |
| **Vercel** | 3% free→paid | 50%+ of Next.js sites | "Hobby plan = 100GB bandwidth/mo; Pro = $20/mo" = the bandwidth-as-paywall. **Apply to:** SOV3's x402 call-volume cap. |
| **GitHub** | 15% free→paid | 90%+ of Fortune 100 devs | "Free for individuals, Team $4/user/mo for org" = the org-vs-individual pivot. **Apply to:** SOV3's Business tier ($49/user/mo) triggers at "organization" usage, not individual. |
| **Supabase** | 6% free→paid | 40% of YC W24 | "Free 500MB database, then $25/mo for 8GB" = the database-size cap. **Apply to:** SOV3's 6-month log-retention cap on free. |
| **Cloudflare** | 2% free→paid | 20%+ of websites | "Free tier is generous; Workers Paid = $5/mo for 10M requests" = the request-volume cap. **Apply to:** SOV3's per-call x402 = the request-as-paywall. |

## 2. The 3 SOV3-specific actions (the freemium wedge)

### Action 1 — The 100-calls/month free tier = the Figma "second project" lever

**Source playbook**: Figma's 3-file free cap is the masterclass — the cap is **invisible until you need it**, then near-impossible to work around.
**MEOK claim**: SOV3's 100-calls/month free tier is the analogous cap. 100 calls is **invisible for an individual developer** (10 calls/day is plenty for exploration), but **impossible for a team** (a 5-person team doing 5 calls/day each = 750 calls/month). The cap is invisible-to-individual, impossible-for-team — exactly the Figma pattern.
**Tactical action**: the free tier is specced (per `PRICING.md`); the 100-call cap is wired. The GTM action is to **promote the free tier in 3 of the 28 hives** (meok.ai, csoai.org, councilof.ai) as the developer-funnel entry.
**Owner**: Eng (DONE) + Marketing. **Effort**: 0 hours; positioning.

### Action 2 — The org-vs-individual pivot (GitHub pattern)

**Source playbook**: GitHub's free tier is **per-individual**, not per-organization. The moment a developer invites a teammate, the org gets the Team $4/user/mo upsell. This is the **single highest-leverage conversion trigger** in the freemium playbook.
**MEOK claim**: SOV3's free tier is **per-wallet** (Coinbase CDP), not per-user. The moment a developer invites a teammate, the wallet needs to be **shared** (per-org) — which triggers the Team $29/user/mo tier.
**Tactical action**: the wallet-based billing is specced (per `meok_x402.py`); the per-org sharing is **not yet specced**. This is a Q3 2026 product gap; flag for engineering.
**Owner**: Eng (Q3 2026). **Effort**: 4-6 weeks engineering (org-wallet + per-seat metering).

### Action 3 — The 6-month log retention as the Supabase-database-size cap

**Source playbook**: Supabase's free tier = 500MB database; $25/mo = 8GB. The 16x jump is a **deliberate pain point** that triggers conversion.
**MEOK claim**: SOV3's free tier = **6-month log retention** (per EU AI Act Article 12 minimum). The Business tier = **24-month retention** with HMAC-chain verification. The 4x retention jump is the audit-driven conversion trigger (CISOs need 2-year retention for SOX/HIPAA/PCI).
**Tactical action**: the retention cap is specced (per the EU AI Act high-risk classifier spec). The 24-month retention tier is the Business tier's headline. The GTM action is to **document the audit-trail retention as a CISO-facing feature**.
**Owner**: Marketing (Nick). **Effort**: 2 hours of writing.

## 3. The 5 "do NOT do" rules (the freemium anti-patterns)

1. **Do NOT make the free tier too generous** — Cloudflare's 2% conversion is the warning sign. SOV3's 100 calls/month is the sweet spot.
2. **Do NOT make the free tier too stingy** — Vercel's 3% conversion shows the opposite failure. 100 calls/month is generous enough to be useful.
3. **Do NOT charge per-seat for the free tier** — the free tier is per-wallet, not per-seat. Per-seat metering on free kills the viral loop.
4. **Do NOT require credit card for the free tier** — Coinbase CDP wallet is the friction-free payment rail; no credit card = no friction.
5. **Do NOT promise "unlimited free forever"** — the Figma + Notion + Linear pattern: the free tier is a **time-limited funnel**, not a permanent state. SOV3's 100 calls/month is the time-limited funnel.

## 4. The 4-year freemium-conversion projection

| Year | Free-tier users | Conversion rate | Paid users | ARPU | ARR |
|---|--:|--:|--:|--:|--:|
| Y1 (2026) | 10,000 | 2% | 200 | $1,500/yr | $300K |
| Y2 (2027) | 50,000 | 3% | 1,500 | $2,000/yr | $3M |
| Y3 (2028) | 200,000 | 4% | 8,000 | $3,000/yr | $24M |
| Y5 (2030) | 1M+ | 5% | 50,000 | $5,000/yr | $250M |

The conversion rate compounds slowly (2% → 5% over 4 years) as the **trust** of the community builds. The 5% terminal rate matches Figma + Notion + GitHub benchmarks.

## 5. Cross-references

- `docs/seo-global-report/research/sov3_bizmodel/sov3_bizmodel_freemium.md` — full 743-line source
- `PRICING.md` — the 4-tier model + 28 x402 call prices
- `EU_AI_ACT_HIGH_RISK_CLASSIFIER_MCP_SPEC.md` — the Article 12 log-retention cap
- `meok_x402.py` — the Coinbase CDP wallet substrate
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — Phase 0-1 cover the free-tier launch
- `SOV3_FINANCIAL_MODEL_2026-2028.md` § Stream 1 + 2 — the conversion-funnel revenue

---

*Synthesized 2026-06-09 by Claude (Opus 4.8 session on `claude/review-changes-mkbcvckpl5ix3r03-MkKCu`). Source playbook is Kimi-derived third-party research; SOV3 applications are keystone-specific. The 2% → 5% conversion curve is a synthesis of 7 benchmark companies; SOV3-specific numbers require validation against actual pilot data.*
