package com.waypoint.partnersource.shared.error;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.waypoint.partnersource.order.api.OrderStatusController;
import com.waypoint.partnersource.order.service.OrderStatusService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(OrderStatusController.class)
@Import({ApiExceptionHandler.class, ProblemDetailFactory.class})
class ApiExceptionHandlerTest {

    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    OrderStatusService orderStatusService;

    @Test
    void invalidOrderIdUsesInvalidRequestProblemDetail() throws Exception {
        mockMvc.perform(get("/api/v1/orders/INVALID/status"))
                .andExpect(status().isBadRequest())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
                .andExpect(jsonPath("$.type").value("https://waypoint.local/problems/invalid-request"))
                .andExpect(jsonPath("$.title").value("Invalid request"))
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.detail").value("Invalid orderId."))
                .andExpect(jsonPath("$.instance").value("/api/v1/orders/INVALID/status"))
                .andExpect(jsonPath("$.errorCode").value("INVALID_REQUEST"))
                .andExpect(jsonPath("$.correlationId").exists());
    }

    @Test
    void requestCorrelationIdIsUsedWhenPresent() throws Exception {
        mockMvc.perform(get("/api/v1/orders/INVALID/status")
                        .header("X-Correlation-Id", "req-123"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.correlationId").value("req-123"));
    }
}
