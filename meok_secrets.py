"""
meok_secrets.py — Reference implementation of CRITICAL Fix #2 from the
76-server MCP master audit (sov3_mcp_master_audit.md, 2026-06-08).

Problem (audit, CRITICAL #2):
    API keys stored at ~/.meok/api_keys.json with no permission restrictions.
    World-readable on macOS / Linux by default. Any local user (or compromised
    subprocess) can read all 76 MCP servers' API keys, including the
    MEOK_ATTESTATION_KEY (Fix #3) and any cloud-provider keys.

Solution:
    1. Try the OS keyring first (macOS Keychain / Linux Secret Service /
       Windows Credential Manager). Cross-platform via the `keyring` PyPI
       package, but we lazy-import so this module is stdlib-only at minimum.
    2. Fall back to a file at ~/.meok/<name>.key, but ONLY if it is
       mode 600 (or 400). If the file is world/group-readable, raise
       PermissionError — never silently read it.
    3. The first time a key is written, ensure the directory exists and
       chmod 600 the file. Never write a key to a pre-existing file
       that has wrong perms (security hole to relax them).

This module is dependency-free at the stdlib level. If `keyring` is
installed (recommended), it uses it. If not, it falls back to the file
with strict perms.

Usage in a flagship:
    from meok_secrets import get_secret, set_secret

    api_key = get_secret("openai")          # reads from keyring or ~/.meok/openai.key
    set_secret("openai", "sk-...")          # writes to keyring or ~/.meok/openai.key
"""
from __future__ import annotations

import logging
import os
import stat
from pathlib import Path
from typing import Optional

log = logging.getLogger("meok.secrets")

# Keyring service name — all MEOK secrets are namespaced under this.
# The keyring user is the secret name (e.g. "openai", "anthropic",
# "mcp-registry-token", etc.).
_KEYRING_SERVICE = "meok.ai"

# Fallback directory for file-based storage when keyring is unavailable.
# Overridable via MEOK_SECRETS_DIR for testing.
_SECRETS_DIR = Path(
    os.environ.get("MEOK_SECRETS_DIR", os.path.expanduser("~/.meok"))
).resolve()


def _keyring_get(name: str) -> Optional[str]:
    """Read from OS keyring. Returns None if not installed or no value."""
    try:
        import keyring  # type: ignore
        return keyring.get_password(_KEYRING_SERVICE, name)
    except ImportError:
        return None
    except Exception as exc:  # noqa: BLE001
        log.debug("keyring get failed for %r (will try file): %r", name, exc)
        return None


def _keyring_set(name: str, value: str) -> bool:
    """Write to OS keyring. Returns True on success."""
    try:
        import keyring  # type: ignore
        keyring.set_password(_KEYRING_SERVICE, name, value)
        return True
    except ImportError:
        return False
    except Exception as exc:  # noqa: BLE001
        log.debug("keyring set failed for %r: %r", name, exc)
        return False


def _file_path(name: str) -> Path:
    """Path to the fallback file for a given secret name."""
    return _SECRETS_DIR / f"{name}.key"


def _file_get(name: str) -> Optional[str]:
    """Read from a mode-600 file. Returns None if file absent.

    Raises PermissionError if file exists but has group/other read bits set.
    Never silently reads a world/group-readable file — that defeats the audit fix.
    """
    path = _file_path(name)
    if not path.exists():
        return None
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        raise PermissionError(
            f"{path} is readable by group/other (mode={oct(mode)}). "
            f"Per CRITICAL #2 from the 2026-06-08 MCP master audit, this is "
            f"a security violation. Fix with: chmod 600 {path}"
        )
    return path.read_text(encoding="utf-8").strip()


def _file_set(name: str, value: str) -> Path:
    """Write a secret to a mode-600 file. Creates the directory if needed.

    Returns the path. Will refuse to overwrite an existing file that has
    wrong perms (don't relax perms; require the operator to fix it).
    """
    path = _file_path(name)
    if path.exists():
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode & 0o077:
            raise PermissionError(
                f"{path} exists with mode={oct(mode)} (group/other readable). "
                f"Refusing to overwrite — fix with: chmod 600 {path}"
            )
    _SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    # Write atomically: write to tmp, then rename + chmod.
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(value, encoding="utf-8")
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)
    # Ensure perms are 600 even if the file already existed (defense in depth).
    os.chmod(path, 0o600)
    return path


def get_secret(name: str) -> Optional[str]:
    """Read a secret by name. Order: keyring → file.

    Returns None if the secret is not found anywhere.
    Raises PermissionError if the file fallback exists with wrong perms.
    """
    val = _keyring_get(name)
    if val is not None:
        return val
    return _file_get(name)


def set_secret(name: str, value: str) -> str:
    """Write a secret by name. Order: keyring → file (with chmod 600).

    Returns a human-readable description of where the secret was stored
    ("keyring" or the file path).
    """
    if _keyring_set(name, value):
        return "keyring"
    path = _file_set(name, value)
    return str(path)


def audit_permissions() -> list[str]:
    """Check the secrets dir + every file in it. Returns a list of warnings.

    Used by CI / health checks. Example output:
        ['~/.meok/ is mode=0o755 (expected 0o700)',
         '~/.meok/openai.key is mode=0o644 (expected 0o600)']
    """
    warnings: list[str] = []
    if not _SECRETS_DIR.exists():
        return warnings
    dir_mode = stat.S_IMODE(_SECRETS_DIR.stat().st_mode)
    if dir_mode & 0o077:
        warnings.append(
            f"{_SECRETS_DIR} is mode={oct(dir_mode)} (expected 0o700 — "
            f"group/other must not be able to list secrets)"
        )
    for path in sorted(_SECRETS_DIR.glob("*.key")):
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode & 0o077:
            warnings.append(
                f"{path} is mode={oct(mode)} (expected 0o600)"
            )
    return warnings


__all__ = [
    "get_secret",
    "set_secret",
    "audit_permissions",
    "MEOK_SECRETS_DIR",  # re-exported for tests
]
