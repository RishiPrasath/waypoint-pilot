package com.waypoint.partnersource.shared.security;

import com.waypoint.partnersource.shared.error.ProblemDetailFactory;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.Ordered;

@Configuration
public class SecurityFilterConfig {
    @Bean
    FilterRegistrationBean<AuthenticationFilter> authenticationFilter(
            DemoTokenAuthenticator authenticator,
            AccessPolicy accessPolicy,
            ProblemDetailFactory problemDetailFactory
    ) {
        var registration = new FilterRegistrationBean<>(
                new AuthenticationFilter(authenticator, accessPolicy, problemDetailFactory)
        );
        registration.setOrder(Ordered.HIGHEST_PRECEDENCE + 1);
        return registration;
    }
}
