from __future__ import annotations

from sdsa.core.models import ConfidenceLevel, ProvenanceRef, ScientificClaim
from sdsa.services.knowledge_graph import KnowledgeGraphService


def seed_knowledge_graph(kg: KnowledgeGraphService) -> None:
    claims = [
        ScientificClaim(
            claim_id="c1",
            statement="Les électrolytes solides sulfidés améliorent la densité énergétique volumique.",
            domain="energy_storage",
            confidence=ConfidenceLevel.MEDIUM,
            supports=[],
            contradicts=["c3"],
            provenance=[ProvenanceRef(source_id="doi:10.1000/solid-1", source_type="paper", version="1")],
        ),
        ScientificClaim(
            claim_id="c2",
            statement="La gestion thermique active réduit fortement le risque d'emballement.",
            domain="energy_storage",
            confidence=ConfidenceLevel.HIGH,
            supports=["c1"],
            contradicts=[],
            provenance=[ProvenanceRef(source_id="doi:10.1000/thermal-2", source_type="paper", version="1")],
        ),
        ScientificClaim(
            claim_id="c3",
            statement="Certains électrolytes solides augmentent la fragilité mécanique en cycle rapide.",
            domain="energy_storage",
            confidence=ConfidenceLevel.MEDIUM,
            supports=[],
            contradicts=["c1"],
            provenance=[ProvenanceRef(source_id="patent:US-EXAMPLE-1", source_type="patent", version="3")],
        ),
    ]
    for claim in claims:
        kg.add_claim(claim)
