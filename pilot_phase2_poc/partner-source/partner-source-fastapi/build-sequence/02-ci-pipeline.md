# 02 - CI Pipeline

## Status

- Status: Done
- Last Updated: 2026-07-02

## Purpose

Create a simple GitHub Actions workflow that runs FastAPI tests in CI.

## Source Docs To Read

- `../../docs/support/cicd-pipeline-guide.md`
- `../../docs/active/test-and-acceptance-handoff.md`
- `01-project-setup.md`

## Tests To Write First

No new behavior test. The scaffold pytest from step 01 is the CI proof.

## Code To Implement

Create from the repository root:

```text
.github/workflows/partner-source-fastapi-ci.yml
```

Use this workflow if using requirements files:

```yaml
name: Partner Source FastAPI CI

on:
  pull_request:
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-fastapi/**"
      - "pilot_phase2_poc/partner-source/docs/**"
      - "pilot_phase2_poc/partner-source/AGREED_SPEC.md"
      - ".github/workflows/partner-source-fastapi-ci.yml"
  push:
    branches: [main]
    paths:
      - "pilot_phase2_poc/partner-source/partner-source-fastapi/**"
      - "pilot_phase2_poc/partner-source/docs/**"
      - "pilot_phase2_poc/partner-source/AGREED_SPEC.md"
      - ".github/workflows/partner-source-fastapi-ci.yml"

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: pilot_phase2_poc/partner-source/partner-source-fastapi
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
          cache: pip
      - uses: astral-sh/setup-uv@v8.1.0
      - run: uv sync --all-extras --dev
      - run: uv run pytest
```

If using `uv`, replace install/test steps with an official `uv` setup and `uv run pytest` after local `uv` setup is stable.

## Commands To Run

Before pushing:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
python -m pytest
```

Check Git from repo root:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot
git status --short
```

## Expected Output

- Local pytest passes.
- GitHub Actions workflow completes green.

## Done Criteria

- [x] Workflow file exists at repo root.
- [x] Workflow uses Python 3.12.
- [x] Workflow runs pytest.
- [x] Workflow path filters include this module and local docs/contracts.
- [x] CI is green after push or PR.

## Change Notes

- The workflow was updated to use the `uv` setup path because the module is scaffolded with `uv`.
- The runner uses `actions/checkout@v5`, `actions/setup-python@v6`, and `astral-sh/setup-uv@v8.1.0`.
- The behavior stayed the same: GitHub installs Python 3.12, syncs dependencies, and runs `uv run pytest`.

## Stop / Do Not Add

- Do not add deployment.
- Do not add Docker publishing.
- Do not add ruff or coverage until pytest CI is green.

