import pytest

from app.domain.orders import OrderStatus
from app.errors.exceptions import DriverNotFoundError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.seed.loader import load_seed_data
from app.services.driver_assignments import DriverAssignmentsService


def build_service() -> DriverAssignmentsService:
    store = load_seed_data()
    return DriverAssignmentsService(
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
        InMemoryOrderRepository(store),
    )


def test_list_active_assignments_for_driver() -> None:
    service = build_service()

    response = service.list_assignments("DRV-2001", None, page=1, page_size=20)

    assert response.driverId == "DRV-2001"
    assert response.totalItems == 2
    assert [item.orderId for item in response.items] == ["ORD-1001", "ORD-1002"]


def test_available_driver_with_no_work_returns_empty_page() -> None:
    service = build_service()

    response = service.list_assignments("DRV-2003", None, page=1, page_size=20)

    assert response.items == []
    assert response.totalItems == 0


def test_status_filter_limits_assignments() -> None:
    service = build_service()

    response = service.list_assignments("DRV-2001", OrderStatus.IN_TRANSIT, page=1, page_size=20)

    assert response.totalItems == 1
    assert response.items[0].orderId == "ORD-1002"


def test_missing_driver_raises_driver_not_found() -> None:
    service = build_service()

    with pytest.raises(DriverNotFoundError):
        service.list_assignments("DRV-9999", None, page=1, page_size=20)
