# Partner Source Build Progress Dashboard

This is the short progress dashboard. It is not an instruction source.

Use the numbered build books for instructions:

```text
partner-source-springboot\build-sequence\00-index.md
partner-source-fastapi\build-sequence\00-index.md
parity\build-sequence\00-index.md
```

Use the agreed implementation spec for behavior:

```text
AGREED_SPEC.md
```

## Master Sequence

- [x] Create shared implementation lane.
- [x] Create root README.
- [x] Create support-only AGENTS rules.
- [x] Create contract sync notes.
- [x] Create agreed local spec from Phase 2 handoff docs.
- [x] Archive old duplicate long-form manuals under `docs/archive/manuals/`.
- [x] Create numbered Spring Boot build sequence.
- [x] Create numbered FastAPI build sequence.
- [x] Create numbered parity build sequence.
- [ ] Human Step 0.1: open implementation lane.
- [ ] Human Step 0.2: read `AGREED_SPEC.md`.
- [ ] Human Step 0.3: check Java, Maven, Python, and Git.
- [ ] Human Step 1.1: create Spring Boot project.
- [ ] Human Step 1.2: run Spring Boot scaffold test.
- [ ] Human Step 1.3: create Spring Boot package folders.
- [ ] Human Step 2.1: add Spring Boot CI workflow.
- [ ] Human Step 2.2: verify Spring Boot CI.
- [ ] Human Step 3.1: create FastAPI project.
- [ ] Human Step 3.2: run FastAPI scaffold test.
- [ ] Human Step 4.1: add FastAPI CI workflow.
- [ ] Human Step 4.2: verify FastAPI CI.
- [ ] Human Phase 5: implement status transition policy in Spring Boot, then FastAPI.
- [ ] Human Phase 6: implement assignment authorization policy in Spring Boot, then FastAPI.
- [ ] Human Phase 7: implement seed store and in-memory repositories in Spring Boot, then FastAPI.
- [ ] Human Phase 8: implement `/health` in Spring Boot, then FastAPI.
- [ ] Human Phase 9: implement `/ready` in Spring Boot, then FastAPI.
- [ ] Human Phase 10: implement order status lookup in Spring Boot, then FastAPI.
- [ ] Human Phase 11: harden shared error envelope in Spring Boot, then FastAPI.
- [ ] Human Phase 12: implement order timeline in Spring Boot, then FastAPI.
- [ ] Human Phase 13: implement driver profile in Spring Boot, then FastAPI.
- [ ] Human Phase 14: implement driver assignments in Spring Boot, then FastAPI.
- [ ] Human Phase 15: implement create status event in Spring Boot, then FastAPI.
- [ ] Human Phase 16: run manual HTTP checklist against both implementations.
- [ ] Human Phase 17: add contract and parity checks.

## Per-Phase Rule

Every implementation phase follows:

```text
read AGREED_SPEC.md and the numbered task file
-> write failing test
-> implement smallest code
-> run focused test
-> run full module test
-> mark checkbox
```

## Build Schedule

### Thursday

- [ ] Read `AGREED_SPEC.md` and the Spring Boot build book.
- [ ] Finish project scaffold, package layout, and CI pipeline.
- [ ] Write and pass `StatusTransitionPolicyTest`.
- [ ] Start `AssignmentAuthorizationPolicyTest` if time remains.

### Friday

- [ ] Finish assignment authorization policy.
- [ ] Build the seed store and in-memory repositories.
- [ ] Lock in seeded data for orders, drivers, assignments, and timelines.
- [ ] Run focused tests, then full module tests.
- [ ] Resolve the `ORD-1003` invalid-transition fixture decision before moving on.

### Saturday

- [ ] Implement `/health`.
- [ ] Implement `/ready`.
- [ ] Implement `GET /api/v1/orders/{orderId}/status`.
- [ ] Add the shared `ProblemDetail`-style error handling.
- [ ] Run module tests and fix any contract mismatches.

### Sunday

- [ ] Implement `GET /api/v1/orders/{orderId}/timeline`.
- [ ] Implement `GET /api/v1/drivers/{driverId}`.
- [ ] Implement `GET /api/v1/drivers/{driverId}/assignments`.
- [ ] Implement `POST /api/v1/orders/{orderId}/status-events`.
- [ ] Finish integration tests.
- [ ] Run the manual HTTP checklist.
- [ ] Complete the final gate and cleanup.
