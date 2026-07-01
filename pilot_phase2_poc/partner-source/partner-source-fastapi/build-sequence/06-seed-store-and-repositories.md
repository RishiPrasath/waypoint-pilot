# 06 - Seed Store And Repositories

## Purpose

Create deterministic in-memory seed data and repository classes for FastAPI.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `7. Seed Data`
- `../../docs/active/data-and-seed-handoff.md`
- `../../partner-source-springboot/build-sequence/06-seed-store-and-repositories.md`

## Tests To Write First

Create:

```text
tests/repositories/test_orders_repository.py
tests/repositories/test_drivers_repository.py
tests/repositories/test_assignments_repository.py
tests/repositories/test_status_events_repository.py
```

Test cases:

- `ORD-1001` exists and current status is `OUT_FOR_DELIVERY`.
- `ORD-9999` is missing.
- `DRV-2001` exists and is `AVAILABLE`.
- `DRV-9999` is missing.
- `DRV-2001` has active assignments `ASN-3001` and `ASN-3002`.
- `DRV-2003` has no active assignments.
- `ORD-1001` has events `EVT-4001` through `EVT-4005` in chronological order.

## Code To Implement

Domain:

```text
app/domain/orders.py
app/domain/drivers.py
app/domain/assignments.py
```

Seed:

```text
app/seed/manifest.py
app/seed/loader.py
app/seed/store.py
```

Repositories:

```text
app/repositories/orders.py
app/repositories/drivers.py
app/repositories/assignments.py
app/repositories/status_events.py
```

Use dataclasses or plain classes for internal domain objects. Use Pydantic at the API schema edge.

## Commands To Run

```powershell
python -m pytest tests/repositories
python -m pytest
```

## Done Criteria

- [ ] Seed data matches agreed IDs and scenarios.
- [ ] Repositories are in-memory only.
- [ ] Tests prove missing IDs.
- [ ] No SQLAlchemy or database dependency exists.

## Stop / Do Not Add

- Do not add SQLAlchemy, Alembic, or database URLs.
- Do not add API routers in this step.

