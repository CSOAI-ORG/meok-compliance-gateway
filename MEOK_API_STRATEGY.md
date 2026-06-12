# MEOK API Strategy — Gap Analysis + Implementation Roadmap

> **Authored**: 2026-06-08
> **Purpose**: synthesize the Kimi dossier's API analysis (`/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md`, 1,053 lines, 10 competitor API profiles + ecosystem matrix + gap analysis) into the keystone's API strategy and engineering roadmap.
> **Source**: `/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md` § "API Gap Analysis" + § "SOV3's API-First Strategy" + § "Recommended API Design for SOV3" + § "Strategic Recommendations".
> **Rubric**: per `RUBRIC_EXTERNAL_COMMS.md` — factual comparative, no war language. Banned vocabulary listed in § 8.

## 1. The 10 API gaps across all competitors

| # | Gap | Current state | MEOK opportunity |
|---:|---|---|---|
| 1 | **Unified AI governance API standard** | APIs fragmented (privacy, security, table) | First unified AI governance API spec |
| 2 | **Real-time AI governance event streaming** | Security event streams exist, not AI-specific | WebSocket/SSE for real-time AI governance events |
| 3 | **GraphQL for AI governance** | All REST-only | GraphQL endpoint for flexible queries |
| 4 | **gRPC for high-performance ops** | REST only, latency overhead | gRPC for high-throughput |
| 5 | **AI agent-specific governance APIs** | Generic APIs adapted | Native AI agent governance primitives |
| 6 | **Developer-first experience** | APIs as afterthought (only OneTrust + CrowdStrike have strong portals) | Developer-first API design |
| 7 | **OpenAPI/Swagger + auto-generated SDKs** | Inconsistent (OneTrust + MetricStream publish, others don't) | OpenAPI-first + 10+ language SDKs |
| 8 | **MCP native support** | Only OneTrust has MCP server | First AI governance platform with native MCP |
| 9 | **Multi-protocol API gateway** | REST-only everywhere | REST + GraphQL + gRPC + WebSockets in one gateway |
| 10 | **Self-service sandbox environments** | Limited (OneTrust has automated labs) | Instant sandbox provisioning |

## 2. The 3-phase API roadmap

### Phase 1: Core API (immediate — Q3 2026 LAUNCH)

1. **REST API** with OpenAPI 3.0 spec (the keystone's `http_server.py` already does this).
2. **OAuth 2.0 + API key** authentication (HMAC-signed tokens via the attestation substrate).
3. **Webhook** support for real-time events (event types listed in § 4).
4. **Python + TypeScript SDKs** (the keystone's existing flagship client surfaces are the seed).
5. **Developer portal** with interactive docs (meok.ai/developers).

### Phase 2: Advanced API (3-6 months — Q4 2026 SCALE)

1. **GraphQL API** for flexible queries.
2. **gRPC API** for high-performance operations.
3. **WebSocket** real-time event streaming (`/ws/v1/{agents,violations,trust-scores,alerts}` per the tech blueprint § 8.6).
4. **Go + Java + Rust SDKs**.
5. **Terraform Provider** for IaC integration.

### Phase 3: Ecosystem (6-12 months — Q1 2027 EXPAND)

1. **MCP Server** native support (the keystone already is one; expose the API as MCP tools).
2. **Multi-protocol API gateway** (single endpoint, multiple protocols).
3. **10+ language SDKs** (Ruby, PHP, .NET, Swift, Kotlin, Scala, Elixir, Clojure, Haskell, OCaml).
4. **Integration marketplace** (1-click install for Splunk, SentinelOne, Datadog, etc.).
5. **Partner developer program** (3rd parties build on MEOK APIs).

## 3. The recommended API architecture

```
MEOK API Gateway
├── REST API (v1)     - Standard CRUD operations        [shipped]
├── GraphQL API       - Flexible queries                [Phase 2]
├── gRPC API          - High-performance streaming      [Phase 2]
├── WebSocket API     - Real-time event subscriptions   [Phase 2]
└── MCP Server        - AI agent native integration     [shipped]
```

### Authentication options

```
├── OAuth 2.0 (Authorization Code + Client Credentials)   [shipped]
├── API Keys (scoped per environment)                       [shipped]
├── JWT Tokens (short-lived, rotating)                     [Phase 1]
├── mTLS (for high-security environments)                  [Phase 2]
└── SAML (enterprise SSO)                                  [Phase 3]
```

### Core API resources

```
/api/v1/
├── /use-cases           # AI use case governance
├── /models              # AI model registry
├── /agents              # AI agent governance
├── /vendors             # Third-party AI vendors
├── /policies            # Governance policies
├── /assessments         # Risk assessments
├── /audits              # Audit trails
├── /compliance          # Compliance status
├── /events              # Real-time events (SSE)
├── /webhooks            # Webhook management
├── /integrations        # Integration configs
├── /discovery           # Shadow AI discovery (per SHADOW_AI_DETECTION_MCP_SPEC.md)
├── /risk-scores         # Risk scoring
├── /reports             # Governance reports
└── /settings            # Platform settings
```

## 4. The 10 event types for webhooks/streaming

| Event | Trigger | MEOK tool / spec |
|---|---|---|
| `ai.usecase.created` | New AI use case registered | keystone inventory API |
| `ai.usecase.updated` | AI use case metadata changes | keystone inventory API |
| `ai.model.deployed` | New model deployment detected | Shadow AI MCP Tool 1 (egress) |
| `ai.model.drift.detected` | Model drift threshold breach | governance engine |
| `ai.agent.action.blocked` | Agent action blocked by policy | enforcement layer |
| `ai.agent.vulnerability.found` | MCP injection scanner finding | meok-mcp-injection-scan-mcp |
| `ai.policy.violation` | Policy engine rule fires | OPA/Rego policy engine |
| `ai.risk.score.changed` | Risk score recomputed | EU AI Act classifier |
| `ai.discovery.found` | New AI asset discovered | Shadow AI MCP Tool 4 (MCP registry) |
| `ai.compliance.status.changed` | Compliance status updated | 13-framework engine |

All events are HMAC-signed per `meok_x402.py:66-126` substrate, so subscribers can verify authenticity offline.

## 5. The 10 competitor API maturity scores

| Rank | Company | API Quality | Developer Experience | Integration Depth | Overall |
|---:|---|---:|---:|---:|---:|
| 1 | **OneTrust** | 9/10 | 9/10 | 9/10 | **9.0/10** |
| 2 | **CrowdStrike Falcon** | 8/10 | 8/10 | 9/10 | **8.3/10** |
| 3 | **Microsoft Graph** | 8/10 | 9/10 | 7/10 | **8.0/10** |
| 4 | **ServiceNow** | 7/10 | 7/10 | 8/10 | **7.3/10** |
| 5 | **Credo AI** | 6/10 | 7/10 | 5/10 | **6.0/10** |
| 6 | **MetricStream** | 6/10 | 6/10 | 6/10 | **6.0/10** |
| 7 | **Holistic AI** | 3/10 | 4/10 | 4/10 | **3.7/10** |
| 8 | **Zenity** | 2/10 | 3/10 | 5/10 | **3.3/10** |
| 9 | **Cranium AI** | 2/10 | 3/10 | 3/10 | **2.7/10** |
| 10 | **WitnessAI** | 1/10 | 2/10 | 2/10 | **1.7/10** |

## 6. The 10 competitor API gap scores (higher = more opportunity)

| Rank | Company | API Gaps | Webhook Gaps | SDK Gaps | Integration Gaps | Total Gap Score |
|---:|---|---|---|---|---|---:|
| 1 | **WitnessAI** | Critical | Critical | Critical | Critical | **10/10** |
| 2 | **Zenity** | Critical | Critical | Critical | High | **9/10** |
| 3 | **Cranium AI** | Critical | Critical | Critical | High | **9/10** |
| 4 | **Holistic AI** | Critical | Critical | High | Medium | **8/10** |
| 5 | **Credo AI** | Medium | High | Medium | Medium | **6/10** |
| 6 | **MetricStream** | Medium | High | High | Medium | **6/10** |
| 7 | **ServiceNow** | Medium | Medium | High | Low | **5/10** |
| 8 | **Microsoft Graph** | Low | Low | Low | Low | **3/10** |
| 9 | **CrowdStrike** | Low | Low | Low | Low | **3/10** |
| 10 | **OneTrust** | Low | Low | Low | Low | **2/10** |

**Reading**: WitnessAI, Zenity, Cranium are the "API-sitting ducks" — they have the worst APIs in the market. Their users are by definition "frustrated" by missing programmatic access. MEOK's API-first pitch lands hardest here.

## 7. The 5 strategic recommendations

1. **Be the first API-first AI governance platform.** Design API before UI. Publish OpenAPI spec day one. Auto-generate SDKs. Developer portal is a first-class product.
2. **Target the API gap sweet spot.**
   - **Primary targets**: Zenity, Cranium, WitnessAI users who need APIs.
   - **Secondary targets**: Credo AI, Holistic AI users frustrated by limited APIs.
   - **Tertiary targets**: ServiceNow, MetricStream users who want modern APIs.
3. **Multi-protocol API advantage.** Offer REST + GraphQL + gRPC + WebSockets. Let developers choose. Be the only platform with MCP native support.
4. **Integration depth as differentiator.** Native integrations with all major platforms. Terraform providers, Ansible collections. GitHub Actions, GitLab CI, Jenkins plugins. SIEM/SOAR connectors (Splunk, SentinelOne, Palo Alto).
5. **Developer experience as moat.** Interactive API explorer (GraphQL Playground-style). Instant sandbox environments. Per-tier rate limits published in docs. Webhook signing (HMAC) by default.

## 8. The 4 do-NOT-do rules (per RUBRIC + the audit's banned-vocab list)

1. **No war vocabulary.** Banned: kill shot, nuclear arsenal, coup de grâce, talent raid, seeding doubt, depletion campaign, strike while, vulnerability window, acquisition target, funding fiction.
2. **No specific-company failure references.** No "WitnessAI users are locked in and frustrated" (use "WitnessAI has the lowest API maturity in the market per this analysis — score 1.7/10").
3. **No feature parity overclaim.** MEOK is NOT 10x better at APIs than OneTrust (OneTrust scores 9/10). MEOK IS the only platform with multi-protocol + MCP-native. Frame precisely.
4. **No external quotes of $1.2T TAM or $48M run-rate.** The API gap data (10 competitors scored 1.7-9.0/10) IS external-safe — it's a tactical market-structure fact.

## 9. Cross-references

- `/Users/nicholas/meok-compliance-gateway/SOV3_UNIQUE_CAPABILITIES_MATRIX.md` — capability #7 (Multi-Protocol API) is this strategy.
- `/Users/nicholas/meok-compliance-gateway/SOV3_FINANCIAL_MODEL_2026-2028.md` — Stream 6 (API consumption) revenue = this strategy.
- `/Users/nicholas/meok-compliance-gateway/COMPARE_MATRIX_15_COMPETITORS.md` — API maturity column references this.
- `/Users/nicholas/meok-compliance-gateway/KEY_DIFFERENTIATORS.md` — differentiator #5 (35K MCP servers) requires the MCP-native API gap fill.
- `/Users/nicholas/meok-compliance-gateway/SHADOW_AI_DETECTION_MCP_SPEC.md` — 6 MCP tools wire to this API surface.
- `/Users/nicholas/meok-compliance-gateway/MCP_SECURITY_CERTIFICATION_STANDARD_v0.1_RFC.md` — Tier 3 cert audit uses this API.
- The keystone's `http_server.py` — the live REST API surface.
- The keystone's `meok_x402.py:66-126` — the HMAC signing substrate for events.
- The keystone's `meok-mcp-injection-scan-mcp` — uses this API for the `ai.agent.vulnerability.found` event.

## 10. Source pointers

- `/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md` § "API Gap Analysis" (10 gaps).
- `/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md` § "SOV3's API-First Strategy" (3 phases).
- `/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md` § "Recommended API Design for SOV3" (architecture + auth + resources + events).
- `/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md` § "Competitive Scoring Summary" (10 competitor scores).
- `/tmp/kimi_dossier_v2/research/deepdive_api_analysis.md` § "Strategic Recommendations for SOV3" (5 recommendations).
- `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § 4.7 (Multi-Protocol API capability).
- `/tmp/kimi_dossier_v2/sov3_tech_blueprint.agent.final.md` § 8.6 (WebSocket /ws/v1/* schemas).
- [[sov3-mcp-master-audit-2026-06-08]] — the audit memory with 13/15 GRC no-MCP finding.
