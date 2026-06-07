#!/usr/bin/env bash
# Smoke test for the MEOK compliance gateway: proves http_server.py serves a MEOK
# FastMCP server over streamable-HTTP and answers `initialize` with HTTP 200.
#
# Usage:
#   # `server` must be importable (Docker image already pip-installs the PKG).
#   # Locally, point PYTHONPATH at a marketplace server module dir:
#   PYTHONPATH=/path/to/eu-ai-act-compliance-mcp PYTHON=python3.11 tests/smoke.sh
#
# Exit 0 = initialize returned 200. Non-zero = failure (CI gate).
set -euo pipefail

PORT="${PORT:-8077}"
PYTHON="${PYTHON:-python3}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"

PORT="$PORT" PYTHONPATH="${PYTHONPATH:-}:$HERE" "$PYTHON" "$HERE/http_server.py" >/tmp/gw_smoke.log 2>&1 &
PID=$!
trap 'kill "$PID" 2>/dev/null || true' EXIT

# wait up to ~10s for the listener
for _ in $(seq 1 20); do
  if curl -s -o /dev/null --max-time 2 "http://127.0.0.1:$PORT/mcp" 2>/dev/null; then break; fi
  sleep 0.5
done

code=$(curl -s -o /tmp/gw_resp.txt -w "%{http_code}" --max-time 8 -X POST "http://127.0.0.1:$PORT/mcp" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"smoke","version":"0"}}}')

if [ "$code" != "200" ]; then
  echo "FAIL: initialize returned HTTP $code"; cat /tmp/gw_resp.txt; echo; tail -10 /tmp/gw_smoke.log; exit 1
fi
if ! grep -q '"result"' /tmp/gw_resp.txt; then
  echo "FAIL: 200 but no JSON-RPC result"; cat /tmp/gw_resp.txt; exit 1
fi
echo "PASS: gateway initialize -> 200 with JSON-RPC result"
