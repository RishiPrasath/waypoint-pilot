import re

from fastapi import APIRouter, status

from app.errors.exceptions import InvalidRequestError, OrderNotFoundError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.repositories.status_events import InMemoryStatusEventRepository
from app.schemas.orders import CreateStatusEventRequest, OrderStatusResponse, OrderTimelineResponse, StatusEventResponse
from app.services.order_timeline import OrderTimelineService
from app.services.status_events import CreateStatusEventService
from app.services.order_status import OrderStatusService
from app.state import get_store

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])
_ORDER_ID_PATTERN = re.compile(r"^ORD-[0-9]{4}$")


@router.get("/{order_id}/status", response_model=OrderStatusResponse)
def get_order_status(order_id: str) -> OrderStatusResponse:
    if not _ORDER_ID_PATTERN.fullmatch(order_id):
        raise InvalidRequestError("Invalid orderId.")

    store = get_store()
    service = OrderStatusService(InMemoryOrderRepository(store))
    response = service.get_order_status(order_id)

    if response is None:
        raise OrderNotFoundError(order_id)

    return response


@router.get("/{order_id}/timeline", response_model=OrderTimelineResponse)
def get_order_timeline(order_id: str, page: int = 1, pageSize: int = 20) -> OrderTimelineResponse:
    if not _ORDER_ID_PATTERN.fullmatch(order_id) or page < 1 or pageSize < 1 or pageSize > 100:
        raise InvalidRequestError("Invalid timeline request.")

    store = get_store()
    service = OrderTimelineService(
        InMemoryOrderRepository(store),
        InMemoryStatusEventRepository(store),
    )
    return service.get_timeline(order_id, page, pageSize)


@router.post("/{order_id}/status-events", response_model=StatusEventResponse, status_code=status.HTTP_201_CREATED)
def create_order_status_event(order_id: str, request: CreateStatusEventRequest) -> StatusEventResponse:
    if not _ORDER_ID_PATTERN.fullmatch(order_id):
        raise InvalidRequestError("Invalid orderId.")

    store = get_store()
    service = CreateStatusEventService(
        InMemoryOrderRepository(store),
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
        InMemoryStatusEventRepository(store),
    )
    return service.create_status_event(order_id, request)
