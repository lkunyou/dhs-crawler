package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.AnalyticsService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/analytics")
@RequiredArgsConstructor
public class AnalyticsController {

    private final AnalyticsService analyticsService;

    @GetMapping("/dashboard")
    public Result<Map<String, Object>> getDashboardStats() {
        return Result.success(analyticsService.getDashboardStats());
    }

    @GetMapping("/email")
    public Result<Map<String, Object>> getEmailAnalytics() {
        return Result.success(analyticsService.getEmailAnalytics());
    }

    @GetMapping("/whatsapp")
    public Result<Map<String, Object>> getWhatsappAnalytics() {
        return Result.success(analyticsService.getWhatsappAnalytics());
    }

    @GetMapping("/funnel")
    public Result<Map<String, Object>> getConversionFunnel() {
        return Result.success(analyticsService.getConversionFunnel());
    }

    @GetMapping("/source-quality")
    public Result<Map<String, Object>> getSourceQuality() {
        return Result.success(analyticsService.getSourceQualityAnalysis());
    }

    @GetMapping("/product-interest")
    public Result<Map<String, Object>> getProductInterest() {
        return Result.success(analyticsService.getProductInterestAnalysis());
    }

    @GetMapping("/trend")
    public Result<Map<String, Object>> getDailyTrend(@RequestParam(defaultValue = "30") int days) {
        return Result.success(analyticsService.getDailyTrend(days));
    }
}
