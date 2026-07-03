from app.domain.orders import DeliveryOrder
from app.seed.store import SeedDataStore


class InMemoryOrderRepository:
    def __init__(self, store: SeedDataStore) -> None:
        self._store = store

    def find_by_id(self, order_id: str) -> DeliveryOrder | None:
        return self._store.orders.get(order_id)

    def save(self, order: DeliveryOrder) -> None:
        self._store.orders[order.order_id] = order