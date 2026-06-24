package com.thaiautoparts.service;

import java.util.Map;

public interface AnalyticsService {
    Map<String, Object> getDashboardStats();
    Map<String, Object> getEmailAnalytics();
    Map<String, Object> getWhatsappAnalytics();
    Map<String, Object> getConversionFunnel();
    Map<String, Object> getSourceQualityAnalysis();
    Map<String, Object> getProductInterestAnalysis();
    Map<String, Object> getDailyTrend(int days);
    void generateDailyStats();
}
