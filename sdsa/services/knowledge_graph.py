from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from sdsa.core.models import ScientificClaim


class KnowledgeGraphService:
    """Stockage mémoire minimal pour prototype SDSA."""

    def __init__(self) -> None:
        self._claims: Dict[str, ScientificClaim] = {}
        self._by_domain: Dict[str, List[str]] = defaultdict(list)

    def add_claim(self, claim: ScientificClaim) -> None:
        self._claims[claim.claim_id] = claim
        self._by_domain[claim.domain].append(claim.claim_id)

    def get_claim(self, claim_id: str) -> ScientificClaim | None:
        return self._claims.get(claim_id)

    def list_claims(self, domain: str | None = None) -> List[ScientificClaim]:
        if domain is None:
            return list(self._claims.values())
        return [self._claims[cid] for cid in self._by_domain.get(domain, [])]

    def detect_contradictions(self) -> List[tuple[ScientificClaim, ScientificClaim]]:
        pairs: List[tuple[ScientificClaim, ScientificClaim]] = []
        for claim in self._claims.values():
            for contradicted_id in claim.contradicts:
                other = self._claims.get(contradicted_id)
                if other:
                    pairs.append((claim, other))
        return pairs
