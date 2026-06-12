# Dockerfile Security Template — for the 75 MEOK flagship MCP servers

> **Source**: sov3_mcp_master_audit.docx (2026-06-08), CRITICAL #1: "All 76 Docker containers run as root."
> **Keystone status**: ✅ Already fixed (`Dockerfile:20-21`, `USER app` with `uid 10001`).
> **Audit remediation scope**: ~75 flagship Dockerfiles that need the same change.
> **Estimated effort**: 1 line per Dockerfile × 75 = ~30 min mechanical.
> **Owner**: per-flagship PR, batched in fleet rollout week (post-OpenSSF work).

This file is the **template + CI check** for the fleet rollout. Copy the `USER` block
into every flagship's Dockerfile and add the CI check to `build-push.yml` (or
`test-gateway.yml` for the keystone).

---

## 1. The pattern (3 lines)

After `pip install`, before `CMD`, add:

```dockerfile
# CRITICAL #1: never run as root. A successful container escape would give the
# attacker root on the host. Per the sov3 master audit, this was an across-the-board
# finding — uid 10001 + chown is the keystone's pattern.
RUN useradd --create-home --uid 10001 app && chown -R app:app /app
USER app
```

If the container needs to write to additional paths (e.g. `/var/log/meok`, `/tmp/cache`),
also add `chown -R app:app` on those paths in the same `RUN` line. Do **not** use
`USER root` anywhere else in the file — the only legitimate root usage is
`RUN` steps that install system packages.

### Why uid 10001 (and not just `app`)?

- Reproducible — bit-for-bit identical image regardless of build host's
  user namespace.
- Compatible with Kubernetes `runAsNonRoot: true` and OpenShift's
  `restricted` SCC (which require `runAsUser` to be in the allowed range).
- High enough to be outside the human-user range on most distros
  (UIDs < 1000 are usually system accounts).

### What about `cap_drop` / `cap_add`?

For MCP servers, you can drop all capabilities. None of the 76 flagship
servers need any Linux capabilities beyond the default docker default
(no caps). If a future flagship needs `NET_BIND_SERVICE` (port < 1024),
add it explicitly:

```dockerfile
# Drop all, then add back only what the process needs.
# (Most MEOK flagships don't need this — they run on high ports.)
# RUN apk add --no-cache libcap && setcap 'cap_net_bind_service=+ep' /usr/bin/python3
```

The keystone currently listens on `PORT=8000` (high port), so no caps needed.

---

## 2. The CI check (copy into `test-gateway.yml` or a new `docker-security.yml`)

```yaml
name: docker-security

on:
  pull_request:
    paths:
      - "Dockerfile"
      - ".github/workflows/test-gateway.yml"

jobs:
  no-root:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build the image
        run: docker build -t meok-test .

      # The audit's CRITICAL #1: must NOT be root. uid=0 would mean a container
      # escape gives the attacker root on the host.
      - name: Verify non-root user
        run: |
          USER_LINE=$(docker run --rm meok-test id -u)
          if [ "$USER_LINE" = "0" ]; then
            echo "::error::Container is running as root (uid=0). Add 'RUN useradd --create-home --uid 10001 app && chown -R app:app /app && USER app' to the Dockerfile."
            exit 1
          fi
          echo "OK — running as uid=$USER_LINE"
```

This runs in ~30s on a PR that touches a Dockerfile. Costs are minimal
because the build context is small (a `requirements.txt` + `server.py`).

---

## 3. Per-flagship checklist (when adopting this template)

- [ ] Dockerfile: add the `RUN useradd ... && USER app` block
- [ ] Any `RUN mkdir /some/path` — add `&& chown app:app /some/path` (or
      do all the chowns in the existing `useradd` line)
- [ ] Any `ENTRYPOINT` or `CMD` referencing a script — make sure the
      script is readable by `app` (chmod 755) and the data files it
      reads are 644
- [ ] Verify: `docker run <image> id` shows `uid=10001(app)`
- [ ] Verify: the flagship's `tests/` still pass when run inside the
      container (some test fixtures write to /tmp or /var — make sure
      those are world-writable or pre-chowned)
- [ ] Add the `no-root` job to the flagship's `test-gateway.yml`

---

## 4. Out of scope (deferred)

- **Distroless base images** (gcr.io/distroless/python3) — would be a nice
  Stage-8 hardening but breaks the `pip install` workflow that the
  75 flagships rely on. Track in a future remediation wave.
- **Read-only root filesystem** (`securityContext.readOnlyRootFilesystem:
  true` in k8s) — would require moving all writes to mounted volumes
  (e.g. `EmptyDir` for `/tmp`). Big UX change, defer to a follow-up.
- **AppArmor / SELinux profiles** — only relevant for production k8s
  deployments, not for the per-PR CI check.

---

## 5. Cross-references

- `CRITICAL_FIXES_2026-06-08.md` — Fix #1, with the full fleet rollout plan
- `keystone_SECREVIEW.md` — the keystone's OpenSSF audit, Packaging (8/10) section
- `meok-compliance-gateway/Dockerfile:20-21` — the keystone's reference impl
- `sov3_mcp_master_audit.docx` (local-only) — CRITICAL #1 source finding
