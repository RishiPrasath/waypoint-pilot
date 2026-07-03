package com.waypoint.partnersource.driver.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.waypoint.partnersource.driver.domain.DriverAvailabilityStatus;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class InMemoryDriverRepositoryTest {

    @Test
    void findsSeededDriver() {
        var repository = new InMemoryDriverRepository(SeedDataLoader.load());

        var driver = repository.findById("DRV-2001");

        assertTrue(driver.isPresent());
        assertEquals(DriverAvailabilityStatus.AVAILABLE, driver.get().availabilityStatus());
    }

    @Test
    void missingDriverReturnsEmpty() {
        var repository = new InMemoryDriverRepository(SeedDataLoader.load());

        assertTrue(repository.findById("DRV-9999").isEmpty());
    }
}
