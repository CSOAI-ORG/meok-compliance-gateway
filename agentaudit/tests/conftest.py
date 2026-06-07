"""Pytest fixtures for AgentAudit.

Hermeticity rules (per repo AGENTS.md):
  1. Never touch `~/.meok/` — live usage counters + PAYG balances. Tests run under a
     temp HOME so the production daemons on this machine are not charged.
  2. X402_ENABLED stays UNSET by default (transparent passthrough). The `x402_enabled`
     fixture flips it on for the paywire tests; the `x402_disabled` fixture flips it
     back off (and reimports x402.py so `enabled()` re-evaluates).
"""
from __future__ import annotations

import importlib
import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _hermetic_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Run every test under a temp HOME so ~/.meok/ (live counters) is never read or written."""
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / ".config"))
    # Belt-and-braces: ensure no X402 env sneaks in from the host shell.
    for k in ("X402_ENABLED", "X402_PAY_TO", "X402_NETWORK", "X402_PRICE",
              "X402_ASSET", "X402_FACILITATOR_URL"):
        monkeypatch.delenv(k, raising=False)


@pytest.fixture
def x402_enabled(monkeypatch: pytest.MonkeyPatch):
    """Enable the x402 paywire for the duration of a test.

    Reimports agentaudit.x402 so the module-level `enabled()` check sees X402_ENABLED=1.
    Yields the (reloaded) x402 module so the test can assert on its symbols.
    """
    monkeypatch.setenv("X402_ENABLED", "1")
    monkeypatch.setenv("X402_PAY_TO", "0x000000000000000000000000000000000000dEaD")
    monkeypatch.setenv("X402_NETWORK", "eip155:8453")
    from agentaudit import x402 as m
    importlib.reload(m)
    yield m
    # Tear-down: flip back to disabled and reload so the module is clean for the next test.
    monkeypatch.delenv("X402_ENABLED", raising=False)
    importlib.reload(m)


@pytest.fixture
def x402_disabled(monkeypatch: pytest.MonkeyPatch):
    """Explicitly DISABLE the paywire (clears any inherited X402_ENABLED) and reload.

    Useful for tests that want to assert the disabled passthrough even when the
    outer env has X402_ENABLED set (e.g. CI secrets, developer shells).
    """
    monkeypatch.delenv("X402_ENABLED", raising=False)
    from agentaudit import x402 as m
    importlib.reload(m)
    return m
