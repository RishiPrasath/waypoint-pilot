# Tuning Playbook

## Objective

Use this playbook to turn failures into controlled experiments and measurable fixes.

## Scope of a Tuning Run

- One failure cluster per run.
- One primary lever change per run.
- One pre/post scenario snapshot.

## Playbook Steps

1. Define failure report and severity band.
2. Confirm baseline outputs and candidate outputs are collected.
3. Select one hypothesis linked to one remediating area:
   - chunking
   - embedding
   - vector config
   - retrieval strategy
   - planner
   - prompt/schema
   - query API
   - local or CI harness
4. Record hypothesis, expected metric movement, and expected risk.
5. Run the affected check only (or smallest superset required).
6. Compare against baseline with identical query set and same environment.
7. Classify outcome as improvement, neutral, or regression.
8. Create follow-up task if required by blocker.

## Experiment Record Template

- run-id:
- target metric:
- hypothesis:
- change made:
- environment:
- results vs baseline:
- decision (`Promote`/`Hold`/`Reject`):
- next owner:

## Promotion Pattern

- `Promote`: metric improvements or neutral drift in non-mandatory dimensions.
- `Hold`: mixed results with unresolved risk.
- `Reject`: any hard failure or mandatory-metric regression.
