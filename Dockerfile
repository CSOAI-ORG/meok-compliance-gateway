# MEOK compliance MCP — streamable-HTTP container for cloud marketplaces.
# Build: docker build --build-arg PKG=eu-ai-act-compliance-mcp -t meok/eu-ai-act:latest .
#
# Base pinned by digest for reproducible builds (tag kept for readability).
# Re-resolve with:  docker buildx imagetools inspect python:3.11-slim
FROM python:3.11-slim@sha256:a3ab0b966bc4e91546a033e22093cb840908979487a9fc0e6e38295747e49ac0
ARG PKG=eu-ai-act-compliance-mcp
ENV PORT=8000 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

WORKDIR /app

# requirements-gateway.txt pins mcp/uvicorn exactly so the build can't drift
# onto an incompatible FastMCP API. The flagship PKG brings the real `server` module.
COPY requirements-gateway.txt /app/requirements-gateway.txt
RUN pip install --no-cache-dir -r /app/requirements-gateway.txt "${PKG}"

COPY http_server.py /app/http_server.py

# Run unprivileged — required by Docker MCP Catalog / AWS Marketplace review.
RUN useradd --create-home --uid 10001 app && chown -R app:app /app
USER app

EXPOSE 8000

# /mcp is the streamable-HTTP endpoint; /healthz + /.well-known/oauth-protected-resource
# are also served by http_server.py. Probe /healthz for liveness (stdlib only).
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import os,sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:%s/healthz' % os.environ.get('PORT','8000'), timeout=2).status==200 else 1)"

CMD ["python", "http_server.py"]
