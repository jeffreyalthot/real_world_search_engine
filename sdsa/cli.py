from __future__ import annotations

import argparse
import json

from sdsa.core.orchestrator import SdsaOrchestrator
from sdsa.services.hypothesis_engine import HypothesisEngine
from sdsa.services.knowledge_graph import KnowledgeGraphService
from sdsa.services.objective_service import ObjectiveBlueprintService
from sdsa.sim.physics_engine import PhysicsEngine
from sdsa.utils.bootstrap import seed_knowledge_graph


def build_orchestrator(kg_path: str | None = None) -> SdsaOrchestrator:
    kg = KnowledgeGraphService()
    if kg_path:
        kg.load_json(kg_path)
    else:
        seed_knowledge_graph(kg)
    return SdsaOrchestrator(kg, HypothesisEngine(), PhysicsEngine())


def main() -> None:
    parser = argparse.ArgumentParser(description="SDSA prototype CLI")
    parser.add_argument("--objective", default="Batterie haute densité, sûre, faible coût")
    parser.add_argument("--domain", default="energy_storage")
    parser.add_argument("--budget", type=int, default=5)
    parser.add_argument("--kg-in", default=None, help="Chemin vers un fichier JSON de claims à charger")
    parser.add_argument("--kg-out", default=None, help="Chemin de sauvegarde du knowledge graph en JSON")
    parser.add_argument("--list-objective-packs", action="store_true", help="Afficher un résumé des packs d'objectifs")
    parser.add_argument("--objective-pack-domain", default=None, help="Domaine pour sélectionner automatiquement un objectif")
    parser.add_argument("--objective-pack-index", type=int, default=0, help="Index de l'objectif dans le pack de domaine")
    args = parser.parse_args()


    objective_service = ObjectiveBlueprintService()
    if args.list_objective_packs:
        summaries = [
            {
                "domain": summary.domain,
                "total": summary.total,
                "horizons": summary.horizons,
            }
            for summary in objective_service.summarize()
        ]
        print(json.dumps({"objective_packs": summaries}, indent=2, ensure_ascii=False))
        return

    resolved_objective = args.objective
    resolved_domain = args.domain
    if args.objective_pack_domain:
        candidates = objective_service.by_domain(args.objective_pack_domain, limit=2000)
        if not candidates:
            raise SystemExit(f"Aucun objectif disponible pour le domaine: {args.objective_pack_domain}")
        selected = candidates[args.objective_pack_index % len(candidates)]
        resolved_objective = objective_service.to_objective_statement(selected)
        resolved_domain = selected["domain"]

    orchestrator = build_orchestrator(kg_path=args.kg_in)
    output = orchestrator.run(objective=resolved_objective, domain=resolved_domain, budget=args.budget)
    if args.kg_out:
        orchestrator.kg.save_json(args.kg_out)
    print(json.dumps({"objective": output.objective, "ranking": output.ranking}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
