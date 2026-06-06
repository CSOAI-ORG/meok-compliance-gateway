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

## Fleet summary (hand-rolled, to be replaced by official Scorecard)

| Repo | Overall | Worst check | Top fix |
|------|---------|-------------|---------|
| meok-compliance-gateway (keystone) | TBD | TBD | TBD |
| eu-ai-act-compliance-mcp | TBD | TBD | TBD |
| cra-compliance-mcp | TBD | TBD | TBD |
| dora-compliance-mcp | TBD | TBD | TBD |
| nis2-compliance-mcp | TBD | TBD | TBD |
| csrd-compliance-mcp | TBD | TBD | TBD |
| gdpr-compliance-ai-mcp | TBD | TBD | TBD |
| hipaa-compliance-mcp | TBD | TBD | TBD |
| iso-42001-ai-mcp | TBD | TBD | TBD |
| soc2-compliance-ai-mcp | TBD | TBD | TBD |
| bias-detection-mcp | TBD | TBD | TBD |
| csoai-governance-crosswalk-mcp | TBD | TBD | TBD |
| meok-mcp-injection-scan-mcp | TBD | TBD | TBD |
| meok-governance-engine-mcp | TBD | TBD | TBD |

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

## Source data

- Audit agent: launched 2026-06-06, ~15-20 min budget, output at `/tmp/ossf_audit/FLEET_SCORE.md` + `/tmp/ossf_audit/keystone_SECREVIEW.md`.
- Official Scorecard API: <https://api.securityscorecards.dev> (returns 404 until the repo is registered; happens automatically after the first `scorecard.yml` run).
- Official workflow: `/Users/nicholas/meok-compliance-gateway/.github/workflows/scorecard.yml` (committed 2026-06-06 in commit `fb50954`).
