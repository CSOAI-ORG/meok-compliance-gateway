# 4 P0-Build MCPs — Engineering Briefs (Q3 2026 LAUNCH)

> **Source**: `sov3_mcp_master_audit.docx` Part 4 "MCP Build Priority Matrix" + Part 15 "Recommended MCP Build Specifications" (8 Jun 2026)
> **Priority**: P0 = "Build now — regulation effective within 6 months"
> **Days remaining** (as of 2026-06-08): EU AI Act 55 days, China AI 37 days, Colorado ADMT 207 days, ETSI CABCA "ongoing" (enables 6-month lead)
> **All 4 are the keystone's deepest differentiators** — they turn "general compliance MCP" into "we cover Aug 2, 2026"

## Why these 4 and not others

The audit's priority definitions:
- **P0**: Build now — regulation effective within 6 months (immediate)
- **P1**: Build in 3 months — regulation effective in 6-12 months (Q3 2026)
- **P2**: Monitor — regulation in development or voluntary (ongoing)

The 4 P0s share one trait: **they fill gaps that no competitor has and that become legally enforceable within 6 months**. The 8 P1s (`sec-ai-disclosure-anti-washing`, `australia-ai-guardrails`, `automotive-ai-type-approval`, `eu-ai-act-article-50-checker`, etc.) and 3 P2s (`iso-23894`, `china-comprehensive`, `uk-ai-regulator-guidance`, `japan-haip-reporting`) come second.

## P0-1: `eu-ai-act-high-risk-classifier-mcp` (MCP-001)

**Regulation**: EU AI Act Article 6 + Annex III (effective 2 Aug 2026)
**Days to enforcement**: **55 days** (most urgent of the 4)
**Confidence**: HIGH (legally certain; Omnibus may extend subset)
**Audit rationale**: "Automated classification is foundational; 58 days to full enforcement"

**Purpose**: Automated classification of AI systems against EU AI Act Annex III
**Framework**: EU AI Act Article 6 + Annex III
**Inputs**: AI system description, intended use case, domain, output type
**Outputs**: Risk classification (prohibited/high/limited/minimal), justification, compliance checklist, documentation requirements

**Key features**:
- Annex III 8-category classifier with decision-tree logic
- Article 6(3) derogation assessment (narrow procedural task, etc.)
- Article 6(4) documentation generation for "not high-risk" determinations
- Integration with EU database registration workflow
- Commission guidelines (May 2026) examples built in
- Appeals/review workflow for contested classifications
- Multi-language support (all EU languages)

**Dependencies**: EU AI Act text database, Commission guidelines corpus

**Build timeline**: Start immediately; **MVP by 15 July 2026**

**Effort estimate**: 1 senior eng × 4 weeks = ~160 eng-h

**Why this is the wedge**: 50,000 EU enterprises need this exact question answered ("am I high-risk?") by Aug 2. The audit's verdict is unambiguous: "this is the single most important MCP in the Q3 LAUNCH."

---

## P0-2: `china-ai-anthropomorphic-compliance-mcp` (MCP-003)

**Regulation**: China Interim Measures for AI Anthropomorphic Interaction Services (effective **15 Jul 2026**)
**Days to enforcement**: **37 days** (most urgent of all 4)
**Confidence**: HIGH (issued, effective date set)
**Audit rationale**: "44 days to enforcement; entirely new regulation"

**Purpose**: Compliance for China's AI Anthropomorphic Interaction Services regulation
**Framework**: Interim Measures for AI Anthropomorphic Interaction Services
**Inputs**: Service description, interaction model, target user demographics, content types, algorithm details
**Outputs**: Compliance checklist, filing documentation, content moderation framework, anti-addiction controls, minor protection assessment

**Key features**:
- Anthropomorphic service scope checker
- Anti-deception control validator
- Anti-addiction mechanism assessment
- **Minor protection compliance checker (virtual companion ban for minors)** — the most consequential provision
- Algorithm filing documentation generator
- Content moderation framework validator
- Incident response plan template
- Chinese language support

**Dependencies**: Chinese regulation text, MIIT filing system integration

**Build timeline**: Start immediately; **MVP by 1 July 2026** (the shortest timeline of the 4)

**Effort estimate**: 1 senior eng × 3 weeks = ~120 eng-h (Chinese-language content is a multiplier)

**Why this matters**: First-mover in China's anthropomorphic-AI regulation. The minor-protection provision is a regulatory innovation (no equivalent in EU/US) and signals China's enforcement posture. Building the MCP first = the de facto reference implementation.

---

## P0-3: `etsi-cabca-continuous-conformity-mcp` (MCP-004)

**Regulation**: ETSI TS 104 008 V1.1.1 (CABCA) — published Jan 2026, "ongoing" applicability
**Confidence**: HIGH (purpose-built for EU AI Act continuous compliance; enables 6-month lead)
**Audit rationale**: "Purpose-built for EU AI Act continuous compliance; enables 6-month lead"

**What CABCA is**: Continuous Auditing-Based Conformity Assessment — the post-market monitoring standard that maps directly to EU AI Act Article 9 (risk management) and Article 15 (accuracy/robustness). The standard operationalizes legal requirements into measurable metrics.

**CABCA key features** (informs MCP design):
- **Continuous compliance** — not point-in-time audits; ongoing monitoring
- **Metric-driven** — legal requirements → measurable metrics
- **Machine-readable specifications** — automated execution and reporting
- **Data drift detection** — built-in monitoring for model degradation
- **Traceability chain** — Results → Metrics → Requirements → Quality Dimensions → Conformity Specification
- **Stakeholder profiles** — different docs for providers, auditors, regulators, operators, end users
- **Non-conformity handling** — automated detection, reporting, and corrective action planning

**Purpose**: Continuous Auditing-Based Conformity Assessment per ETSI TS 104 008
**Framework**: ETSI TS 104 008 V1.1.1 (aligned with EU AI Act)
**Inputs**: AI system operational metrics, model drift data, incident reports, conformity specifications, quality dimensions
**Outputs**: Continuous assessment reports, non-conformity alerts, corrective action plans, conformity status dashboards

**MCP key features**:
- CABCA 3-phase workflow: **Scoping → Operationalization → Continuous Assessment**
- Data drift monitoring (PSI, KS-test, etc.)
- Quality dimension tracking (bias, accuracy, robustness, cybersecurity)
- Metric threshold management with automatic alerting
- Non-conformity detection and corrective action workflow
- Stakeholder-specific documentation profiles (provider, auditor, regulator)
- EU AI Act Article 9 (risk management) and Article 15 (accuracy/robustness) alignment
- Machine-readable specification export

**Dependencies**: ETSI TS 104 008 standard, monitoring infrastructure

**Build timeline**: Start immediately; **MVP by 1 August 2026**

**Effort estimate**: 1 senior eng × 4 weeks = ~160 eng-h (monitoring infra is the multiplier)

**Why this matters**: This is the post-market monitoring engine that **keeps users compliant after Aug 2**, not just at the deadline. The audit explicitly calls it "critical for EU AI Act" — the standard was purpose-built for the AI Act's post-market monitoring obligations, and there's no equivalent competitor offering.

---

## P0-4: `colorado-admt-compliance-mcp` (MCP-002)

**Regulation**: Colorado SB 26-189 (effective **1 Jan 2027**)
**Days to enforcement**: 207 days
**Confidence**: HIGH (signed into law)
**Audit rationale**: "New law, fundamentally different framework; 7 months to prepare"

**Purpose**: Compliance management for Colorado SB 26-189 (ADMT in consequential decisions)
**Framework**: Colorado Revised Statutes SB 26-189
**Inputs**: ADMT system inventory, decision types, consumer interaction points
**Outputs**: Compliance status, impact assessment drafts, consumer notice templates, risk management policy framework, audit trail

**Key features**:
- "Consequential decision" scope checker (**8 categories** — defines what counts as ADMT)
- **ADMT vs. "high-risk AI" distinction** — a new framework that doesn't map 1:1 to EU AI Act
- Annual impact assessment generator
- Consumer notice template generator (at/before decision point)
- Human review workflow for adverse decisions
- Risk management policy template
- Integration with NIST AI RMF and ISO 42001 for **affirmative defense**
- Attorney General reporting workflow

**Dependencies**: Colorado SB 26-189 text, NIST AI RMF MCP, ISO 42001 MCP

**Build timeline**: Start **1 July 2026**; **MVP by 1 October 2026**

**Effort estimate**: 1 senior eng × 4 weeks = ~160 eng-h

**Why this matters**: Colorado is the **first US state with comprehensive AI consumer-protection law** for ADMT. The "ADMT vs. high-risk AI" distinction is a new framework — there's no US federal equivalent to align to. Building the MCP first = the de facto reference implementation for any state that copies Colorado (likely 5-10 states by 2027 per the audit's threat assessment).

---

## Phasing & dependencies

```
JUN 2026 (now)     Start eu-ai-act-high-risk-classifier (MCP-001)
                   Start china-ai-anthropomorphic (MCP-003)
                   Start etsi-cabca-continuous-conformity (MCP-004)

JUL 2026           Start colorado-admt-compliance (MCP-002)
                   MCP-001 MVP target (15 Jul)
                   MCP-003 MVP target (1 Jul)
                   China AI regulation enforcement (15 Jul)

AUG 2026           MCP-004 MVP target (1 Aug)
                   EU AI Act full application (2 Aug) — first day of enforced usage

SEP-NOV 2026       MCP-002 build (3 months)

OCT 2026           MCP-002 MVP target (1 Oct)
                   EU CRA: Vulnerability/incident reporting begins (11 Sep)

DEC 2026           EU CRA: Notified bodies must be operational (11 Dec)
                   EU AI Act Digital Omnibus expected final adoption

JAN 2027           Colorado SB 26-189 effective (1 Jan) — first day of enforced usage
```

## Cross-MCP integration

The 4 P0s share infrastructure:
- **All 4** call into `meok-governance-engine-mcp` (the orchestration layer) for cross-jurisdiction reasoning
- **MCP-001 + MCP-004** share the "consequential decision" / "high-risk AI" concept — colorado-admt is essentially a US state overlay on eu-ai-act
- **MCP-003 + MCP-004** share the consumer-protection pattern (consumer notice, human review)
- **MCP-004** depends on ETSI CABCA (MCP-004's continuous-assessment pattern)

The merge plan (see `MERGE_PLAN_2026_Q4.md`) unifies these patterns in Q4 2026 via `eu-ai-act-complete` (consolidates MCP-001's tree) and `regulatory-crosswalk-engine` (consolidates MCP-001 ↔ MCP-004 reasoning).

## Effort summary

| MCP | Effort | Start | MVP | Days to MVP |
|---|---|---|---|---:|
| MCP-001 eu-ai-act-high-risk-classifier | 4 weeks | Jun 8 | Jul 15 | 37 |
| MCP-003 china-ai-anthropomorphic | 3 weeks | Jun 8 | Jul 1 | 23 |
| MCP-004 etsi-cabca-continuous-conformity | 4 weeks | Jun 8 | Aug 1 | 54 |
| MCP-002 colorado-admt-compliance | 4 weeks | Jul 1 | Oct 1 | 92 |
| **Total** | **15 eng-weeks** (parallelizable to ~8 weeks with 2 engs) | | | |

## What blocks it (gating dependencies)

1. **The 5 manual Nick-gated blockers** (Stripe, Vercel, DNS, Resend, LinkedIn) — for the **distribution** of these 4 MCPs, not the build. The builds can ship to PyPI on Nick's existing token.
2. **Glama / Smithery / MCP.so submissions** (per `DISTRIBUTION_GAPS_2026-06-08.md`) — the 4 P0s are the highest-priority submissions to the 5 missing channels.
3. **MCP Security Cert RFC v0.1** — the certification standard the keystone already has a TOC for. The 4 P0s should be the first 4 MCPs to claim the certification.
4. **The 6→3 / 15-merge refactor** (Q4 2026) — these 4 P0s are the "stable name" anchors for the merge (the merged names like `eu-ai-act-complete` build on top of MCP-001).

## Cross-references

- `sov3-mcp-master-audit-2026-06-08.md` (memory) — the audit that defines these 4 P0s
- `MERGE_PLAN_2026_Q4.md` — the 15-merge refactor that these 4 P0s anchor
- `REGULATORY_CALENDAR_2026-2027.md` — the 17 regulatory deadlines ranked
- `ROADMAP_18_MONTH_2026-2027.md` — the 18-month quarterly plan
- `INDUSTRY_PACKS_2027_Q1.md` — the 7 industry packs that these 4 P0s feed into (esp. `ai-gov-essentials-pack` and `finserv-pack`)
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — the 25-day strike that ships these 4 P0s first
