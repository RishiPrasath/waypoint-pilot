# Explanations

This folder stores requested code and test explanations for the Partner Source build.

Use this folder when a task is technically complete but the structure, purpose, or test logic still feels unclear.

## Naming

Use short, numbered names when the explanation maps to a build task:

```text
task-01-project-setup.md
task-02-ci-pipeline.md
task-03-package-layout.md
task-04-status-transition-policy.md
task-05-assignment-authorization-policy.md
task-06-seed-store-and-repositories.md
```

Use focused names when the explanation is about one file or concept:

```text
springboot-repository-tests.md
fastapi-domain-package-layout.md
assignment-active-work-rule.md
```

## Suggested Format

```text
# Title

## What This Is

## Why It Exists

## Files Involved

## Code Structure

## Test Structure

## How The Pieces Connect

## Common Confusions

## Commands To Verify
```

## Rule

These files are learning notes only. They should explain the existing code and tests, not become a second source of truth for the contract.

For contract decisions, use:

```text
AGREED_SPEC.md
docs/
partner-source-fastapi/build-sequence/
partner-source-springboot/build-sequence/
```
