# Contributing to MEOK

Thanks for your interest in the MEOK compliance gateway. We welcome bug reports, security disclosures, and pull requests.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## How to contribute

### Bug reports

Open an issue on [github.com/CSOAI-ORG/meok-compliance-gateway/issues](https://github.com/CSOAI-ORG/meok-compliance-gateway/issues) with:

- A clear, descriptive title
- Steps to reproduce (or a minimal failing test)
- Expected vs actual behaviour
- Python version + OS

### Security disclosures

**Do not open public issues for security vulnerabilities.** See [SECURITY.md](SECURITY.md) for the private disclosure process and our OpenSSF Scorecard-verified handling.

### Pull requests

1. **Branch from `main`**. Branch naming: `feat/...`, `chore/...`, `fix/...`. No commits to `main` directly.
2. **One concern per PR**. Keep diffs small (< 400 lines if possible).
3. **Add a test** if you're fixing a bug or adding behaviour. We use `pytest` + `hypothesis` for property-based fuzzing.
4. **Run the linters** before pushing:
   ```bash
   ruff check scripts/ agentaudit/
   mypy scripts/ agentaudit/
   ```
5. **Sign the DCO** (Developer Certificate of Origin). Add `Signed-off-by: Your Name <you@example.com>` to your commit message. This is the same approach the Linux kernel uses.
6. **Push** with the keyring token (NOT the env `GITHUB_TOKEN` — it 403s on push):
   ```bash
   env -u GITHUB_TOKEN -u GH_TOKEN git push origin your-branch
   ```
7. **Open the PR** with the keyring token:
   ```bash
   env -u GITHUB_TOKEN -u GH_TOKEN gh pr create --base main --head your-branch
   ```

## Repository conventions

- **Language**: Python 3.11+ (uses `from __future__ import annotations`, `match` statements, `tomllib`).
- **MCP server framework**: [FastMCP](https://github.com/modelcontextprotocol/python-sdk) from the official `mcp` package.
- **Transport**: streamable-HTTP (the [2026-07-28 spec](mcp-2026-07-28-stateless-spec.md) will require a stateless migration; we are tracking it).
- **Tests live in `tests/` and `agentaudit/tests/`**. Run all tests with `pytest`.
- **Cross-hive data** is exchanged via A2A Agent Cards (`.well-known/agent-card.json`).

## Development setup

```bash
# Clone
git clone https://github.com/CSOAI-ORG/meok-compliance-gateway.git
cd meok-compliance-gateway

# Pin the exact dependency versions (per FLEET_BASE.md F3 pattern)
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-gateway.txt
pip install -e ".[dev]"

# Run the gateway
python http_server.py
# Health check: curl http://localhost:8080/healthz

# Run the tests
pytest tests/ -v
```

## Commit message format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary>

<body — what changed and why, with OpenSSF check refs if applicable>

<footer — references, breaks, deprecations>
```

Common types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`.

## What we're NOT accepting

- **Vendor-specific extensions** to MCP (we follow the upstream spec only — see [mcp-2026-07-28-stateless-spec.md](mcp-2026-07-28-stateless-spec.md)).
- **Untested code paths** in the gateway itself (the x402 paywall, the agent-card resolver, the `/healthz` endpoint).
- **License changes** without prior discussion (the keystone is MIT; do not relicense).
- **Trademark / brand assets** for "MEOK," "CSOAI-ORG," or any of the 28 hive domains. These are reserved.

## Questions?

- Open a [GitHub Discussion](https://github.com/CSOAI-ORG/meok-compliance-gateway/discussions).
- The full architecture and constraints are in [FLEET_BASE.md](FLEET_BASE.md).
- See the MEOK GEO/AEO strategy and 28-hive mesh in the project memory file `meok-hive-architecture-2026-06-07.md`.

Thanks for contributing. Together we're building the most defensible open-source sovereign AI compliance infrastructure in the world.
