# Partner Source Parity Checks

This folder contains the local parity harness that compares the Spring Boot and FastAPI implementations against the same Slice 1 contract.

## Current Status

The parity harness is implemented and has a latest generated report:

```text
reports\latest\parity-report.md
reports\latest\parity-report.json
```

Latest result:

| Total scenarios | Passed | Failed | Skipped |
|---:|---:|---:|---:|
| 24 | 24 | 0 | 0 |

Use the numbered parity build book for the implementation sequence:

```text
build-sequence\00-index.md
```

The detailed implementation proposal is:

```text
PARITY_CHECKS_PROPOSAL.md
```

## Purpose

The parity checks:

- target Spring Boot on one base URL
- target FastAPI on another base URL
- run the same request matrix against both
- compare HTTP status codes
- compare required JSON fields
- compare enum values
- compare error envelope shape
- compare `errorCode`
- compare health and readiness behavior
- write human and machine-readable reports

## Inputs

Use these canonical sources:

```text
..\docs\contracts\openapi\partner-source.v1.yaml
..\docs\contracts\openapi\http\partner-source-slice1.http
..\docs\contracts\shared-error-contract.md
```

## Local Run

Start Spring Boot:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd spring-boot:run
```

Start FastAPI:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Run parity:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\parity
python -m parity_runner
```

Run parity harness tests:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\parity
python -m pytest
```

## Reports

Latest reports:

```text
reports\latest\parity-report.md
reports\latest\parity-report.json
```

Timestamped archives:

```text
reports\runs\<timestamp>\parity-report.md
reports\runs\<timestamp>\parity-report.json
```

## Stop Rule

Do not claim FastAPI parity until the same manual checklist passes against both implementations.
