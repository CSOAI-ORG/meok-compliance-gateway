#!/usr/bin/env bash
# Build streamable-HTTP container images for the compliance bundle.
# Requires Docker running (Docker Desktop currently down on this box — run on a host with Docker).
for pkg in eu-ai-act-compliance-mcp dora-compliance-mcp nis2-compliance-mcp cra-compliance-mcp; do
  img="meok/${pkg%-compliance-mcp}"
  echo ">>> building $img from $pkg"
  docker build --build-arg PKG="$pkg" -t "$img:latest" . || echo "FAILED $pkg"
done
echo "Done. Test: docker run -p 8000:8000 meok/eu-ai-act:latest  →  curl POST localhost:8000/mcp"
