# Partner Source Human Build Runbook

This is the actual human sequence for building the application.

Use this as the primary manual. Keep `AGREED_SPEC.md` open while building.

## Operating Rule

For every real behavior:

```text
read the agreed spec
-> write the test first
-> run the focused test and see it fail
-> implement the smallest code
-> run the focused test again
-> run the full module tests
-> mark the task done
-> move to the next task
```

## Phase 0 - Read And Prepare

### Step 0.1 - Open the implementation lane

Action:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source
Get-ChildItem -Force
```

Expected:

```text
AGREED_SPEC.md
HUMAN_BUILD_RUNBOOK.md
MANUAL_BUILD_SEQUENCE.md
partner-source-springboot
partner-source-fastapi
```

### Step 0.2 - Read the spec

Action:

```text
Open AGREED_SPEC.md
```

Do not code until you understand:

- endpoints
- seed data
- status transition table
- error shape
- acceptance scenarios

### Step 0.3 - Check tools

Action:

```powershell
java -version
mvn -version
py -0p
python --version
git --version
```

Expected:

- Java 21 is available.
- Maven is available, or Spring Initializr will generate Maven Wrapper.
- Python 3.12 or newer is available.
- Git is available.

Stop if Java 21 or Python 3.12 is missing.

## Phase 1 - Spring Boot Project Setup

### Step 1.1 - Create the Spring Boot project

Action:

```text
Open partner-source-springboot
Create/generate a Spring Boot Maven project here.
```

Use these settings:

| Setting | Value |
|---|---|
| Java | 21 |
| Build | Maven |
| Group | `com.waypoint` |
| Artifact | `partner-source-springboot` |
| Package | `com.waypoint.partnersource` |
| Dependencies | Spring Web, Spring Validation, Spring Boot Test |

Expected files:

```text
pom.xml
mvnw
mvnw.cmd
.mvn/wrapper/
src/main/java/com/waypoint/partnersource/PartnerSourceApplication.java
src/test/java/com/waypoint/partnersource/PartnerSourceApplicationTests.java
```

### Step 1.2 - Run the scaffold test

Action:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```

Expected:

```text
BUILD SUCCESS
```

Stop if it fails. Fix setup before adding any domain code.

### Step 1.3 - Create package folders

Action: create folders under `src/main/java/com/waypoint/partnersource`.

```text
order/api/dto
order/domain
order/repository
order/service
driver/api/dto
driver/domain
driver/repository
driver/service
assignment/domain
assignment/repository
shared/error
shared/health
shared/seed
```

Action: create matching test folders under `src/test/java/com/waypoint/partnersource`.

```text
order/domain
order/repository
order/service
order/api
driver/repository
driver/api
assignment/domain
shared/health
shared/error
```

## Phase 2 - Spring Boot CI Proof

### Step 2.1 - Add CI workflow

Action: create this file from repo root:

```text
C:\Users\prasa\Documents\Github\waypoint-pilot\.github\workflows\partner-source-springboot-ci.yml
```

Use the workflow in:

```text
partner-source-springboot\BUILD_MANUAL.md
```

### Step 2.2 - Commit/push or open draft PR

Expected:

```text
GitHub Actions runs .\mvnw test equivalent on Ubuntu and passes.
```

Stop if CI fails. Do not start domain behavior until scaffold CI is green.

## Phase 3 - FastAPI Project Setup

### Step 3.1 - Create the FastAPI project

Action:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
```

Choose one setup:

- Preferred: `uv`
- Simple fallback: `.venv` plus requirements files

Use:

```text
partner-source-fastapi\BUILD_MANUAL.md
```

Expected app folders:

```text
app/main.py
app/api
app/schemas
app/domain
app/repositories
app/services
app/seed
app/errors
tests
```

### Step 3.2 - Add tiny app test

Action:

```text
Create tests/test_app.py from BUILD_MANUAL.md
```

Run:

```powershell
python -m pytest
```

Expected:

```text
passed
```

Stop if it fails. Fix setup before adding domain code.

## Phase 4 - FastAPI CI Proof

### Step 4.1 - Add CI workflow

Action: create this file from repo root:

```text
C:\Users\prasa\Documents\Github\waypoint-pilot\.github\workflows\partner-source-fastapi-ci.yml
```

Use the workflow in:

```text
partner-source-fastapi\BUILD_MANUAL.md
```

### Step 4.2 - Commit/push or open draft PR

Expected:

```text
GitHub Actions runs pytest and passes.
```

Stop if CI fails. Do not start domain behavior until scaffold CI is green.

## Phase 5 - Status Transition Policy

Spec:

```text
AGREED_SPEC.md -> Section 6
```

### Step 5.1 - Spring Boot red test

Create:

```text
src/test/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicyTest.java
```

Test at minimum:

- `OUT_FOR_DELIVERY -> DELIVERED` is allowed.
- `DELIVERED -> OUT_FOR_DELIVERY` is rejected.
- `DELIVERY_ATTEMPTED -> anything` is rejected.
- `CREATED -> CONFIRMED` is allowed.
- `CONFIRMED -> PICKED_UP` is allowed.
- `PICKED_UP -> IN_TRANSIT` is allowed.
- `IN_TRANSIT -> OUT_FOR_DELIVERY` is allowed.

Run focused test. It should fail because code is missing.

### Step 5.2 - Spring Boot green code

Create:

```text
OrderStatus.java
StatusTransitionPolicy.java
```

Use only the transition table from `AGREED_SPEC.md`.

Run:

```powershell
.\mvnw.cmd -Dtest=StatusTransitionPolicyTest test
.\mvnw.cmd test
```

### Step 5.3 - FastAPI mirror

Create:

```text
tests/domain/test_status_transition_policy.py
app/domain/orders.py
app/domain/policies.py
```

Mirror the same test cases and transition table.

Run:

```powershell
python -m pytest tests/domain/test_status_transition_policy.py
python -m pytest
```

Stop if Spring Boot and FastAPI do not agree.

## Phase 6 - Assignment Authorization Policy

Spec:

```text
AGREED_SPEC.md -> Sections 5 and 7
```

### Step 6.1 - Spring Boot red test

Create:

```text
src/test/java/com/waypoint/partnersource/assignment/domain/AssignmentAuthorizationPolicyTest.java
```

Test:

- `DRV-2001` can update `ORD-1001` through `ASN-3001 ASSIGNED`.
- `DRV-2002` cannot update `ORD-1001`.
- `COMPLETED` assignment does not count as active authorization for normal updates.

### Step 6.2 - Spring Boot green code

Create:

```text
AssignmentStatus.java
DeliveryAssignment.java
AssignmentAuthorizationPolicy.java
```

Use enum values from `AGREED_SPEC.md`: `ASSIGNED`, `ACCEPTED`, `COMPLETED`, `CANCELLED`.

### Step 6.3 - FastAPI mirror

Create:

```text
tests/domain/test_assignment_authorization_policy.py
app/domain/assignments.py
```

Append `AssignmentAuthorizationPolicy` to `app/domain/policies.py`.

Run full tests in both implementations.

## Phase 7 - Seed Store And Repositories

Spec:

```text
AGREED_SPEC.md -> Section 7
```

### Step 7.1 - Spring Boot tests

Create repository tests proving:

- `ORD-1001` exists and is `OUT_FOR_DELIVERY`.
- `ORD-9999` is missing.
- `DRV-2001` exists and is `AVAILABLE`.
- `DRV-9999` is missing.
- `DRV-2001` has two `ASSIGNED` assignments.
- `DRV-2003` has zero active assignments.

### Step 7.2 - Spring Boot implementation

Create:

```text
DeliveryOrder
DeliveryDriver
OrderStatusEvent
LocationSnapshot
DeliveryWindow
SeedDataStore
OrderRepository / InMemoryOrderRepository
DriverRepository / InMemoryDriverRepository
AssignmentRepository / InMemoryAssignmentRepository
StatusEventRepository / InMemoryStatusEventRepository
```

Do not use a database.

### Step 7.3 - FastAPI mirror

Create equivalent dataclasses, seed store, and repository classes.

Run full tests in both implementations.

## Phase 8 - Health Endpoint

Spec:

```text
AGREED_SPEC.md -> Sections 3 and 8
```

### Step 8.1 - Spring Boot

Test:

```text
GET /health -> 200
body.status = UP
body.service = partner-source
```

Implement `HealthController`.

### Step 8.2 - FastAPI

Mirror with `TestClient`.

Implement `api/health.py`.

Run full tests in both implementations.

## Phase 9 - Readiness Endpoint

Spec:

```text
AGREED_SPEC.md -> Sections 3 and 8
```

Test:

```text
GET /ready -> 200
body.status = READY
body.service = partner-source
body.checks.persistence = UP
body.checks.seedData = UP
```

Implement readiness service/controller/router in both implementations.

Run full tests in both implementations.

## Phase 10 - Order Status Lookup

Spec:

```text
AGREED_SPEC.md -> Sections 3, 7, 8, 9, 10
```

### Step 10.1 - Spring Boot service test

Test:

- `ORD-1001` returns `OUT_FOR_DELIVERY`.
- response includes required `OrderStatusResponse` fields.

### Step 10.2 - Spring Boot API test

Test:

- `GET /api/v1/orders/ORD-1001/status -> 200`.
- `GET /api/v1/orders/ORD-9999/status -> 404 ORDER_NOT_FOUND`.
- `GET /api/v1/orders/INVALID/status -> 400 INVALID_REQUEST`.

### Step 10.3 - Spring Boot implementation

Create:

```text
OrderStatusResponse DTO
OrderResponseMapper
OrderStatusService
OrderStatusController
PartnerSourceException
ErrorCode
ApiExceptionHandler
```

### Step 10.4 - FastAPI mirror

Create matching:

```text
schemas/orders.py
services/order_status.py
api/orders.py
errors/exceptions.py
errors/handlers.py
```

Run full tests in both implementations.

## Phase 11 - Error Envelope Hardening

Spec:

```text
AGREED_SPEC.md -> Section 9
```

For both implementations, add tests proving every error includes:

```text
type
title
status
detail
instance
errorCode
correlationId
```

Also test:

- HTTP status equals body `status`.
- `errorCode` is approved.
- malformed request shape maps to `400 INVALID_REQUEST`.

Run full tests.

## Phase 12 - Timeline Endpoint

Spec:

```text
AGREED_SPEC.md -> Sections 7, 8, 10
```

Build Spring Boot first, then FastAPI.

Test:

- `ORD-1001` returns `totalItems = 5`.
- events are chronological.
- event IDs run `EVT-4001` to `EVT-4005`.
- missing order returns `404 ORDER_NOT_FOUND`.
- invalid page returns `400 INVALID_REQUEST`.

Run full tests.

## Phase 13 - Driver Profile Endpoint

Spec:

```text
AGREED_SPEC.md -> Sections 7, 8, 10
```

Build Spring Boot first, then FastAPI.

Test:

- `DRV-2001` returns `AVAILABLE`.
- `DRV-2001` returns `activeAssignmentCount = 2`.
- `DRV-9999` returns `404 DRIVER_NOT_FOUND`.
- invalid driver ID returns `400 INVALID_REQUEST`.

Run full tests.

## Phase 14 - Driver Assignments Endpoint

Spec:

```text
AGREED_SPEC.md -> Sections 7, 8, 10
```

Build Spring Boot first, then FastAPI.

Test:

- `DRV-2001` returns two items.
- items include `ORD-1001` and `ORD-1002`.
- status filter `OUT_FOR_DELIVERY` returns only matching assignment items.
- invalid status filter returns `400 INVALID_REQUEST`.
- `DRV-2003` returns empty `items`.
- missing driver returns `404 DRIVER_NOT_FOUND`.
- invalid page returns `400 INVALID_REQUEST`.

Run full tests.

## Phase 15 - Create Status Event Endpoint

Spec:

```text
AGREED_SPEC.md -> Sections 6, 7, 8, 9, 10
```

Build Spring Boot first, then FastAPI.

Test in this order:

1. unassigned driver `DRV-2002` on `ORD-1001` returns `403 ORDER_NOT_ASSIGNED_TO_DRIVER`.
2. missing driver `DRV-9999` returns `404 DRIVER_NOT_FOUND`.
3. delivered order `ORD-1003` to `OUT_FOR_DELIVERY` returns `409 INVALID_STATUS_TRANSITION`.
4. far-future `occurredAt` returns `422 INVALID_STATUS_EVENT`.
5. missing order `ORD-9999` returns `404 ORDER_NOT_FOUND`.
6. malformed body returns `400 INVALID_REQUEST`.
7. assigned driver `DRV-2001` delivers `ORD-1001`, returns `201`.

Successful response must include:

```text
previousStatus = OUT_FOR_DELIVERY
newStatus = DELIVERED
actorType = DRIVER
actorId = DRV-2001
orderCurrentStatus = DELIVERED
```

After success, a status lookup for `ORD-1001` must return `DELIVERED` until the app/seed state is reset.

Run full tests.

## Phase 16 - Manual HTTP Checklist

Action:

Run the canonical `.http` checklist against Spring Boot first:

```text
docs\contracts\openapi\http\partner-source-slice1.http
```

Then run the same checklist against FastAPI.

Expected:

Both implementations produce the same status codes, key fields, and error codes.

## Phase 17 - Contract And Parity Checks

Only after both APIs work:

- validate OpenAPI syntax
- add contract smoke tests
- add parity tests comparing both implementations
- move CI from basic tests to contract-aware tests

Do not add deployment yet.

## Stop Conditions

Stop and ask for help when:

- a test fails for a reason unrelated to the behavior being built
- a spec conflicts with code
- Spring Boot and FastAPI disagree
- an error mapping is unclear
- CI fails while local passes
