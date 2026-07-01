# 07 - Health Endpoint

## Purpose

Implement `GET /health`.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `3. Endpoints` and `8. Response Shapes`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../partner-source-springboot/build-sequence/07-health-endpoint.md`

## Tests To Write First

Create:

```text
tests/api/test_health_api.py
```

Test with TestClient:

- `GET /health` returns `200`.
- Body includes `status = UP`.
- Body includes `service = partner-source`.

## Code To Implement

Create:

```text
app/api/health.py
app/schemas/shared.py
```

Update:

```text
app/main.py
```

Include the health router in `create_app()`.

## Commands To Run

```powershell
python -m pytest tests/api/test_health_api.py
python -m pytest
```

Manual check:

```powershell
python -m uvicorn app.main:app --reload
Invoke-RestMethod http://localhost:8000/health
```

## Done Criteria

- [ ] TestClient test passes.
- [ ] Endpoint is outside `/api/v1`.
- [ ] JSON field names match OpenAPI.

## Stop / Do Not Add

- Do not add readiness logic here.
- Do not add external health check packages.

