package com.waypoint.partnersource.driver.repository;

import com.waypoint.partnersource.driver.domain.DeliveryDriver;
import com.waypoint.partnersource.shared.seed.SeedDataStore;
import java.util.Optional;
import org.springframework.stereotype.Repository;

@Repository
public class InMemoryDriverRepository {
    private final SeedDataStore store;

    public InMemoryDriverRepository(SeedDataStore store) {
        this.store = store;
    }

    public Optional<DeliveryDriver> findById(String driverId) {
        return Optional.ofNullable(store.drivers().get(driverId));
    }
}
