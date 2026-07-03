package com.waypoint.partnersource.order.service;

import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import org.springframework.stereotype.Service;

@Service
public class OrderStatusService {
    private final InMemoryOrderRepository orderRepository;
    private final OrderResponseMapper mapper;

    public OrderStatusService(InMemoryOrderRepository orderRepository, OrderResponseMapper mapper) {
        this.orderRepository = orderRepository;
        this.mapper = mapper;
    }

    public OrderStatusResponse getStatus(String orderId) {
        return orderRepository.findById(orderId)
                .map(mapper::toStatusResponse)
                .orElseThrow(() -> PartnerSourceException.orderNotFound(orderId));
    }
}
