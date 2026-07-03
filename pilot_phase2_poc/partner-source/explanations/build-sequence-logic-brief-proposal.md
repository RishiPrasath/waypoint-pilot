# Build Sequence Per-Code-Block Explanation Proposal

## Problem

The build-sequence task files now give exact tests, file maps, exact code, commands, and done criteria.

That helps execution.

But for learning, many tasks still jump too quickly from:

```text
Purpose
-> Tests To Write First
-> Exact Code
```

The missing piece is a short explanation of:

```text
What this task is building
Why these files exist
How the code pieces talk to each other
What the test is proving
What mental model to use before writing the code
```

More specifically, the missing piece is not only task-level explanation.

The bigger gap is per-code-block explanation.

Right now the task files often say:

```text
Create SomeFile.java:

```java
...
```
```

That gives the exact code, but it does not explain how to read that specific file.

The improved structure should explain each code block before showing it.

This is especially important for concepts like:

```text
domain
repository
service
DTO
controller
seed data
resources
configuration
```

## Recommendation

Keep the current 12 top-level headings.

Do not add a new top-level `## Logic Brief` section unless we also update every audit script and task-status guide.

Instead, improve two places:

1. Add a short task-level `### Logic Brief` inside `## Purpose`.
2. Add a short per-file explanation before each code block inside `## Exact Code` and `## Tests To Write First`.

Recommended structure:

```text
## Purpose

One or two sentences explaining the task outcome.

### Logic Brief

- What this task adds:
- Why this exists:
- How the pieces connect:
- What the tests prove:
- What this unlocks next:
```

Then, inside `## Exact Code`, use this per-code-block pattern:

```text
Create `SomeFile.java`:

What this file does:

- [Plain-language role of the file.]

Why this code exists:

- [Why this file is needed for the task.]

How to read the code:

- [Point out the 1-3 important lines or methods.]

```java
[exact code]
```
```

Inside `## Tests To Write First`, use this per-test-file pattern:

```text
`SomeFeatureTest.java`:

What this test proves:

- [Behavior the test locks down.]

Why this test comes first:

- [What failure we expect before implementation.]

How to read the test:

- Arrange: [setup]
- Act: [method call]
- Assert: [expected result]

```java
[exact test code]
```
```

This keeps the existing required template intact:

```text
## Status
## Purpose
## Source Docs To Read
## Prereqs
## Tests To Write First
## File Map
## Exact Code
## Commands To Run
## Done Criteria
## Common Mistakes
## Stop / Do Not Add
## Change Notes
```

## Why This Is Better Than A New Top-Level Heading

The current build-sequence folders already pass template audits.

Adding a new top-level section such as:

```text
## Logic Brief
```

would force us to update:

```text
TASK_STATUS_GUIDE.md
17-final-gate task audits
any script or command that checks exact heading order
all existing task files
```

Putting the logic explanation inside `## Purpose` gives the learning benefit without breaking the structure.

## Proposed Purpose Section Template

Use this inside every task file:

```text
## Purpose

[One or two sentences stating the outcome.]

### Logic Brief

- What this task adds: [new capability, folder, rule, endpoint, or test gate]
- Why this exists: [business/learning reason]
- How the pieces connect: [main flow between files]
- What the tests prove: [specific behavior under test]
- What this unlocks next: [next task or next layer]
```

## Proposed Per-Code-Block Template

Use this before every code block in `## Exact Code`.

```text
Create `FileName.ext`:

What this file does:

- One short explanation of the file's job.

Why this code exists:

- One short explanation of why this task needs the file.

How to read the code:

- Point to the main class/function/record.
- Point to the key method or field.
- Point to anything easy to misunderstand.

```language
code here
```
```

For very small files, use the compact form:

```text
Create `FileName.ext`:

Explanation: this file [does X] so [Y can happen]. The important line is [Z].

```language
code here
```
```

Do not write a paragraph for every line of code.

The goal is:

```text
before seeing the code, Rishi knows what he is looking at
```

not:

```text
repeat the code in English line by line
```

## Proposed Per-Test-Code-Block Template

Use this before every code block in `## Tests To Write First`.

```text
`SomeTest.java`:

What this test file proves:

- [Behavior 1]
- [Behavior 2]

Why this test exists:

- [What bug or contract rule it protects.]

How to read the test:

- Arrange: create the object or seed data.
- Act: call the method under test.
- Assert: check the expected result.

```language
test code here
```
```

For pytest files:

```text
`test_some_feature.py`:

What this test file proves:

- [Behavior 1]
- [Behavior 2]

How to read the test:

- Setup objects.
- Call the function or repository.
- Assert returned values.

```python
test code here
```
```

## Example For Task 04 - Status Transition Policy

```text
## Purpose

Build the first real domain rule with TDD: which order status moves are allowed in Slice 1.

### Logic Brief

- What this task adds: `OrderStatus` and `StatusTransitionPolicy`.
- Why this exists: later status-event creation must reject invalid lifecycle moves.
- How the pieces connect: the policy receives a current status and requested next status, then checks the allowed transition map.
- What the tests prove: allowed moves return `true`; terminal or backwards moves return `false`.
- What this unlocks next: services can call this rule before accepting a new status event.
```

### Per-Code-Block Example For Task 04

```text
Create `OrderStatus.java`:

What this file does:

- Defines every order lifecycle status the app is allowed to use.

Why this code exists:

- The status transition policy should compare known enum values, not raw strings.

How to read the code:

- Each enum value is one allowed contract status.
- `DELIVERED` and `CANCELLED` are terminal statuses in later transition rules.

```java
package com.waypoint.partnersource.order.domain;

public enum OrderStatus {
    CREATED,
    CONFIRMED,
    PICKED_UP,
    IN_TRANSIT,
    OUT_FOR_DELIVERY,
    DELIVERY_ATTEMPTED,
    DELIVERED,
    CANCELLED
}
```

Create `StatusTransitionPolicy.java`:

What this file does:

- Encodes which status changes are allowed.

Why this code exists:

- Later, status-event creation must reject invalid lifecycle moves before mutating the order.

How to read the code:

- The map key is the current status.
- The set value contains the statuses allowed next.
- If the next status is not in the set, the transition is rejected.

```java
[exact policy code]
```
```

## Example For Task 06 - Seed Store And Repositories

```text
## Purpose

Create deterministic in-memory seed data and repository classes used by later services.

This turns the agreed seed tables into reusable objects without adding a database.

### Logic Brief

- What this task adds: seed data, mutable in-memory store, and repositories for orders, drivers, assignments, and status events.
- Why this exists: later services need stable data to query before any database is introduced.
- How the pieces connect: `SeedDataLoader` builds the records, `SeedDataStore` holds them, and repositories expose focused lookup methods.
- What the tests prove: known IDs return records, missing IDs return empty results, timelines are chronological, and `ASN-3004` is not active Slice 1 work.
- What this unlocks next: endpoints and services can read seeded orders, drivers, assignments, and timelines.
```

### Per-Code-Block Example For Task 06

```text
Create `SeedDataStore.java`:

What this file does:

- Holds all in-memory seed data maps.

Why this code exists:

- Repositories need one shared object to read and mutate during Slice 1.

How to read the code:

- `orders` maps `orderId` to `DeliveryOrder`.
- `drivers` maps `driverId` to `DeliveryDriver`.
- `assignments` maps `assignmentId` to `DeliveryAssignment`.
- `statusEventsByOrderId` maps each order to its timeline.

```java
[exact SeedDataStore code]
```

Create `SeedDataLoader.java`:

What this file does:

- Builds the deterministic fake dataset from the agreed spec.

Why this code exists:

- Slice 1 uses in-memory data instead of a database.

How to read the code:

- First it creates drivers.
- Then it creates orders.
- Then it creates assignments.
- Then it creates timeline events.
- Finally it returns one `SeedDataStore`.

```java
[exact SeedDataLoader code]
```

Create `InMemoryAssignmentRepository.java`:

What this file does:

- Provides assignment lookup methods.

Why this code exists:

- Later services need to find active driver work and order assignment history without touching the store directly.

How to read the code:

- `findById` finds one assignment.
- `findActiveByDriverId` returns only Slice 1 active work.
- `ACTIVE_SLICE_1_ASSIGNMENT_IDS` prevents reserved `ASN-3004` from appearing in active driver work.

```java
[exact repository code]
```
```

## Example For Endpoint Tasks

For endpoint tasks, use this shape:

```text
### Logic Brief

- What this task adds: one HTTP endpoint.
- Why this exists: this endpoint satisfies one acceptance scenario from the agreed contract.
- How the pieces connect: controller receives the request, service coordinates repositories and policies, DTO maps the response.
- What the tests prove: success shape, missing resource errors, invalid request handling, and contract field names.
- What this unlocks next: the next API behavior or the final manual checklist.
```

## Example For Final Gate Tasks

For final-gate tasks, use this shape:

```text
### Logic Brief

- What this task adds: no new feature code; it is a verification checkpoint.
- Why this exists: the implementation must prove it matches the Slice 1 contract before moving on.
- How the pieces connect: full tests, manual checks, build-sequence audits, and git diff review all confirm readiness.
- What the tests prove: the whole slice still works together.
- What this unlocks next: parity checks or the next implementation lane.
```

## Rollout Plan

Apply this in three passes.

1. Update the guide files:

```text
partner-source-springboot/build-sequence/TASK_STATUS_GUIDE.md
partner-source-fastapi/build-sequence/TASK_STATUS_GUIDE.md
```

Add a rule that every task's `## Purpose` should include a `### Logic Brief` block, and every major code block should include a short explanation before the code.

2. Update active/recent tasks first:

```text
04-status-transition-policy.md
05-assignment-authorization-policy.md
06-seed-store-and-repositories.md
07-health-endpoint.md
08-readiness-endpoint.md
09-order-status-lookup.md
```

These are the tasks most likely to be read while learning the architecture.

3. Update the remaining tasks:

```text
10-problem-detail-errors.md
11-order-timeline.md
12-driver-profile.md
13-driver-assignments.md
14-create-status-event.md
15-integration-tests.md
16-manual-http-checklist.md
17-final-gate.md
```

## Content Rules

Keep each `### Logic Brief` short.

Target length:

```text
5 bullets
1 line per bullet where possible
```

Do not duplicate the exact code explanation line by line.

The purpose is to explain the mental model before code, not to replace:

```text
Tests To Write First
File Map
Exact Code
Commands To Run
```

Per-code-block explanations should also stay short.

Target length:

```text
3 mini-parts
1-3 bullets each
```

Good:

```text
What this file does: stores deterministic seed maps.
Why this code exists: repositories need one shared in-memory data source.
How to read it: each map is keyed by the matching ID.
```

Too much:

```text
Line 1 imports Map.
Line 2 imports List.
Line 3 imports ConcurrentHashMap.
```

## Decision

Recommended decision:

```text
Keep the 12 top-level sections.
Add `### Logic Brief` inside `## Purpose` across every task file.
Add a short explanation before every major test/code block.
Update task-status guides to make this standard.
```
