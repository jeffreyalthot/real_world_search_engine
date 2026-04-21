from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from sdsa.core.models import ConfidenceLevel, ProvenanceRef, ScientificClaim


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

    def save_json(self, path: str | Path) -> None:
        claims_payload = []
        for claim in self._claims.values():
            claims_payload.append(
                {
                    "claim_id": claim.claim_id,
                    "statement": claim.statement,
                    "domain": claim.domain,
                    "confidence": claim.confidence.value,
                    "supports": claim.supports,
                    "contradicts": claim.contradicts,
                    "provenance": [
                        {
                            "source_id": ref.source_id,
                            "source_type": ref.source_type,
                            "version": ref.version,
                            "created_at": ref.created_at.isoformat(),
                        }
                        for ref in claim.provenance
                    ],
                }
            )

        output = {"claims": claims_payload}
        Path(path).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_json(self, path: str | Path) -> None:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        self._claims.clear()
        self._by_domain.clear()
        for claim_data in raw.get("claims", []):
            claim = ScientificClaim(
                claim_id=claim_data["claim_id"],
                statement=claim_data["statement"],
                domain=claim_data["domain"],
                confidence=ConfidenceLevel(claim_data["confidence"]),
                supports=claim_data.get("supports", []),
                contradicts=claim_data.get("contradicts", []),
                provenance=[
                    ProvenanceRef(
                        source_id=ref["source_id"],
                        source_type=ref["source_type"],
                        version=ref["version"],
                        created_at=datetime.fromisoformat(ref["created_at"]),
                    )
                    for ref in claim_data.get("provenance", [])
                ],
            )
            self.add_claim(claim)
