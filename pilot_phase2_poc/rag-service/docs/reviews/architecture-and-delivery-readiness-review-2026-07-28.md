# RAG Service Architecture And Delivery Readiness Review

Status: Final independent review
Date: 2026-07-28
Scope: `pilot_phase2_poc/rag-service`
Decision: **NO-GO for the published final build sequence and for any
production-readiness claim**

## Executive Decision

The target direction is viable for a local proof of concept:

```text
FastAPI
-> deterministic query planning
-> semantic/lexical hybrid retrieval
-> Qdrant
-> Groq/OpenAI-compatible generation
-> schema and citation validation
```

The repository is not an implemented RAG service yet. It is a well-documented
scaffold: Python/FastAPI setup, static health/readiness endpoints, settings,
shared schemas, CI/security checks, and a mock-injected Qdrant-shaped boundary.
Most ingestion, query, retrieval, generation, and evaluation modules are empty.
The 12 passing tests prove the foundation, not end-to-end RAG behavior.

The current plan is also not executable as published. Serious model-lifecycle,
corpus, evaluation-validity, Qdrant, dependency-DAG, security, reliability,
readiness, and governance gaps invalidate the earlier final-impact approval.

The allowable boundary is:

- **Conditional later GO:** local, fixture-only PoC mechanics after the new and
  reopened design gates complete and `RAG-DT013` Revision 2 returns `GO`.
- **NO-GO now:** every final build task, because `RAG-DT013` is reopened.
- **NO-GO:** shared/staging deployment.
- **NO-GO:** production. A separate production program does not yet exist.

## Independent Review Team

The review team was selected only after researching current architecture-review
practice. AWS Well-Architected recommends the right people, independent review
at lifecycle milestones, and expertise across operational excellence,
security, reliability, performance, cost, and sustainability. NIST AI RMF adds
AI governance, measurement, testing, and risk-management concerns.

Three outside-perspective specialists reviewed the repository independently:

1. **RAG/IR, AI evaluation, corpus, and data-governance specialist**
   - retrieval and fusion validity;
   - embeddings/model evidence;
   - golden-set leakage and scoring;
   - source/corpus authority;
   - citation support and RAG attack cases.
2. **FastAPI/Qdrant, platform, security, SRE, and operations specialist**
   - actual runtime maturity;
   - SDK/service integration;
   - API/runtime trust and abuse controls;
   - readiness, timeouts, concurrency, capacity, recovery, CI, and Docker.
3. **Delivery sequencing, QA governance, evidence, and change-control
   specialist**
   - dependency DAG;
   - task executability;
   - status/source-of-truth consistency;
   - RACI/risk/deferral control;
   - release and production terminology.

This division deliberately separates component expertise from delivery control
and gives each reviewer permission to distrust already “accepted” labels.

Authoritative team-formation basis:

- AWS Well-Architected review process:
  https://docs.aws.amazon.com/wellarchitected/latest/framework/the-review-process.html
- AWS workload scope:
  https://docs.aws.amazon.com/wellarchitected/latest/userguide/workload-and-scope.html
- AWS people and culture:
  https://docs.aws.amazon.com/wellarchitected/latest/userguide/people-and-culture.html
- NIST Generative AI Profile:
  https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

## Actual And Planned Stack

| Area | Current repository | Planned target | Maturity |
|---|---|---|---|
| Runtime | Python 3.12, `uv`, FastAPI, Uvicorn, Pydantic/settings | Same | Foundation implemented |
| API | `/health`, static-success `/ready` | `/api/v1/query`, versioned request/response/errors | Scaffold / contract only |
| Vector DB | Injected mock-compatible protocol | Qdrant SDK, collections, payload indexes, service integration | Missing |
| Embeddings | Design experiment | FastEmbed `BAAI/bge-small-en`, 384 dimensions, cosine | Unimplemented; evidence conditional |
| Retrieval | Design contract | semantic, lexical/BM25-style, hybrid fusion | Unimplemented; fusion reopened |
| Generation | Historical Groq selection | OpenAI-compatible async provider adapter | Unimplemented; model selection reopened |
| Evaluation | Small design-time smoke fixture | offline, Qdrant/API, adversarial, live-provider evaluation | Unimplemented; validity gate missing |
| Local runtime | Docker design | app + Qdrant Compose | Unimplemented |
| Quality/security | pytest, Ruff lint, Bandit, pip-audit, CodeQL, Dependabot | Expanded integration/container/governance gates | Foundation implemented |

## Blocking Findings

### CRITICAL-1: Selected generation model is approaching shutdown

`docs/design/llm-model-selection-decision.md` selected
`llama-3.3-70b-versatile`. Groq now says free/developer-tier access shuts down
on 2026-08-16 and recommends `openai/gpt-oss-120b` or
`qwen/qwen3.6-27b`.

The selected default therefore cannot safely drive `RAG-BT016`.

The same evidence records that a Groq credential was pasted into chat and
should be rotated. No current repository evidence proves revocation/rotation.
No further live provider call should occur until that is verified.

Action taken:

- reopened `RAG-DT015`;
- superseded the old default decision;
- blocked BT016+ on credential-rotation proof, current model inventory,
  independent evaluation, supported default selection, and fallback/lifecycle
  checks.

Official provider evidence:

- https://console.groq.com/docs/deprecations
- https://console.groq.com/docs/production-readiness/security-onboarding

### CRITICAL-2: No runtime-eligible or canonical corpus exists

The candidate registry contains no retrieval-eligible source, and no canonical
corpus release exists. Examples/fixtures cannot override registry authority.
A fixture-only system may be built, but it cannot claim canonical provenance or
production readiness.

The current golden evidence also includes a curator “Review Notes” section as
expected answer content. Internal curator analysis must not be embedded and
served as regulatory/source-grounded evidence.

Action taken:

- added `RAG-DT024` for promotion, freshness, annotation isolation,
  quarantine, revocation, deletion, versioning, and rollback;
- added `RAG-BT024` for an owner-approved immutable canonical corpus release;
- made the canonical task conditional for fixture-only mechanics but mandatory
  for canonical retrieval and any future production program.

OWASP identifies vector/embedding systems as exposed to unauthorized access,
cross-context leakage, embedding inversion, poisoning, and relevance
manipulation:

- https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/

### CRITICAL-3: Evaluation evidence cannot support the accepted decisions

DT010/DT015 reuse a tiny in-sample fixture: 10 chunks, 8 positive queries, 14
total cases, and a few short candidate documents. The same material informs
embedding, model, retrieval, and later regression decisions. There is no
source-level holdout.

The committed DT015 result set has one response per model/case but no committed
evaluator implementation that independently reproduces all heuristic scores.
Several negative outputs and their perfect refusal/safety scores are internally
questionable. This is useful smoke evidence, not model-selection or
production-quality proof.

Action taken:

- added `RAG-DT022`;
- required development, calibration, and held-out source-level splits;
- required human-adjudication and judge-calibration rules;
- required repeated runs, uncertainty, sample sizes, reproducibility, and
  absolute gates;
- required paraphrase, near-negative, mixed-intent, multilingual, stale,
  conflicting, poisoned, indirect-injection, and malformed-output cases;
- reopened DT015, DT018, DT019, and DT020.

NIST’s Generative AI Profile treats testing, measurement, independent
evaluation, incident handling, and third-party risk as governance concerns:

- https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

### HIGH-1: Hybrid fusion and confidence thresholds are uncalibrated

DT018 fixed semantic/lexical weights and low-confidence thresholds without an
independent hybrid benchmark. Per-query min-max normalization can promote each
retriever’s best candidate even when all evidence is weak, so the fused score
cannot by itself be treated as calibrated evidence confidence.

Action taken:

- reopened `RAG-DT018`;
- required comparison of semantic-only, lexical-only, RRF/DBSF, and weighted
  fusion on calibration data;
- required the frozen strategy to be measured on held-out data;
- prohibited normalized fused rank alone from acting as the confidence gate.

Qdrant’s hybrid-search guidance describes multiple fusion strategies and the
need to tune/evaluate rather than assume one weighting:

- https://qdrant.tech/documentation/search/hybrid-queries/

### HIGH-2: The build DAG omitted the real Qdrant boundary

`RAG-BT012` requires service-backed Qdrant, but the current BT010 output is only
a mock-injected wrapper. There is no `qdrant-client` runtime dependency,
SDK-native point/filter conversion, collection lifecycle, payload-index
management, async client lifespan, real integration job, or Qdrant test
service.

The original sequence also expected BT012 to parse, chunk, embed, and index
without explicit dependencies on BT007 and BT009. It placed the only Compose
task after evaluation.

Action taken:

- added `RAG-BT023` before BT012;
- required a locked SDK, lifespan-managed `AsyncQdrantClient`, deterministic
  Qdrant-compatible IDs, create-or-validate collection behavior, schema
  migration failure, real upsert/search/filter/delete tests, cleanup, and CI;
- added BT007, BT009, BT011, and BT023 as explicit BT012 dependencies;
- added BT023 to later integration gates.

Qdrant references:

- points: https://qdrant.tech/documentation/manage-data/points/
- collections: https://qdrant.tech/documentation/manage-data/collections/
- async API: https://qdrant.tech/documentation/tutorials-develop/async-api/
- capacity planning: https://qdrant.tech/documentation/operations/capacity-planning/

### HIGH-3: Security covers a direct prompt, not the RAG trust boundary

The design says retrieved chunks are untrusted but relies mainly on prompt
instruction and a small literal malicious-phrase set. It does not close
indirect injection in retrieved content, obfuscation, multilingual/split
payloads, poisoned sources, citation spoofing, unsafe markup/URLs, or source
quarantine.

The API design also lacks a deployment-tier decision for authentication,
authorization, request/token/filter limits, rate limits, concurrent-request
limits, cost ceilings, total deadlines, debug exposure, outbound allowlists,
privacy/retention, and provider-data handling.

Action taken:

- added `RAG-DT021` as a blocking security/trust/abuse contract;
- required deployment profiles, a threat model, adversarial corpus, source
  provenance/quarantine, indirect-injection tests, API/resource controls,
  outbound-provider policy, logging/privacy, and incident evidence;
- required curator annotations to remain outside the answerable corpus.

Authoritative references:

- OWASP prompt injection:
  https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- OWASP API unrestricted resource consumption:
  https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/
- NIST adversarial machine learning taxonomy:
  https://www.nist.gov/news-events/news/2024/01/nist-identifies-types-cyberattacks-manipulate-behavior-ai-systems

### HIGH-4: Readiness, reliability, deployment, and recovery are undefined

`/ready` always returns HTTP 200. The planned Docker task uses it as a
meaningful container probe, but it cannot detect invalid configuration,
missing collection/schema, or unavailable Qdrant.

No current contract defines:

- sync/async boundaries, connection pooling, cancellation, backpressure,
  retries/jitter, circuits, or idempotency;
- p50/p95/p99 latency, error, availability, provider quota, token, or cost
  budgets;
- workload/capacity/load/soak tests;
- Qdrant backup/restore, RPO/RTO, replication, scaling, and schema migration;
- deployment environments, rollback, alerting, incident, on-call, or support
  ownership.

Action taken:

- added `RAG-DT023`;
- required deployment tiers and an environment matrix;
- required dependency-aware readiness, bounded failure behavior, SLO/PoC
  budgets, capacity/load/cost evidence, backup/restore/rollback policy, and
  operations ownership;
- prevented any production-ready verdict until production-tier evidence exists.

Qdrant operations references:

- backups: https://qdrant.tech/documentation/cloud/backups/
- snapshots: https://qdrant.tech/documentation/tutorials-operations/create-snapshot/
- migration/recovery:
  https://qdrant.tech/documentation/migration-recovery-options/
- scaling: https://qdrant.tech/documentation/scaling/

### HIGH-5: “Production readiness” was an invalid label and an invalid task

BT022 called itself production readiness while explicitly excluding a
deployment target, managed/persistent Qdrant, backups, TLS, production auth,
canonical corpus, and production alerting.

Its red-check instructions wrote Python code into a Markdown file and invoked
pytest on that Markdown file. That is not an executable test.

Action taken:

- reframed BT022 as **PoC Integration Readiness Review** while retaining the
  task ID/path for traceability;
- replaced the Markdown/pytest workflow with artifact-contract and service/
  governance checks;
- required a `POC_GO` or `POC_NO_GO` verdict and an explicit statement that the
  result is not a production-readiness decision;
- made real Qdrant and dependency-aware readiness mandatory.

### HIGH-6: The canonical status and delivery evidence contradicted itself

Before this review:

- the design index marked every DT complete;
- the architecture “source of truth” marked many of the same decisions pending;
- the final impact review claimed no design blocker;
- some design artifacts remained Draft/Pending/Accepted-for-review;
- GOV002 evidence remained Ready for Merge on current `main`;
- the governance script did not detect the contradictions;
- all planned build tasks were generic structured shells, not task-specific
  executable plans.

Action taken:

- reopened `RAG-DT013` as Revision 2;
- updated current indexes and the architecture checklist;
- corrected several obvious artifact statuses while preserving historical
  evidence;
- added `RAG-DT025` to reconcile the full status/dependency matrix, rewrite
  task-specific red checks, add RACI/risk/exception ownership, and extend
  governance with negative tests;
- prohibited `GO_WITH_CONDITIONS` from carrying unowned blocking prose.

### MEDIUM-HIGH: API/error/citation contracts need reconciliation

The implemented shared schemas and the later DT019 contract differ in version
and error-field names. There is no unified FastAPI exception/validation
handler. Citation identity proves which chunk was named, not that individual
answer claims are supported.

Required under reopened DT019 and DT025:

- reconcile `api_version` versus `schema_version`;
- reconcile `error_code` versus `code` and add stage/request correlation;
- add authoritative Pydantic/JSON-schema/OpenAPI contract tests;
- map answer claim IDs to supporting chunk/span references;
- measure citation/attribution precision and recall;
- reject unsupported claims explicitly.

## Adjusted Gate And Build Sequence

```text
completed setup scaffold
-> DT021 security/trust
-> DT024 corpus lifecycle
-> DT022 evaluation validity
-> DT023 reliability/deployment
-> DT015 model-selection revision
-> DT018 retrieval-calibration revision
-> DT019 generation/API revision
-> DT020 evaluation/tuning revision
-> DT025 task/DAG/source-of-truth reconciliation
-> DT013 Revision 2 GO or NO-GO
-> BT007 registry validation
-> BT009 chunking mechanics
-> BT011 embedding adapter
-> BT023 real Qdrant adapter/test infrastructure
-> BT012 fixture ingestion
-> retrieval/query/generation/evaluation
-> BT022 PoC integration-readiness review
```

`RAG-BT024` is a separate canonical-corpus track and is mandatory before
canonical retrieval, canonical evaluation, or a future production program.

## Required Production Program

Do not rename the PoC gate back to production readiness. If production becomes
the target, create a separately approved program after DT023 selects the
deployment environment. It must include at least:

- canonical corpus approval and release;
- deployment topology, IAM/auth, TLS, secrets, and network boundaries;
- persistent Qdrant, backup/restore, restore drill, RPO/RTO, and migrations;
- load/capacity/p95/p99/error/token/cost proof;
- numeric SLOs, dashboards, alerts, on-call, incident, rollback, and support;
- privacy, retention, residency/DPA, and data classification;
- hardened repository/container/supply-chain evidence;
- staged go-live and rollback rehearsal.

## Verification Snapshot

Observed on 2026-07-28 before/while applying this review:

- `uv run pytest -q`: 12 passed.
- `uv run python scripts/check_build_sequence_governance.py`: passed before
  the review, demonstrating that the old checker missed the defects above.
- `uv run pip-audit`: no known vulnerabilities in the audited environment.
- Docker CLI 28.5.1 and Compose 2.40.3 are installed.
- Docker Desktop Linux daemon is not running, so real Qdrant integration cannot
  currently be executed locally.
- The initial `uv run ruff format --check .` found a cross-platform formatting
  drift in `app/shared/tests/test_error_schema.py`; the file was normalized and
  the format check was rerun.
- The user-owned untracked
  `build-sequence/01-setup-tasks/rag-service.code-workspace` was preserved.

Post-adjustment verification:

- `uv run python scripts/check_build_sequence_governance.py`: passed.
- `uv run python -m pytest -q`: 12 passed.
- `uv run ruff format --check .`: 45 files already formatted.
- `uv run ruff check .`: passed.
- the CI-equivalent Bandit command: no issues identified.
- `uv run pip-audit`: no known vulnerabilities found; pip-audit emitted its
  existing virtual-environment context warning.
- `git diff --check`: passed (Git emitted only Windows line-ending notices).

## Final Readiness Verdict

**NO-GO now.**

The design is not rejected wholesale. Its core PoC direction is reasonable,
and much of the historical design work is valuable. The approval state,
evidence strength, missing runtime boundaries, and delivery sequence were too
optimistic. The repository is now explicitly gated on the work needed to make
the plan honest, executable, independently evaluable, and safely scoped.
