# 03 - Spring Boot Vs FastAPI Response Checks

## Purpose

Compare successful response behavior from both implementations.

## Source Docs To Read

- `02-manual-request-matrix.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/17-springboot-final-gate.md`
- `../../partner-source-fastapi/build-sequence/17-fastapi-final-gate.md`

## Tests To Write First

Future automated parity test:

```text
parity/tests/test_success_response_parity.py
```

Test checks:

- HTTP status is the same.
- Required JSON fields exist in both.
- Enum values match.
- Key seed values match.
- Ignore harmless ordering only where the contract does not specify order.
- Do not require identical `correlationId` values.

## Code To Implement

Future helper shape:

```text
parity/scripts/request_matrix.py
parity/scripts/compare_responses.py
```

The helper should accept:

```text
SPRING_BASE_URL=http://localhost:8080
FASTAPI_BASE_URL=http://localhost:8000
```

## Commands To Run

Manual comparison example:

```powershell
$spring = Invoke-RestMethod http://localhost:8080/api/v1/drivers/DRV-2001
$fastapi = Invoke-RestMethod http://localhost:8000/api/v1/drivers/DRV-2001
$spring.activeAssignmentCount
$fastapi.activeAssignmentCount
```

## Done Criteria

- [ ] Success endpoints match expected statuses.
- [ ] Required fields match OpenAPI.
- [ ] Key values match seed expectations.
- [ ] Differences are fixed in the implementation that drifted.

## Stop / Do Not Add

- Do not make parity ignore fields required by OpenAPI.
- Do not change the contract to fit one implementation.
