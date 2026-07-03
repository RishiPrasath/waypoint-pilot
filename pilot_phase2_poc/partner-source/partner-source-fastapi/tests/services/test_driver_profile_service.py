import pytest

from app.errors.exceptions import DriverNotFoundError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.seed.loader import load_seed_data
from app.services.driver_profile import DriverProfileService


def test_get_driver_profile_counts_active_assignments() -> None:
    store = load_seed_data()
    service = DriverProfileService(
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
    )

    response = service.get_driver("DRV-2001")

    assert response.driverId == "DRV-2001"
    assert response.availabilityStatus == "AVAILABLE"
    assert response.activeAssignmentCount == 2


def test_missing_driver_raises_driver_not_found() -> None:
    store = load_seed_data()
    service = DriverProfileService(
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
    )

    with pytest.raises(DriverNotFoundError):
        service.get_driver("DRV-9999")
