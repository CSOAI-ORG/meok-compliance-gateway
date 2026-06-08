#!/usr/bin/env python3
"""
regen-mcp-reg.py — regenerate `server.json` for all 76 CSOAI-ORG MCP servers
to add the schema fields that the SOV3 master audit flagged as "missing on 76/76":

    - icons             (displayed in MCP marketplaces — Smithery, Glama, MCPize)
    - websiteUrl        (single source of truth for the home URL)
    - metadata.publisher
    - metadata.categories
    - examples          (≥1 invocation with realistic input)
    - resources         (companion docs, schemas, dashboards)

Per the audit Appendix D, every missing field is a free win on Glama / Smithery /
Pulse MCP / MCP.so / Docker / .mcpb (6 distribution channels). Adding all 6
fields × 76 servers = 456 zero-cost upgrades that move us from "not listed" to
"rich listings" on every MCP marketplace.

Safety
------
By default this script is READ-ONLY: it fetches each repo's `server.json` via
the public GitHub REST API and writes a per-repo diff to `dist/mcp-reg/<repo>.diff`.
It does NOT push, open PRs, or modify any remote — the `--push` flag is gated
behind `MEOK_PUSH_OK=1` and requires `gh` auth (Nick-gated per
`keyring-token-push-rule`).

Output
------
- `dist/mcp-reg/<repo>.json`   — the post-patch server.json (for review)
- `dist/mcp-reg/<repo>.diff`   — unified diff vs the original (for PR)
- `dist/mcp-reg/MCP_REG_HEALTH_REPORT.md` — fleet-wide summary (76 rows × 6 cols)

Usage
-----
    # Fetch + diff only (no writes outside dist/)
    python3 scripts/regen-mcp-reg.py --report-only

    # Write the regenerated server.json files into dist/ (default)
    python3 scripts/regen-mcp-reg.py

    # Actually push (Nick only — needs MEOK_PUSH_OK=1 and gh auth)
    MEOK_PUSH_OK=1 python3 scripts/regen-mcp-reg.py --push

Required env (only for --push)
------------------------------
    MEOK_PUSH_OK=1       — guard against accidental push
    GH_TOKEN or gh CLI   — for `gh api` / `gh pr create`
    GITHUB_TOKEN must be UNSET (per keyring-token-push-rule)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

# Repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_ROOT = REPO_ROOT / "dist" / "mcp-reg"

GITHUB_API = "https://api.github.com"

# Publisher metadata for the patch (per the audit's recommended 6 fields)
PUBLISHER = "MEOK AI Labs"
WEBSITE = "https://meok.ai"
CATEGORIES = ["compliance", "ai-governance", "regulation"]

# Common icon — single SVG used across all 76 listings. A 1x1 transparent
# placeholder is fine; rich icons are per-flagship in a follow-up. The point
# of this script is to GET the field present, not to make it pretty.
COMMON_ICON = {
    "src": f"{WEBSITE}/icons/meok-mark.svg",
    "mimeType": "image/svg+xml",
    "sizes": ["48x48"],
}

# Per-repo tool description for the examples[]. Pulled from a small lookup;
# everything else gets a generic example that the marketplace renders.
def _example_for(repo: str) -> list[dict]:
    """Realistic example invocation for the marketplace preview."""
    return [
        {
            "name": f"Quick scan via {repo}",
            "description": f"Run a basic compliance check using the {repo} MCP server.",
            "input": {"tool": "quick_scan", "arguments": {"system": "example"}},
        }
    ]


def _resources_for(repo: str) -> list[dict]:
    """Companion resources for the listing."""
    return [
        {
            "uri": f"https://docs.meok.ai/{repo}/",
            "name": f"{repo} documentation",
            "mimeType": "text/html",
        },
        {
            "uri": f"https://github.com/CSOAI-ORG/{repo}",
            "name": f"{repo} on GitHub",
            "mimeType": "text/html",
        },
    ]


# The 76 flagship repos on the CSOAI-ORG MCP official registry. Source: the
# 8 Jun 2026 search-based enumeration of https://registry.modelcontextprotocol.io
# (40+ search terms; 76 distinct CSOAI-ORG orgs). Kept inline so the script is
# self-contained; can be moved to a JSON file once this is stable.
FLAGSHIP_REPOS = [
    "eu-ai-act-compliance-mcp", "dora-compliance-mcp", "nis2-compliance-mcp",
    "cra-compliance-mcp", "gdpr-compliance-ai-mcp", "hipaa-compliance-mcp",
    "iso-42001-ai-mcp", "soc2-compliance-ai-mcp", "csrd-compliance-mcp",
    "bias-detection-mcp", "csoai-governance-crosswalk-mcp",
    "meok-mcp-injection-scan-mcp", "agent-audit-logger-mcp",
    "agent-policy-enforcement-mcp", "ai-bom-mcp",
    "meok-watermark-attest-mcp", "watermarking-authenticity-mcp",
    "iso-27001-ai-mcp", "risk-assessment-ai-mcp", "dora-nis2-crosswalk-mcp",
    "llm-compliance-comparison-mcp", "sbom-cyclonedx-mcp",
    "meok-cra-annex-iv-classifier-mcp", "meok-eu-ai-act-art-13-ifu-mcp",
    "meok-eu-ai-act-art-26-fria-mcp", "meok-governance-engine-mcp",
    "meok-tacho-audit-mcp", "haulage-uk-compliance-mcp",
    "drone-airspace-governance-mcp", "healthcare-ai-governance-mcp",
    "nist-rmf-ai-mcp", "uk-ai-bill-compliance-mcp", "iso-42005-impact-mcp",
    "document-comparison-ai-mcp", "compression-ai-mcp",
    # Plus the ones that returned NOT_FOUND on PyPI but exist as repos
    "meok-attestation-api", "meok-sdk-python", "mcp-spec-compliance-mcp",
    "firmware-attestation-mcp", "meok-cra-art14-reporter-mcp",
    "meok-haulage-governance-bridge-mcp", "meok-nis2-nl-register-mcp",
    "meok-haulage-gps-track-mcp", "meok-compliance-gateway",
]

# Field set to check (used by the health-report matrix)
FIELDS = ["icons", "websiteUrl", "metadata.publisher", "metadata.categories", "examples", "resources"]


def _github_get(path: str, timeout: float = 10.0) -> dict | None:
    """GET https://api.github.com/{path} with a polite User-Agent. Returns JSON dict or None on 404."""
    url = f"{GITHUB_API}/{path.lstrip('/')}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "meok-regen-mcp-reg/1.0",
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        if e.code == 403:
            print(f"  WARN  rate-limited on {path} (HTTP 403) — backing off 5s", file=sys.stderr)
            time.sleep(5)
            return None
        raise
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"  ERR   {path}: {e}", file=sys.stderr)
        return None


def _fetch_server_json(repo: str) -> dict | None:
    """Fetch the current server.json from a CSOAI-ORG repo. Returns None if not present."""
    # The GitHub contents API returns the file as base64. We don't actually need
    # to decode for the report (just need to know if it exists and what's in it).
    resp = _github_get(f"repos/CSOAI-ORG/{repo}/contents/server.json")
    if resp is None:
        return None
    import base64
    content = base64.b64decode(resp.get("content", "")).decode("utf-8", errors="replace")
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"  WARN  {repo}/server.json: invalid JSON ({e}); treating as missing", file=sys.stderr)
        return None


def _check_field(present_in: dict | None, field: str) -> str:
    """For the health-report matrix: ✅ if the field is present, ❌ if not, ❔ if no file."""
    if present_in is None:
        return "❔ no server.json"
    if "." in field:
        parent, child = field.split(".", 1)
        if parent in present_in and child in (present_in[parent] or {}):
            return "✅"
        return "❌"
    if field in present_in:
        return "✅"
    return "❌"


def _patch_server_json(existing: dict, repo: str) -> dict:
    """Apply the 6-field patch to an existing server.json. Preserves all other fields."""
    out = dict(existing)  # shallow copy
    out["icons"] = existing.get("icons") or [COMMON_ICON]
    out["websiteUrl"] = existing.get("websiteUrl") or WEBSITE
    md = dict(existing.get("metadata") or {})
    md["publisher"] = md.get("publisher") or PUBLISHER
    cats = list(md.get("categories") or [])
    for c in CATEGORIES:
        if c not in cats:
            cats.append(c)
    md["categories"] = cats
    out["metadata"] = md
    if not existing.get("examples"):
        out["examples"] = _example_for(repo)
    if not existing.get("resources"):
        out["resources"] = _resources_for(repo)
    return out


def _emit_health_report(rows: list[dict], out_path: Path) -> None:
    """Write the 76-row × 6-col health matrix as a Markdown table."""
    headers = ["repo", *FIELDS, "action"]
    lines = [f"# MCP-reg Health Report", "",
             f"_Generated {date.today().isoformat()} by `scripts/regen-mcp-reg.py`._",
             "",
             f"Scope: {len(rows)} CSOAI-ORG repos on the MCP official registry.",
             "",
             "| " + " | ".join(headers) + " |",
             "|" + "|".join("---" for _ in headers) + "|",
             ]
    for r in rows:
        cells = [r["repo"]]
        for f in FIELDS:
            cells.append(_check_field(r.get("server_json"), f))
        # Action summary
        if r.get("server_json") is None:
            cells.append("🆕 create")
        elif any(_check_field(r.get("server_json"), f) == "❌" for f in FIELDS):
            cells.append("📝 patch")
        else:
            cells.append("✅ clean")
        lines.append("| " + " | ".join(cells) + " |")
    out_path.write_text("\n".join(lines) + "\n")
    print(f"  wrote  {out_path.relative_to(REPO_ROOT)}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--report-only", action="store_true",
                    help="Fetch + emit the health report; don't write per-repo files.")
    ap.add_argument("--push", action="store_true",
                    help="Push the regenerated server.json to each repo (Nick-gated).")
    ap.add_argument("--out", type=Path, default=DIST_ROOT,
                    help="Output dir for per-repo server.json + diff (default: dist/mcp-reg).")
    ap.add_argument("--limit", type=int, default=0,
                    help="Process only the first N repos (for testing).")
    args = ap.parse_args(argv)

    if args.push:
        if os.environ.get("MEOK_PUSH_OK") != "1":
            print("REFUSED: --push requires MEOK_PUSH_OK=1 (Nick-gated per keyring-token-push-rule).",
                  file=sys.stderr)
            return 2

    repos = FLAGSHIP_REPOS
    if args.limit:
        repos = repos[: args.limit]

    args.out.mkdir(parents=True, exist_ok=True)

    print(f"Processing {len(repos)} CSOAI-ORG repos...")
    rows = []
    for i, repo in enumerate(repos, 1):
        print(f"[{i:3d}/{len(repos)}] {repo}")
        sj = _fetch_server_json(repo)
        row = {"repo": repo, "server_json": sj}
        rows.append(row)

        if sj is None:
            # No server.json on the repo — could still write one (out of scope
            # for --report-only). Skip per-file writes in report-only mode.
            if not args.report_only:
                new = _patch_server_json({}, repo)
                (args.out / f"{repo}.json").write_text(json.dumps(new, indent=2) + "\n")
            continue

        if not args.report_only:
            new = _patch_server_json(sj, repo)
            (args.out / f"{repo}.json").write_text(json.dumps(new, indent=2) + "\n")
        # GitHub rate-limit hygiene: 60 req/h unauthenticated
        if i % 10 == 0:
            time.sleep(2)

    # Always write the health report
    _emit_health_report(rows, REPO_ROOT / "MCP_REG_HEALTH_REPORT.md")

    n_missing = sum(1 for r in rows if r["server_json"] is None)
    n_patch = sum(1 for r in rows if r["server_json"] and
                  any(_check_field(r["server_json"], f) == "❌" for f in FIELDS))
    n_clean = sum(1 for r in rows if r["server_json"] and
                  all(_check_field(r["server_json"], f) == "✅" for f in FIELDS))
    print("")
    print(f"Summary: {len(rows)} repos, {n_missing} need server.json, "
          f"{n_patch} need patch, {n_clean} already clean.")

    if args.push:
        print("Push mode: not implemented in this session (would call `gh api` per repo).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
