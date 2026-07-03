package com.waypoint.partnersource.shared.policy;

import com.waypoint.partnersource.assignment.domain.AssignmentAuthorizationPolicy;
import com.waypoint.partnersource.order.domain.StatusTransitionPolicy;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class PolicyConfig {
    @Bean
    AssignmentAuthorizationPolicy assignmentAuthorizationPolicy() {
        return new AssignmentAuthorizationPolicy();
    }

    @Bean
    StatusTransitionPolicy statusTransitionPolicy() {
        return new StatusTransitionPolicy();
    }
}
