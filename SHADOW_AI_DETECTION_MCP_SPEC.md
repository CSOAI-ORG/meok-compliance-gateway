# Shadow AI Detection MCP — Spec

> **Authored**: 2026-06-08
> **Purpose**: spec for `meok-shadow-ai-discovery-mcp` (sister to the keystone's existing `meok-mcp-injection-scan-mcp`). Gap from `/tmp/kimi_dossier_v2/sov3_state_of_empire.agent.final.md` § 5.2 "What NOBODY Has" #3 — Shadow AI detection MCP.
> **Source**: `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` § 1.1 (AI System Inventory) + § 3.1 (Agent Discovery) + `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` (agent infrastructure).
> **Rubric**: factual comparative, no war language per `RUBRIC_EXTERNAL_COMMS.md`. Banned vocabulary in § 11.

## 1. The opportunity

- **The market gap**: 83% of enterprises have no AI inventory. Per the master audit, 13/15 GRC vendors have zero MCP presence — meaning zero MCP-native shadow AI discovery.
- **The competitive capability**: Holistic AI claims 300K+ prompts discovered (network-level). WitnessAI has network-level discovery. Cranium claims 30x visibility. **None have MCP-native exposure** — and none combine it with the keystone's 35,000+ MCP server governance layer.
- **The SOV3 unique position**:
  - 35,000+ MCP servers (Key Differentiator #5)
  - A2A protocol for agent-to-agent communication
  - The keystone's `meok-mcp-injection-scan-mcp` (the sister scanner)
  - The agentaudit server (A2A agent inventory)
  - The 13-framework engine (EU AI Act risk classifier)
- **Revenue angle**: Team tier ($29/mo) feature + Business tier ($49/mo) for full integration. 1,000 customers × $29 = $348K MRR; 200 customers × $49 = $588K MRR.

## 2. The 4 detection sources

| # | Source | Mechanism | Privacy | False-positive rate | Deployment friction |
|---:|---|---|---|---|---|
| 1 | **Network egress scanning** | Egress proxy intercepts TLS via JA3 fingerprint, classifies LLM API calls (OpenAI, Anthropic, Google, Cohere, etc.) | Metadata only (model, tokens, timestamp) — no prompt content | Low (5-10%) | Medium (proxy setup) |
| 2 | **Endpoint agent** | Lightweight Go/Rust binary on each managed device; watches process tree + DNS for LLM SDK patterns | Metadata only | Medium (10-15%) | Low (MDM deploy) |
| 3 | **Cloud logs** | Reads AWS CloudTrail / GCP Audit Logs / Azure Activity Log; filters for Bedrock / Vertex / Azure OpenAI / SageMaker invocations | Org-controlled (no MEOK-side storage) | Very low (<5%) | Low (read-only IAM) |
| 4 | **MCP server discovery** | Crawls the org's GitHub org for `server.json` files; decodes `metadata.publisher` + `name`; registers as known MCP | Public data only | None (deterministic) | None (no install) |

## 3. The 6 MCP tools

| # | Tool | Input | Output | OWASP/MCP category | Pricing |
|---:|---|---|---|---|---|
| 1 | `scan_egress` | `proxy_logs: list[ProxyLog]` (last 24h) | `DiscoveredAI` (model, endpoint, bytes, frequency) | OWASP LLM03 (training data poisoning) | $0.10 per 1K logs |
| 2 | `scan_endpoint` | `host_metrics: list[HostMetric]` (last 24h) | `DiscoveredAI` (process, DNS, model SDK) | OWASP LLM07 (system prompt leakage) | $0.10 per 1K host-metrics |
| 3 | `scan_cloud_logs` | `audit_events: list[AuditEvent]` (last 7d) | `DiscoveredAI` (Bedrock/Vertex/etc. invocations) | OWASP LLM05 (supply chain) | $0.10 per 1K events |
| 4 | `scan_mcp_registry` | `github_org: str` | `DiscoveredAI` (MCP servers in the org's GitHub) | MCP server governance | $0.50 per repo scanned |
| 5 | `classify_risk` | `system: DiscoveredAI` | `RiskClassification` (prohibited / high-risk / limited / out-of-scope) | EU AI Act risk classification | $0.01 per system (free, drives EU AI Act scanner funnel) |
| 6 | `register_inventory` | `system: DiscoveredAI` | `InventoryEntry` (HMAC-signed) | Inventory + attestation | $0.05 per entry |

All tools are `@paywalled` per the keystone's x402 pattern. Free tier = 1,000 calls/month. Team tier = 100K calls/month. Business tier = unlimited.

## 4. The 3 deployment modes

| # | Mode | Architecture | Privacy | Setup time |
|---:|---|---|---|---|
| 1 | **SaaS** | MEOK-hosted, customer forwards logs to a tenant-scoped endpoint | Customer controls retention (default 30d) | 1-click |
| 2 | **Self-hosted on-prem** | Docker image runs in customer's VPC, no egress | Data never leaves the VPC | 48h (MEOK SLA) |
| 3 | **Hybrid** | SaaS control plane + on-prem scanner | Aggregated metadata to control plane, raw data stays local | 1 week |

**The CRITICAL Fix compliance** (per `CRITICAL_FIXES_2026-06-08.md`):
- Container must run as non-root (Fix #1).
- API keys stored in keyring or chmod 600 file (Fix #2).
- HMAC-SHA256 signing key from AWS Secrets Manager / Vault / keyring (Fix #3).

## 5. The privacy + GDPR posture

- **The scanner must NOT log prompt contents.** Only metadata: model identifier, token count, timestamp, user agent. This is enforced in the code AND via a CI lint check that grep's for `print(.*prompt.*content)` and fails the build if any match.
- **Data retention: 30 days max**, HMAC-signed deletion audit trail. Customers can configure shorter (7d default for SaaS, customer-controlled for on-prem).
- **Right-to-erasure**: customer's Privacy Officer can issue `forget_tenant(tenant_id: str) → HMAC-signed deletion receipt`. All data for the tenant is deleted; the deletion is signed and archived (the user can prove deletion happened, and when).
- **DPIA template**: pre-built for EU customers. Available at `meok.ai/dpia-template` (HMAC-signed, 14-page GDPR-compliant template).
- **Public security whitepaper**: the scanner's data flow is documented in a 28-page whitepaper (HMAC-signed), available at `meok.ai/security/shadow-ai-whitepaper.pdf`.

## 6. The MCP-native integration (7 steps)

When the scanner discovers a new MCP server, it auto-wires the server into the MEOK governance layer:

1. **Step 1**: Scanner discovers a new MCP server (via Tool 1, 2, 3, or 4).
2. **Step 2**: Auto-checks the server against `meok-mcp-injection-scan-mcp` for prompt-injection risk. If risk > Medium, flags for review.
3. **Step 3**: Checks the server.json's 6 metadata fields (icons, websiteUrl, publisher, categories, examples, resources). If any are missing, suggests patches (per the keystone's `regen-mcp-reg.py` script's output).
4. **Step 4**: Checks the OpenSSF Scorecard for the server's GitHub repo. If score < 7.0, flags for review.
5. **Step 5**: Runs Tool 5 (EU AI Act risk classifier) on the discovered system. Writes the classification to the inventory.
6. **Step 6**: Writes an HMAC-signed attestation to the org's compliance ledger (signed by `MEOK_ATTESTATION_KEY` per Fix #3).
7. **Step 7**: Returns the inventory entry to the caller. The entry is queryable via `inventory.list_systems()` (also a Tool 7, not in the core 6).

## 7. The x402 paywall

| Tool | Per-call cost | Free tier (Business tier) |
|---|---:|---:|
| `scan_egress` | $0.10 per 1K logs | 1M logs/mo |
| `scan_endpoint` | $0.10 per 1K host-metrics | 5M host-metrics/mo |
| `scan_cloud_logs` | $0.10 per 1K audit events | 2M events/mo |
| `scan_mcp_registry` | $0.50 per repo | 1,000 repos/mo |
| `classify_risk` | $0.01 per system | Unlimited (drives the EU AI Act scanner funnel) |
| `register_inventory` | $0.05 per entry | Unlimited |

**Why `classify_risk` is nearly free**: it's the funnel into the EU AI Act free scanner (5-question risk assessment at `meok.ai/eu-check`). Volume matters; per-call revenue doesn't.

## 8. Build order (~2 weeks)

**Week 1**:
- Day 1-2: Tool 1 (scan_egress) + Tool 4 (scan_mcp_registry) — the two most-requested sources.
- Day 3-4: MCP-native integration (the 7 steps in § 6).
- Day 5: HMAC-signed inventory entry schema + verify URL.

**Week 2**:
- Day 6-7: Tool 2 (scan_endpoint) + Tool 3 (scan_cloud_logs).
- Day 8: Privacy + GDPR posture (§ 5) — DPIA template, whitepaper, deletion flow.
- Day 9: x402 paywall integration + 3 deployment modes (SaaS / self-hosted / hybrid).
- Day 10: Internal testing + dogfood on MEOK's own GitHub org.

**Stretch (post-week 2)**:
- Tool 5 (EU AI Act classifier) — wire to `eu-ai-act-compliance-mcp`.
- Tool 6 (register_inventory) — wire to the keystone's compliance ledger.
- Smithery / Docker / PulseMCP listings for the new MCP server.

## 9. The 5-lever revenue impact

| Lever | Math | Year-1 potential |
|---|---|---:|
| Team tier upsell | 1,000 customers × $29/mo × 12 | $348K ARR |
| Business tier upsell | 200 customers × $49/mo × 12 | $118K ARR |
| Enterprise on-prem | 20 deployments × $50K/yr | $1,000K ARR |
| x402 pay-per-call overflow | 10M calls × $0.10/1K avg | $10K ARR (loss-leader marketing) |
| Adjacency revenue (customers who buy Shadow AI buy MEOK 13-framework) | 200 × $5K avg = $1M | $1,000K ARR (Year-2+) |
| **Total Year-1 potential** | | **~$2.5M ARR** |

## 10. The 4 risks + mitigations

| Risk | Mitigation |
|---|---|
| 1. Network scanning may be blocked by corporate firewalls | Provide a transparent proxy mode + endpoint agent fallback. |
| 2. False positives (every LLM SDK looks like AI) | Confidence scoring (0-100) + human review queue for confidence < 80. |
| 3. GDPR violation if prompt content is logged | Enforce metadata-only in code + CI lint check that fails the build if prompt-content logging is detected. |
| 4. Competitor fast-follow (Holistic AI's 300K+ prompts claim, WitnessAI's network-level) | A2A + MCP-native integration is the moat — competitors would need to rebuild the agent-infrastructure layer. |

## 11. The 4 "do NOT do" rules

1. **Don't name-and-shame competitors.** No "Holistic AI's 300K is fake" or "WitnessAI's gateway is a SPOF." Factual comparison only.
2. **Don't use war vocabulary.** Banned: kill shot, nuclear arsenal, coup de grâce, talent raid, seeding doubt, depletion campaign, strike while, vulnerability window, acquisition target, funding fiction.
3. **Don't claim "the only" shadow AI solution.** Holistic AI and WitnessAI both have network-level discovery. The accurate claim is "the only MCP-native shadow AI MCP server."
4. **Don't log prompt contents.** This is enforced in code (CI lint) AND in policy (DPIA template + public whitepaper). The technical enforcement + the policy commitment = double safety.

## 12. Cross-references

- `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` — differentiator #5 (35K MCP servers).
- `/Users/nicholas/meok-compliance-gateway/PRICING.md` — 4 tiers (Team $29, Business $49).
- `/Users/nicholas/meok-compliance-gateway/CRITICAL_FIXES_2026-06-08.md` — 3 CRITICAL fixes this MCP must follow.
- `/Users/nicholas/meok-compliance-gateway/REGULATORY_CALENDAR_2026-2027.md` — 4 P0 deadlines = scanner urgency.
- `/Users/nicholas/meok-compliance-gateway/EU_AI_ACT_FREE_SCANNER_SPEC.md` — Tool 5 is the funnel into the EU scanner.
- `/Users/nicholas/meok-compliance-gateway/WATCHDOG_CERTIFICATION_PLATFORM_SPEC.md` — Tier-3 system certs should default to "Watchdog-certified" for Shadow AI MCPs.
- `/Users/nicholas/meok-compliance-gateway/COMPARE_MATRIX_15_COMPETITORS.md` — competitor comparison (Holistic AI, WitnessAI, Cranium).
- The keystone's `meok-mcp-injection-scan-mcp` (sister scanner, the prompt-injection layer).
- The agentaudit server (A2A agent inventory — also discovers AI; potential overlap/merger candidate).

## 13. Source pointers

- `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` § 1.1 + § 3.1.
- `/tmp/kimi_dossier_v2/research/deepdive_feature_matrix.md` "Nobody Has This" row 3 (Shadow AI detection).
- `/tmp/kimi_dossier_v2/sov3_state_of_empire.agent.final.md` § 5.2 gap #3 (industry-wide gap Nick can fill).
- `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` (agent infrastructure design — the A2A + MCP layer).
- `/tmp/kimi_dossier_v2/sov3_portfolio_inventory.md` (the meok-mcp-injection-scan-mcp entry, sister repo).
- [[sov3-mcp-master-audit-2026-06-08]] — the audit memory with 13/15 GRC no-MCP finding.
