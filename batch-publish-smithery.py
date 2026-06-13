#!/usr/bin/env python3
"""
SMITHERY BATCH PUBLISHER
Prepares smithery.yaml submissions for all 14 flagships
Account-gated: requires npm install -g @smithery/cli + login
"""

SMITHERY_YAML = """# smithery.yaml — Smithery.ai submission
# Repo: CSOAI-ORG/{name}
runtime: container
startCommand:
  type: http
  transport: streamable-http
  port: 8081
  path: /mcp
  configSchema:
    type: object
    properties:
      apiKey:
        type: string
        description: "MEOK API key (optional; required for x402 paywalled tools)"
        default: ""
    additionalProperties: false
build:
  dockerfile: Dockerfile
  dockerBuildArgs:
    PKG: {name}
"""

def generate_smithery_yaml(name):
    return SMITHERY_YAML.format(name=name)

if __name__ == "__main__":
    flagships = [
        "eu-ai-act-compliance-mcp",
        "dora-compliance-mcp",
        "nis2-compliance-mcp",
        "cra-compliance-mcp",
        "soc2-compliance-ai-mcp",
        "hipaa-compliance-mcp",
        "gdpr-compliance-ai-mcp",
        "iso-42001-ai-mcp",
        "csrd-compliance-mcp",
        "bias-detection-mcp",
        "meok-governance-engine-mcp",
        "meok-mcp-injection-scan-mcp",
        "agent-audit-logger-mcp",
        "agent-policy-enforcement-mcp",
    ]
    
    print("🔧 SMITHERY BATCH PUBLISHER")
    print("=" * 50)
    print("\n📋 Commands to run (after npm install -g @smithery/cli):\n")
    
    for name in flagships:
        print(f"# {name}")
        print(f"cd /path/to/{name}")
        print(f"cat > smithery.yaml << 'EOF'")
        print(generate_smithery_yaml(name))
        print("EOF")
        print(f"smithery publish .  # Requires SMITHERY_API_KEY\n")
    
    print("\n⚠️  Account-gated: set SMITHERY_API_KEY first")