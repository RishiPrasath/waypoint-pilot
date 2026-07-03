package com.waypoint.partnersource.order.service;

import com.waypoint.partnersource.assignment.domain.AssignmentAuthorizationPolicy;
import com.waypoint.partnersource.assignment.repository.InMemoryAssignmentRepository;
import com.waypoint.partnersource.driver.repository.InMemoryDriverRepository;
import com.waypoint.partnersource.order.api.dto.CreateStatusEventRequest;
import com.waypoint.partnersource.order.api.dto.StatusEventResponse;
import com.waypoint.partnersource.order.domain.ActorType;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.domain.OrderStatusEvent;
import com.waypoint.partnersource.order.domain.StatusTransitionPolicy;
import com.waypoint.partnersource.order.repository.InMemoryOrderRepository;
import com.waypoint.partnersource.order.repository.InMemoryStatusEventRepository;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import java.time.OffsetDateTime;
import org.springframework.stereotype.Service;

@Service
public class StatusEventService {
    private final InMemoryOrderRepository orderRepository;
    private final InMemoryDriverRepository driverRepository;
    private final InMemoryAssignmentRepository assignmentRepository;
    private final InMemoryStatusEventRepository statusEventRepository;
    private final AssignmentAuthorizationPolicy assignmentAuthorizationPolicy;
    private final StatusTransitionPolicy statusTransitionPolicy;

    public StatusEventService(
            InMemoryOrderRepository orderRepository,
            InMemoryDriverRepository driverRepository,
            InMemoryAssignmentRepository assignmentRepository,
            InMemoryStatusEventRepository statusEventRepository,
            AssignmentAuthorizationPolicy assignmentAuthorizationPolicy,
            StatusTransitionPolicy statusTransitionPolicy
    ) {
        this.orderRepository = orderRepository;
        this.driverRepository = driverRepository;
        this.assignmentRepository = assignmentRepository;
        this.statusEventRepository = statusEventRepository;
        this.assignmentAuthorizationPolicy = assignmentAuthorizationPolicy;
        this.statusTransitionPolicy = statusTransitionPolicy;
    }

    public StatusEventResponse createStatusEvent(String orderId, CreateStatusEventRequest request) {
        var order = orderRepository.findById(orderId)
                .orElseThrow(() -> PartnerSourceException.orderNotFound(orderId));

        driverRepository.findById(request.driverId())
                .orElseThrow(() -> PartnerSourceException.driverNotFound(request.driverId()));

        var assignments = assignmentRepository.findByOrderId(orderId);
        if (!assignmentAuthorizationPolicy.canDriverUpdateOrder(request.driverId(), orderId, assignments)) {
            throw PartnerSourceException.orderNotAssignedToDriver(orderId, request.driverId());
        }

        if (!statusTransitionPolicy.canTransition(order.currentStatus(), request.status())) {
            throw PartnerSourceException.invalidStatusTransition(
                    "Cannot transition order " + orderId + " from " + order.currentStatus() + " to " + request.status() + "."
            );
        }

        var occurredAt = request.occurredAt() == null ? OffsetDateTime.now() : request.occurredAt();
        if (occurredAt.isAfter(OffsetDateTime.now().plusDays(1))) {
            throw PartnerSourceException.invalidStatusEvent("Status event occurredAt is too far in the future.");
        }

        var event = new OrderStatusEvent(
                nextEventId(orderId),
                orderId,
                order.currentStatus(),
                request.status(),
                statusLabel(request.status()),
                occurredAt,
                ActorType.DRIVER,
                request.driverId()
        );

        statusEventRepository.append(event);
        orderRepository.save(order.withCurrentStatus(request.status(), event.statusLabel(), occurredAt));

        return new StatusEventResponse(
                event.eventId(),
                event.orderId(),
                event.previousStatus(),
                event.newStatus(),
                event.statusLabel(),
                event.occurredAt(),
                event.actorType(),
                event.actorId(),
                request.location(),
                request.note(),
                request.proofOfDeliveryAvailable(),
                request.status()
        );
    }

    private String nextEventId(String orderId) {
        var next = statusEventRepository.findByOrderId(orderId).stream()
                .map(OrderStatusEvent::eventId)
                .map(eventId -> eventId.replace("EVT-", ""))
                .mapToInt(Integer::parseInt)
                .max()
                .orElse(4000) + 1;
        return "EVT-" + next;
    }

    private String statusLabel(OrderStatus status) {
        return switch (status) {
            case CREATED -> "Created";
            case CONFIRMED -> "Confirmed";
            case PICKED_UP -> "Picked up";
            case IN_TRANSIT -> "In transit";
            case OUT_FOR_DELIVERY -> "Out for delivery";
            case DELIVERY_ATTEMPTED -> "Delivery attempted";
            case DELIVERED -> "Delivered";
            case CANCELLED -> "Cancelled";
        };
    }
}
