"""OpenScore Safety Experts — the 14-expert governance layer from the OpenMoE-BFT Empire spec.

See: OPENMOE_BFT_ALIGNMENT.md for cross-agent context.
Empire Spec: ../research/OPENMOE_BFT_EMPIRE_SPEC_v1.0.md (Layer 3)

Each expert is a forked or integrated open-source project that enforces one
compliance, security, or governance dimension.  AgentAudit maps A2A Agent Card
fields to the experts that validate them.
"""

from __future__ import annotations

import enum
import json
from dataclasses import dataclass, asdict
from typing import Any

from .compliance_matrix import Regulation


class ExpertDomain(enum.Enum):
    COMPLIANCE = "compliance"
    SECURITY = "security"
    GOVERNANCE = "governance"
    MONETIZATION = "monetization"
    VERIFICATION = "verification"


@dataclass(frozen=True)
class SafetyExpert:
    """One of the 14 OpenScore safety experts."""
    expert_id: int          # 1-14
    name: str
    source_repo: str        # upstream project we fork/integrate
    domain: ExpertDomain
    description: str
    regulation: Regulation | None = None
    a2a_field: str | None = None
    checks: tuple[str, ...] = ()   # compliance check IDs this expert validates


EXPERTS: list[SafetyExpert] = [
    SafetyExpert(
        1, "EU AI Act Compliance", "AIR Blackbox (fork)",
        ExpertDomain.COMPLIANCE,
        "Scans A2A Agent Cards against EU AI Act Annex III high-risk requirements",
        Regulation.EU_AI_ACT, "metadata.riskAssessment",
        ("eu-ai-act-9", "eu-ai-act-10", "eu-ai-act-13", "eu-ai-act-14",
         "eu-ai-act-52-3", "eu-ai-act-5-1-b"),
    ),
    SafetyExpert(
        2, "NIST RMF Risk Scoring", "DeepTeam (integration)",
        ExpertDomain.COMPLIANCE,
        "Continuous risk scoring using NIST AI Risk Management Framework",
        None, "metadata.nistRmfScore",
        (),
    ),
    SafetyExpert(
        3, "DORA / NIS2 Incident Taxonomy", "DORA ROI Validator (fork)",
        ExpertDomain.COMPLIANCE,
        "Maps ICT incidents to DORA Art. 23 and NIS2 Art. 21 taxonomies",
        Regulation.DORA, "metadata.ictRiskFramework",
        ("dora-6", "dora-11", "nis2-21", "nis2-23"),
    ),
    SafetyExpert(
        4, "Neurorights (GDPR Art 9)", "Custom (GDPR Art 9)",
        ExpertDomain.GOVERNANCE,
        "Protects special-category biometric / neural data under GDPR Article 9",
        None, "metadata.neurorightsPolicy",
        (),
    ),
    SafetyExpert(
        5, "x402 Payment Validation", "AgentMint + Signet (fork)",
        ExpertDomain.MONETIZATION,
        "Validates x402 micropayment tokens before gated tool execution",
        None, "metadata.x402Receipt",
        (),
    ),
    SafetyExpert(
        6, "MCP Tool Attestation", "Agent Security Harness",
        ExpertDomain.SECURITY,
        "Attests that MCP tool descriptors match runtime behaviour",
        None, "metadata.mcpAttestation",
        (),
    ),
    SafetyExpert(
        7, "Blockchain Verification", "liboqs (integration)",
        ExpertDomain.VERIFICATION,
        "Post-quantum ML-DSA-65 signatures for audit-trail anchoring",
        None, "metadata.blockchainAnchor",
        (),
    ),
    SafetyExpert(
        8, "Human-in-the-Loop Gate", "LangGraph Approval Hub (fork)",
        ExpertDomain.GOVERNANCE,
        "Requires human approval for high-risk agent actions",
        None, "metadata.hitlContact",
        (),
    ),
    SafetyExpert(
        9, "Red Team Automation", "RedAmon (fork) + PyRIT",
        ExpertDomain.SECURITY,
        "Autonomous adversarial testing of agent outputs",
        None, "metadata.redTeamReport",
        (),
    ),
    SafetyExpert(
        10, "Blue Team Defense", "Agent Security Harness",
        ExpertDomain.SECURITY,
        "Runtime defensive monitoring and anomaly detection",
        None, "metadata.blueTeamStatus",
        (),
    ),
    SafetyExpert(
        11, "Continuous Monitoring", "DeepTeam (integration)",
        ExpertDomain.SECURITY,
        "Ongoing evaluation of agent behaviour drift and policy violations",
        None, "metadata.continuousMonitoring",
        (),
    ),
    SafetyExpert(
        12, "Fuzzing / Mutation", "FuzzyAI (integration)",
        ExpertDomain.SECURITY,
        "Generative fuzzing of agent inputs to surface edge-case failures",
        None, "metadata.fuzzingReport",
        (),
    ),
    SafetyExpert(
        13, "Autonomous Auditor", "UI-TARS Desktop (ByteDance)",
        ExpertDomain.VERIFICATION,
        "Vision-driven autonomous UI auditing and compliance screenshot verification",
        None, "metadata.autonomousAudit",
        (),
    ),
    SafetyExpert(
        14, "Web Crawler / Extractor", "Firecrawl (integration)",
        ExpertDomain.VERIFICATION,
        "Autonomous web extraction for regulatory document ingestion",
        None, "metadata.webExtractionPolicy",
        (),
    ),
]


def by_id(eid: int) -> SafetyExpert | None:
    for e in EXPERTS:
        if e.expert_id == eid:
            return e
    return None


def by_domain(domain: ExpertDomain) -> list[SafetyExpert]:
    return [e for e in EXPERTS if e.domain == domain]


def by_regulation(reg: Regulation) -> list[SafetyExpert]:
    return [e for e in EXPERTS if e.regulation == reg]


def to_json() -> str:
    return json.dumps([asdict(e) for e in EXPERTS], indent=2, default=str)
