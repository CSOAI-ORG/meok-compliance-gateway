# AgentAudit — Publish & Deploy Checklist

This file is the **Nick-only** runbook for the steps that are account-gated per
[`AGENTS.md`](../../AGENTS.md) (org tokens, paid accounts, signing keys). The
Claude-side work is already on `feat/agentaudit-server` and pushed; the rest is
the operator's switchboard.

---

## 0. Pre-flight

```bash
git checkout feat/agentaudit-server
git log --oneline -10
git status
```

Confirm the branch has all 7 new commits (c4af835 → 1b4af8c, plus the 8th-paid
tool commit at the tip).

---

## 1. Open the PR

```bash
env -u GITHUB_TOKEN -u GH_TOKEN gh pr create \
  --base main \
  --head feat/agentaudit-server \
  --title "feat(agentaudit): 8 priced tools, AA+++ hardening, x402 spending report" \
  --body-file - <<'EOF'
## Summary
- **Paid tool #8:** `score_agent` at $0.10 (was the conspicuously-free headline).
- **AA+++ scorecard gains:** CODEOWNERS for agentaudit/**, Semgrep SAST,
  dependabot github-actions, all 3rd-party actions SHA-pinned.
- **Free observability:** `x402_spending_report` records verified paid calls.
- **Test totals:** 78 passing (55 unit + 14 x402 + 9 hypothesis), up from 56.

## Files of note
- `agentaudit/agentaudit/server.py` — `@paywalled` on `score_agent`
- `agentaudit/agentaudit/x402.py` — `_PAID_LOG` + `spending_snapshot()`
- `agentaudit/tests/test_agentaudit.py` — new spending-report integration test
- `agentaudit/PUBLISH.md` (new) — the checklist you're reading
- `CODEOWNERS` — explicit agentaudit + workflow ownership
- `.github/dependabot.yml` — +github-actions ecosystem
- `.github/workflows/semgrep.yml` (new) — pip-installed Semgrep, advisory mode
- All 6 workflows — every `uses:` pinned to a 40-char commit SHA

## Next steps (Nick)
- See `agentaudit/PUBLISH.md` for the PyPI / GHCR / wallet / cosign checklist
EOF
```

---

## 2. Merge to `main`

```bash
env -u GITHUB_TOKEN -u GH_TOKEN gh pr merge --squash
```

After merge, the `scorecard.yml` weekly cron will start reporting the new
score on the dashboard within 24h.

---

## 3. PyPI publish

```bash
# Token from https://pypi.org/manage/account/token/  (scope: agentaudit)
env -u GITHUB_TOKEN -u GH_TOKEN twine upload \
  agentaudit/dist/agentaudit-0.1.0-py3-none-any.whl \
  agentaudit/dist/agentaudit-0.1.0.tar.gz
```

Verify:
```bash
curl -fsS https://pypi.org/pypi/agentaudit/json | jq -r '.info.version'
```

---

## 4. GHCR — build & push the agentaudit image

The current `build-push.yml` matrix covers 8 flagship packages but **not**
`agentaudit` itself. Add it to the matrix (file lives in
`.github/workflows/build-push.yml`):

```yaml
matrix:
  include:
    - flagship: agentaudit
      pkg: agentaudit
```

Then flip the published image to **Public** (one-time, UI step):
`github.com → CSOAI-ORG → Packages → agentaudit-mcp → Package settings →
Change visibility → Public`.

---

## 5. Coinbase CDP receiving wallet

The paywire is OFF until you set `X402_PAY_TO`. Create the wallet in
[CDP Portal](https://portal.cdp.coinbase.com/) and set it as a deployment
secret:

```bash
# In Cloud Run / AgentCore / your runtime of choice:
X402_ENABLED=1
X402_PAY_TO=0xYourBaseMainnetAddress    # CDP receiving wallet
X402_NETWORK=eip155:8453                # Base mainnet
X402_ASSET=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913  # USDC on Base (default)
```

For testnet first:
```bash
X402_NETWORK=eip155:84532  # Base Sepolia
X402_ASSET=0x036CbD53842c5426634e7929541eC2318f3dCF7e
```

---

## 6. Cosign keyless signing (AA+++ Signed-Releases)

The keystone has cosign keyless on `build-push.yml`. Apply the same pattern to
the agentaudit image after step 4:

```yaml
- name: Sign image with cosign keyless
  uses: sigstore/cosign-installer@v3.10.0
  with:
    cosign-release: 'v2.4.1'

- name: Sign
  env:
    COSIGN_EXPERIMENTAL: '1'
  run: |
    cosign sign --yes ghcr.io/csoai-org/agentaudit-mcp@${{ github.sha }}
```

Requires `id-token: write` in the job `permissions:` block (a Nick-only
org flip).

---

## 7. Smithery + MCP marketplace listing

```bash
npm install -g @smithery/cli
smithery login
smithery publish ./agentaudit
```

(Requires a Smithery API key — see the keystone's marketplace runbook for
the exact MCP card shape.)

---

## 8. Stripe + Resend (optional, subscription rail)

If we add a Stripe + Resend control plane for trial/upgrade flows:

```bash
# Stripe
stripe listen --forward-to localhost:8000/stripe/webhook

# Resend
RESEND_API_KEY=re_xxx
```

Account-gated (Stripe / Resend dashboards) — see the gateway's
`PAYG.md` for the same pattern.

---

## Reference

- Scorecard baseline: see `FLEET_SCORE.md` at repo root (manual heuristic).
- CodeQL: `.github/workflows/codeql.yml` — runs on push to main + every PR.
- Scorecard: `.github/workflows/scorecard.yml` — runs weekly + on every push to main.
- All workflows SHA-pinned: see commit `1b4af8c` (Dangerous-Workflow hardening).
