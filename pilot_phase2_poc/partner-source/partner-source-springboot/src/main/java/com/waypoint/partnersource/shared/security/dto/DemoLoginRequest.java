package com.waypoint.partnersource.shared.security.dto;

import jakarta.validation.constraints.NotBlank;

public record DemoLoginRequest(
        @NotBlank String actorType,
        @NotBlank String actorId
) {
}
