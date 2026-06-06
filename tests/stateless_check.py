"""Asserts the gateway honours the MCP 2026-07-28 stateless contract.

Unlike e2e_smoke.py (which checks initialize + tools/list work), this verifies
the *stateless* guarantees the migration depends on — the properties a
round-robin load balancer needs to be safe:

  1. POST /mcp returns NO `Mcp-Session-Id` header (no sticky sessions).
  2. The response content-type is JSON (json_response mode), not an SSE stream.
  3. Two INDEPENDENT requests each succeed with no shared session state —
     i.e. the second request does not depend on a session established by the first.

Run against a booted gateway (see test-gateway.yml e2e job):
    PORT=8000 python http_server.py &
    GATEWAY_URL=http://127.0.0.1:8000/mcp python tests/stateless_check.py

Exits non-zero on any violation. Stdlib only — no extra CI deps.
"""
import json
import os
import sys
import urllib.request

URL = os.environ.get("GATEWAY_URL", "http://127.0.0.1:8000/mcp")

_INIT = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "stateless-check", "version": "0"},
    },
}


def _post(body: dict):
    """POST one self-contained JSON-RPC request; return (status, headers, raw body)."""
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        URL,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.status, {k.lower(): v for k, v in resp.headers.items()}, resp.read()


def main() -> None:
    failures = []

    status1, headers1, _ = _post(_INIT)
    if status1 != 200:
        failures.append(f"first request status {status1} != 200")

    # 1. no sticky-session header
    if "mcp-session-id" in headers1:
        failures.append(f"Mcp-Session-Id header present ({headers1['mcp-session-id']!r}) — not stateless")
    else:
        print("OK: no Mcp-Session-Id header")

    # 2. JSON response, not an SSE stream
    ctype = headers1.get("content-type", "")
    if "application/json" not in ctype:
        failures.append(f"content-type {ctype!r} is not application/json (json_response off?)")
    else:
        print(f"OK: content-type is {ctype}")

    # 3. a second, fully independent request succeeds with no carried session
    status2, headers2, _ = _post(_INIT)
    if status2 != 200:
        failures.append(f"second independent request status {status2} != 200")
    elif "mcp-session-id" in headers2:
        failures.append("second request returned a session id — server is stateful")
    else:
        print("OK: second independent request succeeded statelessly")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        sys.exit(1)
    print("stateless contract OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"stateless-check FAILED: {exc!r}", file=sys.stderr)
        sys.exit(1)
