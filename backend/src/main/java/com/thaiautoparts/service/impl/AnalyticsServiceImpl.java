package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.DailyStats;
import com.thaiautoparts.entity.EmailRecord;
import com.thaiautoparts.entity.WhatsappRecord;
import com.thaiautoparts.repository.*;
import com.thaiautoparts.service.AnalyticsService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class AnalyticsServiceImpl implements AnalyticsService {

    private final CompanyMapper companyMapper;
    private final EmailRecordMapper emailRecordMapper;
    private final WhatsappRecordMapper whatsappRecordMapper;
    private final DailyStatsMapper dailyStatsMapper;

    @Override
    public Map<String, Object> getDashboardStats() {
        Map<String, Object> stats = new HashMap<>();
        
        // 总客户数
        long totalCompanies = companyMapper.selectCount(new LambdaQueryWrapper<>());
        stats.put("totalCompanies", totalCompanies);
        
        // 各等级客户数
        List<Map<String, Object>> gradeStats = companyMapper.countByLeadGrade();
        stats.put("gradeDistribution", gradeStats);
        
        // 各状态客户数
        List<Map<String, Object>> statusStats = companyMapper.countByStatus();
        stats.put("statusDistribution", statusStats);
        
        // 邮件统计
        LambdaQueryWrapper<EmailRecord> emailWrapper = new LambdaQueryWrapper<>();
        long emailsSent = emailRecordMapper.selectCount(emailWrapper);
        stats.put("emailsSent", emailsSent);
        
        // WhatsApp统计
        LambdaQueryWrapper<WhatsappRecord> waWrapper = new LambdaQueryWrapper<>();
        long whatsappSent = whatsappRecordMapper.selectCount(waWrapper);
        stats.put("whatsappSent", whatsappSent);
        
        // 今日新增
        LambdaQueryWrapper<Company> todayWrapper = new LambdaQueryWrapper<>();
        todayWrapper.ge(Company::getCreatedAt, LocalDateTime.now().toLocalDate().atStartOfDay());
        long todayNew = companyMapper.selectCount(todayWrapper);
        stats.put("todayNew", todayNew);
        
        return stats;
    }

    @Override
    public Map<String, Object> getEmailAnalytics() {
        Map<String, Object> analytics = new HashMap<>();
        
        LambdaQueryWrapper<EmailRecord> wrapper = new LambdaQueryWrapper<>();
        long total = emailRecordMapper.selectCount(wrapper);
        
        wrapper.eq(EmailRecord::getStatus, "Sent");
        long sent = emailRecordMapper.selectCount(wrapper);
        
        wrapper.eq(EmailRecord::getStatus, "Opened");
        long opened = emailRecordMapper.selectCount(wrapper);
        
        wrapper.eq(EmailRecord::getStatus, "Replied");
        long replied = emailRecordMapper.selectCount(wrapper);
        
        analytics.put("total", total);
        analytics.put("sent", sent);
        analytics.put("opened", opened);
        analytics.put("replied", replied);
        analytics.put("openRate", sent > 0 ? String.format("%.2f", (double) opened / sent * 100) : "0.00");
        analytics.put("replyRate", sent > 0 ? String.format("%.2f", (double) replied / sent * 100) : "0.00");
        
        // 按模板统计回复率
        // TODO: 实现按模板的统计分析
        
        return analytics;
    }

    @Override
    public Map<String, Object> getWhatsappAnalytics() {
        Map<String, Object> analytics = new HashMap<>();
        
        LambdaQueryWrapper<WhatsappRecord> wrapper = new LambdaQueryWrapper<>();
        long total = whatsappRecordMapper.selectCount(wrapper);
        
        wrapper.eq(WhatsappRecord::getStatus, "Sent");
        long sent = whatsappRecordMapper.selectCount(wrapper);
        
        wrapper.eq(WhatsappRecord::getStatus, "Read");
        long read = whatsappRecordMapper.selectCount(wrapper);
        
        wrapper.eq(WhatsappRecord::getStatus, "Replied");
        long replied = whatsappRecordMapper.selectCount(wrapper);
        
        analytics.put("total", total);
        analytics.put("sent", sent);
        analytics.put("read", read);
        analytics.put("replied", replied);
        analytics.put("readRate", sent > 0 ? String.format("%.2f", (double) read / sent * 100) : "0.00");
        analytics.put("replyRate", sent > 0 ? String.format("%.2f", (double) replied / sent * 100) : "0.00");
        
        return analytics;
    }

    @Override
    public Map<String, Object> getConversionFunnel() {
        Map<String, Object> funnel = new LinkedHashMap<>();
        
        List<Map<String, Object>> statusStats = companyMapper.countByStatus();
        for (Map<String, Object> stat : statusStats) {
            funnel.put((String) stat.get("status"), stat.get("count"));
        }
        
        return funnel;
    }

    @Override
    public Map<String, Object> getSourceQualityAnalysis() {
        Map<String, Object> analysis = new HashMap<>();
        
        List<Map<String, Object>> sourceStats = companyMapper.countBySource();
        analysis.put("bySource", sourceStats);
        
        // 计算各来源的S/A级客户比例
        Map<String, Object> qualityBySource = new HashMap<>();
        for (Map<String, Object> source : sourceStats) {
            String sourceType = (String) source.get("source");
            LambdaQueryWrapper<Company> wrapper = new LambdaQueryWrapper<>();
            wrapper.eq(Company::getSource, sourceType);
            wrapper.in(Company::getLeadGrade, "S", "A");
            long highQuality = companyMapper.selectCount(wrapper);
            qualityBySource.put(sourceType, Map.of(
                "total", source.get("count"),
                "highQuality", highQuality,
                "qualityRate", (long) source.get("count") > 0 ? 
                    String.format("%.2f", (double) highQuality / (long) source.get("count") * 100) : "0.00"
            ));
        }
        analysis.put("qualityBySource", qualityBySource);
        
        return analysis;
    }

    @Override
    public Map<String, Object> getProductInterestAnalysis() {
        Map<String, Object> analysis = new HashMap<>();
        // TODO: 实现产品兴趣分析
        analysis.put("topProducts", List.of(
            Map.of("product", "Mirror Covers", "interest", 45),
            Map.of("product", "Front Grilles", "interest", 38),
            Map.of("product", "Bumper Assemblies", "interest", 32),
            Map.of("product", "Fenders", "interest", 25)
        ));
        return analysis;
    }

    @Override
    public Map<String, Object> getDailyTrend(int days) {
        Map<String, Object> trend = new HashMap<>();
        LocalDate endDate = LocalDate.now();
        LocalDate startDate = endDate.minusDays(days);
        
        LambdaQueryWrapper<DailyStats> wrapper = new LambdaQueryWrapper<>();
        wrapper.ge(DailyStats::getStatDate, startDate);
        wrapper.le(DailyStats::getStatDate, endDate);
        wrapper.orderByAsc(DailyStats::getStatDate);
        List<DailyStats> stats = dailyStatsMapper.selectList(wrapper);
        
        trend.put("dates", stats.stream().map(DailyStats::getStatDate).toList());
        trend.put("newLeads", stats.stream().map(DailyStats::getNewLeads).toList());
        trend.put("emailsSent", stats.stream().map(DailyStats::getEmailsSent).toList());
        trend.put("replies", stats.stream().map(DailyStats::getNewReplies).toList());
        
        return trend;
    }

    @Override
    @Transactional
    @Scheduled(cron = "0 0 1 * * ?") // 每天凌晨1点执行
    public void generateDailyStats() {
        LocalDate yesterday = LocalDate.now().minusDays(1);
        LocalDateTime startOfDay = yesterday.atStartOfDay();
        LocalDateTime endOfDay = yesterday.atTime(23, 59, 59);
        
        DailyStats stats = new DailyStats();
        stats.setStatDate(yesterday);
        
        // 新增客户
        LambdaQueryWrapper<Company> companyWrapper = new LambdaQueryWrapper<>();
        companyWrapper.ge(Company::getCreatedAt, startOfDay);
        companyWrapper.le(Company::getCreatedAt, endOfDay);
        stats.setNewLeads(Math.toIntExact(companyMapper.selectCount(companyWrapper)));
        
        // 邮件统计
        LambdaQueryWrapper<EmailRecord> emailWrapper = new LambdaQueryWrapper<>();
        emailWrapper.ge(EmailRecord::getSentAt, startOfDay);
        emailWrapper.le(EmailRecord::getSentAt, endOfDay);
        stats.setEmailsSent(Math.toIntExact(emailRecordMapper.selectCount(emailWrapper)));
        
        // 保存统计
        dailyStatsMapper.insert(stats);
        log.info("Daily stats generated for {}", yesterday);
    }
}
