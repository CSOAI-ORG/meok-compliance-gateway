#!/bin/zsh
cd ~/clawd/meok-compliance-gateway
gh auth token | docker login ghcr.io -u CSOAI-ORG --password-stdin >/dev/null 2>&1
declare -A M=( [eu-ai-act-compliance-mcp]=eu-ai-act-mcp [dora-compliance-mcp]=dora-mcp [nis2-compliance-mcp]=nis2-mcp [cra-compliance-mcp]=cra-mcp )
for pkg img in eu-ai-act-compliance-mcp eu-ai-act-mcp dora-compliance-mcp dora-mcp nis2-compliance-mcp nis2-mcp cra-compliance-mcp cra-mcp; do :; done
for pkg in dora-compliance-mcp nis2-compliance-mcp cra-compliance-mcp; do
  img="${pkg%-compliance-mcp}-mcp"
  echo ">>> $pkg -> ghcr.io/csoai-org/$img"
  docker build --build-arg PKG="$pkg" -t "ghcr.io/csoai-org/$img:latest" . >/dev/null 2>&1 && \
  docker push "ghcr.io/csoai-org/$img:latest" 2>&1 | tail -1 || echo "  FAILED $pkg"
done
echo "DONE — 4 flagship images on ghcr.io/csoai-org/"
