from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from sdsa.core.models import Hypothesis, SimulationSpec
from sdsa.services.hypothesis_engine import HypothesisEngine
from sdsa.services.knowledge_graph import KnowledgeGraphService
from sdsa.sim.physics_engine import PhysicsEngine


@dataclass(slots=True)
class PipelineOutput:
    objective: str
    hypotheses: List[Hypothesis]
    ranking: List[Dict[str, float | str]]


class SdsaOrchestrator:
    def __init__(
        self,
        kg: KnowledgeGraphService,
        hypothesis_engine: HypothesisEngine,
        physics_engine: PhysicsEngine,
    ) -> None:
        self.kg = kg
        self.hypothesis_engine = hypothesis_engine
        self.physics_engine = physics_engine

    def run(self, objective: str, domain: str = "energy_storage", budget: int = 5) -> PipelineOutput:
        claims = self.kg.list_claims(domain=domain)
        hypotheses = self.hypothesis_engine.generate(
            objective=objective,
            claims=claims,
            hard_constraints={
                "units": "si_only",
                "safety": "must_pass",
                "conservation": "strict",
            },
            limit=max(1, budget),
        )

        ranking: List[Dict[str, float | str]] = []
        for idx, hyp in enumerate(hypotheses):
            result = self.physics_engine.run(
                SimulationSpec(
                    simulation_id=f"sim-{idx:03d}",
                    hypothesis_id=hyp.hypothesis_id,
                    physics_domains=["thermal", "electrochemical", "mechanical"],
                    fidelity="low" if idx > 2 else "medium",
                    solver="prototype_solver_v1",
                )
            )
            ranking.append(
                {
                    "hypothesis_id": hyp.hypothesis_id,
                    "performance": result.kpis["performance_index"],
                    "risk": result.kpis["risk_index"],
                    "cost": result.kpis["cost_proxy"],
                }
            )

        ranking.sort(key=lambda x: (float(x["risk"]), -float(x["performance"])))
        return PipelineOutput(objective=objective, hypotheses=hypotheses, ranking=ranking)
