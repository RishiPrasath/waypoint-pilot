# RAG-DT023: Runtime Reliability, SLO, Capacity, And Deployment Contract

Status: Planned

| Field | Value |
|---|---|
| Task ID | `RAG-DT023` |
| Lane | design |
| Dependencies | `RAG-DT011`, `RAG-DT014`, `RAG-DT017`, `RAG-DT021` |
| Blocks | `RAG-DT013`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, `RAG-BT020`, `RAG-BT021`, `RAG-BT022` |
| Responsible | Platform/SRE owner |
| Accountable approver | Platform/operations owner |
| Required reviewers | Security owner, service owner, cost owner |
| Branch | `codex/rag-dt023-runtime-reliability-deployment` |
| Worktree | `C:\tmp\rag-dt023-runtime-reliability-deployment` |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT023-runtime-reliability-deployment.md` |

## 1. Objective And Scope

Define the runtime envelope and evidence required for local PoC, shared
service, or production operation. Close the current gaps in readiness
semantics, timeouts, concurrency, capacity, recovery, deployment, and cost.

## 2. Dependencies And Gates

Consume Docker/Qdrant and security decisions. Historical DT019/DT020 artifacts
are review inputs, not gating dependencies. The selected deployment tier must
determine which reliability and recovery controls are mandatory and must drive
the reopened DT019/DT020 revisions.

## 3. Expected Artifacts

```text
docs/design/runtime-reliability-slo-capacity-and-deployment-contract.md
docs/operations/deployment-environment-matrix.md
docs/operations/failure-and-recovery-matrix.md
docs/operations/configuration-matrix.md
docs/operations/readiness-contract.md
build-evidence/RAG-DT023-runtime-reliability-deployment.md
```

## 4. Acceptance Criteria

- Environment matrix defines local, CI, shared test, staging, and production
  applicability without implying environments that do not exist.
- `/health` is liveness and `/ready` is dependency-aware readiness after
  dependencies are integrated; `/health` remains process-only, readiness
  failure returns a non-success status, and provider readiness is non-billable
  rather than a live generation call.
- The configuration matrix makes the Pydantic `RAG_` names canonical,
  including `RAG_QDRANT_URL`, `RAG_QDRANT_API_KEY`,
  `RAG_QDRANT_COLLECTION_NAME`, and `RAG_ENVIRONMENT`; obsolete bare
  `QDRANT_*` and `RAG_ENV` guidance is reconciled or explicitly historical.
- SLOs or PoC budgets define availability, p50/p95/p99 latency, error rate,
  retrieval/generation time budgets, and recovery expectations.
- Sync/async boundaries, cancellation, client pooling, concurrency,
  backpressure, retries, jitter, circuit breaking, and idempotency are defined.
- Groq-compatible provider rate/quota/cost behavior and degraded/fallback
  behavior are explicit.
- Numeric request-byte, input-token, source-filter-cardinality, context,
  output-token, per-caller rate, concurrency/backpressure, deadline, retry,
  provider-quota, and cost-ceiling budgets are declared by tier.
- Qdrant sizing, vector/index assumptions, disk/RAM budget, collection
  lifecycle, backup/snapshot, restore test, RPO/RTO, replication, and scaling
  are selected or tier-specific deferred.
- Load, soak, dependency-failure, restore, and rollback tests have concrete
  commands and pass criteria.
- Observability includes structured logs, correlation IDs, metrics, traces,
  alert ownership, redaction, and runbooks.

## 5. Preflight

Record the present behavior of `/health` and `/ready`, current dependency
scaffolds, Docker plan, Qdrant strategy, and provider configuration.

## 6. Red Check

```powershell
Test-Path docs/design/runtime-reliability-slo-capacity-and-deployment-contract.md
Test-Path docs/operations/failure-and-recovery-matrix.md
Test-Path docs/operations/configuration-matrix.md
Test-Path docs/operations/readiness-contract.md
```

Both results must be `False` before implementation.

## 7. Implementation Or Design Work

1. Select the deployment tier and workload envelope.
2. Define liveness/readiness/startup semantics.
3. Reconcile configuration names and deployment profiles against the actual
   settings model; declare the canonical environment-variable matrix.
4. Allocate latency, retry, quota, and cost budgets by dependency.
5. Define concurrency, backpressure, cancellation, and failure behavior.
6. Size Qdrant and define collection validation, namespace/versioning,
   migration, backup/restore/rollback requirements.
7. Define load, failure, recovery, and observability evidence.
8. Update affected build tasks and readiness terminology.

## 8. Verification Matrix

| Check | Required Result |
|---|---|
| Readiness | Dependency failure makes readiness fail |
| Configuration | One canonical `RAG_` configuration matrix matches the settings model |
| Load | Target workload meets declared latency/error budgets |
| Failure | Qdrant/provider timeout and outage behavior is bounded |
| Recovery | Restore/rollback evidence meets declared RPO/RTO |
| Cost/quota | Request and provider budgets have enforceable limits |

## 9. PR Handoff

Summarize deployment tier, workload assumptions, SLOs/budgets, failure
behavior, recovery objectives, and affected build tasks.

## 10. Merge And Closeout

Require platform, operations, security, and service-owner review. Keep any
production-ready verdict prohibited until all production-tier controls have
evidence.

## 11. Out Of Scope And Deferred Work

A local PoC may defer HA and managed infrastructure. It may not be relabeled
production-ready while those controls remain out of scope.
