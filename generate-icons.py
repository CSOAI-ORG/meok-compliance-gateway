#!/usr/bin/env python3
"""
ICON GENERATOR FOR ALL 14 FLAGSHIPS
Creates SVG icons based on keystone-icon.svg template
"""

ICON_COLORS = {
    "eu-ai-act-compliance-mcp": ("#0B3D0B", "#FFD27A", "EU"),
    "dora-compliance-mcp": ("#0B1B36", "#7BB7FF", "DO"),
    "nis2-compliance-mcp": ("#3D0B3D", "#7BB7FF", "NI"),
    "cra-compliance-mcp": ("#3D0B0B", "#FFD27A", "CR"),
    "soc2-compliance-ai-mcp": ("#0B2B3D", "#7BB7FF", "SO"),
    "hipaa-compliance-mcp": ("#B8860B", "#0B1B36", "HI"),
    "gdpr-compliance-ai-mcp": ("#0B3D3D", "#7BB7FF", "GD"),
    "iso-42001-ai-mcp": ("#1A1A1A", "#7BB7FF", "IS"),
    "csrd-compliance-mcp": ("#2B3D0B", "#FFD27A", "CS"),
    "bias-detection-mcp": ("#3D2B0B", "#7BB7FF", "BI"),
    "meok-governance-engine-mcp": ("#0B1B36", "#7BB7FF", "GO"),
    "meok-mcp-injection-scan-mcp": ("#3D0B1B", "#FFD27A", "IN"),
    "agent-audit-logger-mcp": ("#1B0B3D", "#7BB7FF", "AU"),
    "agent-policy-enforcement-mcp": ("#3D1B0B", "#FFD27A", "PO"),
}

def generate_icon(name, color1, color2, initials):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <title>{name}</title>
  <desc>MEOK {name} MCP server - part of the 28-hive governance mesh.</desc>
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{color1}"/>
      <stop offset="1" stop-color="{color2}"/>
    </linearGradient>
  </defs>
  <rect width="256" height="256" rx="48" fill="url(#g)"/>
  <g fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
    <polygon points="128,40 196,80 196,160 128,200 60,160 60,80"/>
    <polygon points="128,80 168,104 168,152 128,176 88,152 88,104" stroke="#FFFFFF" stroke-width="5"/>
    <line x1="128" y1="20" x2="128" y2="40" stroke-width="3"/>
    <line x1="128" y1="200" x2="128" y2="220" stroke-width="3"/>
    <line x1="40" y1="120" x2="60" y2="120" stroke-width="3"/>
    <line x1="196" y1="120" x2="216" y2="120" stroke-width="3"/>
  </g>
  <g fill="#FFFFFF" font-family="ui-monospace,Menlo,monospace" font-size="22" font-weight="700" text-anchor="middle">
    <text x="128" y="138">{initials}</text>
  </g>
</svg>'''

if __name__ == "__main__":
    import os
    
    templates_dir = Path("/Users/nicholas/meok-compliance-gateway/mcp-registry-templates")
    
    for name, (color1, color2, initials) in ICON_COLORS.items():
        mcp_dir = templates_dir / name
        assets_dir = mcp_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        
        icon_path = assets_dir / "icon.svg"
        icon_path.write_text(generate_icon(name, color1, color2, initials))
        print(f"  ✓ Created assets/icon.svg for {name}")
    
    print("\n📋 Icons created for all 14 flagships")