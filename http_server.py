"""MEOK compliance MCP — streamable-HTTP entrypoint for cloud/marketplace deployment.
Serves any MEOK FastMCP server over streamable-HTTP at /mcp on 0.0.0.0:$PORT.
DNS-rebinding host check is disabled because the platform (Cloud Run / AWS / proxy)
terminates TLS and controls ingress; the *.run.app host is dynamic and trusted."""
import os, server
from mcp.server.transport_security import TransportSecuritySettings
mcp = server.mcp
mcp.settings.host = "0.0.0.0"
mcp.settings.port = int(os.environ.get("PORT", "8000"))
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,
)
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
