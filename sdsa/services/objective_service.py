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
