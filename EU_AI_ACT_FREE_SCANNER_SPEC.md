# EU AI Act Free Scanner — Specification

> **Asset**: `meok.ai/eu-check` — a 5-minute risk-classification tool.
> **Status**: Spec only. No code. Awaiting Phase 2 build (Jun 21-27 per `REGULATORY_CALENDAR_2026-2027.md`).
> **Source-of-truth**: This file. Cross-references are sibling docs in this keystone.

## 1. The opportunity

The EU AI Act high-risk obligations go live on **August 2, 2026** — T-55 from today (2026-06-08) and T-26 from the planned July 4 launch. Per the European Commission, **78% of EU enterprises are unprepared**. That is the addressable market: a population that knows it is exposed, has 55 days to act, and is currently shopping for tooling that will not take 9 months to deploy (cf. OneTrust's published 2.5-9 month implementation cycles; the 76-server MCP master audit puts OneTrust's "EU AI Act bolt-on" status as "immature workflows" with "generic templates require substantial customisation").

**The funnel role.** The scanner is the **freemium gate** of the meok.ai compliance funnel. The flow is `meok.ai/eu-check` (free, no login) → HMAC-signed PDF attestation + email capture → Business tier checkout at **$49/user/month** (per `PRICING.md`). The four tiers in the keystone pricing are: Freemium ($0, 1-100 calls/day on free MCPs), Team ($29/user/mo, $99-499/mo billed), Business ($49/user/mo, $1,499-4,900/mo billed), Enterprise (custom, $50-200K/yr avg). The scanner is the entry point that converts the Freemium visitor into a Business-tier trial, then into a paid customer.

**Why "free" matters.** Enterprise customers will not share their AI system inventory with a vendor they have not yet tried. The 5-question screener is the price of trust — a 5-minute commitment before a single line of inventory is typed. Without it, the funnel starts at the much harder "give us $49 and tell us your stack" pitch. The 78% unprepared statistic is a buying signal that is being wasted on a sales-driven funnel: those buyers are self-motivated to find a tool, but they will not tolerate a sales call before they know whether the tool understands their problem. The scanner is the self-serve answer to that demand.

**The 27% gap.** This asset closes the **27% Article 10 coverage gap** between the keystone + `eu-ai-act-compliance-mcp` (~73%) and full Article 10 conformance, by giving prospective customers a no-friction entry point that demonstrates value before any contract is signed. The keystone + flagship cover the audit and penalty-calculator surface, but they do not give a customer a way to discover their own risk class in under five minutes. The scanner is that front door — and the conversion event the rest of the keystone monetizes.

**Why now.** The urgency engine is the deadline itself. Every week of delay loses 4-7% of the addressable market to a competitor that ships first, to a Big 4 consulting engagement ($50K-$400K), or to "do nothing and pay the fine." The Big 4 floor for EU AI Act compliance is $50K (Holistic AI's "policy alignment engine" tier) and the OneTrust enterprise list is $120-500K/year. The keystone's Business tier is $49/user/month — two orders of magnitude cheaper, and the only one with a free, self-serve front door. The scanner is the asset that makes the price advantage visible in the buyer's first session.

## 2. The 5 questions

Each question is a yes/no binary, surfaced one-per-screen, no jargon. The back-end calls the MCP for the real classification logic (see §5) — the questions are only the front-end splitter.

**Q1. Does your AI system make decisions that produce legal effects on a person?**
Examples shown: denying a loan, terminating employment, denying a public benefit, revoking a visa.
- **Triggers**: Article 6 + Annex III (high-risk use cases involving legal effects on individuals).
- **Outcome**: Yes → classifies as `high-risk`. No → continue to Q2.

**Q2. Does it interact with humans in a way that could materially influence behavior?**
Examples shown: chatbots that steer financial decisions, recommendation systems that exploit vulnerabilities, AI-generated nudges targeted at minors.
- **Triggers**: Article 5(1)(a) — prohibited manipulative/deceptive practices; Article 50 — limited-risk transparency obligations.
- **Outcome**: Yes → classifies as `limited-risk` (with a flag for Article 5 review if the practice crosses into exploitation). No → continue to Q3.

**Q3. Is it used for biometric identification, emotion recognition, or critical infrastructure?**
Examples shown: real-time remote biometric ID in public spaces (Art. 5(1)(h) prohibited in most contexts), emotion recognition in workplace/education (Art. 5(1)(f) prohibited), AI controlling water/gas/electricity/traffic.
- **Triggers**: Article 5 prohibited categories + Annex III (critical infrastructure).
- **Outcome**: Yes → classifies as `prohibited` if it matches Art. 5(1)(h) live biometric ID, or `high-risk` if Annex III critical infrastructure. No → continue to Q4.

**Q4. Is the system used in employment, education, credit, immigration, or law enforcement?**
Examples shown: CV-screening, university admissions, credit scoring, visa processing, predictive policing.
- **Triggers**: Annex III §3-§7 (high-risk by sector).
- **Outcome**: Yes → classifies as `high-risk`. No → continue to Q5.

**Q5. Are you deploying this in the EU, or selling to EU-based customers?**
Examples shown: EU-domiciled company, EU end-users, EU data subjects.
- **Triggers**: Article 2 territorial scope.
- **Outcome**: Yes → `out-of-scope` becomes impossible (it is in scope); the previous 4 questions are re-evaluated. No → `out-of-scope` (but show an informational banner: "If you onboard EU customers or expand to the EU, this changes").

## 3. Risk classification output

The scanner maps answers to exactly one of four buckets, per the EU AI Act risk pyramid:

| Outcome | Triggering article(s) | Compliance obligations | Next-step CTA |
|---|---|---|---|
| **Prohibited** | Article 5(1) (e.g. 5(1)(a) manipulative, 5(1)(h) live biometric ID) | Withdraw from EU market immediately. Notify relevant authorities. No lawful path under the Act. | "**Stop deploying.** Talk to our compliance team — `meok.ai/contact`. Enterprise tier only." |
| **High-risk** | Article 6 + Annex III (Q1, Q3, Q4 hits) | Article 10 data governance, Article 12 logging, Article 13 transparency to deployers, Article 14 human oversight, Article 15 accuracy/robustness, Article 17 quality management, Article 30 post-market monitoring, conformity assessment (Art. 43), CE marking (Art. 48), registration in EU database (Art. 49/71). | "→ **Business tier ($49/user/mo)** for the Article 10 data-governance workspace, Article 12 logging, and Article 30 monitoring. 48-hour deploy." |
| **Limited-risk** | Article 50 (Q2 hit without Art. 5 cross-over) | Transparency: users must be informed they are interacting with AI (Art. 50(1)). AI-generated content must be machine-readable as such (Art. 50(4)). | "→ **Team tier ($29/user/mo)** for AI-system disclosure templates + content-provenance tooling (`meok-watermark-attest-mcp`)." |
| **Out-of-scope** | Article 2 — no EU nexus | No EU AI Act obligations. Voluntary best-practice alignment. (GDPR, sectoral rules, and the EU AI Act GPAI Code of Practice may still apply.) | "→ **Freemium** — bookmark us for the day your footprint changes. Use `eu-ai-act-compliance-mcp` for the 410 verbatim articles as reference." |

## 4. The "5-minute" UX

The whole product is a single-page web form. One question per minute, with a 1-second-per-question pace, a progress bar across 5 segments, and a single CTA at the end.

- **No login required.** The scanner is the trust-builder — gating it behind an account would defeat the purpose.
- **HMAC-SHA256-signed PDF attestation** delivered on the results page. The signing key is `MEOK_ATTESTATION_KEY`, loaded at startup from a secret manager (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, or local `keyring`) per the `get_attestation_key()` pattern in `CRITICAL_FIXES_2026-06-08.md` Fix #3. The PDF carries: timestamp, the five answers, the resulting risk class, the matched articles, and a tamper-evident HMAC signature.
- **Email gate ONLY at the end.** No email is requested until the user has seen their results and the CTA. Email = the $49/mo funnel entry. Email is also the only artifact stored server-side.
- **No storage of answers.** Per GDPR Article 22 (automated decision-making) and Article 25 (data minimization), the five answers are kept in browser memory for the duration of the session and discarded on page close. Only the email + the issued attestation hash are logged for sales-funnel purposes.
- **Cookie-free.** No analytics cookies. Optional Cloudflare Web Analytics (cookieless) for page-view counts only.
- **Single-page deploy.** A static HTML form + one POST endpoint to the MCP. No backend state.

## 5. MCP integration

The scanner is a thin wrapper. The 5 questions are the front-end splitter; the real classification logic lives in the MCP server.

| Component | Role | Detail |
|---|---|---|
| `eu-ai-act-compliance-mcp` (v1.3.0, production) | Existing flagship. Carries 410 verbatim EU AI Act articles, 42-point audit, Article 11 docs, penalty calculator, Article 10 references. PyPI: `eu-ai-act-compliance-mcp`. GHCR: `ghcr.io/csoai-org/eu-ai-act-compliance-mcp`. OpenSSF 81.6/100. | Exposes `classify_system(system_description: str) -> RiskClassification`. The scanner concatenates the 5 yes/no answers into a structured `system_description` and calls this tool. |
| `eu-ai-act-high-risk-classifier-mcp` (P0-build #1) | The MCP that closes the 27% Article 10 gap. Build order: Jun 8 - Jun 21 per `REGULATORY_CALENDAR_2026-2027.md`. Effort: ~2 weeks. | The scanner's heavy lifting routes here once shipped. Until then, `classify_system` on the existing flagship provides the bucket assignment. |
| `meok-watermark-attest-mcp` | For limited-risk outcomes, generates the AI-system disclosure snippet and content-provenance token that the Team-tier CTA references. | Not on the scanner's hot path. Linked from the results page only. |
| `meok-compliance-gateway` keystone | Front-door proxy. The scanner lives behind the same routing the 28 hives use, so the x402 paywall can be slotted in later (e.g. "unlimited scans = $9/mo") without re-architecting. | `http_server.py` already routes `eu-ai-act-compliance-mcp` calls. Add a `/eu-check` static-asset route + a `/api/v1/eu-check/classify` POST. |

## 6. Build order (2-3 days)

**Day 1** — 5 questions, classification logic, MCP wrapper.
- Author the 5-question flow in static HTML + minimal JS (one screen per question, no framework needed).
- Wire the answers into a `classify_system` call against `eu-ai-act-compliance-mcp` (production, available now).
- Map the 2^5 = 32 answer combinations to the 4 outcome buckets per the matrix in §3.
- Add the `/eu-check` static route + `/api/v1/eu-check/classify` POST to `http_server.py`.
- Unit-test the 32 answer combinations end-to-end against the MCP.

**Day 2** — HMAC-SHA256 attestation PDF + email capture.
- Implement `sign_attestation(payload: dict) -> bytes` using the secret-manager pattern from `CRITICAL_FIXES_2026-06-08.md` Fix #3. No fallback to `os.environ`.
- Render the attestation as a single-page PDF (use `reportlab` or `weasyprint`; both are MIT, both are light).
- Add the email-gate POST. Email is the only persisted field. Opt-in checkbox for product updates.
- Wire Cloudflare Web Analytics (cookieless) for page-view counting.
- Verify the CI grep guard for `MEOK_ATTESTATION_KEY` passes (`grep -r "MEOK_ATTESTATION_KEY" --include="*.py" --include="*.yml" --include="*.yaml" .`).

**Day 3** — Deploy, hook Stripe.
- Deploy the static assets to Vercel/Cloudflare Pages (whichever the keystone uses; both work for this).
- Deploy the new `/api/v1/eu-check/*` endpoints through the existing keystone Docker image.
- Point `meok.ai/eu-check` DNS to the deployment.
- Hook the results-page CTA to a Stripe Checkout session for the Business tier ($49/user/mo).
- Smoke-test: complete the 5 questions as an EU-resident, verify the PDF downloads, verify the HMAC verifies, verify the Stripe Checkout opens.

## 7. Success metrics

- **1,000 scanners in week 1.** The EU AI Act urgency engine is the only channel we have that compounds with the August 2 deadline. Each completed scan is a top-of-funnel touch that a paid alternative cannot replicate at this price point.
- **5% conversion to Business tier ($49/user/mo).** 50 paying customers from week 1 = **$2,450 MRR** at full ramp, with no sales-touch cost per conversion. This validates the freemium model and funds the next build wave.
- **100 HMAC-signed attestations archived.** The first 100 PDFs are the proof-of-work artifact for the August 2 PR push. Each one is a public-record demonstration that the keystone is shipping real compliance, not marketing.

## 8. Cross-references

- `REGULATORY_CALENDAR_2026-2027.md` — the build schedule (Phase 2, Jun 21-27) + the 4 P0 deadlines + the Q3 2026 launch MRR target.
- `KEY_DIFFERENTIATORS.md` — differentiator #2 is the **410 verbatim EU AI Act articles** (the scanner's data backbone); differentiator #3 is the **HMAC-SHA256 attestation chain** (the PDF's integrity layer, also the asset Fix #3 protects).
- `PRICING.md` — the **4 SaaS tiers** (Freemium / Team $29 / Business $49 / Enterprise custom). The scanner is the Freemium→Business bridge.
- `CRITICAL_FIXES_2026-06-08.md` — **Fix #3** (MEOK_ATTESTATION_KEY secret management) is the prerequisite for the PDF signing. The scanner must not ship until the `get_attestation_key()` pattern is in place.
- `HIVE_REPO_CREATE_NICK_CHECKLIST_2026-06-08.md` — the 28 repo-creation checklist; the scanner's MCP integration depends on the `eu-ai-act-compliance-mcp` repo being public+mergeable.
- The **4 P0 regulatory deadlines** (EU AI Act Aug 2, China Jul 15, ETSI Q3, Colorado Jan 1 2027) are listed in `REGULATORY_CALENDAR_2026-2027.md`. EU AI Act is the urgency engine; the scanner is its customer-facing surface.

## 9. Source pointers

- `/tmp/kimi_dossier_v2/sov3_state_of_empire.agent.final.md` § 5.1 — gap #2 ("EU AI Act free scanner — Deploy the 5-minute risk assessment tool at meok.ai/eu-check, 2-3 days effort") and § 5.1 readiness checklist.
- `/tmp/kimi_dossier_v2/sov3_portfolio_inventory.md` — `eu-ai-act-compliance-mcp` flagship spec (v1.3.0, 410 articles, 42-point audit, OpenSSF 81.6, x402 monetization, freemium gates).
- `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` § 2.1 — EU AI Act Compliance category feature gap (MEOK vs Credo AI, Holistic AI, Cranium, OneTrust, ServiceNow, AuditBoard).
- `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` — Annex III risk-classification engine + governance engine spec covering Articles 10, 12, 13, 30 (the obligations the scanner routes customers into).
- `/Users/nicholas/meok-compliance-gateway/PRICING.md` — the 4-tier funnel.
- `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` — differentiators #2 (verbatim articles) and #3 (HMAC chain).
- `/Users/nicholas/meok-compliance-gateway/CRITICAL_FIXES_2026-06-08.md` — Fix #3 (attestation key), `get_attestation_key()` reference implementation, CI grep guard.
- `/Users/nicholas/meok-compliance-gateway/REGULATORY_CALENDAR_2026-2027.md` — T-55 to Aug 2, P0 build order, MRR roadmap.
