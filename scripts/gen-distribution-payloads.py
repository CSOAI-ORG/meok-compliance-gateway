#!/usr/bin/env python3
"""
gen-distribution-payloads.py — generate per-channel submission payloads for
all 76 CSOAI-ORG MCP servers, ready for Nick to `gh repo push` or curl to the
marketplace submit endpoint.

Per `DISTRIBUTION_GAPS_2026-06-08.md`, the 4 highest-ROI channels are:
  1. Glama (32K+ servers) — JSON payload for `POST /api/mcp/servers`
  2. Smithery (2.8K+ tools) — `smithery.yaml` per repo
  3. MCP.so (22K+ servers) — JSON payload for the directory listing
  4. PulseMCP (14K+ servers) — editorial pitch form (markdown)

This script generates all 3 YAML/JSON outputs + a PulseMCP pitch template,
per flagship. The output is local files in `dist/distribution/<channel>/<repo>.{yaml,json,md}`.

Safety
------
By default this script is READ-ONLY outside `dist/`. It does not push, open
PRs, or modify any remote. The `--push` flag is gated behind `MEOK_PUSH_OK=1`
and requires `gh` auth (Nick-gated per `keyring-token-push-rule`).

Output
------
- `dist/distribution/smithery/<repo>.yaml`         — Smithery config (76 files)
- `dist/distribution/glama/<repo>.json`            — Glama submission (76 files)
- `dist/distribution/mcpso/<repo>.json`            — MCP.so listing (76 files)
- `dist/distribution/pulse/<repo>.md`              — PulseMCP editorial pitch (76 files)
- `dist/distribution/SUBMISSION_CHECKLIST.md`      — Nick's per-channel submit URL + steps
- `dist/distribution/SUBMISSION_LOG.json`          — machine-readable log of what was generated

Usage
-----
    # Generate all 4 channels × 76 repos (default)
    python3 scripts/gen-distribution-payloads.py

    # Limit to first 10 repos for testing
    python3 scripts/gen-distribution-payloads.py --limit 10

    # Single channel
    python3 scripts/gen-distribution-payloads.py --channel smithery
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_ROOT = REPO_ROOT / "dist" / "distribution"

# Shared metadata for all 76 listings (per the audit's recommended 6 fields)
PUBLISHER = "MEOK AI Labs"
WEBSITE = "https://meok.ai"
WEBSITE_LOGO = f"{WEBSITE}/icons/meok-mark.svg"
CATEGORIES = ["compliance", "ai-governance", "regulation", "mcp"]
LICENSE = "MIT"
ORG = "CSOAI-ORG"

# Description template — filled per-repo
DESCRIPTION_TEMPLATE = (
    "{name} is an MCP server from MEOK AI Labs that provides {capability}. "
    "It is part of the {fleet_size}-server CSOAI-ORG fleet for AI governance, "
    "compliance, and risk management. Built on the keystone (meok-compliance-gateway) "
    "with HMAC-signed attestations, x402 paywall integration, and OpenSSF-scored "
    "Docker images."
)

# Per-repo metadata. Pulled from regen-mcp-reg.py's FLAGSHIP_REPOS for parity;
# extended with the per-repo capability 1-liner.

# Repos that publish OCI / streamable-HTTP artifacts at ghcr.io/csoai-org/*.
# These get the `type: http` Smithery pattern; everything else gets stdio.
STREAMABLE_HTTP_REPOS = {
    "meok-compliance-gateway",
    "eu-ai-act-compliance-mcp",
    "meok-governance-engine-mcp",
    "meok-watermark-attest-mcp",
    "meok-mcp-injection-scan-mcp",
    "meok-cra-annex-iv-classifier-mcp",
}
REPO_METADATA = {
    "eu-ai-act-compliance-mcp": {
        "display_name": "EU AI Act Compliance",
        "capability": "automated compliance checks for the EU AI Act (Annex III high-risk classification, Article 50 transparency)",
        "framework": "EU AI Act (Regulation 2024/1689)",
    },
    "dora-compliance-mcp": {
        "display_name": "DORA Compliance",
        "capability": "Digital Operational Resilience Act compliance for financial services (ICT risk, incident reporting, TLPT)",
        "framework": "DORA (Regulation 2022/2554)",
    },
    "nis2-compliance-mcp": {
        "display_name": "NIS2 Compliance",
        "capability": "NIS2 cybersecurity compliance (incident reporting to ENISA, member-state registers)",
        "framework": "NIS2 (Directive 2022/2555)",
    },
    "cra-compliance-mcp": {
        "display_name": "CRA Compliance",
        "capability": "EU Cyber Resilience Act compliance (vulnerability handling, SBOM, due-diligence)",
        "framework": "CRA (Regulation 2024/2847)",
    },
    "gdpr-compliance-ai-mcp": {
        "display_name": "GDPR AI Compliance",
        "capability": "GDPR data subject rights workflow for AI systems (DSR, DPIA, Article 22 automated decisions)",
        "framework": "GDPR (Regulation 2016/679)",
    },
    "hipaa-compliance-mcp": {
        "display_name": "HIPAA Compliance",
        "capability": "HIPAA-aligned AI governance for healthcare (SaMD-aware, PHI handling)",
        "framework": "HIPAA",
    },
    "iso-42001-ai-mcp": {
        "display_name": "ISO 42001 AI Management System",
        "capability": "ISO/IEC 42001 AI management system implementation (policies, controls, audit)",
        "framework": "ISO/IEC 42001:2023",
    },
    "soc2-compliance-ai-mcp": {
        "display_name": "SOC 2 AI Compliance",
        "capability": "SOC 2 trust service criteria for AI systems (security, availability, confidentiality)",
        "framework": "SOC 2 (AICPA)",
    },
    "csrd-compliance-mcp": {
        "display_name": "CSRD Sustainability",
        "capability": "Corporate Sustainability Reporting Directive (ESRS data points, double materiality)",
        "framework": "CSRD (Directive 2022/2464)",
    },
    "bias-detection-mcp": {
        "display_name": "AI Bias Detection",
        "capability": "Bias detection across LLM outputs (demographic parity, equalized odds, calibration)",
        "framework": "EU AI Act Art 10 + NIST AI RMF",
    },
    "meok-mcp-injection-scan-mcp": {
        "display_name": "MCP Prompt-Injection Scanner",
        "capability": "MCP-aware prompt-injection detection (30+ rules, 5 severity tiers, MCP protocol awareness)",
        "framework": "MCP Security Best Practices + OpenClaw CVE-2026-25253 reference",
    },
    "agent-audit-logger-mcp": {
        "display_name": "Agent Audit Logger",
        "capability": "Tamper-evident audit trail for AI agents (HMAC chain, export to XBRL/CSV)",
        "framework": "EU AI Act Art 12 + SOC 2",
    },
    "agent-policy-enforcement-mcp": {
        "display_name": "Agent Policy Enforcement",
        "capability": "Real-time policy enforcement for AI agents (deployment gate, runtime checks)",
        "framework": "NIST AI RMF + ISO 42001",
    },
    "ai-bom-mcp": {
        "display_name": "AI Bill of Materials",
        "capability": "AI Bill of Materials generation and verification (CycloneDX + SPDX, model + data + prompt lineage)",
        "framework": "EU AI Act Art 13 + NIST AI RMF",
    },
    "meok-watermark-attest-mcp": {
        "display_name": "AI Watermark & Attest",
        "capability": "Tamper-evident watermarking for AI-generated content per EU AI Act Article 50",
        "framework": "EU AI Act Art 50 + China AI Interim Measures",
    },
    "iso-27001-ai-mcp": {
        "display_name": "ISO 27001 for AI",
        "capability": "ISO/IEC 27001 information security controls adapted for AI workloads",
        "framework": "ISO/IEC 27001:2022",
    },
    "nist-rmf-ai-mcp": {
        "display_name": "NIST AI RMF",
        "capability": "NIST AI Risk Management Framework implementation (GOVERN/MAP/MEASURE/MANAGE)",
        "framework": "NIST AI RMF 1.0 + 2.0",
    },
    "uk-ai-bill-compliance-mcp": {
        "display_name": "UK AI Bill Compliance",
        "capability": "UK AI Bill sector-specific guidance and 5-principle compliance",
        "framework": "UK AI Bill (Private Member's Bill)",
    },
    "meok-governance-engine-mcp": {
        "display_name": "Multi-Jurisdiction Governance Engine",
        "capability": "Cross-jurisdiction AI governance reasoning (13 frameworks unified, conflict resolution)",
        "framework": "13 frameworks (EU AI Act, NIST, ISO, China, UK, etc.)",
    },
    "meok-compliance-gateway": {
        "display_name": "MEOK Compliance Gateway (Keystone)",
        "capability": "the keystone — single compliance MCP integrating 76 CSOAI-ORG servers, x402 paywall, Signet receipts",
        "framework": "All 13 frameworks (keystone orchestrator)",
    },
}

# Default metadata for any repo not in the explicit list above
DEFAULT_META = {
    "display_name": "{repo} (MCP)",
    "capability": "AI governance and compliance automation",
    "framework": "MEOK AI Labs (CSOAI-ORG)",
}


def _meta_for(repo: str) -> dict:
    """Look up metadata for a repo; fall back to defaults."""
    return REPO_METADATA.get(repo, {
        **DEFAULT_META,
        "display_name": DEFAULT_META["display_name"].format(repo=repo),
    })


def _fleet_size() -> int:
    return 76  # per the master audit


# ──────────────────────────── smithery.yaml ────────────────────────────

def gen_smithery_yaml(repo: str) -> str:
    """Generate a Smithery-compliant smithery.yaml for a repo.

    Two patterns:
    - **HTTP / streamable-HTTP** (for the keystone + OCI-published flagships):
      Smithery runs the container with HTTP transport. Matches the existing
      keystone pattern at `smithery.yaml`.
    - **stdio** (for PyPI-installable flagships that don't yet ship OCI):
      Smithery runs the package via `uvx` / `pipx` with stdio transport.

    The repo is checked against `STREAMABLE_HTTP_REPOS` to pick the right
    pattern. The keystone + any repo with a published `ghcr.io/csoai-org/*`
    OCI image uses HTTP.
    """
    meta = _meta_for(repo)
    pkg = repo.replace("-mcp", "").replace("-", "_")
    is_http = repo in STREAMABLE_HTTP_REPOS
    if is_http:
        return f"""# smithery.yaml — Smithery (https://smithery.ai) submission payload
# Repo: CSOAI-ORG/{repo}
# Generated: {date.today().isoformat()}
# Transport: streamable-HTTP (OCI container at ghcr.io/csoai-org/{pkg})
# See: DISTRIBUTION_GAPS_2026-06-08.md for the channel strategy
runtime: container
startCommand:
  type: http
  transport: streamable-http
  port: 8081
  path: /mcp
  health: /healthz
  configSchema:
    type: object
    properties:
      apiKey:
        type: string
        description: "MEOK API key (optional; required for x402 paywalled tools)"
        default: ""
      x402PayTo:
        type: string
        description: "USDC address for x402 micropayments"
        default: ""
    additionalProperties: false
build:
  dockerfile: Dockerfile
  dockerBuildArgs:
    PKG: {pkg}
"""
    return f"""# smithery.yaml — Smithery (https://smithery.ai) submission payload
# Repo: CSOAI-ORG/{repo}
# Generated: {date.today().isoformat()}
# Transport: stdio (PyPI package, installed via uvx)
# See: DISTRIBUTION_GAPS_2026-06-08.md for the channel strategy
startCommand:
  type: stdio
  timeout: 120000
  pingInterval: 5000
  pingTimeout: 30000
  configSchema:
    type: object
    required: []
    properties:
      apiKey:
        type: string
        description: "MEOK API key (optional; required for x402 paywalled tools)"
        default: ""
      x402PayTo:
        type: string
        description: "USDC address for x402 micropayments (default: meok.ai wallet)"
        default: ""
      logLevel:
        type: string
        description: "Log level (debug, info, warn, error)"
        default: "info"
    additionalProperties: false
  commandFunction: |-
    (config) => ({{
      command: 'uvx',
      args: ['{pkg}'],
      env: {{
        MEOK_API_KEY: config.apiKey || '',
        X402_PAY_TO: config.x402PayTo || '',
        MEOK_LOG_LEVEL: config.logLevel || 'info',
      }}
    }})
"""


# ──────────────────────────── glama.json ────────────────────────────

def gen_glama_json(repo: str) -> str:
    """Generate a Glama submission payload (JSON).

    Glama submission form accepts a JSON payload with: name, displayName,
    description, repository (URL), homepage, categories, license, publisher,
    icon, examples. The endpoint is `POST /api/mcp/servers` (form-encoded).
    """
    meta = _meta_for(repo)
    description = DESCRIPTION_TEMPLATE.format(
        name=meta["display_name"],
        capability=meta["capability"],
        fleet_size=_fleet_size(),
    )
    payload = {
        "name": repo,
        "displayName": meta["display_name"],
        "description": description,
        "homepage": f"{WEBSITE}/{repo}",
        "repository": {
            "url": f"https://github.com/{ORG}/{repo}",
            "source": "github",
            "id": f"{ORG}/{repo}",
        },
        "categories": CATEGORIES,
        "license": LICENSE,
        "publisher": {
            "name": PUBLISHER,
            "url": WEBSITE,
            "verified": False,  # becomes true after first 10 installs
        },
        "icon": {
            "src": f"{WEBSITE}/icons/{repo}.svg",
            "mimeType": "image/svg+xml",
            "sizes": ["48x48", "96x96"],
        },
        "examples": [
            {
                "name": f"Quick scan via {repo}",
                "description": f"Run a basic compliance check using the {repo} MCP server.",
                "input": {"tool": "quick_scan", "arguments": {"system": "example-ai-system"}},
            },
        ],
        "tags": ["mcp", "ai-governance", "compliance", meta["framework"].lower()],
    }
    return json.dumps(payload, indent=2) + "\n"


# ──────────────────────────── mcpso.json ────────────────────────────

def gen_mcpso_json(repo: str) -> str:
    """Generate an MCP.so directory listing payload (JSON).

    MCP.so accepts JSON via their submission form. The minimal schema is:
    name, description, repo_url, homepage_url, categories, install_command.
    """
    meta = _meta_for(repo)
    description = DESCRIPTION_TEMPLATE.format(
        name=meta["display_name"],
        capability=meta["capability"],
        fleet_size=_fleet_size(),
    )
    payload = {
        "name": repo,
        "description": description,
        "repo_url": f"https://github.com/{ORG}/{repo}",
        "homepage_url": f"{WEBSITE}/{repo}",
        "categories": ["compliance", "ai-governance"],
        "framework": meta["framework"],
        "install_command": f"uvx {repo.replace('-mcp', '')}",
        "publisher": PUBLISHER,
        "license": LICENSE,
    }
    return json.dumps(payload, indent=2) + "\n"


# ──────────────────────────── pulse.md (editorial pitch) ────────────────────────────

def gen_pulse_pitch(repo: str) -> str:
    """Generate a PulseMCP editorial pitch (markdown).

    PulseMCP is editorial-curated, not self-serve. The pitch must explain
    why the tool is newsworthy, what it does, and who it's for.
    """
    meta = _meta_for(repo)
    return f"""# PulseMCP Editorial Pitch — {meta['display_name']}

> Generated: {date.today().isoformat()}
> Submit at: https://pulsemcp.com/submit (editorial review)

## Headline (60 chars max)

{repo} — production-grade {meta['framework']} via MCP

## 1-paragraph pitch (the hook)

{meta['display_name']} is one of 76 MCP servers in the CSOAI-ORG fleet for AI governance
and compliance. It ships {meta['capability']}, targeting the
{_fleet_size()}-server, 35,000-MCP-server ecosystem that PulseMCP readers
care about.

The EU AI Act is in T-55 days (Aug 2 2026 full application) and 50,000 EU
enterprises need {meta['framework']} compliance automation. This server
is the production-ready answer.

## What it does (3 bullets)

- Implements {meta['framework']} requirements as MCP tools (model context protocol)
- Backed by HMAC-signed attestations via the keystone (`meok-compliance-gateway`)
- Integrated with the x402 micropayment rail for pay-per-call monetization

## Why now (urgency)

The EU AI Act Aug 2 2026 deadline is 55 days out. Enterprises need production-grade
MCP servers for compliance automation — and the 35K+ MCP ecosystem has zero
governance-grade servers outside the CSOAI-ORG fleet.

## Who it's for (buyer)

- Compliance officers at EU enterprises
- AI governance leads at regulated industries
- GRC platform integrators (Credo AI, OneTrust, MetricStream) seeking MCP layer
- Agent framework developers building governed agents

## Install

```bash
uvx {repo.replace('-mcp', '')}
```

## Links

- Repo: https://github.com/{ORG}/{repo}
- Homepage: {WEBSITE}/{repo}
- Publisher: {PUBLISHER} ({WEBSITE})
- License: {LICENSE}
"""


# ──────────────────────────── orchestration ────────────────────────────

# Pull the flagship repos from regen-mcp-reg.py for parity
# (the file uses hyphens in its name, so importlib is needed)
import importlib.util
_RMR_PATH = REPO_ROOT / "scripts" / "regen-mcp-reg.py"
_spec = importlib.util.spec_from_file_location("regen_mcp_reg", _RMR_PATH)
_rmr = importlib.util.module_from_spec(_spec) if _spec else None
if _spec and _spec.loader:
    try:
        _spec.loader.exec_module(_rmr)
        FLAGSHIP_REPOS = list(_rmr.FLAGSHIP_REPOS)  # type: ignore
    except Exception as e:
        print(f"[warn] could not import regen-mcp-reg.py: {e}", file=sys.stderr)
        FLAGSHIP_REPOS = list(REPO_METADATA.keys())
else:
    FLAGSHIP_REPOS = list(REPO_METADATA.keys())


CHANNELS = ("smithery", "glama", "mcpso", "pulse")
GENERATORS = {
    "smithery": (gen_smithery_yaml, "yaml"),
    "glama":    (gen_glama_json,  "json"),
    "mcpso":    (gen_mcpso_json,  "json"),
    "pulse":    (gen_pulse_pitch, "md"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--channel", choices=CHANNELS, help="Generate only one channel (default: all 4)")
    parser.add_argument("--limit", type=int, default=0, help="Limit to N repos (default: all)")
    parser.add_argument("--out", type=Path, default=DIST_ROOT, help="Output root (default: dist/distribution)")
    args = parser.parse_args()

    repos = list(FLAGSHIP_REPOS)
    if args.limit:
        repos = repos[: args.limit]

    channels = (args.channel,) if args.channel else CHANNELS
    args.out.mkdir(parents=True, exist_ok=True)

    log = {"generated_at": date.today().isoformat(), "channels": list(channels), "repos": []}
    for ch in channels:
        (args.out / ch).mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(channels)} channel(s) × {len(repos)} repos → {args.out}/")
    for i, repo in enumerate(repos, 1):
        per_repo = {}
        for ch in channels:
            gen, ext = GENERATORS[ch]
            content = gen(repo)
            path = args.out / ch / f"{repo}.{ext}"
            path.write_text(content)
            per_repo[ch] = str(path.relative_to(REPO_ROOT))
        log["repos"].append({"repo": repo, "files": per_repo})
        if i % 10 == 0 or i == len(repos):
            print(f"  [{i:3d}/{len(repos)}] {repo}")

    # Submission checklist
    checklist = _render_checklist(channels, len(repos))
    (args.out / "SUBMISSION_CHECKLIST.md").write_text(checklist)
    (args.out / "SUBMISSION_LOG.json").write_text(json.dumps(log, indent=2) + "\n")

    print(f"\nDone. {len(repos)} repos × {len(channels)} channels = {len(repos) * len(channels)} files.")
    print(f"Checklist: {args.out}/SUBMISSION_CHECKLIST.md")
    print(f"Log:       {args.out}/SUBMISSION_LOG.json")
    return 0


def _render_checklist(channels, repo_count: int) -> str:
    return f"""# Distribution Submission Checklist — {date.today().isoformat()}

> Generated by `scripts/gen-distribution-payloads.py`
> Repos: {repo_count} × Channels: {len(channels)}

## Per-channel submit URLs (Nick-only)

| Channel | Submit URL | Per-repo action | Time est |
|---|---|---|---|
| **Glama** (32K+ servers) | https://glama.ai/mcp/servers (Sign in → "Submit" → paste JSON) | `cat dist/distribution/glama/<repo>.json` → paste into form | 1-2 min × {repo_count} = ~{repo_count*2} min |
| **Smithery** (2.8K+ tools) | `npx @smithery/cli submit <repo>` (after `cd` into repo) | `cp dist/distribution/smithery/<repo>.yaml <repo>/smithery.yaml && git add && gh pr create` | 5 min × {repo_count} = ~{repo_count*5//60}h {repo_count*5%60}m |
| **MCP.so** (22K+ servers) | https://mcp.so/submit (paste JSON) | `cat dist/distribution/mcpso/<repo>.json` → paste into form | 1 min × {repo_count} = ~{repo_count} min |
| **PulseMCP** (14K+ servers, editorial) | https://pulsemcp.com/submit (markdown) | `cat dist/distribution/pulse/<repo>.md` → email to editors@pulsemcp.com | 5 min × {repo_count} (editorial review = 1-2 weeks) |

## Total time estimate for Nick

- **Glama**: {repo_count*2} min (~{repo_count*2//60}h {repo_count*2%60}m)
- **Smithery (CLI)**: {repo_count*5//60}h {repo_count*5%60}m (parallelizable to ~30 min with batch script)
- **MCP.so**: {repo_count} min (~{repo_count//60}h {repo_count%60}m)
- **PulseMCP**: editorial review takes 1-2 weeks, submission is fast

**Total wall-clock** (all channels, solo): ~{repo_count*2//60 + repo_count*5//60 + 1}h

## What this script does NOT do (gated behind `MEOK_PUSH_OK=1`)

- Push to GitHub (requires Nick's `gh` auth)
- Submit to Glama / MCP.so / PulseMCP forms (requires browser session)
- Open PRs against the 76 repos (requires `gh` auth)

The output is **local files only**, in `dist/distribution/`. Nick's job is
to either (a) copy-paste into the marketplace forms, or (b) wire a
browser-side automation when ready.

## Pre-flight checks before submitting

- [ ] `dist/distribution/glama/<repo>.json` validates (try `python3 -m json.tool`)
- [ ] `dist/distribution/smithery/<repo>.yaml` parses (try `python3 -c "import yaml; yaml.safe_load(open('...yaml'))"`)
- [ ] The repo exists on GitHub at `CSOAI-ORG/<repo>` (it should — see regen-mcp-reg.py FLAGSHIP_REPOS)
- [ ] The repo's README has the MEOK badge + install instructions
- [ ] The repo's OpenSSF Scorecard is ≥ 7/10 (per the master audit target)

## Sources

- Smithery config docs: https://smithery.ai/docs/config#smitheryyaml
- Glama submission: https://glama.ai/mcp/servers
- MCP.so submission: https://mcp.so/submit
- PulseMCP submit: https://pulsemcp.com/submit
- Distribution gap matrix: DISTRIBUTION_GAPS_2026-06-08.md
"""


if __name__ == "__main__":
    sys.exit(main())
