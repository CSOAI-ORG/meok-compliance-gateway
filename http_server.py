"""MEOK compliance MCP — streamable-HTTP entrypoint for cloud/marketplace deployment.

Serves any MEOK FastMCP server over streamable-HTTP at /mcp on 0.0.0.0:$PORT.

DNS-rebinding host check is disabled because the platform (Cloud Run / AWS / proxy)
terminates TLS and controls ingress; the *.run.app host is dynamic and trusted.
DO NOT RE-ENABLE without also adding the platform's proxy IP ranges to the
allow-list — otherwise every request returns 421.
"""
import json
import logging
import os
import server
from pathlib import Path
from mcp.server.transport_security import TransportSecuritySettings
from starlette.responses import JSONResponse

log = logging.getLogger("meok.http_server")

# --- Keystone metadata (server.json) ---------------------------------------
# http_server.py ships alongside server.json at the keystone root. The
# container layout in Dockerfile copies http_server.py into /app where
# server.json is installed by the flagship PKG (eu-ai-act-compliance-mcp
# etc.). If we can find it, surface its name/version in /health and the
# A2A agent card. Otherwise synthesize a minimal payload from env + filename.
_SERVER_JSON_CANDIDATES = [
    Path("/app/server.json"),  # container (Dockerfile WORKDIR /app)
    Path(__file__).resolve().parent / "server.json",  # keystone checkout
]
_SERVER_JSON_PATH = next(
    (p for p in _SERVER_JSON_CANDIDATES if p.is_file()), None
)
_SERVER_JSON = {}
if _SERVER_JSON_PATH is not None:
    try:
        with _SERVER_JSON_PATH.open("r", encoding="utf-8") as _f:
            _SERVER_JSON = json.load(_f)
    except (OSError, json.JSONDecodeError) as _e:
        log.warning("server.json present at %s but unreadable: %s", _SERVER_JSON_PATH, _e)

_MEOK_VERSION = str(
    _SERVER_JSON.get("version")
    or os.environ.get("MEOK_VERSION")
    or "unknown"
)
_MEOK_NAME = str(
    _SERVER_JSON.get("name")
    or os.environ.get("MEOK_NAME")
    or "meok-api"
)
_MEOK_PUBLIC_URL = os.environ.get("PUBLIC_URL", "https://gateway.meok.ai")

mcp = server.mcp
mcp.settings.host = "0.0.0.0"
mcp.settings.port = int(os.environ.get("PORT", "8000"))
mcp.settings.transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False,
)
# Stateless mode (MCP 2026-07-28 migration, Phase 0 — see MCP_2026_07_28_SPIKE.md):
# no Mcp-Session-Id stickiness, every request self-contained, JSON responses
# instead of SSE streams. Works on mcp==1.27.2 today; aligns runtime behaviour
# with the stateless spec before the SDK ships full 2026-07-28 support.
# x402 is unaffected: payment travels per-request in _meta["x402/payment"].
mcp.settings.stateless_http = True
mcp.settings.json_response = True


@mcp.custom_route("/health", methods=["GET"])
async def health(_request):
    """Liveness probe for the MEOK_API cron (port 3200).

    Returns HTTP 200 with a small JSON status payload. Distinct from
    ``/healthz`` (the Docker HEALTHCHECK target, kept stdlib-only) so the
    heartbeat cron can target a stable name without conflicting with the
    orchestrator probe.
    """
    return JSONResponse(
        {"status": "ok", "service": "meok-api", "version": _MEOK_VERSION}
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


@mcp.custom_route("/.well-known/agent-card.json", methods=["GET"])
async def agent_card(_request):
    """A2A agent card (Google A2A spec §5) — JSON-LD.

    Discovery endpoint for A2A clients (the CSOAI-ORG agent mesh, plus
    third-party A2A runtimes) to find this server's skills, auth, and
    transport. Prefers the on-disk ``server.json`` (which already carries
    the MCP Registry ``name``/``version``/``description``); falls back to
    a minimal hand-built card from the keystone's known fields.
    """
    public_url = _MEOK_PUBLIC_URL.rstrip("/")
    if _SERVER_JSON.get("name") and _SERVER_JSON.get("version"):
        card = {
            "@context": "https://a2a-protocol.org/schema/v1/agent-card.jsonld",
            "@type": "Agent",
            "name": _SERVER_JSON.get("title") or _SERVER_JSON["name"],
            "description": _SERVER_JSON.get("description", ""),
            "version": _SERVER_JSON["version"],
            "url": public_url,
            "provider": _SERVER_JSON.get("publisher", {}).get("name", "MEOK AI Labs"),
            "capabilities": {
                "streaming": True,
                "pushNotifications": False,
                "stateTransitionHistory": True,
            },
            "defaultInputModes": ["application/json", "text/plain"],
            "defaultOutputModes": ["application/json"],
            "skills": _SERVER_JSON.get("examples", []),
            "endpoints": {"mcp": f"{public_url}/mcp"},
        }
    else:
        # Minimal fallback — no server.json on disk, no env override.
        card = {
            "@context": "https://a2a-protocol.org/schema/v1/agent-card.jsonld",
            "@type": "Agent",
            "name": _MEOK_NAME,
            "description": "MEOK Compliance Gateway — streamable-HTTP MCP server.",
            "version": _MEOK_VERSION,
            "url": public_url,
            "provider": "MEOK AI Labs",
            "capabilities": {
                "streaming": True,
                "pushNotifications": False,
                "stateTransitionHistory": True,
            },
            "defaultInputModes": ["application/json", "text/plain"],
            "defaultOutputModes": ["application/json"],
            "skills": [],
            "endpoints": {"mcp": f"{public_url}/mcp"},
        }
    return JSONResponse(card)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
