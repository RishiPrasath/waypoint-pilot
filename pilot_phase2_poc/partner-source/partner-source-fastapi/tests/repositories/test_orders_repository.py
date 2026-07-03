from app.domain.orders import OrderStatus
from app.repositories.orders import InMemoryOrderRepository
from app.seed.loader import load_seed_data


def test_find_existing_order_by_id() -> None:
    repo = InMemoryOrderRepository(load_seed_data())

    order = repo.find_by_id("ORD-1001")

    assert order is not None
    assert order.order_id == "ORD-1001"
    assert order.current_status == OrderStatus.OUT_FOR_DELIVERY


def test_missing_order_returns_none() -> None:
    repo = InMemoryOrderRepository(load_seed_data())

    assert repo.find_by_id("ORD-9999") is None
