package com.waypoint.partnersource.shared.health;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class ReadinessServiceTest {

    @Test
    void reportsReadyWhenSeedDataExists() {
        var service = new ReadinessService(SeedDataLoader.load());

        var response = service.check();

        assertEquals("READY", response.status());
        assertEquals("partner-source", response.service());
        assertEquals("UP", response.checks().persistence());
        assertEquals("UP", response.checks().seedData());
    }
}
