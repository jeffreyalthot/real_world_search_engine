from sdsa.catalog.objective_blueprints import OBJECTIVE_BLUEPRINTS
from sdsa.services.objective_service import ObjectiveBlueprintService


def test_blueprint_catalog_is_massive() -> None:
    assert len(OBJECTIVE_BLUEPRINTS) == 900


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
