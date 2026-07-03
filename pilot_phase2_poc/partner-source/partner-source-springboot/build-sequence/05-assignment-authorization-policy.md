# 05 - Assignment Authorization Policy

## Status

- Status: Done
- Last Updated: 2026-07-03

## Purpose

Build the domain rule that decides whether a driver may create a status event for an order.

## Source Docs To Read

- `../../AGREED_SPEC.md` sections `7. Seed Data` and `10. Acceptance Scenarios`
- `../../docs/active/data-and-seed-handoff.md`
- `../../docs/active/test-and-acceptance-handoff.md`

## Prereqs

- Task 04 is complete.
- `assignment/domain` package exists.
- Keep this as domain-only code.

## Tests To Write First

Create:

**Test Block Explanation**

- What this block does: Lists the test file paths, expected failures, or test setup for `src/test/java/com/waypoint/partnersource/assignment/domain/AssignmentAuthorizationPolicyTest.java`.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Treat each line as an exact test path or expected first failure, not as a suggestion to rename.

```text
src/test/java/com/waypoint/partnersource/assignment/domain/AssignmentAuthorizationPolicyTest.java
```

Use this exact JUnit test file before implementation:

**Test Block Explanation**

- What this block does: Shows the test code to write first for Use this exact JUnit test file before implementation.
- Why it exists: It makes the expected behavior executable before implementation, so the task stays test-first.
- How to read it: Read each test as arrange, act, assert: setup objects, call the behavior, then check the promised result.

```java
package com.waypoint.partnersource.assignment.domain;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Collection;
import java.util.List;

import org.junit.jupiter.api.Test;

class AssignmentAuthorizationPolicyTest {

    private final AssignmentAuthorizationPolicy policy = new AssignmentAuthorizationPolicy();

    @Test
    void drv2001CanUpdateOrd1001ThroughAsn3001() {
        Collection<DeliveryAssignment> assignments = List.of(
                new DeliveryAssignment("ASN-3001", "ORD-1001", "DRV-2001", AssignmentStatus.ASSIGNED)
        );

        assertTrue(policy.canDriverUpdateOrder("DRV-2001", "ORD-1001", assignments));
    }

    @Test
    void drv2002CannotUpdateOrd1001() {
        Collection<DeliveryAssignment> assignments = List.of(
                new DeliveryAssignment("ASN-3001", "ORD-1001", "DRV-2001", AssignmentStatus.ASSIGNED)
        );

        assertFalse(policy.canDriverUpdateOrder("DRV-2002", "ORD-1001", assignments));
    }

    @Test
    void drv2001CanReachDeliveredOrderInvalidTransitionPathForOrd1003ThroughCompletedAssignment() {
        Collection<DeliveryAssignment> assignments = List.of(
                new DeliveryAssignment("ASN-3003", "ORD-1003", "DRV-2001", AssignmentStatus.COMPLETED)
        );

        assertTrue(policy.canDriverUpdateOrder("DRV-2001", "ORD-1003", assignments));
    }

    @Test
    void cancelledAssignmentDoesNotAuthorizeDriver() {
        Collection<DeliveryAssignment> assignments = List.of(
                new DeliveryAssignment("ASN-3001", "ORD-1001", "DRV-2001", AssignmentStatus.CANCELLED)
        );

        assertFalse(policy.canDriverUpdateOrder("DRV-2001", "ORD-1001", assignments));
    }
}

```
## File Map

Create:

**Block Explanation**

- What this block does: Lists the exact files, folders, or package targets for `src/main/java/com/waypoint/partnersource/assignment/domain/AssignmentStatus.java`, `src/main/java/com/waypoint/partnersource/assignment/domain/DeliveryAssignment.java`.
- Why it exists: It removes folder and package ambiguity, which is the main thing that slows agents and humans down.
- How to read it: Treat each line as exact project structure, expected output, or rule text unless the task says otherwise.

```text
src/main/java/com/waypoint/partnersource/assignment/domain/AssignmentStatus.java
src/main/java/com/waypoint/partnersource/assignment/domain/DeliveryAssignment.java
src/main/java/com/waypoint/partnersource/assignment/domain/AssignmentAuthorizationPolicy.java
```

## Exact Code

Create `AssignmentStatus.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `AssignmentStatus.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.assignment.domain;

public enum AssignmentStatus {
    ASSIGNED,
    ACCEPTED,
    COMPLETED,
    CANCELLED
}

```

Create `DeliveryAssignment.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `DeliveryAssignment.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.assignment.domain;

public record DeliveryAssignment(
        String assignmentId,
        String orderId,
        String driverId,
        AssignmentStatus status
) {
}

```

Create `AssignmentAuthorizationPolicy.java`:

**Code Block Explanation**

- What this block does: Shows the exact Java code for `AssignmentAuthorizationPolicy.java`.
- Why it exists: It gives the concrete implementation target while keeping the slice inside the approved contract boundaries.
- How to read it: Read top-down: package, imports, class or record declaration, then the methods and assertions.

```java
package com.waypoint.partnersource.assignment.domain;

import java.util.Collection;
import java.util.EnumSet;
import java.util.Set;

public final class AssignmentAuthorizationPolicy {
    private static final Set<AssignmentStatus> AUTHORIZING_STATUSES = EnumSet.of(
            AssignmentStatus.ASSIGNED,
            AssignmentStatus.ACCEPTED,
            AssignmentStatus.COMPLETED
    );

    public boolean canDriverUpdateOrder(String driverId, String orderId, Collection<DeliveryAssignment> assignments) {
        return assignments.stream().anyMatch(assignment ->
                assignment.driverId().equals(driverId)
                        && assignment.orderId().equals(orderId)
                        && AUTHORIZING_STATUSES.contains(assignment.status())
        );
    }
}

```

Why `COMPLETED` is included: `ORD-1003` must reach the invalid-transition rule later and return `409 INVALID_STATUS_TRANSITION`, not fail early as `403`.

Why `CANCELLED` is excluded: a cancelled assignment is not valid proof that the driver may update the order.

## Commands To Run

**Command Block Explanation**

- What this block does: Shows the exact PowerShell commands for Commands To Run.
- Why it exists: It gives the verification path for this task without making the reader guess the right shell or module folder.
- How to read it: Run the lines in order from the folder named by the task, and keep them in PowerShell syntax.

```powershell
.\mvnw.cmd -Dtest=AssignmentAuthorizationPolicyTest test
.\mvnw.cmd test
```

## Done Criteria

- [x] Authorization tests pass.
- [x] No HTTP or repository code is required.
- [x] The `ORD-1003` edge case is documented in the test name.

## Common Mistakes

- Forgetting `ACCEPTED` from the agreed enum.
- Treating `COMPLETED` as unauthorized for `ORD-1003`.
- Treating `CANCELLED` as authorized.

## Stop / Do Not Add

- Do not create status events yet.
- Do not add security/authentication.
- Do not add repositories in this task.

## Change Notes

- Added per-code-block explanation wrappers so every fenced block states what it does, why it exists, and how to read it.
- Template normalized to the shared build-task format.
- Exact Java code now includes all agreed assignment statuses.
