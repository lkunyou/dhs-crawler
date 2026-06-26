package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.CustomerSearchService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/customer-search")
@RequiredArgsConstructor
public class CustomerSearchController {

    private final CustomerSearchService customerSearchService;

    @GetMapping("/search")
    public Result<List<Map<String, Object>>> search(
            @RequestParam String keyword,
            @RequestParam(defaultValue = "brave") String source,
            @RequestParam(defaultValue = "TH") String country) {
        return Result.success(customerSearchService.searchCompanies(keyword, source, country));
    }

    @PostMapping("/batch-search")
    public Result<List<Map<String, Object>>> batchSearch(
            @RequestBody List<String> keywords,
            @RequestParam(defaultValue = "brave") String source,
            @RequestParam(defaultValue = "TH") String country) {
        return Result.success(customerSearchService.batchSearchCompanies(keywords, source, country));
    }
}