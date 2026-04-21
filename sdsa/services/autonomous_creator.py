from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from sdsa.core.orchestrator import PipelineOutput, SdsaOrchestrator


@dataclass(slots=True)
class DetailedBlueprint:
    blueprint_id: str
    created_at: str
    title: str
    objective: str
    concept_summary: str
    real_world_constraints: Dict[str, str]
    required_materials: List[str]
    required_processes: List[str]
    validation_protocol: List[str]
    human_readable_plan: str


class AutonomousCreator:
    """Boucle d'invention continue + génération de plans lisibles humains."""

    def __init__(self, orchestrator: SdsaOrchestrator) -> None:
        self.orchestrator = orchestrator
        self._cycle = 0
        self._known_concepts: list[str] = []

    @property
    def cycle_count(self) -> int:
        return self._cycle

    @property
    def known_concepts(self) -> list[str]:
        return list(self._known_concepts)

    def run_cycle(self, objective_seed: str, budget: int = 6) -> tuple[PipelineOutput, DetailedBlueprint]:
        self._cycle += 1
        objective = self._compose_recursive_objective(objective_seed)
        output = self.orchestrator.run(objective=objective, budget=budget)

        ranking_hint = output.ranking[0] if output.ranking else {}
        concept_id = str(ranking_hint.get("hypothesis_id", f"cycle-{self._cycle}"))
        self._known_concepts.append(concept_id)

        blueprint = self._build_blueprint(objective=objective, output=output, concept_id=concept_id)
        return output, blueprint

    def _compose_recursive_objective(self, objective_seed: str) -> str:
        if not self._known_concepts:
            return objective_seed
        recent = ", ".join(self._known_concepts[-3:])
        return (
            f"{objective_seed} | réutiliser concepts antérieurs [{recent}] pour créer une architecture"
            " plus complexe, industrialisable et vérifiable"
        )

    def _build_blueprint(self, objective: str, output: PipelineOutput, concept_id: str) -> DetailedBlueprint:
        created_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        constraints = {
            "physique": "Respect strict conservation masse/énergie, stabilité thermo-mécanique en plage nominale.",
            "sécurité": "Aucune réaction incontrôlée; marge de sécurité >= 20% sur limites critiques.",
            "coût": "Capex et Opex tracés; cible de coût proxy décroissante cycle après cycle.",
            "fabrication": "Procédé reproductible, tolérances mesurables, matériaux disponibles industriellement.",
            "réglementaire": "Traçabilité des décisions et conformité sécurité produit/documentation technique.",
            "durabilité": "Cycle de vie estimé: extraction, fabrication, usage, fin de vie, recyclabilité.",
        }

        top = output.ranking[:3]
        top_lines = [
            f"- {row['hypothesis_id']} | perf={row['performance']} | risque={row['risk']} | coût={row['cost']}"
            for row in top
        ]
        if not top_lines:
            top_lines = ["- Aucun candidat simulé"]

        plan = "\n".join(
            [
                f"Blueprint: {concept_id}",
                f"Date UTC: {created_at}",
                f"Objectif: {objective}",
                "",
                "1) Définition du besoin",
                "   - Mesure principale à optimiser.",
                "   - Seuil d'acceptation quantifié.",
                "",
                "2) Contraintes monde réel",
                *[f"   - {k}: {v}" for k, v in constraints.items()],
                "",
                "3) Concepts simulés prioritaires",
                *top_lines,
                "",
                "4) Plan de réalisation détaillé",
                "   - Conception CAO et schémas d'assemblage.",
                "   - BOM complète et alternative fournisseurs.",
                "   - Procédure de fabrication étape par étape.",
                "   - Protocole de test (sécurité, performance, vieillissement).",
                "   - Critères go/no-go + actions correctives.",
                "",
                "5) Boucle d'amélioration infinie",
                "   - Réinjecter ce blueprint et les mesures réelles dans le cycle suivant.",
                "   - Générer version N+1 plus complexe, sans perdre explicabilité.",
            ]
        )

        return DetailedBlueprint(
            blueprint_id=concept_id,
            created_at=created_at,
            title=f"Plan détaillé cycle {self._cycle}",
            objective=objective,
            concept_summary="Concept généré automatiquement avec priorisation perf/risque/coût.",
            real_world_constraints=constraints,
            required_materials=[
                "Matériaux standard industrialisables",
                "Capteurs de validation",
                "Outillage fabrication et métrologie",
            ],
            required_processes=[
                "Simulation multi-physique",
                "Prototypage",
                "Essais de qualification",
                "Revues sécurité & conformité",
            ],
            validation_protocol=[
                "Test de performance nominale",
                "Test de robustesse conditions extrêmes",
                "Analyse de risque et modes de défaillance",
                "Validation de reproductibilité",
            ],
            human_readable_plan=plan,
        )
