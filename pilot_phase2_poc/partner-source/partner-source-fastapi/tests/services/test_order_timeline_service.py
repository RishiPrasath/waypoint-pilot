from app.repositories.orders import InMemoryOrderRepository
from app.repositories.status_events import InMemoryStatusEventRepository
from app.seed.loader import load_seed_data
from app.services.order_timeline import OrderTimelineService


def test_get_order_timeline_returns_chronological_events() -> None:
    store = load_seed_data()
    service = OrderTimelineService(
        InMemoryOrderRepository(store),
        InMemoryStatusEventRepository(store),
    )

    response = service.get_timeline("ORD-1001", page=1, page_size=20)

    assert response.orderId == "ORD-1001"
    assert [item.eventId for item in response.items] == [
        "EVT-4001",
        "EVT-4002",
        "EVT-4003",
        "EVT-4004",
        "EVT-4005",
    ]
    assert response.totalItems == 5
