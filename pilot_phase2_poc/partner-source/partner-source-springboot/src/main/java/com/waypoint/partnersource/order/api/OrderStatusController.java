package com.waypoint.partnersource.order.api;

import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.service.OrderStatusService;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import java.util.regex.Pattern;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderStatusController {
    private static final Pattern ORDER_ID_PATTERN = Pattern.compile("^ORD-[0-9]{4}$");

    private final OrderStatusService orderStatusService;

    public OrderStatusController(OrderStatusService orderStatusService) {
        this.orderStatusService = orderStatusService;
    }

    @GetMapping("/{orderId}/status")
    public OrderStatusResponse getOrderStatus(@PathVariable String orderId) {
        if (!ORDER_ID_PATTERN.matcher(orderId).matches()) {
            throw PartnerSourceException.invalidRequest("Invalid orderId.");
        }

        return orderStatusService.getStatus(orderId);
    }
}
