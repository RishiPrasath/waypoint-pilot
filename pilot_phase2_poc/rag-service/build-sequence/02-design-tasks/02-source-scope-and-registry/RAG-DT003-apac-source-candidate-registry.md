# RAG-DT003: Create APAC Source Candidate Registry

Status: Complete

## Sequence Entry

Start from build-sequence/00-index.md, then open the lane index for this task before opening the task file.
Task files should follow the canonical template in build-sequence/00-task-sequence-template-proposal.md.

| Field | Value |
|---|---|
| Task ID | `RAG-DT003` |
| Task Name | Create APAC Source Candidate Registry |
| Design Lane | 02-source-scope-and-registry |
| Source Question | RAG-Q012 APAC authoritative-source research |
| Decision / ADR | ADR-RAG-0012 |
| Related Planning Docs | `02-rag-db/research/authoritative-sources-apac.md`, `02-rag-db/active/02-knowledge-source-plan.md` |
| Affected Build Tasks | RAG-BT008, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019 |
| Branch | `codex/rag-dt003-apac-source-candidate-registry` |
| Worktree Path | `D:\Code\Github\waypoint-pilot-worktrees\rag-dt003-apac-source-candidate-registry` |
| Owner | solo developer |
| AI Review Partner | Codex |
| Status | Complete |

## 1. Task Definition

Design: create candidate source rows for APAC authoritative sources.

Goal: identify official customs, trade, logistics, Incoterms, and regional
sources before canonical KB creation.

Output Artifact:

```text
knowledge_base/registry/source_registry.yaml
```

Acceptance Criteria:

- first-pass markets are listed
- source owner and `source_uri` are captured
- `document_id`, `authority_level`, `source_status`, `promotion_status`, and
  `retrieval_eligible` are captured using the source registry vocabulary
- authority, freshness, access, and license/reuse status are captured
- APAC-specific fields are captured where relevant: `source_access_pattern`,
  `language`, `translation_review_required`, `dynamic_lookup_snapshot`,
  `legal_disclaimer`, `license_sensitive`, `reuse_mode`, and
  `retrieval_namespace`
- promotion blockers are visible

Out Of Scope:

- scraping
- cleaned canonical markdown

## 2. Worktree And Branch Setup

Create the branch and worktree before creating or editing design artifacts.

### Windows PowerShell

```powershell
$RepoRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot"
$WorktreeRoot = "C:\Users\prasa\Documents\Github\waypoint-pilot-worktrees"
$TaskId = "rag-dt003"
$Slug = "apac-source-candidate-registry"
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
TASK_ID="rag-dt003"
SLUG="apac-source-candidate-registry"
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
Select-String -Path "$WorktreePath\pilot_phase2_poc\rag-service\knowledge_base\registry\source_registry.yaml" -Pattern "document_id|source_uri|authority_level|source_status|promotion_status|retrieval_eligible"
```

## 4. Design Work

Use APAC research evidence to create candidate registry rows.

The first-pass registry should cover core APAC markets and trade-lane source
assembly needs, including official customs/trade authorities, regional
agreement sources, and license-sensitive global standards bodies where they are
needed for citation or summary-only treatment.

## 5. Build Task Impact

Affected Build Tasks:

- RAG-BT008, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019

Required Updates:

- Update source registry rows, ingestion fixture source list, retrieval metadata expectations, and golden source coverage.

Deferred Impact:

- Scraping/materialization handled by RAG-DT012.

Impact Review Status:

- Pending RAG-DT013 review.

## 6. Verification

Review with Logistics Domain Expert and Knowledge Base Curator.

## 7. Branch Workflow

### Windows PowerShell

```powershell
git -C $WorktreePath status --short
git -C $WorktreePath add pilot_phase2_poc/rag-service
git -C $WorktreePath commit -m "docs(rag): complete rag-dt003 apac-source-candidate-registry"
git -C $WorktreePath push -u origin $Branch
```

### Linux / macOS Bash

```bash
git -C "$WORKTREE_PATH" status --short
git -C "$WORKTREE_PATH" add pilot_phase2_poc/rag-service
git -C "$WORKTREE_PATH" commit -m "docs(rag): complete rag-dt003 apac-source-candidate-registry"
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
## 9. Task Evidence

Branch: `codex/rag-dt003-apac-source-candidate-registry`
Worktree: `D:\Code\Github\waypoint-pilot-worktrees\rag-dt003-apac-source-candidate-registry`
PR:
Commit:

Design Artifact:

`pilot_phase2_poc/rag-service/knowledge_base/registry/source_registry.yaml`

Affected Build Tasks:

RAG-BT008, RAG-BT012, RAG-BT013, RAG-BT014, RAG-BT019

Files Changed:
- `pilot_phase2_poc/rag-service/knowledge_base/registry/source_registry.yaml`
- `pilot_phase2_poc/rag-service/knowledge_base/registry/source_registry.schema.json`
- `pilot_phase2_poc/rag-service/docs/design/source-registry-schema.md`
- `pilot_phase2_poc/rag-service/build-sequence/02-design-tasks/02-source-scope-and-registry/RAG-DT003-apac-source-candidate-registry.md`

Checks Run:
- YAML parse and schema validation using PyYAML 6.0.3 and `jsonschema` 4.26.0.
- Validated 46 `sources[]` records in `source_registry.yaml` against `source_registry.schema.json`.
- Confirmed `retrieval_eligible_true=0`.
- Confirmed first-pass markets: SG, MY, ID, TH, VN, PH, ASEAN, Global.
- `Select-String -Path pilot_phase2_poc/rag-service/knowledge_base/registry/source_registry.yaml -Pattern "document_id|source_uri|source_owner|authority_level|source_status|promotion_status|retrieval_eligible|source_access_pattern|language|translation_review_required|dynamic_lookup_snapshot|legal_disclaimer|license_sensitive|reuse_mode|retrieval_namespace"`

CI Result:

Pending PR.

AI Review Findings:
- Three subagent research lanes completed and were normalized into the registry:
  - Singapore, Malaysia, Indonesia
  - Thailand, Viet Nam, Philippines
  - ASEAN, WCO, WTO, UN/CEFACT, ICC/global references
- No carrier rows were promoted into the APAC candidate registry.
- No live operational shipment/order/status/timeline source was added.

Human Review Notes:
- Pending human owner review.

Issues Encountered:
- DT003 requires `source_owner`, but the DT008 schema did not include it as a first-class field.
- ICC Incoterms sources require an authority class that is not government/intergovernmental.
- Several tariff/trade repository sources are dynamic lookup portals and are unsafe for direct static ingestion without later materialization rules.

Resolution:
- Added required `source_owner` to `source_registry.schema.json` and updated embedded schema examples.
- Added `standards_body` to `authority_level` for ICC Incoterms sources.
- Set all DT003 candidate rows to `retrieval_eligible: false`.
- Used `manual_snapshot` and license-sensitive reuse modes for dynamic or controlled sources.

Debt / Follow-Ups:
- RAG-DT004 must align registry storage/layout decisions with `source_registry.yaml`.
- RAG-DT012 must decide snapshot, canonical Markdown, and extraction rules for each promoted source.
- RAG-BT008/BT012 must consume only explicitly promoted registry rows.
- RAG-BT013/BT014/BT019 must preserve `document_id`, `source_owner`, namespace, language, legal disclaimer, and reuse metadata.
- ICC/WCO licensed or copyright-controlled materials require legal/reuse approval before any ingestion.
- Dynamic portals such as tariff finders and national trade repositories require explicit snapshot/query-output policy before materialization.









