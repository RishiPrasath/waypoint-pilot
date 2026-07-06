package com.waypoint.partnersource.shared.security.dto;

public record DemoLoginResponse(
        String accessToken,
        String tokenType,
        int expiresIn,
        PrincipalResponse principal
) {
}
