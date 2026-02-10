# Prompt Template - PCTF Framework

All prompts follow **Persona-Context-Task-Format**:

| Section | Purpose | Required |
|---------|---------|:--------:|
| **Persona** | WHO the AI should act as | Yes |
| **Context** | BACKGROUND and dependencies | Yes |
| **Task** | WHAT needs to be done | Yes |
| **Format** | HOW output should be structured | Yes |

---

## Execution Flow Reminder

    1. Human requests: "Generate prompt for Task N"
    2. AI creates prompt file → STOPS
    3. Human reviews prompt
    4. Human says: "Execute" / "Go"
    5. AI executes and creates output report

---

## Standard Prompt Structure

    # Task N.M: [Task Title]

    **Phase:** [Phase Name]
    **Initiative:** enhancement--poc-evaluation

    ---

    ## Persona

    You are a **[role]** with expertise in:
    - [Skill 1]
    - [Skill 2]
    - Test-Driven Development (TDD)
    - [Domain expertise]

    You write clean, well-documented, production-ready code.

    ---

    ## Context

    ### Initiative
    Waypoint Phase 1 POC — Week 4 Evaluation & Documentation

    ### Reference Documents
    - Master rules: ./CLAUDE.md (or ./AGENTS.md)
    - Detailed plan: ./pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/01-plan/DETAILED_PLAN.md
    - Roadmap: ./pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/02-roadmap/IMPLEMENTATION_ROADMAP.md
    - Previous task output: ./pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/04-prompts/[prev]/02-output/

    ### Working Directory
    ./pilot_phase1_poc/05_evaluation/

    ### Dependencies
    - [Prerequisite task 1 - COMPLETED]
    - [Prerequisite task 2 - COMPLETED]

    ### Current State
    [Describe what exists now after previous tasks]

    ---

    ## Task

    ### Objective
    [Clear statement of what this task accomplishes]

    ### Research Phase
    Before implementing, research:
    1. [Documentation to read]
    2. [Best practices to find]

    ### Implementation Phase (TDD)

    #### Step 1: Determine Tests
    - [ ] Test case 1: [description]
    - [ ] Test case 2: [description]

    #### Step 2: Write Tests (RED)
    Create tests BEFORE implementation.
    Location: ./pilot_phase1_poc/05_evaluation/tests/

    #### Step 3: Confirm RED
    Run tests, confirm they FAIL.

    #### Step 4: Implement
    Write minimum code to pass tests.
    Files to create/modify:
    - ./pilot_phase1_poc/05_evaluation/[path]

    #### Step 5: Confirm GREEN
    Run tests, confirm they PASS.

    #### Step 6: Refactor
    Clean up while keeping tests green.

    ---

    ## Format

    ### Output Location
    Save output report to:
    ./pilot_phase1_poc/05_evaluation/ai-workflow/enhancement--poc-evaluation/04-prompts/[NN-phase]/task_N/02-output/TASK_N_OUTPUT.md

    ### Output Report Sections
    1. **Summary** - What was accomplished
    2. **Research Findings** - Key learnings
    3. **Test Cases** - Tests written with results
    4. **TDD Log** - RED → GREEN progression
    5. **Implementation** - Files created/modified with key code
    6. **Validation** - How to verify it works
    7. **Issues** - Any problems encountered
    8. **Next Steps** - What comes next

    ### Update on Completion
    - [ ] Checklist updated: Mark task [x]
    - [ ] Roadmap updated: Add actual time

    ---

    ## Validation Criteria

    This task is complete when:
    - [ ] [Criterion 1]
    - [ ] [Criterion 2]
    - [ ] All tests pass
    - [ ] Output report created
    - [ ] Tracking docs updated
