# 16 - Manual HTTP Checklist

## Purpose

Run the canonical manual requests against the local FastAPI app.

## Source Docs To Read

- `../../docs/contracts/openapi/http/partner-source-slice1.http`
- `../../AGREED_SPEC.md` section `10. Acceptance Scenarios`
- `../../partner-source-springboot/build-sequence/16-manual-http-checklist.md`

## Tests To Write First

No new automated tests. This is a human verification pass after pytest is green.

## Code To Implement

No code. Fix only if manual requests reveal drift from the agreed spec or Spring Boot reference behavior.

## Commands To Run

Start the app:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
python -m uvicorn app.main:app --reload
```

In a second PowerShell window:

```powershell
Invoke-RestMethod http://localhost:8000/health
Invoke-RestMethod http://localhost:8000/ready
Invoke-RestMethod http://localhost:8000/api/v1/orders/ORD-1001/status
Invoke-RestMethod "http://localhost:8000/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"
Invoke-RestMethod http://localhost:8000/api/v1/drivers/DRV-2001
Invoke-RestMethod "http://localhost:8000/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"
```

Post success event:

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

## Expected Results

- `/health`: `200`, `UP`.
- `/ready`: `200`, `READY`.
- `ORD-1001/status`: `OUT_FOR_DELIVERY` before status-event mutation.
- `ORD-1001/timeline`: chronological events.
- `DRV-2001`: `activeAssignmentCount = 2`.
- `DRV-2001/assignments`: two active items.
- Status event success: `201`, new/current status `DELIVERED`.

## Done Criteria

- [ ] Manual checklist passes.
- [ ] Any discovered mismatch has an automated test before the fix.
- [ ] Results are ready for parity comparison.

## Stop / Do Not Add

- Do not make manual-only fixes without adding a test.

