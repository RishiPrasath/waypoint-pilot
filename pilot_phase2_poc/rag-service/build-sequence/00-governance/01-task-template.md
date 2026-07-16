# Task Template

Use this structure for new or rewritten setup, design, and build tasks.

```markdown
# RAG-$TaskId: $TaskName

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-$TaskId` |
| Lane | setup / design / build |
| Dependencies | task IDs or `none` |
| Blocks | task IDs or `none` |
| Branch | `codex/rag-$task_slug` |
| Worktree | `C:\tmp\rag-$task_slug` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-$TaskId-$slug.md` |

## 1. Objective And Scope

## 2. Dependencies And Gates

## 3. Expected Artifacts

## 4. Acceptance Criteria

## 5. Preflight

## 6. Red Check

## 7. Implementation Or Design Work

## 8. Verification Matrix

## 9. PR Handoff

## 10. Merge And Closeout

## 11. Out Of Scope And Deferred Work
```

Task files describe intended work. They should link to evidence, not duplicate
the durable closeout record.
