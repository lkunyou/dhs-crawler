package com.thaiautoparts.config;

import com.twilio.Twilio;
import com.thaiautoparts.service.SystemConfigService;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Slf4j
@Configuration
@RequiredArgsConstructor
public class TwilioConfig {

    private final SystemConfigService systemConfigService;

    @Value("${spring.twilio.account-sid:ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}")
    private String accountSidYml;

    @Value("${spring.twilio.auth-token:your_auth_token}")
    private String authTokenYml;

    @Value("${spring.twilio.whatsapp-number:+14155238886}")
    private String whatsappNumberYml;

    private String accountSid;
    private String authToken;
    private String whatsappNumber;

    @PostConstruct
    public void init() {
        loadConfigFromDatabase();
        
        if (!isDefault(accountSid) && !isDefault(authToken)) {
            Twilio.init(accountSid, authToken);
            log.info("Twilio initialized successfully");
        } else {
            log.warn("Twilio credentials not configured - using mock mode");
        }
    }

    private void loadConfigFromDatabase() {
        this.accountSid = systemConfigService.getValue("twilio.account-sid", accountSidYml);
        this.authToken = systemConfigService.getValue("twilio.auth-token", authTokenYml);
        this.whatsappNumber = systemConfigService.getValue("twilio.whatsapp-number", whatsappNumberYml);
    }

    private boolean isDefault(String value) {
        return value == null 
                || "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX".equals(value) 
                || "your_auth_token".equals(value)
                || value.trim().isEmpty();
    }

    public boolean isConfigured() {
        if (isDefault(accountSid) || isDefault(authToken)) {
            return false;
        }
        if (!accountSid.startsWith("AC") || accountSid.length() != 34) {
            log.warn("Invalid Twilio Account SID format: {}", maskValue(accountSid));
            return false;
        }
        if (authToken.length() != 32) {
            log.warn("Invalid Twilio Auth Token format");
            return false;
        }
        return true;
    }

    private String maskValue(String value) {
        if (value == null || value.length() < 8) {
            return "***";
        }
        return value.substring(0, 4) + "******************" + value.substring(value.length() - 4);
    }

    public String getAccountSid() {
        return accountSid;
    }

    public String getAuthToken() {
        return authToken;
    }

    public String getWhatsappNumber() {
        return whatsappNumber;
    }

    public void refreshConfig() {
        loadConfigFromDatabase();
        if (isConfigured()) {
            Twilio.init(accountSid, authToken);
            log.info("Twilio reinitialized after config refresh");
        }
    }
}