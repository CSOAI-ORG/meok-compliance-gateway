# MEOK compliance MCP — streamable-HTTP container for cloud marketplaces
# Build: docker build --build-arg PKG=eu-ai-act-compliance-mcp -t meok/eu-ai-act:latest .
FROM python:3.11-slim
ARG PKG=eu-ai-act-compliance-mcp
ENV PORT=8000 PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir "${PKG}" "uvicorn[standard]"
WORKDIR /app
COPY http_server.py /app/http_server.py
EXPOSE 8000
# /mcp is the streamable-HTTP endpoint (verified HTTP 200 on initialize)
CMD ["python", "http_server.py"]
