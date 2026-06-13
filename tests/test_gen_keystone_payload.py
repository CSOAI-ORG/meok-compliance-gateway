"""Tests for scripts/gen-keystone-payload.py — keeps the marketplace listings
in sync with the keystone's tool surface. If the listings fall out of sync,
the marketplace advertises a tool surface that doesn't match what the
keystone actually serves — agents reading the Glama/Smithery listing see
sign_receipt/verify_receipt at $0.05, hit the gateway, and find something
else. CI runs `python3 scripts/gen-keystone-payload.py --check` and fails
if the diff is non-empty.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


def _run(*args, env=None) -> subprocess.CompletedProcess:
    """Run scripts/gen-keystone-payload.py with the given args, in the
    repo root, with the given env (or default to the test env)."""
    return subprocess.run(
        [sys.executable, "scripts/gen-keystone-payload.py", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, **(env or {})},
    )


def test_check_passes_when_listings_are_fresh():
    """The committed listings are regenerated from server.py in CI; if
    the regen matches, --check exits 0. Pre-condition: the test runs
    after a fresh `gen-keystone-payload.py`, so the listings are in sync."""
    cp = _run("--check")
    assert cp.returncode == 0, f"--check failed: stdout={cp.stdout!r} stderr={cp.stderr!r}"
    assert "OK" in cp.stdout, f"unexpected stdout: {cp.stdout!r}"


def test_check_detects_stale_glama_json(tmp_path, monkeypatch):
    """If a tool is added to the keystone's TOOLS list in
    gen-keystone-payload.py but the generator is not re-run, --check
    should detect the staleness and exit non-zero with a helpful message.
    The test creates a temporary committed-listing directory containing
    a stale glama.json (a ghost tool that's not in TOOLS), then runs
    --check against it. This works on fresh checkouts because we don't
    depend on the real dist/ existing."""
    import shutil
    # Build a temp "committed" listing with a stale glama.json
    fake_committed = tmp_path / "fake_dist"
    fake_committed.mkdir()
    # Generate fresh listings into a sibling dir, then mutate glama.json
    fresh = tmp_path / "fresh"
    fresh.mkdir()
    _run("--out", str(fresh))
    shutil.copy(str(fresh / "glama.json"), str(fake_committed / "glama.json"))
    for f in ("smithery.yaml", "mcpso.json", "pulse.md", "x402-bazaar-discovery.json"):
        shutil.copy(str(fresh / f), str(fake_committed / f))
    # Now add a ghost tool to the committed glama.json
    payload = json.loads((fake_committed / "glama.json").read_text())
    payload["tools"].append({
        "name": "ghost_tool",
        "description": "Does not exist on the real keystone",
        "paywall": False,
        "price": None,
    })
    (fake_committed / "glama.json").write_text(json.dumps(payload, indent=2) + "\n")
    # Point --check at this fake committed dir
    cp = _run("--check", "--out", str(fake_committed))
    # --check regenerates into a tempdir and compares against the
    # fake_committed dir. The ghost tool diff will trip the check.
    assert cp.returncode != 0, f"--check should have detected the stale listing: stdout={cp.stdout!r}"
    assert "out of date" in cp.stdout or "stale" in cp.stdout.lower() or "regenerate" in cp.stdout.lower(), \
        f"unhelpful error message: {cp.stdout!r}"
    assert "glama.json" in cp.stdout, f"should name the differing file: {cp.stdout!r}"


def test_check_passes_cleanly_when_dist_missing(tmp_path, monkeypatch):
    """If dist/keystone-listing/ doesn't exist (fresh CI checkout, fresh
    contributor clone), --check should pass with a clear "regenerate"
    message rather than failing. The contributor will run the generator
    and commit the output; --check on the next push will then verify."""
    # Move the listing aside
    listing_dir = REPO_ROOT / "dist" / "keystone-listing"
    backup = tmp_path / "keystone-listing-backup"
    if listing_dir.exists():
        import shutil
        shutil.move(str(listing_dir), str(backup))
    try:
        cp = _run("--check")
        assert cp.returncode == 0, f"--check should pass on fresh checkout: stdout={cp.stdout!r} stderr={cp.stderr!r}"
        assert "not present" in cp.stdout or "fresh" in cp.stdout.lower(), \
            f"unhelpful fresh-checkout message: {cp.stdout!r}"
    finally:
        if backup.exists():
            import shutil
            shutil.move(str(backup), str(listing_dir))


def test_listings_contain_all_keystone_tools(tmp_path):
    """Sanity check: the glama.json listing has an entry for every tool
    the keystone registers. We regenerate into tmp_path rather than
    reading the committed dist/, so the test works on fresh checkouts
    (where dist/ is gitignored)."""
    # Generate into a temp dir
    out = tmp_path / "out"
    out.mkdir()
    cp = _run("--out", str(out))
    assert cp.returncode == 0, f"gen failed: {cp.stderr!r}"
    import importlib.util
    spec = importlib.util.spec_from_file_location("server", REPO_ROOT / "server.py")
    server = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(server)
    keystone_tools = set(server.mcp._tool_manager._tools.keys())
    glama = json.loads((out / "glama.json").read_text())
    listed_tools = {t["name"] for t in glama["tools"]}
    assert keystone_tools == listed_tools, \
        f"keystone={keystone_tools - listed_tools} not in listing; listing={listed_tools - keystone_tools} extra"


def test_listing_uses_camelCase_for_x402_bazaar(tmp_path):
    """The x402-bazaar-discovery.json uses network=`eip155:8453` (Base
    mainnet). Per x402 Bazaar's wire spec, `network` is required and
    `service_name` is human-readable. Generate into tmp_path so the test
    works on fresh checkouts where dist/ is absent."""
    out = tmp_path / "out"
    out.mkdir()
    cp = _run("--out", str(out))
    assert cp.returncode == 0
    payload = json.loads((out / "x402-bazaar-discovery.json").read_text())
    assert "network" in payload
    assert payload["network"] == "eip155:8453"
    assert "service_name" in payload
    assert "MEOK" in payload["service_name"]


def test_smithery_lists_5_tools(tmp_path):
    """Smithery's listing should match the keystone surface exactly —
    a tool listed but not implemented (or vice versa) is a buyer-pact
    violation. Generate into tmp_path so the test works on fresh
    checkouts where dist/ is absent."""
    out = tmp_path / "out"
    out.mkdir()
    cp = _run("--out", str(out))
    assert cp.returncode == 0
    import yaml
    payload = yaml.safe_load((out / "smithery.yaml").read_text())
    tools = {t["name"] for t in payload["tools"]}
    expected = {"health", "list_experts", "spending_report", "audit_anchor", "sign_receipt", "verify_receipt"}
    assert tools == expected, f"smithery tools mismatch: extra={tools - expected} missing={expected - tools}"
