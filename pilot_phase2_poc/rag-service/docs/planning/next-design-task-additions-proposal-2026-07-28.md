# Proposal: Next RAG Service Design Tasks

Status: Planning input; non-authoritative
Date: 2026-07-28
Scope: `pilot_phase2_poc/rag-service`
Owner: Waypoint RAG service team

## 1. Why This File Lives In `docs/planning/`

This document is a proposal about task additions. It is not itself an
executable design task, an implementation task, an evidence record, or a
sequence authorization.

The correct location is:

```text
docs/planning/next-design-task-additions-proposal-2026-07-28.md
```

The repository boundaries are:

| Location | Authority | Why this proposal does or does not belong there |
|---|---|---|
| `docs/planning/` | Planning input and decision preparation | Correct location for this proposal; it can be reviewed without becoming a runnable task. |
| `docs/design/` | Design contracts, decisions, schemas, and accepted technical artifacts | Not correct yet; placing an unapproved proposal here could make recommendations look accepted. |
| `build-sequence/02-design-tasks/` | Governed executable design tasks | Not correct; files there require the canonical task template, dependencies, red checks, verification, handoff, and evidence. |
| `build-sequence/03-build-tasks/` | Governed implementation tasks | Not correct; this document proposes design work and contains no implementation. |
| `build-evidence/` | Durable task closeout evidence | Not correct; no task has been executed or closed by this proposal. |

This placement prevents a planning recommendation from silently changing the
execution DAG or being mistaken for an accepted design decision.

## 2. Governance And Work-Environment Guardrails

This document deliberately:

- does not allocate a new task ID;
- does not change `build-sequence/00-index.md` or either lane index;
- does not change task status, dependencies, build gates, or evidence;
- does not create a branch, worktree, runtime module, dependency, workflow, or
  environment file;
- does not authorize implementation;
- does not stage editor-only files such as `rag-service.code-workspace`.

If the owner approves a recommendation, it must then be instantiated as a
separate governed file under `build-sequence/02-design-tasks/`, using
`build-sequence/00-governance/01-task-template.md`, and reviewed for index/DAG
impact before execution.

## 3. Current Planning Context

The current implementation is a FastAPI/Pydantic/Uvicorn foundation with static
health/readiness endpoints, shared contracts, CI/security checks, and a
mock-injected Qdrant-shaped boundary. The ingestion, retrieval, generation,
query, and evaluation stages are not an end-to-end implementation.

The current independent review is recorded at:

```text
docs/reviews/architecture-and-delivery-readiness-review-2026-07-28.md
```

Its decision is `NO-GO` for the current final build sequence and for any
production-readiness claim. The earlier DT013 approval is reopened.

## 4. Recommended Next Design-Task Package

The repository already contains the following planned/reopened task files from
the external review. They are the recommended next package; no additional task
IDs should be invented until this package is resolved.

| Priority | Task | Recommendation | Why it must be next |
|---:|---|---|---|
| 1 | `RAG-DT021` Security, Trust, And Abuse-Resistance Contract | Execute first | Establishes deployment tiers, trust boundaries, source poisoning/indirect-injection controls, API abuse limits, provider boundaries, privacy, and logging rules. |
| 2 | `RAG-DT024` Corpus Promotion, Freshness, Revocation, And Rollback Contract | Execute after DT021 | The current registry has no canonical retrieval-eligible corpus; it also needs curator-annotation isolation, promotion authority, expiry, quarantine, revocation, and rollback. |
| 3 | `RAG-DT022` Evaluation Validity And Adversarial Test Contract | Execute after DT021/DT024 | Replaces small in-sample evidence with development/calibration/held-out splits, adjudication, claim-to-span attribution, adversarial cases, uncertainty, and absolute gates. |
| 4 | `RAG-DT023` Runtime Reliability, SLO, Capacity, And Deployment Contract | Execute after DT021 | Defines the PoC/shared/production envelope, dependency-aware readiness, deadlines, cancellation, concurrency, backpressure, quotas, SLOs, capacity, recovery, and operations ownership. |
| 5 | `RAG-DT015` Model Selection Revision | Reopen after DT022 | The previous Groq model is scheduled for shutdown; supported default/fallback models and credential-rotation evidence must be reevaluated. |
| 6 | `RAG-DT018` Retrieval/Fusion Revision | Reopen after DT022/DT024 | Fusion weights and confidence thresholds need independent calibration and held-out validation. |
| 7 | `RAG-DT019` Generation/API Contract Revision | Reopen after DT021/DT022/DT023 | Reconcile API/error schemas, claim-to-span citations, request/resource controls, provider lifecycle, and indirect-injection behavior. |
| 8 | `RAG-DT020` Evaluation/Tuning Loop Revision | Reopen after DT022/DT023 | Replace baseline-relative-only acceptance with absolute quality, safety, attribution, latency, error, and cost gates. |
| 9 | `RAG-DT025` Build-Task Executability And Source-of-Truth Reconciliation | Execute last in the package | Reconcile statuses and indexes, remove invalid commands/placeholders, validate explicit dependencies, add RACI/risk/exception controls, and prepare DT013 Revision 2. |
| 10 | `RAG-DT013` Final Build Task Impact Review, Revision 2 | Do not start until 1–9 are complete | Produces the actual `GO`/`NO-GO` decision for the implementation lane. |

Recommended decision order:

```text
G0 -> DT021
-> { DT024 -> DT022 -> [DT015 + DT018], DT023 }
-> DT019 -> DT020 -> DT025 -> DT013 Revision 2
```

The detailed lanes and closeout gates are defined in sections 8 and 9.

## 5. Proposed Remediation Strategy

The package will address the findings through gated design work, not by
starting runtime implementation in the current workspace. Every gate produces
an accepted design artifact and evidence that the next gate can safely consume.

There are three operating boundaries throughout the plan:

| Boundary | Permitted outcome | Prohibited outcome |
|---|---|---|
| Fixture-only local PoC | Isolated tests against explicitly named, non-authoritative fixtures | Public retrieval, regulatory/source-quality claims, or production-readiness language |
| Shared/internal service | Only after DT021, DT023, DT019, and the relevant build gates select and prove controls | Anonymous access, unrestricted provider spending, or static-success readiness |
| Production | Only after a separate approved production program | Treating candidate sources, local Docker, or PoC evidence as production proof |

The plan uses these rules:

- the source registry is authoritative for source lifecycle state;
- curator and policy annotations are never answerable source text;
- calibration data may tune a decision, but held-out data alone may confirm it;
- a model, retrieval configuration, corpus release, or API contract is not
  accepted until its exact versioned evidence is recorded;
- a deferred risk must have an accountable owner, allowed deployment tier,
  expiry date, exit condition, and failure mode.

## 6. Immediate Containment Gate: G0

G0 is a short containment action, not a new task ID. It must finish before any
live provider call, non-fixture indexing, or readiness claim.

| Finding | Immediate action | Accountable owner | Evidence | Remains blocked until |
|---|---|---|---|---|
| Superseded Groq model and exposed credential | Revoke/rotate the old key outside Git; record only rotation date, secret-store reference/version, invalidation attestation, and owner. Keep the adapter model-agnostic. | Credential owner and LLM owner | Redacted rotation record and current provider lifecycle check | DT015 selects a supported default and fallback through DT022 gates |
| Candidate sources are not canonical | Keep every current candidate, chunk, golden question, and benchmark result labeled fixture-only. | Corpus/data owner | Fixture namespace and provenance inventory | DT024 and BT024 establish an approved corpus release |
| Curator notes are being treated as evidence | Mark review/policy notes non-chunkable and exclude them from retrieval/generation inputs. | Knowledge-base curator | Annotation-isolation test plan and candidate inventory | DT024 dry run proves isolation |
| API/readiness are overstated | Do not use static `/ready` as dependency or container proof. Do not expose the planned API beyond the selected local tier. | Platform/API owner | Current-state note and tier decision | DT023 plus the later dependency-aware readiness build work |
| Build evidence is internally inconsistent | Freeze final-build authorization; retain historical evidence but treat DT013 as blocked. | Architecture/delivery owner | Current indexes and checklist identify DT013 Revision 2 | DT025 and DT013 Revision 2 |

G0 does not require committing a secret, creating a runtime dependency, or
changing a build task. It records only the safe evidence needed to establish
the next design boundary.

## 7. Workstream Plan And Required Outputs

### 7.1 Trust And Corpus Lane

| Step | How it addresses the issue | Required design outputs | Exit gate / evidence | Unlocks |
|---|---|---|---|---|
| DT021 security, trust, and abuse resistance | Defines trust boundaries for callers, source acquisition, registry, chunking, Qdrant, provider, logs, CI, and human reviewers. Covers direct/indirect injection, poisoning, API abuse, privacy, and incident response. | Threat model; deployment-tier matrix; adversarial corpus specification; source-trust policy; logging/redaction and provider-boundary rules. | Security/data/platform review agrees every threat has a preventive, detective, or recovery control and a verification method. | DT024, DT022, DT023, DT019 |
| DT024 corpus lifecycle | Separates immutable source snapshots, answerable source text, source metadata, and non-answerable curator/policy annotations. Defines promotion, expiry, quarantine, revocation, Qdrant deletion, and rollback. | Lifecycle state machine; release-manifest schema; promotion policy; annotation sidecar format; freshness/reverification policy. | A dry-run promotion, quarantine, revocation, deletion, and rollback plan is executable against fixtures; every current registry record remains explicitly classified. | DT022, DT018, DT019, BT024 |

The non-fixture authorization gate is stronger than DT024 design completion.
Before canonical retrieval or a production track, BT024 must execute one
reviewed immutable corpus release with upstream hashes, reuse approval,
annotation-exclusion proof, Qdrant deletion/revocation evidence, and rollback
evidence. Until then, `retrieval_eligible: true` in an example or fixture must
never override the source registry.

### 7.2 Evaluation, Retrieval, And Model Lane

| Step | How it addresses the issue | Required design outputs | Exit gate / evidence | Unlocks |
|---|---|---|---|---|
| DT022 evaluation validity | Replaces the small reused smoke fixture with a defensible, reproducible evaluation contract. | Versioned development/calibration/held-out dataset manifest; leakage-audit rules; adjudication rubric; statistical gates; adversarial-case inventory; scorer/run-manifest contract. | A small reproducibility demonstration records dataset hashes, source/version split, prompt/model parameters, raw outputs, scores, adjudication results, and report. No `TBD` threshold may remain for a claimed gate. | DT015, DT018, DT019, DT020, BT019 |
| DT015 model-selection revision | Replaces the retired default only after credential containment and valid evaluation inputs exist. | Fresh provider inventory; tier/deprecation check; supported default/fallback shortlist; cost/latency/reliability comparison. | Held-out evaluation proves the default and fallback pass quality, safe-refusal, structured-output, latency, error, cost, and lifecycle gates. | BT016, BT017, BT018, BT019 |
| DT018 retrieval/fusion revision | Replaces unvalidated fusion weights and rank-derived confidence. | Candidate comparison for semantic-only, lexical-only, rank fusion, and weighted fusion; calibration method; abstention/confidence design. | Tune only on calibration data; freeze the choice; report held-out retrieval, attribution, false-answer, false-abstention, and confidence-calibration results with uncertainty. | BT014, BT017, BT018, BT019 |

The existing 10-chunk / 14-case material remains a development smoke fixture.
It cannot be the sole basis for embedding, model, fusion, confidence, citation,
or production-quality selection. High-risk regulatory cases require human or
domain-SME adjudication; an LLM judge must be calibrated against that judgment
and may not be the sole judge of its own model family.

### 7.3 Platform, API, And Operations Lane

| Step | How it addresses the issue | Required design outputs | Exit gate / evidence | Unlocks |
|---|---|---|---|---|
| DT023 runtime reliability, SLO, capacity, and deployment | Treats local PoC, shared internal service, and production as separate operating tiers. Defines dependency behavior rather than relying on a static endpoint. | Environment matrix; liveness/readiness semantics; timeout/cancellation/retry/backpressure policy; numeric PoC budgets; capacity/failure/recovery matrix; observability and ownership model. | Selected tier has measurable latency/error/cost limits, non-billable provider readiness behavior, Qdrant lifecycle assumptions, and a defined rollback/recovery outcome. | DT019, DT020, BT023, BT020, BT021 |
| DT019 generation/API revision | Reconciles actual Pydantic/FastAPI schemas with the approved external contract and adds claim-to-source-span support. | Authoritative request/response/problem schema; versioning decision; error taxonomy; public/internal trace separation; citation and policy-notice rules; resource-limit contract. | Pydantic, JSON Schema, and OpenAPI parity checks are specified for 200, 422, 429, 502, 503, and 504 outcomes; no raw provider/error detail or secret can appear in a public response. | BT015, BT016, BT017, BT018, BT019 |
| DT020 evaluation/tuning revision | Prevents baseline-relative-only acceptance and untracked tuning. | Baseline-promotion policy; absolute metric thresholds; experiment/run manifest; change-control and rollback rules. | A release/model/retrieval configuration can be promoted only after it passes frozen held-out quality, attribution, safety, latency, error, and cost gates. | BT019, BT022 |

DT023 must define the canonical application configuration matrix before code is
written. It must reconcile task and Docker references with the Pydantic setting
names, including `RAG_QDRANT_*` versus bare `QDRANT_*` guidance and
`RAG_ENVIRONMENT` versus `RAG_ENV` guidance. DT019 must then use that matrix in
the API/provider contract.

## 8. Parallel Design DAG

The earlier list was intentionally conservative. The actual design work can
use two independent lanes after G0, while preserving the evidence dependencies:

```text
G0 containment
  -> DT021 security/trust
       -> DT024 corpus lifecycle -> DT022 evaluation validity
            -> DT015 supported-model decision
            -> DT018 retrieval calibration
       -> DT023 reliability/platform contract

DT015 + DT018 + DT023 + DT021/DT024
  -> DT019 API/generation revision
  -> DT020 evaluation/tuning revision
  -> DT025 delivery/governance reconciliation
  -> DT013 Revision 2 GO or NO-GO
```

DT015 and DT018 may run in parallel after DT022 accepts the evaluation
contract. DT023 may run in parallel with DT024/DT022 after DT021 defines the
permitted deployment tier. DT019 may not close until all its upstream decisions
are accepted.

## 9. Evidence Gates And Authorization Matrix

| Gate | Required proof | Authorized after passing | Still prohibited |
|---|---|---|---|
| G0 containment | Credential rotation evidence, stale default prohibited, fixture labels, registry/example mismatch identified | Design work only | Live provider calls and non-fixture claims |
| G1 trust/corpus | DT021/DT024 contracts; annotation isolation; promotion/revocation/rollback dry-run evidence | Evaluation design against fixtures | Canonical retrieval and external source claims |
| G2 evaluation foundation | Leakage audit, source-level splits, executable loader/scorer contract, adjudication log, reproducibility run, absolute gates | Model/retrieval decision revisions | Tuning on or promoting held-out results |
| G3 selection | Fresh provider/deprecation evidence; supported default/fallback; frozen retrieval configuration; untouched held-out results | Configurable, mocked adapter and retrieval implementation planning | Live default model, calibrated-confidence claim, or production-quality claim without build evidence |
| G4 runtime/API | Tier matrix, claim-to-span schema, injection outcomes, numeric abuse/cost limits, dependency/readiness design, failure behavior | BT023 and subsequent implementation after DT013 GO | Shared/public API exposure and static-readiness proof |
| G5 delivery | Explicit DAG, task-specific red checks, RACI, risk/exception register, status reconciliation, governance negative tests | DT013 Revision 2 review | Any task whose dependency, test command, owner, or evidence remains ambiguous |
| G6 final authorization | DT013 `GO`; no blocking exception; authorized task list and deployment tier named | Only the explicitly named fixture or non-fixture build tasks | Any unlisted task, shared deployment, or production claim |

## 10. Ownership And Approval Model

| Work | Responsible | Accountable approver | Required consultation |
|---|---|---|---|
| DT021 | Security/RAG engineer | AI/security owner | Platform, corpus/data, service owner |
| DT024 | Knowledge-base curator | Corpus/data-governance owner | Domain SME and legal/reuse approver |
| DT022 | Evaluation/QA lead | Service owner | Independent domain adjudicator and RAG lead |
| DT023 | Platform/SRE engineer | Platform/operations owner | Security, service, and cost owner |
| DT015 and DT018 | ML/RAG lead | Evaluation owner | Service owner and platform owner |
| DT019 | API/service owner | Service owner | Security and client/BFF owner |
| DT020 | Evaluation lead | Product/domain-risk owner | RAG, platform, and service owner |
| DT025 | Delivery/governance owner | Architecture owner | Security, data, evaluation, platform, and documentation reviewers |
| DT013 Revision 2 | Architecture owner | Service owner | Independent security, data, evaluation, platform, and delivery sign-off |

No risk is accepted merely because a task is marked complete. The exception
record must identify the owner, approver, permitted deployment tier, expiry,
exit criterion, and escalation trigger.

## 11. Implementation Handoff After DT013 Revision 2

If DT013 returns `GO`, implementation starts from the explicitly authorized
subset of the build DAG, with one branch/worktree per task and no direct work
on `main`.

| Build boundary | Required first work | Required proof before the next boundary |
|---|---|---|
| Fixture mechanics | BT007 registry validation, BT008 audit reporting, BT009 chunking, BT011 embedding adapter | Fixture data is clearly non-authoritative and carries source/annotation provenance |
| Real vector integration | BT023 before BT012 | Locked `qdrant-client`; lifespan-managed async adapter; collection validation; real upsert/search/filter/delete; cleanup; required CI service-container job |
| Fixture ingestion/retrieval | BT012, then retrieval tasks | Dedicated test namespace; no accidental promotion of candidates; held-out evaluation rules consumed |
| Generation/API | BT016-BT018 after supported model and contract decisions | Credential-safe mocked tests, public-safe errors, resource limits, claim-to-span citations, provider failure behavior |
| Local operations | BT020-BT022 only after dependency readiness exists | Loopback-bound Qdrant, immutable images, no secrets in image layers, container scan/SBOM, explicit PoC-only verdict |
| Canonical/production path | BT024 and a separately approved production program | Approved corpus release, restore/rollback proof, selected deployment controls, capacity/SLO/on-call evidence |

## 12. Tasks That Should Not Be Added Yet

Do not add more design-task IDs for concerns already covered by the package:

- model lifecycle/fallback: covered by reopened DT015;
- claim attribution and evaluation validity: covered by DT022 and DT019;
- corpus authority and rollback: covered by DT024;
- runtime limits, readiness, SLOs, and recovery: covered by DT023;
- task DAG, RACI, status drift, and executable checks: covered by DT025.

Adding parallel tasks now would increase dependency ambiguity and create
duplicate sources of truth.

## 13. Conditional Follow-On Design Tasks

Only add these after DT021–DT025 and DT013 Revision 2 expose a concrete gap:

| Conditional task | Add only if | Expected owner/output |
|---|---|---|
| Deployment-target and production recovery design | A real shared/staging/production target is selected | Platform/operations; topology, IAM/TLS, backup/restore, RPO/RTO, rollback, on-call and incident contract. |
| Provider data-handling and residency design | The chosen provider may receive regulated, confidential, or customer-derived content | Security/legal/data owner; classification, retention, residency/DPA, redaction, and permitted-data matrix. |
| Corpus refresh automation design | Canonical corpus refresh is required beyond a manually released baseline | Corpus owner; source polling, change detection, approval, expiry, rollback, and audit workflow. |
| Attribution/reranking design | Held-out evaluation shows retrieval rank or claim support remains inadequate after DT018/DT022 | RAG/evaluation owner; reranker choice, claim-support model, or human-review boundary. |

These are conditional proposals, not current task additions.

## 14. Acceptance Gate For Turning This Proposal Into Tasks

Before any recommendation becomes a governed task file, the owner should
confirm:

1. the task is not already covered by an existing DT021–DT025 or reopened
   decision;
2. the intended authority is clear (`docs/design/` output versus
   `build-sequence/` task file);
3. the task has one owner, accountable approver, dependencies, blockers,
   acceptance criteria, red check, verification matrix, and evidence path;
4. the task does not require editing runtime code or environment files before
   its design decision is accepted;
5. the task index, build DAG, and architecture checklist can be updated
   together without leaving contradictory statuses.

## 15. Recommendation

Approve the location and the existing ten-step package as the next planning
boundary. Do not create another task file or start final build work from this
proposal alone. First execute the already planned security, corpus, evaluation,
reliability, and delivery-control gates; then rerun DT013 Revision 2.
