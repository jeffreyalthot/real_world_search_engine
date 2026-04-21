from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List

from sdsa.catalog.objective_blueprints import OBJECTIVE_BLUEPRINTS, ObjectiveBlueprint


@dataclass(slots=True)
class ObjectivePackSummary:
    domain: str
    total: int
    horizons: Dict[str, int]


class ObjectiveBlueprintService:
    """Accès aux blueprints d'objectifs pour accélérer l'exploration produit."""

    def __init__(self, blueprints: Iterable[ObjectiveBlueprint] | None = None) -> None:
        self._blueprints: List[ObjectiveBlueprint] = list(blueprints or OBJECTIVE_BLUEPRINTS)

    def list_domains(self) -> list[str]:
        return sorted({bp["domain"] for bp in self._blueprints})

    def by_domain(self, domain: str, limit: int = 20) -> list[ObjectiveBlueprint]:
        filtered = [bp for bp in self._blueprints if bp["domain"] == domain]
        return filtered[: max(1, limit)]

    def by_horizon(self, horizon: str, limit: int = 20) -> list[ObjectiveBlueprint]:
        filtered = [bp for bp in self._blueprints if bp["horizon"] == horizon]
        return filtered[: max(1, limit)]

    def search_by_keyword(self, keyword: str, limit: int = 30) -> list[ObjectiveBlueprint]:
        normalized = keyword.strip().lower()
        if not normalized:
            return []
        filtered = [
            bp
            for bp in self._blueprints
            if any(normalized in token.lower() for token in bp["keywords"])
            or normalized in bp["title"].lower()
            or normalized in bp["mechanism_hint"].lower()
        ]
        return filtered[: max(1, limit)]

    def diversified_batch(self, limit: int = 24) -> list[ObjectiveBlueprint]:
        """Retourne un lot équilibré par domaine pour exploration initiale."""
        capped_limit = max(1, limit)
        buckets: dict[str, list[ObjectiveBlueprint]] = defaultdict(list)
        for bp in self._blueprints:
            buckets[bp["domain"]].append(bp)

        ordered_domains = sorted(buckets)
        result: list[ObjectiveBlueprint] = []
        index = 0
        while len(result) < capped_limit and ordered_domains:
            domain = ordered_domains[index % len(ordered_domains)]
            bucket = buckets[domain]
            pick_index = len(result) // len(ordered_domains)
            if pick_index < len(bucket):
                result.append(bucket[pick_index])
            index += 1
            if index > capped_limit * len(ordered_domains) * 2:
                # borne de sécurité pour éviter toute boucle prolongée
                break
        return result[:capped_limit]

    def summarize(self) -> list[ObjectivePackSummary]:
        counters: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for bp in self._blueprints:
            counters[bp["domain"]][bp["horizon"]] += 1

        summaries: list[ObjectivePackSummary] = []
        for domain, horizons in sorted(counters.items()):
            summaries.append(
                ObjectivePackSummary(
                    domain=domain,
                    total=sum(horizons.values()),
                    horizons=dict(sorted(horizons.items())),
                )
            )
        return summaries

    def to_objective_statement(self, blueprint: ObjectiveBlueprint) -> str:
        keys = ", ".join(blueprint["keywords"])
        return (
            f"{blueprint['title']} | cible={blueprint['target_metric']} | "
            f"barrière={blueprint['risk_guardrail']} | horizon={blueprint['horizon']} | "
            f"mots-clés={keys}"
        )
