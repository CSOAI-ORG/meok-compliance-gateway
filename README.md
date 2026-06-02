# MEOK Compliance Gateway

Streamable-HTTP / containerized builds of MEOK AI Labs compliance MCP servers —
the HTTP transport that cloud marketplaces (AWS Bedrock AgentCore, Google, Azure,
Smithery) and x402 monetization require.

`http_server.py` serves any MEOK FastMCP server over streamable-HTTP at `/mcp`
(verified: `initialize` → HTTP 200). One container image per flagship via the
`PKG` build arg. See **LISTING.md** for the full deploy + marketplace playbook.

```bash
docker build --build-arg PKG=eu-ai-act-compliance-mcp -t meok/eu-ai-act .
docker run -p 8000:8000 meok/eu-ai-act    # → POST /mcp
```

Flagships: eu-ai-act · dora · nis2 · cra (+ any of the 290 MEOK MCP servers).
MIT-licensed. MEOK AI Labs (CSOAI LTD, UK CH 16939677).
