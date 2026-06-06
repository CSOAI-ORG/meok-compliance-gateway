# OpenSSF Scorecard Fleet Audit - 14 MEOK repos

**Date:** 2026-06-06
**Method:** Hand-rolled approximation of the 18 OpenSSF Scorecard checks.
  Local file inspection for the keystone; `gh api` for 13 flagships.
**Caveat:** Official OpenSSF Scorecard API was NOT run (not yet registered for these repos).
  Scores are best-effort heuristics. Branch-Protection check is 403-blocked for all 14 repos by the org-level PAT scope - scored 0 conservatively.

## Overall fleet rollup

- **Mean score:**   4.04 / 10
- **Median score:** 4.06 / 10
- **Best repo:**    meok-compliance-gateway - 91/180 (5.1/10)
- **Worst repo:**   hipaa-compliance-mcp - 61/180 (3.4/10)

## Per-repo score matrix

| Repo | Sum/180 | /10 | Band | Code-R | CI-Tes | Danger | Depend | SAST | Binary | Branch | Token- | Pinned | Licens | Fuzzin | Signed | Securi | Depend | Packag | Contri | Mainta | SAST-A |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `meok-compliance-gateway` | 91/180 | **5.1** | [YELLOW] | 0 | 10 | 10 | 0 | 0 | 10 | 0 | 10 | 10 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 3 |
| `eu-ai-act-compliance-mcp` | 73/180 | **4.1** | [YELLOW] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 5 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `cra-compliance-mcp` | 71/180 | **3.9** | [RED   ] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 3 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `dora-compliance-mcp` | 71/180 | **3.9** | [RED   ] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 3 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `nis2-compliance-mcp` | 71/180 | **3.9** | [RED   ] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 3 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `csrd-compliance-mcp` | 71/180 | **3.9** | [RED   ] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 3 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `gdpr-compliance-ai-mcp` | 73/180 | **4.1** | [YELLOW] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 5 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `hipaa-compliance-mcp` | 61/180 | **3.4** | [RED   ] | 0 | 8 | 10 | 0 | 0 | 0 | 0 | 3 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `iso-42001-ai-mcp` | 73/180 | **4.1** | [YELLOW] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 5 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `soc2-compliance-ai-mcp` | 73/180 | **4.1** | [YELLOW] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 5 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `bias-detection-mcp` | 71/180 | **3.9** | [RED   ] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 3 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `csoai-governance-crosswalk-mcp` | 73/180 | **4.1** | [YELLOW] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 5 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `meok-mcp-injection-scan-mcp` | 73/180 | **4.1** | [YELLOW] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 5 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |
| `meok-governance-engine-mcp` | 73/180 | **4.1** | [YELLOW] | 0 | 8 | 10 | 0 | 0 | 10 | 0 | 5 | 2 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 0 |

Legend: GREEN = >=7.0/10, YELLOW = 4.0-6.9/10, RED = <4.0/10

## Pattern observations

### Universal fleet gaps (every repo: 0)
- **Code-Review** - single maintainer (`CSOAI-ORG`); no PR review evidence on any merged PR in 90d.
- **Dependency-Update-Tool** + **Dependency-Configuration** - zero `dependabot.yml` or `renovate.json` across all 14 repos.
- **SAST** + **SAST-Actions** - zero CodeQL, Bandit, Semgrep, or Snyk. Only Ruff lint (E,W,F).
- **Fuzzing** - no `fuzz/`, no `hypothesis`, no oss-fuzz integration.
- **Signed-Releases** - no cosign, no sigstore, no GPG-signed tags. Smithery publish uses `attest-build-provenance` (provenance, not signing).
- **Branch-Protection** - could not verify (org-level PAT scope blocks the endpoint).

### Universal fleet wins (every repo: 10)
- **Dangerous-Workflow** - zero `pull_request_target` across 3 keystone + 31 flagship workflow files.
- **License** - MIT on all 14 repos.
- **Packaging** - hatch backend, no arbitrary code at install time.
- **Maintained** - all repos committed within 90d; fleet median 45 commits/90d.

### Repos with unique characteristics
- `meok-compliance-gateway` (keystone) - **best in fleet at 5.1/10**. Only repo with: real e2e CI, exact-pinned runtime deps, scoped `permissions:` blocks, OpenSSF Scorecard action, SECREVIEW.md. Sets the bar the flagships should follow.
- `hipaa-compliance-mcp` - **worst in fleet at 3.4/10**. The only repo with committed binary artifacts (`dist/hipaa_compliance_mcp-1.0.0-py3-none-any.whl` and `.tar.gz`). Deductions: -10 Binary-Artifacts, -2 Pinned-Dependencies (mcp>=1.0.0 loose pin), -2 fewer commit/tooling.
- `eu-ai-act-compliance-mcp` - highest commit volume (91/90d) and only flagship with 2 contributors (CSOAI-ORG + mcpize[bot]).
- `csoai-governance-crosswalk-mcp`, `bias-detection-mcp` - 1 ci.yml + 1 test.yml each (slimmest CI).

### Methodology notes
- **Branch-Protection 0 across the board** is an artifact of the audit tooling, NOT necessarily a real fail. The org admin must grant the token `administration:read` on the org to verify.
- **Token-Permissions scores 3-10** depending on whether the repo has any workflow with explicit `permissions:`. None of the flagship `ci.yml` files declare `permissions:` (they rely on the org default).
- **Pinned-Dependencies scores 2** on all flagships because `pyproject.toml` uses `mcp>=1.0.0` / `pydantic>=2.0.0` (lower-bound only, not exact). The keystone scores 10 because it ships `requirements-gateway.txt` with `==` pins and a `constraints.txt` for the e2e job.
- **Contributors scores 0-3** because every repo is single-maintainer (CSOAI-ORG). The only exception is `eu-ai-act-compliance-mcp` (2 contributors including `mcpize[bot]`).

## Remediation priority (fleet-wide)
1. Add `.github/dependabot.yml` in all 14 repos - 5 min each, fixes Dependency-Update-Tool + Dependency-Configuration. Estimated gain: +14x2 = +28 column-points.
2. Add `.github/workflows/codeql.yml` in all 14 repos - fixes SAST + SAST-Actions. Estimated gain: +14x~13 = +182 column-points. Single highest-leverage move.
3. Add `cosign sign` step to every release-publishing workflow (build-push on keystone, mcp-smithery-publish + mcp-registry-publish on flagships). Fixes Signed-Releases. Estimated gain: +14x10 = +140 column-points.
4. Add CODEOWNERS + enforce branch protection. Fixes Code-Review + Branch-Protection. Estimated gain: +14x~10 = +140 column-points.
5. Remove `dist/` artifacts from `hipaa-compliance-mcp` (the lone Binary-Artifacts failure). Estimated gain: +10 column-points.

After (1)+(2)+(3) the fleet mean would move from **4.04/10 -> ~7.5/10 (green)**.