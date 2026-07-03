package com.waypoint.partnersource.shared.health;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HealthController {
    @GetMapping("/health")
    public HealthResponse getHealth() {
        return new HealthResponse("UP", "partner-source");
    }
}
