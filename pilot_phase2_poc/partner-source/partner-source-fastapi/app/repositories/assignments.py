from app.domain.assignments import DeliveryAssignment, DeliveryAssignmentStatus
from app.seed.manifest import ACTIVE_SLICE_1_ASSIGNMENT_IDS
from app.seed.store import SeedDataStore


class InMemoryAssignmentRepository:
    def __init__(self, store: SeedDataStore) -> None:
        self._store = store

    def find_by_driver_id(self, driver_id: str) -> list[DeliveryAssignment]:
        return [
            assignment
            for assignment in self._store.assignments.values()
            if assignment.driver_id == driver_id
            and assignment.assignment_id in ACTIVE_SLICE_1_ASSIGNMENT_IDS
            and assignment.status in {
                DeliveryAssignmentStatus.ASSIGNED,
                DeliveryAssignmentStatus.ACCEPTED,
            }
        ]

    def find_by_order_id(self, order_id: str) -> list[DeliveryAssignment]:
        return [
            assignment
            for assignment in self._store.assignments.values()
            if assignment.order_id == order_id
        ]

    def find_all(self) -> list[DeliveryAssignment]:
        return list(self._store.assignments.values())
