package com.waypoint.partnersource.shared.security;

import com.waypoint.partnersource.assignment.domain.AssignmentAuthorizationPolicy;
import com.waypoint.partnersource.assignment.repository.InMemoryAssignmentRepository;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import org.springframework.stereotype.Component;

@Component
public class AccessPolicy {
    private final InMemoryOrderRepository orderRepository;
    private final InMemoryAssignmentRepository assignmentRepository;
    private final AssignmentAuthorizationPolicy assignmentAuthorizationPolicy;

    public AccessPolicy(
            InMemoryOrderRepository orderRepository,
            InMemoryAssignmentRepository assignmentRepository,
            AssignmentAuthorizationPolicy assignmentAuthorizationPolicy
    ) {
        this.orderRepository = orderRepository;
        this.assignmentRepository = assignmentRepository;
        this.assignmentAuthorizationPolicy = assignmentAuthorizationPolicy;
    }

    public boolean canReadDriverResource(AuthenticatedPrincipal principal, String driverId) {
        return principal.role() == ActorRole.DELIVERY_DRIVER
                && principal.actorType() == PrincipalActorType.DRIVER
                && principal.actorId().equals(driverId);
    }

    public boolean canReadOrder(AuthenticatedPrincipal principal, String orderId) {
        if (principal.role() == ActorRole.CUSTOMER_SERVICE_AGENT) {
            return true;
        }

        if (principal.role() != ActorRole.DELIVERY_DRIVER) {
            return false;
        }

        if (orderRepository.findById(orderId).isEmpty()) {
            return true;
        }

        return assignmentAuthorizationPolicy.canDriverUpdateOrder(
                principal.actorId(),
                orderId,
                assignmentRepository.findByOrderId(orderId)
        );
    }

    public boolean canCreateStatusEvent(AuthenticatedPrincipal principal) {
        return principal.role() == ActorRole.DELIVERY_DRIVER
                && principal.actorType() == PrincipalActorType.DRIVER;
    }

    public boolean canSubmitDriverId(AuthenticatedPrincipal principal, String driverId) {
        return principal.role() == ActorRole.DELIVERY_DRIVER
                && principal.actorType() == PrincipalActorType.DRIVER
                && principal.actorId().equals(driverId);
    }
}
