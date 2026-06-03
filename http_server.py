"""MEOK compliance MCP — streamable-HTTP entrypoint for cloud/marketplace deployment.

Serves any MEOK FastMCP server over streamable-HTTP at /mcp on 0.0.0.0:$PORT.

DNS-rebinding host check is disabled because the platform (Cloud Run / AWS / proxy)
terminates TLS and controls ingress; the *.run.app host is dynamic and trusted.
DO NOT RE-ENABLE without also adding the platform's proxy IP ranges to the
allow-list — otherwise every request returns 421.
"""
import os
import server
from mcp.server.transport_security import TransportSecuritySettings
from starlette.responses import JSONResponse

mcp = server.mcp
mcp.settings.host = "0.0.0.0"
mcp.settings.port = int(os.environ.get("PORT", "8000"))
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,
)


@mcp.custom_route("/healthz", methods=["GET"])
async def healthz(_request):
    """Liveness probe — separate from /mcp so orchestrators don't POST initialize."""
    return JSONResponse({"status": "ok", "server": "meok-compliance-gateway"})


@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET"])
async def oauth_protected_resource(_request):
    """RFC 9728 metadata — required for marketplace OAuth clients (AWS AgentCore,
    Smithery, Cloudflare Agents SDK) to discover auth endpoints."""
    # When real auth is wired up, point `authorization_servers` at the live IdP.
    return JSONResponse(
        {
            "resource": f"https://{os.environ.get('PUBLIC_HOST', 'localhost')}/mcp",
            "authorization_servers": [],
            "bearer_methods_supported": ["header"],
            "scopes_supported": ["mcp:tools"],
        }
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
