from dataclasses import replace
from datetime import datetime, timedelta, timezone

from app.domain.orders import ActorType, OrderStatus, OrderStatusEvent
from app.domain.policies import AssignmentAuthorizationPolicy, StatusTransitionPolicy
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
from app.schemas.orders import CreateStatusEventRequest, StatusEventResponse

STATUS_LABELS = {
    OrderStatus.CREATED: "Created",
    OrderStatus.CONFIRMED: "Confirmed",
    OrderStatus.PICKED_UP: "Picked up",
    OrderStatus.IN_TRANSIT: "In transit",
    OrderStatus.OUT_FOR_DELIVERY: "Out for delivery",
    OrderStatus.DELIVERY_ATTEMPTED: "Delivery attempted",
    OrderStatus.DELIVERED: "Delivered",
    OrderStatus.CANCELLED: "Cancelled",
}


class CreateStatusEventService:
    def __init__(
        self,
        order_repository: InMemoryOrderRepository,
        driver_repository: InMemoryDriverRepository,
        assignment_repository: InMemoryAssignmentRepository,
        status_event_repository: InMemoryStatusEventRepository,
    ) -> None:
        self._order_repository = order_repository
        self._driver_repository = driver_repository
        self._assignment_repository = assignment_repository
        self._status_event_repository = status_event_repository
        self._assignment_policy = AssignmentAuthorizationPolicy()
        self._transition_policy = StatusTransitionPolicy()

    def create_status_event(
        self,
        order_id: str,
        request: CreateStatusEventRequest,
    ) -> StatusEventResponse:
        order = self._order_repository.find_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)

        driver = self._driver_repository.find_by_id(request.driverId)
        if driver is None:
            raise DriverNotFoundError(request.driverId)

        assignments = self._assignment_repository.find_by_order_id(order_id)
        if not self._assignment_policy.can_driver_update_order(request.driverId, order_id, assignments):
            raise OrderNotAssignedToDriverError(order_id, request.driverId)

        if not self._transition_policy.can_transition(order.current_status, request.status):
            raise InvalidStatusTransitionError(
                f"Cannot transition order {order_id} from {order.current_status.value} to {request.status.value}."
            )

        occurred_at = request.occurredAt or datetime.now(timezone.utc)
        if occurred_at.tzinfo is None:
            occurred_at = occurred_at.replace(tzinfo=timezone.utc)
        if occurred_at > datetime.now(timezone.utc) + timedelta(days=1):
            raise InvalidStatusEventError("Status event occurredAt is too far in the future.")

        event = OrderStatusEvent(
            event_id=self._next_event_id(order_id),
            order_id=order_id,
            previous_status=order.current_status,
            new_status=request.status,
            status_label=STATUS_LABELS[request.status],
            occurred_at=occurred_at,
            actor_type=ActorType.DRIVER,
            actor_id=request.driverId,
        )

        self._status_event_repository.append(event)
        updated_order = replace(
            order,
            current_status=request.status,
            status_label=event.status_label,
            last_updated_at=occurred_at,
        )
        self._order_repository.save(updated_order)

        return StatusEventResponse(
            eventId=event.event_id,
            orderId=event.order_id,
            previousStatus=event.previous_status,
            newStatus=event.new_status,
            statusLabel=event.status_label,
            occurredAt=event.occurred_at,
            actorType=event.actor_type,
            actorId=event.actor_id,
            location=request.location,
            note=request.note,
            proofOfDeliveryAvailable=request.proofOfDeliveryAvailable,
            orderCurrentStatus=updated_order.current_status,
        )

    def _next_event_id(self, order_id: str) -> str:
        next_number = (
            max(
                (int(event.event_id.replace("EVT-", "")) for event in self._status_event_repository.find_by_order_id(order_id)),
                default=4000,
            )
            + 1
        )
        return f"EVT-{next_number}"
