import re

from fastapi import APIRouter, Depends, status

from app.errors.exceptions import AccessDeniedError, InvalidRequestError, OrderNotFoundError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.repositories.status_events import InMemoryStatusEventRepository
from app.schemas.orders import CreateStatusEventRequest, OrderStatusResponse, OrderTimelineResponse, StatusEventResponse
from app.security.access_policy import AccessPolicy
from app.security.dependencies import require_principal
from app.security.principal import AuthenticatedPrincipal
from app.services.order_timeline import OrderTimelineService
from app.services.status_events import CreateStatusEventService
from app.services.order_status import OrderStatusService
from app.state import get_store

router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])
_ORDER_ID_PATTERN = re.compile(r"^ORD-[0-9]{4}$")


@router.get("/{order_id}/status", response_model=OrderStatusResponse)
def get_order_status(
    order_id: str,
    principal: AuthenticatedPrincipal = Depends(require_principal),
) -> OrderStatusResponse:
    if not _ORDER_ID_PATTERN.fullmatch(order_id):
        raise InvalidRequestError("Invalid orderId.")

    store = get_store()
    order_repository = InMemoryOrderRepository(store)
    assignment_repository = InMemoryAssignmentRepository(store)
    service = OrderStatusService(order_repository)
    response = service.get_order_status(order_id)

    if response is None:
        raise OrderNotFoundError(order_id)

    if not AccessPolicy(order_repository, assignment_repository).can_read_order(principal, order_id):
        raise AccessDeniedError("Caller cannot access this order resource.")

    return response


@router.get("/{order_id}/timeline", response_model=OrderTimelineResponse)
def get_order_timeline(
    order_id: str,
    page: int = 1,
    pageSize: int = 20,
    principal: AuthenticatedPrincipal = Depends(require_principal),
) -> OrderTimelineResponse:
    if not _ORDER_ID_PATTERN.fullmatch(order_id) or page < 1 or pageSize < 1 or pageSize > 100:
        raise InvalidRequestError("Invalid timeline request.")

    store = get_store()
    order_repository = InMemoryOrderRepository(store)
    assignment_repository = InMemoryAssignmentRepository(store)
    if order_repository.find_by_id(order_id) is None:
        raise OrderNotFoundError(order_id)
    if not AccessPolicy(order_repository, assignment_repository).can_read_order(principal, order_id):
        raise AccessDeniedError("Caller cannot access this order resource.")

    service = OrderTimelineService(
        order_repository,
        InMemoryStatusEventRepository(store),
    )
    return service.get_timeline(order_id, page, pageSize)


@router.post("/{order_id}/status-events", response_model=StatusEventResponse, status_code=status.HTTP_201_CREATED)
def create_order_status_event(
    order_id: str,
    request: CreateStatusEventRequest,
    principal: AuthenticatedPrincipal = Depends(require_principal),
) -> StatusEventResponse:
    if not _ORDER_ID_PATTERN.fullmatch(order_id):
        raise InvalidRequestError("Invalid orderId.")

    store = get_store()
    assignment_repository = InMemoryAssignmentRepository(store)
    access_policy = AccessPolicy(InMemoryOrderRepository(store), assignment_repository)
    if not access_policy.can_create_status_event(principal):
        raise AccessDeniedError("Caller cannot create driver status events.")
    if not access_policy.can_submit_driver_id(principal, request.driverId):
        raise AccessDeniedError("Request driverId does not match the authenticated principal.")

    service = CreateStatusEventService(
        InMemoryOrderRepository(store),
        InMemoryDriverRepository(store),
        assignment_repository,
        InMemoryStatusEventRepository(store),
    )
    return service.create_status_event(order_id, request)
