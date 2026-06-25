package com.thaiautoparts.controller;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.CrawlerResult;
import com.thaiautoparts.service.CrawlerResultService;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/crawler-result")
@RequiredArgsConstructor
public class CrawlerResultController {

    private final CrawlerResultService crawlerResultService;

    @GetMapping("/list")
    public Result<Page<CrawlerResult>> getResults(
            @RequestParam(required = false) Long taskId,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String sourceType,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int size
    ) {
        return Result.success(crawlerResultService.getResults(taskId, status, sourceType, page, size));
    }

    @GetMapping("/{id}")
    public Result<CrawlerResult> getDetail(@PathVariable Long id) {
        return Result.success(crawlerResultService.getResultDetail(id));
    }

    @PostMapping("/{id}/confirm")
    public Result<Void> confirm(@PathVariable Long id) {
        crawlerResultService.confirmResult(id);
        return Result.success();
    }

    @PostMapping("/{id}/reject")
    public Result<Void> reject(@PathVariable Long id, @RequestBody RejectRequest request) {
        crawlerResultService.rejectResult(id, request.getReason());
        return Result.success();
    }

    @PostMapping("/{id}/sync")
    public Result<Void> sync(@PathVariable Long id) {
        crawlerResultService.syncToCompany(id);
        return Result.success();
    }

    @PostMapping("/batch-sync")
    public Result<Map<String, Object>> batchSync(@RequestBody BatchRequest request) {
        int count = crawlerResultService.batchSync(request.getIds());
        return Result.success(Map.of("synced", count));
    }

    @PostMapping("/batch-reject")
    public Result<Map<String, Object>> batchReject(@RequestBody BatchRequest request) {
        int count = crawlerResultService.batchReject(request.getIds(), request.getReason());
        return Result.success(Map.of("rejected", count));
    }

    @GetMapping("/task-stats/{taskId}")
    public Result<Map<String, Object>> getTaskStats(@PathVariable Long taskId) {
        return Result.success(crawlerResultService.getTaskStats(taskId));
    }

    @Data
    static class RejectRequest {
        private String reason;
    }

    @Data
    static class BatchRequest {
        private List<Long> ids;
        private String reason;
    }
}
