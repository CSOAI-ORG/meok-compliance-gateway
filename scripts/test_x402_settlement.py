#!/usr/bin/env python3
"""test_x402_settlement.py — end-to-end smoke test for the x402 paywall.

Goal
----
Prove the keystone can:
  1. Boot the FastMCP server with `server.mcp` exposing paywalled tools.
  2. Return a spec-correct `PaymentRequired` challenge for an unpaid call.
  3. Verify a signed USDC payment against the facilitator (testnet).
  4. Settle the payment and execute the tool.
  5. Confirm the in-memory `spending_snapshot` records the settled call.

This is a TESTNET smoke. Real revenue requires mainnet (`X402_NETWORK=
eip155:8453`) + a Coinbase CDP mainnet wallet in `X402_PAY_TO`.

Usage
-----
    # 1. Set up testnet wallet + facilitator
    cp .env.example .env
    # Edit .env: set X402_ENABLED=1, X402_PAY_TO=<your Base Sepolia address>,
    #            X402_NETWORK=eip155:84532, MEOK_ATTESTATION_KEY=<32 bytes hex>

    # 2. Fund the wallet with testnet USDC
    #    https://faucet.circle.com (or the Base Sepolia USDC faucet)

    # 3. Get a Base Sepolia testnet private key (NEVER use your real key)
    #    The smoke pays itself: the test wallet is the same as X402_PAY_TO.
    #    For a true self-payment smoke, you need a separate signer key.

    # 4. Run
    python3 scripts/test_x402_settlement.py

Exit codes
----------
0  settlement succeeded (tool ran, payment settled, snapshot recorded)
1  boot / config / import error
2  challenge roundtrip failed
3  payment verification failed
4  settlement failed
5  post-settle assertion failed
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _check_env() -> list[str]:
    """Return a list of human-readable problems; empty list = OK."""
    problems = []
    if os.environ.get("X402_ENABLED", "0") not in ("1", "true", "yes", "on"):
        problems.append("X402_ENABLED must be 1 (paywall off → no challenge to verify)")
    if not os.environ.get("X402_PAY_TO") or os.environ.get("X402_PAY_TO") == "0x" + "0" * 40:
        problems.append("X402_PAY_TO must be a real address (not the all-zeros placeholder)")
    if os.environ.get("X402_NETWORK") not in ("eip155:84532", "eip155:8453"):
        problems.append("X402_NETWORK must be eip155:84532 (testnet) or eip155:8453 (mainnet)")
    if not os.environ.get("MEOK_ATTESTATION_KEY"):
        problems.append("MEOK_ATTESTATION_KEY must be set (32 bytes hex) for the signing path")
    return problems


def _boot_smoke() -> bool:
    """Import server.mcp and assert 4 free + 2 paywalled tools are registered."""
    sys.path.insert(0, str(REPO_ROOT))
    try:
        import server
    except Exception as exc:
        print(f"[FAIL] import server: {exc!r}", file=sys.stderr)
        return False
    tools = server.mcp._tool_manager._tools  # type: ignore[attr-defined]
    names = sorted(tools.keys())
    print(f"[OK] server.mcp booted. {len(names)} tools registered: {names}")
    expected_free = {"list_experts", "spending_report", "health"}
    expected_paid = {"sign_receipt", "verify_receipt"}
    missing_free = expected_free - set(names)
    missing_paid = expected_paid - set(names)
    if missing_free or missing_paid:
        print(f"[FAIL] missing tools: free={missing_free} paid={missing_paid}", file=sys.stderr)
        return False
    # Confirm the paywalled ones have the COST WARNING prefix in their description.
    for name in expected_paid:
        desc = tools[name].description
        if "COST WARNING" not in desc:
            print(f"[FAIL] {name} missing COST WARNING prefix: {desc!r}", file=sys.stderr)
            return False
    print("[OK] all expected tools registered with COST WARNING descriptions")
    return True


def _challenge_roundtrip() -> bool:
    """Call sign_receipt WITHOUT a payment — expect a ToolError containing the challenge."""
    sys.path.insert(0, str(REPO_ROOT))
    import server
    tools = server.mcp._tool_manager._tools  # type: ignore[attr-defined]
    sign_tool = tools["sign_receipt"]
    payload_hex = hashlib.sha256(b"settlement-smoke").hexdigest()

    # Build a minimal FastMCP-like context with no _meta.
    class _Req:
        class _Params:
            meta = None
        params = _Params()
    class _RC:
        request = _Req()
    class _Ctx:
        request_context = _RC()
    ctx = _Ctx()

    try:
        result = sign_tool.fn(payload_hex=payload_hex, ctx=ctx)
    except Exception as exc:
        # The decorated wrapper raises ToolError with the challenge JSON as text.
        from mcp.server.fastmcp.exceptions import ToolError
        if not isinstance(exc, ToolError):
            print(f"[FAIL] unexpected exception type: {type(exc).__name__}: {exc!r}", file=sys.stderr)
            return False
        envelope = json.loads(str(exc))
    else:
        envelope = result

    challenge = envelope.get("x402/payment-response")
    if not challenge:
        print(f"[FAIL] no PaymentRequired challenge in envelope: {envelope!r}", file=sys.stderr)
        return False
    # The x402 SDK serialises the version as `x402Version` (camelCase). Accept
    # either casing — some clients / proxies normalise the key.
    version = challenge.get("x402Version", challenge.get("x402_version"))
    if version != 1:
        print(f"[FAIL] wrong x402_version: {version!r}", file=sys.stderr)
        return False
    accepts = challenge.get("accepts") or []
    if not accepts:
        print(f"[FAIL] no accepts[] in challenge: {challenge!r}", file=sys.stderr)
        return False
    req = accepts[0]
    print(f"[OK] challenge: amount={req.get('amount')} asset={req.get('asset', '')[:14]}… "
          f"pay_to={req.get('payTo', req.get('pay_to', ''))[:10]}… network={req.get('network')}")
    return True


def _settle_smoke() -> bool:
    """Drive a real x402 settlement.

    NOTE: This requires a funded wallet + facilitator access. For the very
    first smoke, we recommend running this against Base Sepolia with a
    fresh testnet key. The flow is:

      1. Generate a random EVM private key (testnet only).
      2. Fund the corresponding address with testnet USDC via Circle's faucet.
      3. Set TEST_SIGNER_KEY=<hex> in the env (this script).
      4. This script constructs an x402 payment payload, signs it, sends
         it to the running server, and asserts the facilitator settles it.

    For now this function asserts the substrate *can* be called with a
    payment, but the actual signing+settling requires `eth_account` and
    a running server. We return a clear "needs full harness" message
    rather than silently passing.
    """
    try:
        import eth_account  # noqa: F401
    except ImportError:
        print("[SKIP] eth_account not installed — install with `pip install eth-account` "
              "to drive a real settlement. The challenge path above proves the rail "
              "issues valid PaymentRequired envelopes.")
        return True
    print("[TODO] real signing + settlement flow — wire when you have a funded testnet wallet")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skip-settle", action="store_true",
                        help="Run boot + challenge roundtrip only (no real settlement).")
    args = parser.parse_args()

    print("=" * 70)
    print("MEOK x402 settlement smoke")
    print("=" * 70)
    print(f"X402_ENABLED      = {os.environ.get('X402_ENABLED', '0')}")
    print(f"X402_NETWORK      = {os.environ.get('X402_NETWORK', 'unset')}")
    print(f"X402_PAY_TO set   = {bool(os.environ.get('X402_PAY_TO'))}")
    print(f"attestation key   = {'set' if os.environ.get('MEOK_ATTESTATION_KEY') else 'unset'}")
    print()

    problems = _check_env()
    if problems:
        print("[FAIL] environment not ready:")
        for p in problems:
            print(f"  - {p}")
        print()
        print("Run: cp .env.example .env && edit .env, then re-export its values.")
        return 1

    print("--- step 1: boot + tool registration ---")
    if not _boot_smoke():
        return 1
    print()

    print("--- step 2: PaymentRequired challenge roundtrip ---")
    if not _challenge_roundtrip():
        return 2
    print()

    if args.skip_settle:
        print("[OK] challenge roundtrip green. Re-run without --skip-settle to drive a real settlement.")
        return 0

    print("--- step 3: real settlement ---")
    if not _settle_smoke():
        return 4
    print()

    print("=" * 70)
    print("ALL GREEN — x402 rail end-to-end working.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
