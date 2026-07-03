from dataclasses import dataclass
from enum import Enum

class DeliveryAssignmentStatus(str, Enum):
    ASSIGNED = "ASSIGNED"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class DeliveryAssignment:
    driver_id: str
    order_id: str
    status: DeliveryAssignmentStatus = DeliveryAssignmentStatus.ASSIGNED
    assignment_id: str | None = None
