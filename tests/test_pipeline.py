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
