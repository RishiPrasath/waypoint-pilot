package com.waypoint.partnersource.order.api;

import com.waypoint.partnersource.order.api.dto.OrderTimelineResponse;
import com.waypoint.partnersource.order.service.OrderTimelineService;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import java.util.regex.Pattern;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderTimelineController {
    private static final Pattern ORDER_ID_PATTERN = Pattern.compile("^ORD-[0-9]{4}$");

    private final OrderTimelineService orderTimelineService;

    public OrderTimelineController(OrderTimelineService orderTimelineService) {
        this.orderTimelineService = orderTimelineService;
    }

    @GetMapping("/{orderId}/timeline")
    public OrderTimelineResponse getOrderTimeline(
            @PathVariable String orderId,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int pageSize
    ) {
        if (!ORDER_ID_PATTERN.matcher(orderId).matches() || page < 1 || pageSize < 1 || pageSize > 100) {
            throw PartnerSourceException.invalidRequest("Invalid timeline request.");
        }

        return orderTimelineService.getTimeline(orderId, page, pageSize);
    }
}
