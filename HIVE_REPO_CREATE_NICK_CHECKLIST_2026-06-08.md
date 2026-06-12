# Nick Action Checklist — 28 Hive Repos (`gh repo create`)

> **Date:** 2026-06-08
> **Time required:** ~15 minutes (28 × 5-10s each + push loop)
> **Source:** `DRY_RUN_REPO_CREATE.md` (full dry-run, 108 lines)
> **State on disk:** all 28 repos are git-init'd at `/Users/nicholas/hive-staging/<name>-hive/` with one `chore(geo)` commit on `main`.
> **Account gating:** `gh repo create` uses the keyring token automatically; do NOT set `GITHUB_TOKEN` for this batch. `git push` requires `env -u GITHUB_TOKEN -u GH_TOKEN` per the keyring-token-push-rule.

---

## Step 0 — Verify none already exist (60 seconds)

```bash
for d in meok csoai proofof cobolbridge accountabilityof agisafe asisecurity biasdetectionof dataprivacyof ethicalgovernanceof safetyof transparencyof councilof grabhire muckaway planthire commercialvehicle landlaw fishkeeper koikeeper diyhelp pokerhud loopfactory optimobile socialmediamananger openmoe openMCP meok-compliance-gateway; do
  gh api repos/CSOAI-ORG/${d}-hive --jq '.name // "(free)"' 2>/dev/null || echo "$d-hive: (free)"
done
```

Mark off any that come back as already existing — skip them in the create + push loops.

---

## Step 1 — Create all 28 repos (5 minutes)

Run as a single block. Each command includes the right `--description` and `--homepage` (which become the GitHub repo card and SEO meta). `--enable-issues` on (Discussions off per fleet convention):

```bash
gh repo create CSOAI-ORG/meok-hive --public --description "The customer-facing compliance portal — B2B dashboard, attestation verifier, API-key manager." --homepage https://meok.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/csoai-hive --public --description "The FAA for AI — independent governance institution, multi-jurisdiction crosswalk." --homepage https://csoai.org --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/proofof-hive --public --description "Attestation verification — proofof.ai/v/<cert_id> returns signed compliance evidence." --homepage https://proofof.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/cobolbridge-hive --public --description "COBOL → modern language translator for banks, insurers, government." --homepage https://cobolbridge.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/accountabilityof-hive --public --description "AI incident reporting + tamper-evident audit trail." --homepage https://accountabilityof.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/agisafe-hive --public --description "AGI safety research hub — frontier-model governance." --homepage https://agisafe.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/asisecurity-hive --public --description "AI security for AI systems — defensive, threat-modelling." --homepage https://asisecurity.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/biasdetectionof-hive --public --description "EU AI Act Article 10 — data and model bias detection." --homepage https://biasdetectionof.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/dataprivacyof-hive --public --description "AI-native privacy compliance — GDPR + EU AI Act." --homepage https://dataprivacyof.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/ethicalgovernanceof-hive --public --description "Ethics-first governance — the moral reasoning layer." --homepage https://ethicalgovernanceof.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/safetyof-hive --public --description "Safety monitoring dashboard for deploying enterprises." --homepage https://safetyof.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/transparencyof-hive --public --description "Explainability — what your AI decided and why. The FinServ/Health ticket." --homepage https://transparencyof.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/councilof-hive --public --description "Multi-agent BFT deliberation — board-grade decision-making." --homepage https://councilof.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/grabhire-hive --public --description "UK grab-lorry marketplace + driver recruitment." --homepage https://grabhire.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/muckaway-hive --public --description "UK skip/grab-hire marketplace — 'muck-away' is the UK term." --homepage https://muckaway.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/planthire-hive --public --description "UK plant-hire marketplace — excavators, dumpers, telehandlers." --homepage https://planthire.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/commercialvehicle-hive --public --description "UK commercial fleet optimisation (Samsara/Geotab competitor)." --homepage https://commercialvehicle.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/landlaw-hive --public --description "UK property law tech — conveyancing, leases, planning." --homepage https://landlaw.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/fishkeeper-hive --public --description "Aquarium hobbyist community + care assistant." --homepage https://fishkeeper.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/koikeeper-hive --public --description "Premium koi diagnostics — koi are $1k-50k each; owners pay £199/mo." --homepage https://koikeeper.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/diyhelp-hive --public --description "Home-DIY assistant (FLIP CANDIDATE)." --homepage https://diyhelp.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/pokerhud-hive --public --description "Poker analysis (FLIP — legal grey zone in many jurisdictions)." --homepage https://pokerhud.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/loopfactory-hive --public --description "No-code automation (Zapier competitor, FLIP CANDIDATE)." --homepage https://loopfactory.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/optimobile-hive --public --description "Mobile analytics (FLIP — Firebase/Crashlytics dominate)." --homepage https://optimobile.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/socialmediamananger-hive --public --description "Social media management — DOMAIN HAS TYPO 'mananger' (let expire)." --homepage https://socialmediamananger.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/openmoe-hive --public --description "Base-model layer — OpenMoE-BFT (Opus lane)." --homepage https://openmoe.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/openMCP-hive --public --description "Cross-post CLI + audit engine — feeds the GEO/AEO loop." --homepage https://openMCP --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/meok-compliance-gateway-hive --public --description "Streamable-HTTP gateway + x402 paywall — THIS repo." --homepage https://meok-compliance-gateway --enable-issues --enable-discussions=false
```

If any return "name already exists", drop those from Step 2 (their push loop will fail; check the Step 0 output).

---

## Step 2 — Push the local commits (5 minutes)

Each of the 28 local repos has exactly one commit (`chore(geo): generate llms.txt + JSON-LD landing + sitemap for <name>-hive`). Push `main` to origin:

```bash
for d in /Users/nicholas/hive-staging/*-hive/; do
  name=$(basename "$d")
  cd "$d"
  env -u GITHUB_TOKEN -u GH_TOKEN git remote add origin "git@github.com:CSOAI-ORG/${name}.git" 2>/dev/null
  env -u GITHUB_TOKEN -u GH_TOKEN git push -u origin main
done
```

The `2>/dev/null` on `remote add` is harmless if it's already added (idempotent). If you want to skip the existence check, use `|| true`.

---

## Step 3 — Verify (60 seconds)

```bash
for d in meok csoai proofof cobolbridge accountabilityof agisafe asisecurity biasdetectionof dataprivacyof ethicalgovernanceof safetyof transparencyof councilof grabhire muckaway planthire commercialvehicle landlaw fishkeeper koikeeper diyhelp pokerhud loopfactory optimobile socialmediamananger openmoe openMCP meok-compliance-gateway; do
  url="https://raw.githubusercontent.com/CSOAI-ORG/${d}-hive/main/llms.txt"
  code=$(curl -fsS -o /dev/null -w '%{http_code}' "$url" 2>/dev/null || echo "ERR")
  echo "$d-hive: $code"
done
```

Expected: all 28 return `200` (llms.txt is the file the GEO/AEO generator creates first; if a repo returns 404, the push didn't take).

---

## Step 4 — Trigger the GEO/AEO loop

After all 28 are live:

1. **Regenerate `_cross-links.json`** with the new GitHub URLs as canonical sources:
   ```bash
   python3 /Users/nicholas/meok-compliance-gateway/scripts/gen-geo.py --emit-cross-links \
     --github-base https://github.com/CSOAI-ORG \
     > /Users/nicholas/hive-staging/_cross-links.json
   ```
2. **Commit the regenerated cross-links** back to `/Users/nicholas/hive-staging/_cross-links.json` (or wherever the canonical copy lives).
3. **Re-run the GEO/AEO generator** to pick up the GitHub URLs and re-emit the sitemaps. Each hive gets a one-line commit on its `chore(geo)` branch.

---

## The 28 checkboxes

- [ ] meok-hive (`https://meok.ai`)
- [ ] csoai-hive (`https://csoai.org`)
- [ ] proofof-hive (`https://proofof.ai`)
- [ ] cobolbridge-hive (`https://cobolbridge.ai`)
- [ ] accountabilityof-hive (`https://accountabilityof.ai`)
- [ ] agisafe-hive (`https://agisafe.ai`)
- [ ] asisecurity-hive (`https://asisecurity.ai`)
- [ ] biasdetectionof-hive (`https://biasdetectionof.ai`)
- [ ] dataprivacyof-hive (`https://dataprivacyof.ai`)
- [ ] ethicalgovernanceof-hive (`https://ethicalgovernanceof.ai`)
- [ ] safetyof-hive (`https://safetyof.ai`)
- [ ] transparencyof-hive (`https://transparencyof.ai`)
- [ ] councilof-hive (`https://councilof.ai`)
- [ ] grabhire-hive (`https://grabhire.ai`)
- [ ] muckaway-hive (`https://muckaway.ai`)
- [ ] planthire-hive (`https://planthire.ai`)
- [ ] commercialvehicle-hive (`https://commercialvehicle.ai`)
- [ ] landlaw-hive (`https://landlaw.ai`)
- [ ] fishkeeper-hive (`https://fishkeeper.ai`)
- [ ] koikeeper-hive (`https://koikeeper.ai`)
- [ ] diyhelp-hive (`https://diyhelp.ai`, FLIP CANDIDATE)
- [ ] pokerhud-hive (`https://pokerhud.ai`, FLIP)
- [ ] loopfactory-hive (`https://loopfactory.ai`, FLIP)
- [ ] optimobile-hive (`https://optimobile.ai`, FLIP)
- [ ] socialmediamananger-hive (`https://socialmediamananger.ai`, let expire)
- [ ] openmoe-hive (`https://openmoe.ai`, infra)
- [ ] openMCP-hive (`https://openMCP`, infra)
- [ ] meok-compliance-gateway-hive (`https://meok-compliance-gateway`, infra)

---

## What this is NOT

- **Not** an automatic run. This is a hand-off document; you (`gh` auth holder) execute.
- **Not** including the keystone `meok-compliance-gateway` (already a live repo).
- **Not** including org-level settings (member invites, branch protection, secrets) — those are out of scope for `gh repo create` and ship in the parallel `OpenSSF` branch work.
- **Not** including the 4 MCP Security Cert RFC items (Phase 3-A, separate session).

---

## Cross-references

- `DRY_RUN_REPO_CREATE.md` — the full 108-line dry-run with per-row ordering rationale
- `HIVE_BUILD_DASHBOARD.md` — 28-hive hand-off + 90-min Nick plan
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — phase 0 day -26 mentions "26/26 domains resolve" (this is the repo-create batch that unblocks the DNS step on day -25)
- `MEOK_25_DAY_PLAYBOOK_2026-06-08.md` — phase 0 day -24 mentions "5-channel CVE publication" (separate, but cross-pollinates with the new hive landing pages)
- `FLEET_BASE.md` §3 (this commit, 4bfab80) — the 3 CRITICAL fixes (Docker / secrets / attestation key) that all 28 hives will copy during fleet rollout (Phase 1-3 of the 25-day playbook)
