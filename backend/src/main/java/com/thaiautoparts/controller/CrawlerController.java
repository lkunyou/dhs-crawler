package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.CrawlerTask;
import com.thaiautoparts.service.CrawlerService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/crawler")
@RequiredArgsConstructor
public class CrawlerController {

    private final CrawlerService crawlerService;

    @PostMapping("/task")
    public Result<CrawlerTask> createTask(@RequestBody CrawlerTask task) {
        return Result.success(crawlerService.createCrawlerTask(task));
    }

    @PostMapping("/task/{taskId}/start")
    public Result<CrawlerTask> startTask(@PathVariable Long taskId) {
        return Result.success(crawlerService.startCrawlerTask(taskId));
    }

    @PostMapping("/task/{taskId}/stop")
    public Result<CrawlerTask> stopTask(@PathVariable Long taskId) {
        return Result.success(crawlerService.stopCrawlerTask(taskId));
    }

    @GetMapping("/tasks")
    public Result<List<CrawlerTask>> getTaskHistory() {
        return Result.success(crawlerService.getTaskHistory());
    }

    @GetMapping("/tasks/running")
    public Result<List<CrawlerTask>> getRunningTasks() {
        return Result.success(crawlerService.getRunningTasks());
    }

    @GetMapping("/stats")
    public Result<Map<String, Object>> getStats() {
        return Result.success(crawlerService.getTaskStats());
    }

    @DeleteMapping("/task/{taskId}")
    public Result<Void> deleteTask(@PathVariable Long taskId) {
        crawlerService.deleteTask(taskId);
        return Result.success();
    }
}
