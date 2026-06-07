#!/usr/bin/env python3
"""
gen-geo.py — Generate GEO/AEO files for all 28 staged MEOK hives.

Per [[meok-global-strategy-2026-06-07]] GEO/AEO 2026 strategy:
  - Search-engine answer extraction (AEO) rewards llms.txt
  - LLM citation (GEO) rewards structured data + FAQ schema
  - Cross-linking with real integration paths (not PBN)
  - Per-vertical first-party statistics worth citing

Generates 3 files per hive:
  - index.html         (landing page with JSON-LD, FAQ schema, OG tags)
  - llms.txt           (AEO citation extraction — short, scannable)
  - sitemap.xml        (with <lastmod> from the git head date)

Plus a shared _cross-links.json describing the integration paths
between hives (real, not PBN).

Idempotent. Safe to re-run.

Usage:
  python3 gen-geo.py                      # generate all 28 from registry
  python3 gen-geo.py grabhire.ai          # one hive
  python3 gen-geo.py --list               # list registered domains
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from textwrap import dedent

# Reuse the gen-hive registry (file has hyphen, so importlib)
import importlib.util
_hive_path = Path(__file__).parent / "gen-hive.py"
_spec = importlib.util.spec_from_file_location("gen_hive_alias", _hive_path)
_gen_hive = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gen_hive)
DOMAIN_REGISTRY = _gen_hive.DOMAIN_REGISTRY

HIVE_GENESIS = "2026-06-07"
CSOAI_ORG_URL = "https://github.com/CSOAI-ORG"

# Real cross-hive integration paths (no PBN — each link is justified)
# Format: source -> [(target, anchor_text, why)]
CROSS_LINKS = {
    "meok.ai": [
        ("csoai.org", "CSOAI governance suite", "customer's compliance portal"),
        ("proofof.ai", "Proofof.ai attestations", "evidence layer"),
        ("councilof.ai", "Councilof.ai audit", "every customer action audited"),
    ],
    "csoai.org": [
        ("meok.ai", "MEOK compliance portal", "B2B customer login"),
        ("accountabilityof.ai", "Accountability reports", "AI Act Article 12 logging"),
        ("biasdetectionof.ai", "Bias detection", "EU AI Act Article 10"),
        ("dataprivacyof.ai", "GDPR + privacy", "Article 30 records"),
        ("transparencyof.ai", "Explainability", "Article 13 transparency"),
        ("councilof.ai", "BFT deliberation", "multi-stakeholder audit"),
        ("proofof.ai", "Attestations", "signed compliance evidence"),
    ],
    "proofof.ai": [
        ("csoai.org", "CSOAI governance", "issuer of attestations"),
        ("meok.ai", "MEOK portal", "verify at /v/<cert_id>"),
    ],
    "cobolbridge.ai": [
        ("meok.ai", "MEOK compliance", "modern COBOL clients' compliance stack"),
    ],
    "accountabilityof.ai": [
        ("csoai.org", "CSOAI suite", "bundled governance"),
        ("ai-incident-reporting-mcp", "Incident reporting", "core tool"),
    ],
    "agisafe.ai": [
        ("csoai.org", "CSOAI research", "linked safety research"),
    ],
    "asisecurity.ai": [
        ("csoai.org", "CSOAI suite", "bundled governance"),
    ],
    "biasdetectionof.ai": [
        ("dataprivacyof.ai", "GDPR", "Article 10 + Article 30 bundle"),
        ("csoai.org", "CSOAI suite", "EU AI Act coverage"),
    ],
    "dataprivacyof.ai": [
        ("biasdetectionof.ai", "Bias detection", "GDPR + AI Act package"),
        ("accountabilityof.ai", "Accountability", "audit trail + privacy"),
        ("csoai.org", "CSOAI suite", "EU AI Act coverage"),
    ],
    "ethicalgovernanceof.ai": [
        ("csoai.org", "CSOAI", "redirect — same brand"),
    ],
    "safetyof.ai": [
        ("csoai.org", "CSOAI suite", "landing → suite"),
    ],
    "transparencyof.ai": [
        ("csoai.org", "CSOAI suite", "explainability ticket"),
        ("proofof.ai", "Attestations", "sign + verify explanations"),
    ],
    "councilof.ai": [
        ("csoai.org", "CSOAI", "BFT deliberation backbone"),
    ],
    "grabhire.ai": [
        ("muckaway.ai", "Muck-away (UK term)", "UK haulage cluster"),
        ("planthire.ai", "Plant-hire", "UK construction cluster"),
        ("commercialvehicle.ai", "Fleet", "UK construction cluster"),
    ],
    "muckaway.ai": [
        ("grabhire.ai", "Grab-lorry", "UK cluster"),
        ("planthire.ai", "Plant-hire", "UK cluster"),
        ("commercialvehicle.ai", "Fleet", "UK cluster"),
    ],
    "planthire.ai": [
        ("grabhire.ai", "Grab-lorry", "UK cluster"),
        ("muckaway.ai", "Muck-away", "UK cluster"),
        ("commercialvehicle.ai", "Fleet", "UK cluster"),
    ],
    "commercialvehicle.ai": [
        ("grabhire.ai", "Grab-lorry", "UK cluster"),
        ("muckaway.ai", "Muck-away", "UK cluster"),
    ],
    "landlaw.ai": [
        ("csoai.org", "CSOAI", "compliance for property lawyers"),
    ],
    "fishkeeper.ai": [
        ("koikeeper.ai", "KoiKeeper premium", "premium tier upgrade"),
    ],
    "koikeeper.ai": [
        ("fishkeeper.ai", "FishKeeper community", "consumer base"),
    ],
    "diyhelp.ai": [],  # flip — no cross-links
    "pokerhud.ai": [],  # flip
    "loopfactory.ai": [],
    "optimobile.ai": [],
    "socialmediamananger.ai": [],  # let expire
    "openmoe.ai": [
        ("openMCP", "openMCP audit engine", "cross-post + score"),
        ("meok.ai", "MEOK gateway", "production deployment"),
    ],
    "openMCP": [
        ("openmoe.ai", "OpenMoE-BFT", "audit target"),
        ("meok.ai", "MEOK gateway", "audit target"),
    ],
    "meok-compliance-gateway": [
        ("csoai.org", "CSOAI", "wraps flagship MCPs"),
        ("proofof.ai", "Proofof.ai", "x402 receipts"),
        ("openmoe.ai", "OpenMoE", "BFT receipts via x402"),
    ],
}


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def gen_index_html(d: dict) -> str:
    """Landing page with JSON-LD Organization + SoftwareApplication + FAQPage + OG."""
    name = d['domain'].split('.')[0]
    cross = CROSS_LINKS.get(d['domain'], [])
    cross_items = "\n".join(
        f'<li><a href="https://{t}">{t}</a> &mdash; {why}</li>'
        for (t, _anchor, why) in cross
    )
    tools_items = "\n".join(f'<li>{t}</li>' for t in d['tools'])
    # FAQ questions from the domain's specific value
    faq = d.get('faq', [
        {"q": f"What is {d['domain']}?", "a": d['personality']},
        {"q": f"How much does {d['domain']} cost?", "a": f"x402 micro-settlement: ${d['x402_price']}/call. Free tier: {d['free_tier']} calls/day."},
        {"q": f"Is {d['domain']} open source?", "a": "Yes, MIT licensed at github.com/CSOAI-ORG/" + name + "-hive."},
    ])
    faq_items = "\n".join(
        f'<details><summary>{q["q"]}</summary><p>{q["a"]}</p></details>'
        for q in faq
    )
    pricing_para = (
        f'x402 micro-settlement enabled: <strong>${d["x402_price"]}</strong> per call. '
        f'Free tier: {d["free_tier"]} calls per IP per day.'
        if d['x402_enabled']
        else 'Free — no payment required.'
    )
    # Build JSON-LD blocks at column 4 (one level inside <script>)
    faq_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q["q"],
                "acceptedAnswer": {"@type": "Answer", "text": q["a"]}
            }
            for q in faq
        ]
    }, indent=2, ensure_ascii=False)
    org_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": d['domain'],
        "url": f"https://{d['domain']}",
        "parentOrganization": {"@type": "Organization", "name": "CSOAI-ORG", "url": "https://csoai.org"},
        "sameAs": [f"{CSOAI_ORG_URL}/{name}-hive"]
    }, indent=2, ensure_ascii=False)
    app_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": d['domain'],
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Any (HTTP/MCP)",
        "offers": {
            "@type": "Offer",
            "price": d['x402_price'],
            "priceCurrency": "USD",
            "category": "per-call"
        } if d['x402_enabled'] else {"@type": "Offer", "price": "0.00", "priceCurrency": "USD"},
        "description": d['personality']
    }, indent=2, ensure_ascii=False)
    # Indent each line of the JSON-LD blocks by 4 spaces so they sit inside <script>
    def _js(block: str) -> str:
        return "\n".join("    " + ln if ln.strip() else "" for ln in block.split("\n"))
    # Use plain string template (NOT dedent) — write content at its final column 0
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{d['domain']} &mdash; {d['tier'].replace('_', ' ').title()} Hive</title>
  <meta name="description" content="{d['personality']}" />
  <meta name="keywords" content="{d['domain']}, MEOK, MCP, agent, AI compliance, x402" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{d['domain']}" />
  <meta property="og:description" content="{d['personality']}" />
  <meta property="og:url" content="https://{d['domain']}" />
  <meta property="og:site_name" content="CSOAI-ORG" />

  <!-- Twitter card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{d['domain']}" />
  <meta name="twitter:description" content="{d['personality']}" />

  <!-- JSON-LD: structured data for LLM citation + Google rich results -->
  <script type="application/ld+json">
{_js(org_schema)}
  </script>
  <script type="application/ld+json">
{_js(app_schema)}
  </script>
  <script type="application/ld+json">
{_js(faq_schema)}
  </script>

  <link rel="canonical" href="https://{d['domain']}" />
  <link rel="alternate" type="text/plain" href="/llms.txt" title="LLM-readable summary" />
  <link rel="sitemap" type="application/xml" href="/sitemap.xml" />
</head>
<body>
  <header>
    <h1>{d['domain']}</h1>
    <p><strong>Tier:</strong> {d['tier']} &middot; <strong>Palette:</strong> {d['palette']}</p>
  </header>

  <main>
    <section>
      <h2>What is {d['domain']}?</h2>
      <p>{d['personality']}</p>
    </section>

    <section>
      <h2>Pricing</h2>
      <p>{pricing_para}</p>
    </section>

    <section>
      <h2>MCP tools exposed</h2>
      <ul>
        <li>MCP endpoint: <code>/mcp</code> (streamable-HTTP, mcp={_gen_hive.MCP_VERSION})</li>
        {tools_items}
      </ul>
    </section>

    <section>
      <h2>Cross-hive integrations</h2>
      <ul>
        {cross_items}
      </ul>
    </section>

    <section>
      <h2>Open source</h2>
      <p>Source code: <a href="{CSOAI_ORG_URL}/{name}-hive">github.com/CSOAI-ORG/{name}-hive</a></p>
      <p>License: MIT</p>
    </section>

    <section>
      <h2>FAQ</h2>
{faq_items}
    </section>
  </main>

  <footer>
    <p>Part of the <a href="https://csoai.org">CSOAI-ORG</a> 28-hive mesh.
    A2A Agent Card: <a href="/.well-known/agent-card.json">/.well-known/agent-card.json</a></p>
  </footer>
</body>
</html>
"""


def gen_llms_txt(d: dict) -> str:
    """llms.txt — LLM-readable short summary. Per https://llmstxt.org convention."""
    name = d['domain'].split('.')[0]
    cross = CROSS_LINKS.get(d['domain'], [])
    tools_block = "\n".join(f"- {t}" for t in d['tools']) or "- (none yet)"
    cross_block = "\n".join(f"- {t} ({why})" for (t, _a, why) in cross) or "- (none)"
    pricing = (
        f"x402 $ {d['x402_price']}/call (free tier: {d['free_tier']}/day)"
        if d['x402_enabled'] else "Free"
    )
    return f"""# {d['domain']}

> {d['personality']}

## Key facts

- **Domain:** {d['domain']}
- **Tier:** {d['tier']}
- **MCP endpoint:** https://{d['domain']}/mcp (streamable-HTTP, MCP {_gen_hive.MCP_VERSION})
- **A2A Agent Card:** https://{d['domain']}/.well-known/agent-card.json
- **Open source:** {CSOAI_ORG_URL}/{name}-hive (MIT)
- **Pricing:** {pricing}
- **Memory mode:** {d['memory_mode']}
- **Knowledge subgraph scope:** {d['cognee_scope']}

## Tools exposed (MCP)

{tools_block}

## Cross-hive integrations

{cross_block}

## Brand

- **Palette:** {d['palette']}
- **Voice:** {d['voice']}

## Sources

- Hive architecture: {CSOAI_ORG_URL}/meok-compliance-gateway/blob/main/FLEET_BASE.md
- Global strategy: see the MEOK memory file meok-global-strategy-2026-06-07
- Crown jewels: see the MEOK memory file meok-crown-jewels-2026-06-07
"""


def gen_sitemap_xml(d: dict) -> str:
    """Sitemap with lastmod from git HEAD date of the hive repo."""
    name = d['domain'].split('.')[0]
    # Best-effort: use the genesis date if git lookup fails
    lastmod = HIVE_GENESIS
    try:
        out = subprocess.run(
            ["git", "-C", str(Path("/Users/nicholas/hive-staging") / f"{name}-hive"),
             "log", "-1", "--format=%cI"],
            capture_output=True, text=True, timeout=5
        )
        if out.returncode == 0 and out.stdout.strip():
            # Convert ISO 8601 to YYYY-MM-DD
            lastmod = out.stdout.strip()[:10]
    except Exception:
        pass
    return dedent(f"""\
    <?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>https://{d['domain']}/</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
      </url>
      <url>
        <loc>https://{d['domain']}/.well-known/agent-card.json</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.6</priority>
      </url>
      <url>
        <loc>https://{d['domain']}/llms.txt</loc>
        <lastmod>{lastmod}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
      </url>
    </urlset>
    """)


def gen_cross_links_json() -> str:
    """Shared cross-links file for the GEO strategy."""
    out = {
        "_about": "Real cross-hive integration paths. NOT PBN. Each link has a justification.",
        "links": [
            {"from": src, "to": [t for (t, _a, _w) in targets], "reason": [w for (_t, _a, w) in targets]}
            for src, targets in CROSS_LINKS.items()
            if targets
        ]
    }
    return json.dumps(out, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate_one(spec: dict, out_root: Path) -> Path:
    name = spec['domain'].split('.')[0]
    hive_dir = out_root / f"{name}-hive"
    hive_dir.mkdir(parents=True, exist_ok=True)
    (hive_dir / "index.html").write_text(gen_index_html(spec))
    (hive_dir / "llms.txt").write_text(gen_llms_txt(spec))
    (hive_dir / "sitemap.xml").write_text(gen_sitemap_xml(spec))
    return hive_dir


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("domain", nargs="?")
    p.add_argument("--out", default="/Users/nicholas/hive-staging")
    p.add_argument("--list", action="store_true")
    args = p.parse_args()

    if args.list:
        for s in DOMAIN_REGISTRY:
            print(f"  {s['domain']:<30}  tier={s['tier']}")
        return 0

    out_root = Path(args.out).expanduser()
    out_root.mkdir(parents=True, exist_ok=True)

    # Shared cross-links (one per staging dir)
    cross_path = out_root / "_cross-links.json"
    cross_path.write_text(gen_cross_links_json())
    print(f"Wrote {cross_path}")

    if args.domain:
        spec = next((s for s in DOMAIN_REGISTRY if s['domain'] == args.domain), None)
        if not spec:
            print(f"ERROR: {args.domain} not in registry", file=sys.stderr)
            return 1
        out = generate_one(spec, out_root)
        print(f"  {spec['domain']:<30} -> {out}")
    else:
        for spec in DOMAIN_REGISTRY:
            out = generate_one(spec, out_root)
            print(f"  {spec['domain']:<30}  tier={spec['tier']:<16}  -> {out.name}/{{index.html,llms.txt,sitemap.xml}}")
        print(f"\n{len(DOMAIN_REGISTRY)} hives generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
