# MCP Security Certification Standard v0.1 — RFC

> **Status**: Request for Comments (RFC) — v0.1 draft
> **Authors**: MEOK AI Labs (CSOAI LTD, UK CH 16939677)
> **Date**: 2026-06-08
> **Aligned with**: EU AI Act Article 14 (Human Oversight), ISO 42001 Annex A.7 (AI System Verification), NIST AI RMF 1.0 (Governance)
> **Scope**: MCP servers deployed in production environments requiring regulatory compliance evidence

---

## Abstract

This document defines the **MCP Security Certification Standard (MSCS)** — a vendor-neutral, auditable certification framework for Model Context Protocol (MCP) servers. MSCS v0.1 establishes baseline security, governance, and compliance requirements that an MCP server must satisfy to be certified for production deployment in regulated environments (EU AI Act, DORA, NIS2, CRA, HIPAA, GDPR).

The standard is designed to be:
- **Machine-verifiable**: Every requirement maps to an automated check
- **Attestation-ready**: Produces cryptographically-signed evidence (Signet receipts)
- **Regulation-aligned**: Direct crosswalk to EU AI Act Articles 9, 10, 13, 14, 52; ISO 42001 Annex A; NIST AI RMF
- **Ecosystem-native**: Works with MCP, A2A, ANP, and x402 payment rails

---

## 1. Certification Levels

| Level | Name | Target Audience | Audit Depth |
|-------|------|-----------------|-------------|
| **L1** | **MSCS-Basic** | Self-hosted, low-risk tools | Automated static analysis + runtime smoke test |
| **L2** | **MSCS-Standard** | B2B SaaS, regulated industries | L1 + dynamic analysis + compliance matrix mapping |
| **L3** | **MSCS-Enhanced** | High-risk AI systems (EU AI Act Annex III) | L2 + BFT consensus audit + penetration testing |
| **L4** | **MSCS-Critical** | Safety-critical, financial, healthcare | L3 + formal verification + continuous monitoring |

---

## 2. Requirement Domains (10 Domains)

### 2.1 Transport & Protocol Security (MSCS-TR)
- **TR-1**: Streamable-HTTP transport with `Mcp-Method`, `Mcp-Name`, `MCP-Protocol-Version` headers (MCP 2026-07-28 spec)
- **TR-2**: TLS 1.3 termination at platform edge; no self-signed certs in production
- **TR-3**: DNS-rebinding protection disabled only with documented platform proxy IP allowlist
- **TR-4**: RFC 9728 `/.well-known/oauth-protected-resource` metadata published
- **TR-5**: Rate limiting per client (configurable; default 100 req/min)

### 2.2 Authentication & Authorization (MSCS-AA)
- **AA-1**: OAuth 2.1 / OIDC support with `mcp:tools`, `mcp:read`, `mcp:audit` scopes
- **AA-2**: x402 payment validation for gated tools (per-call USDC on Base/EVM)
- **AA-3**: Per-agent-pair IAM policies (allow/deny tool calls by agent identity)
- **AA-4**: Human-in-the-loop (HITL) gate for high-risk tool categories

### 2.3 Tool Descriptor Integrity (MSCS-TD)
- **TD-1**: Tool schema matches runtime behaviour (attested via `Mcp-Attestation` header)
- **TD-2**: No hidden/undocumented tools; all tools declared in `tools/list`
- **TD-3**: Input validation schemas (JSON Schema Draft 2020-12) for every tool
- **TD-4**: Output schema contracts with versioning

### 2.4 Audit Trail & Tamper Evidence (MSCS-AT)
- **AT-1**: Hash-chained audit log (Merkle-style) for every tool call
- **AT-2**: Signet Ed25519 receipt per audit entry (bilateral co-signing supported)
- **AT-3**: BFT consensus metadata (2f+1 quorum) for multi-party audit entries
- **AT-4**: Blockchain anchor hash (IPFS CID, Arweave txid, or deterministic SHA-256)
- **AT-5**: Exportable audit trail with integrity verification (`verify()` + `verify_signatures()`)

### 2.5 Compliance Matrix Mapping (MSCS-CM)
- **CM-1**: EU AI Act Article 9 (Risk Management) — mapped to tool `risk_assessment`
- **CM-2**: EU AI Act Article 10 (Data Governance) — mapped to tool `bias_detection`
- **CM-3**: EU AI Act Article 13 (Transparency) — mapped to tool `explainability_report`
- **CM-4**: EU AI Act Article 14 (Human Oversight) — mapped to tool `hitl_gate`
- **CM-5**: EU AI Act Article 52(3) (GenAI Disclosure) — mapped to tool `content_origin_tag`
- **CM-6**: DORA Article 6/11 (ICT Risk + Resilience Testing) — mapped to tool `ict_risk_framework`
- **CM-7**: NIS2 Article 21/23 (Supply Chain + Incident Reporting) — mapped to tool `supply_chain_audit`
- **CM-8**: CRA Article 10/13 (Vulnerability Handling + Auto-updates) — mapped to tool `vulnerability_disclosure`

### 2.6 Supply Chain & Provenance (MSCS-SC)
- **SC-1**: SBOM in CycloneDX 1.6 + SPDX 2.3 (EO 14028, NIS2, CRA)
- **SC-2**: AI Bill of Materials (CycloneDX AI) — model, data, training provenance
- **SC-3**: SLSA v1.0 Level 3+ build provenance (sigstore cosign + Rekor)
- **SC-4**: Dependency vulnerability scanning (OSV, GHSA) with 24h SLA for Critical

### 2.7 Runtime Security & Monitoring (MSCS-RM)
- **RM-1**: Red-team automation (prompt injection, tool poisoning, excessive agency)
- **RM-2**: Blue-team defensive monitoring (anomaly detection, policy violation alerts)
- **RM-3**: Continuous evaluation (drift detection, policy compliance scoring)
- **RM-4**: Generative fuzzing of tool inputs (edge-case failure surfacing)

### 2.8 Data Protection & Privacy (MSCS-DP)
- **DP-1**: GDPR Article 30 records of processing activities (ROPA) for MCP data flows
- **DP-2**: Article 22 automated decision-making audit trail
- **DP-3**: Data Subject Request (DSR) workflow via MCP tools
- **DP-4**: Cross-border transfer safeguards (SCC, BCR, adequacy decisions)

### 2.9 Incident Response & Resilience (MSCS-IR)
- **IR-1**: 24h incident notification (NIS2 Article 23, DORA Article 11)
- **IR-2**: Automated incident classification taxonomy (DORA + NIS2 aligned)
- **IR-3**: Rollback/remediation playbooks per tool category
- **IR-4**: Post-incident attestation with root-cause analysis

### 2.10 Governance & Certification Maintenance (MSCS-GV)
- **GV-1**: Annual re-certification; continuous monitoring for L3/L4
- **GV-2**: Change management: any tool schema change triggers re-verification
- **GV-3**: Councilof.ai BFT deliberation for certification decisions (quorum certificate)
- **GV-4**: Public transparency register: `proofof.ai/v/<cert_id>` verification

---

## 3. Certification Process

### 3.1 Application
1. Submit MCP server repository + deployed endpoint
2. Declare target certification level (L1–L4)
3. Provide compliance matrix mapping (self-assessment)

### 3.2 Automated Verification (CI/CD Gate)
```yaml
# .github/workflows/mscs-verification.yml
jobs:
  mscs-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run MSCS verifier
        run: |
          pip install mscs-verifier
          mscs verify --level L2 --endpoint ${{ secrets.MCP_ENDPOINT }}
```

### 3.3 Attestation Issuance
- On pass: `proofof.ai` issues signed attestation (Signet receipt)
- Certificate ID format: `MSCS-L2-<domain>-<YYYYMMDD>-<hash>`
- Valid for 12 months (L1/L2) or 6 months (L3/L4)

### 3.4 Continuous Monitoring
- L3/L4: Real-time `agentmemory` + `Cognee` monitoring
- Drift detection via `mex` (fail under score 90)
- Quarterly BFT consensus re-verification

---

## 4. Crosswalk Matrix (Normative)

| MSCS Req | EU AI Act | ISO 42001 | NIST AI RMF | DORA | NIS2 | CRA |
|----------|-----------|-----------|-------------|------|------|-----|
| TR-1     | —         | A.7.1     | GOVERN-1.1  | —    | —    | —   |
| AA-1     | Art 14    | A.7.2     | MAP-2.1     | Art 6| Art 21| —  |
| TD-1     | Art 13    | A.7.3     | MEASURE-2.3 | —    | —    | Art 10|
| AT-1     | Art 12    | A.7.4     | MANAGE-3.1  | Art 17| Art 23| —  |
| CM-1..8  | Art 9,10,13,14,52 | A.6 | MAP/MEASURE | Art 6,11 | Art 21,23 | Art 10,13 |
| SC-1     | Art 11    | A.8.1     | GOVERN-2.1  | —    | Art 21| Art 10|
| RM-1     | Art 9     | A.9.1     | MEASURE-1.2 | —    | —    | —   |
| DP-1     | —         | A.10.1    | —           | —    | —    | —   |
| IR-1     | Art 12    | A.11.1    | MANAGE-4.1  | Art 11| Art 23| —   |
| GV-1     | —         | A.12.1    | GOVERN-4.1  | —    | —    | —   |

---

## 5. Tooling Reference Implementation

| Component | Repository | Purpose |
|-----------|------------|---------|
| `mscs-verifier` | `github.com/CSOAI-ORG/mscs-verifier` | CI/CD gate + local CLI |
| `meok-compliance-gateway` | `github.com/CSOAI-ORG/meok-compliance-gateway` | Streamable-HTTP transport + x402 |
| `agentaudit` | `github.com/CSOAI-ORG/agentaudit` | OpenScore, Signet, BFT, audit trails |
| `meok-mcp-hardening-mcp` | `github.com/CSOAI-ORG/meok-mcp-hardening-mcp` | Red-team + hardening scanner |
| `meok-mcp-test-mcp` | `github.com/CSOAI-ORG/meok-mcp-test-mcp` | Golden-file + schema-drift tests |
| `proofof.ai` | `github.com/CSOAI-ORG/proofof.ai` | Attestation verification service |

---

## 6. Open Questions (RFC Feedback Requested)

1. **Certification Body**: Should MSCS be governed by a neutral foundation (like CNCF) or remain under CSOAI stewardship with multi-stakeholder council?
2. **Reciprocity**: How to align with existing certs (ISO 42001, SOC 2 Type II, Vanta, Drata)?
3. **Pricing**: L1 free (automated), L2 $500/server/yr, L3 $5K/server/yr, L4 custom — fair?
4. **Revocation**: Automated revocation on critical CVE (CVSS ≥ 9.0) within 24h?
5. **International**: US Executive Order 14110, UK AI Bill, Canada AIDA alignment?

---

## 7. References

- EU AI Act (Regulation (EU) 2024/1689) — Articles 9, 10, 11, 12, 13, 14, 52
- ISO/IEC 42001:2023 — AI Management System, Annex A
- NIST AI Risk Management Framework (AI RMF 1.0) — MAP, MEASURE, MANAGE, GOVERN
- DORA (Regulation (EU) 2022/2554) — Articles 6, 11, 17
- NIS2 (Directive (EU) 2022/2555) — Articles 21, 23
- CRA (Regulation (EU) 2024/2847) — Articles 10, 13
- MCP Specification 2025-03-26 / 2026-07-28 (upcoming)
- A2A Protocol Specification (Google)
- ANP (Agent Network Protocol) — Apache 2.0
- x402 Protocol Specification (Coinbase)

---

## 8. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v0.1 RFC | 2026-06-08 | MEOK AI Labs | Initial RFC draft for community review |

---

## Feedback

Submit comments via:
- GitHub Issues: `github.com/CSOAI-ORG/mscs-standard/issues`
- Email: `mscs@csoai.org`
- Councilof.ai deliberation: propose topic at `councilof.ai/mcp`

> **This is an RFC — not a final standard. Feedback welcome until 2026-07-15.**