"""MEOK compliance MCP — streamable-HTTP entrypoint for cloud/marketplace deployment.
Wraps any MEOK FastMCP server (which installs a top-level `server` module) and serves
it over streamable-HTTP at /mcp on 0.0.0.0:$PORT. Unlocks AWS AgentCore, Google, Azure,
Smithery, and x402 wrapping — all of which require HTTP, not stdio."""
import os, server  # `server` is the top-level module each MEOK package installs
mcp = server.mcp
mcp.settings.host = "0.0.0.0"
mcp.settings.port = int(os.environ.get("PORT", "8000"))
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
