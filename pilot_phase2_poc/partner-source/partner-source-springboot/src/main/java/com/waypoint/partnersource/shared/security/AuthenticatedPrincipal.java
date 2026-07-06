package com.waypoint.partnersource.shared.security;

import java.util.List;

public record AuthenticatedPrincipal(
        String subject,
        ActorRole role,
        PrincipalActorType actorType,
        String actorId,
        List<String> scopes,
        String demoOrgId,
        String channel
) {
}
