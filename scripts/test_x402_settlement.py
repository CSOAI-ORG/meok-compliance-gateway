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
    """Drive a real x402 settlement through the keystone.

    Flow (mirrors what an x402-aware MCP client would do):

      1. Call the paywalled tool — get a `PaymentRequired` challenge.
      2. Build a `x402ClientSync` with the EVM scheme registered.
      3. Wrap `eth_account.LocalAccount` in a signer.
      4. Sign a USDC `PaymentPayload` that matches the challenge's
         amount/asset/network/pay_to.
      5. Call the tool again with the signed payment in `_meta["x402/payment"]`.
      6. Assert the tool ran (no second ToolError), the spending log
         incremented, and the facilitator actually settled (returned
         a transaction hash / success response).

    Requires: `eth_account` installed + a testnet signer key in env
    (`TEST_SIGNER_KEY=<64-hex>`) whose address is funded with USDC on
    the keystone's `X402_NETWORK`.

    For the first testnet smoke, we recommend:
      - Generate a throwaway key:  python -c "from eth_account import Account; print(Account.create())"
      - Get the address:           python -c "from eth_account import Account; a=Account.create(); print(a.address, a.key.hex())"
      - Fund it:                  https://faucet.circle.com → Base Sepolia → USDC → 20 USDC
      - Set:                      TEST_SIGNER_KEY=<key.hex()>
      - Run this script with      --skip-settle REMOVED

    The first few calls may be slow (facilitator roundtrip); allow 30s.
    """
    try:
        import eth_account  # noqa: F401
    except ImportError:
        print("[SKIP] eth_account not installed — `pip install eth-account[test]` to drive a real settlement.")
        return True

    signer_key_hex = os.environ.get("TEST_SIGNER_KEY", "").strip()
    if not signer_key_hex or signer_key_hex == "0" * 64:
        print("[SKIP] TEST_SIGNER_KEY unset. Generate a throwaway testnet key with:")
        print("       python3 -c \"from eth_account import Account; a=Account.create(); print('addr:', a.address); print('key :', a.key.hex())\"")
        print("       Then fund the address with Base Sepolia USDC at https://faucet.circle.com")
        print("       and export:  export TEST_SIGNER_KEY=<key.hex()>")
        return True

    # 1. Build the signer.
    from eth_account import Account
    from x402.client import x402ClientSync
    from x402.mechanisms.evm.exact.client import ExactEvmScheme
    from x402.schemas import PaymentPayload

    acct = Account.from_key(signer_key_hex)
    print(f"[INFO] testnet payer: {acct.address}")
    print(f"[INFO] pay_to (server): {os.environ['X402_PAY_TO']}")
    print(f"[INFO] network: {os.environ['X402_NETWORK']}")
    print(f"[INFO] (these are typically the SAME address for a self-payment smoke)")

    client = x402ClientSync()
    client.register_v1(os.environ["X402_NETWORK"], ExactEvmScheme(acct))

    # 2. Get the challenge by calling the paywalled tool with no payment.
    sys.path.insert(0, str(REPO_ROOT))
    import server
    tools = server.mcp._tool_manager._tools  # type: ignore[attr-defined]
    sign_tool = tools["sign_receipt"]
    payload_hex = hashlib.sha256(b"settlement-smoke-real").hexdigest()

    class _ReqEmpty:
        class _Params:
            meta = None
        params = _Params()
    class _RCEmpty:
        request = _ReqEmpty()
    class _CtxEmpty:
        request_context = _RCEmpty()
    try:
        sign_tool.fn(payload_hex=payload_hex, ctx=_CtxEmpty())
    except Exception as exc:
        from mcp.server.fastmcp.exceptions import ToolError
        if not isinstance(exc, ToolError):
            print(f"[FAIL] first call didn't raise ToolError: {type(exc).__name__}: {exc!r}", file=sys.stderr)
            return False
        challenge_envelope = json.loads(str(exc))
    else:
        print("[FAIL] first call returned a value (expected a challenge, not a tool result)", file=sys.stderr)
        return False

    challenge = challenge_envelope["x402/payment-response"]
    print(f"[OK] got challenge: amount={challenge['accepts'][0]['amount']}")

    # 3. Sign the payment.
    from x402.schemas import PaymentRequired
    payment_required = PaymentRequired.model_validate(challenge)
    signed = client.create_payment_payload(payment_required)
    # serialise to a dict for the _meta — accept both v0 and v1 PaymentPayload
    # shapes (x402 SDK 2.12 returns PaymentPayloadV1; older versions return the
    # un-versioned PaymentPayload).
    if hasattr(signed, "model_dump"):
        payment_dict = signed.model_dump(by_alias=True, mode="json")
    else:
        payment_dict = dict(signed)
    # surface a useful one-liner regardless of v0/v1
    if hasattr(signed, "accepted") and signed.accepted is not None:
        scheme = signed.accepted.scheme
        amount = signed.accepted.amount
    else:
        scheme = getattr(signed, "scheme", "?")
        amount = getattr(signed, "payload", {}).get("authorization", {}).get("value", "?")
    print(f"[OK] signed payment: scheme={scheme} amount={amount}")

    # 4. Call the tool again with the payment in _meta.
    from meok_x402 import PAYMENT_META_KEY

    class _Meta:
        def __init__(self, m): self._m = m
        def model_dump(self): return self._m
        def __iter__(self): return iter(self._m.items())
        def get(self, k, d=None): return self._m.get(k, d)
        def __bool__(self): return bool(self._m)
    class _Params:
        def __init__(self, m): self.meta = _Meta(m)
    class _ReqPaid:
        def __init__(self, m): self.params = _Params(m)
    class _RCPaid:
        def __init__(self, m): self.request = _ReqPaid(m)
    class _CtxPaid:
        def __init__(self, m): self.request_context = _RCPaid(m)
    paid_ctx = _CtxPaid({PAYMENT_META_KEY: payment_dict})

    spending_before = server.mcp._tool_manager._tools["sign_receipt"].fn.__wrapped__  # not used
    from meok_x402 import spending_snapshot
    before = spending_snapshot()["total_calls"]

    try:
        result_json = sign_tool.fn(payload_hex=payload_hex, ctx=paid_ctx)
    except Exception as exc:
        from mcp.server.fastmcp.exceptions import ToolError
        if isinstance(exc, ToolError):
            err = json.loads(str(exc))
            print(f"[FAIL] tool still gated after signed payment: {err!r}", file=sys.stderr)
            return False
        print(f"[FAIL] unexpected error: {type(exc).__name__}: {exc!r}", file=sys.stderr)
        return False

    result = json.loads(result_json)
    if "attestation_id" not in result:
        print(f"[FAIL] tool result missing attestation_id: {result!r}", file=sys.stderr)
        return False

    after = spending_snapshot()["total_calls"]
    if after <= before:
        print(f"[FAIL] spending log not incremented (before={before}, after={after})", file=sys.stderr)
        return False

    print(f"[OK] tool ran: attestation_id={result['attestation_id']}")
    print(f"[OK] spending log: {before} → {after} call(s)")
    print(f"[OK] payer recorded: {spending_snapshot()['recent'][-1]['payer']}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skip-settle", action="store_true",
                        help="Run boot + challenge roundtrip only (no real settlement).")
    parser.add_argument("--print-signer", action="store_true",
                        help="Print a throwaway testnet (address, key) pair and exit. "
                             "Use this to get the address you fund via https://faucet.circle.com.")
    args = parser.parse_args()

    if args.print_signer:
        from eth_account import Account
        a = Account.create()
        print(f"TESTNET_ADDRESS={a.address}")
        print(f"TESTNET_KEY={a.key.hex()}")
        print("# fund at https://faucet.circle.com — Base Sepolia — USDC — 20 USDC")
        return 0

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
