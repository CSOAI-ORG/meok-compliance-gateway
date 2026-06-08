#!/usr/bin/env python3
"""
gen-hive.py — Generate the 7-layer hive config for one MEOK .ai domain.

Usage:
    python gen-hive.py <domain-name> \\
        --tier flagship \\
        --tools bias-detection-mcp,gdpr-compliance-ai-mcp \\
        --palette "privacy purple + GDPR blue" \\
        --out /tmp/hive-staging/biasdetectionof.ai-hive

Produces a directory of 9 files implementing the 7-layer hive stack
(see /Users/nicholas/.claude/projects/-Users-nicholas-meok-compliance-gateway/
memory/meok-hive-architecture-2026-06-07.md):
  - README.md              (human + AGENT entry point)
  - stack.yml              (7-layer config; canonical truth)
  - DESIGN.md              (Open Design palette — L7)
  - agent-card.json        (A2A Agent Card — L5)
  - hermes.yml             (L6 orchestrator config)
  - agentmemory.json       (L4 memory scope)
  - .mex/mex.yml           (L1 drift detection)
  - spawn.py               (EvoAgentX bootstrap)
  - .gitignore             (Python + hive artefacts)
  - LICENSE                (MIT)

Idempotent: re-running overwrites. Safe to invoke from a loop.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path
from textwrap import dedent

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

HIVE_GENESIS = "2026-06-07"
DEFAULT_PALETTE = "MEOK indigo + slate"
DEFAULT_LICENSE = "MIT"
HERMES_VERSION = "v2026.6.5"
AGENTMEMORY_VERSION = "v0.9.26"
MEMORIA_VERSION = "v0.4.0"
EVOAGENTX_VERSION = "v0.1.0"
MCP_VERSION = "1.27.2"

# ---------------------------------------------------------------------------
# Template generators (one per file)
# ---------------------------------------------------------------------------

def gen_readme(d: dict) -> str:
    return dedent(f"""\
    # {d['domain']} Hive 🐝

    > Per-domain 7-layer autonomous Hive. Part of the MEOK 25-hive mesh
    > (see [`meok-hive-architecture-2026-06-07`](https://github.com/CSOAI-ORG/meok-compliance-gateway/blob/chore/ci-hardening/FLEET_BASE.md)).

    **Domain:** `{d['domain']}`
    **Tier:** `{d['tier']}`
    **Genesis:** {HIVE_GENESIS}
    **Status:** scaffolded — awaiting deployment

    ## The 7 layers

    ```
    L7  PRESENTATION    {d['palette']} (Open Design)
    L6  ORCHESTRATION   Hermes sub-context (Kimi K2.6 / DeepSeek V3.5 / local)
    L5  DOMAIN MCP      {', '.join(d['tools']) or '(none yet)'}
    L4  AGENT MEMORY    agentmemory ({AGENTMEMORY_VERSION}) — {d['memory_mode']} mode
    L3  KNOWLEDGE GRAPH Cognee subgraph — scope: {d['cognee_scope']}
    L2  VERSIONED HIST  Memoria ({MEMORIA_VERSION}) — namespace "{d['domain'].split('.')[0]}"
    L1  DRIFT DETECTION mex — fail on score < 90
    ```

    ## Quickstart (one command, post-deploy)

    ```bash
    git clone https://github.com/CSOAI-ORG/{d['domain'].split('.')[0]}-hive
    cd {d['domain'].split('.')[0]}-hive
    pip install -r requirements.txt
    python spawn.py                  # EvoAgentX bootstrap
    python -m mex check              # L1 drift detection
    python -m server                 # L5 MCP server
    ```

    ## A2A Agent Card

    This hive publishes its capabilities at
    `https://{d['domain']}/.well-known/agent-card.json` — see `agent-card.json`.

    ## Cross-hive calls

    Per L6 (hermes.yml), this hive will only call MCPs from:
    - its own tool list (`L5`)
    - shared MEOK governance MCPs (csoai-governance-crosswalk-mcp, etc.)
    - other hives via A2A with explicit user consent

    ## Revenue

    {d['revenue']}

    ## Related

    - [MEOK Hive architecture](https://github.com/CSOAI-ORG/meok-compliance-gateway/blob/chore/ci-hardening/FLEET_BASE.md) — the genome
    - [MEOK global strategy](meok-global-strategy-2026-06-07) — 7 global moves
    - [Crown jewels](meok-crown-jewels-2026-06-07) — verified open-source stack
    """)


def gen_stack_yml(d: dict) -> str:
    # Build the tools list with proper YAML indentation (6 spaces under `tools:`)
    if d['tools']:
        tools_block = "\n".join(f"        - {t}" for t in d['tools'])
    else:
        tools_block = "        - (none yet)"
    return dedent(f"""\
    # {d['domain']} Hive — 7-layer config
    # Generated {HIVE_GENESIS} by gen-hive.py
    # Schema: meok-hive-architecture-2026-06-07 (memory file)

    hive:
      domain: {d['domain']}
      tier: {d['tier']}
      genesis: {HIVE_GENESIS}
      org: CSOAI-ORG
      repo: {d['domain'].split('.')[0]}-hive

    layers:
      L7_presentation:
        type: open_design
        palette: "{d['palette']}"
        exports: [html, mp4, pdf, pptx]
        hyperframes: true
        hosting: vercel  # or cloudflare_pages

      L6_orchestration:
        type: hermes_sub
        version: "{HERMES_VERSION}"
        scope: "I am the {d['domain']} assistant. I only call my own MCPs and
                shared MEOK MCPs. I do NOT call other clusters unless via A2A
                with explicit user consent."
        models:
          reasoning: kimi-k2.6
          speed: deepseek-v3.5
          privacy: local  # for PII / payments
        gateway:
          telegram: "@{d['domain'].split('.')[0].replace('-', '_')}_ai_bot"
          whatsapp: "+44-NNN-NNN-NNN"  # replace per hive
        cron:
          - "0 9 * * 1"  # weekly digest
          - "0 0 * * 0"  # weekly memoria backup

      L5_domain_mcp:
        type: fastmcp
        mcp_version: "{MCP_VERSION}"
        transport: streamable_http
        endpoint: /mcp
        port: 8000
        tools:
{tools_block}
        x402:
          enabled: {str(d['x402_enabled']).lower()}
          price_usd: "{d['x402_price']}"
          free_tier: "{d['free_tier']}"

      L4_agent_memory:
        type: agentmemory
        version: "{AGENTMEMORY_VERSION}"
        mode: {d['memory_mode']}  # shared | isolated
        recall_benchmark: 95.2%_R@5_LongMemEval-S
        tiered: true
        in_runtime: letta
        long_term: agentmemory

      L3_knowledge_graph:
        type: cognee
        scope: "{d['cognee_scope']}"
        entities: {json.dumps(d['entities'], ensure_ascii=False)}
        relations: {json.dumps(d['relations'], ensure_ascii=False)}
        gossip_interval_min: 15
        gossip_protocol: neo4j_streams

      L2_versioned_history:
        type: memoria
        version: "{MEMORIA_VERSION}"
        namespace: "{d['domain'].split('.')[0]}"
        branches: [main, "experiments/*", "prod-fixes/*"]
        audit_by: councilof.ai

      L1_drift_detection:
        type: mex
        fail_under: 90
        scoring: |
          score = 100
          score -= 10 * errors
          score -= 3  * warnings
          score -= 1  * infos
        ci_gate: true
    """)


def gen_design_md(d: dict) -> str:
    return dedent(f"""\
    # {d['domain']} — Open Design palette

    > Open Design (nexu-io) `od/DESIGN.md` format. Consumed by
    > the L7 presentation layer.

    ## Brand

    - **Name:** {d['domain']}
    - **Tier:** {d['tier']}
    - **Personality:** {d['personality']}
    - **Palette:** {d['palette']}

    ## Colors

    - **Primary:** `#5b21b6` (deep indigo)
    - **Secondary:** `#0f172a` (slate)
    - **Accent:** `#fbbf24` (amber)
    - **Success:** `#10b981`
    - **Warning:** `#f59e0b`
    - **Danger:**  `#ef4444`

    ## Typography

    - **Headings:** Inter, system-ui, sans-serif
    - **Body:** Inter, system-ui, sans-serif
    - **Code:** JetBrains Mono, monospace

    ## Voice

    {d['voice']}

    ## Components

    - Hero (HyperFrame — 30s auto-generated from agent transcripts)
    - Pricing table (3 tiers, £/mo)
    - Trust strip (logos, OpenSSF badge, EU AI Act compliance)
    - MCP call-out (`@mcp.tool()` examples)

    ## Exports

    - HTML landing (Vercel)
    - MP4 hero (HyperFrame)
    - PDF capability deck
    - PPTX investor pitch
    """)


def gen_agent_card(d: dict) -> str:
    return json.dumps({
        "name": d['domain'].split('.')[0],
        "description": d['personality'],
        "url": f"https://{d['domain']}",
        "version": "0.1.0",
        "provider": {
            "organization": "CSOAI-ORG",
            "url": "https://csoai.org"
        },
        "capabilities": {
            "streaming": True,
            "pushNotifications": False,
            "stateTransitionHistory": True
        },
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text", "json"],
        "skills": [
            {
                "id": t,
                "name": t,
                "description": f"Tool: {t} (part of {d['domain']} hive L5)"
            }
            for t in d['tools']
        ] + [
            {
                "id": "a2a-mesh",
                "name": "Cross-hive A2A call",
                "description": "Can call other MEOK hives via A2A (with user consent)"
            },
            {
                "id": "memoria-commit",
                "name": "Versioned memory commit",
                "description": f"Commits to memoria namespace '{d['domain'].split('.')[0]}'"
            }
        ],
        "securitySchemes": {
            "oauth2": {
                "type": "oauth2",
                "flows": {
                    "authorizationCode": {
                        "authorizationUrl": f"https://{d['domain']}/oauth/authorize",
                        "tokenUrl": f"https://{d['domain']}/oauth/token",
                        "scopes": {
                            "read": "Read hive state",
                            "write": "Invoke tools (x402-metered)",
                            "audit": "Read audit trail"
                        }
                    }
                }
            }
        },
        "x402Pricing": {
            "enabled": d['x402_enabled'],
            "currency": "USD",
            "amount": d['x402_price'],
            "freeCallsPerIPPerDay": d['free_tier']
        }
    }, indent=2)


def gen_hermes_yml(d: dict) -> str:
    tools_yaml = "\n".join(f"      - {t}" for t in d['tools']) or "      - (none yet)"
    return dedent(f"""\
    # {d['domain']} — Hermes sub-context
    # Hermes (Nous Research) v{HERMES_VERSION} — per-hive scope
    # See: https://github.com/NousResearch/hermes-agent

    hermes:
      version: "{HERMES_VERSION}"
      scope: "{d['domain']}"

      # MCP servers this sub-context can call
      mcp_servers:
        - name: "{d['domain'].split('.')[0]}-mcp"
          transport: streamable_http
          url: "http://localhost:8000/mcp"
          tools: [{', '.join(f'"{t}"' for t in d['tools'])}]

        # Shared MEOK governance MCPs (always available)
        - name: csoai-governance-crosswalk-mcp
          transport: streamable_http
          url: "https://csoai-governance-crosswalk-mcp.example.com/mcp"
        - name: councilof-agent-orchestrator-mcp
          transport: streamable_http
          url: "https://councilof.ai/mcp"

      # A2A peer hives
      a2a_peers:
        # Cross-hive calls go via A2A Agent Card discovery
        discovery_url: "/.well-known/agent-card.json"
        allowed_peers:
          # Filled per-hive based on real cross-hive revenue paths
          - "compliance.meok.ai"
          - "csoai.org"
          - "proofof.ai"

      models:
        primary: kimi-k2.6          # reasoning
        fast: deepseek-v3.5         # speed
        private: local-llama3-8b    # PII / payments

      memory:
        type: agentmemory
        mode: {d['memory_mode']}
        scope: "{d['domain'].split('.')[0]}"

      cron: []
      # Per-hive cron entries (filled by L6 of stack.yml)

      gateway:
        telegram:
          bot: "@{d['domain'].split('.')[0].replace('-', '_')}_ai_bot"
        whatsapp:
          number: "+44-NNN-NNN-NNN"  # replace per hive

      safety:
        max_tool_calls_per_request: 10
        max_total_tokens: 100000
        require_consent_for_a2a: true
        log_to_memoria: true
    """)


def gen_agentmemory_json(d: dict) -> str:
    return json.dumps({  # ensure_ascii=False via post-process
        "agent_id": d['domain'].split('.')[0],
        "agentmemory_agent_scope": d['memory_mode'],
        "version": AGENTMEMORY_VERSION,
        "storage": {
            "type": "local",
            "path": f".agentmemory/{d['domain'].split('.')[0]}/"
        },
        "tiered": {
            "in_runtime": {
                "type": "letta",
                "layers": ["core", "archival", "recall"]
            },
            "long_term": {
                "type": "agentmemory",
                "modes": ["working", "episodic", "semantic"]
            }
        },
        "recall_target": "95.2%_R@5_LongMemEval-S",
        "auto_capture": {
            "tool_use": True,
            "session_summaries": True,
            "compress_observations": True
        },
        "shared_pool": {
            "enabled": d['memory_mode'] == 'shared',
            "cross_hive_context": d['memory_mode'] == 'shared'
        },
        "isolated_overrides": d['isolated_overrides'],
        "links": {
            "memoria_namespace": d['domain'].split('.')[0],
            "cognee_subgraph": d['domain'].split('.')[0]
        }
    }, indent=2)


def gen_mex_yml(d: dict) -> str:
    return dedent(f"""\
    # mex — drift detection for {d['domain']} hive
    # mex (theDakshJaitly) — zero-AI, 8 checkers, 60% token reduction
    # See: https://github.com/theDakshJaitly/mex
    #
    # Run locally:  mex check
    # In CI:        fail build if score < 90

    version: 1
    hive: {d['domain']}
    fail_under: 90

    scoring:
      start: 100
      deductions:
        error: 10
        warning: 3
        info: 1

    checkers:
      - name: code_doc_sync
        type: builtin
        paths: ["{{*.py,*.md}}"]
      - name: imports_resolve
        type: builtin
        paths: ["{{server.py,http_server.py,spawn.py}}"]
      - name: dead_links
        type: builtin
        paths: ["{{*.md,*.yml,*.json}}"]
      - name: agent_card_valid
        type: custom
        script: scripts/check_agent_card.py
        target: agent-card.json
      - name: hermes_config_valid
        type: custom
        script: scripts/check_hermes.py
        target: hermes.yml
      - name: stack_yml_valid
        type: builtin
        target: stack.yml
      - name: design_md_present
        type: builtin
        target: DESIGN.md
      - name: no_secrets
        type: builtin
        patterns: ["*.pem", "*.key", "*credentials*"]

    ci:
      enabled: true
      on: [push, pull_request]
      branch: main
      fail_action: comment_and_block
    """)


def gen_spawn_py(d: dict) -> str:
    return dedent(f"""\
    #!/usr/bin/env python3
    \"\"\"EvoAgentX bootstrap for {d['domain']} hive.

    EvoAgentX (arXiv:2507.03616) autoconstructs agent workflows from
    a single prompt. Three SOTA optimizers built in:
      - TextGrad  (Nature 2025) — gradient-based prompt optimization
      - MIPRO     (arXiv:2406.11695) — Bayesian prompt optimization
      - AFlow     (arXiv:2410.10762) — MCTS-based workflow evolution

    HITL gate: domain owner (Nick) must approve before deployment.
    \"\"\"
    from __future__ import annotations
    import json
    import os
    from pathlib import Path

    import evoagentx  # pip install evoagentx=={EVOAGENTX_VERSION}

    HIVE_NAME = {json.dumps(d['domain'].split('.')[0])}
    PALETTE   = {json.dumps(d['palette'])}
    TOOLS     = {json.dumps(d['tools'])}

    def spawn():
        \"\"\"Build the multi-agent workflow for this hive.\"\"\"
        hive = evoagentx.spawn(
            domain=HIVE_NAME,
            tools=TOOLS,
            autonomy_level="supervised",   # HITL gate
            design_palette=PALETTE,
            initial_agents=__INITIAL_AGENTS__,
            evolution_loop="textgrad",
        )
        # HITL checkpoint: write a proposal for Nick to review
        proposal = Path("hive_proposal.json")
        proposal.write_text(json.dumps({{
            "hive": HIVE_NAME,
            "agents": hive.agents,
            "workflow": hive.workflow,
            "tools": TOOLS,
            "estimated_token_cost_per_request": hive.estimate_cost(),
        }}, indent=2))
        print("Wrote " + str(proposal) + ". Nick must approve before deployment.")
        return hive

    if __name__ == "__main__":
        spawn()
    """)


def gen_gitignore() -> str:
    return dedent("""\
    # Python
    __pycache__/
    *.py[cod]
    *.egg-info/
    .venv/
    venv/

    # Hive artefacts
    .agentmemory/
    .memoria/
    .cognee/
    .mex/cache/

    # Secrets
    .env
    .env.*
    *.pem
    *.key

    # Editor
    .vscode/
    .idea/
    .DS_Store

    # Build
    dist/
    build/
    """)


def gen_license() -> str:
    year = date.fromisoformat(HIVE_GENESIS).year
    return dedent(f"""\
    MIT License

    Copyright (c) {year} CSOAI-ORG

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """)


# ---------------------------------------------------------------------------
# Domain registry — the 25 customer + 3 infra hives
# ---------------------------------------------------------------------------

DOMAIN_REGISTRY = [
    # Flagship
    {
        "domain": "meok.ai", "tier": "flagship",
        "tools": ["meok-attestation-api", "meok-compliance-gateway"],
        "palette": "MEOK indigo + electric cyan",
        "personality": "The customer-facing compliance portal — B2B dashboard, attestation verifier, API-key manager.",
        "voice": "Authoritative, calm, audit-grade. Speaks in compliance clauses and EU AI Act articles.",
        "memory_mode": "shared",
        "cognee_scope": "compliance obligations, attestations, customers, EU AI Act articles, audit trails",
        "entities": ["attestation", "customer", "obligation", "evidence", "audit_log"],
        "relations": ["attestation→customer", "attestation→obligation", "obligation→evidence"],
        "initial_agents": ["Attestation Issuer", "Compliance Officer", "API-Key Manager"],
        "x402_enabled": True, "x402_price": "0.05", "free_tier": "1",
        "isolated_overrides": ["payment_data_meokai"],
        "revenue": "Stripe self-serve on compliance.meok.ai; x402 micro-charges on per-attestation lookups.",
        "pricing_tier": "business_49", "seat_price_usd": "49", "monthly_floor_usd": "4900",
        "stripe_live_ready": False, "vercel_deployed": False,
        "faq": [
            {"q": "How does MEOK pricing compare to Vanta/Drata/OneTrust?", "a": "10-20x undercut for enterprise tier ($50-200K/yr vs $120-500K/yr); 1000-10000x for low-volume agent-to-agent calls via x402 micro-settlement."},
            {"q": "Is my organization prepared for the EU AI Act?", "a": "78% of EU enterprises are not yet prepared per the latest Commission impact assessment; phased enforcement runs through August 2027. MEOK ships turnkey Article 10/12/13/30 evidence stack."},
        ],
    },
    {
        "domain": "csoai.org", "tier": "flagship",
        "tools": ["csoai-governance-crosswalk-mcp", "a2a-governance-bridge-mcp", "csrd-compliance-mcp", "dora-compliance-mcp", "eu-ai-act-compliance-mcp"],
        "palette": "governance gold + deep navy",
        "personality": "The FAA for AI — independent governance institution, multi-jurisdiction crosswalk.",
        "voice": "Regal, deliberative, multi-stakeholder. Speaks in jurisdictions and consensus statements.",
        "memory_mode": "shared",
        "cognee_scope": "governance frameworks, jurisdictions, audit reports, EU AI Act, NIST AI RMF, ISO 42001",
        "entities": ["framework", "jurisdiction", "audit", "obligation", "consensus"],
        "relations": ["framework→jurisdiction", "audit→framework", "obligation→jurisdiction"],
        "initial_agents": ["Governance Analyst", "Cross-Mapping Specialist", "Audit Lead", "Council Recorder"],
        "x402_enabled": True, "x402_price": "3.00", "free_tier": "0",
        "isolated_overrides": [],
        "revenue": "£1,499/mo Enterprise suite, £5,000 48h audit (per DOMAINS.md). Per-call x402 re-priced $1.50→$3.00 (high-trust audit, justified per [[meok-deep-audit-2026-06-08]] P1-2).",
        "pricing_tier": "enterprise_custom", "seat_price_usd": "200", "monthly_floor_usd": "50000",
        "stripe_live_ready": False, "vercel_deployed": False,
        "faq": [
            {"q": "How does MEOK pricing compare to Vanta/Drata/OneTrust?", "a": "10-20x undercut for enterprise tier ($50-200K/yr vs $120-500K/yr); 1000-10000x for low-volume agent-to-agent calls via x402 micro-settlement."},
        ],
    },
    {
        "domain": "proofof.ai", "tier": "flagship",
        "tools": ["meok-attestation-api"],
        "palette": "proof green + trust blue",
        "personality": "Attestation verification — `proofof.ai/v/<cert_id>` returns signed compliance evidence.",
        "voice": "Precise, forensic, evidence-first. Speaks in certificate IDs and signature fingerprints.",
        "memory_mode": "shared",
        "cognee_scope": "attestations, signing keys, certificate chains, signed evidence",
        "entities": ["attestation", "signing_key", "evidence", "verifier"],
        "relations": ["attestation→signing_key", "attestation→evidence", "verifier→attestation"],
        "initial_agents": ["Attestation Verifier", "Signature Inspector", "Trust Score Calculator"],
        "x402_enabled": True, "x402_price": "10.00", "free_tier": "1",
        "isolated_overrides": [],
        "revenue": "£5/attestation lookup. Easiest new revenue line in the portfolio (DOMAINS.md). Per-call x402 re-priced $5→$10 (signed-attestation value vs web search; [[meok-deep-audit-2026-06-08]] P1-2).",
        "pricing_tier": "business_49", "seat_price_usd": "49", "monthly_floor_usd": "4900",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "cobolbridge.ai", "tier": "flagship",
        "tools": ["cobol-bridge-mcp"],
        "palette": "mainframe bronze + modern steel",
        "personality": "COBOL → modern language translator for banks, insurers, government.",
        "voice": "Senior-engineer, methodical, EBCDIC-fluent. Speaks in copybooks, CICS regions, JCL steps.",
        "memory_mode": "isolated",
        "cognee_scope": "COBOL copybooks, CICS regions, JCL, VSAM, EBCDIC, target languages (Java/Go/Python)",
        "entities": ["copybook", "cics_region", "jcl_step", "vsam_file", "ebcdic_record"],
        "relations": ["copybook→vsam_file", "jcl_step→program", "cics_region→copybook"],
        "initial_agents": ["Copybook Parser", "CICS Bridge", "JCL Scanner", "VSAM Mapper", "EBCDIC Translator"],
        "x402_enabled": True, "x402_price": "2.00", "free_tier": "0",
        "isolated_overrides": ["customer_source_code"],
        "revenue": "£199/mo Pro + £1,999/mo Enterprise + £290k/enterprise project floor.",
        "pricing_tier": "enterprise_custom", "seat_price_usd": "150", "monthly_floor_usd": "19990",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    # Governance bundle (9)
    {
        "domain": "accountabilityof.ai", "tier": "governance",
        "tools": ["ai-incident-reporting-mcp", "ai-self-audit-mcp", "a2a-governance-bridge-mcp"],
        "palette": "audit red + ledger grey",
        "personality": "AI incident reporting + tamper-evident audit trail.",
        "voice": "Forensic, blame-free, evidentiary. Speaks in incident IDs and root-cause analyses.",
        "memory_mode": "shared",
        "cognee_scope": "AI incidents, audit trails, root causes, post-mortems",
        "entities": ["incident", "root_cause", "post_mortem", "audit_trail"],
        "relations": ["incident→root_cause", "incident→audit_trail", "post_mortem→incident"],
        "initial_agents": ["Incident Reporter", "Root-Cause Analyst", "Audit Trail Curator"],
        "x402_enabled": True, "x402_price": "0.50", "free_tier": "1",
        "isolated_overrides": [],
        "revenue": "Bundle with csoai.org suite.",
        "pricing_tier": "team_29", "seat_price_usd": "29", "monthly_floor_usd": "2900",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "agisafe.ai", "tier": "governance",
        "tools": ["care-membrane-mcp", "ai-self-audit-mcp", "deepfake-detector-mcp"],
        "palette": "AGI safety amber + frontier black",
        "personality": "AGI safety research hub — frontier-model governance.",
        "voice": "Cautious, peer-reviewed, citation-heavy. Speaks in alignment papers and capability evaluations.",
        "memory_mode": "shared",
        "cognee_scope": "AGI safety research, alignment papers, capability evaluations, frontier-model incidents",
        "entities": ["paper", "evaluation", "incident", "alignment_proposal"],
        "relations": ["paper→alignment_proposal", "evaluation→model", "incident→alignment_proposal"],
        "initial_agents": ["Safety Researcher", "Capability Evaluator", "Alignment Theorist"],
        "x402_enabled": False, "x402_price": "0.00", "free_tier": "100",
        "isolated_overrides": [],
        "revenue": "Research hub; csoai.org traffic absorber. Or flip for $10-25k.",
        "pricing_tier": "micro_free", "seat_price_usd": "0", "monthly_floor_usd": "0",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "asisecurity.ai", "tier": "governance",
        "tools": ["cybersecurity-ai-mcp", "owasp-agentic-mcp", "security-scanner-ai-mcp"],
        "palette": "CISO black + threat red",
        "personality": "AI security for AI systems — defensive, threat-modelling.",
        "voice": "Threat-modeller, red-team, paranoia-as-virtue. Speaks in CVEs and attack surfaces.",
        "memory_mode": "shared",
        "cognee_scope": "AI security threats, CVEs, attack surfaces, defensive patterns",
        "entities": ["threat", "cve", "attack_surface", "defense_pattern"],
        "relations": ["threat→cve", "threat→attack_surface", "defense_pattern→threat"],
        "initial_agents": ["Threat Modeller", "Red Team Lead", "Defense Advisor"],
        "x402_enabled": True, "x402_price": "0.30", "free_tier": "1",
        "isolated_overrides": [],
        "revenue": "Bundle with csoai.org suite. CISOs as buyers.",
        "pricing_tier": "business_49", "seat_price_usd": "49", "monthly_floor_usd": "4900",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "biasdetectionof.ai", "tier": "governance",
        "tools": ["bias-detection-mcp"],
        "palette": "fairness purple + equity teal",
        "personality": "EU AI Act Article 10 — data and model bias detection.",
        "voice": "Statistical, fair-minded, demographic-aware. Speaks in disparate impact ratios and proxy variables.",
        "memory_mode": "shared",
        "cognee_scope": "bias metrics, protected attributes, EU AI Act Article 10, fair-lending rules",
        "entities": ["bias_metric", "protected_attribute", "model", "dataset"],
        "relations": ["bias_metric→model", "model→dataset", "bias_metric→protected_attribute"],
        "initial_agents": ["Bias Auditor", "Fair-Lending Analyst", "Dataset Inspector"],
        "x402_enabled": True, "x402_price": "0.10", "free_tier": "3",
        "isolated_overrides": [],
        "revenue": "£299/mo (cheapest single-MCP SaaS; fastest to monetise per DOMAINS.md).",
        "pricing_tier": "team_29", "seat_price_usd": "29", "monthly_floor_usd": "299",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "dataprivacyof.ai", "tier": "governance",
        "tools": ["dataprivacy-ai-mcp", "gdpr-compliance-ai-mcp", "hipaa-compliance-mcp"],
        "palette": "privacy purple + GDPR blue",
        "personality": "AI-native privacy compliance — GDPR + EU AI Act.",
        "voice": "DPO, lawful-basis-first, data-subject-rights. Speaks in Article 30 records and DSRs.",
        "memory_mode": "isolated",
        "cognee_scope": "data subjects, processing activities, lawful bases, GDPR articles, DSRs",
        "entities": ["data_subject", "processing_activity", "lawful_basis", "dsr", "cross_border_transfer"],
        "relations": ["processing_activity→data_subject", "dsr→data_subject", "cross_border_transfer→processing_activity"],
        "initial_agents": ["DPO Assistant", "DSR Handler", "Cross-Border Transfer Advisor"],
        "x402_enabled": True, "x402_price": "0.20", "free_tier": "1",
        "isolated_overrides": ["data_subject_pii"],
        "revenue": "Bundle with biasdetectionof.ai + accountabilityof.ai as GDPR+EU AI Act package.",
        "pricing_tier": "business_49", "seat_price_usd": "49", "monthly_floor_usd": "4900",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "ethicalgovernanceof.ai", "tier": "governance",
        "tools": ["meok-governance-engine-mcp", "care-membrane-mcp", "ai-bom-mcp", "explainability-report-mcp"],
        "palette": "ethics indigo + care pink",
        "personality": "Ethics-first governance — the moral reasoning layer.",
        "voice": "Philosopher-engineer, principles-first, multi-stakeholder. Speaks in trade-offs and value alignment.",
        "memory_mode": "shared",
        "cognee_scope": "ethical frameworks, value alignment, AI BOM, explainability",
        "entities": ["framework", "value", "trade_off", "ai_bom"],
        "relations": ["framework→value", "trade_off→value", "ai_bom→model"],
        "initial_agents": ["Ethics Reviewer", "AI BOM Curator", "Explainability Writer"],
        "x402_enabled": False, "x402_price": "0.00", "free_tier": "5",
        "isolated_overrides": [],
        "revenue": "Redirect to csoai.org (don't dilute brand).",
        "pricing_tier": "micro_free", "seat_price_usd": "0", "monthly_floor_usd": "0",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "safetyof.ai", "tier": "governance",
        "tools": ["care-membrane-mcp", "ai-incident-reporting-mcp", "deepfake-detector-mcp"],
        "palette": "safety green + alert amber",
        "personality": "Safety monitoring dashboard for deploying enterprises.",
        "voice": "SRE-style, alert-first, MTTR-aware. Speaks in incidents and mitigations.",
        "memory_mode": "shared",
        "cognee_scope": "AI safety incidents, monitoring metrics, mitigation patterns",
        "entities": ["incident", "metric", "mitigation", "alert"],
        "relations": ["incident→metric", "mitigation→incident", "alert→metric"],
        "initial_agents": ["Safety Monitor", "Mitigation Planner", "Alert Router"],
        "x402_enabled": True, "x402_price": "5.00", "free_tier": "1",
        "isolated_overrides": [],
        "revenue": "Landing page pointing at csoai.org suite. Per-call x402 re-priced $0.40→$5.00 (safety monitoring = high-value enterprise; [[meok-deep-audit-2026-06-08]] P1-2).",
        "pricing_tier": "team_29", "seat_price_usd": "29", "monthly_floor_usd": "2900",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "transparencyof.ai", "tier": "governance",
        "tools": ["explainability-report-mcp", "ai-bom-mcp", "watermarking-authenticity-mcp"],
        "palette": "clarity white + transparency sky",
        "personality": "Explainability — what your AI decided and why. The FinServ/Health ticket.",
        "voice": "Plain-language, regulator-friendly, step-by-step. Speaks in feature importances and decision paths.",
        "memory_mode": "shared",
        "cognee_scope": "model decisions, feature importances, decision paths, watermarks, BOM",
        "entities": ["decision", "feature", "decision_path", "watermark", "ai_bom"],
        "relations": ["decision→decision_path", "decision→feature", "watermark→model"],
        "initial_agents": ["Explainability Writer", "BOM Curator", "Watermark Verifier"],
        "x402_enabled": True, "x402_price": "0.75", "free_tier": "1",
        "isolated_overrides": [],
        "revenue": "£399-£1,499/mo. Most credible of the *of.ai cluster for actual build (DOMAINS.md).",
        "pricing_tier": "business_49", "seat_price_usd": "49", "monthly_floor_usd": "1499",
        "stripe_live_ready": False, "vercel_deployed": False,
        "faq": [
            {"q": "How does MEOK pricing compare to Vanta/Drata/OneTrust?", "a": "10-20x undercut for enterprise tier ($50-200K/yr vs $120-500K/yr); 1000-10000x for low-volume agent-to-agent calls via x402 micro-settlement."},
        ],
    },
    {
        "domain": "councilof.ai", "tier": "governance",
        "tools": ["agent-orchestrator-mcp", "agent-negotiation-mcp", "csoai-governance-crosswalk-mcp"],
        "palette": "deliberation gold + ballot blue",
        "personality": "Multi-agent BFT deliberation — board-grade decision-making.",
        "voice": "Deliberative, byzantine-fault-tolerant, multi-stakeholder. Speaks in quorum certificates.",
        "memory_mode": "shared",
        "cognee_scope": "deliberations, quorum certificates, agent votes, audit-signed decisions",
        "entities": ["deliberation", "quorum_certificate", "vote", "decision"],
        "relations": ["deliberation→vote", "decision→quorum_certificate", "deliberation→decision"],
        "initial_agents": ["Council Chair", "Vote Tally Keeper", "Quorum Auditor", "Adversarial Checker"],
        "x402_enabled": True, "x402_price": "5.00", "free_tier": "0",
        "isolated_overrides": [],
        "revenue": "Audits every cross-hive Memoria commit; flip for $5-15k OR keep as governance infra. Per-call x402 re-priced $1→$5 (Watchdog = certification, new market category; [[meok-deep-audit-2026-06-08]] P1-2).",
        "pricing_tier": "business_49", "seat_price_usd": "49", "monthly_floor_usd": "4900",
        "stripe_live_ready": False, "vercel_deployed": False,
        "faq": [
            {"q": "How does MEOK pricing compare to Vanta/Drata/OneTrust?", "a": "10-20x undercut for enterprise tier ($50-200K/yr vs $120-500K/yr); 1000-10000x for low-volume agent-to-agent calls via x402 micro-settlement."},
        ],
    },
    # UK construction cluster
    {
        "domain": "grabhire.ai", "tier": "uk_construction",
        "tools": ["recruitment-ai-mcp", "resume-parser-ai-mcp", "lead-scoring-ai-mcp", "muckaway-ai-mcp"],
        "palette": "safety orange + construction blue",
        "personality": "UK grab-lorry marketplace + driver recruitment.",
        "voice": "Site-manager, plain-spoken, weather-aware. Speaks in 'lorry' not 'truck'.",
        "memory_mode": "shared",
        "cognee_scope": "UK haulage, grab-lorry fleet, council permits, MCIL/MOL, drivers",
        "entities": ["vehicle", "driver", "permit", "council", "site", "customer"],
        "relations": ["vehicle→site", "driver→vehicle", "permit→council", "site→customer"],
        "initial_agents": ["Fleet Dispatcher", "Permit Lookup", "Driver Recruiter", "Lead Scorer"],
        "x402_enabled": True, "x402_price": "0.05", "free_tier": "1",
        "isolated_overrides": [],
        "revenue": "Marketplace fees + £99-499/mo per rental co.",
        "pricing_tier": "team_29", "seat_price_usd": "29", "monthly_floor_usd": "99",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "muckaway.ai", "tier": "uk_construction",
        "tools": ["muckaway-ai-mcp"],
        "palette": "waste teal + earth brown",
        "personality": "UK skip/grab-hire marketplace — 'muck-away' is the UK term.",
        "voice": "Yard-manager, fleet-aware, tonnage-proud. Speaks in loads and landfills.",
        "memory_mode": "shared",
        "cognee_scope": "UK skip/grab-hire, landfills, council permits, fleet capacity",
        "entities": ["skip", "vehicle", "landfill", "permit", "site"],
        "relations": ["skip→site", "vehicle→landfill", "permit→council"],
        "initial_agents": ["Skip Dispatcher", "Landfill Router", "Permit Lookup"],
        "x402_enabled": True, "x402_price": "0.05", "free_tier": "1",
        "isolated_overrides": [],
        "revenue": "5-10% marketplace + £99-499/mo per rental co.",
        "pricing_tier": "team_29", "seat_price_usd": "29", "monthly_floor_usd": "99",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "planthire.ai", "tier": "uk_construction",
        "tools": ["planthire-ai-mcp"],
        "palette": "machinery yellow + hi-vis green",
        "personality": "UK plant-hire marketplace — excavators, dumpers, telehandlers.",
        "voice": "Plant-foreman, machinery-proud, CPCS-fluent. Speaks in 'digger' not 'excavator'.",
        "memory_mode": "shared",
        "cognee_scope": "UK plant-hire, machinery categories, CPCS operator cards, daily rates",
        "entities": ["machine", "operator", "site", "daily_rate", "category"],
        "relations": ["machine→site", "operator→machine", "site→category"],
        "initial_agents": ["Plant Dispatcher", "Rate Optimiser", "Operator Matcher"],
        "x402_enabled": True, "x402_price": "0.10", "free_tier": "1",
        "isolated_overrides": [],
        "revenue": "8-15% marketplace fees (equipment values $1k-10k/day).",
        "pricing_tier": "team_29", "seat_price_usd": "29", "monthly_floor_usd": "199",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "commercialvehicle.ai", "tier": "uk_construction",
        "tools": ["logistics-ai-mcp"],
        "palette": "fleet grey + route blue",
        "personality": "UK commercial fleet optimisation (Samsara/Geotab competitor).",
        "voice": "Fleet manager, telemetry-fluent, TCO-obsessed. Speaks in MPG and telematics.",
        "memory_mode": "shared",
        "cognee_scope": "UK commercial fleets, telematics, routing, TCO, driver hours (DTC)",
        "entities": ["vehicle", "route", "telemetry", "driver_hours", "fuel"],
        "relations": ["vehicle→route", "vehicle→telemetry", "driver_hours→vehicle"],
        "initial_agents": ["Route Optimiser", "Telematics Analyst", "Compliance Checker (DTC)"],
        "x402_enabled": True, "x402_price": "0.15", "free_tier": "1",
        "isolated_overrides": [],
        "revenue": "Cluster with muckaway/grabhire/planthire as one marketing site.",
        "pricing_tier": "business_49", "seat_price_usd": "49", "monthly_floor_usd": "490",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    # Vertical SaaS
    {
        "domain": "landlaw.ai", "tier": "vertical_saas",
        "tools": ["landlaw-ai-mcp", "legal-document-ai-mcp", "contract-review-ai-mcp"],
        "palette": "barrister burgundy + deed cream",
        "personality": "UK property law tech — conveyancing, leases, planning.",
        "voice": "Property lawyer, jurisdiction-aware, case-cite-heavy. Speaks in 'lease' and 'covenant'.",
        "memory_mode": "isolated",
        "cognee_scope": "UK property law, conveyancing, leases, planning, case citations",
        "entities": ["property", "conveyance", "lease", "covenant", "planning_permission", "case"],
        "relations": ["lease→property", "conveyance→property", "case→lease"],
        "initial_agents": ["Conveyancing Assistant", "Lease Reviewer", "Planning Advisor"],
        "x402_enabled": True, "x402_price": "0.50", "free_tier": "3",
        "isolated_overrides": ["client_property_data"],
        "revenue": "£199/mo solo → £999/mo firm. £47B legal tech market.",
        "pricing_tier": "business_49", "seat_price_usd": "49", "monthly_floor_usd": "199",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "fishkeeper.ai", "tier": "vertical_saas",
        "tools": ["fishkeeper-ai-mcp", "pet-care-ai-mcp"],
        "palette": "aquarium teal + coral pink",
        "personality": "Aquarium hobbyist community + care assistant.",
        "voice": "Friendly hobbyist, fish-proud, cycling-fluent. Speaks in ammonia and bio-load.",
        "memory_mode": "shared",
        "cognee_scope": "freshwater/saltwater species, water chemistry, cycling, diseases, compatibility",
        "entities": ["species", "tank", "water_parameter", "disease", "compatibility"],
        "relations": ["species→tank", "disease→species", "tank→water_parameter"],
        "initial_agents": ["Tank Setup Advisor", "Disease Diagnostician", "Compatibility Checker"],
        "x402_enabled": False, "x402_price": "0.00", "free_tier": "100",
        "isolated_overrides": [],
        "revenue": "Consumer subscription £4.99-19.99/mo. Reddit/TikTok brand-build.",
        "pricing_tier": "team_29", "seat_price_usd": "29", "monthly_floor_usd": "5",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "koikeeper.ai", "tier": "vertical_saas",
        "tools": ["fishkeeper-ai-mcp", "k25-vision"],
        "palette": "koi gold + pond jade",
        "personality": "Premium koi diagnostics — koi are $1k-50k each; owners pay £199/mo.",
        "voice": "Senior breeder, koi-proud, water-quality-obsessed. Speaks in 'shiro' and 'sanke'.",
        "memory_mode": "isolated",
        "cognee_scope": "koi varieties, water quality (pH, NH3, NO2), breeding, image-based diagnostics",
        "entities": ["koi", "variety", "water_parameter", "breeding_record", "diagnosis_image"],
        "relations": ["koi→variety", "koi→breeding_record", "diagnosis_image→koi"],
        "initial_agents": ["Koi Diagnostician (vision)", "Breeding Advisor", "Water Quality Sentinel"],
        "x402_enabled": True, "x402_price": "1.00", "free_tier": "0",
        "isolated_overrides": ["premium_pond_data"],
        "revenue": "£199/mo premium tier. Niche, affluent, competition is KoiQuanta.",
        "pricing_tier": "team_29", "seat_price_usd": "29", "monthly_floor_usd": "199",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    # Flip / defer
    {
        "domain": "diyhelp.ai", "tier": "flip",
        "tools": [],
        "palette": "DIY high-vis + timber brown",
        "personality": "Home-DIY assistant (FLIP CANDIDATE).",
        "voice": "Handyman, tool-proud, fixit-first. Speaks in 'Spirit Level' and 'G-clamp'.",
        "memory_mode": "shared",
        "cognee_scope": "DIY topics, tools, materials, techniques",
        "entities": ["project", "tool", "material", "technique"],
        "relations": ["project→tool", "project→material", "project→technique"],
        "initial_agents": ["DIY Advisor", "Tool Recommender"],
        "x402_enabled": False, "x402_price": "0.00", "free_tier": "100",
        "isolated_overrides": [],
        "revenue": "Defer or flip. Affiliate revenue if built.",
        "pricing_tier": "micro_free", "seat_price_usd": "0", "monthly_floor_usd": "0",
        "valuation_usd": "8000", "asking_price_usd": "12000", "flip_status": "candidate",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "pokerhud.ai", "tier": "flip",
        "tools": [],
        "palette": "felt green + chip red",
        "personality": "Poker analysis (FLIP — legal grey zone in many jurisdictions).",
        "voice": "Grinder, GTO-aware, ICM-fluent. Speaks in '3-bet' and 'board texture'.",
        "memory_mode": "shared",
        "cognee_scope": "poker hands, GTO solutions, ICM, hand histories",
        "entities": ["hand", "gto_solution", "tournament", "icm"],
        "relations": ["hand→gto_solution", "tournament→icm"],
        "initial_agents": ["Hand Reviewer", "GTO Solver"],
        "x402_enabled": False, "x402_price": "0.00", "free_tier": "0",
        "isolated_overrides": [],
        "revenue": "FLIP. No MCP fit; legal grey.",
        "pricing_tier": "micro_free", "seat_price_usd": "0", "monthly_floor_usd": "0",
        "valuation_usd": "5000", "asking_price_usd": "15000", "flip_status": "candidate",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "loopfactory.ai", "tier": "flip",
        "tools": ["cron-ai-mcp", "webhook-ai-mcp"],
        "palette": "automation green + workflow blue",
        "personality": "No-code automation (Zapier competitor, FLIP CANDIDATE).",
        "voice": "Maker, no-code-first, IFTTT-aware. Speaks in 'Zap' and 'trigger'.",
        "memory_mode": "shared",
        "cognee_scope": "automation workflows, triggers, actions, integrations",
        "entities": ["workflow", "trigger", "action", "integration"],
        "relations": ["workflow→trigger", "workflow→action", "action→integration"],
        "initial_agents": ["Workflow Builder", "Integration Mapper"],
        "x402_enabled": False, "x402_price": "0.00", "free_tier": "10",
        "isolated_overrides": [],
        "revenue": "Defer or flip. Crowded market.",
        "pricing_tier": "micro_free", "seat_price_usd": "0", "monthly_floor_usd": "0",
        "valuation_usd": "15000", "asking_price_usd": "25000", "flip_status": "candidate",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "optimobile.ai", "tier": "flip",
        "tools": [],
        "palette": "mobile magenta + analytics teal",
        "personality": "Mobile analytics (FLIP — Firebase/Crashlytics dominate).",
        "voice": "Mobile-dev, retention-obsessed, cohort-fluent. Speaks in DAU and ARPU.",
        "memory_mode": "shared",
        "cognee_scope": "mobile apps, retention metrics, cohorts, funnels",
        "entities": ["app", "user", "cohort", "funnel", "metric"],
        "relations": ["app→user", "user→cohort", "cohort→metric"],
        "initial_agents": ["Retention Analyst", "Funnel Optimiser"],
        "x402_enabled": False, "x402_price": "0.00", "free_tier": "10",
        "isolated_overrides": [],
        "revenue": "FLIP. Weak angle vs Firebase/Crashlytics.",
        "pricing_tier": "micro_free", "seat_price_usd": "0", "monthly_floor_usd": "0",
        "valuation_usd": "6000", "asking_price_usd": "10000", "flip_status": "candidate",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "socialmediamananger.ai", "tier": "expire",
        "tools": [],
        "palette": "social purple + share blue",
        "personality": "Social media management — DOMAIN HAS TYPO 'mananger' (let expire).",
        "voice": "Quiet — domain typo kills brand.",
        "memory_mode": "shared",
        "cognee_scope": "(none — let expire at renewal)",
        "entities": [],
        "relations": [],
        "initial_agents": [],
        "x402_enabled": False, "x402_price": "0.00", "free_tier": "0",
        "isolated_overrides": [],
        "revenue": "Let expire. Typo'd domain traffic is near-zero; resale value is negative.",
        "pricing_tier": "micro_free", "seat_price_usd": "0", "monthly_floor_usd": "0",
        "valuation_usd": "100", "asking_price_usd": "100", "flip_status": "expire",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    # Infra hives (3) — the OpenMoE / openMCP / keystone trio
    {
        "domain": "openmoe.ai", "tier": "infra",
        "tools": ["openmoe-bft", "openMCP"],
        "palette": "OpenMoE amber + research slate",
        "personality": "Base-model layer — OpenMoE-BFT (Opus lane).",
        "voice": "Researcher, byzantine-fault-tolerant, expert-routing-aware. Speaks in 'expert' and 'BFT'.",
        "memory_mode": "shared",
        "cognee_scope": "OpenMoE base model, BFT consensus, expert routing, signet receipts",
        "entities": ["expert", "model", "consensus_round", "signet"],
        "relations": ["consensus_round→expert", "model→expert", "signet→consensus_round"],
        "initial_agents": ["Expert Router", "BFT Aggregator", "Signet Issuer"],
        "x402_enabled": True, "x402_price": "0.01", "free_tier": "10",
        "isolated_overrides": [],
        "revenue": "Per-call BFT inference; signet receipts monetisable via x402.",
        "pricing_tier": "micro_paid", "seat_price_usd": "0", "monthly_floor_usd": "0",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "openMCP", "tier": "infra",
        "tools": ["openMCP"],
        "palette": "audit green + transport blue",
        "personality": "Cross-post CLI + audit engine — feeds the GEO/AEO loop.",
        "voice": "Librarian, audit-first, byte-identical. Speaks in scorecards and rank.",
        "memory_mode": "shared",
        "cognee_scope": "MCP server directory listings, audit scores, cross-post runs",
        "entities": ["mcp_server", "audit_result", "directory", "cross_post_run"],
        "relations": ["mcp_server→audit_result", "mcp_server→directory", "cross_post_run→mcp_server"],
        "initial_agents": ["MCP Auditor", "Cross-Poster", "Score Ranker"],
        "x402_enabled": False, "x402_price": "0.00", "free_tier": "5",
        "isolated_overrides": [],
        "revenue": "Free / OSS — drives traffic to monetised flagships.",
        "pricing_tier": "micro_free", "seat_price_usd": "0", "monthly_floor_usd": "0",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
    {
        "domain": "meok-compliance-gateway", "tier": "infra",
        "tools": ["meok-compliance-gateway"],
        "palette": "gateway slate + x402 amber",
        "personality": "Streamable-HTTP gateway + x402 paywall — THIS repo.",
        "voice": "Wrapper, hermetic, instrumented. Speaks in `Mcp-Method` headers and atomic units.",
        "memory_mode": "isolated",
        "cognee_scope": "MCP transport, x402 payments, usage accounting, PayGo balance",
        "entities": ["mcp_call", "x402_payment", "usage_counter"],
        "relations": ["mcp_call→x402_payment", "mcp_call→usage_counter"],
        "initial_agents": ["x402 Paywall", "Usage Accountant", "MCP Router"],
        "x402_enabled": True, "x402_price": "0.05", "free_tier": "1",
        "isolated_overrides": ["x402_payment_data", "usage_counters"],
        "revenue": "x402 micro-settlement per tool call. 4-way split on cross-hive calls.",
        "pricing_tier": "business_49", "seat_price_usd": "49", "monthly_floor_usd": "490",
        "stripe_live_ready": False, "vercel_deployed": False,
    },
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate_one(spec: dict, out_root: Path) -> Path:
    """Generate the 9-file hive config for one domain spec."""
    name = spec['domain'].split('.')[0]
    hive_dir = out_root / f"{name}-hive"
    hive_dir.mkdir(parents=True, exist_ok=True)
    (hive_dir / ".mex").mkdir(exist_ok=True)

    (hive_dir / "README.md").write_text(gen_readme(spec))
    (hive_dir / "stack.yml").write_text(gen_stack_yml(spec))
    (hive_dir / "DESIGN.md").write_text(gen_design_md(spec))
    # Re-render agent-card.json with ensure_ascii=False to keep unicode (em-dash etc.)
    (hive_dir / "agent-card.json").write_text(json.dumps(json.loads(gen_agent_card(spec)), indent=2, ensure_ascii=False) + "\n")
    (hive_dir / "hermes.yml").write_text(gen_hermes_yml(spec))
    (hive_dir / "agentmemory.json").write_text(gen_agentmemory_json(spec) + "\n")
    (hive_dir / ".mex" / "mex.yml").write_text(gen_mex_yml(spec))
    # spawn.py: post-process the __INITIAL_AGENTS__ sentinel (f-string-safe)
    spawn_text = gen_spawn_py(spec).replace("__INITIAL_AGENTS__", json.dumps(spec['initial_agents'], ensure_ascii=False))
    (hive_dir / "spawn.py").write_text(spawn_text)
    (hive_dir / ".gitignore").write_text(gen_gitignore())
    (hive_dir / "LICENSE").write_text(gen_license())

    return hive_dir


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("domain", nargs="?", help="Domain name (e.g. meok.ai); omit to generate all")
    p.add_argument("--tier", default="flagship")
    p.add_argument("--tools", default="", help="Comma-separated tool list")
    p.add_argument("--palette", default=DEFAULT_PALETTE)
    p.add_argument("--out", default="/tmp/hive-staging", help="Output root directory")
    p.add_argument("--list", action="store_true", help="List registered domains and exit")
    args = p.parse_args()

    if args.list:
        for s in DOMAIN_REGISTRY:
            print(f"  {s['domain']:<30}  tier={s['tier']}")
        return 0

    out_root = Path(args.out).expanduser()
    out_root.mkdir(parents=True, exist_ok=True)

    if args.domain:
        # Custom one-off (not in registry)
        spec = {
            "domain": args.domain,
            "tier": args.tier,
            "tools": [t.strip() for t in args.tools.split(",") if t.strip()],
            "palette": args.palette,
            "personality": f"Custom hive for {args.domain}",
            "voice": "TBD — edit DESIGN.md voice section.",
            "memory_mode": "shared",
            "cognee_scope": "(scope TBD)",
            "entities": ["entity1", "entity2"],
            "relations": ["entity1→entity2"],
            "initial_agents": ["Agent 1", "Agent 2"],
            "x402_enabled": False, "x402_price": "0.00", "free_tier": "1",
            "isolated_overrides": [],
            "revenue": "TBD",
        }
        out = generate_one(spec, out_root)
        print(f"  {spec['domain']:<30} -> {out}")
    else:
        # Generate all 28 from the registry
        print(f"Generating {len(DOMAIN_REGISTRY)} hive configs into {out_root}/")
        for spec in DOMAIN_REGISTRY:
            out = generate_one(spec, out_root)
            print(f"  {spec['domain']:<30}  tier={spec['tier']:<16}  -> {out.name}/")
        print(f"\n{len(DOMAIN_REGISTRY)} hives generated.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
