# 21 - Status Event Principal Migration

## Status

- Status: Done
- Last Updated: 2026-07-06

## Goal

Ensure status-event writes cannot spoof another driver while the request body still contains `driverId`.

## Tests First

```powershell
.\mvnw.cmd "-Dtest=AuthAccessIntegrationTest,StatusEventControllerTest" test
```

Expected coverage:

- token `DRV-2001` with body `DRV-2001` can proceed.
- token `DRV-2001` with body `DRV-2002` returns `403 ACCESS_DENIED`.
- token `DRV-2002` with body `DRV-2002` on `ORD-1001` returns `403 ORDER_NOT_ASSIGNED_TO_DRIVER`.

## Implementation Notes

- This is a compatibility step.
- The cleaner future contract should remove `driverId` from the status-event body and derive actor identity from the principal.

## Done Criteria

- [x] Body `driverId` must match authenticated driver principal.
- [x] Domain assignment denial remains separate from generic access denial.

