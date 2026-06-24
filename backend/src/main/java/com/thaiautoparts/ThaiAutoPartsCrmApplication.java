package com.thaiautoparts;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
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
}
