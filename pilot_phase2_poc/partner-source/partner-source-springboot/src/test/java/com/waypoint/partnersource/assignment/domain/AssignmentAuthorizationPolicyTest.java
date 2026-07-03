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
            new DeliveryAssignment(
                "ASN-3001",
                "ORD-1001",
                "DRV-2001",
                AssignmentStatus.ASSIGNED
            )
        );

        assertTrue(policy.canDriverUpdateOrder("DRV-2001", "ORD-1001", assignments));
    }

    @Test
    void drv2002CannotUpdateOrd1001() {
        Collection<DeliveryAssignment> assignments = List.of(
            new DeliveryAssignment(
                "ASN-3001",
                "ORD-1001",
                "DRV-2001",
                AssignmentStatus.ASSIGNED
            )
        );

        assertFalse(policy.canDriverUpdateOrder("DRV-2002", "ORD-1001", assignments));
    }

    @Test
    void drv2001CanReachDeliveredOrderInvalidTransitionPathForOrd1003ThroughCompletedAssignment() {
        Collection<DeliveryAssignment> assignments = List.of(
            new DeliveryAssignment(
                "ASN-3003",
                "ORD-1003",
                "DRV-2001",
                AssignmentStatus.COMPLETED
            )
        );

        assertTrue(policy.canDriverUpdateOrder("DRV-2001", "ORD-1003", assignments));
    }

    @Test
    void cancelledAssignmentDoesNotAuthorizeDriver() {
        Collection<DeliveryAssignment> assignments = List.of(
            new DeliveryAssignment(
                "ASN-3001",
                "ORD-1001",
                "DRV-2001",
                AssignmentStatus.CANCELLED
            )
        );

        assertFalse(policy.canDriverUpdateOrder("DRV-2001", "ORD-1001", assignments));
    }
}
