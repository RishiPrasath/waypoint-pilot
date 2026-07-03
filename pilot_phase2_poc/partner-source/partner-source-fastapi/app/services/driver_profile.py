from app.errors.exceptions import DriverNotFoundError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.schemas.drivers import DriverResponse


class DriverProfileService:
    def __init__(
        self,
        driver_repository: InMemoryDriverRepository,
        assignment_repository: InMemoryAssignmentRepository,
    ) -> None:
        self._driver_repository = driver_repository
        self._assignment_repository = assignment_repository

    def get_driver(self, driver_id: str) -> DriverResponse:
        driver = self._driver_repository.find_by_id(driver_id)
        if driver is None:
            raise DriverNotFoundError(driver_id)

        active_assignments = self._assignment_repository.find_by_driver_id(driver_id)

        return DriverResponse(
            driverId=driver.driver_id,
            displayName=driver.display_name,
            availabilityStatus=driver.availability_status,
            activeAssignmentCount=len(active_assignments),
        )
