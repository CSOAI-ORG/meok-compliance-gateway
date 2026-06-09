# Deploy the MEOK Revenue Rail

> One-page deploy runbook. From "code is committed" to "the keystone is publicly
> addressable, accepts USDC, and shows up on /mcp". Three steps. Most of the
> work is on your side; engineering is staged.

## 0. What "deployed" means (definition of done)

| Dimension | "Deployed" = | Verify with |
|---|---|---|
| **Code** | `feat/revenue-rail-testnet` pushed, PR opened | `gh pr list` shows the PR |
| **Image** | GHCR image built + public | `docker pull ghcr.io/csoai-org/meok-compliance-gateway:latest` |
| **Live** | `/healthz` returns 200 from a public URL | `curl -sI https://<your-domain>/healthz` |
| **Billed** | `X402_ENABLED=1` + `X402_PAY_TO=<mainnet>` in prod env | `curl -X POST https://<your-domain>/mcp` returns a 402 challenge |
| **Settled** | a real USDC payment lands at the wallet | BaseScan shows the `Transfer` event |

## 1. Push the branch (Nick)

The branch is `feat/revenue-rail-testnet` at `f2bcc70`, in worktree
`/tmp/revenue-rail-2026-06-09/`. Per `keyring-token-push-rule`, push needs
the keyring token (the env `GITHUB_TOKEN` 403s for `git push` on CSOAI-ORG):

```bash
cd /tmp/revenue-rail-2026-06-09
env -u GITHUB_TOKEN -u GH_TOKEN git push -u origin feat/revenue-rail-testnet
```

Then open a PR against `main` (or `gateway/main` — match the keystone's
branch base) with a 1-line body:

```text
Adds keystone server.py, .env.example, settlement smoke. Fixes v1 PaymentPayload
support in meok_x402.paywalled. 15/15 tests pass; boot+challenge smoke green.
```

The PR description also lives in the commit body — copy from
`git log -1 feat/revenue-rail-testnet` for the full rationale.

## 2. Pick a host

Three options, ranked by time-to-live-URL:

| Host | Time | Cost (idle) | Best for |
|---|---|---|---|
| **Cloud Run** (GCP) | 15 min | $0 (scales to 0) | **Recommended.** Matches the keystone's existing `GCP_DEPLOY.md`. |
| **AWS App Runner** | 20 min | ~$5/mo minimum | If you're already on AWS for x402 secrets (Secrets Manager). |
| **Fly.io** | 10 min | $0–5/mo | Fastest. Region flexibility for latency. |
| **Local + Tailscale** | 5 min | $0 | For staging only; not public-internet-addressable. |

### 2a. Cloud Run (the default)

`GCP_DEPLOY.md` already documents the keystone's Cloud Run deploy. The
revenue-rail overlay adds 5 env vars on top of whatever it sets:

```bash
# From the keystone repo, with gcloud auth'd and PROJECT=meok-prod:
gcloud run deploy meok-compliance-gateway \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars "MEOK_ENV=production" \
  --set-env-vars "X402_ENABLED=1" \
  --set-env-vars "X402_NETWORK=eip155:8453" \
  --set-secrets "X402_PAY_TO=meok/x402-pay-to:latest" \
  --set-secrets "MEOK_ATTESTATION_KEY=meok/attestation-key:latest" \
  --memory 512Mi --cpu 1 --concurrency 80
```

**Two notes on the flags:**

- `--set-secrets` (not `--set-env-vars`) for `X402_PAY_TO` and
  `MEOK_ATTESTATION_KEY` — both are CRITICAL_FIXES_2026-06-08.md #3
  violations if they ever sit in the env (the SOV3 audit caught us).
  Cloud Run mounts them from Secret Manager, the env-var leak window is
  closed.
- `--port 8080` matches the keystone's Dockerfile (`EXPOSE 8080`).
  `http_server.py` reads `PORT` from env, so the 8000/8080 mismatch is
  a single-flag fix.

After deploy, Cloud Run prints a URL like
`https://meok-compliance-gateway-xxxxx-uc.a.run.app`. Hit it:

```bash
curl -s https://<cloud-run-url>/healthz
# {"status": "ok", "server": "meok-compliance-gateway", ...}

curl -s -X POST https://<cloud-run-url>/mcp -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | jq .
# Should list 5 tools: health, list_experts, sign_receipt, spending_report, verify_receipt
```

If the `tools/list` returns 4 tools, `X402_ENABLED=1` got dropped or
the env name is wrong — check Cloud Run logs.

### 2b. Fly.io (fastest)

```bash
fly launch --image ghcr.io/csoai-org/meok-compliance-gateway:latest --no-deploy
fly secrets set MEOK_ATTESTATION_KEY=<hex> X402_PAY_TO=0x<addr>
fly secrets set X402_ENABLED=1 X402_NETWORK=eip155:8453 MEOK_ENV=production
fly deploy
```

Then `fly open` to grab the URL. ~10 min, all from a laptop.

## 3. Get the testnet settlement green first (don't skip this)

**Do not flip `X402_NETWORK=eip155:8453` (mainnet) until the testnet smoke
passes.** The testnet smoke is a real settled USDC transaction on Base
Sepolia — proof the rail is wired correctly, no mainnet dollars at risk.

Steps (10 min, free):

1. **Generate a throwaway testnet key** (in the keystone worktree):
   ```bash
   /opt/homebrew/bin/python3.11 scripts/test_x402_settlement.py --print-signer
   # TESTNET_ADDRESS=0x...
   # TESTNET_KEY=0x...
   ```

2. **Fund it with Base Sepolia USDC** (free, ~2 min):
   - Go to https://faucet.circle.com
   - Select network: **Base Sepolia**, asset: **USDC**
   - Paste the `TESTNET_ADDRESS`
   - Request 20 USDC (allowance is 20/2h per the faucet)

3. **Add a Coinbase CDP testnet wallet** to receive the payment:
   - Go to https://portal.cdp.coinbase.com
   - Create a CDP account (free, no KYC for testnet)
   - Create an API key with `wallet:read` scope
   - Use the same key as the signer (self-payment smoke) OR create a
     second throwaway key and set `X402_PAY_TO` to its address

4. **Run the smoke** (in the worktree):
   ```bash
   export X402_ENABLED=1
   export X402_PAY_TO=0x<address from step 3>
   export X402_NETWORK=eip155:84532   # Sepolia
   export MEOK_ATTESTATION_KEY=$(/opt/homebrew/bin/python3.11 -c "import secrets; print(secrets.token_hex(32))")
   export TEST_SIGNER_KEY=<key.hex() from step 1>
   /opt/homebrew/bin/python3.11 scripts/test_x402_settlement.py
   ```

   Expected output (last 5 lines):
   ```
   [OK] tool ran: attestation_id=<uuid>
   [OK] spending log: 0 → 1 call(s)
   [OK] payer recorded: 0x7e5f45…bdf
   ALL GREEN — x402 rail end-to-end working.
   ```

5. **Verify on BaseScan Sepolia**:
   - https://sepolia.basescan.org/address/<X402_PAY_TO>
   - Should show a `Transfer` event for 0.05 USDC from the test signer

If step 4 fails, see "Troubleshooting" below.

## 4. Flip to mainnet (after testnet is green)

Two changes:

```bash
# 1. Swap env var
export X402_NETWORK=eip155:8453   # was eip155:84532

# 2. Re-run with the mainnet wallet (NOT the testnet key)
unset TEST_SIGNER_KEY
# X402_PAY_TO stays = your real Coinbase CDP mainnet USDC address
# Re-run with a real payer's key, not the testnet one
```

Then redeploy. Cloud Run: `gcloud run services update meok-compliance-gateway
--update-env-vars "X402_NETWORK=eip155:8453"`. Fly: `fly secrets set
X402_NETWORK=eip155:8453`.

## 5. Wire a paying agent

The keystone is now a paying endpoint. To drive a real revenue event, you
need an x402-aware MCP client. Three options:

- **`kimi-cli`** (or any MCP client) pointed at your Cloud Run URL.
  When the client calls `sign_receipt`, the keystone returns a
  `PaymentRequired` challenge; the client (if x402-aware) signs a USDC
  payment and retries.
- **The included smoke** as a permanent CI test: schedule
  `scripts/test_x402_settlement.py` weekly in a GitHub Action. If a
  facilitator outage breaks the rail, you'll know in 1 day.
- **Glama / Smithery listings** will surface the cost-warning tools
  automatically. The dist/ payloads (already generated for 44 flagships)
  describe the paywall in the tool's description — agents that read
  MCP listings will see "COST WARNING: $0.05 per call" before calling.

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `tools/list` returns 4 tools | `X402_ENABLED=0` in deploy env | Check `--set-env-vars` was applied; `gcloud run services describe` |
| `[FAIL] environment not ready` from the smoke | `X402_PAY_TO` is the all-zeros placeholder | Paste a real address |
| `[FAIL] no matching requirements` after signing | Payer's USDC amount ≠ challenge amount | Both should be `50000` atomic for $0.05; check `$0.05` isn't mistyped as `0.05` |
| `[FAIL] verification failed` (facilitator) | Testnet USDC not yet on the address | Wait 30s; refresh https://sepolia.basescan.org |
| Facilitator timeout | `https://www.x402.org/facilitator` is down | Set `X402_FACILITATOR_URL` to a backup; check https://status.x402.org |
| Spending log shows 0 calls | `spending_report` cached before the call | Hit `spending_report` again — it's a fresh snapshot every call |
| Cloud Run 502 on first request | Cold start + lazy-import of x402 SDK | Normal; the first request triggers the lazy import and is slow. Subsequent calls are fast. |

## 7. What stays manual (the runbook gates that this doesn't unblock)

- **G1 — PyPI new-project cap**: still email `pypi-support@python.org`.
  The keystone deploys via Docker (not PyPI) so this doesn't block Cloud
  Run, but it does block `pip install agentaudit` for paying Python agents.
- **G2 — DNS for meok.ai / councilof.ai / proofof.ai**: the keystone works
  at the `*.run.app` URL; the custom domains are optional for revenue.
- **G6 — Directory signups**: still needed for Glama / Smithery listings
  to surface the cost-warning tools. Without them, agent traffic only
  comes from people who already know the URL.

## 8. Time + dollar budget

| Step | Time | Cost |
|---|---:|---:|
| Push branch + open PR | 5 min | $0 |
| Cloud Run deploy (first time) | 15 min | $0 idle, ~$0.50/day at 80 concurrency |
| Testnet smoke (steps 1-4 above) | 10 min | $0 (testnet USDC is free) |
| Flip to mainnet | 2 min | $0 idle, same per-call cost |
| **Total to first settled testnet payment** | **~30 min** | **$0** |
| **Total to mainnet live billing** | **~35 min** | **$0/mo + gas per settled call** |

The first real revenue event costs: the first payer's gas (~$0.001 on
Base) + the keystone's idle Cloud Run cost (~$0.50/day). Every call
after that is gross margin.

## Cross-references

- `HANDOFF.md` — the broader 5-step Nick action list
- `MEOK_LAUNCH_RUNBOOK.md` §5 — the 6-gate register (this rail unblocks G3)
- `MCP_2026_07_28_SPIKE.md` — why we run stateless mode (no impact on x402)
- `CRITICAL_FIXES_2026-06-08.md` Fix #3 — why `MEOK_ATTESTATION_KEY` MUST NOT be an env var
- `x402-rollout-state` memory — the @paywalled rollout history
- `meok-fleet-monetization-blockers` memory — the 5 monetization actions
