from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from typing import Any

from sdsa.cli import build_orchestrator
from sdsa.gui.app import main as launch_gui
from sdsa.services.autonomous_creator import AutonomousCreator
from sdsa.services.objective_service import ObjectiveBlueprintService


PROJECT_MODULES: dict[str, list[str]] = {
    "entrypoints": ["main.py", "sdsa/cli.py", "sdsa/gui/app.py"],
    "core": ["sdsa/core/models.py", "sdsa/core/orchestrator.py"],
    "services": [
        "sdsa/services/knowledge_graph.py",
        "sdsa/services/hypothesis_engine.py",
        "sdsa/services/objective_service.py",
        "sdsa/services/autonomous_creator.py",
    ],
    "simulation": ["sdsa/sim/physics_engine.py"],
    "catalog": [
        "sdsa/catalog/objective_blueprints.py",
        "sdsa/catalog/objective_blueprints_phase2.py",
        "sdsa/catalog/objective_blueprints_phase3.py",
    ],
    "utils": ["sdsa/utils/bootstrap.py"],
    "tests": [
        "tests/test_pipeline.py",
        "tests/test_autonomous_creator.py",
        "tests/test_objective_service.py",
    ],
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Point d'entrée racine SDSA: analyse, exécution pipeline, mode autonome et GUI."
    )
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Exécuter 1 cycle pipeline SDSA")
    run_parser.add_argument("--objective", default="Batterie haute densité, sûre, faible coût")
    run_parser.add_argument("--domain", default="energy_storage")
    run_parser.add_argument("--budget", type=int, default=5)
    run_parser.add_argument("--kg-in", default=None)
    run_parser.add_argument("--kg-out", default=None)

    catalog_parser = subparsers.add_parser("catalog", help="Explorer le catalogue d'objectifs")
    catalog_parser.add_argument("--domain", default=None)
    catalog_parser.add_argument("--horizon", default=None)
    catalog_parser.add_argument("--keyword", default=None)
    catalog_parser.add_argument("--limit", type=int, default=10)

    autonomous_parser = subparsers.add_parser("autonomous", help="Exécuter N cycles d'invention")
    autonomous_parser.add_argument("--objective", default="Créer un système innovant industrialisable")
    autonomous_parser.add_argument("--cycles", type=int, default=3)
    autonomous_parser.add_argument("--budget", type=int, default=6)

    subparsers.add_parser("analyze", help="Afficher l'analyse d'architecture et points de liaison")
    subparsers.add_parser("gui", help="Lancer l'interface Tkinter")

    return parser.parse_args()


def _analyze_project() -> dict[str, Any]:
    objective_service = ObjectiveBlueprintService()
    domains = objective_service.list_domains()
    sample_domain = domains[0] if domains else "energy_storage"

    return {
        "project": "SDSA",
        "analysis": {
            "flow": [
                "KnowledgeGraphService (claims)",
                "HypothesisEngine (génération contrainte)",
                "PhysicsEngine (simulation et KPI)",
                "SdsaOrchestrator (classement risque/performance)",
                "AutonomousCreator (boucle récursive + blueprint)",
                "GUI/CLI/Main (orchestration utilisateur)",
            ],
            "modules": PROJECT_MODULES,
            "catalog": {
                "total_blueprints": objective_service.total_blueprints(),
                "domains": len(domains),
                "sample_domain": sample_domain,
                "sample_roadmap_horizons": list(objective_service.roadmap_by_domain(sample_domain).keys()),
            },
            "integration_contracts": {
                "orchestrator_input": ["objective", "domain", "budget"],
                "orchestrator_output": ["objective", "hypotheses", "ranking"],
                "ranking_fields": ["hypothesis_id", "performance", "risk", "cost"],
            },
        },
    }


def _run_pipeline(args: argparse.Namespace) -> dict[str, Any]:
    orchestrator = build_orchestrator(kg_path=args.kg_in)
    output = orchestrator.run(objective=args.objective, domain=args.domain, budget=max(1, args.budget))
    if args.kg_out:
        orchestrator.kg.save_json(args.kg_out)

    return {
        "mode": "run",
        "objective": output.objective,
        "hypotheses": [asdict(h) for h in output.hypotheses],
        "ranking": output.ranking,
    }


def _run_catalog(args: argparse.Namespace) -> dict[str, Any]:
    service = ObjectiveBlueprintService()

    if args.keyword:
        results = service.search_by_keyword(args.keyword, limit=max(1, args.limit))
    elif args.horizon:
        results = service.by_horizon(args.horizon, limit=max(1, args.limit))
    elif args.domain:
        results = service.by_domain(args.domain, limit=max(1, args.limit))
    else:
        results = service.diversified_batch(limit=max(1, args.limit))

    return {
        "mode": "catalog",
        "count": len(results),
        "results": results,
        "summary": [asdict(summary) for summary in service.summarize()],
    }


def _run_autonomous(args: argparse.Namespace) -> dict[str, Any]:
    creator = AutonomousCreator(build_orchestrator())
    history: list[dict[str, Any]] = []

    for _ in range(max(1, args.cycles)):
        output, blueprint = creator.run_cycle(args.objective, budget=max(1, args.budget))
        history.append(
            {
                "cycle": creator.cycle_count,
                "top_ranking": output.ranking[:3],
                "blueprint": asdict(blueprint),
            }
        )

    return {
        "mode": "autonomous",
        "cycles": creator.cycle_count,
        "known_concepts": creator.known_concepts,
        "history": history,
    }


def main() -> None:
    args = _parse_args()

    if args.command == "gui":
        launch_gui()
        return

    if args.command == "analyze" or args.command is None:
        payload = _analyze_project()
    elif args.command == "run":
        payload = _run_pipeline(args)
    elif args.command == "catalog":
        payload = _run_catalog(args)
    elif args.command == "autonomous":
        payload = _run_autonomous(args)
    else:
        raise SystemExit(f"Commande non supportée: {args.command}")

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
