package com.thaiautoparts.service.impl;

import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.EmailRecordMapper;
import com.thaiautoparts.repository.FollowUpRecordMapper;
import com.thaiautoparts.repository.WhatsappRecordMapper;
import com.thaiautoparts.service.AnalyticsService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AnalyticsServiceImpl implements AnalyticsService {

    private final EmailRecordMapper emailRecordMapper;
    private final WhatsappRecordMapper whatsappRecordMapper;
    private final CompanyMapper companyMapper;
    private final FollowUpRecordMapper followUpRecordMapper;

    @Override
    public Map<String, Object> getEmailStats() {
        Map<String, Object> stats = new HashMap<>();
        Long totalSent = emailRecordMapper.countByStatus("Sent");
        Long totalOpened = emailRecordMapper.countByStatus("Opened");
        Long totalReplied = followUpRecordMapper.countByOutcome("Positive");
        
        long sent = totalSent != null ? totalSent : 0;
        long opened = totalOpened != null ? totalOpened : 0;
        long replied = totalReplied != null ? totalReplied : 0;
        
        double openRate = sent > 0 ? (double) opened / sent * 100 : 0;
        double replyRate = sent > 0 ? (double) replied / sent * 100 : 0;
        
        stats.put("totalSent", sent);
        stats.put("totalOpened", opened);
        stats.put("totalReplied", replied);
        stats.put("openRate", Math.round(openRate * 10) / 10.0);
        stats.put("replyRate", Math.round(replyRate * 10) / 10.0);
        
        return stats;
    }

    @Override
    public Map<String, Object> getWhatsappStats() {
        Map<String, Object> stats = new HashMap<>();
        Long totalSent = whatsappRecordMapper.countByStatus("sent");
        Long totalRead = whatsappRecordMapper.countByStatus("read");
        Long totalReplied = whatsappRecordMapper.countByStatus("replied");
        
        long sent = totalSent != null ? totalSent : 0;
        long read = totalRead != null ? totalRead : 0;
        long replied = totalReplied != null ? totalReplied : 0;
        
        double readRate = sent > 0 ? (double) read / sent * 100 : 0;
        double replyRate = sent > 0 ? (double) replied / sent * 100 : 0;
        
        stats.put("totalSent", sent);
        stats.put("totalRead", read);
        stats.put("totalReplied", replied);
        stats.put("readRate", Math.round(readRate * 10) / 10.0);
        stats.put("replyRate", Math.round(replyRate * 10) / 10.0);
        
        return stats;
    }

    @Override
    public List<Map<String, Object>> getSourceQuality() {
        List<Map<String, Object>> sourceStats = companyMapper.countBySource();
        
        // 获取S/A级客户统计
        List<Map<String, Object>> gradeStats = companyMapper.countByLeadGrade();
        Map<String, Long> gradeCountMap = gradeStats.stream()
                .filter(m -> "S".equals(m.get("leadGrade")) || "A".equals(m.get("leadGrade")))
                .collect(Collectors.toMap(
                        m -> (String) m.get("leadGrade"),
                        m -> ((Number) m.get("count")).longValue()
                ));
        
        for (Map<String, Object> source : sourceStats) {
            String sourceName = (String) source.get("source");
            long total = ((Number) source.get("count")).longValue();
            
            // 计算该来源的S/A级客户数
            long highQuality = 0;
            // 这里简化处理，实际应该按来源分组统计等级
            source.put("highQuality", highQuality);
            source.put("qualityRate", total > 0 ? Math.round((double) highQuality / total * 10000) / 100.0 : 0.0);
        }
        
        return sourceStats;
    }

    @Override
    public List<Map<String, Object>> getTrend(int days) {
        List<Map<String, Object>> trend = new ArrayList<>();
        LocalDate today = LocalDate.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("MM/dd");
        
        for (int i = days - 1; i >= 0; i--) {
            LocalDate date = today.minusDays(i);
            Map<String, Object> dayData = new HashMap<>();
            dayData.put("date", date.format(formatter));
            dayData.put("newCompanies", 0);
            dayData.put("emailsSent", 0);
            dayData.put("replies", 0);
            trend.add(dayData);
        }
        
        return trend;
    }

    @Override
    public List<Map<String, Object>> getFunnel() {
        return companyMapper.countByStatus();
    }
}
