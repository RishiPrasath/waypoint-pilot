package com.waypoint.partnersource.driver.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.waypoint.partnersource.assignment.repository.InMemoryAssignmentRepository;
import com.waypoint.partnersource.driver.domain.DriverAvailabilityStatus;
import com.waypoint.partnersource.driver.repository.InMemoryDriverRepository;
import com.waypoint.partnersource.shared.error.ErrorCode;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class DriverServiceTest {
    @Test
    void returnsDriverProfileWithActiveAssignmentCount() {
        var store = SeedDataLoader.load();
        var service = new DriverService(
                new InMemoryDriverRepository(store),
                new InMemoryAssignmentRepository(store),
                new DriverResponseMapper()
        );

        var response = service.getDriver("DRV-2001");

        assertEquals("DRV-2001", response.driverId());
        assertEquals("A. Kumar", response.displayName());
        assertEquals(DriverAvailabilityStatus.AVAILABLE, response.availabilityStatus());
        assertEquals(2, response.activeAssignmentCount());
    }

    @Test
    void missingDriverThrowsDriverNotFound() {
        var store = SeedDataLoader.load();
        var service = new DriverService(
                new InMemoryDriverRepository(store),
                new InMemoryAssignmentRepository(store),
                new DriverResponseMapper()
        );

        var exception = assertThrows(PartnerSourceException.class, () -> service.getDriver("DRV-9999"));

        assertEquals(ErrorCode.DRIVER_NOT_FOUND, exception.errorCode());
    }
}
