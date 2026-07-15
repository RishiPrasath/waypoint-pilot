# RAG Service Setup Task Lane

Status: Active
Date: 2026-07-09

This folder contains setup tasks for `rag-service`.

Setup tasks prepare the repository, FastAPI skeleton, CI/CD pipeline, quality
gates, security scan foundation, configuration, shared schemas, and vector DB
connection foundation.

They should not implement real RAG behavior.

## Template Rule

Every setup task must follow the accepted task execution template:

1. task definition
2. worktree and branch setup
3. test code or acceptance check
4. implementation
5. test execution
6. branch workflow
7. merge
8. task evidence

Each task must include Windows PowerShell and Linux/macOS Bash commands where
file creation or command execution is required. All tasks also follow
`../00-governance/`: create one matching file under `build-evidence/`, pass the
pre-PR evidence gate before opening a PR, and mark the task `Complete` only
after merged closeout and worktree cleanup are recorded.

## Task List

| Order | ID | Task | File | Status | Evidence |
|---:|---|---|---|---|---|
| 0 | `RAG-BT000` | Prove branch/worktree/PR workflow | `RAG-BT000-prove-workflow.md` | Complete | `build-evidence/RAG-BT000-prove-workflow.md` |
| 1 | `RAG-BT001` | Create FastAPI project skeleton | `RAG-BT001-fastapi-skeleton.md` | Complete | `build-evidence/RAG-BT001-fastapi-skeleton.md` |
| 2 | `RAG-BT002` | Add health endpoint | `RAG-BT002-health-endpoint.md` | Planned | `build-evidence/RAG-BT002-health-endpoint.md` |
| 3 | `RAG-BT003` | Add readiness endpoint | `RAG-BT003-readiness-endpoint.md` | Planned | `build-evidence/RAG-BT003-readiness-endpoint.md` |
| 4 | `RAG-BT004` | Add Stage 1 CI, CodeQL, and Dependabot | `RAG-BT004-stage-1-ci.md` | Planned | `build-evidence/RAG-BT004-stage-1-ci.md` |
| 5 | `RAG-BT005` | Add config/settings module | `RAG-BT005-config-settings.md` | Planned | `build-evidence/RAG-BT005-config-settings.md` |
| 6 | `RAG-BT006` | Add shared schemas and error envelope | `RAG-BT006-shared-schemas.md` | Planned | `build-evidence/RAG-BT006-shared-schemas.md` |
| 7 | `RAG-BT010` | Add Qdrant vector DB client wrapper | `RAG-BT010-qdrant-vector-db-client.md` | Planned | `build-evidence/RAG-BT010-qdrant-vector-db-client.md` |

## Boundary

If a task starts implementing ingestion, query planning, retrieval, generation,
or evaluation behavior, it belongs in `../03-build-tasks/`, not here.

## Main Sequence

The overall execution sequence is:

```text
../00-index.md
```

