import json

from sdsa.cli import build_orchestrator


def test_pipeline_returns_ranking() -> None:
    orchestrator = build_orchestrator()
    output = orchestrator.run(objective="test", budget=4)
    assert output.objective == "test"
    assert len(output.ranking) == 3
    assert all("hypothesis_id" in entry for entry in output.ranking)


def test_ranking_sorted_by_risk_then_performance() -> None:
    orchestrator = build_orchestrator()
    output = orchestrator.run(objective="tri", budget=3)
    ranking = output.ranking
    assert ranking == sorted(ranking, key=lambda x: (float(x["risk"]), -float(x["performance"])))


def test_knowledge_graph_can_be_saved_and_reloaded(tmp_path) -> None:
    kg_file = tmp_path / "kg.json"

    orchestrator = build_orchestrator()
    orchestrator.kg.save_json(kg_file)

    saved_data = json.loads(kg_file.read_text(encoding="utf-8"))
    assert len(saved_data["claims"]) == 3

    loaded_orchestrator = build_orchestrator(kg_path=str(kg_file))
    loaded_output = loaded_orchestrator.run(objective="reload", budget=3)
    assert len(loaded_output.hypotheses) == 3
