# 01 - Contract Source Check

## Purpose

Confirm the parity checks use the local Partner Source source of truth.

## Source Docs To Read

- `../../AGREED_SPEC.md`
- `../../CONTRACT_SYNC.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`
- `../../docs/contracts/shared-error-contract.md`
- `../../docs/contracts/openapi/http/partner-source-slice1.http`

## Tests To Write First

Future automated parity script should first test that required source files exist.

Suggested file later:

```text
parity/tests/test_contract_sources.py
```

Expected checks:

- OpenAPI file exists.
- Shared error contract exists.
- Manual HTTP checklist exists.
- Required paths exist in OpenAPI.
- Approved error codes exist in OpenAPI and shared error contract.

## Code To Implement

No parity code yet unless both implementations are ready.

When ready, create:

```text
parity/README.md
parity/tests/
parity/scripts/
```

## Commands To Run

Current manual source check:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source
Test-Path docs\contracts\openapi\partner-source.v1.yaml
Test-Path docs\contracts\shared-error-contract.md
Test-Path docs\contracts\openapi\http\partner-source-slice1.http
```

## Done Criteria

- [ ] Local contract files exist.
- [ ] Parity work points to `docs/contracts`, not external planning paths.
- [ ] No behavior is added in parity yet.

## Stop / Do Not Add

- Do not duplicate the contract into code constants without a provenance note.
