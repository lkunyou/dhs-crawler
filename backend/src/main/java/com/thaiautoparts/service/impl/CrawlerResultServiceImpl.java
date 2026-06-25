package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.CrawlerResult;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.CrawlerResultMapper;
import com.thaiautoparts.service.CrawlerResultService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class CrawlerResultServiceImpl implements CrawlerResultService {

    private final CrawlerResultMapper crawlerResultMapper;
    private final CompanyMapper companyMapper;

    @Override
    public Page<CrawlerResult> getResults(Long taskId, String status, String sourceType, int page, int size) {
        LambdaQueryWrapper<CrawlerResult> wrapper = new LambdaQueryWrapper<>();
        if (taskId != null) wrapper.eq(CrawlerResult::getTaskId, taskId);
        if (status != null && !status.isEmpty()) wrapper.eq(CrawlerResult::getStatus, status);
        if (sourceType != null && !sourceType.isEmpty()) wrapper.eq(CrawlerResult::getSourceType, sourceType);
        wrapper.orderByDesc(CrawlerResult::getCreatedAt);
        return crawlerResultMapper.selectPage(new Page<>(page, size), wrapper);
    }

    @Override
    public CrawlerResult getResultDetail(Long id) {
        return crawlerResultMapper.selectById(id);
    }

    @Override
    @Transactional
    public int confirmResult(Long id) {
        CrawlerResult result = crawlerResultMapper.selectById(id);
        if (result == null || !"Pending".equals(result.getStatus())) {
            throw new RuntimeException("结果不存在或已处理");
        }
        result.setStatus("Confirmed");
        result.setConfirmedAt(LocalDateTime.now());
        return crawlerResultMapper.updateById(result);
    }

    @Override
    @Transactional
    public int rejectResult(Long id, String reason) {
        CrawlerResult result = crawlerResultMapper.selectById(id);
        if (result == null || !"Pending".equals(result.getStatus())) {
            throw new RuntimeException("结果不存在或已处理");
        }
        result.setStatus("Rejected");
        result.setRejectionReason(reason);
        result.setConfirmedAt(LocalDateTime.now());
        return crawlerResultMapper.updateById(result);
    }

    @Override
    @Transactional
    public int syncToCompany(Long id) {
        CrawlerResult result = crawlerResultMapper.selectById(id);
        if (result == null) {
            throw new RuntimeException("结果不存在");
        }
        if ("Synced".equals(result.getStatus())) {
            throw new RuntimeException("已同步");
        }

        // 检查是否重复
        LambdaQueryWrapper<Company> companyWrapper = new LambdaQueryWrapper<>();
        companyWrapper.eq(Company::getCompanyName, result.getCompanyName())
                .or()
                .eq(result.getWebsite() != null, Company::getWebsite, result.getWebsite())
                .or()
                .eq(result.getPhone() != null, Company::getPhone, result.getPhone());
        Long existCount = companyMapper.selectCount(companyWrapper);
        if (existCount > 0) {
            result.setStatus("Duplicate");
            result.setConfirmedAt(LocalDateTime.now());
            crawlerResultMapper.updateById(result);
            return 0;
        }

        // 创建公司记录
        Company company = new Company();
        company.setCompanyName(result.getCompanyName());
        company.setCompanyNameTh(result.getCompanyNameTh());
        company.setCompanyNameEn(result.getCompanyNameEn());
        company.setWebsite(result.getWebsite());
        company.setAddress(result.getAddress());
        company.setCity(result.getCity());
        company.setProvince(result.getProvince());
        company.setPhone(result.getPhone());
        company.setWhatsapp(result.getWhatsapp());
        company.setEmail(result.getEmail());
        company.setSource(result.getSourceType());
        company.setSourceUrl(result.getSourceUrl());
        company.setRawData(result.getRawData());
        company.setLeadScore(result.getLeadScore() != null ? result.getLeadScore() : 0);
        company.setLeadGrade(result.getLeadGrade() != null ? result.getLeadGrade() : "C");
        company.setIsAutoPartsCore(result.getIsAutoPartsCore() != null ? result.getIsAutoPartsCore() : false);
        company.setIsImporterDistributor(result.getIsImporterDistributor() != null ? result.getIsImporterDistributor() : false);
        company.setStatus("New");

        companyMapper.insert(company);

        // 更新结果状态
        result.setStatus("Synced");
        result.setSyncedCompanyId(company.getId());
        result.setSyncedAt(LocalDateTime.now());
        crawlerResultMapper.updateById(result);

        log.info("Synced crawler result {} to company {}", id, company.getId());
        return 1;
    }

    @Override
    @Transactional
    public int batchSync(List<Long> ids) {
        int count = 0;
        for (Long id : ids) {
            try {
                count += syncToCompany(id);
            } catch (Exception e) {
                log.error("Failed to sync result {}: {}", id, e.getMessage());
            }
        }
        return count;
    }

    @Override
    @Transactional
    public int batchReject(List<Long> ids, String reason) {
        int count = 0;
        for (Long id : ids) {
            try {
                rejectResult(id, reason);
                count++;
            } catch (Exception e) {
                log.error("Failed to reject result {}: {}", id, e.getMessage());
            }
        }
        return count;
    }

    @Override
    public Map<String, Object> getTaskStats(Long taskId) {
        List<Map<String, Object>> statusCounts = crawlerResultMapper.countByStatus(taskId);
        List<Map<String, Object>> sourceCounts = crawlerResultMapper.countBySource(taskId);

        return Map.of(
                "statusBreakdown", statusCounts,
                "sourceBreakdown", sourceCounts
        );
    }

    @Override
    public int countByTask(Long taskId) {
        LambdaQueryWrapper<CrawlerResult> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(CrawlerResult::getTaskId, taskId);
        return Math.toIntExact(crawlerResultMapper.selectCount(wrapper));
    }

    @Override
    public int saveResult(CrawlerResult result) {
        return crawlerResultMapper.insert(result);
    }

    @Override
    @Transactional
    public int batchSaveResults(List<CrawlerResult> results) {
        int count = 0;
        for (CrawlerResult result : results) {
            crawlerResultMapper.insert(result);
            count++;
        }
        return count;
    }
}
