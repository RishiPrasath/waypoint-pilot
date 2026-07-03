from datetime import datetime, timedelta, timezone

import pytest

from app.domain.orders import OrderStatus
from app.errors.exceptions import (
    DriverNotFoundError,
    InvalidStatusEventError,
    InvalidStatusTransitionError,
    OrderNotAssignedToDriverError,
    OrderNotFoundError,
)
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.repositories.status_events import InMemoryStatusEventRepository
from app.schemas.orders import CreateStatusEventRequest
from app.seed.loader import load_seed_data
from app.services.status_events import CreateStatusEventService


def build_service() -> tuple[CreateStatusEventService, InMemoryOrderRepository, InMemoryStatusEventRepository]:
    store = load_seed_data()
    order_repository = InMemoryOrderRepository(store)
    status_event_repository = InMemoryStatusEventRepository(store)
    return (
        CreateStatusEventService(
            order_repository,
            InMemoryDriverRepository(store),
            InMemoryAssignmentRepository(store),
            status_event_repository,
        ),
        order_repository,
        status_event_repository,
    )


def test_assigned_driver_can_mark_order_delivered() -> None:
    service, order_repository, status_event_repository = build_service()

    response = service.create_status_event(
        "ORD-1001",
        CreateStatusEventRequest(
            driverId="DRV-2001",
            status=OrderStatus.DELIVERED,
            occurredAt=datetime.now(timezone.utc) - timedelta(minutes=1),
        ),
    )

    assert response.previousStatus == "OUT_FOR_DELIVERY"
    assert response.newStatus == "DELIVERED"
    assert response.orderCurrentStatus == "DELIVERED"
    assert order_repository.find_by_id("ORD-1001").current_status == OrderStatus.DELIVERED  # type: ignore[union-attr]
    assert len(status_event_repository.find_by_order_id("ORD-1001")) == 6


def test_unassigned_driver_is_rejected_before_transition_check() -> None:
    service, _, _ = build_service()

    with pytest.raises(OrderNotAssignedToDriverError):
        service.create_status_event(
            "ORD-1001",
            CreateStatusEventRequest(driverId="DRV-2002", status=OrderStatus.DELIVERED),
        )


def test_missing_driver_returns_driver_not_found() -> None:
    service, _, _ = build_service()

    with pytest.raises(DriverNotFoundError):
        service.create_status_event(
            "ORD-1001",
            CreateStatusEventRequest(driverId="DRV-9999", status=OrderStatus.DELIVERED),
        )


def test_missing_order_returns_order_not_found() -> None:
    service, _, _ = build_service()

    with pytest.raises(OrderNotFoundError):
        service.create_status_event(
            "ORD-9999",
            CreateStatusEventRequest(driverId="DRV-2001", status=OrderStatus.DELIVERED),
        )


def test_delivered_order_reaches_invalid_transition_path() -> None:
    service, _, _ = build_service()

    with pytest.raises(InvalidStatusTransitionError):
        service.create_status_event(
            "ORD-1003",
            CreateStatusEventRequest(driverId="DRV-2001", status=OrderStatus.OUT_FOR_DELIVERY),
        )


def test_far_future_occurred_at_returns_invalid_status_event() -> None:
    service, _, _ = build_service()

    with pytest.raises(InvalidStatusEventError):
        service.create_status_event(
            "ORD-1001",
            CreateStatusEventRequest(
                driverId="DRV-2001",
                status=OrderStatus.DELIVERED,
                occurredAt=datetime.now(timezone.utc) + timedelta(days=2),
            ),
        )
