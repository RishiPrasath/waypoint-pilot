# 17 - FastAPI Final Gate

## Purpose

Confirm the FastAPI parity implementation is complete enough for shared parity checks.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../CONTRACT_SYNC.md`
- `../../docs/active/test-and-acceptance-handoff.md`
- `../../partner-source-springboot/build-sequence/17-springboot-final-gate.md`

## Tests To Run

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
python -m pytest
```

If using `uv`:

```powershell
uv run pytest
```

## Final Review Checklist

- [ ] All Slice 1 endpoints exist.
- [ ] All response fields match OpenAPI.
- [ ] All required seed scenarios exist.
- [ ] Status transition policy matches Spring Boot.
- [ ] Assignment authorization matches Spring Boot.
- [ ] Errors use ProblemDetail with `errorCode` and `correlationId`.
- [ ] Manual HTTP checklist passes.
- [ ] GitHub Actions is green.
- [ ] No out-of-scope dependencies were added.

## Code To Implement

No new code. Only fix proven gaps with tests first.

## Done Criteria

FastAPI is ready when this statement is true:

```text
The FastAPI implementation matches the Partner Source Slice 1 contract and Spring Boot reference behavior.
```

## Next Step

Move to:

```text
..\..\parity\build-sequence\00-index.md
```

