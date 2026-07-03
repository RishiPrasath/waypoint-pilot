package com.waypoint.partnersource.shared.error;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.stereotype.Component;

@Component
public class ProblemDetailFactory {
    static final String CORRELATION_ID_ATTRIBUTE = "correlationId";

    public ProblemDetailResponse from(HttpServletRequest request, PartnerSourceException exception) {
        return new ProblemDetailResponse(
                problemType(exception.errorCode()),
                exception.title(),
                exception.status().value(),
                exception.getMessage(),
                request.getRequestURI(),
                exception.errorCode(),
                correlationId(request)
        );
    }

    private String problemType(ErrorCode errorCode) {
        var slug = errorCode.name().toLowerCase().replace("_", "-");
        return "https://waypoint.local/problems/" + slug;
    }

    private String correlationId(HttpServletRequest request) {
        var attribute = request.getAttribute(CORRELATION_ID_ATTRIBUTE);
        if (attribute instanceof String value && !value.isBlank()) {
            return value;
        }

        var header = request.getHeader("X-Correlation-Id");
        if (header != null && !header.isBlank()) {
            return header;
        }

        return "local-dev";
    }
}
