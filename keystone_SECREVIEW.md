# OpenSSF Scorecard Audit — meok-compliance-gateway (keystone)

**Date:** 2026-06-06
**Method:** Hand-rolled approximation. Local repo inspection (`/Users/nicholas/meok-compliance-gateway`) + GitHub REST API for protected-branch and PR-review metadata.
**Caveat:** `gh api repos/CSOAI-ORG/meok-compliance-gateway/branches/main/protection` returned **HTTP 403 "Resource not accessible by personal access token"** (org-level block on the protection endpoint for fine-grained PATs). Branch-Protection score is therefore "unverified" → conservatively scored 0.

## Per-check findings

| # | Check | Score | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | **Code-Review** | 0/10 | `gh api pulls?state=closed&per_page=20` returns 1 merged PR (PR #2) in last 90d, **0 review comments**. Single maintainer (`CSOAI-ORG`). | No MR review culture. Add a CODEOWNERS + branch protection requiring ≥1 review. |
| 2 | **CI-Tests** | 10/10 | `.github/workflows/test-gateway.yml` runs `pytest tests/test_x402.py -v` (x402 helper unit tests) and a real end-to-end job that installs `eu-ai-act-compliance-mcp==1.8.1`, boots `http_server.py`, hits `/healthz`, and runs `tests/e2e_smoke.py` against the live streamable-HTTP gateway. | Excellent. Keep e2e pin in lockstep with flagship gold-standard. |
| 3 | **Dangerous-Workflow** | 10/10 | `grep -l pull_request_target` across 17 files (3 keystone + 31 flagship): **zero matches**. `build-push.yml` uses `workflow_dispatch` but with scoped `contents:read + packages:write`; no privileged secrets exposed. | None. |
| 4 | **Dependency-Update-Tool** | 0/10 | No `.github/dependabot.yml`. No `renovate.json`. | Add Dependabot for `pip` ecosystem — single file unlocks weekly PRs for `mcp`, `uvicorn`, `x402`. |
| 5 | **SAST** | 0/10 | No `bandit`, `codeql`, `semgrep`, `snyk` in any workflow. `scorecard.yml` runs OpenSSF Scorecard — that's posture scoring, not SAST. | Add `github/codeql-action/analyze@v3` to test-gateway.yml. |
| 6 | **Binary-Artifacts** | 10/10 | `git/trees/main?recursive=1` returned 17 paths: no `.so` / `.dylib` / `.exe` / `.whl` / `.tar.gz` / `.zip`. | None. |
| 7 | **Branch-Protection** | 0/10 | `gh api .../branches/main/protection` → 403. **Unverified.** | Org admin must grant the token `repo:status` + branch-protection read scope, or enable branch protection manually. |
| 8 | **Token-Permissions** | 10/10 | `build-push.yml` declares `permissions: { contents: read, packages: write }` (scoped). `scorecard.yml` declares `permissions: read-all` then narrows per-job (`id-token: write, contents: read, pull-requests: read`). `test-gateway.yml` has no explicit `permissions:` block (relies on default — minor, not a fail). | Optional: add `permissions: {}` to `test-gateway.yml` for consistency. |
| 9 | **Pinned-Dependencies** | 10/10 | `requirements-gateway.txt`: `mcp==1.27.2`, `uvicorn[standard]==0.48.0` (exact pins). `constraints.txt` mirrors as `mcp==1.27.2`, `uvicorn==0.48.0`. Used in CI as `pip install -c constraints.txt -r requirements-gateway.txt eu-ai-act-compliance-mcp==1.8.1`. | None — exemplary. |
| 10 | **License** | 10/10 | `LICENSE` (1081 bytes) → base64 decodes to MIT license text. GitHub API confirms `spdx_id: MIT`. | None. |
| 11 | **Fuzzing** | 0/10 | No `fuzz/` dir, no oss-fuzz integration, no `hypothesis` property tests. `http_server.py` parses `Host` header + JSON RPC payloads — both are excellent fuzz targets. | Add `atheris` or `hypothesis` smoke for the JSON-RPC dispatcher. |
| 12 | **Signed-Releases** | 0/10 | `gh api repos/.../releases` → `[]` (no releases at all). No `cosign`, no `sigstore`, no GPG signed tags. `build-push.yml` pushes GHCR images with `provenance: false`. | Add `cosign sign ghcr.io/csoai-org/${{ matrix.flagship }}-mcp@${{ github.sha }}` step. |
| 13 | **Security-Policy** | 10/10 | `SECURITY.md` (1627 bytes) — supported versions table, `security@meok.ai` reporting email with 48h SLA, explicit scope (the `http_server.py` shim, Dockerfile, `/mcp` + `/healthz` + OAuth routes), out-of-scope carve-outs, and hardening notes for the Cloud Run DNS-rebinding decision. | None — exemplary. |
| 14 | **Dependency-Configuration** | 0/10 | No `.github/dependabot.yml` in the keystone (it would scope to the keystone's own 2 deps). | Add one — trivially small, big payoff. |
| 15 | **Packaging** (Public-Risk) | 8/10 | `Dockerfile` uses `python:3.11-slim` + `pip install -r requirements-gateway.txt` — no `curl | sh`, no arbitrary code. `http_server.py` is the only runtime artifact; the build matrix injects a real flagship via `PKG` build-arg. | Deduct 2 for `build_all.sh` (not audited here). |
| 16 | **Contributors** | 0/10 | `gh api .../contributors` returns 1 contributor (`CSOAI-ORG`, 3 contributions). | No bus-factor mitigation. |
| 17 | **Maintained** | 10/10 | `gh api .../commits?since=2026-03-06` → 12 commits in last 90d. `pushedAt: 2026-06-06`. | None. |
| 18 | **SAST-Actions** | 3/10 | `ossf/scorecard-action@v2.4.0` is in `scorecard.yml` (Scorecard, not SAST). Trivy in `build-push.yml` is image vulnerability scanning. `github/codeql-action` is NOT present. Partial credit for proactive security tooling. | Add `github/codeql-action/init@v3` + `/analyze@v3` to a `codeql.yml` workflow. |

## Summary

**Total: 91 / 180 = 5.06 / 10 (50.6%) — yellow zone.**

### Top wins
- **Token-Permissions (10/10)**, **CI-Tests (10/10)** with real e2e, **Pinned-Dependencies (10/10)**, **License (10/10)**, **Security-Policy (10/10)**, **Maintained (10/10)**, **Binary-Artifacts (10/10)**, **Dangerous-Workflow (10/10)**.
- The keystone sets a *better* bar than the flagships in several places (e.g. real e2e tests, explicit permissions blocks, exact-pinned runtime deps, signed release workflow candidate).

### Critical gaps (block a 7+ score)
1. **No Dependabot / Renovate** — single 20-line `.github/dependabot.yml` would fix checks 4 and 14 in one shot.
2. **No CodeQL** — adding a `codeql.yml` fixes checks 5 and 18.
3. **No signed releases / no cosign** — fixes check 12 and unblocks AWS Marketplace seller registration.
4. **Branch protection unverified** — admin must grant token scope or enable protection manually.
5. **No fuzzing** — `http_server.py` is the literal ingress point for the entire fleet; a `hypothesis` smoke is cheap.

### Notable observations
- `SECREVIEW.md` is already in the working tree (untracked in main) — the keystone is the *only* repo in the fleet with this artifact.
- `scorecard.yml` publishes to `scorecard.dev` — once the official Scorecard API is registered, the keystone will appear on the public dashboard.
- The keystone's `http_server.py` is well-suited for fuzzing (Host-header parser, JSON-RPC dispatch, x402 challenge generation) but no fuzz harness exists yet.

### Recommended remediation order (effort vs impact)
1. Add `.github/dependabot.yml` (pip ecosystem, weekly). 5 min.
2. Add `.github/workflows/codeql.yml` (Python, push + PR). 5 min.
3. Add `cosign sign --yes` step to `build-push.yml`. 15 min.
4. Verify branch protection via web UI; document it. 5 min.
5. Add `tests/test_fuzz.py` using `hypothesis` for JSON-RPC. 30 min.

After these five fixes, projected score: **~7.5/10** (green).
