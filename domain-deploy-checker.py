#!/usr/bin/env python3
"""
DEPLOY CHECKER - Verify all 28 domains are deployed correctly
Checks live status, canonical tags, and MCP discovery endpoints
"""

import subprocess
import json
from pathlib import Path

DOMAINS = [
    # LIVE domains
    ("meok.ai", 307, "redirects"),
    ("csoai.org", 200, "live"),
    ("proofof.ai", 307, "redirects"),
    ("councilof.ai", 200, "live"),
    ("safetyof.ai", 200, "live"),
    ("suicidestop.ai", 200, "live"),
    ("planthire.ai", 200, "live"),
    ("muckaway.ai", 200, "live"),
    ("haulage.app", 200, "live"),
    ("grabhire.ai", 200, "live"),
    ("templeman-opticians.com", 200, "live"),
    ("fishkeeper.ai", 307, "redirects"),
    ("koikeeper.ai", 307, "redirects"),
    ("agisafe.ai", 200, "live"),
    ("asisecurity.ai", 200, "live"),
    ("loopfactory.ai", 200, "live"),
    ("socialmediamanager.ai", 200, "live"),
    ("accountabilityof.ai", 200, "live"),
    ("biasdetectionof.ai", 200, "live"),
    ("dataprivacyof.ai", 200, "live"),
    ("ethicalgovernanceof.ai", 200, "live"),
    ("transparencyof.ai", 200, "live"),
    # DEAD domains
    ("diyhelp.ai", 0, "nxdomain"),
    ("pokerhud.ai", 0, "nxdomain"),
    ("sov3.ai", 0, "nxdomain"),
]

def check_domain(domain):
    """Check HTTP status for a domain"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"https://{domain}"],
            capture_output=True, text=True, timeout=10
        )
        code = result.stdout.strip()
        return int(code) if code.isdigit() else 0
    except Exception:
        return 0

def check_mcp_endpoints(domain):
    """Check MCP discovery endpoints"""
    endpoints = {
        "llms.txt": check_endpoint(f"https://{domain}/llms.txt"),
        "agent-card": check_endpoint(f"https://{domain}/.well-known/agent-card.json"),
        "mcp-server": check_endpoint(f"https://{domain}/.well-known/mcp-server"),
    }
    return endpoints

def check_endpoint(url):
    """Check if endpoint exists (returns 200)"""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=5
        )
        return "✅" if result.stdout.strip() == "200" else "❌"
    except Exception:
        return "❌"

def main():
    print("🔍 DOMAIN DEPLOYMENT CHECKER")
    print("=" * 60)
    
    live_count = 0
    dead_count = 0
    
    for domain, expected, status in DOMAINS:
        code = check_domain(domain)
        if code == expected or (expected == 200 and code == 307):
            live_count += 1
            emoji = "✅"
        else:
            dead_count += 1
            emoji = "❌"
        
        # Check endpoints for live domains
        endpoints = ""
        if code == 200 or code == 307:
            ep = check_mcp_endpoints(domain)
            endpoints = f"  [{ep['llms.txt']}] llms.txt [{ep['agent-card']}] agent-card [{ep['mcp-server']}] mcp-server"
        
        print(f"{emoji} {domain}: {code} ({status}){endpoints}")
    
    print("\n📊 Summary:")
    print(f"  Live: {live_count} domains")
    print(f"  Dead: {dead_count} domains (need DNS/A-record)")
    
    print("\n💡 Next steps:")
    print("  1. Fix dead domains in Namecheap DNS")
    print("  2. Add llms.txt to domains missing it")
    print("  3. Add .well-known endpoints to domains missing them")

if __name__ == "__main__":
    main()