# PCTF Prompt Template Format

**PCTF** = **P**ersona, **C**ontext, **T**ask, **F**ormat

---

## Instructions for Claude

When the user requests a task from the implementation roadmap:

1. **Create task folder** in `prompts/` with naming: `[GROUP]_[TASK]_[description]/`
   - Example: `01_1.1_folder_structure/`
   - Example: `02_2.1_config_module/`

2. **Create prompt file** inside the task folder: `prompt.md`

3. **Follow TDD (Test-Driven Development)**:
   - Write tests FIRST in `tests/test_<module>.py`
   - Run tests to confirm they fail (Red)
   - Implement code to make tests pass (Green)
   - Refactor if needed while keeping tests green

4. **After completion**, create report file in same folder: `REPORT.md`

**Folder structure created on-demand**:
```
prompts/
├── 00_PCTF_TEMPLATE.md
├── 01_1.1_folder_structure/      ← Created when Task 1.1 requested
│   ├── prompt.md
│   └── REPORT.md
├── 02_2.1_config_module/         ← Created when Task 2.1 requested
│   ├── prompt.md
│   └── REPORT.md
└── ...
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
- [ ] Test file created at `tests/test_<module>.py`
- [ ] Tests written BEFORE implementation
- [ ] All tests pass

---

## Format

### Output Structure
[Expected file structure, naming conventions]

### Code Style
[Language-specific style guidelines]

### Documentation
[Inline comments, docstrings requirements]

### Tests (TDD)
```
tests/
└── test_<module>.py    # Test file for this module
```

**Test Structure**:
```python
import pytest
from scripts.<module> import <functions>

class Test<FunctionName>:
    def test_<scenario>_<expected>(self):
        # Arrange
        # Act
        # Assert
```

### Validation
[Commands to verify the output is correct]

```bash
# Run tests first (TDD)
python -m pytest tests/test_<module>.py -v

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
| Task folder | `[GROUP]_[TASK]_[description]/` | `01_1.1_folder_structure/` |
| Prompt file | `prompt.md` | `prompt.md` |
| Report file | `REPORT.md` | `REPORT.md` |

---

## Placeholders

| Placeholder | Value |
|-------------|-------|
| `{{PROJECT_ROOT}}` | `C:\Users\prasa\Documents\Github\waypoint-pilot` |
| `{{PILOT_DIR}}` | `{{PROJECT_ROOT}}\pilot_phase1_poc` |
| `{{PIPELINE_DIR}}` | `{{PILOT_DIR}}\02_ingestion_pipeline` |
| `{{KB_DIR}}` | `{{PILOT_DIR}}\01_knowledge_base` |
| `{{SCRIPTS_DIR}}` | `{{PIPELINE_DIR}}\scripts` |
| `{{PROMPTS_DIR}}` | `{{PIPELINE_DIR}}\prompts` |
