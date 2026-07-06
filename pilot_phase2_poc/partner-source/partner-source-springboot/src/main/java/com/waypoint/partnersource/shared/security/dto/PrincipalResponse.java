package com.waypoint.partnersource.shared.security.dto;

import com.waypoint.partnersource.shared.security.ActorRole;
import com.waypoint.partnersource.shared.security.PrincipalActorType;
import java.util.List;

public record PrincipalResponse(
        String subject,
        ActorRole role,
        PrincipalActorType actorType,
        String actorId,
        List<String> scopes,
        String demoOrgId,
        String channel
) {
}
