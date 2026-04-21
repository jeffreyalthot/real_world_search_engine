from sdsa.cli import build_orchestrator
from sdsa.services.autonomous_creator import AutonomousCreator


def test_autonomous_creator_reuses_previous_concepts() -> None:
    creator = AutonomousCreator(build_orchestrator())

    first_output, first_blueprint = creator.run_cycle("inventer un système inédit", budget=3)
    assert first_output.ranking
    assert "Contraintes monde réel" in first_blueprint.human_readable_plan

    second_output, second_blueprint = creator.run_cycle("inventer un système inédit", budget=3)
    assert second_output.ranking
    assert creator.cycle_count == 2
    assert len(creator.known_concepts) == 2
    assert "réutiliser concepts antérieurs" in second_blueprint.objective


def test_blueprint_contains_real_world_constraints() -> None:
    creator = AutonomousCreator(build_orchestrator())
    _, blueprint = creator.run_cycle("nouvelle techno", budget=3)

    assert "physique" in blueprint.real_world_constraints
    assert "sécurité" in blueprint.real_world_constraints
    assert "réglementaire" in blueprint.real_world_constraints
    assert "Boucle d'amélioration infinie" in blueprint.human_readable_plan
