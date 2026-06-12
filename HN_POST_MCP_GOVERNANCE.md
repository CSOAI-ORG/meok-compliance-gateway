# Show HN: MEOK — sovereign AI compliance infrastructure as a 28-hive mesh

> **Status**: P1-1, [[meok-deep-audit-2026-06-08]]
> **Target**: Hacker News, Day 5 of the 25-day pre-launch (June 13, 2026)
> **Length target**: 600-1000 words
> **Tone**: technical, NOT marketing. HN hates marketing; loves architectural posts.
> **Pre-publish check**: run through [RUBRIC_EXTERNAL_COMMS.md](RUBRIC_EXTERNAL_COMMS.md) before posting.

---

**TL;DR**: We open-sourced a 28-hive mesh for AI governance where each of 25 industry-specific `.ai` domains runs its own autonomous 7-layer agent stack. The keystone is a streamable-HTTP gateway with x402 paywall and OpenSSF Scorecard 7.5/10. Here's what we learned shipping it.

---

We're a small team that has spent the last 90 days building what we call the **MEOK 28-hive mesh**: 25 industry-specific AI agent stacks (one per `.ai` domain: meok.ai, csoai.org, proofof.ai, grabhire.ai, koikeeper.ai, …) plus 3 infrastructure hives (openmoe.ai, openMCP, meok-compliance-gateway), all peer-to-peer via A2A.

We hit the wall on something we didn't see coming: **governance**. We had 13,000+ MCP servers in our directory, 97M downloads, and not a single one with built-in authentication, audit logging, or paywall semantics. We were the only governance tooling in the ecosystem, and we weren't sure we were doing it right.

So we open-sourced everything and asked the security community to break it.

This post is about three things we learned in the process.

## 1. The MCP ecosystem has a governance gap

We did a hand-rolled OpenSSF Scorecard audit (against the 18-check matrix) of our own fleet: **mean 4.04/10, median 4.06/10**. The 14 flagship MCPs had identical universal gaps:

- No Dependabot
- No CodeQL
- No cosign
- No fuzzing
- No branch-protection evidence

The fix was mechanical: add `.github/dependabot.yml`, `.github/workflows/codeql.yml`, a `cosign sign --yes` step in the publish workflow, and a `tests/test_fuzz.py` with `hypothesis` for property-based fuzzing. After the four fixes, our keystone projected to **7.5/10** (green), the fleet to **~7.0/10**. Total cost: ~3 hours of human time and 52 PRs across 14 repos.

We wrote [FLEET_SCORE.md](https://github.com/CSOAI-ORG/meok-compliance-gateway/blob/main/FLEET_SCORE.md) as the canonical per-repo scoreboard. Each flagship repo now has its own OpenSSF badge in the README.

## 2. Byzantine fault tolerance works for AI agent memory

The architectural decision we agonised over most: how do you stop a single rogue agent from corrupting the shared memory across 25 hives?

We landed on **Byzantine Fault Tolerant (BFT) consensus** for every Memoria commit. The keystone now has:

- **mex** (memory exchange) for inter-hive sync
- **Memoria** (Rust) for Git-for-memory
- **Cognee** for the knowledge subgraph
- **agentmemory** for agent-private state
- **domain-MCP** for the industry-specific tool surface
- **Hermes Agent** (184k★) for the message router
- **Open Design** (60k★) for the agent composition layer

The 7-layer stack runs in each hive. Cross-hive calls go through **A2A Agent Cards** (`.well-known/agent-card.json`) and are signed with **BFT quorum certificates**. Every cross-hive call also returns a **proofof.ai attestation** that the customer can verify offline.

What this means in practice: if one agent goes rogue, the BFT layer refuses the commit. If a hive goes down, the A2A peer mesh routes around it. If a customer asks "what did your AI decide and why?", they get a signed evidence trail.

## 3. x402 micro-settlement is the smallest bridge to revenue

We priced per-call MCP at $0.01-$10.00 per request, with 0-100 free calls per IP per day. Payment rail is **x402 / Coinbase CDP** — a 1-line payment-challenge protocol that fits inside HTTP.

The `@paywalled` decorator (in our keystone's `meok_x402.py`) wraps any MCP tool. If a request comes in without a valid payment, the gateway returns a 402 with the challenge. The customer pays, retries, gets the response. End-to-end verified, both modes, with hermetic test fixtures that don't touch the live network.

Why this matters: a 25-hive mesh with 300+ tools and 0-100 free calls per IP per day is a *self-monetising* OSS project. We don't need 50 customers to make payroll. We need 1 customer to call one expensive proofof.ai lookup, and we cover infra for the month.

## What's open-sourced

Everything. MIT license. The keystone repo is [github.com/CSOAI-ORG/meok-compliance-gateway](https://github.com/CSOAI-ORG/meok-compliance-gateway). The 25 hive-configs (10-file starter kits per hive) are in `/Users/nicholas/hive-staging/`, public-org-pushable once DNS resolves.

The 19 open-source "crown jewels" we verified and integrated — mcp-gateway (36★), mcp-proxy (2.5k★), Hermes Agent (184k★), Open Design (60k★), agentmemory (21.5k★), Memoria (Rust, Git-for-memory), EvoAgentX, Google A2A, swarms-rs, ANP — are listed in [meok-crown-jewels-2026-06-07.md](https://github.com/CSOAI-ORG/meok-compliance-gateway/blob/main/memory/crown-jewels.md).

## What's NOT open-sourced

- The 5 manual revenue gates (Stripe live mode, Vercel auth, Namecheap DNS, Resend, LinkedIn). These are account-gated for the human founder, not engineering problems.
- The competitive-intelligence dossier (we don't publish "kill shot" rhetoric about named competitors; see [RUBRIC_EXTERNAL_COMMS.md](https://github.com/CSOAI-ORG/meok-compliance-gateway/blob/main/RUBRIC_EXTERNAL_COMMS.md)).
- The M&A target valuations and talent rosters.

## What we got wrong

- "10x undercut" headlines were oversold. The honest comparison is **2-20x cheaper at the enterprise tier**, **1000-10000x for low-volume customers**. The framing matters.
- Branch protection is the audit check we still can't pass — it requires org-level admin token scope, not an engineering fix.
- The MCP 2026-07-28 spec freeze will require us to migrate `http_server.py` to stateless. ~8 weeks of work. We're tracking it.

## What we'd love feedback on

- **The BFT layer**: are we re-inventing something that's already solved by Raft/PBFT libraries? We rolled our own because none of the existing ones fit the "agent commits" workload, but we might be wrong.
- **The x402 payment-challenge protocol**: is the 1-line challenge format the right shape, or should it be a full RFC-9728-style `WWW-Authenticate` header?
- **The 4-tier SaaS pricing** (Freemium / Team $29 / Business $49 / Enterprise custom) alongside the per-call x402 micro-call layer. Is the dual-SKU pattern confusing, or is it the right shape for both human and agent buyers?

Drop a comment, open an issue, or DM us on the GitHub Discussions. The keystone's [FLEET_BASE.md](https://github.com/CSOAI-ORG/meok-compliance-gateway/blob/main/FLEET_BASE.md) has the full architecture.

— The MEOK team
