from app.domain.orders import OrderStatusEvent
from app.seed.store import SeedDataStore


class InMemoryStatusEventRepository:
    def __init__(self, store: SeedDataStore) -> None:
        self._store = store

    def find_by_order_id(self, order_id: str) -> list[OrderStatusEvent]:
        return sorted(
            self._store.status_events_by_order_id.get(order_id, []),
            key=lambda event: event.occurred_at,
        )

    def append(self, event: OrderStatusEvent) -> None:
        self._store.status_events_by_order_id.setdefault(event.order_id, []).append(event)