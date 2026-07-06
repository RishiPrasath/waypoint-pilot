# 19 - Demo Login And Principal

## Status

- Status: Done
- Last Updated: 2026-07-06

## Goal

Add deterministic demo login and principal extraction for FastAPI.

## Tests First

```powershell
python -m pytest tests/api/test_demo_login_endpoint.py
```

## Implementation Files

```text
app/api/auth.py
app/schemas/auth.py
app/security/principal.py
app/security/demo_tokens.py
app/security/authenticator.py
app/security/demo_login.py
```

## Done Criteria

- [x] Demo login returns deterministic bearer tokens.
- [x] Principal shape matches Spring Boot.
- [x] Unsupported identities return ProblemDetail.

