# 17 - Spring Boot Final Gate

## Purpose

Confirm the Spring Boot reference implementation is complete enough for FastAPI parity work.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../CONTRACT_SYNC.md`
- `../../docs/active/test-and-acceptance-handoff.md`

## Tests To Run

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```

If verify is configured:

```powershell
.\mvnw.cmd verify
```

## Final Review Checklist

- [ ] All Slice 1 endpoints exist.
- [ ] All response fields match OpenAPI.
- [ ] All required seed scenarios exist.
- [ ] Status transition policy matches the agreed table.
- [ ] Assignment authorization matches agreed behavior.
- [ ] Errors use ProblemDetail with `errorCode` and `correlationId`.
- [ ] Manual HTTP checklist passes.
- [ ] GitHub Actions is green.
- [ ] No out-of-scope dependencies were added.

## Code To Implement

No new code. Only fix proven gaps with tests first.

## Done Criteria

Spring Boot is ready when this statement is true:

```text
The Spring Boot implementation is the reference behavior for Partner Source Slice 1.
```

## Next Step

Move to:

```text
..\..\partner-source-fastapi\build-sequence\00-index.md
```

