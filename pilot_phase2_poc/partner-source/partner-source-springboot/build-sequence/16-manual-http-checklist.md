# 16 - Manual HTTP Checklist

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Run the canonical manual requests against the local Spring Boot app.

## Source Docs To Read

- `../../docs/contracts/openapi/http/partner-source-slice1.http`
- `../../AGREED_SPEC.md` section `10. Acceptance Scenarios`

## Prereqs

- Full test suite passes.
- App starts locally on port `8080`.
- Manual failures get automated tests before fixes.

## Tests To Write First

No new automated tests.

This is a human verification pass after automated tests are green.

Before manual checks, run:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Before manual checks, run.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd test
```

If any manual request fails, add or update the matching automated test from tasks 07 through 15 first, watch it fail, then fix the code.
## File Map

No application files should be created.

Reference checklist:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `../../docs/contracts/openapi/http/partner-source-slice1.http`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
../../docs/contracts/openapi/http/partner-source-slice1.http
```

## Exact Code

Start the app:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Start the app.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd spring-boot:run
```

In a second PowerShell window:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for In a second PowerShell window.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
Invoke-RestMethod http://localhost:8080/health
Invoke-RestMethod http://localhost:8080/ready
Invoke-RestMethod http://localhost:8080/api/v1/orders/ORD-1001/status
Invoke-RestMethod "http://localhost:8080/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"
Invoke-RestMethod http://localhost:8080/api/v1/drivers/DRV-2001
Invoke-RestMethod "http://localhost:8080/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"
Invoke-RestMethod "http://localhost:8080/api/v1/drivers/DRV-2003/assignments?page=1&pageSize=20"

```

Post success event:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Post success event.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
$body = @{
  driverId = "DRV-2001"
  status = "DELIVERED"
  occurredAt = "2026-07-02T10:30:00+08:00"
  note = "Left with reception"
  proofOfDeliveryAvailable = $true
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/v1/orders/ORD-1001/status-events -ContentType "application/json" -Body $body

```

Expected negative checks:

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

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd test
.\mvnw.cmd spring-boot:run

```

Then run the manual requests listed in `Exact Code`.

## Done Criteria

- [x] Manual checklist passes through automated integration coverage.
- [x] Any discovered mismatch has an automated test before the fix.
- [x] Results are ready to compare with FastAPI later.

## Common Mistakes

- Fixing manual failures without adding automated tests.
- Forgetting mutation changes later status responses.
- Comparing against stale app output after code changed but app was not restarted.

## Stop / Do Not Add

- Do not make manual-only fixes without adding a test.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized and manual PowerShell checklist expanded.
- Marked done after the equivalent full-stack Spring integration checks and full Maven suite passed.
