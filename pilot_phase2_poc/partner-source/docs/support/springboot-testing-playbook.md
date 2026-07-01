# Spring Boot Testing Playbook For Partner Source

## 1. Purpose

This document explains how to test the `partner-source` Spring Boot API.

It is beginner-friendly and focused on the API behaviors already planned:

- get order status
- get order timeline
- get driver profile
- list driver assignments
- create order status event
- reject invalid transitions
- reject unassigned driver updates

## 2. Testing Mental Model

Do not test the whole application with one giant test style.

Use the right test for the right layer:

```text
domain policy tests
-> seed/repository behavior tests
-> service tests
-> error handling tests
-> controller tests
-> small number of integration tests
-> contract checks
```

## 3. Test Types

| Test Type | Plain-English Meaning | Partner-Source Example |
|---|---|---|
| Unit test | Tests one small class by itself. | `StatusTransitionPolicyTest` |
| Service test | Tests business flow, often with mocked repositories. | `StatusEventServiceTest` |
| Controller/API test | Tests HTTP request/response behavior. | `OrderControllerTest` with `MockMvc` |
| Repository behavior test | Tests in-memory lookup, filtering, ordering, and save behavior. | `AssignmentRepositoryTest` |
| Integration test | Tests multiple layers together. | `PartnerSourceApiIntegrationTest` |

## 4. Testing Tools

| Tool | What It Does |
|---|---|
| JUnit 5 | Main Java testing framework. |
| Mockito | Lets tests fake dependencies. |
| MockMvc | Tests Spring MVC controllers without starting a full server. |
| `@WebMvcTest` | Loads only the web/controller layer. |
| Plain JUnit repository tests | Tests Slice 1 in-memory repositories. |
| `@DataJpaTest` | Later JPA-only test slice after persistence is introduced. |
| `@SpringBootTest` | Loads the full Spring Boot application context. |

## 5. Arrange, Act, Assert

Use this structure:

```text
Arrange: prepare input, test data, and mocks
Act: call the method or endpoint
Assert: check the result
```

Example:

```java
@Test
void getOrderStatus_existingOrder_returnsStatus() {
    String orderId = "ORD-1001";

    OrderStatusResponse response = service.getOrderStatus(orderId);

    assertEquals("ORD-1001", response.orderId());
    assertEquals(OrderStatus.OUT_FOR_DELIVERY, response.currentStatus());
}
```

## 6. Domain Policy Tests

Start with domain policy tests because they lock the most important rules.

Recommended tests:

| Test | Why |
|---|---|
| `StatusTransitionPolicyTest` | Proves valid and invalid status changes. |
| `AssignmentAuthorizationPolicyTest` | Proves only assigned drivers can update orders. |

Example scenarios:

```text
OUT_FOR_DELIVERY -> DELIVERED = allowed
DELIVERED -> OUT_FOR_DELIVERY = rejected
DRV-2001 assigned to ORD-1001 = can update
DRV-2002 not assigned to ORD-1001 = cannot update
```

## 7. Service Tests

Service tests prove business behavior without needing a real HTTP request.

Recommended service tests:

| Service Test | Behavior |
|---|---|
| `OrderStatusServiceTest` | Existing order returns status. |
| `OrderStatusServiceTest` | Missing order throws not found. |
| `DriverAssignmentServiceTest` | Driver gets active assignments. |
| `StatusEventServiceTest` | Assigned driver creates valid status event. |
| `StatusEventServiceTest` | Invalid transition is rejected. |
| `StatusEventServiceTest` | Unassigned driver is rejected. |

Use Mockito when a service depends on repositories.

## 8. Controller Tests With MockMvc

Controller tests prove the HTTP contract.

Use them to check:

- endpoint path
- HTTP method
- status code
- request body validation
- response JSON shape
- error response shape

Example:

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private OrderStatusService orderStatusService;

    @Test
    void getOrderStatus_existingOrder_returns200() throws Exception {
        when(orderStatusService.getOrderStatus("ORD-1001"))
            .thenReturn(TestFixtures.orderStatusResponse());

        mockMvc.perform(get("/api/v1/orders/ORD-1001/status"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.orderId").value("ORD-1001"))
            .andExpect(jsonPath("$.currentStatus").value("OUT_FOR_DELIVERY"));
    }
}
```

## 9. Repository Tests

Repository behavior tests prove lookup, filtering, ordering, and save behavior.

For Slice 1, use plain JUnit tests against in-memory repository implementations for:

- finding order by ID
- finding driver by ID
- listing assignments by driver
- ordering timeline events by `occurredAt`
- saving status events

Use `@DataJpaTest` later only when JPA/H2/PostgreSQL persistence is introduced.

## 10. Integration Tests

Use a small number of full integration tests.

These prove that the app wiring works:

```text
Controller
-> Service
-> Repository
-> Seed data
-> Response
```

Recommended integration tests:

| Test | Expected Result |
|---|---|
| Seeded order status returns `ORD-1001`. | `200 OK` |
| Seeded driver assignments return active assignments. | `200 OK` |
| Valid status event updates order status. | `201 Created` |
| Invalid transition returns problem detail. | `409 INVALID_STATUS_TRANSITION` |

## 11. Test Fixture Strategy

Fixtures are reusable test data.

Recommended support classes:

```text
OrderFixtures
DriverFixtures
AssignmentFixtures
StatusEventFixtures
ApiRequestFixtures
```

Keep fixtures boring and explicit.

They should match:

- [seed-data-detail.md](seed-data-detail.md)
- [domain-model-detail.md](domain-model-detail.md)
- [../contracts/openapi/partner-source.v1.yaml](../contracts/openapi/partner-source.v1.yaml)

## 12. Partner-Source Test Matrix

| Use Case | Endpoint | Test Type | Expected Result |
|---|---|---|---|
| Get current order status | `GET /api/v1/orders/{orderId}/status` | Controller + integration | `200 OK` |
| Missing order | `GET /api/v1/orders/ORD-9999/status` | Controller + service | `404 ORDER_NOT_FOUND` |
| Get driver | `GET /api/v1/drivers/{driverId}` | Controller + service | `200 OK` |
| Missing driver | `GET /api/v1/drivers/DRV-9999` | Controller + service | `404 DRIVER_NOT_FOUND` |
| Get assignments | `GET /api/v1/drivers/{driverId}/assignments` | Controller + repository | `200 OK` |
| Driver with no work | `GET /api/v1/drivers/DRV-2003/assignments` | Controller + integration | `200 OK`, empty `items` |
| Create status event | `POST /api/v1/orders/{orderId}/status-events` | Controller + service + integration | `201 Created` |
| Invalid transition | Delivered order moved backward | Service + controller | `409 INVALID_STATUS_TRANSITION` |
| Unassigned driver update | Wrong driver updates assigned order | Service + controller | `403 ORDER_NOT_ASSIGNED_TO_DRIVER` |
| Timeline ordering | `GET /api/v1/orders/{orderId}/timeline` | Repository + integration | Events ordered by `occurredAt` |

## 13. Recommended First Tests

Write tests in this order:

| Order | Test | Why |
|---|---|---|
| 1 | `StatusTransitionPolicyTest` | Locks the status lifecycle. |
| 2 | `AssignmentAuthorizationPolicyTest` | Prevents wrong driver updates. |
| 3 | `AssignmentRepositoryTest` | Proves active assignment queries over seed data. |
| 4 | `OrderRepositoryTest` | Proves order lookup and timeline ordering. |
| 5 | `OrderStatusServiceTest` | Proves status lookup and missing order handling. |
| 6 | `StatusEventServiceTest` | Proves valid and invalid status updates. |
| 7 | ProblemDetail/error mapping tests | Proves canonical error shape. |
| 8 | `OrderControllerTest` | Proves HTTP contract for status lookup. |
| 9 | `StatusEventControllerTest` | Proves request validation and response shape. |
| 10 | `PartnerSourceApiIntegrationTest` | Proves seed data and full app wiring. |

## 14. TDD Strategy

Use TDD at the behavior level.

Flow:

```text
pick one API behavior
-> write the domain policy test when the behavior has a rule
-> write the seed/repository behavior test when lookup or save behavior is involved
-> write the service test for the use case
-> write the error mapping test when the behavior can fail
-> write the controller test from OpenAPI
-> implement minimum code
-> run tests
-> refactor after green
```

Example behavior:

```text
driver creates status event for assigned order

Test 1: policy allows OUT_FOR_DELIVERY -> DELIVERED
Test 2: repository finds assignment and appends event
Test 3: service accepts assigned driver and rejects unassigned driver
Test 4: error mapping returns the canonical ProblemDetail when rejected
Test 5: controller accepts valid request JSON
Test 6: integration test proves full request path
```

## 15. What Not To Test

Do not waste time testing:

- generated getters and setters
- simple DTO constructors
- Spring framework internals
- every single JSON field in every test
- private methods directly
- JPA built-in behavior unless the query or relationship is yours

Test behavior and contract.

## 16. Source Links

- [Spring Boot - Testing Spring Boot Applications](https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html)
- [Spring Boot - Test Slices](https://docs.spring.io/spring-boot/appendix/test-auto-configuration/slices.html)
- [Spring Framework - MockMvc](https://docs.spring.io/spring-framework/reference/testing/mockmvc.html)
- [Spring Boot `@WebMvcTest` API Docs](https://docs.spring.io/spring-boot/3.5/api/java/org/springframework/boot/test/autoconfigure/web/servlet/WebMvcTest.html)
- [JUnit 5 User Guide](https://docs.junit.org/5.10.2/user-guide/index.html)
- [Mockito](https://site.mockito.org/)
- [Mockito Javadoc](https://javadoc.io/doc/org.mockito/mockito-core/latest/org.mockito/org/mockito/Mockito.html)
