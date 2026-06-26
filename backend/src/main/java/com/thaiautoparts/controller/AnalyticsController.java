package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.AnalyticsService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/analytics")
@RequiredArgsConstructor
public class AnalyticsController {

    private final AnalyticsService analyticsService;

    @GetMapping("/email-stats")
    public Result<Map<String, Object>> getEmailStats() {
        return Result.success(analyticsService.getEmailStats());
    }

    @GetMapping("/whatsapp-stats")
    public Result<Map<String, Object>> getWhatsappStats() {
        return Result.success(analyticsService.getWhatsappStats());
    }

    @GetMapping("/source-quality")
    public Result<List<Map<String, Object>>> getSourceQuality() {
        return Result.success(analyticsService.getSourceQuality());
    }

    @GetMapping("/trend")
    public Result<List<Map<String, Object>>> getTrend(@RequestParam(defaultValue = "30") int days) {
        return Result.success(analyticsService.getTrend(days));
    }

    @GetMapping("/funnel")
    public Result<List<Map<String, Object>>> getFunnel() {
        return Result.success(analyticsService.getFunnel());
    }
}
