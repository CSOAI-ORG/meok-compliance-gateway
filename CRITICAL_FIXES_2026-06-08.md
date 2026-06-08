# MCP Master Audit — 3 Critical Fixes (2026-06-08)

> **Source**: `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/sov3_mcp_master_audit.md` (the 76-server master audit, ingested 2026-06-08 13:48).
> **Audit score**: C+ (56/100) fleet-wide. **Production security grade**: OpenSSF 81.6 (keystone).
> **Scope**: 76 MCP servers, 35 PyPI packages, 250+ public GitHub repos.
> **Status**: keystone already has Fix #1 (USER app in Dockerfile, line 21). Fleet-wide remediation pending.

## The 3 critical fixes (CRITICAL severity)

### Fix #1 — Drop root in Docker containers

**Issue**: All 76 Docker containers run as root. A successful container escape gives the attacker root on the host.

**Keystone status**: ✅ **Already fixed** (`Dockerfile:21` `USER app` with `uid 10001`).

**Fleet-wide action**:
- Add to every flagship's `Dockerfile` (after `pip install`, before `CMD`):
  ```dockerfile
  RUN useradd --create-home --uid 10001 app && chown -R app:app /app
  USER app
  ```
- Verify with `docker run <image> id` — must show `uid=10001(app)`.

**Affected**: ~75 flagship Dockerfiles (audit found 1 already done = keystone).
**Effort**: 1 line per Dockerfile × 75 = ~30 min mechanical.
**Owner**: fleet rollout (post-OpenSSF Scorecard work, separate session).

### Fix #2 — API key permission lockdown (CRITICAL)

**Issue**: API keys stored at `~/.meok/api_keys.json` with no permission restrictions. Per the master audit, this file is world-readable by default on macOS / Linux.

**Risk**: Any process running as the user (or any local user on a shared host) can read all 76 MCP servers' API keys, including `MEOK_ATTESTATION_KEY` (used for HMAC-SHA256 signing — Fix #3) and any cloud-provider keys.

**Action**:
- Replace file-based key storage with `keyring` (cross-platform: macOS Keychain, Linux Secret Service, Windows Credential Manager).
- Fall back to `~/.meok/api_keys.json` only when keyring is unavailable, with explicit `chmod 600` on creation.
- Add an audit step: `os.stat(path).st_mode & 0o077 == 0` before any read.
- Add a CI check: `find / -name 'api_keys.json' -not -perm 600 -delete 2>/dev/null` (aggressive, only on dev VMs).

**Code reference** (Python):
```python
import keyring
import os
import stat

KEYRING_SERVICE = "meok.ai"

def get_api_key(name: str) -> str | None:
    """Read API key from OS keyring; fallback to file with strict perms."""
    key = keyring.get_password(KEYRING_SERVICE, name)
    if key:
        return key
    fallback = os.path.expanduser(f"~/.meok/{name}.key")
    if os.path.exists(fallback):
        # Hard-fail if file is readable by group/other
        mode = os.stat(fallback).st_mode
        if mode & 0o077:
            raise PermissionError(
                f"{fallback} is world/group-readable (mode={oct(mode & 0o777)}); "
                f"fix with: chmod 600 {fallback}"
            )
        return open(fallback).read().strip()
    return None

def set_api_key(name: str, value: str) -> None:
    """Write to OS keyring; chmod 600 the fallback if used."""
    try:
        keyring.set_password(KEYRING_SERVICE, name, value)
    except keyring.errors.KeyringError:
        fallback = os.path.expanduser(f"~/.meok/{name}.key")
        os.makedirs(os.path.dirname(fallback), exist_ok=True)
        with open(fallback, "w") as f:
            f.write(value)
        os.chmod(fallback, 0o600)
```

**Affected**: every flagship that reads API keys (all 76).
**Effort**: 1-2 hours per flagship for the wrapper logic; 30 min for the CI check.
**Owner**: fleet rollout + per-flagship PR.

### Fix #3 — MEOK_ATTESTATION_KEY secret management (CRITICAL)

**Issue**: `MEOK_ATTESTATION_KEY` is the HMAC-SHA256 signing key for compliance attestations. Currently exposed via environment variables — `printenv` shows it, container introspection shows it, and any subprocess inherits it.

**Risk**: An attacker who reads `MEOK_ATTESTATION_KEY` can forge any compliance attestation. **This breaks the entire attestation chain** (differentiation #3 in `KEY_DIFFERENTIATORS.md`).

**Action**:
- Read `MEOK_ATTESTATION_KEY` only at startup from a secret manager (AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, or local `keyring`).
- Do NOT set it via `ENV` in Dockerfile.
- Do NOT log it. Add a CI check: `grep -r "MEOK_ATTESTATION_KEY" --include="*.py" --include="*.yml" --include="*.yaml" .` — any hit in a non-secret file fails the build.
- Rotate the key on a 90-day schedule (production).

**Code reference** (Python):
```python
import os
import boto3  # or google.cloud.secretmanager, or hvac

def get_attestation_key() -> bytes:
    """Read HMAC-SHA256 signing key from secret manager, never from env."""
    # 1. Try AWS Secrets Manager (production)
    try:
        client = boto3.client("secretsmanager")
        resp = client.get_secret_value(SecretId="meok/attestation-key")
        return resp["SecretString"].encode()
    except Exception:
        pass
    # 2. Try local keyring (dev)
    import keyring
    val = keyring.get_password("meok.ai", "attestation-key")
    if val:
        return val.encode()
    # 3. Hard-fail: do NOT fall back to env (per audit)
    raise RuntimeError(
        "MEOK_ATTESTATION_KEY not found in secret manager or keyring. "
        "Refusing to start to prevent attestation forgery. "
        "Run: aws secretsmanager create-secret --name meok/attestation-key "
        "--secret-string <32-bytes-base64>"
    )
```

**Affected**: every flagship that issues attestations (~30+ servers).
**Effort**: 1-2 hours per flagship + AWS Secrets Manager setup.
**Owner**: fleet rollout + cloud account (G5 in `MEOK_LAUNCH_RUNBOOK.md`).

## Other high-severity items from the audit (not blocking launch)

- **High**: HTTP for PAYG balance queries (token in URL) → enforce HTTPS, move token to headers.
- **High**: Stripe webhook secrets in plaintext → use encrypted env or secret manager.
- **High**: MCP Router = single point of failure → add health checks, circuit breakers, failover.

## Fleet rollout plan (post-OpenSSF work, separate session)

1. **Week 1 (Jun 9-13)**: Fix #1 mechanical rollout (75 lines × 30 min). Add CI check `docker run <image> id` must show non-root.
2. **Week 2 (Jun 16-20)**: Fix #2 wrapper logic per flagship. Add keyring dependency.
3. **Week 3 (Jun 23-27)**: Fix #3 secret-manager integration. Requires Nick to provision AWS Secrets Manager (G5 in launch runbook).
4. **Week 4 (Jun 30-Jul 3)**: Final audit pass. Re-score the MCP master audit. Target: B (≥75/100).

## Cross-references

- `clawd-workspace/SOV3_INTEL_DOSSIER_2026-06-08/sov3_mcp_master_audit.md` (full audit, 9,424 lines)
- `meok-compliance-gateway/KEY_DIFFERENTIATORS.md` (Differentiator #3 is the HMAC-SHA256 chain that Fix #3 protects)
- `meok-compliance-gateway/SECURITY.md` (keystone's security policy)
- `meok-compliance-gateway/Dockerfile:21` (the keystone's existing Fix #1 implementation)
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` (Phase 1-2: 73 mandatory demand waves align with these fixes)
- [[openssf-scorecard-remediation-2026-06-06]] (Phase A/B/C complete; the 3 fixes are the next round)
