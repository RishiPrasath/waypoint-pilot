# Shared Error Contract

## 1. Purpose

This document defines the shared API error response shape for Phase 2 services.

The shared error contract is the portability boundary for failures. The BFF, `partner-source`, `rag-db`, and future services should use the same error envelope so client applications can handle failures predictably.

## 2. Canonical Error Envelope

Use a `ProblemDetail`-style response.

```json
{
  "type": "https://waypoint.local/problems/order-not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "No order exists for orderId ORD-9999.",
  "instance": "/api/v1/orders/ORD-9999/status",
  "errorCode": "ORDER_NOT_FOUND",
  "correlationId": "req-123"
}
```

## 3. Required Fields

| Field | Type | Required | Purpose |
|---|---|---:|---|
| `type` | string URI | Yes | Stable problem type identifier. |
| `title` | string | Yes | Short human-readable error title. |
| `status` | integer | Yes | HTTP status code repeated in the response body. |
| `detail` | string | Yes | Specific human-readable explanation. |
| `instance` | string | Yes | Request path or instance where the error occurred. |
| `errorCode` | string | Yes | Stable application-level error code for clients and tests. |
| `correlationId` | string | Yes | Request correlation ID for debugging and logs. |

## 4. Naming Rules

| Rule | Decision |
|---|---|
| Request trace field | Use `correlationId`. Do not use `requestId` unless the whole contract is deliberately renamed later. |
| Validation failure | Use `INVALID_REQUEST` for malformed path/query/body shape. Use a domain-specific code for semantic failures. |
| Missing or invalid bearer token | Use `UNAUTHENTICATED`. Do not expose whether a submitted token almost matched a known credential. |
| Authenticated but not allowed | Use `ACCESS_DENIED` for role, ownership, or route-level authorization failures. |
| Status transition failure | Use `INVALID_STATUS_TRANSITION`. Do not use `ORDER_TRANSITION_INVALID`. |
| Media type | Prefer `application/problem+json` for error responses. |
| Unknown server failure | Use `INTERNAL_SERVER_ERROR`. Do not expose stack traces or internal implementation details. |

## 5. Partner Source Slice 1 Error Codes

| Error Code | HTTP Status | Owner | When To Use |
|---|---:|---|---|
| `UNAUTHENTICATED` | `401` | shared | Protected route was called without a valid bearer token. |
| `ACCESS_DENIED` | `403` | shared | Authenticated principal is not allowed to access the resource or action. |
| `INVALID_REQUEST` | `400` | shared | Request syntax, path parameter, query parameter, or JSON shape is invalid. |
| `ORDER_NOT_FOUND` | `404` | partner-source | No order exists for the requested `orderId`. |
| `DRIVER_NOT_FOUND` | `404` | partner-source | No driver exists for the requested `driverId`. |
| `ASSIGNMENT_NOT_FOUND` | `404` | partner-source | A required assignment record does not exist. |
| `ORDER_NOT_ASSIGNED_TO_DRIVER` | `403` | partner-source | Driver exists but is not assigned to the order they are trying to update. |
| `INVALID_STATUS_TRANSITION` | `409` | partner-source | Requested order status transition violates lifecycle rules. |
| `INVALID_STATUS_EVENT` | `422` | partner-source | Status event body is syntactically valid but semantically invalid. |
| `INTERNAL_SERVER_ERROR` | `500` | shared | Unexpected server failure. |

## 6. Validation Taxonomy

Use these rules to decide between `400`, `409`, and `422`.

| Case | HTTP Status | Error Code | Layer That Should Catch It | Examples |
|---|---:|---|---|---|
| Caller is missing valid authentication | `401` | `UNAUTHENTICATED` | Auth filter/dependency | missing `Authorization` header, invalid bearer token |
| Caller is authenticated but forbidden | `403` | `ACCESS_DENIED` | Access policy/route guard | driver reads another driver's resource, customer-service user attempts a driver write |
| Request shape is invalid | `400` | `INVALID_REQUEST` | Controller/request validation | malformed JSON, unknown field, missing required field, invalid path ID format, invalid query parameter, invalid enum value, invalid date-time format |
| Request shape is valid, but the order lifecycle rejects the move | `409` | `INVALID_STATUS_TRANSITION` | Domain policy | `DELIVERED -> OUT_FOR_DELIVERY`, `CANCELLED -> IN_TRANSIT` |
| Request shape is valid, but the status event meaning is invalid | `422` | `INVALID_STATUS_EVENT` | Service/domain validation | `occurredAt` is far in the future, delivery-event business details fail a Slice 1 semantic rule |

Beginner rule:

```text
400 = the API cannot trust the request shape
409 = the requested status move conflicts with the order lifecycle
422 = the request shape is valid, but the event meaning is unacceptable
```

## 7. Planned Cross-Service Error Codes

These codes are not all required for `partner-source` Slice 1, but they should use the same envelope.

| Error Code | Suggested HTTP Status | Owner | When To Use |
|---|---:|---|---|
| `RAG_NO_SUPPORTING_CONTEXT` | `422` | rag-db | Retrieval cannot find sufficient source context to answer safely. |
| `RAG_UNSAFE_INPUT` | `400` | rag-db | Query guardrails reject malicious or unsafe input. |
| `RAG_UNSAFE_OUTPUT` | `422` | rag-db | Output validation rejects unsafe or unsupported model output. |
| `DOWNSTREAM_TIMEOUT` | `504` | bff | BFF dependency call times out. |
| `DOWNSTREAM_UNAVAILABLE` | `503` | bff | BFF dependency is unavailable. |

## 8. Example Responses

### 8.1 Missing Order

```json
{
  "type": "https://waypoint.local/problems/order-not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "No order exists for orderId ORD-9999.",
  "instance": "/api/v1/orders/ORD-9999/status",
  "errorCode": "ORDER_NOT_FOUND",
  "correlationId": "req-123"
}
```

### 8.2 Unauthenticated

```json
{
  "type": "https://waypoint.local/problems/unauthenticated",
  "title": "Unauthenticated",
  "status": 401,
  "detail": "Missing or invalid bearer token.",
  "instance": "/api/v1/orders/ORD-1001/status",
  "errorCode": "UNAUTHENTICATED",
  "correlationId": "req-123"
}
```

### 8.3 Access Denied

```json
{
  "type": "https://waypoint.local/problems/access-denied",
  "title": "Access denied",
  "status": 403,
  "detail": "Caller cannot access this resource.",
  "instance": "/api/v1/orders/ORD-1001/status",
  "errorCode": "ACCESS_DENIED",
  "correlationId": "req-123"
}
```

### 8.4 Missing Driver

```json
{
  "type": "https://waypoint.local/problems/driver-not-found",
  "title": "Driver not found",
  "status": 404,
  "detail": "No driver exists for driverId DRV-9999.",
  "instance": "/api/v1/drivers/DRV-9999",
  "errorCode": "DRIVER_NOT_FOUND",
  "correlationId": "req-123"
}
```

### 8.5 Order Not Assigned To Driver

```json
{
  "type": "https://waypoint.local/problems/order-not-assigned-to-driver",
  "title": "Order not assigned to driver",
  "status": 403,
  "detail": "Driver DRV-2002 is not assigned to order ORD-1001.",
  "instance": "/api/v1/orders/ORD-1001/status-events",
  "errorCode": "ORDER_NOT_ASSIGNED_TO_DRIVER",
  "correlationId": "req-123"
}
```

### 8.6 Invalid Status Transition

```json
{
  "type": "https://waypoint.local/problems/invalid-status-transition",
  "title": "Invalid status transition",
  "status": 409,
  "detail": "Cannot transition order ORD-1003 from DELIVERED to OUT_FOR_DELIVERY.",
  "instance": "/api/v1/orders/ORD-1003/status-events",
  "errorCode": "INVALID_STATUS_TRANSITION",
  "correlationId": "req-123"
}
```

### 8.7 Invalid Status Event

```json
{
  "type": "https://waypoint.local/problems/invalid-status-event",
  "title": "Invalid status event",
  "status": 422,
  "detail": "Status event is semantically invalid.",
  "instance": "/api/v1/orders/ORD-1001/status-events",
  "errorCode": "INVALID_STATUS_EVENT",
  "correlationId": "req-123"
}
```

## 9. Implementation Notes

### Spring Boot

Use centralized exception handling:

```text
@RestControllerAdvice
-> @ExceptionHandler
-> ProblemDetail-compatible response body
```

The Spring Boot implementation should map domain exceptions to the error codes in this document.

### FastAPI

When the FastAPI equivalent is built as a contract-parity implementation, it should return the same envelope and `errorCode` values.

The BFF should not need to know whether the upstream implementation is Spring Boot or FastAPI.

## 10. Contract Tests

Contract tests should verify:

- every error response includes all required fields
- HTTP status matches the `status` field
- `errorCode` uses an approved value
- `correlationId` is present
- deprecated codes such as `ORDER_TRANSITION_INVALID` are not returned
- the OpenAPI `ProblemDetail` schema matches this document
