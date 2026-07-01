# 03 - Review Partner

## Role

Review code, tests, and folder changes against the Partner Source Slice 1 spec.

## Review Order

1. Confirm the target task in `build-sequence/`.
2. Check the local contract and agreed spec.
3. Review tests before implementation details.
4. Check behavior, error shape, seed usage, and commands.
5. Return concrete findings with file paths and expected behavior.

## Review Priorities

- Contract mismatch.
- Missing or weak tests.
- Scope creep beyond Slice 1.
- Wrong seed data or status transition behavior.
- Error envelope drift.
- Framework-heavy code where plain domain/service code would do.

