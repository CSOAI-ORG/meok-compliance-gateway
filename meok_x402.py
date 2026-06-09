"""MEOK x402 — per-call monetization for high-value MCP tools.

A second revenue rail that stacks on the existing Stripe subscriptions: it bills
*autonomous agents* per call in USDC, and (on first settled payment) auto-lists the
endpoint in the x402 Bazaar / AWS AgentCore. The flagships stay free/MIT for human
self-host; this only activates when a deployment opts in.

Design — correct x402-over-MCP semantics (NOT HTTP 402, which MCP clients can't read):
the payment travels in the MCP request `_meta["x402/payment"]`, and the challenge is
returned to the client describing price + how to pay (mirrors the x402 SDK's
`create_payment_wrapper`, bridged onto FastMCP's `@mcp.tool()` convention).

OFF by default: with `X402_ENABLED` unset, `@paywalled(...)` returns the function
UNCHANGED — zero overhead, zero behaviour change, so existing builds/tests are unaffected.

Turn on per-deployment via env:
    X402_ENABLED=1
    X402_PAY_TO=0xYourBaseWallet      # Coinbase CDP receiving address  ← NEEDS NICK
    X402_PRICE=$0.10                  # default price per call (override per-tool)
    X402_NETWORK=eip155:8453          # Base mainnet (84532 = Base Sepolia testnet)
    X402_ASSET=0x833589fCD6...        # optional; defaults to USDC for the network
    X402_FACILITATOR_URL=https://x402.org/facilitator   # optional override

Usage in a flagship `server.py` (apply only to high-value tools; leave quick_scan /
deadline_check FREE as top-of-funnel):

    from meok_x402 import paywalled
    from mcp.server.fastmcp import Context

    @mcp.tool()
    @paywalled(price="$0.25")   # COST WARNING surfaced in the tool description (AWS convention)
    def audit_report(system: str, ctx: Context) -> dict:
        ...
"""
from __future__ import annotations

import collections
import contextvars
import functools
import json
import logging
import math
import os
import time
from typing import Any, Callable, Optional

log = logging.getLogger("meok.x402")

# True while the wrapped tool body runs under a VERIFIED x402 payment. Flagship
# rate-limiters consult this so paying agents bypass the free-tier daily cap.
_paid_call: contextvars.ContextVar[bool] = contextvars.ContextVar("meok_x402_paid", default=False)

# ── Secret resolution for the (future) MEOK_ATTESTATION_KEY ─────────────────
# Per the SOV3 master audit (CRITICAL #3, sov3_mcp_master_audit.docx 2026-06-08),
# the HMAC-SHA256 signing key for compliance attestations MUST NEVER live in an
# env var: `printenv` shows it, container introspection shows it, any subprocess
# inherits it. An attacker who reads it can forge any compliance attestation,
# which breaks the entire attestation chain.
#
# Resolution order: AWS Secrets Manager → meok_secrets (keyring → file, with
# chmod 600) → env (dev only, warns) → fail closed. Env-only is rejected in
# production (`MEOK_ENV=production`). See CRITICAL_FIXES_2026-06-08.md Fix #3
# for the full rationale.
_ATTESTATION_KEYRING_USER = "attestation-key"
_ATTESTATION_AWS_SECRET_ID = "meok/attestation-key"


def _resolve_attestation_key() -> bytes:
    """Read the HMAC-SHA256 signing key from a secret store. Never env-only.

    Order:
      1. AWS Secrets Manager (production).
      2. meok_secrets (keyring → file-with-chmod-600; ref impl of Fix #2).
      3. MEOK_ATTESTATION_KEY env var — only in dev, with a loud warning.
      4. Otherwise: fail closed (refuse to start an attestation issuer).
    """
    # 1. AWS Secrets Manager (production path)
    try:
        import boto3  # type: ignore
        client = boto3.client("secretsmanager")
        resp = client.get_secret_value(SecretId=_ATTESTATION_AWS_SECRET_ID)
        val = resp.get("SecretString")
        if val:
            return val.encode()
    except ImportError:
        pass  # boto3 not installed → skip to meok_secrets
    except Exception as exc:  # noqa: BLE001
        log.debug("AWS Secrets Manager lookup failed (will try meok_secrets): %r", exc)

    # 2. meok_secrets (the keystone's audited secret-store wrapper)
    try:
        from meok_secrets import get_secret  # local module, stdlib-only
        val = get_secret(_ATTESTATION_KEYRING_USER)
        if val:
            return val.encode()
    except ImportError:
        pass  # module not on path (e.g. running tests in isolation)
    except Exception as exc:  # noqa: BLE001
        log.debug("meok_secrets lookup failed (will try env): %r", exc)

    # 3. Env var fallback (dev/test ONLY)
    val = os.environ.get("MEOK_ATTESTATION_KEY")
    if val:
        env_name = os.environ.get("MEOK_ENV", "development").lower()
        if env_name == "production":
            raise RuntimeError(
                "MEOK_ATTESTATION_KEY was set in the environment, but MEOK_ENV=production. "
                "Per the SOV3 master audit (CRITICAL #3) the HMAC signing key must NOT be "
                "in an env var in production. Use AWS Secrets Manager (id="
                f"{_ATTESTATION_AWS_SECRET_ID!r}) or meok_secrets (name={_ATTESTATION_KEYRING_USER!r})."
            )
        log.warning(
            "MEOK_ATTESTATION_KEY read from env var in dev mode. "
            "This is the audit-flagged CRITICAL #3 pattern — move to meok_secrets / "
            "AWS Secrets Manager before MEOK_ENV=production."
        )
        return val.encode()

    # 4. Fail closed — never default to anything
    raise RuntimeError(
        "MEOK_ATTESTATION_KEY not found in AWS Secrets Manager, meok_secrets, or env. "
        "Refusing to start attestation signing to prevent forgery. "
        f"Set it via: aws secretsmanager create-secret --name {_ATTESTATION_AWS_SECRET_ID} "
        f"--secret-string <32-bytes-base64>  OR  "
        f"python -c \"import meok_secrets; meok_secrets.set_secret({_ATTESTATION_KEYRING_USER!r}, '<key>')\""
    )


def is_paid_call() -> bool:
    """True if the current tool invocation is backed by a verified x402 payment."""
    return _paid_call.get()

# Rolling in-memory log of verified paid calls. Bounded so a long-running server
# doesn't grow unbounded. Surfaced via `spending_snapshot()` (free observability
# endpoint) so enterprise buyers can audit their call volume. NEVER persisted
# to ~/.meok/ — that directory holds the live fleet counters and is hermetic
# to tests.
_PAID_LOG: collections.deque = collections.deque(maxlen=10_000)


def _record_paid_call(tool_name: str, price: str, payer: str) -> None:
    """Append a single record to the rolling paid-call log. Best-effort, no I/O."""
    _PAID_LOG.append({
        "tool": tool_name,
        "price": price,
        "payer": payer,
        "ts": time.time(),
    })


def _payer_hint(payment: Any) -> str:
    """Best-effort pull of a payer address from a payment payload, for the spending log."""
    if isinstance(payment, dict):
        for key in ("from", "payer", "address", "wallet"):
            v = payment.get(key)
            if isinstance(v, str) and v.startswith("0x"):
                return v[:10] + "…" + v[-4:] if len(v) > 14 else v
        auth = payment.get("payload", {}).get("authorization") if isinstance(payment.get("payload"), dict) else None
        if isinstance(auth, dict):
            f = auth.get("from")
            if isinstance(f, str) and f.startswith("0x"):
                return f[:10] + "…" + f[-4:] if len(f) > 14 else f
    return "unknown"


def spending_snapshot() -> dict[str, Any]:
    """Return the current in-memory paid-call log + summary stats.

    Free observability endpoint — the gateway to enterprise buyers
    (reconciliation against their facilitator dashboard). No PII: payer
    is the truncated hex address embedded in the x402 payment payload,
    not a user identifier.
    """
    if not _PAID_LOG:
        return {"total_calls": 0, "by_tool": {}, "recent": []}
    by_tool: dict[str, int] = {}
    for rec in _PAID_LOG:
        by_tool[rec["tool"]] = by_tool.get(rec["tool"], 0) + 1
    recent = list(_PAID_LOG)[-50:]
    return {
        "total_calls": len(_PAID_LOG),
        "by_tool": by_tool,
        "recent": [
            {"tool": r["tool"], "price": r["price"], "payer": r["payer"], "ts": r["ts"]}
            for r in recent
        ],
    }

# x402/payment carries the signed payment; x402/payment-response carries the challenge.
PAYMENT_META_KEY = "x402/payment"
PAYMENT_RESPONSE_META_KEY = "x402/payment-response"

# Canonical USDC (6-decimal) per network, used when X402_ASSET is unset.
_USDC = {
    "eip155:8453": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",   # Base mainnet
    "eip155:84532": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",  # Base Sepolia
}
_USDC_DECIMALS = 6


def enabled() -> bool:
    """True only when the deployment has explicitly opted into x402 billing."""
    return os.environ.get("X402_ENABLED", "").strip().lower() in ("1", "true", "yes", "on")


def _network() -> str:
    return os.environ.get("X402_NETWORK", "eip155:8453")


def _asset(network: str) -> str:
    return os.environ.get("X402_ASSET") or _USDC.get(network, _USDC["eip155:8453"])


def _price_to_atomic(price: str) -> str:
    """'$0.10' -> '100000' (USDC has 6 decimals). Accepts bare numbers too."""
    try:
        dollars = float(str(price).strip().lstrip("$"))
    except ValueError:
        raise ValueError(f"X402 price must be a dollar amount like '$0.10', got: {price!r}") from None
    if not math.isfinite(dollars):
        # float() happily parses 'inf'/'nan'; without this guard they surface as
        # OverflowError / a cryptic NaN message from int(round(...)) (found by fuzz).
        raise ValueError(f"X402 price must be a finite dollar amount like '$0.10', got: {price!r}")
    return str(int(round(dollars * (10 ** _USDC_DECIMALS))))


def _accepts(price: str) -> list:
    """The PaymentRequirements list for this deployment's wallet/network/price."""
    from x402.schemas import PaymentRequirements

    network = _network()
    return [
        PaymentRequirements(
            scheme="exact",
            network=network,
            asset=_asset(network),
            amount=_price_to_atomic(price),
            pay_to=os.environ["X402_PAY_TO"],
            max_timeout_seconds=int(os.environ.get("X402_TIMEOUT", "300")),
        )
    ]


def build_challenge(tool_name: str, price: str, error: str = "Payment required") -> dict:
    """Return the spec-correct x402 PaymentRequired challenge as wire JSON.

    Pure/deterministic — no chain calls, no wallet — so it is unit-testable and is
    also what an x402-aware MCP client reads to construct its payment.
    """
    from x402 import ResourceInfo
    from x402.schemas import PaymentRequired

    challenge = PaymentRequired(
        x402_version=1,
        error=error,
        resource=ResourceInfo(url=f"mcp://tool/{tool_name}", service_name="meok-compliance-gateway"),
        accepts=_accepts(price),
    )
    return challenge.model_dump(by_alias=True)


# ── facilitator (verify/settle) is lazy: only imported once a payment is presented,
#    so the EVM/web3 dependency tree never loads for the free-discovery path. ──────────
_server = None


def _resource_server():
    global _server
    if _server is None:
        from x402 import x402ResourceServerSync
        from x402.http import HTTPFacilitatorClientSync

        url = os.environ.get("X402_FACILITATOR_URL")
        facilitator = HTTPFacilitatorClientSync({"url": url}) if url else HTTPFacilitatorClientSync()
        _server = x402ResourceServerSync(facilitator)
    return _server


def _extract_meta(ctx: Any) -> dict:
    """Best-effort read of the MCP request `_meta` from a FastMCP Context."""
    for path in (
        lambda: ctx.request_context.request.params.meta,
        lambda: ctx.request_context.meta,
        lambda: ctx.request_context.request.params.model_extra.get("_meta"),
    ):
        try:
            meta = path()
            if meta:
                return dict(meta)
        except Exception:
            continue
    return {}


def _find_ctx(args: tuple, kwargs: dict):
    if "ctx" in kwargs:
        return kwargs["ctx"]
    for v in list(kwargs.values()) + list(args):
        # duck-type a FastMCP Context without importing it at module load
        if hasattr(v, "request_context"):
            return v
    return None


def _unpaid(tool_name: str, price: str, error: str = "Payment required"):
    """Emit the challenge in x402's canonical MCP shape: an isError result whose text
    is the PaymentRequired JSON (mirrors the SDK's create_payment_wrapper). Raising
    ToolError keeps FastMCP's typed-output validation out of the way for `-> str` tools.
    """
    envelope = {PAYMENT_RESPONSE_META_KEY: build_challenge(tool_name, price, error)}
    try:
        from mcp.server.fastmcp.exceptions import ToolError
    except ImportError:  # non-FastMCP harness (e.g. unit tests without mcp)
        return envelope
    raise ToolError(json.dumps(envelope))


def paywalled(price: Optional[str] = None, *, tool_name: Optional[str] = None) -> Callable:
    """Decorator for a FastMCP tool. No-op unless X402_ENABLED.

    When enabled, the decorated tool must be able to see the request `_meta` — declare a
    `ctx: Context` parameter so FastMCP injects it. If no valid payment is present the
    tool returns the x402 challenge (price + pay-to); otherwise the call runs and the
    payment is verified/settled via the facilitator.
    """
    price = price or os.environ.get("X402_PRICE", "$0.10")

    def deco(fn: Callable) -> Callable:
        if not enabled():
            return fn  # transparent passthrough — free self-host unaffected
        name = tool_name or fn.__name__

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            ctx = _find_ctx(args, kwargs)
            payment = _extract_meta(ctx).get(PAYMENT_META_KEY)
            if not payment:
                return _unpaid(name, price)
            try:
                server = _resource_server()
                reqs = server.find_matching_requirements(_accepts(price), payment)
                verify = server.verify_payment(payment, reqs)
                if not getattr(verify, "is_valid", False):
                    return _unpaid(name, price, getattr(verify, "invalid_reason", None) or "verification failed")
                token = _paid_call.set(True)  # lets flagship rate-limiters waive the free-tier cap
                _record_paid_call(name, price, _payer_hint(payment))
                try:
                    result = fn(*args, **kwargs)
                finally:
                    _paid_call.reset(token)
                try:
                    server.settle_payment(payment, reqs)  # best-effort settle
                except Exception as exc:  # noqa: BLE001
                    log.warning("x402 settle failed for %s: %r", name, exc)
                return result
            except Exception as exc:  # noqa: BLE001 — never let billing break the tool
                if type(exc).__name__ == "ToolError":
                    raise  # the challenge itself — must reach the client, not fail open
                log.error("x402 path errored for %s, failing OPEN (serving the call): %r", name, exc)
                return fn(*args, **kwargs)

        return wrapper

    return deco
