# Security Policy — AgentAudit

## Supported versions
| Version | Supported |
|---|---|
| Latest (main) | ✅ |
| Older | ❌ — please upgrade |

## Reporting a vulnerability
**Please do not open a public GitHub issue for security problems.**

Email: **security@meok.ai** (PGP key on request).
Subject prefix: `[SECURITY][agentaudit]`

We acknowledge within 48 hours and aim to ship a fix within 7 days for
critical issues. We follow responsible disclosure — please give us a
reasonable window before any public writeup.

## Scope
- The `agentaudit/agentaudit/` package (`server.py`, `x402.py`, `audit_trail.py`,
  `signet.py`, `bft.py`, `openscore.py`, `compliance_matrix.py`, `safety_experts.py`,
  `shadow_scanner.py`).
- The Signet Ed25519 receipt flow + BFT consensus state.
- The MCP server (stdio + streamable HTTP via `http_server.py`).
- The Dockerfile + `DEPLOY.sh` / `UPLOAD.sh` build pipeline.

## Out of scope
- The keystone `meok-compliance-gateway` wrapper (file the issue there).
- The x402 facilitator at `x402.org` or any other third-party USDC settlement
  service.
- Cloud Run / AWS AgentCore / Smithery / PyPI deployment platforms.

## Hardening notes (for operators)
- **x402 paywall is off by default.** Set `X402_ENABLED=1` only on deployments
  that have a real `X402_PAY_TO` wallet configured. The paywire is a transparent
  no-op when the env var is unset, so self-host and tests are unaffected.
- **In-memory state.** `_trails`, `_bft_states`, `_PAID_LOG` are in-memory dicts /
  deques. A production deployment should swap these for Redis / Postgres
  (the dicts exist in the same module to make that swap a one-line change).
  The paid-call log is bounded (10k entries) to avoid unbounded growth.
- **Signet signing key** is derived from `SIGNET_SEED` if set, otherwise
  generated ephemerally (no persistence). Treat the seed like a private key.
- **DNS-rebinding protection is disabled** by default in the HTTP wrapper
  (Cloud Run / AWS proxy ingress terminates TLS with dynamic upstreams; see the
  comment block in `http_server.py` for the rationale).
- **Audit-trail integrity** is enforced via Signet Ed25519 + a hash chain
  (see `audit_trail.py`). `verify_audit_trail` returns the broken entry IDs
  and any invalid signatures — call it after every batch ingest.
- **BFT finality is honest, not Sybil-resistant.** A 5-node cluster assumes
  honest nodes; the Signet receipt on `finalize_bft_round` attests the
  majority hash, not the identity of voters. Use the receipt as
  cross-party evidence, not as a unique proof.

## Threat model (what we defend, what we don't)
- **Defend against:** tampering with audit entries, replay of stale BFT votes,
  silent bypass of the x402 paywall, signature forgery on Signet receipts.
- **Don't defend against:** compromised node identity (no PKI on BFT nodes —
  the trust comes from the Signet receipt over the *count* of votes, not the
  *identity* of voters), facilitator downtime (the wrapper fails open so
  paying customers are not locked out), running untrusted MCP input as code
  (the server is a tool, not a sandbox).
