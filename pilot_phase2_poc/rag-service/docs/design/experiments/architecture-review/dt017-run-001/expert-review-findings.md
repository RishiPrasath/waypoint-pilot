# DT017 Expert Review Findings

Status: In Review
Run: `dt017-run-001`
Date: 2026-07-18

## 1. FastAPI/API Architecture Reviewer

Reviewed:

- `app/main.py`, `app/api/`, current endpoint tests, shared schemas, and stage
  package scaffolds;
- setup/build tasks that affect API behavior, especially `RAG-BT001`,
  `RAG-BT002`, `RAG-BT003`, `RAG-BT006`, and `RAG-BT018`.

Sufficient:

- FastAPI imports cleanly and exposes `/health` and `/ready`.
- Stage packages use Python-safe names and leave real RAG behavior to later
  tasks.
- `RAG-BT018` is correctly sequenced after query planning, retrieval,
  generation, and output validation.

Risks or missing items:

- The external query route contract is not pinned tightly enough for downstream
  consumers.

New design task needed:

- Yes, as part of `RAG-DT019`.

Affected tasks:

- `RAG-BT015`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, `RAG-BT019`.

Severity:

- High for API consumer contract precision; otherwise None.

## 2. Python Packaging And Unit-Testing Reviewer

Reviewed:

- `pyproject.toml`, `uv.lock`, local pytest behavior, Ruff/Bandit/pip-audit,
  and root RAG service CI.

Sufficient:

- Python 3.12, `uv`, pytest `pythonpath`, `integration` marker, and root CI are
  usable.
- Local baseline passed with 12 tests.

Risks or missing items:

- Runtime/test environment variable names are split between `RAG_*` runtime
  settings and bare integration-test names in design docs.
- Future `app/stages/**/tests` may trigger Bandit `assert_used` unless the
  exclusion strategy is broadened.
- `httpx2`/`httpcore2` are unusual dependencies and require an explicit
  project decision or replacement.

New design task needed:

- No separate Python task required if `RAG-DT013` normalizes the build-task
  handoffs and the owner accepts or remediates `httpx2` provenance.

Affected tasks:

- `RAG-BT004`, `RAG-BT010`, `RAG-BT011`, `RAG-BT012`, `RAG-BT013`,
  `RAG-BT014`, `RAG-BT016`, `RAG-BT018`, `RAG-BT019`, `RAG-BT020`.

Severity:

- Medium for env/test configuration; High for dependency provenance until
  accepted or remediated.

## 3. Qdrant/Vector Database Reviewer

Reviewed:

- `app/shared/vector_db`, `RAG-DT014`, `RAG-DT016`, `RAG-BT010`,
  `RAG-BT012`, `RAG-BT013`, `RAG-BT014`, `RAG-BT019`, and `RAG-BT020`.

Sufficient:

- The three-layer testing strategy is clear: fast unit/mock checks, local
  Docker Qdrant parity, and future GitHub Actions service-container
  integration.
- Qdrant payload, cleanup, collection prefix, readiness, and integration marker
  guidance are defined.

Risks or missing items:

- Current vector DB wrapper is intentionally a mocked boundary; no service
  integration should be claimed before `RAG-BT012`/`RAG-BT013`.

New design task needed:

- No.

Affected tasks:

- `RAG-BT010`, `RAG-BT012`, `RAG-BT013`, `RAG-BT014`, `RAG-BT019`,
  `RAG-BT020`.

Severity:

- Low.

## 4. Ingestion, Source Registry, And KB Materialization Reviewer

Reviewed:

- `knowledge_base/`, source registry/schema, snapshot manifest, candidates,
  source design artifacts, DT002/DT003/DT004/DT008/DT012 evidence, and
  ingestion build tasks.

Sufficient:

- Legacy KB material is audit-only.
- The Phase 2 registry/schema boundary is strong.
- First-pass materialization is representative enough for fixture/chunking
  work.
- Current ingestion code is scaffold only and does not bypass the KB gates.

Risks or missing items:

- Markdown candidate hashes should use normalized-text SHA semantics because
  Windows checkout line endings can differ from canonical LF text.
- No canonical runtime retrieval corpus exists yet; current first-pass
  candidates are review fixtures.
- Raw upstream snapshot automation remains deferred.

New design task needed:

- No pre-`RAG-DT013` task required unless the owner wants production canonical
  corpus promotion before fixture-based build validation.

Affected tasks:

- `RAG-BT007`, `RAG-BT008`, `RAG-BT009`, `RAG-BT012`, `RAG-BT013`,
  `RAG-BT014`, `RAG-BT019`, `RAG-BT022`.

Severity:

- Medium.

## 5. Chunking, Retrieval, And Evaluation Reviewer

Reviewed:

- DT005 chunking artifacts, DT006 golden questions, DT010 embedding benchmark,
  retrieval build tasks, and evaluation handoffs.

Sufficient:

- `hybrid_structure_recursive_v1` is selected and preserves lineage.
- `BAAI/bge-small-en` is selected as the first-pass semantic embedding model.
- Golden questions provide positive, negative, malicious, and boundary cases.
- The first evaluation fixture is adequate for a first build baseline.

Risks or missing items:

- Hybrid retrieval lacks a concrete scoring/fusion contract: BM25/tokenization
  choice, score normalization, fusion rule, candidate-pool sizes, metadata
  boost/filter behavior, and rerank interface are not yet pinned.
- The first evaluation set is intentionally small and should not be treated as
  broad production quality proof.

New design task needed:

- Yes: `RAG-DT018`.

Affected tasks:

- `RAG-BT013`, `RAG-BT014`, `RAG-BT018`, `RAG-BT019`.

Severity:

- High for hybrid fusion contract; Medium for evaluation breadth.

## 6. LLM/Generation And Prompt-Safety Reviewer

Reviewed:

- `RAG-DT007`, `RAG-DT009`, `RAG-DT015`, LLM evaluation artifacts,
  `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, and `RAG-BT019`.

Sufficient:

- Query planner safety classifications are strong and should block malicious,
  license-sensitive, irrelevant, and unsupported operational requests before
  retrieval/generation.
- Groq `llama-3.3-70b-versatile` is a reasonable configurable first-pass model
  selection based on DT015 results.

Risks or missing items:

- There is no explicit production prompt/message contract covering role
  structure, retrieved-context formatting, chunk-as-untrusted-data handling,
  citation instruction, refusal wording, output JSON contract, and context
  budget.
- DT015 scoring is design-time/heuristic and must be made repeatable in
  `RAG-BT019`.

New design task needed:

- Yes: `RAG-DT019`.

Affected tasks:

- `RAG-BT016`, `RAG-BT017`, `RAG-BT018`, `RAG-BT019`.

Severity:

- High for prompt/output contract; Medium for repeatable evaluation.

## 7. CI/CD And Local Ops Reviewer

Reviewed:

- root `.github/workflows`, root Dependabot config, DT011, DT014, DT016,
  `RAG-BT020`, `RAG-BT021`, `RAG-BT022`, and live GitHub check status.

Sufficient:

- Root RAG Service CI and CodeQL workflows exist and passed on `main`.
- CI covers frozen dependency sync, pytest, Ruff format/check, Bandit, and
  pip-audit.
- Docker image build, Compose runtime, Trivy/container scan, and service-backed
  Qdrant integration are correctly deferred to later tasks.

Risks or missing items:

- CI exists but is not enforced by branch protection/rulesets.
- Repository secret scanning and Dependabot security updates are disabled.
- Nested `pilot_phase2_poc/rag-service/.github/` files are inert because GitHub
  only honors root `.github/` workflows/config.

New design task needed:

- No. Owner/admin action, cleanup, or explicit risk acceptance is sufficient.

Affected tasks:

- All build tasks, especially `RAG-BT020`, `RAG-BT021`, `RAG-BT022`.

Severity:

- High for repo enforcement/security settings; Medium for inert nested
  workflow config.

## 8. Security And Data-Governance Reviewer

Reviewed:

- query safety rules, source registry schema, license-sensitive exclusions,
  CI/security checks, repository security setting evidence, and secret-handling
  notes.

Sufficient:

- Prompt-injection and protected-content categories are represented in query
  planning and golden-question fixtures.
- API keys are treated as local/env-only and not committed.
- `APAC-215` is explicitly excluded as metadata-only/license-sensitive.

Risks or missing items:

- Repo-level secret scanning is disabled.
- Branch protection/rulesets are absent.
- Raw upstream snapshot automation and production canonical promotion are
  deferred.
- The pasted Groq key from the DT015 setup should remain a rotation follow-up.

New design task needed:

- No, unless production corpus promotion/raw snapshot automation is pulled into
  pre-build scope.

Affected tasks:

- `RAG-BT012`, `RAG-BT013`, `RAG-BT014`, `RAG-BT018`, `RAG-BT019`,
  `RAG-BT020`, `RAG-BT022`.

Severity:

- High for repo security settings; Medium for data-governance deferrals.

## 9. Frontend/API-Consumer Impact Reviewer

Reviewed:

- `RAG-BT018`, query planner artifacts, LLM/generation plans, error schemas,
  citation requirements, and evaluation handoffs.

Sufficient:

- The intended API behavior is described in prose and correctly defers live
  external calls from default CI.
- Safe refusals and planner classifications are available as design inputs.

Risks or missing items:

- The API consumer contract is not explicit enough: request schema, response
  schema, citation object, safe refusal fields, confidence/status, model
  metadata, latency metadata, and error-envelope mapping are not pinned in one
  artifact.

New design task needed:

- Yes, as part of `RAG-DT019`.

Affected tasks:

- `RAG-BT018`, `RAG-BT019`, and later BFF/chatbot frontend work.

Severity:

- High.

## 10. Overall Systems Architect Synthesis

Reviewed:

- all specialist findings plus the full DT017 local inventory and baseline
  checks.

Sufficient:

- The design is not blocked.
- The core build path is coherent: KB fixtures -> chunking -> embeddings ->
  Qdrant integration -> semantic retrieval -> hybrid retrieval -> generation
  -> query API -> evaluation -> Docker/ops readiness.
- CI is in place and passing.

Risks or missing items:

- Two design contracts are still too implicit for a clean final impact review:
  hybrid retrieval fusion and generation/API output contract.
- Two high-risk non-design items need owner decision or remediation:
  repository enforcement/security settings and dependency provenance.

New design task needed:

- Yes: two proposed follow-up design tasks before `RAG-DT013`, unless waived.

Affected tasks:

- All final build tasks remain gated by `RAG-DT013`; most directly affected are
  `RAG-BT013`, `RAG-BT014`, `RAG-BT016`, `RAG-BT017`, `RAG-BT018`,
  `RAG-BT019`, `RAG-BT020`, `RAG-BT022`.

Severity:

- High, not Blocker.

