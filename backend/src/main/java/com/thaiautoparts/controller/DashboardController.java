package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/dashboard")
@RequiredArgsConstructor
public class DashboardController {

    private final DashboardService dashboardService;

    @GetMapping("/stats")
    public Result<Map<String, Object>> getDashboardStats() {
        return Result.success(dashboardService.getDashboardStats());
    }

    @GetMapping("/grade-distribution")
    public Result<List<Map<String, Object>>> getGradeDistribution() {
        return Result.success(dashboardService.getGradeDistribution());
    }

    @GetMapping("/source-distribution")
    public Result<List<Map<String, Object>>> getSourceDistribution() {
        return Result.success(dashboardService.getSourceDistribution());
    }

    @GetMapping("/funnel")
    public Result<List<Map<String, Object>>> getFunnelData() {
        return Result.success(dashboardService.getFunnelData());
    }
}
