package com.waypoint.partnersource.order.service;

import com.waypoint.partnersource.order.api.dto.OrderTimelineResponse;
import com.waypoint.partnersource.order.api.dto.TimelineEventResponse;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import com.waypoint.partnersource.order.repository.InMemoryStatusEventRepository;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class OrderTimelineService {
    private final InMemoryOrderRepository orderRepository;
    private final InMemoryStatusEventRepository statusEventRepository;

    public OrderTimelineService(
            InMemoryOrderRepository orderRepository,
            InMemoryStatusEventRepository statusEventRepository
    ) {
        this.orderRepository = orderRepository;
        this.statusEventRepository = statusEventRepository;
    }

    public OrderTimelineResponse getTimeline(String orderId, int page, int pageSize) {
        orderRepository.findById(orderId)
                .orElseThrow(() -> PartnerSourceException.orderNotFound(orderId));

        var events = statusEventRepository.findByOrderId(orderId);
        var items = events.stream()
                .map(event -> new TimelineEventResponse(
                        event.eventId(),
                        event.newStatus(),
                        event.statusLabel(),
                        event.occurredAt(),
                        event.actorType(),
                        event.actorId(),
                        null,
                        null
                ))
                .toList();

        return new OrderTimelineResponse(orderId, page(items, page, pageSize), page, pageSize, items.size());
    }

    private static List<TimelineEventResponse> page(List<TimelineEventResponse> items, int page, int pageSize) {
        var fromIndex = Math.min((page - 1) * pageSize, items.size());
        var toIndex = Math.min(fromIndex + pageSize, items.size());
        return items.subList(fromIndex, toIndex);
    }
}
