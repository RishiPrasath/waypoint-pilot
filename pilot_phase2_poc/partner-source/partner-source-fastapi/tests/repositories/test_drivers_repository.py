from app.domain.drivers import DriverAvailabilityStatus
from app.repositories.drivers import InMemoryDriverRepository
from app.seed.loader import load_seed_data


def test_find_existing_driver_by_id() -> None:
    repo = InMemoryDriverRepository(load_seed_data())

    driver = repo.find_by_id("DRV-2001")

    assert driver is not None
    assert driver.driver_id == "DRV-2001"
    assert driver.availability_status == DriverAvailabilityStatus.AVAILABLE


def test_missing_driver_returns_none() -> None:
    repo = InMemoryDriverRepository(load_seed_data())

    assert repo.find_by_id("DRV-9999") is None
