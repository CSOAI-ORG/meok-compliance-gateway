"""Property/fuzz tests for meok_x402's pure parsing surface (Fuzzing scorecard check).

    pip install x402 hypothesis pytest && pytest tests/test_x402_properties.py

The gateway's own untrusted-input parsers are the x402 helpers (price strings from
env/decorator args, tool names interpolated into challenge JSON) — the JSON-RPC
dispatcher itself lives in the mcp SDK and is fuzzed upstream. Like test_x402.py,
this is wallet-free and chain-free: only the deterministic paths are exercised.
Hypothesis runs derandomized so CI failures reproduce exactly.
"""
import json
import os
import sys
from decimal import Decimal

from hypothesis import given, settings, strategies as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

settings.register_profile("ci", deadline=None, derandomize=True, max_examples=200)
settings.load_profile("ci")


def _enable():
    os.environ.update(
        X402_ENABLED="1",
        X402_PAY_TO="0x000000000000000000000000000000000000dEaD",
        X402_NETWORK="eip155:8453",
    )
    import importlib
    import meok_x402
    importlib.reload(meok_x402)
    return meok_x402


# ── _price_to_atomic ──────────────────────────────────────────────────────────────


@given(
    dollars=st.decimals(min_value="0", max_value="100000", places=6, allow_nan=False, allow_infinity=False),
    prefix=st.sampled_from(["", "$"]),
    pad=st.sampled_from(["", " ", "  "]),
)
def test_price_to_atomic_matches_decimal_math(dollars, prefix, pad):
    m = _enable()
    atomic = m._price_to_atomic(f"{pad}{prefix}{dollars}{pad}")
    expected = int(round(float(dollars) * 10**6))  # mirrors the float path in production
    assert atomic == str(expected)
    assert Decimal(atomic) >= 0


@given(garbage=st.text(max_size=40))
def test_price_to_atomic_garbage_raises_only_valueerror(garbage):
    m = _enable()
    try:
        out = m._price_to_atomic(garbage)
    except ValueError as exc:
        # the contract: a clean, actionable error — never a TypeError/AttributeError
        assert "price" in str(exc).lower()
    else:
        # if it parsed, it must have been a real number (possibly $-prefixed)
        float(garbage.strip().lstrip("$"))
        assert out.lstrip("-").isdigit()


# ── enabled() ─────────────────────────────────────────────────────────────────────


# env values cannot contain NUL or lone surrogates (OS/UTF-8 contract —
# os.environ raises before our code runs)
_env_text = st.text(
    alphabet=st.characters(exclude_characters="\x00", exclude_categories=("Cs",)),
    max_size=20,
)


@given(raw=_env_text)
def test_enabled_truthy_set_is_exact(raw):
    os.environ["X402_ENABLED"] = raw
    import importlib
    import meok_x402
    importlib.reload(meok_x402)
    assert meok_x402.enabled() is (raw.strip().lower() in ("1", "true", "yes", "on"))


# ── build_challenge ───────────────────────────────────────────────────────────────


@given(tool_name=st.text(min_size=1, max_size=80))
def test_challenge_is_wire_safe_for_any_tool_name(tool_name):
    m = _enable()
    ch = m.build_challenge(tool_name, "$0.10")
    # must always survive the wire: round-trips through JSON, keeps the contract
    rt = json.loads(json.dumps(ch))
    assert rt["x402Version"] == 1
    assert rt["resource"]["url"] == f"mcp://tool/{tool_name}"
    assert rt["accepts"][0]["amount"] == "100000"


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
