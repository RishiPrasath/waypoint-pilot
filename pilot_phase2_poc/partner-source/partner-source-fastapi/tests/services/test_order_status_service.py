from app.repositories.orders import InMemoryOrderRepository
from app.seed.loader import load_seed_data
from app.services.order_status import OrderStatusService


def test_get_order_status_for_seeded_order() -> None:
    service = OrderStatusService(InMemoryOrderRepository(load_seed_data()))

    response = service.get_order_status("ORD-1001")

    assert response is not None
    assert response.orderId == "ORD-1001"
    assert response.currentStatus == "OUT_FOR_DELIVERY"
    assert response.deliveryWindow is not None
    assert response.assignedDriver is not None
    assert response.assignedDriver.driverId == "DRV-2001"


def test_missing_order_returns_none() -> None:
    service = OrderStatusService(InMemoryOrderRepository(load_seed_data()))

    assert service.get_order_status("ORD-9999") is None
