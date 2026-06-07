"""Streamable-HTTP entrypoint for AgentAudit MCP server."""

from __future__ import annotations

import os

from mcp.server.streamable_http import TransportSecuritySettings

from agentaudit.server import mcp

mcp.settings.host = "0.0.0.0"
mcp.settings.port = int(os.environ.get("PORT", "8000"))
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,
)


@mcp.app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "agentaudit"}


@mcp.app.get("/.well-known/oauth-protected-resource")
def oauth_metadata() -> dict[str, str]:
    return {
        "resource": os.environ.get("OAUTH_RESOURCE", "https://agentaudit.meok.ai"),
        "authorization_servers": [
            os.environ.get("OAUTH_ISSUER", "https://auth.meok.ai")
        ],
    }


if __name__ == "__main__":  # pragma: no cover
    mcp.run(transport="streamable-http")
