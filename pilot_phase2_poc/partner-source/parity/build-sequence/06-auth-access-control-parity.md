# 06 - Auth Access-Control Parity

## Status

- Status: Done
- Last Updated: 2026-07-06

## Goal

Expand parity checks so Spring Boot and FastAPI prove the same auth and access-control behavior.

## Matrix Group

```text
AUTH-01 missing-token-order-status
AUTH-02 invalid-token-order-status
AUTH-03 driver-own-profile
AUTH-04 driver-other-profile-denied
AUTH-05 driver-own-assignments
AUTH-06 driver-other-assignments-denied
AUTH-07 driver-assigned-order-status
AUTH-08 driver-unassigned-order-status-denied
AUTH-09 driver-assigned-status-event
AUTH-10 driver-unassigned-status-event-domain-denial
AUTH-11 driver-spoofed-body-driver-denied
AUTH-12 csa-read-order-status
AUTH-13 csa-status-event-write-denied
AUTH-14 health-public
AUTH-15 ready-policy
AUTH-16 demo-driver-login
AUTH-17 demo-csa-login
AUTH-18 unsupported-demo-login
```

## Commands

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\parity
python -m pytest
python -m parity_runner
```

## Done Criteria

- [x] Parity harness supports per-scenario auth headers.
- [x] Auth scenarios pass against both implementations.
- [x] Generated parity report is updated.

