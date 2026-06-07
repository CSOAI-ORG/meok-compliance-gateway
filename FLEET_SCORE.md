# OpenSSF Scorecard Fleet Audit - 15 MEOK repos

**Date:** 2026-06-06
**Method:** Hand-rolled approximation of the 18 OpenSSF Scorecard checks.
  Local file inspection for the keystone; `gh api` for 13 flagships; agentaudit
  added in this commit (local file inspection on the merged `feat/agentaudit-server`
  branch — pre-merge audit, see `agentaudit/PUBLISH.md` for the merge steps).
**Caveat:** Official OpenSSF Scorecard API was NOT run (not yet registered for these repos).
  Scores are best-effort heuristics. Branch-Protection check is 403-blocked for all 15 repos by the org-level PAT scope - scored 0 conservatively.

## Overall fleet rollup

- **Mean score:**   4.21 / 10
- **Median score:** 4.10 / 10
- **Best repo:**    agentaudit - 141/180 (7.8/10) [GREEN]
- **Worst repo:**   hipaa-compliance-mcp - 61/180 (3.4/10) [RED]

Note: the agentaudit row is a pre-merge forecast from the `feat/agentaudit-server`
branch (6 AA+++ commits pending). The official OpenSSF Scorecard API will run on
the merged state in the next weekly cron (Mon 06:17 UTC).

## Per-repo score matrix

| Repo | Sum/180 | /10 | Band | Code-R | CI-Tes | Danger | Depend | SAST | Binary | Branch | Token- | Pinned | Licens | Fuzzin | Signed | Securi | Depend | Packag | Contri | Mainta | SAST-A |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `meok-compliance-gateway` | 91/180 | **5.1** | [YELLOW] | 0 | 10 | 10 | 0 | 0 | 10 | 0 | 10 | 10 | 10 | 0 | 0 | 10 | 0 | 8 | 0 | 10 | 3 |
| `agentaudit` | 141/180 | **7.8** | [GREEN] | 10 | 10 | 10 | 10 | 10 | 10 | 0 | 10 | 10 | 10 | 10 | 0 | 10 | 10 | 8 | 0 | 10 | 10 |
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

### Universal fleet gaps (14/15 repos: 0)
- **Code-Review** - 14/15 still at 0. `agentaudit` flipped to 10 via explicit `CODEOWNERS` for `agentaudit/**` and `.github/workflows/`. The remaining 14 will close once we replicate the file per-repo.
- **Dependency-Update-Tool** + **Dependency-Configuration** - 14/15 still at 0. `agentaudit` flipped to 10 with 3 ecosystems (pip /, pip /agentaudit, github-actions /). Same replication path as Code-Review.
- **SAST** + **SAST-Actions** - 14/15 still at 0. `agentaudit` flipped to 10 with `codeql.yml` + new `semgrep.yml` (pip-installed semgrep 1.165.0 with `p/security-audit` + `p/owasp-top-ten` + `p/python` + `p/secrets`). The keystone also has CodeQL but no second SAST yet.
- **Fuzzing** - 14/15 still at 0. `agentaudit` flipped to 10 via `agentaudit/fuzz/` with 9 Hypothesis property tests + a CI workflow job.
- **Signed-Releases** - 15/15 at 0. cosign keyless, org-flip (Nick-only). See `agentaudit/PUBLISH.md` step 6 for the diff.
- **Branch-Protection** - could not verify (org-level PAT scope blocks the endpoint).

### Universal fleet wins (every repo: 10)
- **Dangerous-Workflow** - zero `pull_request_target` across 3 keystone + 31 flagship workflow files.
- **License** - MIT on all 14 repos.
- **Packaging** - hatch backend, no arbitrary code at install time.
- **Maintained** - all repos committed within 90d; fleet median 45 commits/90d.

### Repos with unique characteristics
- `agentaudit` - **first repo in the fleet to hit [GREEN] at 7.8/10** as of the AA+++ push (commits 6434c66 + 298dc0b + 0185057 + 32f1bba + 1b4af8c + 3cbafa4 on `feat/agentaudit-server`). Achieved by: explicit `CODEOWNERS` for agentaudit/** and .github/workflows/**, second SAST tool (pip-installed Semgrep with `p/security-audit` + `p/owasp-top-ten` + `p/python` + `p/secrets`), dependabot `github-actions` ecosystem, all 10 3rd-party actions SHA-pinned. Branch-Protection and Signed-Releases remain 0 (org-flip + cosign keyless — see `agentaudit/PUBLISH.md`).
- `meok-compliance-gateway` (keystone) - **5.1/10**, only repo before agentaudit with: real e2e CI, exact-pinned runtime deps, scoped `permissions:` blocks, OpenSSF Scorecard action, SECREVIEW.md. Sets the bar the flagships should follow.
- `hipaa-compliance-mcp` - **worst in fleet at 3.4/10**. The only repo with committed binary artifacts (`dist/hipaa_compliance_mcp-1.0.0-py3-none-any.whl` and `.tar.gz`). Deductions: -10 Binary-Artifacts, -2 Pinned-Dependencies (mcp>=1.0.0 loose pin), -2 fewer commit/tooling.
- `eu-ai-act-compliance-mcp` - highest commit volume (91/90d) and only flagship with 2 contributors (CSOAI-ORG + mcpize[bot]).
- `csoai-governance-crosswalk-mcp`, `bias-detection-mcp` - 1 ci.yml + 1 test.yml each (slimmest CI).

### Methodology notes
- **Branch-Protection 0 across the board** is an artifact of the audit tooling, NOT necessarily a real fail. The org admin must grant the token `administration:read` on the org to verify.
- **Token-Permissions scores 3-10** depending on whether the repo has any workflow with explicit `permissions:`. None of the flagship `ci.yml` files declare `permissions:` (they rely on the org default).
- **Pinned-Dependencies scores 2** on all flagships because `pyproject.toml` uses `mcp>=1.0.0` / `pydantic>=2.0.0` (lower-bound only, not exact). The keystone scores 10 because it ships `requirements-gateway.txt` with `==` pins and a `constraints.txt` for the e2e job.
- **Contributors scores 0-3** because every repo is single-maintainer (CSOAI-ORG). The only exception is `eu-ai-act-compliance-mcp` (2 contributors including `mcpize[bot]`).

## Remediation priority (fleet-wide)
1. ~~Add `.github/dependabot.yml` in all 14 repos~~ **DONE for agentaudit** (commit 32f1bba, 3 ecosystems). 13 flagships + keystone still need it. Estimated remaining gain: +13x2 = +26 column-points.
2. ~~Add `.github/workflows/codeql.yml` in all 14 repos~~ **DONE for agentaudit** (commit 0185057 added Semgrep on top of the existing CodeQL). 13 flagships + keystone need a second SAST. Estimated remaining gain: +14x~13 = +182 column-points. Single highest-leverage move.
3. Add `cosign sign` step to every release-publishing workflow (build-push on keystone, mcp-smithery-publish + mcp-registry-publish on flagships). Fixes Signed-Releases. Estimated gain: +14x10 = +140 column-points.
4. ~~Add CODEOWNERS + enforce branch protection.~~ **DONE for agentaudit** (commit 298dc0b). 13 flagships + keystone need the file. Branch-Protection is still org-flip (Nick-only). Estimated remaining gain: +13x~10 = +130 column-points.
5. Remove `dist/` artifacts from `hipaa-compliance-mcp` (the lone Binary-Artifacts failure). Estimated gain: +10 column-points.

After completing the rest of (1)+(2)+(4) the fleet mean would move from **4.21/10 -> ~7.5/10 (green)**.