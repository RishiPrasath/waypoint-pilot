package com.waypoint.partnersource.order.api;

import com.waypoint.partnersource.order.api.dto.CreateStatusEventRequest;
import com.waypoint.partnersource.order.api.dto.StatusEventResponse;
import com.waypoint.partnersource.order.service.StatusEventService;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import jakarta.validation.Valid;
import java.util.regex.Pattern;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/orders")
public class StatusEventController {
    private static final Pattern ORDER_ID_PATTERN = Pattern.compile("^ORD-[0-9]{4}$");

    private final StatusEventService statusEventService;

    public StatusEventController(StatusEventService statusEventService) {
        this.statusEventService = statusEventService;
    }

    @PostMapping("/{orderId}/status-events")
    @ResponseStatus(HttpStatus.CREATED)
    public StatusEventResponse createStatusEvent(
            @PathVariable String orderId,
            @Valid @RequestBody CreateStatusEventRequest request
    ) {
        if (!ORDER_ID_PATTERN.matcher(orderId).matches()) {
            throw PartnerSourceException.invalidRequest("Invalid orderId.");
        }

        return statusEventService.createStatusEvent(orderId, request);
    }
}
