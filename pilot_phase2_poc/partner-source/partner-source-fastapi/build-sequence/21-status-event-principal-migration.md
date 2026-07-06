# 21 - Status Event Principal Migration

## Status

- Status: Done
- Last Updated: 2026-07-06

## Goal

Prevent status-event driver spoofing while the request body still contains `driverId`.

## Tests First

```powershell
python -m pytest tests/api/test_create_status_event_endpoint.py tests/api/test_access_control_endpoint.py
```

## Done Criteria

- [x] Body `driverId` must match authenticated driver principal.
- [x] CSA writes are denied.
- [x] Unassigned matching driver still returns `ORDER_NOT_ASSIGNED_TO_DRIVER`.

