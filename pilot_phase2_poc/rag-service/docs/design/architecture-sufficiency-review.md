# RAG-DT017 Architecture Sufficiency Review

Status: Accepted for RAG-DT017
Run: `dt017-run-001`
Date: 2026-07-18

## Purpose

This review checks whether the RAG service design surface is sufficient before
`RAG-DT013` performs the final build-task impact review.

The review covered:

- completed design task files under `build-sequence/02-design-tasks/`;
- final build task files under `build-sequence/03-build-tasks/`;
- design artifacts under `docs/design/` and `docs/evaluation/`;
- design evidence under `build-evidence/RAG-DT*.md`;
- current service code under `app/`;
- current Python packaging, tests, and CI/CD posture;
- knowledge-base registry, candidate, and snapshot artifacts;
- GitHub repository settings visible through the GitHub API.

## Review Inputs

Baseline inventory:

| Input | Count / Result |
|---|---:|
| Design task files | 17 |
| Design artifact files | 39 |
| Design evidence files | 15 |
| Local unit tests | 12 passed |
| Root RAG Service CI | present and passing |
| Root RAG Service CodeQL | present and passing |

Specialist review perspectives were recorded in:

```text
docs/design/experiments/architecture-review/dt017-run-001/expert-review-findings.md
```

## Sufficient Areas

The review found the project has enough architecture foundation in these areas:

- FastAPI service baseline: `app.main:app`, `/health`, `/ready`, and stage
  package scaffolds are present and tested.
- Python test and packaging baseline: Python 3.12, `uv`, pytest
  `pythonpath`, `integration` marker, Ruff, Bandit, and pip-audit are wired
  into local and CI checks.
- Source and KB governance: legacy material is audit-only; Phase 2 ingestion
  must use `knowledge_base/`; registry/schema boundaries prevent review,
  candidate, cite-only, or do-not-ingest sources from becoming runtime
  retrieval content accidentally.
- Chunking: `hybrid_structure_recursive_v1` is selected and has deterministic
  lineage-rich fixture output.
- Embeddings: `BAAI/bge-small-en` is selected as the first-pass FastEmbed model
  with 384-dimensional cosine vectors.
- Vector DB testing: the accepted three-layer strategy separates unit/mock,
  local Docker Qdrant, and GitHub Actions Qdrant service-container testing.
- Query planning: deterministic classifications and safe pre-retrieval
  behavior are defined for in-scope, unsupported, irrelevant, malicious,
  license-sensitive, and ambiguous queries.
- LLM model selection: Groq `llama-3.3-70b-versatile` is selected as a
  configurable first-pass generation model, not a permanent production lock.
- CI/CD: dedicated root workflows for RAG service CI and CodeQL are present and
  passed on PR and `main`.
- Ops design: Docker/Compose, logs, production-readiness, and accepted
  deferrals are assigned to later ops-readiness build tasks.

## Required Follow-Up Design Tasks

The review requires three follow-up design tasks before `RAG-DT013`, unless the
owner explicitly waives them:

1. `RAG-DT018`: Retrieval Strategy Selection, Scoring, And Fusion Contract
2. `RAG-DT019`: Generation Prompt, Safeguards, Output Schema, And Query API
   Contract
3. `RAG-DT020`: Post-Build Evaluation And Tuning Loop

These are required because the current build tasks describe the intended
behavior, but still need accepted implementation contracts for retrieval-mode
selection, hybrid scoring/fusion, external query/generation response shape,
safeguard behavior, and post-build evaluation/tuning decisions.

The proposed tasks are defined in:

```text
docs/design/experiments/architecture-review/dt017-run-001/recommended-follow-up-design-tasks.md
```

The follow-up task files already exist in the current build sequence after PR
#44 and PR #45. DT017 therefore treats them as created but not yet completed;
`RAG-DT013` remains blocked until `RAG-DT018`, `RAG-DT019`, and `RAG-DT020` are
completed or explicitly waived.

## High Risks Requiring Owner Decision Or Remediation

The review also found high-risk non-design items that should be resolved or
explicitly accepted before `RAG-DT013`:

- GitHub repository enforcement is not active: secret scanning and Dependabot
  security updates are disabled, branch protection is not enabled for `main`,
  and no rulesets were returned by the GitHub API.
- The test stack currently uses `httpx2`/`httpcore2`. Local package metadata
  identifies them as `https://github.com/pydantic/httpx2`, local tests pass,
  and `pip-audit` reports no known vulnerabilities, but the dependency choice
  is not yet recorded as an accepted project decision.

## Medium Build-Task Updates For RAG-DT013

`RAG-DT013` should update final build tasks to carry these details:

- normalize environment-variable naming across runtime and test docs
  (`RAG_QDRANT_*` vs bare `QDRANT_*`, `LLM_*` vs `RAG_LLM_*`);
- pin `/api/v1/query` method, request/response schema, `response_model`, error
  envelope, and FastAPI dependency override pattern;
- broaden Bandit/test exclusion guidance for future `app/stages/**/tests`;
- require normalized-text SHA semantics for markdown candidate hash checks;
- state that first-pass candidate chunks are review fixtures, not a production
  canonical retrieval corpus;
- preserve raw upstream snapshot automation and canonical promotion as deferred
  production/data-governance work unless the owner expands scope.

## Decision

Decision gate:

```text
Pass With Required Follow-Up Tasks
```

`RAG-DT013` should remain blocked until:

- the owner completes the three required follow-up design tasks, or explicitly
  waives them;
- the owner remediates or explicitly accepts the high-risk repository
  enforcement and dependency-provenance items;
- the final build-task impact review records the medium handoffs above.

