from app.domain.orders import OrderStatus
from app.errors.exceptions import DriverNotFoundError, OrderNotFoundError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.schemas.drivers import DriverAssignmentItem, DriverAssignmentsResponse
from app.schemas.orders import DeliveryWindowResponse


class DriverAssignmentsService:
    def __init__(
        self,
        driver_repository: InMemoryDriverRepository,
        assignment_repository: InMemoryAssignmentRepository,
        order_repository: InMemoryOrderRepository,
    ) -> None:
        self._driver_repository = driver_repository
        self._assignment_repository = assignment_repository
        self._order_repository = order_repository

    def list_assignments(
        self,
        driver_id: str,
        status: OrderStatus | None,
        page: int,
        page_size: int,
    ) -> DriverAssignmentsResponse:
        driver = self._driver_repository.find_by_id(driver_id)
        if driver is None:
            raise DriverNotFoundError(driver_id)

        items: list[DriverAssignmentItem] = []
        for assignment in self._assignment_repository.find_by_driver_id(driver_id):
            order = self._order_repository.find_by_id(assignment.order_id)
            if order is None:
                raise OrderNotFoundError(assignment.order_id)
            if status is not None and order.current_status != status:
                continue

            items.append(
                DriverAssignmentItem(
                    assignmentId=assignment.assignment_id or "",
                    orderId=assignment.order_id,
                    assignmentStatus=assignment.status,
                    currentStatus=order.current_status,
                    recipientName=order.recipient_name,
                    deliveryAddressSummary=order.delivery_address_summary,
                    deliveryWindow=DeliveryWindowResponse(
                        start=order.delivery_window_start,
                        end=order.delivery_window_end,
                    ),
                    lastUpdatedAt=order.last_updated_at,
                )
            )

        start = (page - 1) * page_size
        end = start + page_size

        return DriverAssignmentsResponse(
            driverId=driver_id,
            items=items[start:end],
            page=page,
            pageSize=page_size,
            totalItems=len(items),
        )
