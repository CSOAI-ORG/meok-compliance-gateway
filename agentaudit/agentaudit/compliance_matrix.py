"""EU AI Act / DORA / NIS2 / CRA  ←→  A2A Agent Card compliance matrix.

Aligned with OpenMoE-BFT Empire Layer 3 (OpenScore Safety Experts) and
Layer 8 (Compliance Gateway).  Each check maps to one or more safety
experts via safety_experts.py.
"""

from __future__ import annotations

import enum
import json
from dataclasses import dataclass, asdict


class Regulation(enum.Enum):
    EU_AI_ACT = "eu_ai_act"
    DORA = "dora"
    NIS2 = "nis2"
    CRA = "cra"


class RiskLevel(enum.Enum):
    MINIMAL = "minimal"
    LIMITED = "limited"
    HIGH = "high"
    UNACCEPTABLE = "unacceptable"


@dataclass(frozen=True)
class Check:
    """A single compliance check extracted from a regulation article."""
    id: str                # e.g. "eu-ai-act-52-3"
    regulation: Regulation
    article: str           # human-readable citation
    requirement: str       # one-sentence summary
    a2a_field: str | None  # A2A Agent Card field that carries the evidence
    mandatory: bool
    risk_trigger: RiskLevel | None = None
    expert_ids: tuple[int, ...] = ()  # OpenScore safety expert IDs


MATRIX: list[Check] = [
    # EU AI Act – High-risk systems (Annex III) → Expert #1
    Check("eu-ai-act-9",   Regulation.EU_AI_ACT, "Art. 9  — Risk management",
          "Continuous iterative risk management system", "metadata.riskAssessment", True, RiskLevel.HIGH, (1,)),
    Check("eu-ai-act-10",  Regulation.EU_AI_ACT, "Art. 10 — Data governance",
          "Training data governance + bias mitigation log", "metadata.trainingDataProvenance", True, RiskLevel.HIGH, (1,)),
    Check("eu-ai-act-13",  Regulation.EU_AI_ACT, "Art. 13 — Transparency",
          "Instructions for use / system card", "documentationUrl", True, RiskLevel.HIGH, (1,)),
    Check("eu-ai-act-14",  Regulation.EU_AI_ACT, "Art. 14 — Human oversight",
          "Natural persons able to oversee high-risk AI", "metadata.humanOversightContact", True, RiskLevel.HIGH, (1, 8)),
    Check("eu-ai-act-52-3", Regulation.EU_AI_ACT, "Art. 52(3) — GenAI disclosure",
          "AI-generated content must be marked", "metadata.contentOriginTag", True, RiskLevel.LIMITED, (1,)),
    Check("eu-ai-act-5-1-b", Regulation.EU_AI_ACT, "Art. 5(1)(b) — Unacceptable",
          "No social scoring by public authorities", "metadata.forbiddenUseCases", True, RiskLevel.UNACCEPTABLE, (1,)),

    # DORA → Expert #3
    Check("dora-6",  Regulation.DORA, "Art. 6 — ICT risk management",
          "Sound ICT risk-management framework", "metadata.ictRiskFramework", True, RiskLevel.HIGH, (3,)),
    Check("dora-11", Regulation.DORA, "Art. 11 — Digital operational resilience testing",
          "Periodic resilience testing program", "metadata.resilienceTestReport", True, RiskLevel.HIGH, (3,)),

    # NIS2 → Expert #3
    Check("nis2-21", Regulation.NIS2, "Art. 21 — Risk management",
          "Supply-chain security including data processing", "metadata.supplyChainAudit", True, RiskLevel.HIGH, (3,)),
    Check("nis2-23", Regulation.NIS2, "Art. 23 — Incident reporting",
          "Notify competent authority within 24h", "metadata.lastIncidentReport", True, RiskLevel.HIGH, (3,)),

    # CRA → Expert #3 (supply chain overlap)
    Check("cra-10", Regulation.CRA, "Art. 10 — Vulnerability handling",
          "Identify and remediate vulnerabilities", "metadata.vulnerabilityDisclosure", True, RiskLevel.HIGH, (3, 10)),
    Check("cra-13", Regulation.CRA, "Art. 13 — Exploits / auto-updates",
          "Automatic updates with rollback", "metadata.updatePolicy", True, RiskLevel.HIGH, (3,)),
]


def by_regulation(reg: Regulation) -> list[Check]:
    return [c for c in MATRIX if c.regulation == reg]


def by_risk(level: RiskLevel) -> list[Check]:
    return [c for c in MATRIX if c.risk_trigger == level]


def by_expert(eid: int) -> list[Check]:
    return [c for c in MATRIX if eid in c.expert_ids]


def to_json() -> str:
    return json.dumps([asdict(c) for c in MATRIX], indent=2, default=str)
