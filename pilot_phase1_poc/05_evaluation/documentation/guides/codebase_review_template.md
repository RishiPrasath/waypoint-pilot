# Waypoint Co-Pilot Evaluation Codebase Review Template

Use this template to document the `pilot_phase1_poc/05_evaluation` codebase in a
single, evidence-driven review. Replace every placeholder with findings backed by
specific file paths, commands, or test output.

---

## 1. Document Metadata

- **Project:** Waypoint Co-Pilot
- **Target folder:** `pilot_phase1_poc/05_evaluation`
- **Review date:** `[YYYY-MM-DD]`
- **Reviewer:** `[name]`
- **Scope:** `[what is included]`
- **Out of scope:** `[what is excluded]`

## 2. Executive Summary

Write a concise summary of what this codebase is, what it does, and the most
important conclusions from the review.

- **What the system does:** `[one-paragraph summary]`
- **Current maturity:** `[POC / beta / near-production / etc.]`
- **Primary strengths:** `[top 3]`
- **Primary risks:** `[top 3]`
- **Bottom line:** `[overall judgment]`

## 3. Repository Map

Describe the top-level layout and the role of each major directory.

| Path | Role | Notes |
| --- | --- | --- |
| `backend/` | `[what it contains]` | `[important observations]` |
| `client/` | `[what it contains]` | `[important observations]` |
| `scripts/` | `[what it contains]` | `[important observations]` |
| `tests/` | `[what it contains]` | `[important observations]` |
| `kb/` | `[what it contains]` | `[important observations]` |
| `documentation/` | `[what it contains]` | `[important observations]` |
| `demo/` | `[what it contains]` | `[important observations]` |
| `ai-workflow/` | `[what it contains]` | `[important observations]` |

## 4. System Overview

Explain the system at the architecture level.

- **User entry points:** `[UI, API, scripts, etc.]`
- **Backend responsibilities:** `[summary]`
- **Frontend responsibilities:** `[summary]`
- **Python responsibilities:** `[summary]`
- **Data stores:** `[ChromaDB, files, JSON, etc.]`
- **External services:** `[Groq, browser tools, etc.]`

## 5. How It Works

Describe the runtime flow end to end.

### 5.1 Request Flow

1. `[step 1]`
2. `[step 2]`
3. `[step 3]`
4. `[step 4]`
5. `[step 5]`

### 5.2 Data Flow

- **Input data:** `[what enters the system]`
- **Transformations:** `[how data changes]`
- **Outputs:** `[what the system emits]`
- **Persistence:** `[what gets stored, where]`

### 5.3 Control Flow

- **Happy path:** `[describe]`
- **Validation/error path:** `[describe]`
- **Fallback path:** `[describe]`
- **Out-of-scope path:** `[describe]`

## 6. Component Breakdown

Document each subsystem with concrete evidence.

### 6.1 Backend

- **Entry point:** `[file path]`
- **Core services:** `[file paths]`
- **Routes:** `[file paths]`
- **Config:** `[file paths]`
- **Prompting:** `[file paths]`
- **Observed design decisions:** `[what and why]`
- **Issues or gaps:** `[what needs attention]`

### 6.2 Frontend

- **Component tree:** `[file paths]`
- **State flow:** `[how state moves through the UI]`
- **Response rendering:** `[markdown, sections, etc.]`
- **Styling system:** `[Tailwind, custom CSS, etc.]`
- **Observed design decisions:** `[what and why]`
- **Issues or gaps:** `[what needs attention]`

### 6.3 Scripts

- **Ingestion:** `[file paths]`
- **Chunking:** `[file paths]`
- **Evaluation harness:** `[file paths]`
- **PDF extraction:** `[file paths]`
- **Utility scripts:** `[file paths]`
- **Observed design decisions:** `[what and why]`
- **Issues or gaps:** `[what needs attention]`

### 6.4 Tests

- **Backend tests:** `[file paths]`
- **Python tests:** `[file paths]`
- **Frontend tests:** `[file paths]`
- **What the tests protect:** `[coverage summary]`
- **What is not covered:** `[coverage gaps]`

### 6.5 Knowledge Base

- **Content structure:** `[directories and scope]`
- **Metadata schema:** `[frontmatter fields]`
- **Ingestion assumptions:** `[what the pipeline expects]`
- **Constraints:** `[frozen content, scope limits, etc.]`

### 6.6 Documentation and Workflow

- **Docs structure:** `[documentation tree]`
- **Workflow rules:** `[ai-workflow structure and checkpoints]`
- **Operational guidance:** `[how the repo expects work to happen]`

## 7. Evaluation Process

Document the evaluation workflow in detail.

### 7.1 Setup

- **Prerequisites:** `[Node, Python, env vars, services]`
- **How to start the stack:** `[commands]`
- **How to prepare data:** `[ingestion commands]`

### 7.2 Automated Checks

- **Ingestion checks:** `[what is validated]`
- **Unit tests:** `[what runs and what it covers]`
- **Integration checks:** `[API, pipeline, UI, etc.]`
- **Evaluation harness:** `[what it measures]`

### 7.3 Metrics

| Metric | Target | Current Result | Evidence |
| --- | --- | --- | --- |
| Deflection rate | `[target]` | `[result]` | `[path or command output]` |
| Citation accuracy | `[target]` | `[result]` | `[path or command output]` |
| Hallucination rate | `[target]` | `[result]` | `[path or command output]` |
| Out-of-scope handling | `[target]` | `[result]` | `[path or command output]` |
| Latency | `[target]` | `[result]` | `[path or command output]` |
| Stability | `[target]` | `[result]` | `[path or command output]` |

### 7.4 Checkpoints

- **Checkpoint 1:** `[what was reviewed]`
- **Checkpoint 2:** `[what was reviewed]`
- **Checkpoint 3:** `[what was reviewed]`
- **Any blockers:** `[issues that slowed or blocked evaluation]`

## 8. Design Decisions

Record the important design choices and the reasoning behind them.

| Decision | Why it was chosen | Tradeoff | Evidence |
| --- | --- | --- | --- |
| `[decision]` | `[reason]` | `[tradeoff]` | `[file path]` |
| `[decision]` | `[reason]` | `[tradeoff]` | `[file path]` |
| `[decision]` | `[reason]` | `[tradeoff]` | `[file path]` |

## 9. What Went Well

Summarize the strong parts of the codebase.

- `[strength 1]`
- `[strength 2]`
- `[strength 3]`
- `[strength 4]`

For each strength, include:
- **Evidence:** `[file path or test result]`
- **Impact:** `[why it matters]`

## 10. What Did Not Go Well

Summarize weaknesses, confusing areas, or technical debt.

- `[issue 1]`
- `[issue 2]`
- `[issue 3]`
- `[issue 4]`

For each issue, include:
- **Evidence:** `[file path or test result]`
- **Risk:** `[why it matters]`
- **Severity:** `[low / medium / high]`

## 11. Regression-Level Critique

Focus on what can break when changes are made.

### 11.1 High-Risk Regression Areas

- `[area where changes are risky]`
- `[area where tests are thin]`
- `[area with hidden coupling]`

### 11.2 Likely Regression Modes

- `[example failure mode]`
- `[example failure mode]`
- `[example failure mode]`

### 11.3 Missing Safeguards

- `[missing test type]`
- `[missing validation]`
- `[missing runtime guard]`

## 12. Improvement Recommendations

Group improvements by leverage.

### 12.1 Quick Wins

- `[small improvement]`
- `[small improvement]`

### 12.2 Medium Effort

- `[medium improvement]`
- `[medium improvement]`

### 12.3 Structural Improvements

- `[larger architecture improvement]`
- `[larger test/process improvement]`

## 13. Open Questions

Capture anything that still needs confirmation.

- `[question 1]`
- `[question 2]`
- `[question 3]`

## 14. Evidence Appendix

List the files, commands, and outputs used to support the review.

| Evidence Type | Reference | Notes |
| --- | --- | --- |
| File | `[absolute path]` | `[why it mattered]` |
| Command | `[command]` | `[what it proved]` |
| Test output | `[summary]` | `[what passed or failed]` |

## 15. Final Verdict

Write the final judgment in plain language.

- **Overall assessment:** `[summary]`
- **Recommended next steps:** `[bulleted list]`
- **If I had one week to improve this codebase:** `[priority list]`

