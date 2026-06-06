"""BFT Consensus metadata for OpenMoE-BFT Empire Layer 2 & Layer 9.

See: OPENMOE_BFT_ALIGNMENT.md for cross-agent context.

Tracks 2f+1 Byzantine-Fault-Tolerant consensus rounds on audit-trail entries.
Production deployments replace the in-memory dict with a distributed consensus
log (Mysticeti, Lachesis, or ByzFL aggregator).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class BFTConsensus:
    """Consensus state for a single audit entry or round."""
    round_id: int
    total_nodes: int
    votes: dict[str, str] = field(default_factory=dict)   # node_id -> vote_hash
    leader_id: str | None = None
    ai_enhanced_selection: bool = False   # AI-enhanced leader election

    @property
    def quorum(self) -> int:
        """2f+1 where f = floor((n-1)/3)."""
        f = (self.total_nodes - 1) // 3
        return 2 * f + 1

    @property
    def consensus_reached(self) -> bool:
        """True when at least quorum nodes have voted with the same hash."""
        if not self.votes:
            return False
        from collections import Counter
        tally = Counter(self.votes.values())
        return tally.most_common(1)[0][1] >= self.quorum

    @property
    def majority_hash(self) -> str | None:
        """The hash with the most votes, or None if no votes."""
        if not self.votes:
            return None
        from collections import Counter
        return Counter(self.votes.values()).most_common(1)[0][0]

    def vote(self, node_id: str, vote_hash: str) -> bool:
        """Cast a vote. Returns True if consensus is now reached."""
        self.votes[node_id] = vote_hash
        return self.consensus_reached

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
