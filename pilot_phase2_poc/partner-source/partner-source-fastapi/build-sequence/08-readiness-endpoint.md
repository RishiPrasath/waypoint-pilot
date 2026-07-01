# 08 - Readiness Endpoint

## Purpose

Implement `GET /ready` to prove in-memory persistence and seed data are ready.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `3. Endpoints` and `8. Response Shapes`
- `../../docs/active/data-and-seed-handoff.md`
- `../../partner-source-springboot/build-sequence/08-readiness-endpoint.md`

## Tests To Write First

Create:

```text
tests/services/test_readiness_service.py
tests/api/test_readiness_api.py
```

Test cases:

- Service reports ready when seed data exists.
- `GET /ready` returns `200`.
- Body includes `status = READY`, `service = partner-source`, `checks.persistence = UP`, and `checks.seedData = UP`.

## Code To Implement

Create:

```text
app/services/readiness.py
app/schemas/shared.py
```

Update:

```text
app/api/health.py
```

## Commands To Run

```powershell
python -m pytest tests/services/test_readiness_service.py tests/api/test_readiness_api.py
python -m pytest
```

Manual check:

```powershell
Invoke-RestMethod http://localhost:8000/ready
```

## Done Criteria

- [ ] Readiness tests pass.
- [ ] Endpoint is outside `/api/v1`.
- [ ] No database readiness check exists.

## Stop / Do Not Add

- Do not add database dependencies.
- Do not add deployment probe config.

