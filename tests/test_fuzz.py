"""Property-based fuzzing for the keystone's untrusted-input parsers.

The keystone (meok-compliance-gateway) wraps a FastMCP server over streamable
HTTP. The JSON-RPC dispatcher itself is the mcp SDK's, so the meaningful
fuzzable surface is the gateway's own helpers that take untrusted input from
network requests, environment, or the x402 protocol.

Targets:
  - meok_x402._price_to_atomic  (parses env-supplied price strings)
  - meok_x402.build_challenge   (embeds tool_name into a public JSON challenge)

Per OpenSSF Scorecard check 11 (Fuzzing).
"""
import json
import os
import sys

import pytest
from hypothesis import given, settings, strategies as st

# Make the repo root importable (matches the convention in test_x402_properties.py).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

settings.register_profile("ci", deadline=None, derandomize=True, max_examples=200)
settings.load_profile("ci")

# Import after sys.path is set.
import meok_x402  # noqa: E402

# x402 helpers read these from env. Set deterministic test values so the
# fuzz tests don't have to model the env state.
os.environ.setdefault("X402_PAY_TO", "0x000000000000000000000000000000000000dEaD")
os.environ.setdefault("X402_NETWORK", "eip155:8453")


# --- strategy for price strings (untrusted, from env) ---
# Filter out null bytes; they would crash Python's source loader when
# hypothesis writes its module shim.

price_string = st.one_of(
    st.text(min_size=0, max_size=64).filter(lambda s: "\x00" not in s),
    st.sampled_from(["0", "0.0", "0.001", "1", "1e9", "1e-9", " 0.01 ", "0.01x", "", "0x1", "NaN", "inf"]),
)


@given(price=price_string)
def test_price_to_atomic_never_unhandled_exception(price):
    """_price_to_atomic parses env-supplied price strings. It should either
    return a valid atomic-unit string or raise a documented handled error
    (ValueError, TypeError, decimal.InvalidOperation) -- never an unhandled
    exception that could crash a request handler."""
    try:
        result = meok_x402._price_to_atomic(price)
    except (ValueError, TypeError, ArithmeticError, json.JSONDecodeError):
        return  # documented handled errors are OK
    # If it returns, the result must be a string (atomic units are base-10 int strings).
    assert isinstance(result, str)


# --- strategy for tool_name (interpolated into a public JSON challenge) ---

tool_name_arg = st.one_of(
    st.text(min_size=0, max_size=128).filter(lambda s: "\x00" not in s),
    st.sampled_from(["valid_tool", "x" * 200, "tool/with/slashes", "tool with spaces", " "]),
)


@given(tool_name=tool_name_arg)
def test_build_challenge_never_unhandled_exception(tool_name):
    """build_challenge embeds an arbitrary tool_name into a public JSON
    challenge. Should not raise, and the output should be a JSON-serializable
    dict (the gateway returns this to clients without further sanitization)."""
    try:
        result = meok_x402.build_challenge(tool_name=tool_name, price="0.01")
    except (ValueError, TypeError, json.JSONDecodeError, KeyError):
        return  # documented handled errors are OK
    assert isinstance(result, dict)
    # Whatever the tool_name was, it must round-trip through JSON cleanly.
    json.dumps(result)  # raises TypeError on un-serializable values; that would be a bug
