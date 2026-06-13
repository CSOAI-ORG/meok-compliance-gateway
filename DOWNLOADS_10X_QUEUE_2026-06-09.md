# 10x Downloads — Nick's Publish Queue (2026-06-09)

Everything below is **built, validated, and smoke-tested**. Each step is one
command or one paste. Nothing here was published/submitted automatically —
it's all queued for you because it needs your PyPI token / registry accounts.

Baseline reality: only `openmcp` is currently on PyPI; revenue rail is $0/testnet.
"10x from ~zero" = **shipping what's already built**, in this order.

---

## ① PyPI publish — the #1 download lever (≈5 min)

Wheels are built + `twine check`-PASSED + installed-clean-in-a-fresh-venv
(import OK, entry points present). Names confirmed free on PyPI.

```bash
# one-time: export your PyPI token (or put it in ~/.pypirc)
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-XXXXXXXX   # your real token

# agentaudit — the compliance product (import OK, agentaudit-server entry point OK)
twine upload /Users/nicholas/clawd/meok-compliance-gateway/agentaudit/dist/agentaudit-0.1.0*

# meok-cross-post — the distribution CLI (entry points: meok-cross-post, openmcp)
twine upload /Users/nicholas/meok-cross-post/dist/meok_cross_post-0.1.0*
```

Verify after:
```bash
pip install agentaudit meok-cross-post   # should now resolve
```

> **agentaudit README upgraded** for the PyPI page: now leads with
> `pip install agentaudit`, internal "Empire" jargon scrubbed, HTTP-gateway
> instructions corrected (it's not in the wheel). Wheel rebuilt + re-checked.

**🚫 DO NOT PUBLISH `meok` — it's broken, not just README-less.** Its
`pyproject.toml` has `[tool.setuptools.packages] find = {where = ["ui"], ...}`,
so the wheel ships **zero modules** — `pip install meok && python -c "import meok"`
**fails with ModuleNotFoundError**. Publishing it would burn the name on a
dead package. Fix the package-discovery config (point it at the `meok/` package,
not `ui/`), rebuild, and re-test `import meok` before ever uploading.

---

## ② MCP registry submissions — the discovery lever

176 payloads generated for **44 repos × 4 channels** in
`dist/distribution/` (+ `SUBMISSION_CHECKLIST.md`). This is where agents
*find* MCP servers. Ranked by download impact:

| Priority | Channel | Action | Effort |
|---|---|---|---|
| **1** | **Smithery** (2.8K tools) | **Batched for you:** `SUBMIT=1 LIMIT=3 ./scripts/submit-smithery-batch.sh` (smoke-test 3), then drop `LIMIT` for all 44. Dry-run by default. | ~5 min to fire |
| **2** | **Glama** (32K servers) | Sign in → Submit → paste `dist/distribution/glama/<repo>.json` | ~88 min |
| **3** | **MCP.so** (22K servers) | https://mcp.so/submit → paste `dist/distribution/mcpso/<repo>.json` | ~44 min |
| **4** | **PulseMCP** (editorial) | email `dist/distribution/pulse/<repo>.md` to editors@pulsemcp.com | fast send, 1-2wk review |

> I can drive the Glama/MCP.so browser submissions for you via the
> `kimi-webbridge` skill (it uses your logged-in browser) — just say the word
> and confirm you want me submitting to external sites on your behalf.

---

## ③ PR #20 CI fix — repo health (not on the download path)

The fix is **done and pushed**: branch `fix/pr20-ci-install-x402`
(commit `d64f21b` — adds `pip install 'agentaudit[x402,dev]'` to
`agentaudit-ci.yml`). BUT PR #20 itself is **`CONFLICTING`** and its head is a
*different* branch (`feat/agentaudit-stage6-from-server`). To land it:

```bash
# option A: open a fresh PR from the fix branch (simplest)
gh pr create --repo CSOAI-ORG/meok-compliance-gateway \
  --head fix/pr20-ci-install-x402 --base main \
  --title "ci(agentaudit): install x402 extra (fixes PR #20 red CI)"
# then resolve the merge conflict the PR flags, and merge.
```
Publishing agentaudit to PyPI (step ①) does **not** depend on this.

---

## What I did this session (all local / reversible, nothing published)
- Built + validated + venv-smoke-tested agentaudit & meok-cross-post wheels
- Built meok wheel (held — needs README)
- Generated 176 registry payloads (44×4)
- Pushed `fix/pr20-ci-install-x402`
- Pushed `.env` hygiene to optimobile-practice-hub; safetyofai gitignore commit
  is local (its `.env.production` was never on remote — divergent commit `e500a01`
  there needs your reconciliation)
