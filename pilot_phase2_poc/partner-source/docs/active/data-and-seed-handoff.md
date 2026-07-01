# Partner Source Data And Seed Handoff

This file summarizes the deterministic Slice 1 seed data that both Spring Boot and FastAPI must use.

## Seed Rule

Every seed record must support an endpoint, a domain rule, or a test. No filler data in Slice 1.

## Persistence

Use in-memory repositories for Slice 1.

H2 and PostgreSQL are deferred so the first implementation can focus on contract behavior, domain rules, tests, and CI/CD.

## Driver Seeds

| ID | Role |
|---|---|
| `DRV-2001` | Main active driver with two active assignments. |
| `DRV-2002` | Valid but unassigned/unavailable driver for authorization tests. |
| `DRV-2003` | Available driver with no assignments for empty-list tests. |
| `DRV-9999` | Missing-driver negative test ID. |

## Order Seeds

| ID | Current status | Purpose |
|---|---|---|
| `ORD-1001` | `OUT_FOR_DELIVERY` | Main happy-path delivery order. |
| `ORD-1002` | `IN_TRANSIT` | Second active assignment and in-transit example. |
| `ORD-1003` | `DELIVERED` | Delivered order for invalid transition tests. |
| `ORD-1004` | Planned Slice 2 fixture | Reserved for failed-attempt planning. Do not let it expand Slice 1. |
| `ORD-9999` | Not seeded | Missing-order negative test ID. |

## Assignment Seeds

| ID | Driver | Order | Status | Purpose |
|---|---|---|---|---|
| `ASN-3001` | `DRV-2001` | `ORD-1001` | `ASSIGNED` | Main active delivery job. |
| `ASN-3002` | `DRV-2001` | `ORD-1002` | `ASSIGNED` | Second active job. |
| `ASN-3003` | `DRV-2001` | `ORD-1003` | `COMPLETED` | Delivered-order history and invalid transition planning. |
| `ASN-3004` | `DRV-2001` | `ORD-1004` | `ASSIGNED` | Slice 2 failed-attempt planning. |

Implementation note: if the service checks active assignment before status transition, the invalid transition test needs either an active delivered-order fixture or a deliberate policy decision that completed assignments can still prove historical authorization for delivered-order validation. Keep both implementations aligned on the same choice.

## Timeline Seeds

| Order | Events | Purpose |
|---|---|---|
| `ORD-1001` | `EVT-4001` to `EVT-4005` | Main chronological timeline ending at `OUT_FOR_DELIVERY`. |
| `ORD-1002` | `EVT-4101` to `EVT-4104` | In-transit timeline. |
| `ORD-1003` | `EVT-4201` to `EVT-4203` | Delivered timeline for invalid transition scenarios. |

## Required Seed Scenarios

| Scenario | Seed data |
|---|---|
| Existing order status lookup | `ORD-1001` |
| Missing order | `ORD-9999` |
| Existing driver profile | `DRV-2001` |
| Missing driver | `DRV-9999` |
| Active driver assignment list | `DRV-2001`, `ASN-3001`, `ASN-3002` |
| Available driver with no work | `DRV-2003` |
| Assigned driver marks order delivered | `ORD-1001`, `DRV-2001`, `ASN-3001` |
| Unassigned driver cannot update order | `ORD-1001`, `DRV-2002` |
| Delivered order cannot move backward | `ORD-1003`, `DRV-2001`, `ASN-3003` or aligned replacement fixture |
| Timeline is chronological | `ORD-1001`, `EVT-4001` to `EVT-4005` |

