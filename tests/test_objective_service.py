from sdsa.catalog.objective_blueprints import OBJECTIVE_BLUEPRINTS
from sdsa.services.objective_service import ObjectiveBlueprintService


def test_blueprint_catalog_is_massive() -> None:
    assert len(OBJECTIVE_BLUEPRINTS) == 2400


def test_service_can_list_domains_and_filter() -> None:
    service = ObjectiveBlueprintService()
    domains = service.list_domains()
    assert "energy_storage" in domains

    batch = service.by_domain("energy_storage", limit=7)
    assert len(batch) == 7
    assert all(item["domain"] == "energy_storage" for item in batch)


def test_service_summary_and_statement() -> None:
    service = ObjectiveBlueprintService()
    summaries = service.summarize()
    assert summaries

    first_domain = summaries[0].domain
    sample = service.by_domain(first_domain, limit=1)[0]
    statement = service.to_objective_statement(sample)

    assert sample["title"] in statement
    assert "cible=" in statement
    assert "barrière=" in statement


def test_filter_by_horizon_and_keyword_search() -> None:
    service = ObjectiveBlueprintService()

    horizon_batch = service.by_horizon("court_terme", limit=12)
    assert len(horizon_batch) == 12
    assert all(item["horizon"] == "court_terme" for item in horizon_batch)

    keyword_hits = service.search_by_keyword("window_2028", limit=15)
    assert len(keyword_hits) == 15
    assert all("window_2028" in item["keywords"] for item in keyword_hits)


def test_diversified_batch_covers_multiple_domains() -> None:
    service = ObjectiveBlueprintService()
    diversified = service.diversified_batch(limit=18)

    assert len(diversified) == 18
    domains = {item["domain"] for item in diversified}
    assert len(domains) >= 6
