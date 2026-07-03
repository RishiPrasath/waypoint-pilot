package com.waypoint.partnersource.assignment.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class InMemoryAssignmentRepositoryTest {

    @Test
    void findsActiveAssignmentsForDriver() {
        var repository = new InMemoryAssignmentRepository(SeedDataLoader.load());

        var assignments = repository.findActiveByDriverId("DRV-2001");

        assertEquals(2, assignments.size());
        assertEquals("ASN-3001", assignments.get(0).assignmentId());
        assertEquals("ASN-3002", assignments.get(1).assignmentId());
    }

    @Test
    void completedAssignmentExistsButIsNotActiveWork() {
        var repository = new InMemoryAssignmentRepository(SeedDataLoader.load());

        assertFalse(repository.findActiveByDriverId("DRV-2001").stream()
                .anyMatch(assignment -> "ASN-3003".equals(assignment.assignmentId())));
        assertEquals(AssignmentStatus.COMPLETED, repository.findById("ASN-3003").orElseThrow().status());
    }

    @Test
    void reservedSlice2AssignmentExistsButIsNotActiveWork() {
        var repository = new InMemoryAssignmentRepository(SeedDataLoader.load());

        assertTrue(repository.findById("ASN-3004").isPresent());
        assertFalse(repository.findActiveByDriverId("DRV-2001").stream()
                .anyMatch(assignment -> "ASN-3004".equals(assignment.assignmentId())));
    }
}
