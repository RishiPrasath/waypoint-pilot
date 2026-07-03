package com.waypoint.partnersource.order.api;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.waypoint.partnersource.order.service.OrderStatusService;
import com.waypoint.partnersource.shared.error.ApiExceptionHandler;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.error.ProblemDetailFactory;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(OrderStatusController.class)
@Import({ApiExceptionHandler.class, ProblemDetailFactory.class})
class OrderStatusErrorContractTest {

    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    OrderStatusService orderStatusService;

    @Test
    void missingOrderUsesProblemDetail() throws Exception {
        when(orderStatusService.getStatus("ORD-9999"))
                .thenThrow(PartnerSourceException.orderNotFound("ORD-9999"));

        mockMvc.perform(get("/api/v1/orders/ORD-9999/status"))
                .andExpect(status().isNotFound())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
                .andExpect(jsonPath("$.type").value("https://waypoint.local/problems/order-not-found"))
                .andExpect(jsonPath("$.title").value("Order not found"))
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.detail").value("No order exists for orderId ORD-9999."))
                .andExpect(jsonPath("$.instance").value("/api/v1/orders/ORD-9999/status"))
                .andExpect(jsonPath("$.errorCode").value("ORDER_NOT_FOUND"))
                .andExpect(jsonPath("$.correlationId").exists());
    }

    @Test
    void deprecatedTransitionCodeIsNotReturned() throws Exception {
        when(orderStatusService.getStatus("ORD-9999"))
                .thenThrow(PartnerSourceException.orderNotFound("ORD-9999"));

        mockMvc.perform(get("/api/v1/orders/ORD-9999/status"))
                .andExpect(result -> assertThat(result.getResponse().getContentAsString())
                        .doesNotContain("ORDER_TRANSITION_INVALID"));
    }
}
