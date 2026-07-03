from app.repositories.orders import InMemoryOrderRepository
from app.schemas.orders import (
    AssignedDriverResponse,
    DeliveryWindowResponse,
    LocationSnapshotResponse,
    OrderStatusResponse,
)


class OrderStatusService:
    def __init__(self, order_repository: InMemoryOrderRepository) -> None:
        self._order_repository = order_repository

    def get_order_status(self, order_id: str) -> OrderStatusResponse | None:
        order = self._order_repository.find_by_id(order_id)
        if order is None:
            return None

        assigned_driver = None
        if order.assigned_driver_id is not None and order.assigned_driver_name is not None:
            assigned_driver = AssignedDriverResponse(
                driverId=order.assigned_driver_id,
                displayName=order.assigned_driver_name,
            )

        current_location = None
        if order.current_location is not None:
            current_location = LocationSnapshotResponse(label=order.current_location)

        return OrderStatusResponse(
            orderId=order.order_id,
            currentStatus=order.current_status,
            statusLabel=order.status_label,
            estimatedDeliveryAt=order.estimated_delivery_at,
            deliveryWindow=DeliveryWindowResponse(
                start=order.delivery_window_start,
                end=order.delivery_window_end,
            ),
            currentLocation=current_location,
            assignedDriver=assigned_driver,
            lastUpdatedAt=order.last_updated_at,
        )
