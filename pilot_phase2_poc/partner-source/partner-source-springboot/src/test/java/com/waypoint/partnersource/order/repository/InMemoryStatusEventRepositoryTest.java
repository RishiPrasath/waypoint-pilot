package com.waypoint.partnersource.order.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class InMemoryStatusEventRepositoryTest {

    @Test
    void findsChronologicalEventsForOrder() {
        var repository = new InMemoryStatusEventRepository(SeedDataLoader.load());

        var events = repository.findByOrderId("ORD-1001");

        assertEquals(5, events.size());
        assertEquals("EVT-4001", events.get(0).eventId());
        assertEquals("EVT-4005", events.get(4).eventId());
        assertEquals(OrderStatus.OUT_FOR_DELIVERY, events.get(4).newStatus());
    }

    @Test
    void missingOrderEventsReturnEmptyList() {
        var repository = new InMemoryStatusEventRepository(SeedDataLoader.load());

        assertTrue(repository.findByOrderId("ORD-9999").isEmpty());
    }
}
