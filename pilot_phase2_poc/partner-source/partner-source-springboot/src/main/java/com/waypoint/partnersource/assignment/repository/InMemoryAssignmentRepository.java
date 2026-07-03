package com.waypoint.partnersource.assignment.repository;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.assignment.domain.DeliveryAssignment;
import com.waypoint.partnersource.shared.seed.SeedDataStore;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import org.springframework.stereotype.Repository;

@Repository
public class InMemoryAssignmentRepository {
    private static final Set<String> ACTIVE_SLICE_1_ASSIGNMENT_IDS = Set.of("ASN-3001", "ASN-3002");

    private final SeedDataStore store;

    public InMemoryAssignmentRepository(SeedDataStore store) {
        this.store = store;
    }

    public Optional<DeliveryAssignment> findById(String assignmentId) {
        return Optional.ofNullable(store.assignments().get(assignmentId));
    }

    public List<DeliveryAssignment> findActiveByDriverId(String driverId) {
        return store.assignments().values().stream()
            .filter(assignment -> assignment.driverId().equals(driverId))
            .filter(assignment -> ACTIVE_SLICE_1_ASSIGNMENT_IDS.contains(assignment.assignmentId()))
            .filter(assignment -> assignment.status() == AssignmentStatus.ASSIGNED
                || assignment.status() == AssignmentStatus.ACCEPTED)
            .sorted(InMemoryAssignmentRepository::compareByAssignmentId)
            .toList();
    }

    public List<DeliveryAssignment> findByOrderId(String orderId) {
        return store.assignments().values().stream()
            .filter(assignment -> assignment.orderId().equals(orderId))
            .sorted(InMemoryAssignmentRepository::compareByAssignmentId)
            .toList();
    }

    public List<DeliveryAssignment> findAll() {
        return store.assignments().values().stream()
            .sorted(InMemoryAssignmentRepository::compareByAssignmentId)
            .toList();
    }

    private static int compareByAssignmentId(DeliveryAssignment left, DeliveryAssignment right) {
        return left.assignmentId().compareTo(right.assignmentId());
    }
}
