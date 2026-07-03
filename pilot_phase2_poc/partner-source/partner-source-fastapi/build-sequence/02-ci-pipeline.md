# 02 - CI Pipeline

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Create a simple GitHub Actions workflow that runs FastAPI tests in CI.

## Source Docs To Read

- `../../docs/support/cicd-pipeline-guide.md`
- `../../docs/active/test-and-acceptance-handoff.md`
- `01-project-setup.md`

## Prereqs

- Confirm the previous task is complete, or confirm the prerequisite files already exist.
- Read the source docs above before writing code.
- Keep FastAPI aligned with Spring Boot and the shared OpenAPI contract.

## Tests To Write First

No new test file for this task.

The CI task proves that existing tests run in GitHub Actions. Before creating the workflow, make sure this local test already exists:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for The CI task proves that existing tests run in GitHub Actions. Before creating the workflow, make sure this local test already exists.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
tests/test_app.py
```

Expected test content from task 01:

**Test Block Explanation**

- What this block does: Shows the test code to write first for `from fastapi.testclient import TestClient`, `from app.main import app`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```python
from fastapi.testclient import TestClient

from app.main import app


def test_app_starts() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code in {200, 404}

```

The workflow is done when CI runs `python -m pytest` or `uv run pytest` against that test suite.
## File Map

Create from the repository root:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Create from the repository root.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
.github/workflows/partner-source-fastapi-ci.yml
```

Use this workflow if using requirements files:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for Use this workflow if using requirements files.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Read indentation carefully: top-level keys define the workflow, nested keys define jobs and steps.

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

## Exact Code

Create `.github/workflows/partner-source-fastapi-ci.yml` from the repository root:

**Code Block Explanation**

- What this block does: Shows the exact YAML configuration for `.github/workflows/partner-source-fastapi-ci.yml`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read indentation carefully: top-level keys define the workflow, nested keys define jobs and steps.

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
      - uses: astral-sh/setup-uv@v8.1.0
      - run: uv sync --all-extras --dev
      - run: uv run pytest

```

This workflow intentionally runs only tests. Do not add deployment, Docker, databases, or parity scripts in this task.

## Commands To Run

Before pushing:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for `cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi`, `python -m pytest`.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
python -m pytest
```

Check Git from repo root:

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Check Git from repo root.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot
git status --short
```

## Done Criteria

- [x] Workflow file exists at repo root.
- [x] Workflow uses Python 3.12.
- [x] Workflow runs pytest.
- [x] Workflow path filters include this module and local docs/contracts.
- [x] CI is green after push or PR.

## Common Mistakes

- Putting tests outside the `tests/` tree.
- Creating files in a different package or folder than the file map.
- Adding endpoints, fields, statuses, seed data, or dependencies not named by the task.
- Skipping the focused test before the full test run.

## Stop / Do Not Add

- Do not add deployment.
- Do not add Docker publishing.
- Do not add ruff or coverage until pytest CI is green.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- The workflow was updated to use the `uv` setup path because the module is scaffolded with `uv`.
- The runner uses `actions/checkout@v5`, `actions/setup-python@v6`, and `astral-sh/setup-uv@v8.1.0`.
- The behavior stayed the same: GitHub installs Python 3.12, syncs dependencies, and runs `uv run pytest`.
