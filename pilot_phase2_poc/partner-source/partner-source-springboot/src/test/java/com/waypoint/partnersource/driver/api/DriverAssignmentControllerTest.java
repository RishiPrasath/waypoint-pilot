package com.waypoint.partnersource.driver.api;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.waypoint.partnersource.assignment.domain.AssignmentStatus;
import com.waypoint.partnersource.driver.api.dto.DriverAssignmentItemResponse;
import com.waypoint.partnersource.driver.api.dto.DriverAssignmentsResponse;
import com.waypoint.partnersource.driver.service.DriverAssignmentService;
import com.waypoint.partnersource.order.api.dto.DeliveryWindowResponse;
import com.waypoint.partnersource.order.domain.OrderStatus;
import java.time.OffsetDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(DriverAssignmentController.class)
class DriverAssignmentControllerTest {
    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    DriverAssignmentService driverAssignmentService;

    @Test
    void listAssignmentsReturnsContractShape() throws Exception {
        when(driverAssignmentService.listAssignments("DRV-2001", null, 1, 20))
                .thenReturn(new DriverAssignmentsResponse(
                        "DRV-2001",
                        List.of(
                                item("ASN-3001", "ORD-1001", OrderStatus.OUT_FOR_DELIVERY),
                                item("ASN-3002", "ORD-1002", OrderStatus.IN_TRANSIT)
                        ),
                        1,
                        20,
                        2
                ));

        mockMvc.perform(get("/api/v1/drivers/DRV-2001/assignments?page=1&pageSize=20"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.driverId").value("DRV-2001"))
                .andExpect(jsonPath("$.page").value(1))
                .andExpect(jsonPath("$.pageSize").value(20))
                .andExpect(jsonPath("$.totalItems").value(2))
                .andExpect(jsonPath("$.items[0].orderId").value("ORD-1001"))
                .andExpect(jsonPath("$.items[1].orderId").value("ORD-1002"));
    }

    @Test
    void invalidDriverIdReturnsProblemDetail() throws Exception {
        mockMvc.perform(get("/api/v1/drivers/INVALID/assignments"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errorCode").value("INVALID_REQUEST"));
    }

    private DriverAssignmentItemResponse item(String assignmentId, String orderId, OrderStatus status) {
        return new DriverAssignmentItemResponse(
                assignmentId,
                orderId,
                AssignmentStatus.ASSIGNED,
                status,
                "Recipient",
                "Singapore",
                new DeliveryWindowResponse(null, null),
                OffsetDateTime.parse("2026-07-02T09:00:00+08:00")
        );
    }
}
