from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERY_ATTEMPTED = "DELIVERY_ATTEMPTED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class ActorType(str, Enum):
    SYSTEM = "SYSTEM"
    DRIVER = "DRIVER"
    SUPPORT_AGENT = "SUPPORT_AGENT"


@dataclass(frozen=True)
class DeliveryOrder:
    order_id: str
    current_status: OrderStatus
    status_label: str
    recipient_name: str
    delivery_address_summary: str
    estimated_delivery_at: datetime | None = None
    delivery_window_start: datetime | None = None
    delivery_window_end: datetime | None = None
    current_location: str | None = None
    assigned_driver_id: str | None = None
    assigned_driver_name: str | None = None
    last_updated_at: datetime | None = None


@dataclass(frozen=True)
class OrderStatusEvent:
    event_id: str
    order_id: str
    previous_status: OrderStatus | None
    new_status: OrderStatus
    status_label: str
    occurred_at: datetime
    actor_type: ActorType
    actor_id: str