from __future__ import annotations

from argparse import Namespace

from main import _analyze_project, _run_autonomous, _run_catalog, _run_pipeline


def test_analyze_project_contains_integration_map() -> None:
    payload = _analyze_project()
    assert payload["project"] == "SDSA"
    assert "flow" in payload["analysis"]
    assert "modules" in payload["analysis"]


def test_run_pipeline_returns_ranking_and_hypotheses() -> None:
    payload = _run_pipeline(
        Namespace(
            objective="test main",
            domain="energy_storage",
            budget=4,
            kg_in=None,
            kg_out=None,
        )
    )
    assert payload["mode"] == "run"
    assert payload["ranking"]
    assert payload["hypotheses"]


def test_catalog_and_autonomous_modes() -> None:
    catalog = _run_catalog(Namespace(domain="energy_storage", horizon=None, keyword=None, limit=5))
    assert catalog["mode"] == "catalog"
    assert catalog["count"] == 5

    autonomous = _run_autonomous(Namespace(objective="invent", cycles=2, budget=3))
    assert autonomous["mode"] == "autonomous"
    assert autonomous["cycles"] == 2
    assert len(autonomous["history"]) == 2
