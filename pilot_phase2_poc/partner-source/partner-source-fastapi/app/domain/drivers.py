from dataclasses import dataclass
from enum import Enum

class DriverAvailabilityStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    OFFLINE = "OFFLINE"

@dataclass(frozen=True)
class DeliveryDriver:
    driver_id: str
    display_name: str
    availability_status: DriverAvailabilityStatus

