package com.example;

import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class HeaderConfig {

    @Bean
    @ConditionalOnClass(name = "io.jsonwebtoken.Jwts")
    public HeaderParser headerParser(){

        return new HeaderParser();
    }

    @Bean
    public HeaderGenerator headerGenerator(){

        return new HeaderGenerator();
    }

}
