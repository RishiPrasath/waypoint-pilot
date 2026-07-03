package com.waypoint.partnersource.driver.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.waypoint.partnersource.assignment.repository.InMemoryAssignmentRepository;
import com.waypoint.partnersource.driver.repository.InMemoryDriverRepository;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import com.waypoint.partnersource.shared.error.ErrorCode;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class DriverAssignmentServiceTest {
    @Test
    void returnsTwoActiveAssignmentsForDrv2001() {
        var service = service();

        var response = service.listAssignments("DRV-2001", null, 1, 20);

        assertEquals(2, response.totalItems());
        assertEquals("ORD-1001", response.items().get(0).orderId());
        assertEquals("ORD-1002", response.items().get(1).orderId());
    }

    @Test
    void availableDriverWithNoAssignmentsReturnsEmptyItems() {
        var service = service();

        var response = service.listAssignments("DRV-2003", null, 1, 20);

        assertTrue(response.items().isEmpty());
        assertEquals(0, response.totalItems());
    }

    @Test
    void statusFilterLimitsAssignments() {
        var service = service();

        var response = service.listAssignments("DRV-2001", OrderStatus.IN_TRANSIT, 1, 20);

        assertEquals(1, response.totalItems());
        assertEquals("ORD-1002", response.items().get(0).orderId());
    }

    @Test
    void missingDriverThrowsDriverNotFound() {
        var service = service();

        var exception = assertThrows(PartnerSourceException.class,
                () -> service.listAssignments("DRV-9999", null, 1, 20));

        assertEquals(ErrorCode.DRIVER_NOT_FOUND, exception.errorCode());
    }

    private DriverAssignmentService service() {
        var store = SeedDataLoader.load();
        return new DriverAssignmentService(
                new InMemoryDriverRepository(store),
                new InMemoryAssignmentRepository(store),
                new InMemoryOrderRepository(store),
                new DriverResponseMapper()
        );
    }
}
