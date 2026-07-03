from app.seed.store import SeedDataStore
from app.services import readiness as readiness_module
from app.services.readiness import ReadinessService


def test_readiness_service_reports_seed_data_ready() -> None:
    checks = ReadinessService().check()

    assert checks == {
        "persistence": "UP",
        "seedData": "UP",
    }


def test_readiness_service_reports_not_ready_when_timeline_seeds_are_missing(
    monkeypatch,
) -> None:
    store = SeedDataStore(
        orders={"ORD-1": object()},
        drivers={"DRV-1": object()},
        assignments={"ASN-1": object()},
        status_events_by_order_id={},
    )
    monkeypatch.setattr(readiness_module, "load_seed_data", lambda: store)

    checks = ReadinessService().check()

    assert checks == {
        "persistence": "UP",
        "seedData": "DOWN",
    }
