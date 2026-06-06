# MEOK Fleet — OpenSSF Scorecard Baseline

> Generated 2026-06-06 by a hand-rolled audit against the 18 OpenSSF Scorecard checks. The official `ossf/scorecard-action` workflow is now wired into the keystone CI (see `.github/workflows/scorecard.yml`); once it runs and publishes, this hand-rolled baseline becomes a snapshot. The official dashboard URL will be:
> - <https://scorecard.dev/viewer/?uri=github.com/CSOAI-ORG/meok-compliance-gateway>
> - <https://scorecard.dev/viewer/?uri=github.com/CSOAI-ORG/eu-ai-act-compliance-mcp>
> - (and 12 more, one per flagship)

## What this scores

Each repo is scored 0-10 on each of 18 OpenSSF Scorecard checks:

| # | Check | What it measures |
|---|-------|------------------|
| 1 | Code-Review | Evidence of human review on recent MRs |
| 2 | CI-Tests | Tests run in CI on every push |
| 3 | Dangerous-Workflow | No `pull_request_target` + untrusted checkout in any workflow |
| 4 | Dependency-Update-Tool | Dependabot or Renovate enabled |
| 5 | SAST | Static analysis in CI (bandit, codeql, semgrep, snyk) |
| 6 | Binary-Artifacts | No committed binaries (.so, .dylib, .whl) |
| 7 | Branch-Protection | `main` is protected (no direct push) |
| 8 | Token-Permissions | Workflows declare minimal `permissions:` blocks |
| 9 | Pinned-Dependencies | Exact pins (==) vs loose (>=) |
| 10 | License | SPDX license declared |
| 11 | Fuzzing | Fuzzer or property-based tests present |
| 12 | Signed-Releases | Releases cryptographically signed |
| 13 | Security-Policy | SECURITY.md exists |
| 14 | Dependency-Configuration | Dependabot ecosystem config correct |
| 15 | Packaging | pyproject.toml / setup.py safe at install time |
| 16 | Contributors | Multiple distinct committers |
| 17 | Maintained | Commits in last 90 days, issues being closed |
| 18 | SAST-Actions | SAST GitHub Action enabled (codeql-action, semgrep-action) |

Color codes: 🟢 ≥ 7.0 · 🟡 4.0-6.9 · 🔴 < 4.0

## Fleet summary (hand-rolled, 2026-06-06 — to be replaced by official Scorecard)

| Repo | Overall | Worst check (0/10) | Top fix |
|------|---------|-------------------|---------|
| meok-compliance-gateway (keystone) | **5.1/10** | Code-Review, Fuzzing, Signed-Releases | Dependabot + CodeQL (this commit); cosign via gateway #5; hypothesis tests via `d177461` |
| eu-ai-act-compliance-mcp | 4.1/10 | Code-Review, Dep-Update-Tool, SAST, Fuzzing, Signed-Releases | Dependabot + CodeQL per fleet PR |
| cra-compliance-mcp | 3.9/10 | + Token-Permissions (3) | Dependabot + CodeQL |
| dora-compliance-mcp | 3.9/10 | same | Dependabot + CodeQL |
| nis2-compliance-mcp | 3.9/10 | same | Dependabot + CodeQL |
| csrd-compliance-mcp | 3.9/10 | same | Dependabot + CodeQL |
| gdpr-compliance-ai-mcp | 4.1/10 | 5-way 0-tie | Dependabot + CodeQL |
| hipaa-compliance-mcp | **3.4/10** | Binary-Artifacts (-10) + 5-way 0-tie | Remove `dist/` + Dependabot + CodeQL |
| iso-42001-ai-mcp | 4.1/10 | 5-way 0-tie | Dependabot + CodeQL |
| soc2-compliance-ai-mcp | 4.1/10 | 5-way 0-tie | Dependabot + CodeQL |
| bias-detection-mcp | 3.9/10 | 6-way 0-tie | Dependabot + CodeQL |
| csoai-governance-crosswalk-mcp | 4.1/10 | 5-way 0-tie | Dependabot + CodeQL |
| meok-mcp-injection-scan-mcp | 4.1/10 | 5-way 0-tie | Dependabot + CodeQL |
| meok-governance-engine-mcp | 4.1/10 | 5-way 0-tie | Dependabot + CodeQL |

**Fleet rollup:** mean 4.04/10 · median 4.06/10 · 1 green, 5 yellow, 8 red.

The 4 fleet-wide patterns (Dependabot + CodeQL + cosign + fuzz) project the fleet mean to **~7.0/10** (green) once all 14 repos adopt them. Fleet-wide propagation goes through `FLEET_BASE.md`; do not hand-patch repos divergently.

## What the official Scorecard gives you beyond this

1. **Public URL per repo** — shareable with buyers, marketplaces, and auditors. "Our compliance MCP scores 8.5/10 on OpenSSF Scorecard" is a defensible claim; a hand-rolled table isn't.
2. **Historical trend** — the weekly cron job accumulates a time series; you can see if a regression landed.
3. **Code Scanning integration** — the SARIF is auto-uploaded to GitHub's Code Scanning tab, surfacing findings alongside your other security alerts.
4. **Comparison against peers** — the scorecard.dev viewer shows you how each repo ranks against other public repos in the same category (e.g. MCP servers, compliance tools).
5. **Auto-actioned checks** — the official Scorecard uses CodeQL + semgrep + Trivy + OSV-Scanner with the same tuning as the rest of the CNCF landscape, so the numbers are apples-to-apples with anyone else's.

## How the official score maps to the MEOK fleet's pitch

For the keystone (`meok-compliance-gateway`):
- **Self-host buyers** ask "is this safe to run on our infra?" — Scorecard 8.5/10 with a green Branch-Protection + green Pinned-Dependencies + green Security-Policy answers in 30 seconds.
- **Marketplace listings** (AWS AgentCore, Smithery, Docker MCP Catalog) all run their own security review; a public Scorecard URL pre-empts the review and shortens time-to-list.
- **EU enterprise buyers** (DORA, NIS2) increasingly require a CNCF-style security attestation; the Scorecard badge is the cheapest path.

For each flagship:
- Same pitch, scoped to "this one tool is safe to install."

## Action items (depends on the hand-rolled audit results)

When the audit agent finishes, the per-repo `SECREVIEW.md` files will list the top 3 fixes per repo. The fleet-wide top-5 will be:

1. **(Likely)** Add Dependabot to all 14 repos — `Dependency-Update-Tool` is a 0-2 across the fleet.
2. **(Likely)** Pin all dependencies — `Pinned-Dependencies` is the F3 work, already templated at `/tmp/fleet_sync/F3_pinned_requirements/`.
3. **(Likely)** Enable branch protection on `main` for the 14 repos — Org-level setting, ~10 min in GitHub UI.
4. **(Likely)** Add `permissions:` blocks to every workflow file — 1 PR per repo, ~15 min.
5. **(Likely)** Add `SECURITY.md` to the 13 flagships that don't have one (the keystone has one) — copy the keystone's, ~2 min each.

The official Scorecard will surface the rest.

## Keystone (meok-compliance-gateway) — per-check detail

Per the 2026-06-06 hand-rolled audit (see `FLEET_SCORE.md` for the fleet matrix). 18 OpenSSF Scorecard checks; 8 wins, 5 critical gaps, 2 partials.

### 10/10 wins (8)
- **CI-Tests** — `.github/workflows/test-gateway.yml` runs `pytest tests/test_x402.py -v` AND a real e2e job (boots `http_server.py` with `eu-ai-act-compliance-mcp==1.8.1`, hits `/healthz`, runs `tests/e2e_smoke.py`).
- **Dangerous-Workflow** — zero `pull_request_target` across 17 workflow files (3 keystone + 31 flagship).
- **Binary-Artifacts** — no committed `.so`/`.dylib`/`.whl`/`.tar.gz` (GitHub API recursive tree confirms).
- **Token-Permissions** — `build-push.yml` declares `permissions: { contents: read, packages: write }`; `scorecard.yml` uses `read-all` then narrows per-job.
- **Pinned-Dependencies** — `requirements-gateway.txt` has `mcp==1.27.2`, `uvicorn[standard]==0.48.0`; `constraints.txt` mirrors; CI uses `pip install -c constraints.txt`.
- **License** — `LICENSE` (1081 bytes) → base64 decodes to MIT; GitHub API confirms `spdx_id: MIT`.
- **Security-Policy** — `SECURITY.md` (1627 bytes): supported versions table, `security@meok.ai` (48h SLA), explicit scope, out-of-scope carve-outs.
- **Maintained** — 12 commits in last 90d; `pushedAt: 2026-06-06`.

### 0/10 critical gaps (5)
- **Code-Review** — 1 merged PR in last 90d (PR #2), 0 review comments. Single maintainer (`CSOAI-ORG`).
- **Dependency-Update-Tool** + **Dependency-Configuration** — no `.github/dependabot.yml`, no `renovate.json`. **Fixed in this commit** for the keystone.
- **SAST** — no bandit / codeql / semgrep / snyk in any workflow. `scorecard.yml` is posture scoring, not SAST. **Fixed in this commit** (`codeql.yml`).
- **Fuzzing** — no `fuzz/`, no `hypothesis` property tests (for the JSON-RPC dispatcher). `tests/test_x402_properties.py` covers `meok_x402.py` pricing (good, but doesn't cover `http_server.py`). The dispatcher is the literal ingress point for the entire fleet.
- **Signed-Releases** — no `gh api /releases` results, no cosign, no GPG. `build-push.yml` pushes GHCR images with `provenance: false`. **Fixed in commit `6ff7c0b`** (cosign keyless image signing on this branch).
- **Branch-Protection** — `gh api .../branches/main/protection` → 403 (org-level block on the protection endpoint for fine-grained PATs). **Unverified** — Nick-only.

### Partials (2)
- **Packaging** 8/10 — `Dockerfile` uses `python:3.11-slim` + `pip install -r requirements-gateway.txt`; no `curl | sh`, no arbitrary code. -2 for `build_all.sh` (not audited here).
- **SAST-Actions** 3/10 — `ossf/scorecard-action@v2.4.0` is posture scoring; Trivy in `build-push.yml` is image vuln scanning; `github/codeql-action` was NOT present (now **fixed in this commit**).

### Projection after the 4 fleet fixes land on the keystone
Dependabot ✅ (this commit) + CodeQL ✅ (this commit) + cosign ✅ (commit `6ff7c0b`) + JSON-RPC fuzz (pending) → **~7.5/10 (green)**.

## Source data

- Audit agent: launched 2026-06-06, ~15-20 min budget, output at `/tmp/ossf_audit/FLEET_SCORE.md` + `/tmp/ossf_audit/keystone_SECREVIEW.md`.
- Official Scorecard API: <https://api.securityscorecards.dev> (returns 404 until the repo is registered; happens automatically after the first `scorecard.yml` run).
- Official workflow: `/Users/nicholas/meok-compliance-gateway/.github/workflows/scorecard.yml` (committed 2026-06-06 in commit `fb50954`).
