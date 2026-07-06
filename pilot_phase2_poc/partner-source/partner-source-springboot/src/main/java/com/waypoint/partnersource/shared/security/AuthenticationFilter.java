package com.waypoint.partnersource.shared.security;

import com.waypoint.partnersource.shared.error.PartnerSourceException;
import com.waypoint.partnersource.shared.error.ProblemDetailFactory;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.regex.Pattern;
import org.springframework.http.MediaType;
import org.springframework.web.filter.OncePerRequestFilter;

public class AuthenticationFilter extends OncePerRequestFilter {
    private static final Pattern DRIVER_PATH = Pattern.compile("^/api/v1/drivers/(DRV-[0-9]{4})(/assignments)?$");
    private static final Pattern ORDER_READ_PATH = Pattern.compile("^/api/v1/orders/(ORD-[0-9]{4})/(status|timeline)$");
    private static final Pattern STATUS_EVENT_PATH = Pattern.compile("^/api/v1/orders/(ORD-[0-9]{4})/status-events$");

    private final DemoTokenAuthenticator authenticator;
    private final AccessPolicy accessPolicy;
    private final ProblemDetailFactory problemDetailFactory;

    public AuthenticationFilter(
            DemoTokenAuthenticator authenticator,
            AccessPolicy accessPolicy,
            ProblemDetailFactory problemDetailFactory
    ) {
        this.authenticator = authenticator;
        this.accessPolicy = accessPolicy;
        this.problemDetailFactory = problemDetailFactory;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {
        if (!isProtectedRoute(request)) {
            filterChain.doFilter(request, response);
            return;
        }

        var principal = authenticate(request);
        if (principal == null) {
            writeProblem(response, request, PartnerSourceException.unauthenticated("Missing or invalid bearer token."));
            return;
        }

        request.setAttribute(CurrentPrincipal.ATTRIBUTE, principal);
        var denied = routeDenied(request, principal);
        if (denied != null) {
            writeProblem(response, request, denied);
            return;
        }

        filterChain.doFilter(request, response);
    }

    private boolean isProtectedRoute(HttpServletRequest request) {
        var path = request.getRequestURI();
        return path.startsWith("/api/v1/")
                && !path.equals("/api/v1/auth/demo-login");
    }

    private AuthenticatedPrincipal authenticate(HttpServletRequest request) {
        var header = request.getHeader("Authorization");
        if (header == null || !header.startsWith("Bearer ")) {
            return null;
        }

        var token = header.substring("Bearer ".length()).trim();
        if (token.isBlank()) {
            return null;
        }

        return authenticator.authenticate(token).orElse(null);
    }

    private PartnerSourceException routeDenied(HttpServletRequest request, AuthenticatedPrincipal principal) {
        var path = request.getRequestURI();
        var method = request.getMethod();

        var driverMatcher = DRIVER_PATH.matcher(path);
        if ("GET".equals(method) && driverMatcher.matches()
                && !accessPolicy.canReadDriverResource(principal, driverMatcher.group(1))) {
            return PartnerSourceException.accessDenied("Caller cannot access this driver resource.");
        }

        var orderReadMatcher = ORDER_READ_PATH.matcher(path);
        if ("GET".equals(method) && orderReadMatcher.matches()
                && !accessPolicy.canReadOrder(principal, orderReadMatcher.group(1))) {
            return PartnerSourceException.accessDenied("Caller cannot access this order resource.");
        }

        var statusEventMatcher = STATUS_EVENT_PATH.matcher(path);
        if ("POST".equals(method) && statusEventMatcher.matches()
                && !accessPolicy.canCreateStatusEvent(principal)) {
            return PartnerSourceException.accessDenied("Caller cannot create driver status events.");
        }

        return null;
    }

    private void writeProblem(HttpServletResponse response, HttpServletRequest request, PartnerSourceException exception)
            throws IOException {
        response.setStatus(exception.status().value());
        response.setContentType(MediaType.APPLICATION_PROBLEM_JSON_VALUE);
        var problem = problemDetailFactory.from(request, exception);
        response.getWriter().write("""
                {"type":"%s","title":"%s","status":%d,"detail":"%s","instance":"%s","errorCode":"%s","correlationId":"%s"}\
                """.formatted(
                escape(problem.type()),
                escape(problem.title()),
                problem.status(),
                escape(problem.detail()),
                escape(problem.instance()),
                problem.errorCode().name(),
                escape(problem.correlationId())
        ));
    }

    private String escape(String value) {
        return value.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
