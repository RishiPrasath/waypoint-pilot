from datetime import datetime, timezone

from app.domain.assignments import DeliveryAssignment, DeliveryAssignmentStatus
from app.domain.drivers import DeliveryDriver, DriverAvailabilityStatus
from app.domain.orders import ActorType, DeliveryOrder, OrderStatus, OrderStatusEvent
from app.seed.store import SeedDataStore


def _utc(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def load_seed_data() -> SeedDataStore:
    drivers = {
        "DRV-2001": DeliveryDriver("DRV-2001", "A. Kumar", DriverAvailabilityStatus.AVAILABLE),
        "DRV-2002": DeliveryDriver("DRV-2002", "B. Santos", DriverAvailabilityStatus.UNAVAILABLE),
        "DRV-2003": DeliveryDriver("DRV-2003", "C. Lee", DriverAvailabilityStatus.AVAILABLE),
    }

    orders = {
        "ORD-1001": DeliveryOrder(
            order_id="ORD-1001",
            current_status=OrderStatus.OUT_FOR_DELIVERY,
            status_label="Out for delivery",
            recipient_name="Jamie Tan",
            delivery_address_summary="Tampines, Singapore",
            assigned_driver_id="DRV-2001",
            assigned_driver_name="A. Kumar",
            last_updated_at=_utc("2026-07-02T09:00:00"),
        ),
        "ORD-1002": DeliveryOrder(
            order_id="ORD-1002",
            current_status=OrderStatus.IN_TRANSIT,
            status_label="In transit",
            recipient_name="Priya Nair",
            delivery_address_summary="Jurong East, Singapore",
            assigned_driver_id="DRV-2001",
            assigned_driver_name="A. Kumar",
            last_updated_at=_utc("2026-07-02T08:30:00"),
        ),
        "ORD-1003": DeliveryOrder(
            order_id="ORD-1003",
            current_status=OrderStatus.DELIVERED,
            status_label="Delivered",
            recipient_name="Mei Wong",
            delivery_address_summary="Woodlands, Singapore",
            assigned_driver_id="DRV-2001",
            assigned_driver_name="A. Kumar",
            last_updated_at=_utc("2026-07-01T18:00:00"),
        ),
        "ORD-1004": DeliveryOrder(
            order_id="ORD-1004",
            current_status=OrderStatus.OUT_FOR_DELIVERY,
            status_label="Out for delivery",
            recipient_name="Reserved Slice 2",
            delivery_address_summary="Singapore",
            assigned_driver_id="DRV-2001",
            assigned_driver_name="A. Kumar",
            last_updated_at=_utc("2026-07-02T10:00:00"),
        ),
    }

    assignments = {
        "ASN-3001": DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1001",
            status=DeliveryAssignmentStatus.ASSIGNED,
            assignment_id="ASN-3001",
        ),
        "ASN-3002": DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1002",
            status=DeliveryAssignmentStatus.ASSIGNED,
            assignment_id="ASN-3002",
        ),
        "ASN-3003": DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1003",
            status=DeliveryAssignmentStatus.COMPLETED,
            assignment_id="ASN-3003",
        ),
        "ASN-3004": DeliveryAssignment(
            driver_id="DRV-2001",
            order_id="ORD-1004",
            status=DeliveryAssignmentStatus.ASSIGNED,
            assignment_id="ASN-3004",
        ),
    }

    status_events_by_order_id = {
        "ORD-1001": [
            OrderStatusEvent(
                "EVT-4001",
                "ORD-1001",
                None,
                OrderStatus.CREATED,
                "Created",
                _utc("2026-07-02T05:00:00"),
                ActorType.SYSTEM,
                "system",
            ),
            OrderStatusEvent(
                "EVT-4002",
                "ORD-1001",
                OrderStatus.CREATED,
                OrderStatus.CONFIRMED,
                "Confirmed",
                _utc("2026-07-02T06:00:00"),
                ActorType.SYSTEM,
                "system",
            ),
            OrderStatusEvent(
                "EVT-4003",
                "ORD-1001",
                OrderStatus.CONFIRMED,
                OrderStatus.PICKED_UP,
                "Picked up",
                _utc("2026-07-02T07:00:00"),
                ActorType.DRIVER,
                "DRV-2001",
            ),
            OrderStatusEvent(
                "EVT-4004",
                "ORD-1001",
                OrderStatus.PICKED_UP,
                OrderStatus.IN_TRANSIT,
                "In transit",
                _utc("2026-07-02T08:00:00"),
                ActorType.DRIVER,
                "DRV-2001",
            ),
            OrderStatusEvent(
                "EVT-4005",
                "ORD-1001",
                OrderStatus.IN_TRANSIT,
                OrderStatus.OUT_FOR_DELIVERY,
                "Out for delivery",
                _utc("2026-07-02T09:00:00"),
                ActorType.DRIVER,
                "DRV-2001",
            ),
        ],
        "ORD-1002": [
            OrderStatusEvent(
                "EVT-4101",
                "ORD-1002",
                None,
                OrderStatus.CREATED,
                "Created",
                _utc("2026-07-02T05:30:00"),
                ActorType.SYSTEM,
                "system",
            ),
            OrderStatusEvent(
                "EVT-4102",
                "ORD-1002",
                OrderStatus.CREATED,
                OrderStatus.CONFIRMED,
                "Confirmed",
                _utc("2026-07-02T06:30:00"),
                ActorType.SYSTEM,
                "system",
            ),
            OrderStatusEvent(
                "EVT-4103",
                "ORD-1002",
                OrderStatus.CONFIRMED,
                OrderStatus.PICKED_UP,
                "Picked up",
                _utc("2026-07-02T07:30:00"),
                ActorType.DRIVER,
                "DRV-2001",
            ),
            OrderStatusEvent(
                "EVT-4104",
                "ORD-1002",
                OrderStatus.PICKED_UP,
                OrderStatus.IN_TRANSIT,
                "In transit",
                _utc("2026-07-02T08:30:00"),
                ActorType.DRIVER,
                "DRV-2001",
            ),
        ],
        "ORD-1003": [
            OrderStatusEvent(
                "EVT-4201",
                "ORD-1003",
                None,
                OrderStatus.CREATED,
                "Created",
                _utc("2026-07-01T15:00:00"),
                ActorType.SYSTEM,
                "system",
            ),
            OrderStatusEvent(
                "EVT-4202",
                "ORD-1003",
                OrderStatus.CREATED,
                OrderStatus.OUT_FOR_DELIVERY,
                "Out for delivery",
                _utc("2026-07-01T17:00:00"),
                ActorType.DRIVER,
                "DRV-2001",
            ),
            OrderStatusEvent(
                "EVT-4203",
                "ORD-1003",
                OrderStatus.OUT_FOR_DELIVERY,
                OrderStatus.DELIVERED,
                "Delivered",
                _utc("2026-07-01T18:00:00"),
                ActorType.DRIVER,
                "DRV-2001",
            ),
        ],
    }

    return SeedDataStore(
        orders=orders,
        drivers=drivers,
        assignments=assignments,
        status_events_by_order_id=status_events_by_order_id,
    )
