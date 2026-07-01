# 02 - CI Pipeline

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
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: python -m pytest
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

- [ ] Workflow file exists at repo root.
- [ ] Workflow uses Python 3.12.
- [ ] Workflow runs pytest.
- [ ] Workflow path filters include this module and local docs/contracts.
- [ ] CI is green after push or PR.

## Stop / Do Not Add

- Do not add deployment.
- Do not add Docker publishing.
- Do not add ruff or coverage until pytest CI is green.

