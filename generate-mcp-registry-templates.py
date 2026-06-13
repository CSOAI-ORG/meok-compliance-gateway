#!/usr/bin/env python3
"""
BULK MCP REGISTRY TEMPLATE GENERATOR
Generates server.json + llms.txt + .well-known/mcp-server for all 14 flagships
"""

import json
from pathlib import Path

FLAGSHIPS = [
    ("eu-ai-act-compliance-mcp", "EU AI Act Compliance", "1.8.3", "Eu Ai Act (Regulation (EU) 2024/1689) compliance checking, risk classification, and documentation generation."),
    ("dora-compliance-mcp", "DORA Compliance", "1.6.2", "DORA (Regulation (EU) 2024/1687) compliance for financial ICT risk management."),
    ("nis2-compliance-mcp", "NIS2 Compliance", "1.5.1", "NIS2 (Directive (EU) 2022/2555) cybersecurity risk management for essential entities."),
    ("cra-compliance-mcp", "CRA Compliance", "1.4.0", "CRA (Regulation (EU) 2024/2847) compliance for AI system providers."),
    ("soc2-compliance-ai-mcp", "SOC 2 Compliance", "1.7.3", "SOC 2 Type II compliance for trust services criteria (security, availability, processing integrity, confidentiality, privacy)."),
    ("hipaa-compliance-mcp", "HIPAA Compliance", "1.9.1", "HIPAA compliance for healthcare AI systems handling PHI."),
    ("gdpr-compliance-ai-mcp", "GDPR Compliance", "1.10.2", "GDPR (Regulation (EU) 2016/679) compliance for AI systems processing personal data."),
    ("iso-42001-ai-mcp", "ISO 42001 Compliance", "1.3.4", "ISO/IEC 42001 AI management system compliance assessment."),
    ("csrd-compliance-mcp", "CSRD Compliance", "1.2.1", "CSRD (Regulation (EU) 2024/2848) sustainability reporting for AI systems."),
    ("bias-detection-mcp", "Bias Detection", "2.1.0", "AI bias detection and fairness assessment across 7 protected characteristics."),
    ("meok-governance-engine-mcp", "Governance Engine", "1.5.0", "Multi-framework governance engine with weighted voting and attestation."),
    ("meok-mcp-injection-scan-mcp", "Injection Scanner", "1.3.2", "Prompt injection and jailbreak detection for MCP servers."),
    ("agent-audit-logger-mcp", "Audit Logger", "1.1.5", "Immutable audit trail logging for agent actions with cryptographic signatures."),
    ("agent-policy-enforcement-mcp", "Policy Enforcement", "1.2.3", "Runtime policy enforcement for agent behavior and tool restrictions."),
]

TEMPLATE_SERVER_JSON = {
    "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
    "name": "CSOAI-ORG/{name}",
    "title": "{title}",
    "version": "{version}",
    "description": "{description} Part of the MEOK 28-hive MCP governance mesh. 13 unified frameworks + attestation chain.",
    "websiteUrl": "https://meok.ai/{name}",
    "repository": {
        "type": "git",
        "url": "https://github.com/CSOAI-ORG/{name}",
        "source": "https://github.com/CSOAI-ORG/{name}"
    },
    "icons": [{
        "src": "https://raw.githubusercontent.com/CSOAI-ORG/{name}/main/assets/icon.svg",
        "mimeType": "image/svg+xml",
        "sizes": ["256x256"],
        "theme": "dark"
    }],
    "packages": [{
        "registryType": "pypi",
        "identifier": "{name}",
        "version": "{version}",
        "transport": {"type": "stdio"}
    }],
    "_meta": {"io.modelcontextprotocol.registry/publisher-provided": {
        "category": "ai-governance",
        "subcategories": ["compliance", "audit"],
        "tier": "flagship",
        "openSsfScorecard": "7.06/10"
    }},
    "metadata": {"publisher": "MEOK AI Labs", "categories": ["compliance", "ai-governance"]},
    "examples": [{
        "name": "Quick scan via {name}",
        "description": "Run a compliance check using the MCP server.",
        "input": {"tool": "quick_scan", "arguments": {"system": "example"}}
    }],
    "resources": [
        {"uri": "https://docs.meok.ai/{name}/", "name": "{name} documentation", "mimeType": "text/html"},
        {"uri": "https://github.com/CSOAI-ORG/{name}", "name": "{name} on GitHub", "mimeType": "text/html"}
    ],
    "publisher": {"name": "CSOAI Ltd", "url": "https://csoai.org"},
    "categories": ["compliance", "ai-governance"]
}

def generate_server_json(name, title, version, description):
    data = json.loads(json.dumps(TEMPLATE_SERVER_JSON))
    data["name"] = f"CSOAI-ORG/{name}"
    data["title"] = title
    data["version"] = version
    data["description"] = f"{description} Part of the MEOK 28-hive MCP governance mesh. 13 unified frameworks + attestation chain."
    data["websiteUrl"] = f"https://meok.ai/{name}"
    data["repository"]["url"] = f"https://github.com/CSOAI-ORG/{name}"
    data["repository"]["source"] = f"https://github.com/CSOAI-ORG/{name}"
    data["icons"][0]["src"] = f"https://raw.githubusercontent.com/CSOAI-ORG/{name}/main/assets/icon.svg"
    data["packages"][0]["identifier"] = name
    data["packages"][0]["version"] = version
    data["examples"][0]["name"] = f"Quick scan via {name}"
    data["resources"][0]["uri"] = f"https://docs.meok.ai/{name}/"
    data["resources"][0]["name"] = f"{name} documentation"
    data["resources"][1]["uri"] = f"https://github.com/CSOAI-ORG/{name}"
    data["resources"][1]["name"] = f"{name} on GitHub"
    return json.dumps(data, indent=2)

def generate_llms_txt(name, title, version, description):
    return f"""# {name}
> {title} {description} By MEOK AI Labs.

## Install
pip install {name}

## Auth
- Free tier: 100 calls/month, no API key needed
- Pro tier: unlimited, set MEOK_API_KEY env var

## Tools

### quick_scan
Instant compliance check from a system description. No API key required.
- `system` (str): One-sentence AI system description
- Returns: compliance_status, top_obligations

### deadline_check
Regulatory deadlines with days remaining.
- Returns: List of dates with days_remaining

### framework_scan
Detailed compliance assessment.
- `framework` (str, required): {name.split("-")[0].upper()} or other framework
- `system` (str, required): System description
- Returns: compliance_score, gaps, remediation

## Endpoints
- MCP: https://gateway.meok.ai/mcp
- A2A: https://gateway.meok.ai/.well-known/agent-card.json

## License
MIT — https://github.com/CSOAI-ORG/{name}/blob/main/LICENSE
"""

if __name__ == "__main__":
    output_dir = Path("/Users/nicholas/meok-compliance-gateway/mcp-registry-templates")
    output_dir.mkdir(exist_ok=True)
    
    for name, title, version, description in FLAGSHIPS:
        repo_dir = output_dir / name
        repo_dir.mkdir(exist_ok=True)
        
        (repo_dir / "server.json").write_text(generate_server_json(name, title, version, description))
        (repo_dir / "llms.txt").write_text(generate_llms_txt(name, title, version, description))
        (repo_dir / ".well-known").mkdir(exist_ok=True)
        (repo_dir / ".well-known" / "mcp-server").write_text(json.dumps({
            "name": name,
            "description": description,
            "version": version
        }, indent=2))
        
    print(f"Generated templates for {len(FLAGSHIPS)} flagships in {output_dir}")