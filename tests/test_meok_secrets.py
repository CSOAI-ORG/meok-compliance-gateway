"""Tests for meok_secrets.py — CRITICAL Fix #2 from the 2026-06-08 MCP master audit."""
from __future__ import annotations

import os
import stat
import tempfile
from pathlib import Path
from unittest import mock

import pytest

# Import the module under test (file is at the repo root, not a package).
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "meok_secrets",
    Path(__file__).parent.parent / "meok_secrets.py",
)
meok_secrets = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(meok_secrets)


@pytest.fixture
def tmp_secrets_dir(monkeypatch, tmp_path):
    """Point MEOK_SECRETS_DIR at a fresh tmp dir for each test."""
    monkeypatch.setenv("MEOK_SECRETS_DIR", str(tmp_path))
    # Re-import the module to pick up the new env var.
    spec = importlib.util.spec_from_file_location(
        "meok_secrets_isolated",
        Path(__file__).parent.parent / "meok_secrets.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, tmp_path


def test_set_and_get_secret(tmp_secrets_dir):
    mod, tmp_path = tmp_secrets_dir
    location = mod.set_secret("test-key", "secret-value-123")
    assert "test-key.key" in location
    assert mod.get_secret("test-key") == "secret-value-123"
    # File must exist with mode 600
    f = tmp_path / "test-key.key"
    assert f.exists()
    mode = stat.S_IMODE(f.stat().st_mode)
    assert mode == 0o600, f"expected mode 0o600, got {oct(mode)}"


def test_get_secret_missing_returns_none(tmp_secrets_dir):
    mod, _ = tmp_secrets_dir
    assert mod.get_secret("nonexistent") is None


def test_world_readable_file_raises(tmp_secrets_dir):
    """The whole point: a mode-644 file MUST NOT be silently read."""
    mod, tmp_path = tmp_secrets_dir
    # Write a file with intentionally wrong perms
    f = tmp_path / "leaked.key"
    f.write_text("leaked-secret")
    os.chmod(f, 0o644)
    with pytest.raises(PermissionError, match="readable by group/other"):
        mod.get_secret("leaked")


def test_set_secret_refuses_to_overwrite_bad_perms(tmp_secrets_dir, monkeypatch):
    """Don't relax perms when writing over an existing file with wrong mode.

    Backend-agnostic: if the keyring backend is functional, the file path
    is never touched (keyring succeeded). The audit-critical invariant —
    the file must NOT be written/relaxed — holds either way.
    """
    mod, tmp_path = tmp_secrets_dir
    f = tmp_path / "existing.key"
    f.write_text("old")
    os.chmod(f, 0o644)

    # Force the file path: pretend keyring is unavailable
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "keyring":
            raise ImportError("simulated no keyring")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(PermissionError, match="Refusing to overwrite"):
        mod.set_secret("existing", "new")
    # Original content preserved, perms unchanged
    assert f.read_text() == "old"
    assert stat.S_IMODE(f.stat().st_mode) == 0o644


def test_audit_permissions_clean(tmp_secrets_dir):
    mod, _ = tmp_secrets_dir
    mod.set_secret("a", "1")
    mod.set_secret("b", "2")
    assert mod.audit_permissions() == []


def test_audit_permissions_flags_wrong_mode(tmp_secrets_dir):
    mod, tmp_path = tmp_secrets_dir
    f = tmp_path / "bad.key"
    f.write_text("x")
    os.chmod(f, 0o644)
    warnings = mod.audit_permissions()
    assert len(warnings) == 1
    assert "mode=0o644" in warnings[0]
    assert "expected 0o600" in warnings[0]


def test_audit_permissions_flags_wrong_dir_mode(tmp_secrets_dir):
    mod, tmp_path = tmp_secrets_dir
    mod.set_secret("a", "1")
    os.chmod(tmp_path, 0o755)
    warnings = mod.audit_permissions()
    assert any("expected 0o700" in w for w in warnings)


def test_keyring_fallback_when_keyring_missing(tmp_secrets_dir, monkeypatch):
    """If keyring import fails, fall back to file."""
    mod, tmp_path = tmp_secrets_dir

    # Force the keyring import to fail
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "keyring":
            raise ImportError("simulated keyring not installed")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    location = mod.set_secret("nokeyring", "value")
    assert "nokeyring.key" in location
    assert mod.get_secret("nokeyring") == "value"
