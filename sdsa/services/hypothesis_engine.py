from __future__ import annotations

import hashlib
from typing import Dict, Iterable, List

from sdsa.core.models import Hypothesis, ScientificClaim


class HypothesisEngine:
    """Génération contrainte d'hypothèses à partir de claims."""

    def generate(
        self,
        objective: str,
        claims: Iterable[ScientificClaim],
        hard_constraints: Dict[str, str],
        limit: int = 20,
    ) -> List[Hypothesis]:
        hypotheses: List[Hypothesis] = []
        for index, claim in enumerate(claims):
            if len(hypotheses) >= limit:
                break
            mechanism = f"Exploiter '{claim.statement}' pour atteindre: {objective}"
            digest = hashlib.sha1(f"{objective}:{claim.claim_id}:{index}".encode()).hexdigest()[:12]
            novelty = min(0.99, 0.4 + 0.05 * index)
            testability = max(0.1, 0.95 - 0.03 * index)
            hypotheses.append(
                Hypothesis(
                    hypothesis_id=f"hyp-{digest}",
                    objective=objective,
                    mechanism=mechanism,
                    constraints=hard_constraints,
                    novelty_score=round(novelty, 3),
                    testability_score=round(testability, 3),
                )
            )
        return hypotheses
