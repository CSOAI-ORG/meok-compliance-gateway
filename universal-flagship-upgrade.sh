#!/usr/bin/env bash
# UNIVERSAL FLAGSHIP UPGRADER
# Clones, applies templates, and prepares PRs for all 14 flagships
# Account-gated: requires GitHub auth for PR creation

set -e

FLAGSHIPS=(
  "eu-ai-act-compliance-mcp"
  "dora-compliance-mcp"
  "nis2-compliance-mcp"
  "cra-compliance-mcp"
  "soc2-compliance-ai-mcp"
  "hipaa-compliance-mcp"
  "gdpr-compliance-ai-mcp"
  "iso-42001-ai-mcp"
  "csrd-compliance-mcp"
  "bias-detection-mcp"
  "meok-governance-engine-mcp"
  "meok-mcp-injection-scan-mcp"
  "agent-audit-logger-mcp"
  "agent-policy-enforcement-mcp"
)

TEMPLATES_DIR="/Users/nicholas/meok-compliance-gateway/mcp-registry-templates"
WORK_DIR="/tmp/meok-upgrade-$(date +%s)"

mkdir -p "$WORK_DIR"

echo "🚀 UNIVERSAL FLAGSHIP UPGRADER"
echo "==============================="
echo ""

# Clone each flagship
for mcp in "${FLAGSHIPS[@]}"; do
  echo "📦 Processing: $mcp"
  
  # Clone
  cd "$WORK_DIR"
  git clone "https://github.com/CSOAI-ORG/$mcp.git" 2>/dev/null || {
    echo "  ⚠️  Clone failed (may already exist or private)"
    continue
  }
  
  cd "$mcp"
  
  # Apply templates
  echo "  → Applying server.json..."
  cp "$TEMPLATES_DIR/$mcp/server.json" ./server.json 2>/dev/null || echo "  ⚠️  server.json template missing"
  
  echo "  → Applying llms.txt..."
  cp "$TEMPLATES_DIR/$mcp/llms.txt" ./llms.txt 2>/dev/null || echo "  ⚠️  llms.txt template missing"
  
  echo "  → Creating .well-known..."
  mkdir -p .well-known
  cp "$TEMPLATES_DIR/$mcp/.well-known/mcp-server" ./.well-known/mcp-server 2>/dev/null || echo "  ⚠️  mcp-server template missing"
  
  echo "  → Creating assets/icon.svg..."
  mkdir -p assets
  cp "$TEMPLATES_DIR/$mcp/assets/icon.svg" ./assets/icon.svg 2>/dev/null || echo "  ⚠️  icon.svg template missing"
  
  # Git operations (would need auth)
  git add -A
  
  echo "  ✅ $mcp ready for PR"
  echo "     Run: cd $WORK_DIR/$mcp && git commit -m 'feat: Add MCP Registry discovery files' && gh pr create"
  echo ""
done

echo "🏁 All flagships processed in $WORK_DIR"
echo ""
echo "🔑 Account-gated next steps:"
echo "  1. Set GITHUB_TOKEN or use keyring token"
echo "  2. Uncomment the git push + PR creation in this script"
echo "  3. Or manually run PRs for each repo"