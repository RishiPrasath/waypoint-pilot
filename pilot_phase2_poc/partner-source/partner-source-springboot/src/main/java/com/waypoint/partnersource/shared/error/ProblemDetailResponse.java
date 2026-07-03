package com.waypoint.partnersource.shared.error;

public record ProblemDetailResponse(
        String type,
        String title,
        int status,
        String detail,
        String instance,
        ErrorCode errorCode,
        String correlationId
) {
}
