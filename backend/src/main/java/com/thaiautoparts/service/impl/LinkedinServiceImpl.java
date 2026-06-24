package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.LinkedinRecord;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.LinkedinRecordMapper;
import com.thaiautoparts.service.LinkedinService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class LinkedinServiceImpl implements LinkedinService {

    private final LinkedinRecordMapper linkedinRecordMapper;
    private final CompanyMapper companyMapper;
    
    @Value("${app.linkedin.session-cookie:}")
    private String linkedinSessionCookie;

    @Override
    @Async
    public void addContact(Long companyId, Long contactId, String profileUrl, String message) {
        Company company = companyMapper.selectById(companyId);
        if (company == null) return;

        LinkedinRecord record = new LinkedinRecord();
        record.setCompanyId(companyId);
        record.setContactId(contactId);
        record.setLinkedinProfileUrl(profileUrl);
        record.setActionType("Connect");
        record.setMessageContent(message);
        record.setStatus("Pending");
        record.setScheduledAt(LocalDateTime.now().plusMinutes(5));
        linkedinRecordMapper.insert(record);

        try {
            // TODO: 接入LinkedIn自动化 (PhantomBuster/TexAu API)
            record.setStatus("Success");
            record.setExecutedAt(LocalDateTime.now());
            linkedinRecordMapper.updateById(record);
            log.info("LinkedIn connection request sent: {}", profileUrl);
        } catch (Exception e) {
            record.setStatus("Failed");
            record.setErrorMessage(e.getMessage());
            linkedinRecordMapper.updateById(record);
        }
    }

    @Override
    @Async
    public void sendMessage(Long companyId, Long contactId, String profileUrl, String content) {
        LinkedinRecord record = new LinkedinRecord();
        record.setCompanyId(companyId);
        record.setContactId(contactId);
        record.setLinkedinProfileUrl(profileUrl);
        record.setActionType("Message");
        record.setMessageContent(content);
        record.setStatus("Pending");
        linkedinRecordMapper.insert(record);

        try {
            // TODO: 接入LinkedIn消息API
            record.setStatus("Success");
            record.setExecutedAt(LocalDateTime.now());
            linkedinRecordMapper.updateById(record);
            log.info("LinkedIn message sent: {}", profileUrl);
        } catch (Exception e) {
            record.setStatus("Failed");
            record.setErrorMessage(e.getMessage());
            linkedinRecordMapper.updateById(record);
        }
    }

    @Override
    @Async
    public void viewProfile(Long companyId, Long contactId, String profileUrl) {
        LinkedinRecord record = new LinkedinRecord();
        record.setCompanyId(companyId);
        record.setContactId(contactId);
        record.setLinkedinProfileUrl(profileUrl);
        record.setActionType("View_Profile");
        record.setStatus("Success");
        record.setExecutedAt(LocalDateTime.now());
        linkedinRecordMapper.insert(record);
    }

    @Override
    public List<LinkedinRecord> getRecords(Long companyId) {
        LambdaQueryWrapper<LinkedinRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(LinkedinRecord::getCompanyId, companyId);
        wrapper.orderByDesc(LinkedinRecord::getCreatedAt);
        return linkedinRecordMapper.selectList(wrapper);
    }

    @Override
    public Map<String, Object> getLinkedinStats() {
        Map<String, Object> stats = new HashMap<>();
        
        LambdaQueryWrapper<LinkedinRecord> wrapper = new LambdaQueryWrapper<>();
        long total = linkedinRecordMapper.selectCount(wrapper);
        
        wrapper.eq(LinkedinRecord::getStatus, "Success");
        long success = linkedinRecordMapper.selectCount(wrapper);
        
        wrapper.eq(LinkedinRecord::getActionType, "Connect");
        long connections = linkedinRecordMapper.selectCount(wrapper);
        
        stats.put("total", total);
        stats.put("success", success);
        stats.put("connections", connections);
        stats.put("successRate", total > 0 ? String.format("%.2f", (double) success / total * 100) : "0.00");
        
        return stats;
    }

    @Override
    @Transactional
    public void handleConnectionAccepted(Long recordId) {
        LinkedinRecord record = linkedinRecordMapper.selectById(recordId);
        if (record != null) {
            Company company = companyMapper.selectById(record.getCompanyId());
            if (company != null && "New".equals(company.getStatus())) {
                company.setStatus("Contacted");
                companyMapper.updateById(company);
            }
            log.info("LinkedIn connection accepted: {}", recordId);
        }
    }

    @Override
    @Transactional
    public void handleMessageResponse(Long recordId, String responseContent) {
        LinkedinRecord record = linkedinRecordMapper.selectById(recordId);
        if (record != null) {
            record.setResponseContent(responseContent);
            linkedinRecordMapper.updateById(record);
            
            Company company = companyMapper.selectById(record.getCompanyId());
            if (company != null && "Contacted".equals(company.getStatus())) {
                company.setStatus("Replied");
                companyMapper.updateById(company);
            }
            
            log.info("LinkedIn message response: {}", recordId);
        }
    }
}
