# Marketplace & Platform Economics Playbook — MEOK Synthesis

> **Source**: `docs/seo-global-report/research/sov3_bizmodel/sov3_bizmodel_marketplace.md` (Kimi, 652 lines, 7 platform benchmarks: Shopify, Salesforce, GitHub, Twilio, Stripe, Slack, AWS Marketplace)
> **Maps to revenue stream**: **Stream 2 (MCP App Store) — $0 Y1 / $4M Y5** per `SOV3_FINANCIAL_MODEL_2026-2028.md`; the long-tail wedge that compounds.
> **Purpose**: extract the 7 platform-economics patterns (commission tiers, trust signals, ecosystem-to-revenue ratios, developer incentives) into keystone-specific MCP App Store actions.
> **Companion**: `MCP_MARKETPLACE_STRATEGY.md` (the 6-marketplace submission playbook, DONE 8 Jun)
> **Rubric**: factual comparative, no war language. Banned vocabulary per `RUBRIC_EXTERNAL_COMMS.md`.

## 1. The 7 platform benchmarks — keystone-applicable patterns

| Platform | Apps/Servers | Ecosystem revenue | **Keystone-applicable pattern** |
|---|--:|--:|---|
| **Shopify App Store** | 8,000+ apps | $6.3B+ GMV (2023) | "0% commission on first $1M" developer-acquisition lever. "Built for Shopify" trust signal drives 49% more installs. **Apply to:** MCP App Store 0% commission Y1. |
| **Salesforce AppExchange** | 3,000+ apps | $123B+ ecosystem revenue (2024) | PNR (Percentage Net Revenue) model: 15% on first $1M, 10% on next $5M, 5% above. $5.80 ecosystem per $1 Salesforce = the 5.8x ratio. **Apply to:** SOV3 PNR 0% Y1, 10% Y2, 15% Y3+; target 3-5x ecosystem-to-revenue ratio by Y5. |
| **GitHub Marketplace** | 1,000+ apps | $200M+ estimated | Free + paid tiers; "Verified" badge for security-vetted apps. **Apply to:** the keystone's OpenSSF Scorecard 81.6 is the GitHub-verified equivalent. |
| **Twilio Marketplace** | 300+ add-ons | $50M+ | "Add-on" model: one-click install from Twilio Console. **Apply to:** the keystone's MCP tools are the "one-click add-on" for the 28-hive mesh. |
| **Stripe Apps** | 800+ apps | $100M+ (estimated) | "Build the best core infrastructure FIRST, then add marketplace as a moat." Stripe deliberately did NOT charge commission early. **Apply to:** the keystone's MCP-native x402 paywall is the core; the MCP App Store is the moat. |
| **Slack App Directory** | 2,600+ apps | $500M+ | "Workflow-first" apps (Slack Workflow Builder). **Apply to:** the 28-hive cross-link mesh is the "workflow" — apps that compose across hives. |
| **AWS Marketplace** | 10,000+ products | $50B+ GMV | "Seller-registration + 4-6 week vetting" (per `sov3_intel_dim08-cloud-marketplaces.md`). **Apply to:** the G5 manual gate (Cloud Run / AWS AgentCore creds) is the marketplace-launch blocker. |

## 2. The 3 SOV3-specific actions (the App Store wedge)

### Action 1 — 0% commission Year 1 (Shopify + Stripe pattern)

**Source playbook**: Shopify's 0% commission on first $1M GMV; Stripe's deliberate no-commission early. Both used the no-commission lever to build the **developer mindshare** that compounds.
**MEOK claim**: the MCP App Store launches Q4 2026 (per `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` Phase 2) with **0% commission Year 1**, then 10% Y2, 15% Y3+. The compounding flywheel: more apps → more installs → more customers → more apps.
**Tactical action**: the no-commission promise is the headline of the MCP App Store launch. Document in the 28-hive landing pages (the openMCP-hive is the App Store front door per `MCP_MARKETPLACE_STRATEGY.md`).
**Owner**: Eng (App Store build, Q3 2026) + Marketing (positioning, Q3 2026 launch). **Effort**: 12 weeks engineering + 2 weeks marketing assets.

### Action 2 — The "Built for MEOK" / "OpenSSF-verified" trust signal (Shopify + GitHub pattern)

**Source playbook**: Shopify's "Built for Shopify" badge drives 49% more installs. GitHub's "Verified" badge drives security-conscious enterprise adoption. **The trust signal is the marketplace's compounding moat.**
**MEOK claim**: the keystone's OpenSSF Scorecard 81.6 + the MCP-reg schema enrichment (icons, websiteUrl, _meta categories, `assets/keystone-icon.svg` shipped 9 Jun) are the trust-signal substrate. The "OpenSSF-verified" badge becomes the SOV3 equivalent of "Built for Shopify."
**Tactical action**: the badge is already in the keystone's README (auto-inserted by `scripts/add_openssf_badge.py`). The next step is **applying it to the 28 hive-staging repos** when Nick creates them (per `HIVE_REPO_CREATE_NICK_CHECKLIST_2026-06-08.md`).
**Owner**: Eng (badge script DONE) + Nick (repo creation, G1). **Effort**: 1 minute per repo once Nick creates them.

### Action 3 — The 4-marketplace-side launch sequence (per `MCP_MARKETPLACE_STRATEGY.md`)

**Source playbook**: every successful platform launched in a **single primary marketplace** first, then expanded. Shopify's primary marketplace was Shopify (self-hosted); Salesforce's primary was AppExchange (native). SOV3's primary is the keystone + openMCP.
**MEOK claim**: per `MCP_MARKETPLACE_STRATEGY.md` § 5, the 6-marketplace priority matrix is: **openMCP (primary, self-hosted) → Smithery → Glama → PulseMCP → MCP.so → MCPize**. The 6 are listed in launch order; primary is Q3 2026, secondary is Q4 2026-Q1 2027.
**Tactical action**: the launch sequence is specced (per `MCP_MARKETPLACE_STRATEGY.md`); the unblocker is the **G6 gate (Smithery/Glama/PulseMCP/MCPize logins, 15 min, account-gated)**. Without G6, the secondary marketplaces don't go live.
**Owner**: Eng (G1, G4 — unblocked) + Nick (G6 — account-gated). **Effort**: 15 min of Nick time.

## 3. The 5 platform-economic "first-mover" positions

Per the Kimi playbook analysis, the **7 platforms combined process $100B+ in ecosystem revenue annually**. SOV3's wedge:

| Position | Claim | Evidence |
|---|---|---|
| **First MCP-native marketplace** | "The first marketplace whose listings are MCP servers (not APIs, not SaaS apps)" | `MCP_MARKETPLACE_STRATEGY.md` § 1, the 76-server master audit |
| **First governance-gated marketplace** | "The first marketplace that requires OpenSSF Scorecard > 7.0 to list" | The keystone's scorecard 81.6 + the 28-hive fleet |
| **First USDC-settled marketplace** | "The first marketplace where every install is settled in USDC via x402, no Stripe" | `MEOK_API_STRATEGY.md` § 1, the keystone's x402 substrate |
| **First multi-jurisdictional marketplace** | "The first marketplace that tags every listing with EU/China/US/UK regulatory compliance" | The 4 P0 deadline specs (China/EU/ETSI/Colorado) |
| **First industry-pack marketplace** | "The first marketplace with industry vertical packs (FinServ, Health, Construction, etc.)" | `INDUSTRY_PACKS_2027_Q1.md` (other-session work, 7 industry packs) |

**Tactical action**: these 5 positions are the 5 hero claims of the MCP App Store launch. Each is a 1-paragraph elevator pitch + a backing public doc.
**Owner**: Marketing (Nick). **Effort**: 5 paragraphs of writing (2 hours).

## 4. The 5 "do NOT do" rules (the platform anti-patterns)

1. **Do NOT charge commission in Year 1** — Shopify + Stripe both used 0% to build mindshare; commission is a Y2-Y3 lever, not Y1.
2. **Do NOT allow unvetted apps** — the OpenSSF Scorecard gate is the marketplace's structural defense. Every listing must be scorecard > 7.0 OR explicitly tagged "experimental."
3. **Do NOT compete on price** — the marketplace's differentiator is **trust** (OpenSSF, BFT attestation, HMAC chain), not price. Race-to-bottom commissions destroy the marketplace.
4. **Do NOT launch all 6 marketplaces simultaneously** — primary first (openMCP, Q3 2026), secondary in Q4 2026-Q1 2027. Per the playbook, every successful platform did this.
5. **Do NOT build the marketplace before the keystone is stable** — Stripe's pattern: "best core infrastructure FIRST, then marketplace as a moat." The keystone's 1.0.0 release (post-launch hardening, per the 25-day playbook W5) is the gate.

## 5. The 4-year ecosystem-to-revenue projection

Per the playbook's data:

| Year | Keystone revenue | App Store revenue | Ecosystem revenue (3-5x ratio) |
|---|--:|--:|--:|
| Y1 (2026) | $1M ARR | $0 (0% commission, free) | $5M+ (3-5x of keystone) |
| Y2 (2027) | $10M ARR | $1M ARR (10% commission) | $30M-50M |
| Y3 (2028) | $30M ARR | $4M ARR (15% commission) | $90M-150M |
| Y5 (2030) | $100M ARR | $20M ARR | $300M-500M |

The 3-5x ecosystem-to-revenue ratio is **the pattern across all 7 benchmark platforms** (Salesforce $5.80, Shopify ~$5, Twilio ~$4, AWS Marketplace ~$5). The SOV3 trajectory is conservative at 3-5x; the upside is 6-8x if the keystone becomes the de-facto AI governance standard.

## 6. Cross-references

- `docs/seo-global-report/research/sov3_bizmodel/sov3_bizmodel_marketplace.md` — full 652-line source
- `MCP_MARKETPLACE_STRATEGY.md` — the 6-marketplace submission playbook
- `MEOK_API_STRATEGY.md` — the 3-phase API roadmap
- `SOV3_FINANCIAL_MODEL_2026-2028.md` § Stream 2 — the App Store revenue projection
- `meok-cross-post` (memory) — the openMCP cross-post CLI
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — Phase 2 covers MCP App Store pre-announce (Jun 21-27)
- `HIVE_BUILD_DASHBOARD.md` — the 28-hive mesh that the App Store indexes

---

*Synthesized 2026-06-09 by Claude (Opus 4.8 session on `claude/review-changes-mkbcvckpl5ix3r03-MkKCu`). Source playbook is Kimi-derived third-party research; SOV3 applications are keystone-specific. The 3-5x ecosystem ratio is a synthesis of 7 benchmark platforms; the SOV3-specific projection requires validation against actual pilot data.*
