package com.waypoint.partnersource.order.api;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.waypoint.partnersource.order.api.dto.AssignedDriverSummaryResponse;
import com.waypoint.partnersource.order.api.dto.DeliveryWindowResponse;
import com.waypoint.partnersource.order.api.dto.OrderStatusResponse;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.service.OrderStatusService;
import com.waypoint.partnersource.shared.error.ApiExceptionHandler;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.error.ProblemDetailFactory;
import java.time.OffsetDateTime;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(OrderStatusController.class)
@Import({ApiExceptionHandler.class, ProblemDetailFactory.class})
class OrderStatusControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    OrderStatusService orderStatusService;

    @Test
    void getOrderStatusReturnsContractShape() throws Exception {
        when(orderStatusService.getStatus("ORD-1001"))
                .thenReturn(new OrderStatusResponse(
                        "ORD-1001",
                        OrderStatus.OUT_FOR_DELIVERY,
                        "Out for delivery",
                        null,
                        null,
                        new DeliveryWindowResponse(null, null),
                        new AssignedDriverSummaryResponse("DRV-2001", "A. Kumar"),
                        OffsetDateTime.parse("2026-07-02T09:00:00+08:00")
                ));

        mockMvc.perform(get("/api/v1/orders/ORD-1001/status"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.orderId").value("ORD-1001"))
                .andExpect(jsonPath("$.currentStatus").value("OUT_FOR_DELIVERY"))
                .andExpect(jsonPath("$.statusLabel").value("Out for delivery"))
                .andExpect(jsonPath("$.deliveryWindow").exists())
                .andExpect(jsonPath("$.assignedDriver.driverId").value("DRV-2001"));
    }

    @Test
    void getMissingOrderReturnsNotFound() throws Exception {
        when(orderStatusService.getStatus("ORD-9999"))
                .thenThrow(PartnerSourceException.orderNotFound("ORD-9999"));

        mockMvc.perform(get("/api/v1/orders/ORD-9999/status"))
                .andExpect(status().isNotFound());
    }

    @Test
    void invalidOrderIdReturnsBadRequest() throws Exception {
        mockMvc.perform(get("/api/v1/orders/INVALID/status"))
                .andExpect(status().isBadRequest());
    }
}
