package com.thaiautoparts.service;

import java.util.List;
import java.util.Map;

public interface AnalyticsService {
    Map<String, Object> getEmailStats();
    Map<String, Object> getWhatsappStats();
    List<Map<String, Object>> getSourceQuality();
    List<Map<String, Object>> getTrend(int days);
    List<Map<String, Object>> getFunnel();
}
