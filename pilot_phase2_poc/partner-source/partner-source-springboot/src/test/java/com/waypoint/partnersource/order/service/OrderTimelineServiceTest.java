package com.waypoint.partnersource.order.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import com.waypoint.partnersource.order.repository.InMemoryStatusEventRepository;
import com.waypoint.partnersource.shared.error.ErrorCode;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.seed.SeedDataLoader;
import org.junit.jupiter.api.Test;

class OrderTimelineServiceTest {
    @Test
    void returnsChronologicalTimelineForOrd1001() {
        var store = SeedDataLoader.load();
        var service = new OrderTimelineService(
                new InMemoryOrderRepository(store),
                new InMemoryStatusEventRepository(store)
        );

        var response = service.getTimeline("ORD-1001", 1, 20);

        assertEquals("ORD-1001", response.orderId());
        assertEquals(5, response.totalItems());
        assertEquals("EVT-4001", response.items().get(0).eventId());
        assertEquals("EVT-4005", response.items().get(4).eventId());
    }

    @Test
    void missingOrderThrowsOrderNotFound() {
        var store = SeedDataLoader.load();
        var service = new OrderTimelineService(
                new InMemoryOrderRepository(store),
                new InMemoryStatusEventRepository(store)
        );

        var exception = assertThrows(PartnerSourceException.class, () -> service.getTimeline("ORD-9999", 1, 20));

        assertEquals(ErrorCode.ORDER_NOT_FOUND, exception.errorCode());
    }
}
