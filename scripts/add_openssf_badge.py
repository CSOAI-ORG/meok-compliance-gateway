#!/usr/bin/env python3
"""
add_openssf_badge.py — insert the OpenSSF Scorecard badge into a flagship README.

Per [[meok-deep-audit-2026-06-08]] P3-3: once the keystone's `chore/ci-hardening`
worktree is merged and the 52 OpenSSF PRs land, every flagship README should
carry the OpenSSF Scorecard badge as proof of supply-chain posture.

This script:
  1. Looks up the flagship's scorecard.dev URL (per the org/repo convention).
  2. Inserts a markdown badge line after the first `# <Title>` heading in
     the README. Idempotent — won't double-insert.
  3. Optionally runs a `git commit` (with the right message format) on the
     branch you pass via --branch.

Usage:
  python3 add_openssf_badge.py eu-ai-act-compliance-mcp
  python3 add_openssf_badge.py --all --branch chore/scorecard-badge
  python3 add_openssf_badge.py --dry-run eu-ai-act-compliance-mcp

Per [[agentaudit-concurrent-session-hazards]]: this script operates on a
fleet-clone directory tree, not the keystone's main checkout. It never
modifies the keystone.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ORG = "CSOAI-ORG"
DEFAULT_CLONE_ROOT = Path("/Users/nicholas/fleet-clones")
SCORECARD_BASE = "https://scorecard.dev/viewer/?uri=github.com"

# Badges we always want. Customise per-repo by adding to this dict.
DEFAULT_BADGES = [
    ("OpenSSF Scorecard",
     "https://api.securityscorecards.dev/projects/github.com/{org}/{repo}/badge",
     SCORECARD_BASE + "/{org}/{repo}"),
    ("License",
     "https://img.shields.io/github/license/{org}/{repo}",
     "blob/main/LICENSE"),
    ("Last commit",
     "https://img.shields.io/github/last-commit/{org}/{repo}",
     "commits/main"),
]


def badge_block(org: str, repo: str) -> str:
    """Return markdown badge lines."""
    lines = ["<!-- OpenSSF + hygiene badges (auto-inserted by add_openssf_badge.py) -->"]
    for label, img_tmpl, href_tmpl in DEFAULT_BADGES:
        img = f"![{label}]({img_tmpl.format(org=org, repo=repo)})"
        href = href_tmpl.format(org=org, repo=repo)
        if not href.startswith("http"):
            href = f"https://github.com/{org}/{repo}/{href}"
        lines.append(f"[{img}]({href})")
    lines.append("")  # trailing blank
    return "\n".join(lines)


def has_badge(readme: str) -> bool:
    return "add_openssf_badge.py" in readme or "OpenSSF Scorecard" in readme


def insert_after_first_h1(readme: str, block: str) -> str:
    """Insert block immediately after the first H1 (or at top if no H1)."""
    lines = readme.splitlines()
    out = []
    inserted = False
    for i, line in enumerate(lines):
        out.append(line)
        if not inserted and line.lstrip().startswith("# "):
            # Append block after the H1 + one blank line
            out.append("")
            out.extend(block.splitlines())
            inserted = True
    if not inserted:
        # No H1 — prepend
        out = block.splitlines() + [""] + out
    return "\n".join(out) + "\n"


def process_one(clone_root: Path, repo: str, dry_run: bool) -> str:
    repo_dir = clone_root / repo
    readme = repo_dir / "README.md"
    if not readme.exists():
        return f"  [skip] {repo}: no README.md at {readme}"
    text = readme.read_text()
    if has_badge(text):
        return f"  [skip] {repo}: badge already present"
    new_text = insert_after_first_h1(text, badge_block(ORG, repo))
    if dry_run:
        return f"  [dry-run] {repo}: would insert {len(badge_block(ORG, repo).splitlines())} lines"
    readme.write_text(new_text)
    return f"  [ok] {repo}: badge block inserted"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("repo", nargs="?", help="Single repo name (e.g. eu-ai-act-compliance-mcp)")
    p.add_argument("--all", action="store_true", help="Process all 14 flagships")
    p.add_argument("--clone-root", default=DEFAULT_CLONE_ROOT, type=Path)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--branch", help="Branch name to commit on (e.g. chore/scorecard-badge)")
    args = p.parse_args()

    if not args.repo and not args.all:
        p.error("Provide a repo name or --all")

    repos = []
    if args.all:
        # Iterate the clone root
        repos = sorted(d.name for d in args.clone_root.iterdir() if d.is_dir())
    else:
        repos = [args.repo]

    for repo in repos:
        print(process_one(args.clone_root, repo, args.dry_run))

    if args.branch and not args.dry_run:
        print(f"\nCreating branch {args.branch} across all touched repos...")
        for repo in repos:
            repo_dir = args.clone_root / repo
            if not (repo_dir / "README.md").exists():
                continue
            try:
                subprocess.run(
                    ["git", "-C", str(repo_dir), "checkout", "-b", args.branch],
                    check=True, capture_output=True
                )
                subprocess.run(
                    ["git", "-C", str(repo_dir), "add", "README.md"],
                    check=True, capture_output=True
                )
                subprocess.run(
                    ["git", "-C", str(repo_dir), "commit", "-m",
                     f"chore(scorecard): add OpenSSF Scorecard + hygiene badges to README\n\n"
                     f"Auto-inserted by scripts/add_openssf_badge.py.\n"
                     f"Fixes OpenSSF best-practice gap (badge visibility on every flagship)."],
                    check=True, capture_output=True
                )
                print(f"  [committed] {repo} on {args.branch}")
            except subprocess.CalledProcessError as e:
                print(f"  [git-error] {repo}: {e.stderr.decode() if e.stderr else e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
