# Partner Source Parity Checks Proposal

## Status

Draft proposal.

## Why This Exists

Spring Boot and FastAPI now pass their own Slice 1 test suites. That proves each implementation works on its own, but it does not yet prove that both implementations return equivalent contract behavior for the same requests.

The parity layer should catch drift between the two stacks:

- different HTTP status codes
- missing or extra required response fields
- different enum values or casing
- different seed-data values
- different pagination fields
- different ProblemDetail error shapes
- different `errorCode` values

## Grounding Sources

Parity checks must be grounded in the product use cases, then constrained by the frozen Slice 1 spec.

Use this authority order:

1. Product intent and actor use cases: `../docs/research/use-cases.md`
2. Use-case to API resource mapping: `../docs/research/use-case-resource-map.md`
3. Frozen Slice 1 behavior: `../AGREED_SPEC.md`
4. Contract details: `../docs/contracts/openapi/partner-source.v1.yaml`
5. Manual request examples: `../docs/contracts/openapi/http/partner-source-slice1.http`
6. Shared error envelope: `../docs/contracts/shared-error-contract.md`

The research use-case docs explain why a behavior matters. `AGREED_SPEC.md` decides whether that behavior is in Slice 1. If a broader research use case conflicts with the frozen Slice 1 scope, follow `AGREED_SPEC.md`.

## Use Case To Parity Mapping

Each parity scenario should trace back to a Slice 1 use case or platform readiness need.

| Use Case | Actor / Intent | Slice 1 Resource | Slice 1 Endpoint | Parity Checks |
|---|---|---|---|---|
| `CSA-01` Look up order by order ID | Customer Service Agent confirms an order exists. | `orders` | `GET /api/v1/orders/{orderId}/status` | `ORD-1001` returns `200`; `ORD-9999` returns `404 ORDER_NOT_FOUND`; malformed ID returns `400 INVALID_REQUEST`. |
| `CSA-02` View current order status | Customer Service Agent answers "where is my order?" | `orders` | `GET /api/v1/orders/{orderId}/status` | `currentStatus`, `statusLabel`, `assignedDriver.driverId`, ETA, delivery window, and required fields match. |
| `CSA-03` View order timeline | Customer Service Agent explains what happened to the shipment. | `status-events` | `GET /api/v1/orders/{orderId}/timeline` | `ORD-1001` timeline returns `totalItems = 5`, chronological events, and matching required item fields. |
| `CSA-04` View ETA and delivery window | Customer Service Agent answers arrival-window questions. | `orders` | `GET /api/v1/orders/{orderId}/status` | `estimatedDeliveryAt` and `deliveryWindow` fields exist and match the frozen seed values. |
| `DA-01` Demo login as driver | Delivery Agent confirms seeded driver identity. | `drivers` | `GET /api/v1/drivers/{driverId}` | `DRV-2001` returns profile fields; `DRV-9999` returns `404 DRIVER_NOT_FOUND`; malformed ID returns `400 INVALID_REQUEST`. |
| `DA-02` Retrieve assigned orders | Delivery Agent sees active assigned work. | `assignments` | `GET /api/v1/drivers/{driverId}/assignments` | `DRV-2001` returns `totalItems = 2` and `ORD-1001`/`ORD-1002`; `DRV-2003` returns empty `items`; missing driver returns `404 DRIVER_NOT_FOUND`. |
| `DA-05` Mark order as out for delivery | Delivery Agent reports a status event. | `status-events` | `POST /api/v1/orders/{orderId}/status-events` | Invalid transition, unassigned driver, missing driver, missing order, malformed body, and semantic validation errors match. |
| `DA-06` Mark order as delivered | Delivery Agent completes a delivery. | `status-events` | `POST /api/v1/orders/{orderId}/status-events` | Happy path returns `201`, appends a status event, and updates order current status to `DELIVERED`. |
| Service liveness | Local tooling and CI know the process is running. | `health` | `GET /health` | `status = UP`, `service = partner-source`, and required fields match. |
| Service readiness | Local tooling and CI know seed data is ready. | `ready` | `GET /ready` | `status = READY`, `checks.persistence = UP`, `checks.seedData = UP`, and required fields match. |

## Deferred Use Cases

These use cases exist in the research docs, but they are outside the frozen Slice 1 parity gate unless the spec is deliberately reopened:

- `CSA-05` View delay or exception reason
- `CSA-06` View failed delivery attempt details
- `CSA-07` View delivered but not found support facts
- `CSA-08` View available customer actions
- `CSA-09` Get support summary
- `DA-03` View delivery details through a separate delivery-view endpoint
- `DA-07` Report failed delivery attempt
- `DA-08` Report operational exception
- `DA-09` Add delivery note

The parity harness must not add endpoints, fields, statuses, seed data, or assertions for these deferred use cases during Slice 1.

## Traceability Rule

Every parity scenario should carry enough metadata to explain why it exists.

Suggested shape:

```text
id: CSA-02-order-status-happy-path
use_case: CSA-02
actor: Customer Service Agent
intent: View current order status
resource: orders
method: GET
path: /api/v1/orders/ORD-1001/status
source_use_case: ../docs/research/use-cases.md
source_mapping: ../docs/research/use-case-resource-map.md
source_spec: ../AGREED_SPEC.md
source_contract: ../docs/contracts/openapi/partner-source.v1.yaml
asserts: status code, required fields, currentStatus, assignedDriver.driverId
```

When a parity check fails, the failure should make it clear whether the drift affects a customer-service read path, a delivery-agent write path, or platform readiness.

## Proposal

Build a small local parity checker in two stages.

Stage 1 should be a manual local parity harness. It should assume both services are already running:

```text
Spring Boot: http://localhost:8080
FastAPI:     http://localhost:8000
```

The harness should run the same request matrix against both base URLs and compare the contract-relevant response parts.

Stage 2 should add GitHub Actions parity CI only after the local harness is proven. CI parity is a separate step because it must boot both services in the same job, wait for readiness, run checks, and shut them down cleanly.

## Scope For Stage 1

Create:

```text
parity/pyproject.toml
parity/parity_runner.py
parity/scripts/
parity/tests/
parity/tests/test_contract_sources.py
parity/tests/test_success_response_parity.py
parity/tests/test_error_response_parity.py
```

Use Python and pytest because the FastAPI project already uses pytest and HTTP comparison code is small in Python.

Use environment variables for service locations:

```text
SPRING_BASE_URL=http://localhost:8080
FASTAPI_BASE_URL=http://localhost:8000
```

Default to those localhost values when the variables are not set.

## Request Matrix

Start with the Slice 1 acceptance scenarios from `../AGREED_SPEC.md`, then expand them to cover every default executable scenario in `../docs/contracts/openapi/http/partner-source-slice1.http`.

Attach each scenario to the use-case mapping above. If a scenario is a validation or platform check rather than a direct actor use case, mark it as protecting the related resource contract.

Success checks:

- `GET /health`
- `GET /ready`
- `GET /api/v1/orders/ORD-1001/status`
- `GET /api/v1/orders/ORD-1001/timeline?page=1&pageSize=20`
- `GET /api/v1/drivers/DRV-2001`
- `GET /api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20`
- `GET /api/v1/drivers/DRV-2001/assignments?status=OUT_FOR_DELIVERY&page=1&pageSize=20`
- `GET /api/v1/drivers/DRV-2003/assignments?page=1&pageSize=20`

Error checks:

- `GET /api/v1/orders/ORD-9999/status`
- `GET /api/v1/orders/INVALID/status`
- `GET /api/v1/orders/ORD-9999/timeline?page=1&pageSize=20`
- `GET /api/v1/orders/ORD-1001/timeline?page=0&pageSize=20`
- `GET /api/v1/drivers/DRV-9999`
- `GET /api/v1/drivers/INVALID`
- `GET /api/v1/drivers/DRV-2001/assignments?status=NOT_A_STATUS&page=1&pageSize=20`
- `GET /api/v1/drivers/DRV-9999/assignments?page=1&pageSize=20`
- `GET /api/v1/drivers/DRV-2001/assignments?page=0&pageSize=20`
- `POST /api/v1/orders/ORD-1001/status-events` with wrong driver
- `POST /api/v1/orders/ORD-1001/status-events` with missing driver
- `POST /api/v1/orders/ORD-1003/status-events` with invalid transition
- `POST /api/v1/orders/ORD-1001/status-events` with far-future `occurredAt`
- `POST /api/v1/orders/ORD-9999/status-events`
- `POST /api/v1/orders/ORD-1001/status-events` with malformed body

Handle the successful state-changing request separately:

- `POST /api/v1/orders/ORD-1001/status-events` with `DRV-2001`, `DELIVERED`

This request mutates in-memory state, so the parity harness must either run it last against fresh services or provide a documented reset/startup rule.

Do not include the deliberately-not-ready `/ready` scenario in the default parity run unless the harness also controls a not-ready service setup. Keep that as a future environment-specific check.

## Comparison Rules

Compare exactly:

- HTTP status code
- required JSON field names
- enum values
- seeded IDs
- seeded counts such as `activeAssignmentCount` and `totalItems`
- ProblemDetail `status`
- ProblemDetail `errorCode`

Compare shape but not exact value:

- `correlationId`
- generated status-event IDs, if implementations generate them differently
- timestamps only when the spec allows generated values

Do not ignore fields required by OpenAPI. If one implementation differs, fix the implementation rather than loosening parity.

## Parity Report Output

The parity harness should produce a human-readable report and a machine-readable report on every run.

The primary local command should be a report-first runner:

```powershell
python -m parity_runner
```

Pytest should still validate the same request matrix, comparison functions, and report writer, but `python -m parity_runner` is the command to use when the goal is a durable parity report.

Latest report paths:

```text
parity/reports/latest/parity-report.md
parity/reports/latest/parity-report.json
```

Optional timestamped archive paths:

```text
parity/reports/runs/YYYY-MM-DDTHH-mm-ss/parity-report.md
parity/reports/runs/YYYY-MM-DDTHH-mm-ss/parity-report.json
```

The Markdown report is for humans. The JSON report is for scripts, CI, and future dashboarding.

Each report row should include:

- scenario ID
- use case
- actor
- intent
- method and path
- expected status
- Spring Boot status
- FastAPI status
- result: `PASS` or `FAIL`
- compared fields
- mismatch details, when present

Example Markdown row:

```text
| CSA-02-order-status-happy-path | CSA-02 | GET /api/v1/orders/ORD-1001/status | 200 | 200 | 200 | PASS |
```

Example failure detail:

```text
Scenario: CSA-02-order-status-happy-path
Field: assignedDriver.driverId
Expected: DRV-2001
Spring Boot: DRV-2001
FastAPI: null
Result: FAIL
```

The report should start with a summary:

- total scenarios
- passed scenarios
- failed scenarios
- skipped scenarios, if any
- Spring Boot base URL
- FastAPI base URL
- report timestamp

The report generator should exit non-zero when any scenario fails. That keeps local runs and future CI honest while still leaving a readable artifact behind.

When parity CI is added later, CI should upload both report files as workflow artifacts.

## Proposed Implementation Steps

1. Add parity project scaffolding with pytest and a tiny source-file existence test.
2. Add a request matrix module that names each scenario, method, path, body, and expected status.
3. Add an HTTP client helper that targets both base URLs.
4. Add comparison result objects that preserve scenario metadata and mismatch details.
5. Add a report writer for Markdown and JSON outputs.
6. Add `parity_runner.py` so `python -m parity_runner` runs the full default matrix and writes both reports.
7. Add success-response parity tests.
8. Add ProblemDetail/error-response parity tests.
9. Add a README section with exact local run commands and report locations.
10. Only after local parity is stable, add a root `.github/workflows/partner-source-parity-ci.yml`.

## Local Commands

Run both services first.

Spring Boot:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd spring-boot:run
```

FastAPI:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
uv run fastapi dev app/main.py --host 127.0.0.1 --port 8000
```

Parity:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\parity
python -m parity_runner
```

Validation tests for the parity harness:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\parity
python -m pytest
```

## Done Criteria

- Both implementations pass their own full test suites.
- Parity source-file checks pass.
- The request matrix covers the default executable scenarios in `../docs/contracts/openapi/http/partner-source-slice1.http`.
- `python -m parity_runner` runs the full default matrix.
- Success-response parity checks pass.
- Error-response parity checks pass.
- `parity/reports/latest/parity-report.md` is generated.
- `parity/reports/latest/parity-report.json` is generated.
- State-changing request behavior is documented and checked without contaminating later checks.
- Any drift found by parity is fixed in Spring Boot or FastAPI, not hidden in the parity layer.

## Not In Scope

- Do not add Docker.
- Do not add databases.
- Do not change the OpenAPI contract to match implementation drift.
- Do not add deployment behavior.
- Do not require CI parity until local parity is stable.
