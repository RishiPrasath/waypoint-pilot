package com.waypoint.partnersource.shared.health;

import org.springframework.stereotype.Service;

import com.waypoint.partnersource.shared.seed.SeedDataStore;

@Service
public class ReadinessService {
    private final SeedDataStore store;

    public ReadinessService(SeedDataStore store) {
        this.store = store;
    }

    public ReadinessResponse check() {
        boolean seedReady = !store.orders().isEmpty()
                && !store.drivers().isEmpty()
                && !store.assignments().isEmpty()
                && !store.statusEventsByOrderId().isEmpty();

        return new ReadinessResponse(
                seedReady ? "READY" : "NOT_READY",
                "partner-source",
                new ReadinessChecks("UP", seedReady ? "UP" : "DOWN")
        );
    }
}
