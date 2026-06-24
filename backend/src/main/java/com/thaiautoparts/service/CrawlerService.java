package com.thaiautoparts.service;

import com.thaiautoparts.entity.CrawlerTask;
import java.util.List;
import java.util.Map;

public interface CrawlerService {
    CrawlerTask createCrawlerTask(CrawlerTask task);
    CrawlerTask startCrawlerTask(Long taskId);
    CrawlerTask stopCrawlerTask(Long taskId);
    List<CrawlerTask> getTaskHistory();
    List<CrawlerTask> getRunningTasks();
    Map<String, Object> getTaskStats();
    void scheduleCrawlerTask(CrawlerTask task);
}
