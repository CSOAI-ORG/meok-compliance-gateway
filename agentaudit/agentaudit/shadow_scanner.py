"""Shadow A2A agent scanner — discover unregistered agents inside an estate."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urljoin

try:
    import aiohttp
except Exception:  # pragma: no cover
    aiohttp = None


@dataclass
class DiscoveredAgent:
    url: str
    status: str               # "live" | "dead" | "unreachable"
    agent_card: dict[str, Any] | None = None
    trust_score: float | None = None
    fingerprints: list[str] = field(default_factory=list)


class ShadowScanner:
    """Probe a list of candidate URLs for A2A `/.well-known/agent.json` endpoints."""

    WELL_KNOWN = "/.well-known/agent-card.json"

    def __init__(self, timeout: float = 5.0) -> None:
        self.timeout = timeout
        self._results: list[DiscoveredAgent] = []

    async def scan(self, candidates: list[str]) -> list[DiscoveredAgent]:
        if aiohttp is None:
            raise RuntimeError("aiohttp is required for shadow scanning")
        self._results = []
        async with aiohttp.ClientSession() as session:
            tasks = [self._probe(session, u) for u in candidates]
            self._results = await asyncio.gather(*tasks, return_exceptions=True)
            # Filter out exceptions
            self._results = [
                r for r in self._results if isinstance(r, DiscoveredAgent)
            ]
        return self._results

    async def _probe(self, session: aiohttp.ClientSession, url: str) -> DiscoveredAgent:
        target = urljoin(url.rstrip("/") + "/", self.WELL_KNOWN)
        try:
            async with session.get(target, timeout=self.timeout) as resp:
                if resp.status == 200:
                    card = await resp.json()
                    return DiscoveredAgent(
                        url=url,
                        status="live",
                        agent_card=card,
                        fingerprints=["a2a-well-known"],
                    )
                return DiscoveredAgent(url=url, status="dead", fingerprints=[])
        except asyncio.TimeoutError:
            return DiscoveredAgent(url=url, status="unreachable", fingerprints=[])
        except Exception:
            return DiscoveredAgent(url=url, status="unreachable", fingerprints=[])

    def suspicious(self, threshold: float = 0.3) -> list[DiscoveredAgent]:
        """Agents that responded but have low or missing trust scores."""
        return [
            r for r in self._results
            if r.status == "live" and (r.trust_score or 0.0) < threshold
        ]
