package com.waypoint.partnersource.shared.seed;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SeedDataConfig {
    @Bean
    SeedDataStore seedDataStore() {
        return SeedDataLoader.load();
    }
}
