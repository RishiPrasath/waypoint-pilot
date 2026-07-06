# 20 - Access Policy And Route Guards

## Status

- Status: Done
- Last Updated: 2026-07-06

## Goal

Protect FastAPI `/api/v1/**` routes with dependency-based auth and the access-control matrix.

## Tests First

```powershell
python -m pytest tests/api/test_access_control_endpoint.py
```

## Implementation Files

```text
app/security/dependencies.py
app/security/access_policy.py
app/api/orders.py
app/api/drivers.py
```

## Done Criteria

- [x] Protected routes require bearer tokens.
- [x] Wrong role/resource returns `ACCESS_DENIED`.
- [x] Public health/readiness behavior is preserved.

