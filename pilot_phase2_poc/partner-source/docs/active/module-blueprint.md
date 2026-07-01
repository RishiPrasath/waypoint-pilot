# Partner Source Module Blueprint

This is the beginner-friendly handoff for the Partner Source module.

## What Partner Source Is

`partner-source` is a synthetic logistics partner API. It gives Waypoint stable demo data for orders, drivers, assignments, and status events without connecting to a real logistics company.

The module exists so later systems can ask practical questions such as:

- Where is my order?
- When will it arrive?
- Who is delivering it?
- What happened to my shipment?
- What orders are assigned to this driver?
- Can this driver mark this order as delivered?

## Slice 1 Goal

Expose a small, stable API that proves the core delivery-status loop:

```text
seeded order
  -> assigned driver
  -> current status lookup
  -> timeline lookup
  -> driver assignment lookup
  -> driver creates a valid status event
```

## Endpoints In Scope

```text
GET  /api/v1/orders/{orderId}/status
GET  /api/v1/orders/{orderId}/timeline
GET  /api/v1/drivers/{driverId}
GET  /api/v1/drivers/{driverId}/assignments
POST /api/v1/orders/{orderId}/status-events
GET  /health
GET  /ready
```

## Deferred From Slice 1

- PostgreSQL and H2.
- Spring Boot Actuator.
- Real authentication.
- Delivery attempts endpoint.
- Support summary endpoint.
- Exceptions endpoint.
- Available actions endpoint.
- Delivery view endpoint.
- Assignment creation endpoint.
- Driver availability update endpoint.
- BFF-specific shaping.

## Domain Objects

| Object | Role |
|---|---|
| `DeliveryOrder` | Owns stable order facts and current operational state. |
| `DeliveryDriver` | Owns seeded driver profile and availability for demo flows. |
| `DeliveryAssignment` | Links a driver to an order and proves who may update an order. |
| `OrderStatusEvent` | Append-only event that records status changes and powers the timeline. |
| `LocationSnapshot` | Lightweight location detail for status and timeline views. |
| `DeliveryWindow` | Planned delivery time range. |
| `StatusTransitionPolicy` | Decides whether a status move is allowed. |
| `AssignmentAuthorizationPolicy` | Decides whether a driver can update an order. |

## Frozen Status Transition Rules

| Current status | Allowed next status |
|---|---|
| `CREATED` | `CONFIRMED`, `CANCELLED` |
| `CONFIRMED` | `PICKED_UP`, `CANCELLED` |
| `PICKED_UP` | `IN_TRANSIT` |
| `IN_TRANSIT` | `OUT_FOR_DELIVERY` |
| `OUT_FOR_DELIVERY` | `DELIVERED` |
| `DELIVERY_ATTEMPTED` | none in Slice 1 |
| `DELIVERED` | none |
| `CANCELLED` | none |

`DELIVERY_ATTEMPTED` can remain in the enum for future compatibility, but Slice 1 should not create new delivery-attempt behavior.

## Governing Sources

- Contract handoff: `contract-handoff.md`
- Seed handoff: `data-and-seed-handoff.md`
- Test handoff: `test-and-acceptance-handoff.md`
- Design freeze archive source: `../archive/slice-1-design-freeze.md`
- Final audit archive source: `../archive/audits/final-plan-audit-report.md`
- ADRs: `../../99-decisions/`
