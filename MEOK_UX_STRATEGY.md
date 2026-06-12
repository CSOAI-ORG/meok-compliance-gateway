# MEOK UX Strategy — Dossier-Validated Patterns

> **Authored**: 2026-06-08
> **Purpose**: UX strategy for the MEOK Compliance Gateway, synthesised from `/tmp/kimi_dossier_v2/research/deepdive_uiux_analysis.md` (654 lines, 10 competitor UI/UX deep-dives + UX benchmark rankings + recommended SOV3 UI patterns + scorecard + anti-patterns). Backed by G2, Capterra, Trustpilot, Gartner Peer Insights, and YouTube-demo signal.
> **Source**: `/tmp/kimi_dossier_v2/research/deepdive_uiux_analysis.md` § 1-10 (per-competitor UX analysis) + § "UX Benchmark Rankings" (best/worst + SOV3 target) + § "Recommended SOV3 UI Patterns" (dashboard, navigation, onboarding, mobile, a11y) + § "Competitive UX Scorecard" (10-row scorecard) + § "Killer UI Patterns to Copy" / "UX Anti-Patterns to Avoid".
> **Rubric**: factual comparative, no war language per `RUBRIC_EXTERNAL_COMMS.md`. Banned vocabulary in § 8.

## 1. The 10-platform UX scorecard (factual)

| Platform | Info density | Nav complexity | Onboarding | Dashboard pattern | UX score (source) |
|---|---|---|---|---|---:|
| **Wiz** | Low-Med | Simple | Agentless deploy | Security graph | **8/10** |
| **Vanta** | Low-Med | Simple | Checklist | Progress bars | **7.5/10** |
| **Credo AI** | Medium | Moderate | Demo-only | Radar charts | **7/10** |
| **Drata** | Medium | Moderate | Guided setup | Trust Dashboard | **7/10** |
| **Cranium** | Low-Med | Simple | Demo-only | Pipeline view | **6.5/10** |
| **Zenity** | Medium | Moderate | Video demos | Agent orbit | **6/10** |
| **WitnessAI** | Medium | Moderate | Demo+tour | 4-quadrant | **5.5/10** |
| **OneTrust** | Very High | Very Complex | 3-month impl | Modular cards | **5/10** |
| **ServiceNow** | High | Very Complex | Consultant req | Form-heavy | **5/10** |
| **CrowdStrike** | Very High | Very Complex | Week+ training | SIEM console | **4.5/10** |

**Source**: dossier § "Competitive UX Scorecard" + per-competitor sections. Scores synthesised from G2, Capterra, Trustpilot, Gartner Peer Insights, and YouTube-demo signal.

## 2. The 3 best UX patterns (study + copy)

### Wiz (8/10) — "Single pane of glass"
- Minimal homepage (headline + body + CTA + illustration)
- "Security graph" concept — connects code, cloud, runtime into one visualisation
- Agentless deployment (zero friction to start)
- Whitespace-heavy design (proves security doesn't have to look scary)
- G2 reviews: "single pane of glass to see what is going on" (CSO, Blackstone), "very intuitive interface and a really simple dashboard" (Cloud Security Architect)

**What MEOK copies**: "agent governance graph" — all AI agents in one view, with the same single-pane-of-glass confidence Wiz has. MEOK's `meok-hive/index.html` is already minimal + whitespace-heavy per `gen-geo.py`; this validates the design.

### Vanta (7.5/10) — "Checklist onboarding"
- 5-step compliance setup checklist with progress bar
- Welcome chatbot
- Light-purple aesthetic (friendly, non-intimidating)
- 1,818 G2 reviews at 4.6/5

**What MEOK copies**: 5-step agent governance setup checklist (Connect agent → Set policy → Review inventory → Invite team → Customise dashboard), progress bar to "first insight", sample data pre-loaded.

### Credo AI (7/10) — "Radar trust chart"
- Multi-dimensional trust score (Bias, Compliance, Security, Privacy, Safety, Reliability)
- Dark mode default
- Governance flow diagram: Unmanaged → Governance → Trusted

**What MEOK copies**: trust-score radar chart on the agent detail view, dark mode default, the "unmanaged → governed → trusted" progression as a flow diagram.

## 3. The 3 worst UX patterns (anti-patterns to avoid)

### OneTrust (5/10) — "Settings inside settings, 3-month implementation"
- 2.5-3.5 month implementation timelines
- Modular disconnect (users toggle between tools)
- Enterprise-only support alienates mid-market
- G2 recurring complaint: "platform does not reveal its secrets easily"
- Trustpilot rating: 1.5/5

**What MEOK avoids**: flat navigation (max 2 levels deep), no 3-month implementation (<5 minutes to first value), self-serve tier at $29/mo that doesn't alienate SMB.

### CrowdStrike (4.5/10) — "Alert fatigue, SIEM console"
- Dense SIEM-style interface
- "Gets easier after a solid week or two" — admission of UX failure
- July 2024 BSOD incident destroyed trust (8.5M machines down, $10B+ in damages)
- Requires dedicated security analysts to operate

**What MEOK avoids**: actionable insights only (no raw alert feeds), intuitive from first click, no kernel-mode dependencies (MEOK is governance-layer, not Ring 0).

### ServiceNow (5/10) — "Form-heavy, consultant-required"
- Form-heavy enterprise UI
- AI chat assistant (Otto) — partial credit
- "Overkill" complaint from G2/Trustpilot

**What MEOK avoids**: streamlined forms, smart defaults, no consultant requirement (self-serve signup).

## 4. The 4 SOV3 design principles (dossier-derived)

### Principle 1 — Zero-friction onboarding
- **Self-service signup** (no demo gate, no sales call)
- **<5 minutes to first value** (target: sign up → connect agent → see results)
- **Sample data pre-loaded** (dashboard populated immediately)
- **Progress bar to "first insight"** (gamify setup)
- **Interactive checklist** (5 steps, Vanta pattern)

### Principle 2 — Single-pane-of-glass dashboard
- **Agent governance graph** (Wiz-style) — all agents in one view
- **Trust score radar** (Credo AI pattern) — multi-dimensional scoring
- **Framework compliance %** (Drata pattern) — circular progress indicators
- **Risk timeline** — chronological view of agent activities + policy violations
- **Card-based agent inventory** — status indicators per agent
- **Dark mode default** with light-mode option (security users expect dark)

### Principle 3 — Agent-first navigation
- **Left sidebar** with icon + label (Vanta/ServiceNow pattern)
- **Max 5 top-level sections**: Dashboard, Agents, Policies, Reports, Settings
- **Command bar** (type to navigate, search everywhere)
- **Max 2 clicks** to any key action
- **Contextual help tooltips** on every element
- **Breadcrumb navigation** for deep pages

### Principle 4 — Accessible by default
- **WCAG 2.1 AA compliance** from day one
- **Keyboard navigation** for all features
- **Screen reader support** for charts and visualisations
- **High contrast mode** option
- **Reduced motion** option
- **Font size controls** in settings

## 5. The 6 SOV3 UX differentiators (positioning)

1. **Zero-friction onboarding** — sign up, connect agent, see results in <5 minutes
2. **Agent governance graph** — Wiz-style "single pane of glass" for all AI agents
3. **Trust score radar** — Credo-style multi-dimensional visualisation
4. **Self-service first** — no demo gates, no sales calls required
5. **Dark mode by default** — security professionals expect it
6. **Transparent pricing** — no quote-only pricing (4 tiers, public, $0/$29/$49/custom)

## 6. The 4-tier implementation roadmap

### Tier 1 — Day 1 (MVP, ships with launch Jul 4)
- Self-service signup (OAuth + email)
- Single agent connection (1-click OAuth or paste endpoint)
- 1 framework selected (EU AI Act)
- Trust score radar (basic, 5 dimensions)
- Agent inventory list view
- Dark mode default

### Tier 2 — Week 2 (post-launch, drives paid conversion)
- 5-step onboarding checklist with progress bar
- All 13 frameworks selectable
- Command bar (Cmd+K) navigation
- Risk timeline view
- Audit trail export (HMAC-signed PDF)
- x402 paywall integration for the 6 free-scanner follow-ups

### Tier 3 — Month 1 (drives Team tier $29/mo)
- Multi-agent inventory grid
- Custom policies (Rego / natural-language)
- Webhook subscriptions (per `MEOK_API_STRATEGY.md` § 4 10 event types)
- Slack + email notifications
- Mobile-responsive (PWA, no separate app)

### Tier 4 — Quarter 1 (drives Business tier $49/mo + Enterprise)
- Multi-tenant dashboard
- White-label attestations (HMAC-signed verify URLs)
- API access (REST + GraphQL per `MEOK_API_STRATEGY.md` Phase 2)
- SOC 2 / ISO 27001 evidence collection
- SSO (SAML, OIDC)

## 7. The 5 wireframe specs (per dashboard section)

### Section 1 — Agent governance graph (Wiz-inspired)

```
+----------------------------------------------------------+
| MEOK  [search]            [Cmd+K]   [bell] [user@org]    |
+----------------------------------------------------------+
| > Dashboard > Agents > Agent-42                          |
+----------------------------------------------------------+
|                                                          |
|        [Trust Score Radar]      [Agent Detail Card]      |
|             Compliance (87)        Name: Agent-42        |
|             Bias (94)              Framework: EU AI Act  |
|             Security (76)          Last scan: 12m ago    |
|             Privacy (88)           Status: ✓ Compliant   |
|             Safety (91)            Owner: alice@org       |
|             Reliability (83)       Tools: 12 active      |
|                                                          |
|        [Risk Timeline (last 7d)]                         |
|        12:34  Policy: GDPR-30  ✓ pass                    |
|        12:30  Tool:  query_db   ✓ allow                  |
|        12:25  Action: redact   ⚠ warn                    |
|                                                          |
+----------------------------------------------------------+
```

### Section 2 — Framework compliance dashboard (Drata-inspired)

```
+----------------------------------------------------------+
| Compliance overview              [Export PDF] [Audit log]|
+----------------------------------------------------------+
|                                                          |
| EU AI Act        ████████░░  78%    ✓ 12/15 articles    |
| NIST AI RMF      ██████░░░░  62%    ✓ 18/29 controls    |
| ISO 42001        ███████░░░  71%    ✓ 22/31 controls    |
| SOC 2            █████████░  91%    ✓ 64/70 criteria    |
| ISO 27001        ████████░░  84%    ✓ 93/110 controls   |
| GDPR             ████████░░  88%    ✓ 44/50 articles    |
| ... (13 frameworks total)                                |
|                                                          |
| [View all 13] [Last audit: 2026-05-12]                   |
+----------------------------------------------------------+
```

### Section 3 — Onboarding checklist (Vanta-inspired)

```
+----------------------------------------------------------+
| Welcome to MEOK — let's get your first agent monitored  |
+----------------------------------------------------------+
|                                                          |
| 1. ✓ Connect your first AI agent     [done]              |
| 2. ✓ Set your first policy           [done]              |
| 3. → Review your agent inventory     [3 agents, 2 warn] |
| 4.   Invite team members             [skip for now]      |
| 5.   Customize your dashboard        [skip for now]      |
|                                                          |
| Progress: 40% — you're 2 steps from first insight!      |
+----------------------------------------------------------+
```

### Section 4 — Command bar (Cmd+K)

```
+----------------------------------------------------------+
| 🔍  Type a command, search, or navigate...              |
+----------------------------------------------------------+
| →  Agents          [G then A]                            |
| →  Policies        [G then P]                            |
| →  Frameworks      [G then F]                            |
| →  Audit log       [G then L]                            |
| →  Settings        [G then S]                            |
|                                                          |
| Recent:  Agent-42, Policy "GDPR-30", Audit 2026-05-12   |
+----------------------------------------------------------+
```

### Section 5 — Pricing page (transparent, no quote-only)

```
+----------------------------------------------------------+
| Pricing — simple, transparent, no surprises              |
+----------------------------------------------------------+
|                                                          |
| FREE          TEAM           BUSINESS        ENTERPRISE  |
| $0/mo         $29/user/mo    $49/user/mo     Custom      |
|                                                          |
| 1 user        5 users        25 users        Unlimited   |
| 1 framework   5 frameworks   13 frameworks   13+ custom  |
| 100 MCP calls 100K calls    1M calls         Unlimited   |
| Community     Email support  Slack support   CSM         |
|                                                          |
| [Sign up]    [Start trial]  [Start trial]   [Contact]    |
|                                                          |
| 70-95% cheaper than OneTrust (see TCO calc)              |
+----------------------------------------------------------+
```

## 8. The 4 "do NOT do" rules

1. **Do NOT name-and-shame specific competitors beyond the UX score.** The scorecard IS external-safe (factual UX ratings from public review sites). The narrative "X is awful" is NOT — use "X's G2 reviews mention a 3-month implementation timeline" (sourced to a public review).
2. **Do NOT use war vocabulary.** Banned per `RUBRIC_EXTERNAL_COMMS.md` § 8: "kill shot", "nuclear arsenal", "coup de grâce", "talent raid", "seeding doubt", "depletion campaign", "strike while", "vulnerability window", "acquisition target", "funding fiction".
3. **Do NOT claim UX scores that aren't sourced.** Every score in § 1 has a source (G2, Capterra, Trustpilot, Gartner Peer Insights, YouTube demo). If a claim can't be sourced, drop it.
4. **Do NOT quote CrowdStrike's "$10B BSOD damages" externally without the source.** The dossier's source is the Delta Air Lines + Fortune 500 financial impact disclosures. Always cite the primary source.

## 9. Cross-references

- `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` — the 8 differentiators, #6 mentions "Wiz-style single-pane-of-glass" (this doc is the spec for that claim).
- `/Users/nicholas/meok-compliance-gateway/SOV3_UNIQUE_CAPABILITIES_MATRIX.md` — capabilities #1-#10, the architecture-agnostic substrate this UX doc wraps.
- `/Users/nicholas/meok-compliance-gateway/PRICING.md` — the 4-tier transparent pricing (§ 7 wireframe 5 references this).
- `/Users/nicholas/meok-compliance-gateway/EU_AI_ACT_FREE_SCANNER_SPEC.md` — the funnel into the Business tier (UX onboarding checklist § 7 wireframe 3 references this).
- `/Users/nicholas/meok-compliance-gateway/MEOK_API_STRATEGY.md` — the 10 event types that the Webhook subscriptions + Notifications features wire to (Tier 3 implementation).
- `/Users/nicholas/meok-compliance-gateway/CRITICAL_FIXES_2026-06-08.md` — the 3 CRITICAL security fixes (root Docker, API key storage, HMAC env-var) that the "secure by default" UX promise depends on.
- `/Users/nicholas/meok-compliance-gateway/CVE_INTEL_BRIEF_2026-06-08.md` — the trust-score dimensions (Bias, Security, Privacy) reference the OWASP Agentic Top 10 + the 30+ MCP CVE database.
- `/Users/nicholas/meok-compliance-gateway/MCP_MARKETPLACE_STRATEGY.md` — the 6-marketplace rollout plan the "API access" Tier 4 feature supports.
- `/Users/nicholas/meok-compliance-gateway/28_DAY_BLOG_CALENDAR.md` — the content calendar (Jul 4 28-post blitz) that drives the marketing-side UX messaging.
- `/Users/nicholas/meok-compliance-gateway/SOV3_FINANCIAL_MODEL_2026-2028.md` — the 8-quarter P&L that the 4-tier pricing structure backs (INTERNAL ONLY).
- `/Users/nicholas/meok-compliance-gateway/scripts/gen-geo.py` — the landing-page generator that already implements many of these UX patterns (minimal hero, whitespace, dark mode default, FAQ + authority queries).
- [[meok-geo-strategy-2026-06-07]] — the GEO/AEO strategy that the dashboard content (FAQs, llms.txt) implements.

## 10. Source pointers

- `/tmp/kimi_dossier_v2/research/deepdive_uiux_analysis.md` (full file, 654 lines).
- G2 review data: OneTrust (4.3/5, 148 reviews), Vanta (4.6/5, 1,818 reviews), Drata (4.8/5), Wiz (4.5/5+).
- Capterra reviews: OneTrust (4.3/5), Vanta (4.3/5), Drata (4.8/5).
- Trustpilot reviews: CrowdStrike (1.5/5 pattern).
- Gartner Peer Insights: Credo AI (no reviews yet), Drata (3.8/5), WitnessAI (~4.5/5).
- Sprinto blog: "Honest OneTrust Review 2026".
- ComplyJet blog: "Drata Review 2026".
- CheckThat.ai: "WitnessAI: Details, Reviews, Pricing, & Features".
- UnderDefense: "Wiz Pricing Overview".
- YouTube demos: OneTrust Technical Workshop (46min), Credo AI Agent Registry Demo, Wiz Intro.
- [[meok-deep-audit-2026-06-08]] — the deep audit memory, this UX strategy is the Tier-2 deliverable in § 5.
- [[eat-execute-july4-plan-2026-06-08]] — the 5-lane alignment plan, Lane E (keystone docs) is where this doc lives.
