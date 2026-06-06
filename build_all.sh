#!/usr/bin/env bash
# Build streamable-HTTP container images for the compliance bundle.
# Mirrors .github/workflows/build-push.yml so local dev matches what CI pushes:
# namespace is ghcr.io/csoai-org/<flagship>-mcp, but locally we just tag
# csoai-org/<flagship>-mcp:latest (no push) so `docker images` shows the same
# names a developer will pull from GHCR.
#
# Requires Docker running (Docker Desktop currently down on this box — run on
# a host with Docker).
set -euo pipefail

# flagship_name : pypi_package
flagships=(
  "eu-ai-act:eu-ai-act-compliance-mcp"
  "dora:dora-compliance-mcp"
  "nis2:nis2-compliance-mcp"
  "cra:cra-compliance-mcp"
)

for entry in "${flagships[@]}"; do
  flagship="${entry%%:*}"
  pkg="${entry#*:}"
  img="csoai-org/${flagship}-mcp"
  echo ">>> building $img from $pkg"
  docker build --build-arg PKG="$pkg" -t "$img:latest" . || echo "FAILED $pkg"
done
echo
echo "Done. Test a flagship locally:"
echo "  docker run -p 8000:8000 csoai-org/eu-ai-act-mcp:latest"
echo "  curl -XPOST localhost:8000/mcp -H 'content-type: application/json' \\"
echo "    -H 'accept: application/json, text/event-stream' \\"
echo "    -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{\"protocolVersion\":\"2025-03-26\",\"capabilities\":{},\"clientInfo\":{\"name\":\"t\",\"version\":\"1\"}}}'"
