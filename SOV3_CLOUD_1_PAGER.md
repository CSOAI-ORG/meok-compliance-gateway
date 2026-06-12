# SOV3 Cloud — 1-pager (the MongoDB play)

> **Source**: `sov3_business_model.docx` §1.5 Stream 1 (referenced in `meok-deep-audit-2026-06-08.md` P2-7) + `GCP_DEPLOY.md` (existing Cloud Run foundation)
> **Year-1 target**: $400K ARR (40% of the $1M Year-1 mix per the corrected business-model breakdown)
> **Status**: Pre-build — Docker + Dockerfile exist; the multi-tenant managed product does not
> **Owner**: Infra team (not Claude-actionable in a single session)

## What SOV3 Cloud is

The **managed multi-tenant hosted version of the keystone**. The 76 flagships + 7 industry packs are the open-source substrate (MIT, self-host); SOV3 Cloud is the **SaaS** layered on top — sign up, get an API key, point your agent at `api.meok.ai/mcp`, no infra to run.

**The "MongoDB play"**: MongoDB Atlas won the NoSQL-database market by being the obvious managed option for an open-source server (MongoDB itself). SOV3 Cloud is the analogous play for compliance MCPs — the keystone + 76 flagships are the open-source substrate; SOV3 Cloud is the obvious "just give me an API key" layer.

## What SOV3 Cloud does (the product spec, 1 line per feature)

| Feature | Today (open-source keystone) | SOV3 Cloud adds |
|---|---|---|
| **Compute** | User runs `docker run` or `pip install` | Multi-tenant cluster, per-customer isolation |
| **Storage** | User's local FS / S3 | Managed Postgres (audit trail) + S3 (attestation evidence) |
| **Auth** | User's OIDC provider | Built-in OAuth (Google, Microsoft, Okta) + API key issuance |
| **Billing** | User's Stripe / x402 wallet | **4-tier SaaS billing** ($0/$29/$49/Enterprise) — the keystone's `pricing_tier` field is the SKU map |
| **Observability** | User's OpenSSF + own dashboards | Per-tenant logs, audit-trail UI, usage reports, alerts |
| **Compliance evidence** | User runs `meok-attestation-api` | **Auto-emission of signed attestations** per customer (the `proofof.ai/v/<cert_id>` flow but for the customer's compliance posture, not a single MCP call) |
| **x402 paywall** | User sets `X402_PAY_TO` | **MEOK's wallet receives**, MEOK takes 10% (the first revenue-share model in the fleet) |
| **SLA** | None (best effort) | 99.9% uptime, 48h support response, EU-only data residency by default |
| **Multi-region** | User deploys per region | 3 regions (EU, US, APAC) with failover |

## The 4 pricing tiers (Stream 1 in the business model)

| Tier | Seat Price | What's included | Target buyer |
|---|---:|---|---|
| **Free** | $0 | 1 user, 100 MCP calls/day, 1 flagship, community support | Hobbyists, students, evaluators |
| **Team** | $29/user/mo | 5 users, 10K calls/day, any 3 flagships, email support, basic audit trail | Small teams, startups |
| **Business** | $49/user/mo | 25 users, 100K calls/day, any 7 flagships, priority support, advanced audit trail, SAML SSO | Mid-market, regulated industries |
| **Enterprise** | Custom ($50K-$500K/yr) | Unlimited users, unlimited calls, all flagships, dedicated CSM, custom SLA, on-prem option, FedRAMP-ready | Fortune 500, government |

The 4 tiers are the **second pricing axis** (per-call x402 is the first). The keystone's `pricing_tier` + `seat_price_usd` + `monthly_floor_usd` fields in `gen-hive.py:DOMAIN_REGISTRY` are the SKU map for SOV3 Cloud. A user subscribing to the **Business tier** at meok.ai gets instant access to all 7 flagships in the `ai-gov-essentials-pack` (the Q3 LAUNCH wedge).

## What it takes to build (the engineering skeleton)

| Phase | Week | Deliverable | Effort |
|---|---:|---|---|
| 0 | W1-W2 | **Multi-tenant auth layer** — OAuth + API key issuance + per-tenant isolation in the keystone | 1 senior eng × 2 weeks |
| 1 | W3-W4 | **Managed Postgres + S3** — schema for audit trail, evidence, customer config; per-tenant encryption keys | 1 senior eng × 2 weeks |
| 2 | W5-W6 | **Stripe billing integration** — 4-tier SaaS subscription model + per-tenant quotas + overage | 1 eng × 2 weeks (mostly integration) |
| 3 | W7-W8 | **Multi-region Cloud Run deploy** — EU + US + APAC with Terraform + failover | 1 DevOps × 2 weeks |
| 4 | W9-W10 | **Customer dashboard** — usage reports, audit trail UI, attestation download | 1 frontend eng × 2 weeks |
| 5 | W11-W12 | **Beta with 10 customers** — early-access pricing ($99/mo flat), weekly office hours, bug-bash | 1 PM + 1 eng × 2 weeks |

**Total**: 12 weeks, 3-4 engineers. **Earliest ship date**: Q4 2026 (per master audit roadmap, post-merge refactor).

## What blocks it (gating dependencies)

1. **The 5 manual Nick-gated blockers** (Stripe Live Mode, Vercel, DNS, Resend, LinkedIn) — even the self-serve sign-up flow needs Stripe Live. Without this, **no subscription can bill**.
2. **Coinbase CDP wallet** for the x402 paywall go-live — without it, **the per-call revenue-share (MEOK's 10% cut) can't settle**.
3. **`gh repo create` × 28 hive-config repos** — the public discovery surface for self-serve sign-ups lives on the hive READMEs. Without them public, the funnel has no top.
4. **The 4 P0-build MCPs** — the EU AI Act / China / ETSI / Colorado deadline alignment is the urgency engine that drives sign-ups. Without them, SOV3 Cloud's value prop is "general compliance MCP" not "we cover Aug 2, 2026."
5. **The 6→3 / 15-merge refactor** (Q4 2026) — SOV3 Cloud's 4-tier pricing assumes the post-merge MCP names (`eu-ai-act-complete` etc.). Pre-merge, the SKU map is a 76-row table; post-merge, it's a 59-row table.

## What SOV3 Cloud is NOT (explicit non-goals)

- **Not a CRM / GRC platform replacement**. The keystone's differentiation is "compliance MCP layer for agents," not "OneTrust competitor with a UI." SOV3 Cloud is the API + dashboard, not a full GRC suite.
- **Not a single-tenant on-prem product**. On-prem is the **Enterprise** tier's "on-prem option" — not a separate product line. The keystone's MIT license + Dockerfile is the on-prem path for OSS users; SOV3 Cloud is the multi-tenant hosted path.
- **Not a marketplace**. The 6-channel distribution (Smithery, Glama, Pulse, MCP.so, Docker, .mcpb) is free + open. SOV3 Cloud is the **paid hosted SKU**, not a marketplace.
- **Not a managed service for the open-source flagships**. The 76 flagships stay MIT-licensed and self-host-friendly. SOV3 Cloud is the **opinionated managed distribution** of the same MCPs.

## Why this is the right product gap to fill

| Fact | Implication |
|---|---|
| 13 of 15 GRC competitors have zero MCP presence | The market is wide open for the "MCP layer" wedge |
| `$50B GRC market` (per master audit) by 2028, CAGR 13.6% | The market is large enough to support a $400K Y1 SaaS layer |
| `0/15 GRC competitors offer compliance-as-an-MCP` | No incumbent in this exact layer |
| 76 flagships are open-source | The 4-tier SaaS is the obvious monetization — same wedge as MongoDB Atlas / Elastic Cloud / Confluent Cloud |
| 165M x402 tx / $50M+ USDC processed (per `mcp-x402-bazaar-micropayments.md`) | Per-call micropayments are real; SOV3 Cloud's x402 cut is the second revenue rail |
| EU AI Act deadline is T-58 days (from 2026-06-08) | Urgency engine: 50,000 EU enterprises need this by Aug 2 |

## How this intersects the Q3 LAUNCH

SOV3 Cloud is **NOT** the Q3 LAUNCH deliverable — the LAUNCH is the open-source keystone + 4 P0-build MCPs + 6-channel distribution. SOV3 Cloud is the **Q4 SCALE** deliverable, riding on top of the LAUNCH. The keystone is the demo; SOV3 Cloud is the production deployment.

## Cross-references

- `GCP_DEPLOY.md` — the existing single-tenant Cloud Run deploy (the foundation SOV3 Cloud builds on)
- `PRICING.md` — the 4-tier SaaS pricing detail
- `MANUAL_BLOCKER_IMPACT_DASHBOARD_2026-06-08.md` — the 5 manual blockers that gate SOV3 Cloud
- `meok-deep-audit-2026-06-08.md` (memory) — P0-3, P0-5, P2-7 (the source of the SOV3 Cloud product gap)
- `sov3-mcp-master-audit-2026-06-08.md` (memory) — the 18-month roadmap that puts SOV3 Cloud in Q4 2026 SCALE
- `MERGE_PLAN_2026_Q4.md` — the 15-merge refactor that simplifies SOV3 Cloud's SKU map
- [[meok-fleet-monetization-blockers]] — the 5 manual blockers
- [[mcp-x402-bazaar-micropayments]] — the x402 state of play
