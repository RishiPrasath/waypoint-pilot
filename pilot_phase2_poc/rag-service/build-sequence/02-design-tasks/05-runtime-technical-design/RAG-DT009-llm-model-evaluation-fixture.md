# RAG-DT009: Define LLM Model Evaluation Fixture

Status: Planned

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT009` |
| Task Name | Define LLM Model Evaluation Fixture |
| Design Lane | 05-runtime-technical-design |
| Source Question | LLM model selection process |
| Decision / ADR | ADR-RAG-0003 |
| Related Planning Docs | `02-rag-db/research/llm-provider-selection.md` |
| Affected Build Tasks | RAG-BT016, RAG-BT017, RAG-BT018, RAG-BT019 |
| Branch | `codex/rag-dt009-llm-model-evaluation-fixture` |
| Worktree Path | `C:\tmp\rag-dt009-llm-model-evaluation-fixture` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Planned |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT009-llm-model-evaluation-fixture.md` |

## 1. Task Definition

Design: define model discovery, inventory, shortlist, and evaluation fixture
for Groq/OpenAI-compatible models.

Goal: compare candidate models using simulated or retrieved chunks before
locking final generation model.

Output Artifacts:

```text
docs/design/llm-model-evaluation-plan.md
docs/design/experiments/llm-model-evaluation/model-inventory.schema.json
docs/design/experiments/llm-model-evaluation/model-capability-review.md
docs/design/experiments/llm-model-evaluation/model-evaluation-runbook.md
```

Acceptance Criteria:

- credential and endpoint collection gate is defined
- API keys are never committed or written into evidence
- OpenAI-compatible `/models` inventory process is defined
- model capability and specification review is defined before assessment
- context window, max output, supported inputs, supported outputs, API surface,
  tool support, schema/JSON support, and known limitations are recorded when
  available
- gaps or unknowns from provider model metadata are explicitly marked and
  enriched from official/provider docs or safe capability probes
- candidate model listing process is defined
- model shortlist criteria are defined from the capability review, not raw
  model IDs alone
- simulated chunk test set is defined
- evaluation code shape and command contract are defined
- quality rubric is defined
- latency measurement is defined
- schema adherence and citation behavior are scored

Out Of Scope:

- live production model calls
- final model lock without evidence

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt009"
$Slug = "llm-model-evaluation-fixture"
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
TASK_ID="rag-dt009"
SLUG="llm-model-evaluation-fixture"
BRANCH="codex/$TASK_ID-$SLUG"
WORKTREE_PATH="$WORKTREE_ROOT/$TASK_ID-$SLUG"

mkdir -p "$WORKTREE_ROOT"
git -C "$REPO_ROOT" fetch origin
git -C "$REPO_ROOT" pull --ff-only origin main
git -C "$REPO_ROOT" config core.longpaths true
git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$WORKTREE_PATH" origin/main
git -C "$WORKTREE_PATH" status --short --branch
```
## 3. Acceptance Check

```powershell
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\llm-model-evaluation-plan.md" -Pattern "quality|latency|schema|citation"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\llm-model-evaluation-plan.md" -Pattern "LLM_BASE_URL|LLM_API_KEY|/models|inventory|shortlist|redact"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\llm-model-evaluation-plan.md" -Pattern "capability|context window|supported inputs|supported outputs|max output|modalities|unknown"
Test-Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\experiments\llm-model-evaluation\model-inventory.schema.json"
Test-Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\experiments\llm-model-evaluation\model-capability-review.md"
Test-Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\design\experiments\llm-model-evaluation\model-evaluation-runbook.md"
```

## 4. Design Work

Define model discovery, inventory, shortlist, evaluation process, and fixture
data.

The task must define the exact point where the owner provides provider
configuration. The configuration gate must ask for:

- OpenAI-compatible base URL, stored only in an environment variable such as
  `LLM_BASE_URL`
- API key, stored only in an environment variable such as `LLM_API_KEY`
- optional provider label, stored in an environment variable such as
  `LLM_PROVIDER_LABEL`

Credential safety requirements:

- do not paste API keys into repository files
- do not write API keys into evidence
- do not echo API keys in commands
- evidence may record provider label and endpoint host only after redaction
- scripts and runbooks must read secrets from environment variables

The plan must define how to inventory provider models through the
OpenAI-compatible endpoint:

```text
GET {LLM_BASE_URL}/models
```

The inventory design must specify:

- request headers
- timeout and error handling
- redaction behavior
- inventory output fields
- excluded fields, if they could contain secrets
- output path for a non-secret inventory artifact

Create a schema for inventory output:

```text
pilot_phase2_poc/rag-service/docs/design/experiments/llm-model-evaluation/model-inventory.schema.json
```

After model inventory, define a model capability and specification review before
shortlisting or assessing any LLM. The task must make clear that
OpenAI-compatible model inventory endpoints can identify available models, but
may expose only basic identity metadata for some providers. Richer capability
data must be gathered from the best available non-secret source before deciding
which models are necessary for evaluation.

The capability review must use this evidence order:

1. inventory from `GET {LLM_BASE_URL}/models`
2. per-model metadata from `GET {LLM_BASE_URL}/models/{model}` when the
   provider supports it
3. official provider model docs, model cards, or model comparison pages
4. safe capability probes only after the owner permits API-backed checks

Capability probes must be non-secret and minimal. They may check text response,
structured JSON/schema behavior, and citation-shaped output. Do not probe PDF,
file, image, audio, voice, realtime, or other multimodal behavior unless it is
necessary for the RAG design and explicitly approved for that provider.

Create the capability review artifact at:

```text
pilot_phase2_poc/rag-service/docs/design/experiments/llm-model-evaluation/model-capability-review.md
```

For each model under consideration, the capability review must record:

- provider label
- model ID
- source of capability data, such as `/models`, `/models/{model}`, provider
  docs, model comparison page, or probe
- context window, or `unknown` when unavailable
- max output tokens, or `unknown` when unavailable
- supported inputs, including text, image, PDF/file, audio, and voice where
  known
- supported outputs, including text, structured JSON, audio, and voice where
  known
- API surfaces, such as Responses API, Chat Completions compatibility, batch,
  or realtime where known
- tool/function support where known
- schema or JSON suitability where known
- relevant latency, cost, quota, or rate-limit notes when available
- assessment decision: include, defer, or exclude
- rationale for the decision

Unknown capabilities must remain marked as `unknown`; do not infer support from
the model name alone.

The model shortlist rules must define how to include, defer, or exclude models.
At minimum:

- include likely chat or instruct models
- exclude embedding-only models
- exclude audio, image, moderation, TTS, STT, or tool-specific models unless a
  later task explicitly needs them
- exclude deprecated models when provider metadata makes that clear
- record uncertainty when `/models` does not expose capabilities
- base shortlist decisions on the capability review, including context window,
  max output, supported inputs, supported outputs, API surface, and schema/JSON
  suitability
- prefer models with JSON/schema-following behavior when known

The runbook must define the proposed code shape and command contract for:

- provider inventory
- model capability/specification review
- model shortlist
- evaluation fixture construction
- model evaluation run
- output collection
- report generation

Create the runbook at:

```text
pilot_phase2_poc/rag-service/docs/design/experiments/llm-model-evaluation/model-evaluation-runbook.md
```

Evaluation must use project-local fixtures where possible:

- DT006 golden questions
- DT005 hybrid chunk outputs
- DT007 planner classifications
- DT012 first-pass candidate lineage

The assessment design must score:

- answer quality
- groundedness
- schema adherence
- citation behavior
- refusal and safety behavior
- latency
- provider/model errors
- malformed output handling

Final model lock remains out of scope until an evaluation run produces evidence.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT016, RAG-BT017, RAG-BT018, RAG-BT019

Required Updates:

- Update generation adapter candidates, provider inventory command assumptions,
  model capability/specification assumptions, mocked provider tests, response
  quality rubric, latency capture, schema adherence, citation checks, and
  no-secrets evidence handling.

Deferred Impact:

- Final model lock requires evaluation evidence.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with LLM Integration Engineer and RAG Evaluation Lead.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt009 llm-model-evaluation-fixture"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt009 llm-model-evaluation-fixture"
git -C "$WORKTREE_PATH" push -u origin "$BRANCH"
```

Open a PR to main.

Required PR checks:

- CI pipeline runs
- CI passes
- AI scans the design artifact and affected build-task updates
- human owner reviews the PR
- accepted findings are fixed

## 8. Merge

Merge only after CI passes and the PR is reviewed. Record PR URL, CI result,
merge commit, unresolved risks, and follow-up debt entries if any. Then clean up
the worktree.

### Windows PowerShell

```powershell
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree remove $WorktreePath
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" worktree prune
git -C "C:\Users\prasa\Documents\Github\waypoint-pilot" pull --ff-only origin main
```

### Linux / macOS Bash

```bash
git -C "$REPO_ROOT" worktree remove "$WORKTREE_PATH"
git -C "$REPO_ROOT" worktree prune
git -C "$REPO_ROOT" pull --ff-only origin main
```
## Task Evidence

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT009-llm-model-evaluation-fixture.md`.
