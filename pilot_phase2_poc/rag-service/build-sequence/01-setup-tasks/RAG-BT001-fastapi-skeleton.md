# RAG-BT001: Create FastAPI Project Skeleton

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT001` |
| Task Name | Create FastAPI Project Skeleton |
| Source Question | Codebase structure and setup |
| Decision / ADR | ADR-RAG-0001 |
| Branch | `codex/rag-bt001-fastapi-skeleton` |
| Worktree Path | `C:\tmp\rag-bt001-fastapi-skeleton` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-BT001-fastapi-skeleton.md` |

## 1. Task Definition

Build: the minimal Python/FastAPI package skeleton for `rag-service`.

Goal: create the service root, Python project files, app entrypoint, accepted
stage folders, shared folders, KB placeholder, and module-local test folders.

Module: `pilot_phase2_poc/rag-service`.

Acceptance Criteria:

- `pyproject.toml` exists
- `app/main.py` exists
- `app/api/router.py` exists for future API route registration
- `app/core/config.py`, `app/core/dependencies.py`, and `app/core/logging.py`
  placeholders exist
- accepted stage structure exists with Python-safe stage package names
- each Python package has `__init__.py`
- module-local test folders exist
- shared schema, error, and vector DB folders exist as placeholders
- `knowledge_base/README.md` exists as the KB root placeholder
- a failing app import smoke test is written before implementation

Out Of Scope:

- real health endpoint behavior
- CI workflow
- Qdrant client behavior
- final KB folder layout
- KB registry schema or content
- real ingestion, query, retrieval, generation, or evaluation behavior

## 2. Worktree And Branch Setup

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-bt001"
$Slug = "fastapi-skeleton"
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
TASK_ID="rag-bt001"
SLUG="fastapi-skeleton"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" config core.longpaths true
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Test Code

Create the failing app import smoke test first. Expected failing reason: the
project package and/or FastAPI app does not exist.

### Windows PowerShell Test File Creation

```powershell
$TestPath = Join-Path $WorktreePath "pilot_phase2_poc/rag-service/app/api/tests/test_app_smoke.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@'
from app.main import app


def test_fastapi_app_exists():
    assert app.title == "rag-service"
'@ | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/api/tests/test_app_smoke.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
from app.main import app


def test_fastapi_app_exists():
    assert app.title == "rag-service"
EOF
```

## 4. Implementation

Create the minimal project scaffold only.

### Required Structure

```text
pilot_phase2_poc/rag-service/
  .python-version
  pyproject.toml
  knowledge_base/
    README.md
  app/
    __init__.py
    main.py
    api/
      __init__.py
      router.py
      tests/
    core/
      __init__.py
      config.py
      dependencies.py
      logging.py
      tests/
    shared/
      __init__.py
      errors/
        __init__.py
      schemas/
        __init__.py
      tests/
      vector_db/
        __init__.py
        tests/
    stages/
      __init__.py
      stage_01_ingestion/
        __init__.py
        schemas.py
        service.py
        parsers/
        chunkers/
        tests/
      stage_02_query/
        __init__.py
        schemas.py
        service.py
        validators.py
        tests/
      stage_03_retrieval/
        __init__.py
        schemas.py
        service.py
        retrievers/
        tests/
      stage_04_generation/
        __init__.py
        schemas.py
        service.py
        client.py
        validation.py
        tests/
      stage_05_evaluation/
        __init__.py
        schemas.py
        service.py
        tests/
```

The accepted ADR names stages as `01-ingestion`, `02-query`, `03-retrieval`,
`04-generation`, and `05-evaluation`. The implementation uses Python-safe
package names (`stage_01_ingestion`, etc.) while preserving the same order and
meaning.

### Windows PowerShell Implementation File Creation

```powershell
$ServiceRoot = Join-Path $WorktreePath "pilot_phase2_poc/rag-service"
$Dirs = @(
  "app/api/tests",
  "app/core/tests",
  "app/shared/errors",
  "app/shared/schemas",
  "app/shared/tests",
  "app/shared/vector_db/tests",
  "app/stages/stage_01_ingestion/parsers",
  "app/stages/stage_01_ingestion/chunkers",
  "app/stages/stage_01_ingestion/tests",
  "app/stages/stage_02_query/tests",
  "app/stages/stage_03_retrieval/retrievers",
  "app/stages/stage_03_retrieval/tests",
  "app/stages/stage_04_generation/tests",
  "app/stages/stage_05_evaluation/tests",
  "knowledge_base"
)
foreach ($dir in $Dirs) {
  New-Item -ItemType Directory -Force -Path (Join-Path $ServiceRoot $dir) | Out-Null
}
```

Create minimal files after the directories exist:

```powershell
$Files = @(
  ".python-version",
  "app/__init__.py",
  "app/api/__init__.py",
  "app/api/router.py",
  "app/core/__init__.py",
  "app/core/config.py",
  "app/core/dependencies.py",
  "app/core/logging.py",
  "app/shared/__init__.py",
  "app/shared/errors/__init__.py",
  "app/shared/schemas/__init__.py",
  "app/shared/vector_db/__init__.py",
  "app/stages/__init__.py",
  "app/stages/stage_01_ingestion/__init__.py",
  "app/stages/stage_01_ingestion/schemas.py",
  "app/stages/stage_01_ingestion/service.py",
  "app/stages/stage_02_query/__init__.py",
  "app/stages/stage_02_query/schemas.py",
  "app/stages/stage_02_query/service.py",
  "app/stages/stage_02_query/validators.py",
  "app/stages/stage_03_retrieval/__init__.py",
  "app/stages/stage_03_retrieval/schemas.py",
  "app/stages/stage_03_retrieval/service.py",
  "app/stages/stage_04_generation/__init__.py",
  "app/stages/stage_04_generation/schemas.py",
  "app/stages/stage_04_generation/service.py",
  "app/stages/stage_04_generation/client.py",
  "app/stages/stage_04_generation/validation.py",
  "app/stages/stage_05_evaluation/__init__.py",
  "app/stages/stage_05_evaluation/schemas.py",
  "app/stages/stage_05_evaluation/service.py",
  "knowledge_base/README.md"
)
foreach ($file in $Files) {
  $path = Join-Path $ServiceRoot $file
  New-Item -ItemType Directory -Force -Path (Split-Path $path) | Out-Null
  if (-not (Test-Path $path)) { New-Item -ItemType File -Path $path | Out-Null }
}
```

Create the minimal app and project files:

```powershell
@'
from fastapi import FastAPI

app = FastAPI(title="rag-service")
'@ | Set-Content -Path (Join-Path $ServiceRoot "app/main.py") -Encoding UTF8

@'
[project]
name = "rag-service"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "fastapi",
  "pydantic",
  "pydantic-settings",
  "uvicorn",
]

[dependency-groups]
dev = [
  "bandit",
  "httpx",
  "pip-audit",
  "pytest",
  "ruff",
]
'@ | Set-Content -Path (Join-Path $ServiceRoot "pyproject.toml") -Encoding UTF8

"3.12" | Set-Content -Path (Join-Path $ServiceRoot ".python-version") -Encoding UTF8
"# Knowledge Base`n" | Set-Content -Path (Join-Path $ServiceRoot "knowledge_base/README.md") -Encoding UTF8
```

### Linux / macOS Bash Implementation File Creation

```bash
SERVICE_ROOT="$WORKTREE_PATH/pilot_phase2_poc/rag-service"
mkdir -p \
  "$SERVICE_ROOT/app/api/tests" \
  "$SERVICE_ROOT/app/core/tests" \
  "$SERVICE_ROOT/app/shared/errors" \
  "$SERVICE_ROOT/app/shared/schemas" \
  "$SERVICE_ROOT/app/shared/tests" \
  "$SERVICE_ROOT/app/shared/vector_db/tests" \
  "$SERVICE_ROOT/app/stages/stage_01_ingestion/parsers" \
  "$SERVICE_ROOT/app/stages/stage_01_ingestion/chunkers" \
  "$SERVICE_ROOT/app/stages/stage_01_ingestion/tests" \
  "$SERVICE_ROOT/app/stages/stage_02_query/tests" \
  "$SERVICE_ROOT/app/stages/stage_03_retrieval/retrievers" \
  "$SERVICE_ROOT/app/stages/stage_03_retrieval/tests" \
  "$SERVICE_ROOT/app/stages/stage_04_generation/tests" \
  "$SERVICE_ROOT/app/stages/stage_05_evaluation/tests" \
  "$SERVICE_ROOT/knowledge_base"
```

```bash
touch \
  "$SERVICE_ROOT/app/__init__.py" \
  "$SERVICE_ROOT/app/api/__init__.py" \
  "$SERVICE_ROOT/app/api/router.py" \
  "$SERVICE_ROOT/app/core/__init__.py" \
  "$SERVICE_ROOT/app/core/config.py" \
  "$SERVICE_ROOT/app/core/dependencies.py" \
  "$SERVICE_ROOT/app/core/logging.py" \
  "$SERVICE_ROOT/app/shared/__init__.py" \
  "$SERVICE_ROOT/app/shared/errors/__init__.py" \
  "$SERVICE_ROOT/app/shared/schemas/__init__.py" \
  "$SERVICE_ROOT/app/shared/vector_db/__init__.py" \
  "$SERVICE_ROOT/app/stages/__init__.py" \
  "$SERVICE_ROOT/app/stages/stage_01_ingestion/__init__.py" \
  "$SERVICE_ROOT/app/stages/stage_01_ingestion/schemas.py" \
  "$SERVICE_ROOT/app/stages/stage_01_ingestion/service.py" \
  "$SERVICE_ROOT/app/stages/stage_02_query/__init__.py" \
  "$SERVICE_ROOT/app/stages/stage_02_query/schemas.py" \
  "$SERVICE_ROOT/app/stages/stage_02_query/service.py" \
  "$SERVICE_ROOT/app/stages/stage_02_query/validators.py" \
  "$SERVICE_ROOT/app/stages/stage_03_retrieval/__init__.py" \
  "$SERVICE_ROOT/app/stages/stage_03_retrieval/schemas.py" \
  "$SERVICE_ROOT/app/stages/stage_03_retrieval/service.py" \
  "$SERVICE_ROOT/app/stages/stage_04_generation/__init__.py" \
  "$SERVICE_ROOT/app/stages/stage_04_generation/schemas.py" \
  "$SERVICE_ROOT/app/stages/stage_04_generation/service.py" \
  "$SERVICE_ROOT/app/stages/stage_04_generation/client.py" \
  "$SERVICE_ROOT/app/stages/stage_04_generation/validation.py" \
  "$SERVICE_ROOT/app/stages/stage_05_evaluation/__init__.py" \
  "$SERVICE_ROOT/app/stages/stage_05_evaluation/schemas.py" \
  "$SERVICE_ROOT/app/stages/stage_05_evaluation/service.py"

cat > "$SERVICE_ROOT/app/main.py" <<'EOF'
from fastapi import FastAPI

app = FastAPI(title="rag-service")
EOF

cat > "$SERVICE_ROOT/pyproject.toml" <<'EOF'
[project]
name = "rag-service"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "fastapi",
  "pydantic",
  "pydantic-settings",
  "uvicorn",
]

[dependency-groups]
dev = [
  "bandit",
  "httpx",
  "pip-audit",
  "pytest",
  "ruff",
]
EOF

printf '3.12\n' > "$SERVICE_ROOT/.python-version"
printf '# Knowledge Base\n' > "$SERVICE_ROOT/knowledge_base/README.md"
```

## 5. Test Execution

### Windows PowerShell

```powershell
cd "$WorktreePath\pilot_phase2_poc\rag-service"
uv run pytest app/api/tests/test_app_smoke.py -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest app/api/tests/test_app_smoke.py -q
```

## 6. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "build(rag): add FastAPI project skeleton"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "build(rag): add FastAPI project skeleton"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to `main`.

## 7. Merge

Merge after local tests, PR review, PR CI/CD, and `main` CI/CD pass. Then clean
up the worktree.

## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-BT001-fastapi-skeleton.md`.
