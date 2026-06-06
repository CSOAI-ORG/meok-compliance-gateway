# AGENTS.md — ground rules for AI agents in this repo

Multiple agent TUIs (Claude Code sessions, ollama/minimax agents, etc.) work this
repo **concurrently on the same checkout**. These rules exist because real
collisions happened: files rewritten mid-edit, branches switched under another
session, duplicate work. Follow them exactly.

## Coordination (the important part)

1. **Before editing anything**: run `git branch --show-current` and `git status`.
   If the branch isn't the one you chose, another session moved it — re-checkout
   your own branch; never assume the tree is as you left it.
2. **One branch per task, PRs only.** Never commit directly to `main`.
   Branch naming: `feat/…`, `chore/…`, `fix/…`. If your work extends an open PR,
   push to that PR's branch; otherwise make a new branch.
3. **Re-read any file immediately before writing it** (a write that fails with
   "modified since read" means another session touched it — reconcile, don't force).
4. **Claim work in the session memory** (`~/.claude/projects/-Users-nicholas-meok-compliance-gateway/memory/MEMORY.md`)
   — one line: what you're doing + branch. Check it for other sessions' claims first.
5. **Account-gated actions are Nick-only**: merging PRs, PyPI publish, GHCR/package
   visibility, wallets (Coinbase CDP), Smithery/AWS/Docker logins, any spending.
   Stage the work; leave the gate to him.

## Hard environment hazards

- **Never touch `~/.meok/`** — live usage counters + PAYG balances for production
  daemons on this machine. Tests MUST run under a temp `HOME` (see the flagships'
  `conftest.py` pattern). Local tool calls burn the real anonymous daily quota.
- **`/tmp` is volatile** — venvs/clones there vanish between days. Recreate, don't assume.
- Two `gh` tokens exist: env `GITHUB_TOKEN` (can push, cannot create PRs) and the
  keyring token (full). For PR create/view: `env -u GITHUB_TOKEN -u GH_TOKEN gh …`.

## Project conventions

- **Pinning**: the gateway pins exact (`requirements-gateway.txt`: `mcp==`,
  `uvicorn==`); flagship packages pin loose (`mcp>=1.0.0`). Never bump `mcp`
  without a fleet-sync plan — `http_server.py` and `meok_x402.py` import
  version-sensitive APIs (verified set: mcp 1.27.2).
- **x402 paid tools** (`meok_x402.py`): OFF unless `X402_ENABLED=1`. Challenge is
  x402-over-MCP (`_meta["x402/payment"]` / ToolError JSON), never HTTP 402. Paid
  tools carry `COST WARNING:` in their description (AWS billable-tool convention).
  Keep funnel tools (quick_scan/deadline_check-class) free.
- **Tests**: pytest, hermetic (temp HOME), no duplicate `test_*.py` basenames
  across root and `tests/` (corrupts pytest imports).
- **Fleet pattern**: `FLEET_BASE.md` is the canonical template for all ~290
  flagship repos. Improve the template, then fleet-sync; don't hand-patch repos
  divergently.
- **Deadlines that gate decisions**: MCP spec freeze 2026-07-28 (gateway cutover
  target 2026-07-14); EU AI Act full enforcement 2026-08-02.

## Current open work (update this list when it changes)

- PR board (all x402): gateway #5, eu-ai-act #6, dora #2, nis2 #1, cra #1 —
  green + CLEAN, awaiting Nick's review. Do not merge.
- Backlog: MCP 2026-07-28 stateless migration spike; `.well-known` Server Cards;
  GHCR `eu-ai-act-mcp` visibility flip (Nick, UI-only).
