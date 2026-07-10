# RAG-BT005: Add Config And Settings Module

Status: Draft

| Field | Value |
|---|---|
| Task ID | `RAG-BT005` |
| Task Name | Add Config And Settings Module |
| Source Question | Runtime configuration and secrets policy |
| Decision / ADR | ADR-RAG-0011 |
| Branch | `codex/rag-bt005-config-settings` |
| Worktree Path | `C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees\rag-bt005-config-settings` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Draft |

## 1. Task Definition

Build: typed configuration and safe environment handling.

Goal: centralize service settings before clients and providers are added.

Module: `app/core/config.py`.

Acceptance Criteria:

- settings load from environment
- defaults are safe for local development
- missing required secrets fail predictably only when secret-backed feature is used
- secrets are not logged

Out Of Scope:

- real Groq client
- real Qdrant client

## 2. Worktree And Branch Setup

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-bt005"
$Slug = "config-settings"
$Branch = "codex/$TaskId-$Slug"
$WorktreePath = Join-Path $WorktreeRoot "$TaskId-$Slug"
New-Item -ItemType Directory -Force -Path $WorktreeRoot | Out-Null
git -C $RepoRoot fetch origin
git -C $RepoRoot worktree add -b $Branch $WorktreePath origin/main
git -C $WorktreePath status --short --branch
```

### Linux / macOS Bash

```bash
REPO_ROOT="$HOME/code/waypoint-pilot"
WORKTREE_ROOT="$HOME/code/waypoint-pilot-worktrees"
TASK_ID="rag-bt005"
SLUG="config-settings"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"
mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```

## 3. Test Code

Expected failing reason before implementation: `Settings` is not implemented.

### Windows PowerShell Test File Creation

```powershell
$TestPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\core\tests\test_config.py"
New-Item -ItemType Directory -Force -Path (Split-Path $TestPath) | Out-Null
@'
from app.core.config import Settings


def test_settings_have_safe_local_defaults():
    settings = Settings()

    assert settings.environment == "local"
    assert settings.service_name == "rag-service"
'@ | Set-Content -Path $TestPath -Encoding UTF8
```

### Linux / macOS Bash Test File Creation

```bash
TEST_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/core/tests/test_config.py"
mkdir -p "$(dirname "$TEST_PATH")"
cat > "$TEST_PATH" <<'EOF'
from app.core.config import Settings


def test_settings_have_safe_local_defaults():
    settings = Settings()

    assert settings.environment == "local"
    assert settings.service_name == "rag-service"
EOF
```

## 4. Implementation

Create `app/core/config.py` with a Pydantic settings model.

### Windows PowerShell Implementation File Creation

```powershell
$ConfigPath = "$WorktreePath\pilot_phase2_poc\rag-service\app\core\config.py"
@'
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "rag-service"
    environment: str = "local"

    model_config = SettingsConfigDict(env_prefix="RAG_", env_file=".env")
'@ | Set-Content -Path $ConfigPath -Encoding UTF8
```

### Linux / macOS Bash Implementation File Creation

```bash
CONFIG_PATH="$WORKTREE_PATH/pilot_phase2_poc/rag-service/app/core/config.py"
cat > "$CONFIG_PATH" <<'EOF'
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "rag-service"
    environment: str = "local"

    model_config = SettingsConfigDict(env_prefix="RAG_", env_file=".env")
EOF
```

## 5. Test Execution

### Windows PowerShell

```powershell
cd "$WorktreePath\pilot_phase2_poc\rag-service"
uv run pytest app/core/tests/test_config.py -q
```

### Linux / macOS Bash

```bash
cd "$WORKTREE_PATH/pilot_phase2_poc/rag-service"
uv run pytest app/core/tests/test_config.py -q
```

## 6. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "feat(rag): add config settings"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "feat(rag): add config settings"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to `main`.

## 7. Merge

Merge after local checks, PR CI/CD, and `main` CI/CD. Then clean up the
worktree.

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
