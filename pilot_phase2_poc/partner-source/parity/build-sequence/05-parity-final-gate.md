# 05 - Parity Final Gate

## Purpose

Decide whether Spring Boot and FastAPI are contract-equivalent for Partner Source Slice 1.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../CONTRACT_SYNC.md`
- `01-contract-source-check.md`
- `02-manual-request-matrix.md`
- `03-springboot-vs-fastapi-response-checks.md`
- `04-error-contract-checks.md`

## Required Preconditions

- [ ] Spring Boot final gate passed.
- [ ] FastAPI final gate passed.
- [ ] Both apps can run locally at known base URLs.
- [ ] Both apps start from deterministic seed data.
- [ ] Manual request matrix has been run against both.

## Tests To Run

For each module:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test

cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
python -m pytest
```

Run parity checks only after they exist:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\parity
python -m pytest
```

## Final Checklist

- [ ] Same endpoints.
- [ ] Same success HTTP statuses.
- [ ] Same required response fields.
- [ ] Same enum values.
- [ ] Same seed scenarios.
- [ ] Same error HTTP statuses.
- [ ] Same `errorCode` values.
- [ ] Same ProblemDetail required fields.
- [ ] No extra behavior in FastAPI.
- [ ] No contract drift from Spring Boot implementation.

## Done Criteria

Parity is complete when this statement is true:

```text
Spring Boot and FastAPI produce equivalent Partner Source Slice 1 behavior for the shared request matrix.
```

## Stop / Do Not Add

- Do not claim parity if the manual checklist differs.
- Do not create new contract rules in the parity layer.
