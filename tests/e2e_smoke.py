"""Real end-to-end smoke test for the MEOK compliance gateway.

Unlike a mock, this drives the ACTUAL server: it connects to a running
`http_server.py` (which must have a flagship PKG installed so `import server`
resolves), performs the real MCP initialize handshake over streamable-HTTP,
and lists the flagship's tools.

Usage (CI or local):
    pip install -r requirements-gateway.txt eu-ai-act-compliance-mcp
    PORT=8000 python http_server.py &        # boot the gateway
    python tests/e2e_smoke.py                 # exits non-zero on failure

Env:
    GATEWAY_URL  override the endpoint (default http://127.0.0.1:8000/mcp)
"""
import os
import sys

import anyio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = os.environ.get("GATEWAY_URL", "http://127.0.0.1:8000/mcp")


async def main() -> None:
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            info = init.serverInfo
            print(f"initialize OK — {info.name} {info.version}")

            tools = await session.list_tools()
            names = [t.name for t in tools.tools]
            if not names:
                raise SystemExit("FAIL: server returned zero tools")
            print(f"tools/list OK — {len(names)} tools: {names[:5]}{' …' if len(names) > 5 else ''}")


if __name__ == "__main__":
    try:
        anyio.run(main)
    except Exception as exc:  # noqa: BLE001 — surface any failure as a non-zero exit
        print(f"e2e FAILED: {exc!r}", file=sys.stderr)
        sys.exit(1)
    print("e2e OK")
