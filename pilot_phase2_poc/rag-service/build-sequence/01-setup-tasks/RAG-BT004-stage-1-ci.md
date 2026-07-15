# RAG-BT004: Add Stage 1 CI, CodeQL, And Dependabot

Status: Draft

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.

| Field | Value |
|---|---|
| Task ID | `RAG-BT004` |
| Task Name | Add Stage 1 CI, CodeQL, And Dependabot |
| Source Question | CI/CD pipeline and security scan baseline |
| Decision / ADR | ADR-RAG-0010, ADR-RAG-0011 |
| Branch | `codex/rag-bt004-stage-1-ci` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-bt004-stage-1-ci` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Build: first GitHub Actions workflow and baseline security automation for
`rag-service`.

Goal: run quality, unit test, and security checks on PRs and `main` pushes.

Module:

```text
.github/workflows/rag-service-ci.yml
.github/workflows/codeql.yml
.github/dependabot.yml
```

Acceptance Criteria:

- workflow runs on pull requests to `main`
- workflow runs on pushes to `main`
- workflow sets up Python and installs service dependencies with `uv`
- workflow verifies the application can be imported or tested through pytest
- workflow runs Ruff format check
- workflow runs Ruff lint check
- workflow runs pytest
- workflow runs Bandit
- workflow runs pip-audit
- CodeQL workflow/config exists for Python code scanning
- Dependabot config exists for Python dependency review
- secret-scanning evidence is recorded as GitHub public repository behavior or
  repo setting evidence
- workflow documents that Dockerized dependency tests are not part of Stage 1

Out Of Scope:

- Docker image build
- Dockerized Qdrant integration tests
- Dockerized test database/service dependencies
- Trivy
- RAG regression

## 2. Worktree And Branch Setup

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-bt004"
$Slug = "stage-1-ci"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"
New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
git -C $RepoRoot fetch origin
git -C $RepoRoot pull --ff-only origin main
git -C $RepoRoot config core.longpaths true
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

### Linux / macOS Bash

```bash
REPO_ROOT="$HOME/code/waypoint-pilot"
WORKTREE_ROOT="$HOME/code/waypoint-pilot-worktrees"
TASK_ID="rag-bt004"
SLUG="stage-1-ci"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"
mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" config core.longpaths true
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Test Code Or Acceptance Check

Expected failing reason before implementation: workflow/config files do not
exist.

### Windows PowerShell Acceptance Check

```powershell
$WorkflowPath = "$WorktreePath\.github\workflows\rag-service-ci.yml"
$CodeQlPath = "$WorktreePath\.github\workflows\codeql.yml"
$DependabotPath = "$WorktreePath\.github\dependabot.yml"
Test-Path $WorkflowPath
Test-Path $CodeQlPath
Test-Path $DependabotPath
```

### Linux / macOS Bash Acceptance Check

```bash
WORKFLOW_PATH="$WORKTREE_PATH/.github/workflows/rag-service-ci.yml"
CODEQL_PATH="$WORKTREE_PATH/.github/workflows/codeql.yml"
DEPENDABOT_PATH="$WORKTREE_PATH/.github/dependabot.yml"
test -f "$WORKFLOW_PATH"
test -f "$CODEQL_PATH"
test -f "$DEPENDABOT_PATH"
```

## 4. Implementation

Create these files at the repository root:

- `.github/workflows/rag-service-ci.yml`
- `.github/workflows/codeql.yml`
- `.github/dependabot.yml`

Stage 1 CI builds the Python application environment, not the final Docker
image. Unit tests must not require Dockerized Qdrant, external LLM calls, or
network access.

### Windows PowerShell Implementation File Creation

```powershell
$WorkflowDir = "$WorktreePath\.github\workflows"
New-Item -ItemType Directory -Force -Path $WorkflowDir | Out-Null
New-Item -ItemType Directory -Force -Path "$WorktreePath\.github" | Out-Null
@'
name: rag-service-ci

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: pilot_phase2_poc/rag-service
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install uv
      - run: uv sync --all-extras --dev
      - run: uv run ruff format --check .
      - run: uv run ruff check .
      - run: uv run pytest -q
      - run: uv run bandit -r app -ll
      - run: uv run pip-audit --strict
'@ | Set-Content -Path "$WorkflowDir\rag-service-ci.yml" -Encoding UTF8
```

Create CodeQL and Dependabot config:

```powershell
@'
name: codeql

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  schedule:
    - cron: "0 3 * * 1"

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      packages: read
      actions: read
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: python
      - uses: github/codeql-action/analyze@v3
'@ | Set-Content -Path "$WorkflowDir\codeql.yml" -Encoding UTF8

@'
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/pilot_phase2_poc/rag-service"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
'@ | Set-Content -Path "$WorktreePath\.github\dependabot.yml" -Encoding UTF8
```

### Linux / macOS Bash Implementation File Creation

```bash
WORKFLOW_DIR="$WORKTREE_PATH/.github/workflows"
mkdir -p "$WORKFLOW_DIR" "$WORKTREE_PATH/.github"
cat > "$WORKFLOW_DIR/rag-service-ci.yml" <<'EOF'
name: rag-service-ci

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: pilot_phase2_poc/rag-service
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install uv
      - run: uv sync --all-extras --dev
      - run: uv run ruff format --check .
      - run: uv run ruff check .
      - run: uv run pytest -q
      - run: uv run bandit -r app -ll
      - run: uv run pip-audit --strict
EOF
```

```bash
cat > "$WORKFLOW_DIR/codeql.yml" <<'EOF'
name: codeql

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  schedule:
    - cron: "0 3 * * 1"

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      packages: read
      actions: read
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: python
      - uses: github/codeql-action/analyze@v3
EOF

cat > "$WORKTREE_PATH/.github/dependabot.yml" <<'EOF'
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/pilot_phase2_poc/rag-service"
    schedule:
      interval: "weekly"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
EOF
```

## 5. Test Execution

### Windows PowerShell

```powershell
git -C $WorktreePath diff --check
cd "$WorktreePath\pilot_phase2_poc\rag-service"
uv sync --all-extras --dev
uv run ruff format --check .
uv run ruff check .
uv run pytest -q
uv run bandit -r app -ll
uv run pip-audit --strict
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" diff --check
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv sync --all-extras --dev
uv run ruff format --check .
uv run ruff check .
uv run pytest -q
uv run bandit -r app -ll
uv run pip-audit --strict
```

## 6. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add .github pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "ci(rag): add stage 1 quality and security checks"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add .github pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "ci(rag): add stage 1 quality and security checks"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to `main`.

## 7. Merge

Merge only after PR CI/CD passes and confirm `main` CI/CD also passes. Then
clean up the worktree, delete the merged local branch, and delete the merged
remote branch when permitted.

## 8. Task Evidence

Branch:
Worktree:
PR:
Commit:

Files Changed:
-

Tests Run:
-

CI Result:

AI Review Findings:
-

Human Review Notes:
-

Issues Encountered:
-

Resolution:
-

Debt / Follow-Ups:
-


