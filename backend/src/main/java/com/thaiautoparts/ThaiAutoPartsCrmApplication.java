package com.thaiautoparts;

import com.thaiautoparts.service.SystemConfigService;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@MapperScan("com.thaiautoparts.repository")
@EnableScheduling
@EnableAsync
public class ThaiAutoPartsCrmApplication {
    public static void main(String[] args) {
        SpringApplication.run(ThaiAutoPartsCrmApplication.class, args);
    }

    @Bean
    public CommandLineRunner initDefaultConfigs(SystemConfigService systemConfigService) {
        return args -> {
            try {
                systemConfigService.initDefaultConfigs();
            } catch (Exception e) {
                // Ignore errors during startup config initialization
            }
        };
    }
}
