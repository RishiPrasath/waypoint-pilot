# Checkpoint Template

Use this template for checkpoint review documents created after reaching each milestone.

**IMPORTANT — Two Separate Artifacts:**
- `description/DESCRIPTION.md` = Pre-created acceptance criteria. Exists before the checkpoint is reached. Update checkboxes as tasks complete.
- `review/CHECKPOINT_N_REVIEW.md` = The actual review deliverable. Created ONLY when the checkpoint is reached. This is the PRIMARY output.

**When a checkpoint is triggered (last task before it completes):**
1. Update `description/DESCRIPTION.md` checkboxes
2. **CREATE** `review/CHECKPOINT_N_REVIEW.md` using the template below — this is the deliverable
3. Mark the checkpoint as complete in the checklist

Updating DESCRIPTION.md alone is NOT sufficient. The review file MUST exist.

---

## Review Document Structure

    # Checkpoint N Review

    **Checkpoint:** [N] - [Feature Name]
    **Status:** ✅ COMPLETE / ❌ INCOMPLETE
    **Date:** [Date]

    ---

    ## Summary

    | Metric | Value |
    |--------|-------|
    | Tasks Completed | X/Y |
    | Tests Passing | X |
    | Criteria Met | X/Y |

    ---

    ## Progress

        Task X: [Name]    ████████████████████ 100% ✅
        Task Y: [Name]    ████████████████████ 100% ✅

        Overall: ████████████████████ 100% ✅

    ---

    ## Validation Results

    | Criterion | Status | Notes |
    |-----------|--------|-------|
    | [Criterion] | ✅ | [Notes] |

    ---

    ## Demo Results

        [Command run]
        [Output received]
        [Expected vs Actual]

    ---

    ## Issues Encountered

    [Any issues and how they were resolved]

    ---

    ## Verdict

    **✅ CHECKPOINT PASSED** / **❌ CHECKPOINT FAILED**

    [Summary statement]

    ---

    ## Next Steps

    Proceed to:
    - Task [Z]: [Description]
