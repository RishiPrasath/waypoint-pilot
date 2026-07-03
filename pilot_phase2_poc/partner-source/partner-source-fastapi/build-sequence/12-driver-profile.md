# 12 - Driver Profile

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Implement `GET /api/v1/drivers/{driverId}`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data`, `8. Response Shapes`, and `10. Acceptance Scenarios`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/12-driver-profile.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `tests/services/test_driver_profile_service.py`, `tests/api/test_driver_profile_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/services/test_driver_profile_service.py
tests/api/test_driver_profile_endpoint.py
```

`tests/services/test_driver_profile_service.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/services/test_driver_profile_service.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.seed.loader import load_seed_data
from app.services.driver_profile import DriverProfileService


def test_get_driver_profile_counts_active_assignments() -> None:
    store = load_seed_data()
    service = DriverProfileService(
        InMemoryDriverRepository(store),
        InMemoryAssignmentRepository(store),
    )

    response = service.get_driver("DRV-2001")

    assert response is not None
    assert response.driverId == "DRV-2001"
    assert response.availabilityStatus == "AVAILABLE"
    assert response.activeAssignmentCount == 2

```

`tests/api/test_driver_profile_endpoint.py`:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `tests/api/test_driver_profile_endpoint.py`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from fastapi.testclient import TestClient

from app.main import app


def test_get_driver_profile_returns_contract_shape() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-2001")

    assert response.status_code == 200
    body = response.json()
    assert body["driverId"] == "DRV-2001"
    assert body["displayName"] == "A. Kumar"
    assert body["availabilityStatus"] == "AVAILABLE"
    assert body["activeAssignmentCount"] == 2


def test_missing_driver_returns_problem_detail() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/drivers/DRV-9999")

    assert response.status_code == 404
    assert response.json()["errorCode"] == "DRIVER_NOT_FOUND"

```
## File Map

Schemas:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/schemas/drivers.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/schemas/drivers.py
```

Service/router:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `app/services/driver_profile.py`, `app/api/drivers.py`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
app/services/driver_profile.py
app/api/drivers.py
```

Update `app/main.py` to register the drivers router.

## Exact Code

Create `app/schemas/drivers.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/schemas/drivers.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from datetime import datetime

from pydantic import BaseModel

from app.domain.assignments import DeliveryAssignmentStatus
from app.domain.drivers import DriverAvailabilityStatus
from app.domain.orders import OrderStatus
from app.schemas.orders import DeliveryWindowResponse


class DriverResponse(BaseModel):
    driverId: str
    displayName: str
    availabilityStatus: DriverAvailabilityStatus
    activeAssignmentCount: int

```

Create `app/services/driver_profile.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/services/driver_profile.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from app.domain.assignments import DeliveryAssignmentStatus
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

    def get_driver(self, driver_id: str) -> DriverResponse | None:
        driver = self._driver_repository.find_by_id(driver_id)
        if driver is None:
            return None

        active_assignments = [
            assignment
            for assignment in self._assignment_repository.find_by_driver_id(driver_id)
            if assignment.status
            in {
                DeliveryAssignmentStatus.ASSIGNED,
                DeliveryAssignmentStatus.ACCEPTED,
            }
        ]

        return DriverResponse(
            driverId=driver.driver_id,
            displayName=driver.display_name,
            availabilityStatus=driver.availability_status,
            activeAssignmentCount=len(active_assignments),
        )

```

Create `app/api/drivers.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/api/drivers.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import APIRouter

from app.errors.exceptions import DriverNotFoundError
from app.repositories.assignments import InMemoryAssignmentRepository
from app.repositories.drivers import InMemoryDriverRepository
from app.schemas.drivers import DriverResponse
from app.seed.loader import load_seed_data
from app.services.driver_profile import DriverProfileService

router = APIRouter(prefix="/api/v1/drivers", tags=["Drivers"])
_STORE = load_seed_data()


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: str) -> DriverResponse:
    service = DriverProfileService(
        InMemoryDriverRepository(_STORE),
        InMemoryAssignmentRepository(_STORE),
    )
    response = service.get_driver(driver_id)

    if response is None:
        raise DriverNotFoundError(driver_id)

    return response

```

Update `app/main.py`:

**Code Block Explanation**

- What this block does: Shows the exact Python code for `app/main.py`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: imports first, then enums/data models/functions/classes, then returns or assertions.

```python
from fastapi import FastAPI

from app.api.drivers import router as drivers_router
from app.api.health import router as health_router
from app.api.orders import router as orders_router
from app.errors.handlers import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(title="Waypoint Partner Source API", version="1.0.0")
    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(orders_router)
    app.include_router(drivers_router)
    return app


app = create_app()

```

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest tests/services/test_driver_profile_service.py tests/api/test_driver_profile_endpoint.py
python -m pytest

```

Manual check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `Invoke-RestMethod http://localhost:8000/api/v1/drivers/DRV-2001`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/drivers/DRV-2001

```

## Done Criteria

- [x] Success and missing-driver tests pass.
- [x] `activeAssignmentCount` counts active assignments only.
- [x] Error envelope is reused.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add driver create/update endpoints.
- Do not add authentication.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Implemented and marked done after focused tests and the full pytest suite passed.
