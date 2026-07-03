import re

from fastapi import APIRouter

from app.domain.orders import OrderStatus
from app.errors.exceptions import InvalidRequestError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.repositories.orders import InMemoryOrderRepository
from app.schemas.drivers import DriverAssignmentsResponse, DriverResponse
from app.services.driver_assignments import DriverAssignmentsService
from app.services.driver_profile import DriverProfileService
from app.state import get_store

router = APIRouter(prefix="/api/v1/drivers", tags=["Drivers"])
_DRIVER_ID_PATTERN = re.compile(r"^DRV-[0-9]{4}$")


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: str) -> DriverResponse:
    if not _DRIVER_ID_PATTERN.fullmatch(driver_id):
        raise InvalidRequestError("Invalid driverId.")

    store = get_store()
    service = DriverProfileService(
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
    )
    return service.get_driver(driver_id)


@router.get("/{driver_id}/assignments", response_model=DriverAssignmentsResponse)
def list_driver_assignments(
    driver_id: str,
    status: OrderStatus | None = None,
    page: int = 1,
    pageSize: int = 20,
) -> DriverAssignmentsResponse:
    if not _DRIVER_ID_PATTERN.fullmatch(driver_id) or page < 1 or pageSize < 1 or pageSize > 100:
        raise InvalidRequestError("Invalid driver assignment request.")

    store = get_store()
    service = DriverAssignmentsService(
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
        InMemoryOrderRepository(store),
    )
    return service.list_assignments(driver_id, status, page, pageSize)
