# Security Policy — MEOK Compliance Gateway

## Supported versions
| Version | Supported |
|---|---|
| Latest (main) | ✅ |
| Older | ❌ — please upgrade |

## Reporting a vulnerability
**Please do not open a public GitHub issue for security problems.**

Email: **security@meok.ai** (PGP key on request).
Subject prefix: `[SECURITY][meok-compliance-gateway]`

We acknowledge within 48 hours and aim to ship a fix within 7 days for
critical issues. We follow responsible disclosure — please give us a
reasonable window before any public writeup.

## Scope
- The `http_server.py` streamable-HTTP shim
- The Dockerfile + `build_all.sh` build pipeline
- The `/mcp`, `/healthz`, and `/.well-known/oauth-protected-resource` routes

## Out of scope
- The installed flagship `server` package (file the issue against that repo)
- The Cloud Run / AWS AgentCore / Smithery deployment platform itself
- x402 paywall behavior (file the issue against `meok-x402-wrap-mcp`)

## Hardening notes (for operators)
- DNS-rebinding protection is **disabled** by design because Cloud Run / AWS
  reverse-proxy ingress terminates TLS and the upstream host is dynamic. See
  the comment block in `http_server.py` for the rationale. If you re-enable
  it, you must also allow-list your platform's proxy IP ranges or every
  request returns 421.
- `/.well-known/oauth-protected-resource` returns an empty
  `authorization_servers` array by default. Wire up a real OAuth 2.1 + PKCE
  IdP before exposing the gateway to untrusted clients.
- `/healthz` is unauthenticated by design (load balancers need it). `/mcp`
  is the only stateful endpoint.
