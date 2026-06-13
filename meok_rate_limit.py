"""MEOK free-tier rate limiter — daily cap per tool per anonymous caller.

Why this exists
---------------
Without a cap, an agent can call `list_experts` 10,000 times a day and
never encounter the paywall. That's not a funnel, it's free compute.
A real revenue funnel is: free tier (5 calls/day per tool) → paywall.

Design
------
* Per-tool counter, daily, resets at UTC midnight.
* Caller identity: best-effort from the MCP request context. For anonymous
  callers we use a per-process sentinel ("anon") so heavy hitters get
  capped even without auth. Authed callers (MEOK_API_KEY in `_meta`) get
  a stable key.
* Counts live in-process (dict, bounded). For multi-instance, swap to
  Redis with the same API. The keystone doesn't ship a Redis dep yet.
* Paying callers bypass the cap: `meok_x402.is_paid_call()` is checked
  before the cap, and `is_paid_call()` is True only inside a verified
  `@paywalled` wrapper body.
* Free tools only. The paywalled tools already have their gate.

Usage
-----
    from meok_rate_limit import free_tier_check

    @mcp.tool(description="List the 14 OpenScore safety experts (free, top-of-funnel).")
    def list_experts(ctx=None) -> str:
        if err := free_tier_check("list_experts", ctx, limit=5):
            return json.dumps(err)  # returns the 429-like JSON
        ...

Returns
-------
On allow: None (caller proceeds).
On deny: dict with `error`, `code=429`, `retry_after_seconds`, `limit`,
`reset_at` — JSON-serialisable so the tool can return it directly.
"""
from __future__ import annotations

import functools
import json
import time
from collections import defaultdict
from threading import Lock
from typing import Any, Callable, Optional

# Tool name → daily cap. Override per-deployment via env if needed
# (e.g. a flagship might want 100 free calls/day to seed adoption).
_DEFAULT_LIMITS = {
    "list_experts": 5,
    "spending_report": 20,    # observability: a bit more headroom
    "health": 1000,           # liveness: effectively unlimited
}
_LOCK = Lock()
# (tool, caller, day) -> count
_COUNTS: dict[tuple[str, str, int], int] = defaultdict(int)


def _caller_id(ctx: Any) -> str:
    """Best-effort caller identity. Authed → API key. Unauthed → 'anon'.

    In production, an authed call would carry MEOK_API_KEY in `_meta`; we
    hash it (don't store raw keys). For anonymous calls, we use a sentinel
    so a single anonymous flooder gets capped.
    """
    if ctx is None:
        return "anon"
    try:
        from meok_x402 import _extract_meta
        meta = _extract_meta(ctx)
        key = meta.get("MEOK_API_KEY")
        if key and isinstance(key, str):
            # Truncated hash — enough to bucket per-caller without storing keys
            import hashlib
            return "auth:" + hashlib.sha256(key.encode()).hexdigest()[:16]
    except Exception:
        pass
    return "anon"


def _utc_day() -> int:
    return int(time.time() // 86400)


def _seconds_until_utc_midnight() -> int:
    now = time.time()
    return int(86400 - (now % 86400))


def free_tier_check(tool_name: str, ctx: Any, *, limit: Optional[int] = None) -> Optional[dict]:
    """Check + increment the daily counter. Return None on allow, error dict on deny.

    Parameters
    ----------
    tool_name : str
        The tool's name (used as the bucket key).
    ctx : Any
        The FastMCP Context (or None for unkeyed calls).
    limit : int | None
        Override the default limit for this tool. If None, uses
        `_DEFAULT_LIMITS[tool_name]` (or 5 if unset).
    """
    # Paying callers bypass the cap.
    try:
        from meok_x402 import is_paid_call
        if is_paid_call():
            return None
    except ImportError:
        pass

    cap = limit if limit is not None else _DEFAULT_LIMITS.get(tool_name, 5)
    caller = _caller_id(ctx)
    day = _utc_day()
    key = (tool_name, caller, day)

    with _LOCK:
        if _COUNTS[key] >= cap:
            return {
                "error": "free tier daily limit reached",
                "code": 429,
                "limit": cap,
                "reset_at_seconds": _seconds_until_utc_midnight(),
                "tool": tool_name,
                "hint": "call sign_receipt or verify_receipt (paywalled) to remove the cap",
            }
        _COUNTS[key] += 1
        return None


def free_tier_snapshot() -> dict:
    """Return the current free-tier counters. For observability/audit.

    Free tool. No PII (caller ids are truncated hashes or 'anon').
    """
    with _LOCK:
        snapshot: dict[str, dict[str, int]] = defaultdict(dict)
        for (tool, caller, day), count in _COUNTS.items():
            snapshot[tool][caller] = count
    return {
        "utc_day": _utc_day(),
        "by_tool": {k: dict(v) for k, v in snapshot.items()},
        "limits": dict(_DEFAULT_LIMITS),
    }


def ratelimited(tool_name: str, *, limit: Optional[int] = None) -> Callable:
    """Decorator. Free tools: wrap with a free-tier check.

    Usage:
        @mcp.tool(description="...")
        @ratelimited("list_experts")
        def list_experts(ctx=None) -> str:
            ...
    """
    def deco(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            ctx = kwargs.get("ctx")
            err = free_tier_check(tool_name, ctx, limit=limit)
            if err is not None:
                return json.dumps(err)
            return fn(*args, **kwargs)
        return wrapper
    return deco
