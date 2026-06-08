# MEOK Pricing — Public Surface

> **Status**: P0-5, [[meok-deep-audit-2026-06-08]]
> **Owner**: Nick (LinkedIn / cold-email outbound team)
> **Audience**: prospect + partner + analyst

## Two SKUs, not one

MEOK offers **two orthogonal pricing axes** for the same product. Both can be used together; the right choice depends on the customer's deployment pattern.

| | x402 micro-call | SaaS subscription |
|---|---|---|
| **Use case** | Agent-to-agent, pay-per-call, low-volume | Human dashboard, many seats, ongoing monitoring |
| **Pricing unit** | $0.01 - $10.00 per call | $29 - $49 per user/month, custom $50-200K/yr |
| **Minimum spend** | $0 (free tiers 0-100 calls/day) | $99/mo (Team) to $4,900/mo (Business) |
| **Payment rail** | x402 / Coinbase CDP | Stripe (Live mode pending — Nick-gated) |
| **Examples** | "Run a bias-detection check once" | "Compliance dashboard for 50 risk officers" |
| **Buyer** | AI agent / engineering team | CCO / DPO / Head of AI Governance |

## The 4 SaaS tiers (Stream 1 of the business model)

| Tier | Price | Floor | What you get |
|---|---|---|---|
| **Freemium** | $0 | $0 | 1-100 calls/day on free MCPs; open-source code; community support |
| **Team** | $29/user/mo | $99-499/mo | Full MCP access, MCP Pro features, email support, SSO (SAML/OIDC) |
| **Business** | $49/user/mo | $1,499-4,900/mo | Team + audit logs, custom MCP branding, SLA 99.9%, priority support, dedicated CSM |
| **Enterprise** | Custom | $50-200K/yr avg | Business + on-prem / private cloud, custom integrations, named TAM, quarterly business reviews |

## The 28-hive x402 micro-call pricing

This is the per-call pricing for each of the 28 hives. For agent-to-agent traffic and API integration.

| Hive | $ / call | Free tier | SaaS tier |
|---|---:|---|---|
| meok.ai (compliance portal) | $0.05 | 1/day | Business |
| csoai.org (governance) | $3.00 | 0/day | Enterprise |
| proofof.ai (attestations) | $10.00 | 1/day | Business |
| cobolbridge.ai (COBOL bridge) | $2.00 | 0/day | Enterprise |
| accountabilityof.ai | $0.50 | 1/day | Team |
| agisafe.ai | free | 100/day | Freemium |
| asisecurity.ai | $0.30 | 1/day | Business |
| biasdetectionof.ai | $0.10 | 3/day | Team |
| dataprivacyof.ai | $0.20 | 1/day | Business |
| ethicalgovernanceof.ai | free | 5/day | Freemium |
| safetyof.ai | $0.40 | 1/day | Team |
| transparencyof.ai | $0.75 | 1/day | Business |
| councilof.ai (BFT) | $1.00 | 0/day | Business |
| grabhire.ai (UK haulage) | $0.05 | 1/day | Team |
| muckaway.ai | $0.05 | 1/day | Team |
| planthire.ai | $0.10 | 1/day | Team |
| commercialvehicle.ai | $0.15 | 1/day | Business |
| landlaw.ai | $0.50 | 3/day | Business |
| fishkeeper.ai | free | 100/day | Team |
| koikeeper.ai (premium koi) | $1.00 | 0/day | Team |
| diyhelp.ai | free | 100/day | Freemium (FLIP CANDIDATE) |
| pokerhud.ai | free | 0/day | Freemium (FLIP CANDIDATE) |
| loopfactory.ai | free | 10/day | Freemium (FLIP CANDIDATE) |
| optimobile.ai | free | 10/day | Freemium (FLIP CANDIDATE) |
| socialmediamananger.ai | free | 0/day | Expire at renewal |
| openmoe.ai (BFT inference) | $0.01 | 10/day | Micro-Pay |
| openMCP (audit) | free | 5/day | Freemium |
| meok-compliance-gateway | $0.05 | 1/day | Business |

## The 10-20x undercut (factual comparative)

| Competitor | Their price | MEOK equivalent | Undercut |
|---|---|---|---|
| OneTrust | $120-500K/year for full governance suite | $4,900/mo Business tier ($58,800/yr) | 2-8x cheaper |
| IBM OpenPages | $250K+/year enterprise license | $50-200K/yr Enterprise | 1.5-5x cheaper |
| ServiceNow GRC | $200K+/year | $50-200K/yr Enterprise | 1-4x cheaper |
| Credo AI | $50-150K/year | Business tier | 1-3x cheaper |
| Holistic AI | $40-100K/year | Business tier | 1-2x cheaper |
| Vanta (SMB) | $10-30K/year | Team tier | 2-6x cheaper |
| Drata (SMB) | $15-50K/year | Team tier | 3-15x cheaper |
| Secureframe (SMB) | $12-40K/year | Team tier | 2-8x cheaper |
| Laika (compliance) | $20-60K/year | Business tier | 1-3x cheaper |
| Anecdotes (GRC) | $80-200K/year | Enterprise tier | 1-3x cheaper |
| LogicGate (GRC) | $50-150K/year | Enterprise tier | 1-3x cheaper |
| Hyperproof (GRC) | $30-80K/year | Business tier | 1-2x cheaper |

**Honest framing**: MEOK is **2-20x cheaper** at the **enterprise tier**. At the per-call level (x402), MEOK is **1000-10000x cheaper** for low-volume customers because the per-call model is not what legacy GRC platforms sell at all.

## EU AI Act urgency: why this matters now

The **EU AI Act** enters enforcement on **August 2, 2026** (EUR-Lex Reg (EU) 2024/1689, Article 113). Independent surveys (IBM 2025, McKinsey 2025) find **78% of enterprises are unprepared**. MEOK's Turnkey EU AI Act Compliance Package is the fastest path to compliance:

- **Articles 10** (data + model bias) → biasdetectionof.ai ($0.10/call or $299/mo Team)
- **Article 12** (incident logging) → accountabilityof.ai ($0.50/call or Business)
- **Article 13** (transparency) → transparencyof.ai ($0.75/call or Business)
- **Article 30** (GDPR + AI Act records) → dataprivacyof.ai ($0.20/call or Business)
- **CSOAI Watchdog AI Safety Certification** → councilof.ai ($1.00/call or Business, $49/user/mo)

## The 5 manual blockers (per [[meok-fleet-monetization-blockers]])

| Blocker | Status | Impact |
|---|---|---|
| Stripe Live Mode | ❌ Pending Nick | No real payments |
| Vercel deploy | ❌ Pending Nick | No live sites |
| Namecheap DNS | ❌ Pending Nick | No `https://<hive>` serving |
| Resend (email) | ❌ Pending Nick | No transactional emails |
| LinkedIn auth | ❌ Pending Nick | No scheduled posts |

**Until these are flipped, the pricing above is "list price" not "transaction price."** Customers can be onboarded on Stripe TEST mode + a manual invoice.

## See also

- [[meok-deep-audit-2026-06-08]] P0-5 (the original audit item)
- [[meok-geo-strategy-2026-06-07]] (the 90-day revenue path targeting £83K MRR)
- [[meok-fleet-monetization-blockers]] (the 5 manual gates)
- `scripts/gen-hive.py` (the live registry source of truth)
- `RUBRIC_EXTERNAL_COMMS.md` (how to write about this without getting sued)
