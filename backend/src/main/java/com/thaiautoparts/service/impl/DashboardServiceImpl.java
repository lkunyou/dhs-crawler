package com.thaiautoparts.service.impl;

import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.EmailRecordMapper;
import com.thaiautoparts.repository.FollowUpRecordMapper;
import com.thaiautoparts.service.DashboardService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
@RequiredArgsConstructor
public class DashboardServiceImpl implements DashboardService {

    private final CompanyMapper companyMapper;
    private final EmailRecordMapper emailRecordMapper;
    private final FollowUpRecordMapper followUpRecordMapper;

    @Override
    public Map<String, Object> getDashboardStats() {
        Map<String, Object> stats = new HashMap<>();
        
        // 总客户数
        Long totalCompanies = companyMapper.countTotal();
        stats.put("totalCompanies", totalCompanies != null ? totalCompanies : 0);
        
        // 邮件已发送数（状态为 sent）
        Long emailsSent = emailRecordMapper.countByStatus("Sent");
        stats.put("emailsSent", emailsSent != null ? emailsSent : 0);
        
        // 客户回复数（跟进结果为 Positive）
        Long replies = followUpRecordMapper.countByOutcome("Positive");
        stats.put("replies", replies != null ? replies : 0);
        
        // WhatsApp发送数（暂时用跟进记录数替代）
        Long whatsappSent = followUpRecordMapper.countByType("whatsapp");
        stats.put("whatsappSent", whatsappSent != null ? whatsappSent : 0);
        
        return stats;
    }

    @Override
    public List<Map<String, Object>> getGradeDistribution() {
        return companyMapper.countByLeadGrade();
    }

    @Override
    public List<Map<String, Object>> getSourceDistribution() {
        return companyMapper.countBySource();
    }

    @Override
    public List<Map<String, Object>> getFunnelData() {
        return companyMapper.countByStatus();
    }
}
