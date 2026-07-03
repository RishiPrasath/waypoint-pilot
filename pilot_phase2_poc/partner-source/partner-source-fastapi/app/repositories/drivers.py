from app.domain.drivers import DeliveryDriver
from app.seed.store import SeedDataStore


class InMemoryDriverRepository:
    def __init__(self, store: SeedDataStore) -> None:
        self._store = store

    def find_by_id(self, driver_id: str) -> DeliveryDriver | None:
        return self._store.drivers.get(driver_id)