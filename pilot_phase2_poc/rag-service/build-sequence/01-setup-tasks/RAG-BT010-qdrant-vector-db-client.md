# RAG-BT010: Add Qdrant Vector DB Client Wrapper

Status: Draft

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-task-sequence-template-proposal.md.

| Field | Value |
|---|---|
| Task ID | `RAG-BT010` |
| Task Name | Add Qdrant Vector DB Client Wrapper |
| Source Question | Vector database selection |
| Decision / ADR | ADR-RAG-0002 |
| Branch | `codex/rag-bt010-qdrant-vector-db-client` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-bt010-qdrant-vector-db-client` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Build: Qdrant client wrapper.

Goal: isolate vector database access behind `app/shared/vector_db`.

Module: `app/shared/vector_db/`.

Acceptance Criteria:

- mocked client test passes
- collection settings are loaded from config
- collection contract fields are represented: collection name, vector size,
  distance metric, payload schema version, and optional embedding model/version
- client boundary supports upsert/search/delete test cleanup
- optional local Qdrant smoke test is documented

Out Of Scope:

- full ingestion
- production deployment
- embedding model selection

## 2. Worktree And Branch Setup

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-bt010"
$Slug = "qdrant-vector-db-client"
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
TASK_ID="rag-bt010"
SLUG="qdrant-vector-db-client"
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

Expected failing reason before implementation: `VectorDbConfig` is not
implemented.

### Windows PowerShell Test File Creation

```powershell
$TestPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\shared\vector_db\tests\test_qdrant_client.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@'
from app.shared.vector_db.client import VectorDbConfig


def test_vector_db_config_has_collection_name():
    config = VectorDbConfig(
        collection_name="rag_chunks_test",
        vector_size=384,
        distance="Cosine",
        payload_schema_version="v1",
        embedding_model_name="test-embedding-model",
    )

    assert config.collection_name == "rag_chunks_test"
    assert config.vector_size == 384
    assert config.distance == "Cosine"
    assert config.payload_schema_version == "v1"
'@ | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/shared/vector_db/tests/test_qdrant_client.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
from app.shared.vector_db.client import VectorDbConfig


def test_vector_db_config_has_collection_name():
    config = VectorDbConfig(
        collection_name="rag_chunks_test",
        vector_size=384,
        distance="Cosine",
        payload_schema_version="v1",
        embedding_model_name="test-embedding-model",
    )

    assert config.collection_name == "rag_chunks_test"
    assert config.vector_size == 384
    assert config.distance == "Cosine"
    assert config.payload_schema_version == "v1"
EOF
```

## 4. Implementation

Add config and wrapper classes under `app/shared/vector_db/`.

### Windows PowerShell Implementation File Creation

```powershell
$ClientPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\shared\vector_db\client.py"
New-Item -ItemType Directory -Force -Path (Split-Path $ClientPath) | Out-Null
@'
from typing import Literal

from pydantic import BaseModel


class VectorDbConfig(BaseModel):
    collection_name: str
    vector_size: int
    distance: Literal["Cosine", "Dot", "Euclid"] = "Cosine"
    payload_schema_version: str = "v1"
    embedding_model_name: str | None = None
    embedding_model_version: str | None = None
'@ | Set-Content -Path $ClientPath -Encoding UTF8
```

### Linux / macOS Bash Implementation File Creation

```bash
CLIENT_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/shared/vector_db/client.py"
mkdir -p "$(dirname "$CLIENT_PATH")"
cat > "$CLIENT_PATH" <<'EOF'
from typing import Literal

from pydantic import BaseModel


class VectorDbConfig(BaseModel):
    collection_name: str
    vector_size: int
    distance: Literal["Cosine", "Dot", "Euclid"] = "Cosine"
    payload_schema_version: str = "v1"
    embedding_model_name: str | None = None
    embedding_model_version: str | None = None
EOF
```

## 5. Test Execution

### Windows PowerShell

```powershell
cd "$WorktreePath\pilot_phase2_poc\rag-service"
uv run pytest app/shared/vector_db/tests -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest app/shared/vector_db/tests -q
```

Optional smoke test requires local Qdrant and must be marked explicitly.

## 6. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "feat(rag): add qdrant vector db client wrapper"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "feat(rag): add qdrant vector db client wrapper"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to `main`.

## 7. Merge

Merge after review and CI. Then clean up the worktree, delete the merged local
branch, and delete the merged remote branch when permitted.

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




