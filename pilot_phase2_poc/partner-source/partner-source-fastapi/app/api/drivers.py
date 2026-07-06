import re

from fastapi import APIRouter, Depends

from app.domain.orders import OrderStatus
from app.errors.exceptions import AccessDeniedError, InvalidRequestError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.schemas.drivers import DriverAssignmentsResponse, DriverResponse
from app.security.access_policy import AccessPolicy
from app.security.dependencies import require_principal
from app.security.principal import AuthenticatedPrincipal
from app.services.driver_assignments import DriverAssignmentsService
from app.services.driver_profile import DriverProfileService
from app.state import get_store

router = APIRouter(prefix="/api/v1/drivers", tags=["Drivers"])
_DRIVER_ID_PATTERN = re.compile(r"^DRV-[0-9]{4}$")


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(
    driver_id: str,
    principal: AuthenticatedPrincipal = Depends(require_principal),
) -> DriverResponse:
    if not _DRIVER_ID_PATTERN.fullmatch(driver_id):
        raise InvalidRequestError("Invalid driverId.")

    store = get_store()
    assignment_repository = InMemoryAssignmentRepository(store)
    if not AccessPolicy(InMemoryOrderRepository(store), assignment_repository).can_read_driver_resource(principal, driver_id):
        raise AccessDeniedError("Caller cannot access this driver resource.")

    service = DriverProfileService(
        InMemoryDriverRepository(store),
        assignment_repository,
    )
    return service.get_driver(driver_id)


@router.get("/{driver_id}/assignments", response_model=DriverAssignmentsResponse)
def list_driver_assignments(
    driver_id: str,
    status: OrderStatus | None = None,
    page: int = 1,
    pageSize: int = 20,
    principal: AuthenticatedPrincipal = Depends(require_principal),
) -> DriverAssignmentsResponse:
    if not _DRIVER_ID_PATTERN.fullmatch(driver_id) or page < 1 or pageSize < 1 or pageSize > 100:
        raise InvalidRequestError("Invalid driver assignment request.")

    store = get_store()
    assignment_repository = InMemoryAssignmentRepository(store)
    order_repository = InMemoryOrderRepository(store)
    if not AccessPolicy(order_repository, assignment_repository).can_read_driver_resource(principal, driver_id):
        raise AccessDeniedError("Caller cannot access this driver resource.")

    service = DriverAssignmentsService(
        InMemoryDriverRepository(store),
        assignment_repository,
        order_repository,
    )
    return service.list_assignments(driver_id, status, page, pageSize)
