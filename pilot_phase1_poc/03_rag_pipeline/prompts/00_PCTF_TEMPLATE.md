# PCTF Prompt Template Format

**PCTF** = **P**ersona, **C**ontext, **T**ask, **F**ormat

---

## Instructions for Claude

When the user requests a task from the implementation roadmap:

1. **Create task folder** in `prompts/` with naming: `[GROUP]_[TASK]_[description]/`
   - Example: `01_1.1_copy_assets/`
   - Example: `02_2.1_retrieval_quality_test/`
   - Example: `05_5.1_llm_service/`

2. **Create prompt file** inside the task folder: `prompt.md`

3. **Follow TDD (Test-Driven Development)**:
   - Write tests FIRST in `tests/test_<module>.py` (Python) or `tests/<module>.test.js` (Node.js)
   - Run tests to confirm they fail (Red)
   - Implement code to make tests pass (Green)
   - Refactor if needed while keeping tests green

4. **After completion**, create report file in same folder: `REPORT.md`

**Folder structure created on-demand**:
```
prompts/
├── 00_PCTF_TEMPLATE.md
├── 01_1.1_copy_assets/           ← Created when Task 1.1 requested
│   ├── prompt.md
│   └── REPORT.md
├── 02_2.1_retrieval_quality_test/ ← Created when Task 2.1 requested
│   ├── prompt.md
│   └── REPORT.md
└── ...
```

---

## MCP Tools for Documentation Lookup

Before implementing any task involving external libraries, use MCP tools to fetch current documentation:

### docfork (Primary)
Use `docfork:docfork_search_docs` to search library documentation:
- Query: Library name + specific topic (e.g., "chromadb query collection")
- Use `docforkIdentifier` for targeted searches (e.g., "chroma-core/chroma")

Use `docfork:docfork_read_url` to read full documentation pages from search results.

### context7 (Alternative)
Use `mcp_context7_resolve-library-id` to find library IDs:
- Input: Library name (e.g., "express", "chromadb")

Use `mcp_context7_query-docs` to fetch documentation:
- Input: Library ID from resolve step
- Topic: Specific feature (e.g., "middleware", "routing")

### When to Use
- **Always** before implementing new library integrations
- When encountering unfamiliar APIs
- When error messages suggest API changes
- For best practices and recommended patterns

### Example Workflow
```
1. Task requires ChromaDB collection querying
2. Use docfork: search "chromadb collection query filter"
3. Read relevant documentation URLs
4. Implement based on current API
5. Write tests reflecting actual API behavior
```

---

## Prompt Template

```markdown
# [TASK_ID]: [Brief Task Title]

## Persona

> You are a [role] with expertise in [relevant skills].
> You follow [standards/practices] and prioritize [qualities].

---

## Context

### Project Background
[Brief project context]

### Current State
[What exists now - files, folders, dependencies]

### Reference Documents
[Paths to relevant documentation]

### Dependencies
[Previous tasks this depends on]

---

## Task

### Objective
[Clear statement of what needs to be accomplished]

### Requirements
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

### Specifications
[Technical specifications, configurations, schemas]

### Constraints
[Limitations, boundaries, things to avoid]

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### TDD Requirements

**For Python modules:**
- [ ] Test file created at `tests/test_<module>.py`
- [ ] Tests written BEFORE implementation
- [ ] All tests pass with `python -m pytest tests/test_<module>.py -v`

**For Node.js modules:**
- [ ] Test file created at `tests/<module>.test.js`
- [ ] Tests written BEFORE implementation
- [ ] All tests pass with `npm test`

**TDD Workflow:**
1. **Red**: Write failing tests first
2. **Green**: Implement minimum code to pass
3. **Refactor**: Clean up while keeping tests green

---

## Format

### Output Structure
[Expected file structure, naming conventions]

### Code Style

**Python:**
- Google-style docstrings with Args/Returns sections
- Type hints for function signatures
- snake_case for functions/variables, PascalCase for classes

**Node.js/Express:**
- JSDoc comments for exported functions
- camelCase for functions/variables, PascalCase for classes
- ES modules (import/export)
- async/await for asynchronous code

### Documentation
[Inline comments, docstrings requirements]

### Tests

**Python:**
```
tests/
└── test_<module>.py    # pytest test file
```

```python
import pytest
from scripts.<module> import <functions>

class Test<FunctionName>:
    def test_<scenario>_<expected>(self):
        # Arrange
        # Act
        # Assert
```

**Node.js:**
```
tests/
└── <module>.test.js    # Jest test file
```

```javascript
const { functionName } = require('../src/services/module');

describe('functionName', () => {
  test('should <expected behavior>', async () => {
    // Arrange
    // Act
    // Assert
  });
});
```

### Validation
[Commands to verify the output is correct]

```bash
# Python tests
python -m pytest tests/test_<module>.py -v

# Node.js tests
npm test

# Then run validation commands
```
```

---

## Report Template

```markdown
# [TASK_ID]: [Brief Task Title] - Output Report

**Completed**: [YYYY-MM-DD HH:MM]
**Status**: [Complete / Partial / Failed]

---

## Summary
[Brief description of what was accomplished]

---

## Files Created/Modified

| File | Action | Path |
|------|--------|------|
| [filename] | Created/Modified | [full path] |

---

## Acceptance Criteria

- [x] [Criterion 1 - completed]
- [ ] [Criterion 2 - incomplete]

---

## Issues Encountered
[Any problems or blockers, or "None"]

---

## Next Steps
[Recommendations or follow-up tasks]
```

---

## Naming Convention

| Item | Pattern | Example |
|------|---------|---------|
| Task folder | `[GROUP]_[TASK]_[description]/` | `01_1.1_copy_assets/` |
| Prompt file | `prompt.md` | `prompt.md` |
| Report file | `REPORT.md` | `REPORT.md` |

---

## Placeholders

| Placeholder | Value |
|-------------|-------|
| `{{PROJECT_ROOT}}` | `C:\Users\prasa\Documents\Github\waypoint-pilot` |
| `{{PILOT_DIR}}` | `{{PROJECT_ROOT}}\pilot_phase1_poc` |
| `{{RAG_DIR}}` | `{{PILOT_DIR}}\03_rag_pipeline` |
| `{{INGESTION_DIR}}` | `{{PILOT_DIR}}\02_ingestion_pipeline` |
| `{{KB_DIR}}` | `{{PILOT_DIR}}\01_knowledge_base` |
| `{{SRC_DIR}}` | `{{RAG_DIR}}\src` |
| `{{CLIENT_DIR}}` | `{{RAG_DIR}}\client` |
| `{{SCRIPTS_DIR}}` | `{{RAG_DIR}}\scripts` |
| `{{PROMPTS_DIR}}` | `{{RAG_DIR}}\prompts` |
