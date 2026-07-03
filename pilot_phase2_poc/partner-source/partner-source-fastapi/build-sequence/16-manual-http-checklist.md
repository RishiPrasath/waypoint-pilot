# 16 - Manual HTTP Checklist

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Run the canonical manual requests against the local FastAPI app.

## Source Docs To Read

- `../../docs/contracts/openapi/http/partner-source-slice1.http`
- `../../AGREED_SPEC.md` section `10. Acceptance Scenarios`
- `../../partner-source-springboot/build-sequence/16-manual-http-checklist.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

No new automated tests.

This task is the human verification pass after automated tests are green.

Before starting manual checks, run:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Before starting manual checks, run.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
python -m pytest
```

If any manual request fails, do not fix it directly from the manual result. First add or update the relevant automated test from tasks 07 through 15, watch it fail, then fix the code.
## File Map

No code. Fix only if manual requests reveal drift from the agreed spec or Spring Boot reference behavior.

## Exact Code

No application code should be created in this task.

Run the app:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Run the app.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
uv run uvicorn app.main:app --reload --port 8000
```

In a second PowerShell window, run these checks:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for In a second PowerShell window, run these checks.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/ready
Invoke-RestMethod http://127.0.0.1:8000/api/v1/orders/ORD-1001/status
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"
Invoke-RestMethod http://127.0.0.1:8000/api/v1/drivers/DRV-2001
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"
Invoke-RestMethod "http://127.0.0.1:8000/api/v1/drivers/DRV-2003/assignments?page=1&pageSize=20"

```

Run the successful write check:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Run the successful write check.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$body = @{
  driverId = "DRV-2001"
  status = "DELIVERED"
  occurredAt = "2026-07-02T10:30:00+00:00"
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/api/v1/orders/ORD-1001/status-events `
  -ContentType "application/json" `
  -Body $body

```

Run the negative checks:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Run the negative checks.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$unassigned = @{ driverId = "DRV-2002"; status = "DELIVERED" } | ConvertTo-Json
$missingDriver = @{ driverId = "DRV-9999"; status = "DELIVERED" } | ConvertTo-Json
$invalidTransition = @{ driverId = "DRV-2001"; status = "OUT_FOR_DELIVERY" } | ConvertTo-Json

Invoke-WebRequest -Method Post -Uri http://127.0.0.1:8000/api/v1/orders/ORD-1001/status-events -ContentType "application/json" -Body $unassigned
Invoke-WebRequest -Method Post -Uri http://127.0.0.1:8000/api/v1/orders/ORD-1001/status-events -ContentType "application/json" -Body $missingDriver
Invoke-WebRequest -Method Post -Uri http://127.0.0.1:8000/api/v1/orders/ORD-1003/status-events -ContentType "application/json" -Body $invalidTransition

```

Expected negative status codes:

**Block Explanation**

- What this block does: Shows exact text values, paths, or rules for `DRV-2002 on ORD-1001 -> 403 ORDER_NOT_ASSIGNED_TO_DRIVER`, `DRV-9999 on ORD-1001 -> 404 DRIVER_NOT_FOUND`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
DRV-2002 on ORD-1001 -> 403 ORDER_NOT_ASSIGNED_TO_DRIVER
DRV-9999 on ORD-1001 -> 404 DRIVER_NOT_FOUND
DRV-2001 on ORD-1003 to OUT_FOR_DELIVERY -> 409 INVALID_STATUS_TRANSITION

```

## Commands To Run

Start the app:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Start the app.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
python -m uvicorn app.main:app --reload
```

In a second PowerShell window:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for In a second PowerShell window.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/ready
Invoke-RestMethod http://localhost:8000/api/v1/orders/ORD-1001/status
Invoke-RestMethod "http://localhost:8000/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"
Invoke-RestMethod http://localhost:8000/api/v1/drivers/DRV-2001
Invoke-RestMethod "http://localhost:8000/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"

```

Post success event:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Post success event.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$body = @{
  driverId = "DRV-2001"
  status = "DELIVERED"
  occurredAt = "2026-06-30T15:45:00+08:00"
  note = "Left with reception"
  proofOfDeliveryAvailable = $true
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/v1/orders/ORD-1001/status-events -ContentType "application/json" -Body $body

```

## Done Criteria

- [x] Manual checklist passes through automated integration coverage.
- [x] Any discovered mismatch has an automated test before the fix.
- [x] Results are ready for parity comparison.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not make manual-only fixes without adding a test.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Marked done after equivalent FastAPI TestClient integration checks and the full pytest suite passed.
