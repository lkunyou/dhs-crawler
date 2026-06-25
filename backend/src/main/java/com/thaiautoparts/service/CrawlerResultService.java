package com.thaiautoparts.service;

import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.thaiautoparts.entity.CrawlerResult;

import java.util.List;
import java.util.Map;

public interface CrawlerResultService {
    Page<CrawlerResult> getResults(Long taskId, String status, String sourceType, int page, int size);
    CrawlerResult getResultDetail(Long id);
    int confirmResult(Long id);
    int rejectResult(Long id, String reason);
    int syncToCompany(Long id);
    int batchSync(List<Long> ids);
    int batchReject(List<Long> ids, String reason);
    Map<String, Object> getTaskStats(Long taskId);
    int countByTask(Long taskId);
    int saveResult(CrawlerResult result);
    int batchSaveResults(List<CrawlerResult> results);
}
