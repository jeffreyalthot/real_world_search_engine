from __future__ import annotations

import argparse
import json

from sdsa.core.orchestrator import SdsaOrchestrator
from sdsa.services.hypothesis_engine import HypothesisEngine
from sdsa.services.knowledge_graph import KnowledgeGraphService
from sdsa.sim.physics_engine import PhysicsEngine
from sdsa.utils.bootstrap import seed_knowledge_graph


def build_orchestrator() -> SdsaOrchestrator:
    kg = KnowledgeGraphService()
    seed_knowledge_graph(kg)
    return SdsaOrchestrator(kg, HypothesisEngine(), PhysicsEngine())


def main() -> None:
    parser = argparse.ArgumentParser(description="SDSA prototype CLI")
    parser.add_argument("--objective", default="Batterie haute densité, sûre, faible coût")
    parser.add_argument("--domain", default="energy_storage")
    parser.add_argument("--budget", type=int, default=5)
    args = parser.parse_args()

    orchestrator = build_orchestrator()
    output = orchestrator.run(objective=args.objective, domain=args.domain, budget=args.budget)
    print(json.dumps({"objective": output.objective, "ranking": output.ranking}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
