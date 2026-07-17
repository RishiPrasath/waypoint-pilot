# RAG-DT006: Define Golden Questions And Answer Rubrics

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-governance/01-task-template.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT006` |
| Task Name | Define Golden Questions And Answer Rubrics |
| Design Lane | 04-chunking-and-evaluation-design |
| Source Question | Evaluation and use-case decision |
| Decision / ADR | ADR-RAG-0008 |
| Related Planning Docs | `02-rag-db/active/07-evaluation-plan.md` |
| Affected Build Tasks | RAG-BT019, RAG-BT013, RAG-BT014, RAG-BT018 |
| Branch | `codex/rag-dt006-golden-questions` |
| Worktree Path | `C:\tmp\rag-dt006-golden-questions` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |
| Evidence | `pilot_phase2_poc/rag-service/build-evidence/RAG-DT006-golden-questions.md` |

## 1. Task Definition

Design: research RAG evaluation practice, assess candidate golden questions,
then define the first golden question set and answer rubrics.

Goal: make evaluation possible before the evaluation harness is built.

Output Artifacts:

```text
docs/evaluation/golden-question-research-findings.md
docs/evaluation/golden-questions.md
```

Acceptance Criteria:

- questions map to supported use cases
- research findings summarize current RAG evaluation practices relevant to this
  service, including retrieval quality, answer quality, groundedness,
  citation correctness, refusal behavior, and malicious/prompt-injection cases
- candidate questions are assessed before final selection
- candidate assessment records include use case, question type, expected source
  coverage, inclusion decision, and rationale
- expected source types are listed
- expected approved source IDs or citation IDs are listed for positive cases
- APAC trade-lane questions are included
- negative cases include order status, driver assignment, partner operational
  procedure, irrelevant, and malicious/prompt-injection questions
- legacy Phase 1 KB examples can inform coverage gaps but cannot become
  expected sources unless audited/promoted
- answer quality rubric exists
- citation requirements exist
- irrelevant and malicious examples are included

Out Of Scope:

- evaluation runner code

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\tmp"
$TaskId = "rag-dt006"
$Slug = "golden-questions"
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
TASK_ID="rag-dt006"
SLUG="golden-questions"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\evaluation\golden-question-research-findings.md" -Pattern "retrieval|answer quality|groundedness|citation|refusal|malicious|candidate assessment"
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\docs\evaluation\golden-questions.md" -Pattern "rubric|citation|approved_source|order status|partner-source|malicious"
```

## 4. Design Work

Research current RAG evaluation practice before selecting golden questions.
Capture findings in:

```text
pilot_phase2_poc/rag-service/docs/evaluation/golden-question-research-findings.md
```

The findings report must:

- cite the external references used
- summarize applicable RAG evaluation dimensions
- distinguish retrieval scoring from answer scoring
- explain which practices are adopted for this service and which are deferred
- assess candidate golden questions before final selection

Candidate question assessment must record:

- candidate question
- supported use case or negative-case category
- question type: positive, unsupported operational, irrelevant, malicious, or
  prompt-injection
- expected source type
- expected approved source IDs or citation IDs when applicable
- inclusion decision: include, defer, or reject
- rationale

After the research and assessment pass, create the selected golden question set
and scoring rubric in:

```text
pilot_phase2_poc/rag-service/docs/evaluation/golden-questions.md
```

Separate retrieval scoring from answer scoring. Retrieval cases should define
expected source or citation matches, while answer cases should define grounded
response quality, refusal behavior, and citation requirements.

Review the legacy snapshot for useful examples and coverage gaps:

```text
pilot_phase2_poc/rag-service/legacy/phase1-kb-snapshot/
```

Golden answers must cite approved Phase 2 source candidates, not legacy files
directly, unless a design task explicitly promotes the source.

The final golden question set should not include every researched candidate.
Only include questions that are defensible against approved Phase 2 source
coverage, supported use cases, and required negative-case coverage.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT019, RAG-BT013, RAG-BT014, RAG-BT018

Required Updates:

- Update evaluation harness cases, expected source matches, retrieval acceptance
  checks, API contract expectations, research findings, candidate-question
  assessment, and the distinction between legacy examples and approved expected
  sources.

Deferred Impact:

- Golden set may expand after KB materialization.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with RAG Evaluation Lead and Logistics Domain Expert.

Verify that:

- research findings exist before the final golden question artifact
- every selected positive question has an expected approved source or citation
  target
- negative cases cover unsupported operational, irrelevant, malicious, and
  prompt-injection examples
- rejected/deferred candidates have a recorded reason
- the evidence file records the research references, acceptance-check output,
  affected build-task review, PR URL, CI result, and merge result

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt006 golden-questions"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt006 golden-questions"
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

Evidence is recorded in `pilot_phase2_poc/rag-service/build-evidence/RAG-DT006-golden-questions.md`.
