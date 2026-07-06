package com.waypoint.partnersource.order.api;

import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.waypoint.partnersource.order.api.dto.CreateStatusEventRequest;
import com.waypoint.partnersource.order.api.dto.StatusEventResponse;
import com.waypoint.partnersource.order.domain.ActorType;
import com.waypoint.partnersource.order.domain.OrderStatus;
import com.waypoint.partnersource.order.service.StatusEventService;
import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.security.AccessPolicy;
import com.waypoint.partnersource.shared.security.ActorRole;
import com.waypoint.partnersource.shared.security.AuthenticatedPrincipal;
import com.waypoint.partnersource.shared.security.CurrentPrincipal;
import com.waypoint.partnersource.shared.security.PrincipalActorType;
import java.time.OffsetDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentMatchers;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(StatusEventController.class)
class StatusEventControllerTest {
    @Autowired
    MockMvc mockMvc;

    @MockitoBean
    StatusEventService statusEventService;

    @MockitoBean
    AccessPolicy accessPolicy;

    private final AuthenticatedPrincipal driverPrincipal = new AuthenticatedPrincipal(
            "driver:DRV-2001",
            ActorRole.DELIVERY_DRIVER,
            PrincipalActorType.DRIVER,
            "DRV-2001",
            List.of(),
            "ORG-DEMO-1",
            "DRIVER_APP"
    );

    @Test
    void createStatusEventReturnsCreated() throws Exception {
        when(accessPolicy.canSubmitDriverId(driverPrincipal, "DRV-2001")).thenReturn(true);
        when(statusEventService.createStatusEvent(
                ArgumentMatchers.eq("ORD-1001"),
                ArgumentMatchers.any(CreateStatusEventRequest.class)
        )).thenReturn(new StatusEventResponse(
                "EVT-4006",
                "ORD-1001",
                OrderStatus.OUT_FOR_DELIVERY,
                OrderStatus.DELIVERED,
                "Delivered",
                OffsetDateTime.parse("2026-07-02T10:30:00+08:00"),
                ActorType.DRIVER,
                "DRV-2001",
                null,
                "Left with reception",
                true,
                OrderStatus.DELIVERED
        ));

        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
                        .with(request -> {
                            request.setAttribute(CurrentPrincipal.ATTRIBUTE, driverPrincipal);
                            return request;
                        })
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "driverId": "DRV-2001",
                                  "status": "DELIVERED",
                                  "occurredAt": "2026-07-02T10:30:00+08:00",
                                  "note": "Left with reception",
                                  "proofOfDeliveryAvailable": true
                                }
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.eventId").value("EVT-4006"))
                .andExpect(jsonPath("$.previousStatus").value("OUT_FOR_DELIVERY"))
                .andExpect(jsonPath("$.newStatus").value("DELIVERED"))
                .andExpect(jsonPath("$.orderCurrentStatus").value("DELIVERED"));
    }

    @Test
    void unassignedDriverReturnsProblemDetail() throws Exception {
        var driver2002 = new AuthenticatedPrincipal(
                "driver:DRV-2002",
                ActorRole.DELIVERY_DRIVER,
                PrincipalActorType.DRIVER,
                "DRV-2002",
                List.of(),
                "ORG-DEMO-1",
                "DRIVER_APP"
        );
        when(accessPolicy.canSubmitDriverId(driver2002, "DRV-2002")).thenReturn(true);
        when(statusEventService.createStatusEvent(
                ArgumentMatchers.eq("ORD-1001"),
                ArgumentMatchers.any(CreateStatusEventRequest.class)
        )).thenThrow(PartnerSourceException.orderNotAssignedToDriver("ORD-1001", "DRV-2002"));

        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
                        .with(request -> {
                            request.setAttribute(CurrentPrincipal.ATTRIBUTE, driver2002);
                            return request;
                        })
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "driverId": "DRV-2002",
                                  "status": "DELIVERED"
                                }
                                """))
                .andExpect(status().isForbidden())
                .andExpect(jsonPath("$.errorCode").value("ORDER_NOT_ASSIGNED_TO_DRIVER"));
    }

    @Test
    void malformedBodyReturnsInvalidRequestProblemDetail() throws Exception {
        mockMvc.perform(post("/api/v1/orders/ORD-1001/status-events")
                        .with(request -> {
                            request.setAttribute(CurrentPrincipal.ATTRIBUTE, driverPrincipal);
                            return request;
                        })
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "driverId": "DRV-2001"
                                }
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errorCode").value("INVALID_REQUEST"));
    }
}
