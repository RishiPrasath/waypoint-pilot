package com.waypoint.partnersource.order.api;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.waypoint.partnersource.order.api.dto.OrderTimelineResponse;
import com.waypoint.partnersource.order.api.dto.TimelineEventResponse;
import com.waypoint.partnersource.order.domain.ActorType;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.service.OrderTimelineService;
import java.time.OffsetDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(OrderTimelineController.class)
class OrderTimelineControllerTest {
    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    OrderTimelineService orderTimelineService;

    @Test
    void getTimelineReturnsContractShape() throws Exception {
        when(orderTimelineService.getTimeline("ORD-1001", 1, 20))
                .thenReturn(new OrderTimelineResponse(
                        "ORD-1001",
                        List.of(
                                new TimelineEventResponse("EVT-4001", OrderStatus.CREATED, "Created",
                                        OffsetDateTime.parse("2026-07-02T05:00:00+08:00"), ActorType.SYSTEM, "system", null, null),
                                new TimelineEventResponse("EVT-4005", OrderStatus.OUT_FOR_DELIVERY, "Out for delivery",
                                        OffsetDateTime.parse("2026-07-02T09:00:00+08:00"), ActorType.DRIVER, "DRV-2001", null, null)
                        ),
                        1,
                        20,
                        5
                ));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/timeline?page=1&pageSize=20"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.orderId").value("ORD-1001"))
                .andExpect(jsonPath("$.page").value(1))
                .andExpect(jsonPath("$.pageSize").value(20))
                .andExpect(jsonPath("$.totalItems").value(5))
                .andExpect(jsonPath("$.items[0].eventId").value("EVT-4001"))
                .andExpect(jsonPath("$.items[1].eventId").value("EVT-4005"));
    }

    @Test
    void invalidOrderIdReturnsProblemDetail() throws Exception {
        mockMvc.perform(get("/api/v1/orders/INVALID/timeline"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errorCode").value("INVALID_REQUEST"));
    }
}
