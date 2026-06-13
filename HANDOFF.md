# MEOK Launch Handoff — 1-pager for Nick

> **Total time**: ~3.5 hours manual. **$11K/day of Year-1 ARR at risk** per `meok-deep-audit-2026-06-08` P0-4.
> **Goal**: unblock the keystone for live revenue. Every step is account-gated — no automation can do these.
> **Per memory `meok-fleet-monetization-blockers.md`**: each step is independent; do them in the listed order for fastest first $$ impact.
>
> **Last updated**: 2026-06-09 — added §6 "Revenue Rail: x402 testnet → mainnet" (~30 min, $0). The keystone is now bootable end-to-end on `feat/revenue-rail-testnet` (commit `f2bcc70`). See `DEPLOY_REVENUE_RAIL.md` for the full 8-step deploy runbook.

---

## The 5 manual blockers (in order of revenue impact)

### 1. 🔴 Stripe Live Mode (2 hours, ~$XK/day ARR)

**What it unblocks**: `meok.ai` B2B subscriptions on the `meok-compliance-gateway`. All the hive `pricing_tier` + `monthly_floor_usd` configs (`scripts/gen-hive.py`) reference this.

**Steps**:
- Go to → https://dashboard.stripe.com/account/onboarding
- Fill in: business details, bank account, tax info, public/business URL (`https://meok.ai`)
- Switch to **Live mode** (top-right toggle in the dashboard)
- Get the **live secret key** (starts with `sk_live_...`) + **publishable key** (starts with `pk_live_...`)
- Set up **3 products** matching `gen-hive.py` pricing:
  - Team ($29/seat/mo)
  - Business ($49/seat/mo)
  - Enterprise (contact sales)
- Create a **webhook endpoint** at `https://meok.ai/api/stripe/webhook` (events: `customer.subscription.created/updated/deleted`, `invoice.paid/failed`)
- Save the **webhook signing secret** (starts with `whsec_...`)

**Then**:
- `cd /Users/nicholas/meok-compliance-gateway && python3 scripts/check-secret-perms.sh --fix` (chmod 600 the dir)
- Add to OS keyring: `python3 -c "import keyring; keyring.set_password('meok.ai', 'stripe-secret-key', 'sk_live_...')"`
- Add the webhook secret the same way

---

### 2. 🟠 Vercel deploy (10 min × 4 sites = 40 min, ~$XK/day)

**What it unblocks**: `meok.ai`, `csoai.org`, `proofof.ai`, `openmoe.ai` public-facing sites. The 28 hive READMEs link to these.

**Steps** (do once per site):
- Go to → https://vercel.com/dashboard
- **Add New Project** → **Import** from `CSOAI-ORG/<site>` (e.g. `meok-ai`, `csoai-org`, `proof-of-ai`, `openmoe-ai`)
- For each: framework = "Other", root = `./`, no build command
- **Environment variables** (per site):
  - `STRIPE_SECRET_KEY` = (from step 1)
  - `STRIPE_WEBHOOK_SECRET` = (from step 1)
  - `MEOK_ENV` = `production`
  - `MEOK_PUSH_OK` = `1` (only on the keystone build)
- Click **Deploy**. Vercel auto-assigns a `*.vercel.app` URL.
- **Buy the domain** (if not already) and add it in **Settings → Domains**

**Then**: re-deploy the keystone as `https://meok.ai/api/mcp` so the gateway has a public endpoint.

---

### 3. 🟡 Namecheap DNS for meok.ai (1 hour, ~$X/day)

**What it unblocks**: `meok.ai` resolving to the Vercel deploy. Until this is done, the keystone lives at a `*.vercel.app` URL only.

**Steps**:
- Go to → https://www.namecheap.com/domains/list/
- Click **`meok.ai`** → **Manage** → **Advanced DNS**
- **Delete** any default parking records
- **Add**:
  - `A Record`  → `@`   → `76.76.21.21` (Vercel)
  - `CNAME`     → `www` → `cname.vercel-dns.com.`
  - `CNAME`     → `api` → `cname.vercel-dns.com.`
- **Save**. DNS propagates in 5-30 min.
- Same for `csoai.org`, `proofof.ai`, `openmoe.ai` (if they're in Namecheap too — some may be on a different registrar)

---

### 4. 🟢 Resend API key (5 min, ~$X/day)

**What it unblocks**: transactional email from the keystone (subscription confirmations, x402 settlement receipts, attestation delivery). Without this, users get no receipts.

**Steps**:
- Go to → https://resend.com/api-keys
- Click **Create API Key** → name `meok-keystone-prod` → permission: **Full access**
- **Copy** the key (starts with `re_...`) — only shown once
- Verify the sending domain (`meok.ai`):
  - Go to → https://resend.com/domains → **Add Domain** → `meok.ai`
  - Add the 3 DNS records Namecheap shows (SPF, DKIM, DMARC)
  - Wait for "Verified" badge (~5 min)
- **Save the key to the keyring**:
  ```bash
  python3 -c "import keyring; keyring.set_password('meok.ai', 'resend-api-key', 're_...')"
  ```

---

### 5. 🔵 LinkedIn recovery (10 min, ~$X/day ARR via enterprise inbound)

**What it unblocks**: the keystone's LinkedIn page (currently a key part of the `csoai.org` enterprise pipeline — see `meok-hive-architecture-2026-06-07.md`). Inbound from Fortune 500 GRC leads stalled since the page got locked.

**Steps**:
- Go to → https://www.linkedin.com/company/csocai/
- Click **Having trouble?** under the sign-in form
- Use the **email recovery** option; the recovery email is `linkedin@meok.ai`
- If 2FA is on, check the auth app (or SMS — there's a backup number on file)
- **Once in**: change the password to a new strong one, save in 1Password
- **Enable 2FA** (if not already)
- **Post** the 4-P0-build announcement (or schedule it for the morning of EU AI Act 2026-08-02)

---

## Bonus: x402 paywall go-live (gated on Coinbase CDP wallet)

> **2026-06-09 update**: this section is now superseded by §6 above. The
> code is staged on `feat/revenue-rail-testnet`; the wallet-paste is the
> last manual step. Do §6 first; the rest of this bonus section
> (wallet, env, merge PRs, PyPI) applies once the testnet settlement is
> green.

After the 5 above are done, the x402 paywall can go live. This is the second revenue rail.

**What's needed**:
- **Coinbase CDP wallet** for the keystone's receive address
  - Sign up at → https://portal.cdp.coinbase.com/
  - Create a new project, get the **API key** + **secret**
  - Generate a **Base mainnet receiving address** (starts with `0x`); this becomes `X402_PAY_TO`
- **Save the wallet seed/key** to OS keyring (NEVER env, per `CRITICAL_FIXES_2026-06-08.md` Fix #3)
- **Set the env** on the Vercel deploy: `X402_ENABLED=1`, `X402_PAY_TO=0x...`, `X402_NETWORK=eip155:8453`
- **Merge the 5 open x402 PRs** (keystone #5, eu-ai-act #6, dora #2, nis2 #1, cra #1) — all e2e-verified, just waiting on Nick's `gh` auth + branch protection setup
- **Publish bumped PyPI versions** of the 4 flagships that got `@paywalled` shipped (eu-ai-act, dora, nis2, cra) — `python3 -m twine upload dist/*` per repo

---

## Bonus: gh auth for the 28 hive-config repos

The 28 hive-config repos under `CSOAI-ORG/<domain>-hive` are scaffolded locally but unpushed. `gh repo create` × 28 needs Nick's `gh auth login`.

**Steps**:
- `gh auth login` → choose **HTTPS**, **Login with a web browser** → follow the prompts
- Then: `for d in meok ai csoai org proofof ai cobolbridge ai ...; do gh repo create "CSOAI-ORG/${d}-hive" --public --description "..."; done` (the full list is in `scripts/gen-hive.py:DOMAIN_REGISTRY`)

**Push token rule** (per `keyring-token-push-rule`):
- Use `env -u GITHUB_TOKEN -u GH_TOKEN git push` so the keyring token is the only one in scope
- The env `GITHUB_TOKEN` 403s on org-level write

---

## Order of execution (by fastest first-$$)

| # | Action | Time | What you see when done |
|---|---|---|---|
| 1 | **🆕 Revenue rail testnet smoke (§6)** | 30 min | first settled USDC payment on Base Sepolia |
| 2 | Resend (step 4) | 5 min | keystone sends real emails |
| 3 | LinkedIn (step 5) | 10 min | enterprise inbound resumes |
| 4 | Vercel deploys (step 2) | 40 min | `*.vercel.app` URLs live |
| 5 | Stripe Live (step 1) | 2 h | subscriptions billable |
| 6 | Namecheap DNS (step 3) | 1 h | `meok.ai` resolves to Vercel |
| 7 | Coinbase CDP + mainnet x402 (post-§6) | 5 min | per-call monetization live on mainnet |
| 8 | gh auth + 28 repos | 30 min | public hive configs discoverable |
| 9 | Push 41 server.json patches | 30 min | 6-channel MCP marketplace listings go live |

**Total: ~5.5 hours manual** (was 5.5; +30 min for §6, but §6 is the fastest first-$$ and is now unblocked). Do it on a Sunday with coffee; the EU AI Act clock is at T-58 days.

---

## When something breaks

- **Stripe 403 on webhook**: check the signing secret matches in Vercel env. Re-create the endpoint if needed.
- **DNS not propagating**: `dig +short meok.ai A` should return `76.76.21.21` within 30 min. If not, re-check the records in Namecheap.
- **x402 challenge 402/500**: the keystone logs will show whether it's the facilitator URL or the wallet. Default facilitator is `https://x402.org/facilitator` — change via `X402_FACILITATOR_URL` if needed.
- **LinkedIn recovery fails**: the backup contact is in `MEOK_LAUNCH_RUNBOOK.md` G-section.
- **`gh` 403 on push**: see `keyring-token-push-rule.md`. Use `env -u GITHUB_TOKEN -u GH_TOKEN git push`.

---

## Cross-references

- `MASTER_AUDIT_INGESTION.md` — 1-page digest of the SOV3 master audit (companion to this handoff)
- `CRITICAL_FIXES_2026-06-08.md` — the 3 CRITICAL security fixes (Fix #3 gates x402 go-live)
- `MEOK_LAUNCH_RUNBOOK.md` — full 9-workstream plan
- `meok-fleet-monetization-blockers.md` (memory) — source memory for the 5 actions
- `keyring-token-push-rule.md` (memory) — the `env -u GITHUB_TOKEN -u GH_TOKEN` rule
- `mcp-x402-bazaar-micropayments.md` (memory) — x402 state of play (165M tx, $50M+ USDC processed)
- `x402-rollout-state.md` (memory) — 5 open PRs awaiting merge
- `meok-deep-audit-2026-06-08.md` (memory) — the $11K/day ARR-at-risk calc (P0-4)

---

## 6. 🆕 Revenue Rail: x402 testnet → mainnet (~30 min, $0) — staged 2026-06-09

**What it unblocks**: the keystone can boot (was previously broken — `http_server.py:6` did `import server` and the file didn't exist), accept a USDC payment, and settle it on-chain. The first revenue event is a real `Transfer` event on Base Sepolia USDC.

**Where the code lives**: branch `feat/revenue-rail-testnet` at `f2bcc70` (worktree `/tmp/revenue-rail-2026-06-09/`). 6 files:
- `server.py` (new) — 5 keystone tools (3 free + 2 paywalled at $0.05)
- `meok_x402.py` (patched) — adds `_PAID_LOG` + `spending_snapshot`; fixes v1 `PaymentPayload` validation in `paywalled`
- `.env.example` (new) — 5 env vars, testnet default
- `scripts/test_x402_settlement.py` (new) — boot + challenge + real-settlement smoke (with `--print-signer` helper)
- `DEPLOY_REVENUE_RAIL.md` (new) — the 8-step deploy runbook
- `HANDOFF.md` (this file) — updated with §6

**Steps** (in order):

1. **Push the branch** (5 min):
   ```bash
   cd /tmp/revenue-rail-2026-06-09
   env -u GITHUB_TOKEN -u GH_TOKEN git push -u origin feat/revenue-rail-testnet
   ```
   Then open a PR (the body is the commit message).

2. **Deploy to Cloud Run** (15 min, per `GCP_DEPLOY.md` + the env-var overlay in `DEPLOY_REVENUE_RAIL.md` §2a). Two CRITICAL notes:
   - `X402_PAY_TO` and `MEOK_ATTESTATION_KEY` go via `--set-secrets` (not `--set-env-vars`) — the SOV3 audit caught us with CRITICAL #3 if they ever sit in env.
   - Port is 8080, not 8000.

3. **Run the testnet smoke first** (10 min, $0):
   ```bash
   # Get a throwaway testnet key
   /opt/homebrew/bin/python3.11 scripts/test_x402_settlement.py --print-signer
   # → prints TESTNET_ADDRESS + TESTNET_KEY
   ```
   - Fund the address at https://faucet.circle.com (Base Sepolia, USDC, 20 USDC, free, 2h cooldown per pair)
   - Create a Coinbase CDP testnet wallet at https://portal.cdp.coinbase.com (free, no KYC for testnet)
   - Paste both into env, run the smoke **without** `--skip-settle`

4. **Verify on BaseScan Sepolia**: https://sepolia.basescan.org/address/<X402_PAY_TO> should show a 0.05 USDC `Transfer`.

5. **Flip to mainnet** (2 min): `X402_NETWORK=eip155:8453` (was `84532`), redeploy.

**Verify the smoke passed before flipping**: the script exits 0 only if the facilitator actually settled. If it hangs, the facilitator (`https://www.x402.org/facilitator`) is probably timing out — wait 30s and retry, or set `X402_FACILITATOR_URL` to a backup.

**Time + cost**: ~30 min to first settled testnet payment. $0 (testnet USDC is free). ~35 min total to mainnet live billing.

**What this does NOT unblock**: G1 (PyPI cap), G2 (DNS for meok.ai etc.), G6 (directory signups). The keystone deploys via Docker, so G1 is non-blocking for the Docker path. G2 is cosmetic (Cloud Run gives a `*.run.app` URL that works fine for x402). G6 is the next-batch work after this.
