#!/usr/bin/env python3
"""
CANONICAL NUMBERS RECONCILER
Fixes the install count discrepancy across all surfaces
"""

CANONICAL_NUMBER = {
    "installs_per_month": 6798,  # Verified from PyPI
    "mcp_servers": 341,  # SOV3 mcp_bridge_discover count
    "frameworks": 13,
    "domains": 28,
    "compliance_mcp": 13,
}

def generate_canonical_text():
    """Generate consistent install count references"""
    return f"""
CANONICAL NUMBERS (verified 2026-06-13):
- Monthly installs: {CANONICAL_NUMBER['installs_per_month']:,}/mo (PyPI eu-ai-act-compliance-mcp)
- MCP servers discoverable: {CANONICAL_NUMBER['mcp_servers']} (via SOV3 bridge)
- Governance frameworks: {CANONICAL_NUMBER['frameworks']}
- Live domains: {CANONICAL_NUMBER['domains']}
- Compliance MCPs: {CANONICAL_NUMBER['compliance_mcp']}
"""

def update_readme_stats(readme_path):
    """Update numbers in a README file"""
    replacements = [
        ("22.6K", f"{CANONICAL_NUMBER['installs_per_month'] / 1000:.1f}K"),
        ("6,798", f"{CANONICAL_NUMBER['installs_per_month']:,}"),
        ("67 MCPs", f"{CANONICAL_NUMBER['compliance_mcp']} MCPs"),
        ("70 MCPs", f"{CANONICAL_NUMBER['compliance_mcp']} MCPs"),
    ]
    
    try:
        content = Path(readme_path).read_text()
        changed = False
        for old, new in replacements:
            if old in content:
                content = content.replace(old, new)
                changed = True
        if changed:
            Path(readme_path).write_text(content)
            print(f"  ✅ Updated: {readme_path}")
            return True
    except FileNotFoundError:
        pass
    return False

from pathlib import Path

if __name__ == "__main__":
    import os
    
    print("🔢 CANONICAL NUMBERS RECONCILER")
    print("=" * 50)
    print(generate_canonical_text())
    
    # Update keystone files
    keystone = Path("/Users/nicholas/meok-compliance-gateway")
    
    files_to_check = [
        keystone / "README.md",
        keystone / "llms.txt",
        keystone / "server.json",
    ]
    
    for f in files_to_check:
        if f.exists():
            update_readme_stats(f)
    
    print("\n📝 Apply to flagship repos with:")
    print("  sed -i 's/22.6K/6.8K/g' README.md")
    print("  sed -i 's/67 MCPs/13 MCPs/g' README.md")