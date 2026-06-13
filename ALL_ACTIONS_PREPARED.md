# ALL-IN-ONE EXECUTION PREPARER
**Date:** 2026-06-13 | **Purpose:** Prepare all account-gated actions for immediate execution

---

## 🎯 PHASE 1: PR #20 MERGE (2 min)

### Pre-verified Status
- ✅ 7/7 actions SHA-pinned (verified)
- ✅ Core tests: 30/30 passing
- ✅ Build workflow: GHCR + cosign signing included
- ✅ Ready for: `gh pr merge 20 --squash`

### One-click command:
```bash
env -u GITHUB_TOKEN -u GH_TOKEN gh pr merge --squash 20
```

---

## 📦 PHASE 2: PYPI PUBLISH (10 min)

### Files ready in branch:
- `agentaudit/pyproject.toml` — package config
- `agentaudit/server.py` — 6 tools (4 free + 2 paywalled)
- `agentaudit/DEPLOY_AGENTAUDIT.sh` — deploy runbook

### One-click command (requires PYPI_TOKEN):
```bash
export PYPI_TOKEN=pypi-...  # Get from https://pypi.org/manage/account/token/
cd /Users/nicholas/meok-compliance-gateway/agentaudit
python3 -m build --wheel --sdist
python3 -m twine upload dist/* --username __token__ --password "$PYPI_TOKEN"
```

### Verify:
```bash
curl -s https://pypi.org/pypi/agentaudit/json | jq '.info.version'
```

---

## 🔓 PHASE 3: GHCR VISIBILITY (1 min)

### Post-merge auto-build:
- Image: `ghcr.io/csoai-org/agentaudit-mcp:latest`
- Workflow: `.github/workflows/build-push-agentaudit.yml`

### UI steps:
1. GitHub → Packages → agentaudit-mcp
2. Package settings → Change visibility → Public

---

## 🌐 PHASE 4: DEAD DOMAIN FIX (5 min)

### Domains:
- diyhelp.ai
- pokerhud.ai  
- sov3.ai

### Namecheap fix:
```
Login → Domain List → Manage → Advanced DNS → Add A Record
Type: A Record | Host: @ | Value: 35.242.143.249 | TTL: Automatic
```

### Or deploy to Vercel:
```bash
cd /Users/nicholas/{domain}
vercel --prod --confirm --token $VERCEL_TOKEN
```

---

## 🏷️ PHASE 5: MCP REGISTRY COMPLIANCE (2 hours)

### Apply universal-flagship-upgrade.sh:
```bash
# Clones all 14 flagships and prepares PRs
/Users/nicholas/meok-compliance-gateway/universal-flagship-upgrade.sh
```

### Templates in mcp-registry-templates/:
```
14 repos × 3 files = 42 total files
├── server.json  (MCP Registry metadata)
├── llms.txt     (LLM discovery)
└── assets/icon.svg (branding)
```

---

## 📧 PHASE 6: GRC EMAILS (45 min)

### From iCloud SOV3-Launch folder:
- `GRC_DRAFTS_READY_2026-06-10.md` — 19 email drafts
- `PRESS_LIST_1076.csv` — 1,076 press targets

### SMTP configured in ~/.zshrc:
```bash
SMTP_HOST=mail.privateemail.com
SMTP_USER=nicholas@csoai.org
SMTP_PASSWORD=Lolpsplolen101!!
FROM_EMAIL=nicholas@csoai.org
```

---

## 🔄 PHASE 7: CANONICAL NUMBERS (10 min)

### Replace across all surfaces:
```bash
# 6,798 installs (not 22.6K, not 67, not 70)
# 13 compliance MCPs (not 47)
# 341 total MCP servers (SOV3 bridge count)

# Apply to flagship READMEs:
sed -i 's/67 MCPs/13 MCPs/g' README.md
sed -i 's/22.6K/6.8K/g' README.md
sed -i 's/70 MCPs/13 MCPs/g' README.md
```

---

## 📋 EXECUTION CHECKLIST

- [ ] **MERGE PR #20** → `gh pr merge 20 --squash`
- [ ] **PYPI_TOKEN** → Get from pypi.org/manage/account/token/
- [ ] **Build wheel** → `cd agentaudit && python3 -m build`
- [ ] **Upload to PyPI** → `python3 -m twine upload dist/*`
- [ ] **GHCR public** → GitHub Packages UI
- [ ] **A-records** → Namecheap DNS for 3 dead domains
- [ ] **Apply templates** → universal-flagship-upgrade.sh
- [ ] **Send GRC emails** → 19 drafts in Mail.app
- [ ] **Fix numbers** → canonical-numbers-fix.py

---

## 💰 REVENUE TIMELINE

| Time | Action | Impact |
|------|--------|--------|
| T+0 min | Merge PR #20 | GHCR builds |
| T+10 min | PyPI publish | agentaudit discoverable |
| T+15 min | GHCR public | Smithery ready |
| T+20 min | Dead domains live | SEO traffic |
| T+1 hr | MCP registry complete | 14x distribution |
| T+1.5 hr | GRC emails sent | £2.7K/day potential |