package com.thaiautoparts.service;

import java.util.List;
import java.util.Map;

public interface DashboardService {
    Map<String, Object> getDashboardStats();
    List<Map<String, Object>> getGradeDistribution();
    List<Map<String, Object>> getSourceDistribution();
    List<Map<String, Object>> getFunnelData();
}
