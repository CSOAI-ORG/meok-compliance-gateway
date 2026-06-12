# MEOK Hive Build Dashboard

> **28 autonomous hive-config repos, scaffolded 2026-06-07, awaiting Nick-side
> hand-off (org repo creation + push).**
>
> Each hive is a self-contained 7-layer stack (mex → Memoria → Cognee →
> agentmemory → domain-MCP → Hermes → Open Design). All files generated
> from a single source: [`scripts/gen-hive.py`](scripts/gen-hive.py).
>
> Source of truth: [`meok-hive-architecture-2026-06-07`](
> ../../.claude/projects/-Users-nicholas-meok-compliance-gateway/memory/
> meok-hive-architecture-2026-06-07.md)

## Build slot (per [[meok-hive-architecture-2026-06-07]])

| Slot | Days | Tier | Count | Domains |
|---|---|---|---|---|
| 1 | 1–7 | Flagship | 4 | meok.ai, csoai.org, proofof.ai, cobolbridge.ai |
| 2 | 8–21 | Governance | 9 | accountabilityof, agisafe, asisecurity, biasdetectionof, dataprivacyof, ethicalgovernanceof, safetyof, transparencyof, councilof |
| 3 | 22–35 | UK construction | 4 | grabhire, muckaway, planthire, commercialvehicle |
| 4 | 36–49 | Vertical SaaS | 3 | landlaw, fishkeeper, koikeeeper |
| 5 | 50–60 | Flip/expire | 5 | diyhelp, pokerhud, loopfactory, optimobile, socialmediamananger |
| — | — | **Infra (already live)** | 3 | openmoe.ai, openMCP, meok-compliance-gateway (this repo) |

**Total: 28 hive-config repos.** 25 customer-facing + 3 infrastructure.

## File-level summary (10 files per hive)

```
<hive>-hive/
├── README.md           # human + AGENT entry point
├── stack.yml           # 7-layer config (canonical truth)
├── DESIGN.md           # Open Design palette (L7)
├── agent-card.json     # A2A Agent Card (L5)
├── hermes.yml          # L6 orchestrator config
├── agentmemory.json    # L4 memory scope
├── .mex/mex.yml        # L1 drift detection
├── spawn.py            # EvoAgentX bootstrap
├── .gitignore          # Python + hive artefacts
└── LICENSE             # MIT
```

**Validation status:** 28/28 hives pass — JSON parses, YAML parses, Python compiles.

## All 28 hives (sorted by build slot)

| # | Hive | Tier | Local path | Head SHA | Build slot |
|---|---|---|---|---|---|
| 1 | **meok.ai** | flagship | `/Users/nicholas/hive-staging/meok-hive` | `9da8e0a` | Days 1–7 |
| 2 | **csoai.org** | flagship | `/Users/nicholas/hive-staging/csoai-hive` | `0f66620` | Days 1–7 |
| 3 | **proofof.ai** | flagship | `/Users/nicholas/hive-staging/proofof-hive` | `766b286` | Days 1–7 |
| 4 | **cobolbridge.ai** | flagship | `/Users/nicholas/hive-staging/cobolbridge-hive` | `a6c4d98` | Days 1–7 |
| 5 | accountabilityof.ai | governance | `/Users/nicholas/hive-staging/accountabilityof-hive` | `a60b7da` | Days 8–21 |
| 6 | agisafe.ai | governance | `/Users/nicholas/hive-staging/agisafe-hive` | `46696cb` | Days 8–21 |
| 7 | asisecurity.ai | governance | `/Users/nicholas/hive-staging/asisecurity-hive` | `811accc` | Days 8–21 |
| 8 | biasdetectionof.ai | governance | `/Users/nicholas/hive-staging/biasdetectionof-hive` | `9b3b682` | Days 8–21 |
| 9 | dataprivacyof.ai | governance | `/Users/nicholas/hive-staging/dataprivacyof-hive` | `db10185` | Days 8–21 |
| 10 | ethicalgovernanceof.ai | governance | `/Users/nicholas/hive-staging/ethicalgovernanceof-hive` | `c764928` | Days 8–21 |
| 11 | safetyof.ai | governance | `/Users/nicholas/hive-staging/safetyof-hive` | `8ca9299` | Days 8–21 |
| 12 | transparencyof.ai | governance | `/Users/nicholas/hive-staging/transparencyof-hive` | `5c11d5f` | Days 8–21 |
| 13 | councilof.ai | governance | `/Users/nicholas/hive-staging/councilof-hive` | `44241f3` | Days 8–21 |
| 14 | grabhire.ai | uk_construction | `/Users/nicholas/hive-staging/grabhire-hive` | `8dd07dd` | Days 22–35 |
| 15 | muckaway.ai | uk_construction | `/Users/nicholas/hive-staging/muckaway-hive` | `0b667d1` | Days 22–35 |
| 16 | planthire.ai | uk_construction | `/Users/nicholas/hive-staging/planthire-hive` | `e1193df` | Days 22–35 |
| 17 | commercialvehicle.ai | uk_construction | `/Users/nicholas/hive-staging/commercialvehicle-hive` | `63975c4` | Days 22–35 |
| 18 | landlaw.ai | vertical_saas | `/Users/nicholas/hive-staging/landlaw-hive` | `7d341d7` | Days 36–49 |
| 19 | fishkeeper.ai | vertical_saas | `/Users/nicholas/hive-staging/fishkeeper-hive` | `9905402` | Days 36–49 |
| 20 | koikeeper.ai | vertical_saas | `/Users/nicholas/hive-staging/koikeeper-hive` | `9323598` | Days 36–49 |
| 21 | diyhelp.ai | flip | `/Users/nicholas/hive-staging/diyhelp-hive` | `bb15291` | Days 50–60 |
| 22 | pokerhud.ai | flip | `/Users/nicholas/hive-staging/pokerhud-hive` | `845729c` | Days 50–60 |
| 23 | loopfactory.ai | flip | `/Users/nicholas/hive-staging/loopfactory-hive` | `917d0a8` | Days 50–60 |
| 24 | optimobile.ai | flip | `/Users/nicholas/hive-staging/optimobile-hive` | `00c549a` | Days 50–60 |
| 25 | socialmediamananger.ai | expire | `/Users/nicholas/hive-staging/socialmediamananger-hive` | `a424ace` | Days 50–60 |
| 26 | openmoe.ai | infra | `/Users/nicholas/hive-staging/openmoe-hive` | `51df57f` | already live |
| 27 | openMCP | infra | `/Users/nicholas/hive-staging/openMCP-hive` | `933354c` | already live |
| 28 | meok-compliance-gateway | infra | `/Users/nicholas/hive-staging/meok-compliance-gateway-hive` | `8e2b925` | already live (this repo) |

## What Nick needs to do (one-time, ~30 min total)

For each of the 28 hives, three org-gated steps:

1. **Create the org repo:**
   ```bash
   gh repo create CSOAI-ORG/<hive>-hive --public --description "MEOK 7-layer autonomous hive for <domain>"
   ```
   The `<hive>-hive` name comes from the `repo:` field in each `stack.yml`.

2. **Add the remote and push:**
   ```bash
   cd /Users/nicholas/hive-staging/<hive>-hive
   env -u GITHUB_TOKEN -u GH_TOKEN git remote add origin git@github.com:CSOAI-ORG/<hive>-hive.git
   env -u GITHUB_TOKEN -u GH_TOKEN git push -u origin main
   ```
   Per [[keyring-token-push-rule]] — env GITHUB_TOKEN 403s on new repos.

3. **Add the OpenSSF Scorecard fixes** (Dependabot + CodeQL + cosign + fuzz) — pattern shipped in keystone (commit `912ceef` etc.) per [[openssf-scorecard-remediation-2026-06-06]]. Branches already pushed in OpenSSF Phase A/B/C.

**Helper to enumerate all 28 (paste into a session):**
```bash
for d in /Users/nicholas/hive-staging/*/; do
  name=$(basename "$d")
  echo "  $name"
done
```

## What these hives unlock

- **Cross-hive A2A mesh** — 28 Agent Cards at `https://<domain>/.well-known/agent-card.json`
- **x402 micro-settlement** — 4-way split on every cross-hive call
- **Councilof.ai audit** — every cross-hive Memoria commit gets a quorum certificate
- **Proofof.ai attestation** — every hive output is signed + verifiable
- **GEO/AEO 28-way blast** — 28 landing pages with structured data, cross-linked
- **OpenSSF fleet mean 7.0+** — after the 4 keystone fixes ship on each

## Per-hive specifics (drawn from DOMAINS.md)

| Hive | OpenSSF projected | x402 $/call | Memory | Anchor MCP | Revenue path |
|---|---|---|---|---|---|
| meok.ai | 7.5/10 → green | 0.05 | shared | meok-attestation-api | Stripe self-serve + per-attestation |
| csoai.org | 7.5/10 → green | 1.50 | shared | csoai-governance-crosswalk-mcp | £1,499/mo Enterprise suite |
| proofof.ai | 7.5/10 → green | 5.00 | shared | meok-attestation-api | £5/attestation lookup |
| cobolbridge.ai | 7.5/10 → green | 2.00 | isolated | cobol-bridge-mcp | £199/mo Pro + £290k/enterprise |
| accountabilityof.ai | 7.0/10 | 0.50 | shared | ai-incident-reporting-mcp | Bundle under csoai.org |
| agisafe.ai | 7.0/10 | free (100/day) | shared | care-membrane-mcp | Research hub; or flip for $10-25k |
| asisecurity.ai | 7.0/10 | 0.30 | shared | cybersecurity-ai-mcp | Bundle under csoai.org |
| biasdetectionof.ai | 7.0/10 | 0.10 | shared | bias-detection-mcp | £299/mo (cheapest single-MCP SaaS) |
| dataprivacyof.ai | 7.0/10 | 0.20 | isolated | gdpr-compliance-ai-mcp | GDPR + EU AI Act package |
| ethicalgovernanceof.ai | 7.0/10 | free (5/day) | shared | meok-governance-engine-mcp | Redirect to csoai.org |
| safetyof.ai | 7.0/10 | 0.40 | shared | care-membrane-mcp | Landing → csoai.org suite |
| transparencyof.ai | 7.0/10 | 0.75 | shared | explainability-report-mcp | £399-£1,499/mo (FinServ/Health) |
| councilof.ai | 7.0/10 | 1.00 | shared | agent-orchestrator-mcp | Audits every cross-hive commit |
| grabhire.ai | 7.0/10 | 0.05 | shared | recruitment-ai-mcp | UK marketplace fees |
| muckaway.ai | 7.0/10 | 0.05 | shared | muckaway-ai-mcp | 5-10% marketplace |
| planthire.ai | 7.0/10 | 0.10 | shared | planthire-ai-mcp | 8-15% marketplace fees |
| commercialvehicle.ai | 7.0/10 | 0.15 | shared | logistics-ai-mcp | Cluster with grabhire/muckaway |
| landlaw.ai | 7.0/10 | 0.50 | isolated | landlaw-ai-mcp | £199/mo solo → £999/mo firm |
| fishkeeper.ai | 7.0/10 | free (100/day) | shared | fishkeeper-ai-mcp | £4.99-19.99/mo consumer |
| koikeeper.ai | 7.0/10 | 1.00 | isolated | fishkeeper-ai-mcp + k25-vision | £199/mo premium tier |
| diyhelp.ai | 7.0/10 | free (100/day) | shared | (none) | FLIP candidate |
| pokerhud.ai | 7.0/10 | free | shared | (none) | FLIP (legal grey) |
| loopfactory.ai | 7.0/10 | free (10/day) | shared | cron-ai-mcp | FLIP / defer |
| optimobile.ai | 7.0/10 | free (10/day) | shared | (none) | FLIP (Firebase competition) |
| socialmediamananger.ai | 7.0/10 | free | shared | (none) | **Let expire** (typo) |
| openmoe.ai | 7.0/10 | 0.01 | shared | openmoe-bft + openMCP | Per-call BFT inference |
| openMCP | 7.0/10 | free (5/day) | shared | openMCP | Free/OSS — drives traffic |
| meok-compliance-gateway | 7.0/10 | 0.05 | isolated | meok-compliance-gateway | x402 4-way split |

## What's still on the user's plate (Nick-gated)

| Action | Approx time | Why Nick-only |
|---|---|---|
| 28× `gh repo create` | ~15 min | org-admin |
| 28× `git remote add + push` | ~10 min | needs keyring token (not env token) |
| DNS flip for live `/.well-known/agent-card.json` | ~5 min | Namecheap admin |
| Vercel deploys for hive landing pages | ~30 min | account login |
| x402 wallet wiring per hive | ~30 min | Coinbase CDP key |

**Total: ~90 min of Nick time** to take all 28 from local-stage to live-stage.

## What's on the agent's plate (can be scripted)

| Task | Status | Notes |
|---|---|---|
| Define 7-file template | ✅ done | [`scripts/gen-hive.py`](scripts/gen-hive.py) |
| Build the per-hive config generator | ✅ done | idempotent, parametrized |
| Generate all 28 hive configs | ✅ done | 28/28 validated |
| Init 28 git repos + commit | ✅ done | 28/28 committed locally |
| Write the build dashboard | ✅ done | this file |
| Per-hive OpenSSF rollout | ⏳ partial | keystone done; fleet follows Nick's push |
| A2A Agent Card verification | ⏳ pending | needs live deploy |
| Cognee subgraph provisioning | ⏳ pending | needs Neo4j instance per tier |
| Memoria namespace provisioning | ⏳ pending | needs Rust binary on a host |
| Open Design `od/DESIGN.md` per hive | ✅ done | (in each hive, ready for nexu-io sync) |
| Hermes sub-context registration | ⏳ pending | needs Hermes dev cloud |
| EvoAgentX HITL proposal runs | ⏳ pending | needs `pip install evoagentx` then `python spawn.py` per hive |

## Re-running the generator

```bash
# All 28
python3 /Users/nicholas/meok-compliance-gateway/scripts/gen-hive.py

# One custom domain
python3 /Users/nicholas/meok-compliance-gateway/scripts/gen-hive.py mynewdomain.ai \\
    --tier flagship \\
    --tools my-mcp,another-mcp \\
    --palette "fuchsia + obsidian" \\
    --out /Users/nicholas/hive-staging

# List the 28 registered
python3 /Users/nicholas/meok-compliance-gateway/scripts/gen-hive.py --list
```

Idempotent — re-running overwrites files. Git history of each hive is independent.

## Related

- [`meok-hive-architecture-2026-06-07`](../../.claude/projects/-Users-nicholas-meok-compliance-gateway/memory/meok-hive-architecture-2026-06-07.md) — the 7-layer design + inter-hive protocols
- [`meok-global-strategy-2026-06-07`](../../.claude/projects/-Users-nicholas-meok-compliance-gateway/memory/meok-global-strategy-2026-06-07.md) — 7 global moves (Proxima, mex, Robinhood-clone, Higgsfield, EU AI Act wedge, WiFi-CSI farm, PQC audit)
- [`meok-crown-jewels-2026-06-07`](../../.claude/projects/-Users-nicholas-meok-compliance-gateway/memory/meok-crown-jewels-2026-06-07.md) — 11 verified open-source weapons mapped to the 7 layers
- [`/Users/nicholas/clawd/_TOPOLOGY/DOMAINS.md`](/Users/nicholas/clawd/_TOPOLOGY/DOMAINS.md) — source of truth for the 25-domain portfolio
- [`FLEET_BASE.md`](FLEET_BASE.md) — canonical MCP template (the L5 layer is the thin wrapper per hive)
- [[MEOK Launch Runbook]] — 9-workstream, 6-gate register
- [[openmoe-ai-project]] — Opus-owned, infra hive #26
- [[keyring-token-push-rule]] — `env -u GITHUB_TOKEN -u GH_TOKEN git push` for CSOAI-ORG
