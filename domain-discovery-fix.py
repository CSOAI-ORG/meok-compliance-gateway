#!/usr/bin/env python3
"""
DOMAIN DISCOVERY FIXER
Creates llms.txt + .well-known endpoints for all 28 domains
Run: python3 domain-discovery-fix.py --apply (dry-run by default)
"""

DOMAINS_NEEDING_FIX = [
    "meok.ai",
    "proofof.ai",
    "councilof.ai",  # Missing mcp-server
    "safetyof.ai",
    "suicidestop.ai",
    "planthire.ai",  # Has all
    "muckaway.ai",   # Has all
    "haulage.app",   # Has all
    "grabhire.ai",   # Has all
    "templeman-opticians.com",  # Missing agent-card, mcp-server
    "agisafe.ai",
    "asisecurity.ai",
    "accountabilityof.ai",
    "biasdetectionof.ai",
    "dataprivacyof.ai",
    "ethicalgovernanceof.ai",
    "transparencyof.ai",
]

LLMS_TEMPLATE = """# {domain}
> {domain} compliance and AI safety. Part of the MEOK 28-hive MCP governance mesh.

## Install
pip install {mcp_name}

## Tools
- quick_scan: Compliance check
- deadline_check: Regulatory deadlines
- framework_scan: Detailed assessment

## MCP Gateway
https://gateway.meok.ai/mcp

MIT Licensed.
"""

MCP_SERVER_TEMPLATE = """{{
  "name": "{mcp_name}",
  "description": "{domain} compliance MCP",
  "version": "1.0.0",
  "protocols": ["MCP", "A2A"],
  "capabilities": ["compliance", "audit", "risk"]
}}
"""

AGENT_CARD_TEMPLATE = """{{
  "@context": "https://a2a-protocol.org/schema/v1/agent-card.jsonld",
  "@type": "Agent",
  "name": "{name}",
  "description": "Compliance gateway for {domain}",
  "url": "https://{domain}",
  "skills": ["compliance-check", "deadline-tracking", "framework-audit"],
  "endpoints": {{"mcp": "https://gateway.meok.ai/mcp"}}
}}
"""

def generate_fixes(domain):
    """Generate discovery files for a domain"""
    mcp_name = domain.replace(".ai", "-ai-mcp").replace(".app", "-app-mcp").replace(".com", "-com-mcp")
    if "proofof" in domain:
        mcp_name = "proofof-ai-mcp"
    elif "councilof" in domain:
        mcp_name = "councilof-ai-mcp"
    elif "safety" in domain:
        mcp_name = "safetyof-ai-mcp"
    
    return {
        "llms.txt": LLMS_TEMPLATE.format(domain=domain, mcp_name=mcp_name),
        ".well-known/mcp-server": MCP_SERVER_TEMPLATE.format(mcp_name=mcp_name, domain=domain),
        ".well-known/agent-card.json": AGENT_CARD_TEMPLATE.format(name=domain, domain=domain),
    }

def main(dry_run=True):
    import os
    
    print("🔧 DOMAIN DISCOVERY FIXER")
    print("=" * 50)
    
    for domain in DOMAINS_NEEDING_FIX:
        print(f"\n📦 {domain}:")
        
        # Find local repo
        local_path = f"/Users/nicholas/{domain}"
        if os.path.exists(local_path):
            fixes = generate_fixes(domain)
            for filename, content in fixes.items():
                filepath = f"{local_path}/{filename}"
                if dry_run:
                    print(f"  Would create: {filepath}")
                else:
                    # Create directories if needed
                    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
                    Path(filepath).write_text(content)
                    print(f"  ✓ Created: {filename}")
        else:
            print(f"  ⚠️  Local repo not found: {local_path}")
    
    if dry_run:
        print("\n⚠️  Dry run complete. Run with --apply to write files.")

if __name__ == "__main__":
    import sys
    from pathlib import Path
    main(dry_run="--apply" not in sys.argv)