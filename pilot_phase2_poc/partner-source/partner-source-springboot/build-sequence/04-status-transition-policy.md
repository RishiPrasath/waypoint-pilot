# 04 - Status Transition Policy

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Build the first real domain rule with TDD: which order status moves are allowed in Slice 1.

## Source Docs To Read

- `../../AGREED_SPEC.md` section `6. Status Transition Rules`
- `../../docs/active/contract-handoff.md`
- `../../docs/contracts/openapi/partner-source.v1.yaml`

## Prereqs

- Task 03 package layout exists.
- `order/domain` package exists.
- Keep this framework-free.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicyTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicyTest.java
```

Use this exact JUnit test file before implementation:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this exact JUnit test file before implementation.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.order.domain;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class StatusTransitionPolicyTest {

    private final StatusTransitionPolicy policy = new StatusTransitionPolicy();

    @Test
    void outForDeliveryCanTransitionToDelivered() {
        assertTrue(policy.canTransition(OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED));
    }

    @Test
    void deliveredCannotTransitionToOutForDelivery() {
        assertFalse(policy.canTransition(OrderStatus.DELIVERED, OrderStatus.OUT_FOR_DELIVERY));
    }

    @Test
    void confirmedCanTransitionToPickedUp() {
        assertTrue(policy.canTransition(OrderStatus.CONFIRMED, OrderStatus.PICKED_UP));
    }

    @Test
    void deliveryAttemptedCannotTransitionToOutForDelivery() {
        assertFalse(policy.canTransition(OrderStatus.DELIVERY_ATTEMPTED, OrderStatus.OUT_FOR_DELIVERY));
    }

    @Test
    void terminalStatusesHaveNoOutgoingTransitions() {
        assertFalse(policy.canTransition(OrderStatus.DELIVERED, OrderStatus.CANCELLED));
        assertFalse(policy.canTransition(OrderStatus.CANCELLED, OrderStatus.CREATED));
    }
}

```

Expected first result before implementation: compilation fails because `OrderStatus` or `StatusTransitionPolicy` does not exist.
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `src/main/java/com/waypoint/partnersource/order/domain/OrderStatus.java`, `src/main/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicy.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
src/main/java/com/waypoint/partnersource/order/domain/OrderStatus.java
src/main/java/com/waypoint/partnersource/order/domain/StatusTransitionPolicy.java
```

## Exact Code

Create `OrderStatus.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `OrderStatus.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

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

**Code Block Explanation**

- What this block does: Shows the exact Java code for `StatusTransitionPolicy.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.order.domain;

import java.util.EnumSet;
import java.util.Map;
import java.util.Set;

public class StatusTransitionPolicy {
    private static final Map<OrderStatus, Set<OrderStatus>> ALLOWED_TRANSITIONS = Map.of(
            OrderStatus.CREATED, EnumSet.of(OrderStatus.CONFIRMED, OrderStatus.CANCELLED),
            OrderStatus.CONFIRMED, EnumSet.of(OrderStatus.PICKED_UP, OrderStatus.CANCELLED),
            OrderStatus.PICKED_UP, EnumSet.of(OrderStatus.IN_TRANSIT),
            OrderStatus.IN_TRANSIT, EnumSet.of(OrderStatus.OUT_FOR_DELIVERY),
            OrderStatus.OUT_FOR_DELIVERY, EnumSet.of(OrderStatus.DELIVERED),
            OrderStatus.DELIVERY_ATTEMPTED, Set.of(),
            OrderStatus.DELIVERED, Set.of(),
            OrderStatus.CANCELLED, Set.of()
    );

    public boolean canTransition(OrderStatus currentStatus, OrderStatus nextStatus) {
        return ALLOWED_TRANSITIONS.getOrDefault(currentStatus, Set.of()).contains(nextStatus);
    }
}

```

Important: `CONFIRMED -> CANCELLED` is allowed by the agreed spec. `DELIVERY_ATTEMPTED` has no outgoing Slice 1 behavior.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd -Dtest=StatusTransitionPolicyTest test
.\mvnw.cmd test
```

## Done Criteria

- [x] Tests prove allowed and rejected transitions.
- [x] Policy has no Spring annotations.
- [x] `DELIVERY_ATTEMPTED` is not expanded into Slice 1 behavior.

## Common Mistakes

- Forgetting `CONFIRMED -> CANCELLED`.
- Adding Spring annotations to the domain policy.
- Adding controller or service code here.

## Stop / Do Not Add

- Do not add controllers or services.
- Do not add status-event mutation yet.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Exact code now reflects the full agreed transition table.
