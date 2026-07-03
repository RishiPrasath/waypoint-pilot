from app.domain.orders import OrderStatus
from app.domain.assignments import DeliveryAssignment, DeliveryAssignmentStatus
from collections.abc import Iterable


class StatusTransitionPolicy:
    _ALLOWED_TRANSITIONS = {
        OrderStatus.CREATED: {
            OrderStatus.CONFIRMED,
            OrderStatus.CANCELLED,
        },
        OrderStatus.CONFIRMED: {
            OrderStatus.PICKED_UP,
            OrderStatus.CANCELLED,
        },
        OrderStatus.PICKED_UP: {
            OrderStatus.IN_TRANSIT,
        },
        OrderStatus.IN_TRANSIT: {
            OrderStatus.OUT_FOR_DELIVERY,
        },
        OrderStatus.OUT_FOR_DELIVERY: {
            OrderStatus.DELIVERED,
        },
        OrderStatus.DELIVERY_ATTEMPTED: set(),
        OrderStatus.DELIVERED: set(),
        OrderStatus.CANCELLED: set(),
    }

    def can_transition(
        self,
        current_status: OrderStatus,
        next_status: OrderStatus,
    ) -> bool:
        return next_status in self._ALLOWED_TRANSITIONS.get(current_status, set())


class AssignmentAuthorizationPolicy:
    def can_driver_update_order(
        self,
        driver_id: str,
        order_id: str,
        assignments: Iterable[DeliveryAssignment],
    ) -> bool:
        return any(
            assignment.driver_id == driver_id
            and assignment.order_id == order_id
            and assignment.status in {
                DeliveryAssignmentStatus.ASSIGNED,
                DeliveryAssignmentStatus.ACCEPTED,
                DeliveryAssignmentStatus.COMPLETED,
            }
            for assignment in assignments
        )
