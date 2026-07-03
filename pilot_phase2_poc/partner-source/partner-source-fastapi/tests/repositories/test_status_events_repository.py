from app.domain.orders import OrderStatus
from app.repositories.status_events import InMemoryStatusEventRepository
from app.seed.loader import load_seed_data


def test_find_order_status_events_in_chronological_order() -> None:
    repo = InMemoryStatusEventRepository(load_seed_data())

    events = repo.find_by_order_id("ORD-1001")

    assert [event.event_id for event in events] == [
        "EVT-4001",
        "EVT-4002",
        "EVT-4003",
        "EVT-4004",
        "EVT-4005",
    ]
    assert events[-1].new_status == OrderStatus.OUT_FOR_DELIVERY


def test_missing_order_status_events_returns_empty_list() -> None:
    repo = InMemoryStatusEventRepository(load_seed_data())

    assert repo.find_by_order_id("ORD-9999") == []
