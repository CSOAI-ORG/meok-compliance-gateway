# Dry-Run: 28 `gh repo create` commands for CSOAI-ORG

> **Account-gated. Do not execute without Nick's explicit go.**
> Per [[agentaudit-concurrent-session-hazards]] + [[keyring-token-push-rule]].

**Org:** `CSOAI-ORG`
**Default visibility:** `--public` (all 28 repos are open-source per [[meok-hive-architecture-2026-06-07]]). The keystone (`meok-compliance-gateway`) is **already live** and is excluded from this batch.
**Source path:** `/Users/nicholas/hive-staging/<repo>/` (already committed locally with 10 hive-config files + 3 GEO/AEO files = 13 files each)

## Build-slot ordering (per `HIVE_BUILD_DASHBOARD.md`)

| # | Domain | Tier | Local repo | Head SHA | Visibility | Description |
|---|--------|------|------------|----------|------------|-------------|
| 1 | `meok.ai` | flagship | `meok-hive` | TBD | public | "The customer-facing compliance portal — B2B dashboard, attestation verifier, API-key manager." |
| 2 | `csoai.org` | flagship | `csoai-hive` | TBD | public | "The FAA for AI — independent governance institution, multi-jurisdiction crosswalk." |
| 3 | `proofof.ai` | flagship | `proofof-hive` | TBD | public | "Attestation verification — `proofof.ai/v/<cert_id>` returns signed compliance evidence." |
| 4 | `cobolbridge.ai` | flagship | `cobolbridge-hive` | TBD | public | "COBOL → modern language translator for banks, insurers, government." |
| 5 | `accountabilityof.ai` | governance | `accountabilityof-hive` | TBD | public | "AI incident reporting + tamper-evident audit trail." |
| 6 | `agisafe.ai` | governance | `agisafe-hive` | TBD | public | "AGI safety research hub — frontier-model governance." |
| 7 | `asisecurity.ai` | governance | `asisecurity-hive` | TBD | public | "AI security for AI systems — defensive, threat-modelling." |
| 8 | `biasdetectionof.ai` | governance | `biasdetectionof-hive` | TBD | public | "EU AI Act Article 10 — data and model bias detection." |
| 9 | `dataprivacyof.ai` | governance | `dataprivacyof-hive` | TBD | public | "AI-native privacy compliance — GDPR + EU AI Act." |
| 10 | `ethicalgovernanceof.ai` | governance | `ethicalgovernanceof-hive` | TBD | public | "Ethics-first governance — the moral reasoning layer." |
| 11 | `safetyof.ai` | governance | `safetyof-hive` | TBD | public | "Safety monitoring dashboard for deploying enterprises." |
| 12 | `transparencyof.ai` | governance | `transparencyof-hive` | TBD | public | "Explainability — what your AI decided and why. The FinServ/Health ticket." |
| 13 | `councilof.ai` | governance | `councilof-hive` | TBD | public | "Multi-agent BFT deliberation — board-grade decision-making." |
| 14 | `grabhire.ai` | uk_construction | `grabhire-hive` | TBD | public | "UK grab-lorry marketplace + driver recruitment." |
| 15 | `muckaway.ai` | uk_construction | `muckaway-hive` | TBD | public | "UK skip/grab-hire marketplace — 'muck-away' is the UK term." |
| 16 | `planthire.ai` | uk_construction | `planthire-hive` | TBD | public | "UK plant-hire marketplace — excavators, dumpers, telehandlers." |
| 17 | `commercialvehicle.ai` | uk_construction | `commercialvehicle-hive` | TBD | public | "UK commercial fleet optimisation (Samsara/Geotab competitor)." |
| 18 | `landlaw.ai` | vertical_saas | `landlaw-hive` | TBD | public | "UK property law tech — conveyancing, leases, planning." |
| 19 | `fishkeeper.ai` | vertical_saas | `fishkeeper-hive` | TBD | public | "Aquarium hobbyist community + care assistant." |
| 20 | `koikeeper.ai` | vertical_saas | `koikeeper-hive` | TBD | public | "Premium koi diagnostics — koi are $1k-50k each; owners pay £199/mo." |
| 21 | `diyhelp.ai` | flip | `diyhelp-hive` | TBD | public | "Home-DIY assistant (FLIP CANDIDATE)." |
| 22 | `pokerhud.ai` | flip | `pokerhud-hive` | TBD | public | "Poker analysis (FLIP — legal grey zone in many jurisdictions)." |
| 23 | `loopfactory.ai` | flip | `loopfactory-hive` | TBD | public | "No-code automation (Zapier competitor, FLIP CANDIDATE)." |
| 24 | `optimobile.ai` | flip | `optimobile-hive` | TBD | public | "Mobile analytics (FLIP — Firebase/Crashlytics dominate)." |
| 25 | `socialmediamananger.ai` | expire | `socialmediamananger-hive` | TBD | public | "Social media management — DOMAIN HAS TYPO 'mananger' (let expire)." |
| 26 | `openmoe.ai` | infra | `openmoe-hive` | TBD | public | "Base-model layer — OpenMoE-BFT (Opus lane)." |
| 27 | `openMCP` | infra | `openMCP-hive` | TBD | public | "Cross-post CLI + audit engine — feeds the GEO/AEO loop." |
| 28 | `meok-compliance-gateway` | infra | `meok-compliance-gateway-hive` | TBD | public | "Streamable-HTTP gateway + x402 paywall — THIS repo." |

## The 28 commands (exact, dry-run only)

```bash
gh repo create CSOAI-ORG/meok-hive --public --description "The customer-facing compliance portal — B2B dashboard, attestation verifier, API-key manager." --homepage https://meok.ai --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/csoai-hive --public --description "The FAA for AI — independent governance institution, multi-jurisdiction crosswalk." --homepage https://csoai.org --enable-issues --enable-discussions=false
gh repo create CSOAI-ORG/proofof-hive --public --description "Attestation verification — `proofof.ai/v/<cert_id>` returns signed compliance evidence." --homepage https://proofof.ai --enable-issues --enable-discussions=false
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

## What Nick does after this

1. Review the 28 commands above. Flag any domain that should be `--private` (none expected; all 28 are open-source per architecture).
2. Run the block. (`env -u GITHUB_TOKEN -u GH_TOKEN` is NOT needed for `gh repo create` — the `gh` CLI uses the keyring token automatically when `GITHUB_TOKEN` is not set.)
3. For each created repo, push the local commit:
   ```bash
   for d in /Users/nicholas/hive-staging/*-hive/; do
     name=$(basename "$d")
     cd "$d"
     env -u GITHUB_TOKEN -u GH_TOKEN git remote add origin "git@github.com:CSOAI-ORG/${name}.git"
     env -u GITHUB_TOKEN -u GH_TOKEN git push -u origin main
   done
   ```
4. The `.github/dependabot.yml` + `.github/workflows/codeql.yml` ship in the initial commit (already in each repo). cosign + fuzz fixes ship in the 4 OpenSSF branches (Phase B of the keystone plan; already done — just needs merge).
5. After all 28 push, the live `/.well-known/agent-card.json` and `/llms.txt` start serving once DNS points at the Vercel deploys (Nick-only step).

## What this is NOT

- **Not** an automatic run. This is a hand-off document.
- **Not** including the keystone `meok-compliance-gateway` (already a live repo under `CSOAI-ORG` per the user's own session history; entry #28 in the registry above is its `-hive` shadow copy at `meok-compliance-gateway-hive/`, also already shipped via the keystone push).
- **Not** including org-level settings (member invites, branch protection, secrets) — those are out of scope for `gh repo create`.

## Verification before Nick runs

```bash
# Confirm no repo with these names already exists
for d in meok csoai proofof cobolbridge accountabilityof agisafe asisecurity biasdetectionof dataprivacyof ethicalgovernanceof safetyof transparencyof councilof grabhire muckaway planthire commercialvehicle landlaw fishkeeper koikeeper diyhelp pokerhud loopfactory optimobile socialmediamananger; do
  gh api repos/CSOAI-ORG/${d}-hive --jq '.name // "(free)"' 2>/dev/null || echo "$d-hive: (free)"
done
```

If any come back with a name, those are already created — skip them in the batch.
