from dataclasses import dataclass
from app.domain.assignments import DeliveryAssignment
from app.domain.drivers import DeliveryDriver
from app.domain.orders import DeliveryOrder,OrderStatusEvent


@dataclass(frozen=True)
class SeedDataStore:
    orders: dict[str,DeliveryOrder]
    drivers: dict[str,DeliveryDriver]
    assignments: dict[str,DeliveryAssignment]
    status_events_by_order_id:dict[str,list[OrderStatusEvent]]


    