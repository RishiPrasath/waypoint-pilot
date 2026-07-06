# Partner Source Auth And Access-Control Plan

Status: draft for next implementation slice.

This plan promotes the queued access-control thinking from the wider Phase 2
planning notes into the local `partner-source` implementation lane.

It does not change Slice 1 retroactively. Slice 1 intentionally shipped without
real authentication. This plan defines the next auth/access-control slice before
BFF and frontend flows depend on protected Partner Source data.

## 1. Current State

Implemented today:

- Spring Boot and FastAPI expose the Slice 1 Partner Source API.
- Both implementations use deterministic in-memory seed data.
- Both implementations enforce assignment-based domain authorization through
  `ORDER_NOT_ASSIGNED_TO_DRIVER`.
- Both implementations return the shared ProblemDetail-style error envelope.
- Parity checks prove current Spring Boot and FastAPI response behavior.

Not implemented today:

- real authentication
- bearer/JWT validation
- Spring Security
- FastAPI security dependencies
- caller identity propagation from BFF
- `401 UNAUTHENTICATED`
- generic `403 ACCESS_DENIED`
- role/scope-based resource access

## 2. Decision Gates Before Code

Do not implement framework security until these decisions are accepted.

| Decision | Recommended default |
|---|---|
| Should Partner Source enforce auth, or only BFF? | Both. BFF authenticates/orchestrates, Partner Source still enforces final resource access. |
| Identity format | Demo bearer token that maps to claims: `sub`, `role`, `actorType`, `actorId`, `scopes`, `demoOrgId`, `channel`. |
| Token type for this slice | Static signed-token simulation or static bearer-token map, not a production IdP. |
| Login endpoint | Add a demo-only login endpoint that returns one of the deterministic bearer tokens. |
| Driver profile access | Driver can read own profile only. |
| Driver assignment access | Driver can read own assignments only. |
| Driver order status/timeline access | Driver can read assigned orders only. |
| Driver status-event write | Driver can write status events only for own assigned orders. |
| Customer-service read access | Customer-service agent can read support-safe order status and timeline for the demo org. |
| Customer-service write access | No driver status-event writes unless a support-correction workflow is explicitly accepted later. |
| Unauthorized resource access | Use `403 ACCESS_DENIED` for authenticated-but-not-allowed. Do not mask as `404` for this learning slice. |
| Existing domain denial | Keep `ORDER_NOT_ASSIGNED_TO_DRIVER` separate from `ACCESS_DENIED`. |
| Status-event `driverId` body field | Deprecate or remove after auth is accepted; derive driver identity from principal. |

## 3. Contract Changes

Update the shared contract before implementation:

1. Add bearer security scheme to OpenAPI.
2. Add operation-level security to protected `/api/v1/**` routes.
3. Add `POST /api/v1/auth/demo-login` as a demo-only public login endpoint.
4. Keep `/health` public.
5. Decide whether `/ready` is public or platform-only.
6. Add `401 UNAUTHENTICATED` response.
7. Add `403 ACCESS_DENIED` response.
8. Keep `403 ORDER_NOT_ASSIGNED_TO_DRIVER` for domain assignment denial.
9. Add examples for:
   - demo driver login
   - demo customer-service-agent login
   - unknown demo login identity
   - delivery driver own-resource success
   - delivery driver cross-resource denial
   - customer-service read success
   - customer-service write denial
   - missing token
   - invalid token
10. Decide status-event request shape:
   - preferred next shape: remove `driverId` from request body
   - compatibility option: keep `driverId` temporarily but reject spoofing when it does not match principal `actorId`

### Demo Login Contract Shape

Recommended request:

```http
POST /api/v1/auth/demo-login
Content-Type: application/json

{
  "actorType": "DRIVER",
  "actorId": "DRV-2001"
}
```

Recommended response:

```json
{
  "accessToken": "demo-driver-2001-token",
  "tokenType": "Bearer",
  "expiresIn": 3600,
  "principal": {
    "subject": "driver:DRV-2001",
    "role": "DELIVERY_DRIVER",
    "actorType": "DRIVER",
    "actorId": "DRV-2001",
    "scopes": [
      "driver:read:self",
      "assignment:read:self",
      "order:read:assigned",
      "status-event:create:assigned"
    ],
    "demoOrgId": "ORG-DEMO-1",
    "channel": "DRIVER_APP"
  }
}
```

Recommended customer-service-agent login request:

```http
POST /api/v1/auth/demo-login
Content-Type: application/json

{
  "actorType": "USER",
  "actorId": "CSA-5001"
}
```

Recommended negative cases:

| Scenario | Expected |
|---|---|
| Unknown `actorId` | `404 DRIVER_NOT_FOUND` for driver login, or agreed `404 USER_NOT_FOUND` if CSA users become seeded resources. |
| Unsupported `actorType` | `400 INVALID_REQUEST` |
| Missing required field | `400 INVALID_REQUEST` |

Decision still needed: whether customer-service agents are first-class seeded
resources in Partner Source, or whether the demo CSA token is a BFF/platform
identity stub. Do not implement CSA persistence until this is accepted.

## 4. Access-Control Matrix

This matrix is the implementation source for who can access which protected
Partner Source route.

For this auth slice, use two user types:

| User type | Role | Actor type | Example actor ID |
|---|---|---|---|
| Delivery driver | `DELIVERY_DRIVER` | `DRIVER` | `DRV-2001` |
| Customer service agent | `CUSTOMER_SERVICE_AGENT` | `USER` | `CSA-5001` |

### Route Access Rules

| Route or action | Delivery driver | Customer service agent | No or invalid token | Enforcement point |
|---|---|---|---|---|
| `POST /api/v1/auth/demo-login` | Allowed for seeded driver identity. | Allowed for accepted demo CSA identity. | Public endpoint. | Demo login service. |
| `GET /health` | Allowed without token. | Allowed without token. | `200` public. | No auth guard. |
| `GET /ready` | Pending decision: public or platform-only. | Pending decision: public or platform-only. | Pending decision. | Readiness route policy. |
| `GET /api/v1/drivers/{driverId}` | Allowed only when `{driverId}` equals principal `actorId`; otherwise `403 ACCESS_DENIED`. | Denied for direct driver profile lookup unless support workflow later accepts it; default `403 ACCESS_DENIED`. | `401 UNAUTHENTICATED`. | Route access policy. |
| `GET /api/v1/drivers/{driverId}/assignments` | Allowed only when `{driverId}` equals principal `actorId`; otherwise `403 ACCESS_DENIED`. | Denied for direct driver assignment lookup unless support workflow later accepts it; default `403 ACCESS_DENIED`. | `401 UNAUTHENTICATED`. | Route access policy. |
| `GET /api/v1/orders/{orderId}/status` | Allowed only for orders assigned to the principal driver; otherwise `403 ACCESS_DENIED`. | Allowed for support-safe order status inside demo org. | `401 UNAUTHENTICATED`. | Route access policy plus assignment lookup. |
| `GET /api/v1/orders/{orderId}/timeline` | Allowed only for orders assigned to the principal driver; otherwise `403 ACCESS_DENIED`. | Allowed for support-safe order timeline inside demo org. | `401 UNAUTHENTICATED`. | Route access policy plus assignment lookup. |
| `POST /api/v1/orders/{orderId}/status-events` | Allowed only for own assigned orders. If authenticated driver exists but assignment rule fails, return `403 ORDER_NOT_ASSIGNED_TO_DRIVER`. | Denied by default: `403 ACCESS_DENIED`. | `401 UNAUTHENTICATED`. | Route access policy, then domain assignment authorization, then transition policy. |
| Driver attempts to submit another driver's `driverId` while body field still exists | `403 ACCESS_DENIED`. | Not applicable; CSA write is denied. | `401 UNAUTHENTICATED`. | Route access policy before domain mutation. |

### Error Separation Rules

Use these rules consistently in Spring Boot, FastAPI, and parity checks:

| Situation | Error |
|---|---|
| Missing `Authorization` header on protected route | `401 UNAUTHENTICATED` |
| Invalid bearer token on protected route | `401 UNAUTHENTICATED` |
| Valid token, wrong role for route | `403 ACCESS_DENIED` |
| Valid driver token, trying to read another driver's route resource | `403 ACCESS_DENIED` |
| Valid driver token, trying to read an unassigned order | `403 ACCESS_DENIED` |
| Valid driver token, creating status event for an unassigned order | `403 ORDER_NOT_ASSIGNED_TO_DRIVER` |
| Valid driver token, invalid status transition on assigned order | `409 INVALID_STATUS_TRANSITION` |
| Valid token, malformed request body/query/path | `400 INVALID_REQUEST` |

### Why Read And Write Denials Differ

For reads, an unassigned order is a resource-access problem:

```text
Driver DRV-2002 should not read ORD-1001 status or timeline.
-> 403 ACCESS_DENIED
```

For writes, the existing domain rule is more specific:

```text
Driver DRV-2002 is real, but is not assigned to update ORD-1001.
-> 403 ORDER_NOT_ASSIGNED_TO_DRIVER
```

This preserves the Slice 1 domain behavior while adding real route-level access
control around it.

## 5. TDD Implementation Order

Use this order for both implementations. Spring Boot remains the reference
implementation; FastAPI follows for parity.

### Step 1 - Contract Red

Add failing contract/parity fixtures first.

Expected new error codes:

```text
UNAUTHENTICATED
ACCESS_DENIED
```

Expected protected-route behavior:

| Scenario | Expected |
|---|---|
| Demo driver login | `200`, returns `demo-driver-2001-token` |
| Demo customer-service-agent login | `200`, returns `demo-csa-5001-token` |
| Unsupported demo login identity | `400 INVALID_REQUEST` or accepted `404` identity error |
| Missing bearer token on protected route | `401 UNAUTHENTICATED` |
| Invalid bearer token on protected route | `401 UNAUTHENTICATED` |
| Driver reads own profile | `200` |
| Driver reads another driver profile | `403 ACCESS_DENIED` |
| Driver reads own assignments | `200` |
| Driver reads another driver's assignments | `403 ACCESS_DENIED` |
| Driver reads assigned order status | `200` |
| Driver reads unassigned order status | `403 ACCESS_DENIED` |
| Driver writes assigned order status event | `201` |
| Driver writes unassigned order status event | `403 ORDER_NOT_ASSIGNED_TO_DRIVER` |
| Driver spoofs a different `driverId` in body, if body field remains | `403 ACCESS_DENIED` |
| Customer-service agent reads order status | `200` |
| Customer-service agent writes driver status event | `403 ACCESS_DENIED` |
| `/health` without token | `200` |
| `/ready` without token | accept explicit decision before testing |

### Step 2 - Shared Identity Model And Demo Login

Define the same conceptual identity in both implementations:

```text
subject
role
actorType
actorId
scopes
demoOrgId
channel
```

Suggested demo identities:

| Token label | Role | Actor type | Actor ID | Purpose |
|---|---|---|---|---|
| `demo-driver-2001-token` | `DELIVERY_DRIVER` | `DRIVER` | `DRV-2001` | Main driver success path. |
| `demo-driver-2002-token` | `DELIVERY_DRIVER` | `DRIVER` | `DRV-2002` | Valid driver, unassigned denial path. |
| `demo-csa-5001-token` | `CUSTOMER_SERVICE_AGENT` | `USER` | `CSA-5001` | Support read path. |
| `invalid-token` | none | none | none | `401` negative path. |

For this learning slice, keep the token store in memory and deterministic.

Login should not create a real session. It simply exchanges a known demo
identity for a deterministic bearer token so frontend and parity tests can use
the same flow a real login would use later.

Example flow:

```text
POST /api/v1/auth/demo-login
-> returns accessToken

GET /api/v1/drivers/DRV-2001/assignments
Authorization: Bearer demo-driver-2001-token
-> returns DRV-2001 assignments
```

### Step 3 - Spring Boot TDD

Add tests first.

Suggested test files:

```text
partner-source-springboot/src/test/java/com/waypoint/partnersource/shared/security/DemoTokenAuthenticatorTest.java
partner-source-springboot/src/test/java/com/waypoint/partnersource/shared/security/AccessPolicyTest.java
partner-source-springboot/src/test/java/com/waypoint/partnersource/shared/security/SecurityFilterTest.java
partner-source-springboot/src/test/java/com/waypoint/partnersource/shared/security/AuthControllerTest.java
partner-source-springboot/src/test/java/com/waypoint/partnersource/order/api/OrderStatusAccessControlTest.java
partner-source-springboot/src/test/java/com/waypoint/partnersource/order/api/OrderTimelineAccessControlTest.java
partner-source-springboot/src/test/java/com/waypoint/partnersource/driver/api/DriverAccessControlTest.java
partner-source-springboot/src/test/java/com/waypoint/partnersource/order/api/StatusEventAccessControlTest.java
```

Suggested implementation files:

```text
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/AuthenticatedPrincipal.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/ActorRole.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/ActorType.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/DemoTokenAuthenticator.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/DemoLoginService.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/AuthController.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/dto/DemoLoginRequest.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/dto/DemoLoginResponse.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/AccessPolicy.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/AuthenticationFilter.java
partner-source-springboot/src/main/java/com/waypoint/partnersource/shared/security/CurrentPrincipal.java
```

Spring Boot implementation rule:

- Start with a small custom filter and plain Java policy unless Spring Security is explicitly accepted.
- If Spring Security is accepted, add it deliberately and keep the first config minimal.
- Keep domain assignment authorization separate from route/user access control.

### Step 4 - FastAPI TDD

Mirror the Spring Boot behavior after the Spring tests are green.

Suggested test files:

```text
partner-source-fastapi/tests/security/test_demo_token_authenticator.py
partner-source-fastapi/tests/security/test_access_policy.py
partner-source-fastapi/tests/api/test_demo_login_endpoint.py
partner-source-fastapi/tests/api/test_order_status_access_control.py
partner-source-fastapi/tests/api/test_order_timeline_access_control.py
partner-source-fastapi/tests/api/test_driver_access_control.py
partner-source-fastapi/tests/api/test_status_event_access_control.py
```

Suggested implementation files:

```text
partner-source-fastapi/app/security/principal.py
partner-source-fastapi/app/security/demo_tokens.py
partner-source-fastapi/app/security/authenticator.py
partner-source-fastapi/app/security/demo_login.py
partner-source-fastapi/app/security/access_policy.py
partner-source-fastapi/app/security/dependencies.py
partner-source-fastapi/app/api/auth.py
partner-source-fastapi/app/schemas/auth.py
```

FastAPI implementation rule:

- Use FastAPI dependencies for principal extraction and route guards.
- Keep token parsing deterministic and in-memory for the demo slice.
- Do not introduce OAuth provider integration, database sessions, or background auth refresh.

### Step 5 - Status-Event Principal Migration

Current Slice 1 request body includes `driverId`.

Auth slice should decide one of two paths:

| Path | Behavior |
|---|---|
| Remove `driverId` | `actorId` comes only from authenticated principal. Cleaner final design. |
| Keep temporarily | Request `driverId` must match principal `actorId`; mismatch returns `403 ACCESS_DENIED`. Easier compatibility step. |

Preferred: remove `driverId` from the new contract slice. If time is tight, keep
it temporarily with spoofing protection and mark removal as the next contract
cleanup.

## 6. Parity Checks

Expand the parity harness after both implementations pass their local tests.

Suggested new matrix group:

```text
AUTH-01 missing-token-order-status
AUTH-02 invalid-token-order-status
AUTH-03 driver-own-profile
AUTH-04 driver-other-profile-denied
AUTH-05 driver-own-assignments
AUTH-06 driver-other-assignments-denied
AUTH-07 driver-assigned-order-status
AUTH-08 driver-unassigned-order-status-denied
AUTH-09 driver-assigned-status-event
AUTH-10 driver-unassigned-status-event-domain-denial
AUTH-11 driver-spoofed-body-driver-denied
AUTH-12 csa-read-order-status
AUTH-13 csa-status-event-write-denied
AUTH-14 health-public
AUTH-15 ready-policy
AUTH-16 demo-driver-login
AUTH-17 demo-csa-login
AUTH-18 unsupported-demo-login
```

Parity assertions should compare:

- HTTP status code
- `errorCode`
- `status`
- `title`
- `correlationId` presence
- response body fields for successful reads
- event actor fields for successful writes
- no implementation-specific security fields leaking in errors

Auth headers should be part of the parity matrix:

```text
Authorization: Bearer demo-driver-2001-token
Authorization: Bearer demo-driver-2002-token
Authorization: Bearer demo-csa-5001-token
Authorization: Bearer invalid-token
```

## 7. Acceptance Gates

Spring Boot gate:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-springboot
.\mvnw.cmd test
```

FastAPI gate:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\partner-source-fastapi
python -m pytest
```

Parity gate:

```powershell
cd C:\Users\prasa\Documents\Github\waypoint-pilot\pilot_phase2_poc\partner-source\parity
python -m pytest
```

Final acceptance:

- Contract includes auth/security decisions.
- Spring Boot and FastAPI both implement the same auth behavior.
- Parity matrix passes for success and denial cases.
- Existing Slice 1 non-auth behavior remains green.
- `ORDER_NOT_ASSIGNED_TO_DRIVER` remains a domain error, not a generic auth error.
- `UNAUTHENTICATED` and `ACCESS_DENIED` use the shared ProblemDetail envelope.

## 8. Recommended Next Build Tasks

Create these numbered tasks only after the decisions in section 2 are accepted:

| Task | Purpose |
|---|---|
| 18 | Auth/access-control contract update. |
| 19 | Spring Boot demo principal and token authentication. |
| 20 | Spring Boot access policy and protected-route tests. |
| 21 | Spring Boot status-event principal migration. |
| 22 | FastAPI demo principal and token authentication. |
| 23 | FastAPI access policy and protected-route tests. |
| 24 | FastAPI status-event principal migration. |
| 25 | Auth parity matrix and final auth gate. |
