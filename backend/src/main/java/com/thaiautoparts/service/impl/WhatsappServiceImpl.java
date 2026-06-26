package com.thaiautoparts.service.impl;

import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.FollowUpRecord;
import com.thaiautoparts.entity.WhatsappRecord;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.FollowUpRecordMapper;
import com.thaiautoparts.repository.WhatsappRecordMapper;
import com.thaiautoparts.service.SystemConfigService;
import com.thaiautoparts.service.WhatsappService;
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
public class WhatsappServiceImpl implements WhatsappService {

    private final WhatsappRecordMapper whatsappRecordMapper;
    private final CompanyMapper companyMapper;
    private final FollowUpRecordMapper followUpRecordMapper;
    private final SystemConfigService systemConfigService;
    
    @Value("${app.whatsapp.api-url:https://api.whatsapp.com}")
    private String whatsappApiUrlYml;
    
    @Value("${app.whatsapp.api-token:}")
    private String whatsappApiTokenYml;

    private String getWhatsappConfig(String key, String defaultValue) {
        return systemConfigService.getValue(key, defaultValue);
    }

    @Override
    @Async
    public void sendTextMessage(Long companyId, Long contactId, String phoneNumber, String content) {
        Company company = companyMapper.selectById(companyId);
        if (company == null) {
            log.error("Company not found: {}", companyId);
            return;
        }

        WhatsappRecord record = new WhatsappRecord();
        record.setCompanyId(companyId);
        record.setContactId(contactId);
        record.setPhoneNumber(phoneNumber);
        record.setMessageType("Text");
        record.setContent(content);
        record.setDirection("Outbound");
        record.setStatus("Pending");
        whatsappRecordMapper.insert(record);

        try {
            // TODO: 接入WhatsApp Business API (Cloud API / Twilio / 360dialog)
            // 这里模拟发送成功
            String messageId = "WA_" + System.currentTimeMillis();
            
            record.setStatus("Sent");
            record.setSentAt(LocalDateTime.now());
            record.setMessageId(messageId);
            whatsappRecordMapper.updateById(record);
            
            // 插入跟进记录
            FollowUpRecord followUp = new FollowUpRecord();
            followUp.setCompanyId(companyId);
            followUp.setContactId(contactId);
            followUp.setFollowUpType("WhatsApp");
            followUp.setDirection("Outbound");
            followUp.setSummary("发送WhatsApp消息");
            followUp.setDetail(content);
            followUp.setOutcome("Sent");
            followUpRecordMapper.insert(followUp);
            
            // 更新公司状态
            if ("New".equals(company.getStatus())) {
                company.setStatus("Contacted");
                company.setLastContactedAt(LocalDateTime.now());
                companyMapper.updateById(company);
            }
            
            log.info("WhatsApp sent to {} for company {}", phoneNumber, companyId);
        } catch (Exception e) {
            record.setStatus("Failed");
            record.setErrorMessage(e.getMessage());
            whatsappRecordMapper.updateById(record);
            
            // 插入跟进记录
            FollowUpRecord followUp = new FollowUpRecord();
            followUp.setCompanyId(companyId);
            followUp.setContactId(contactId);
            followUp.setFollowUpType("WhatsApp");
            followUp.setDirection("Outbound");
            followUp.setSummary("发送WhatsApp消息失败");
            followUp.setDetail(content);
            followUp.setOutcome("Failed");
            followUpRecordMapper.insert(followUp);
            
            log.error("Failed to send WhatsApp to {}: {}", phoneNumber, e.getMessage());
        }
    }

    @Override
    @Async
    public void sendImageMessage(Long companyId, Long contactId, String phoneNumber, String imageUrl, String caption) {
        WhatsappRecord record = new WhatsappRecord();
        record.setCompanyId(companyId);
        record.setContactId(contactId);
        record.setPhoneNumber(phoneNumber);
        record.setMessageType("Image");
        record.setContent(caption);
        record.setMediaUrl(imageUrl);
        record.setDirection("Outbound");
        record.setStatus("Pending");
        whatsappRecordMapper.insert(record);

        try {
            // TODO: 接入WhatsApp Business API发送图片
            String messageId = "WA_" + System.currentTimeMillis();
            record.setStatus("Sent");
            record.setSentAt(LocalDateTime.now());
            record.setMessageId(messageId);
            whatsappRecordMapper.updateById(record);
            log.info("WhatsApp image sent to {} for company {}", phoneNumber, companyId);
        } catch (Exception e) {
            record.setStatus("Failed");
            record.setErrorMessage(e.getMessage());
            whatsappRecordMapper.updateById(record);
        }
    }

    @Override
    @Async
    public void sendBatchMessages(List<Long> companyIds, String templateContent) {
        log.info("Starting batch WhatsApp send for {} companies", companyIds.size());
        for (Long companyId : companyIds) {
            try {
                Company company = companyMapper.selectById(companyId);
                if (company != null && StrUtil.isNotBlank(company.getWhatsapp())) {
                    sendTextMessage(companyId, null, company.getWhatsapp(), templateContent);
                    Thread.sleep(3000); // 避免发送过快
                }
            } catch (Exception e) {
                log.error("Failed to send WhatsApp to company {}: {}", companyId, e.getMessage());
            }
        }
        log.info("Batch WhatsApp send completed");
    }

    @Override
    public List<WhatsappRecord> getMessageRecords(Long companyId) {
        LambdaQueryWrapper<WhatsappRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(WhatsappRecord::getCompanyId, companyId);
        wrapper.orderByDesc(WhatsappRecord::getCreatedAt);
        return whatsappRecordMapper.selectList(wrapper);
    }

    @Override
    public Map<String, Object> getWhatsappStats() {
        Map<String, Object> stats = new HashMap<>();
        
        LambdaQueryWrapper<WhatsappRecord> wrapper = new LambdaQueryWrapper<>();
        long total = whatsappRecordMapper.selectCount(wrapper);
        
        wrapper.eq(WhatsappRecord::getStatus, "Sent");
        long sent = whatsappRecordMapper.selectCount(wrapper);
        
        wrapper.eq(WhatsappRecord::getStatus, "Read");
        long read = whatsappRecordMapper.selectCount(wrapper);
        
        wrapper.eq(WhatsappRecord::getStatus, "Replied");
        long replied = whatsappRecordMapper.selectCount(wrapper);
        
        stats.put("total", total);
        stats.put("sent", sent);
        stats.put("read", read);
        stats.put("replied", replied);
        stats.put("readRate", sent > 0 ? String.format("%.2f", (double) read / sent * 100) : "0.00");
        stats.put("replyRate", sent > 0 ? String.format("%.2f", (double) replied / sent * 100) : "0.00");
        
        return stats;
    }

    @Override
    @Transactional
    public void handleDelivery(String messageId) {
        LambdaQueryWrapper<WhatsappRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(WhatsappRecord::getMessageId, messageId);
        WhatsappRecord record = whatsappRecordMapper.selectOne(wrapper);
        
        if (record != null && "Sent".equals(record.getStatus())) {
            record.setStatus("Delivered");
            record.setDeliveredAt(LocalDateTime.now());
            whatsappRecordMapper.updateById(record);
        }
    }

    @Override
    @Transactional
    public void handleRead(String messageId) {
        LambdaQueryWrapper<WhatsappRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(WhatsappRecord::getMessageId, messageId);
        WhatsappRecord record = whatsappRecordMapper.selectOne(wrapper);
        
        if (record != null && ("Sent".equals(record.getStatus()) || "Delivered".equals(record.getStatus()))) {
            record.setStatus("Read");
            record.setReadAt(LocalDateTime.now());
            whatsappRecordMapper.updateById(record);
        }
    }

    @Override
    @Transactional
    public void handleReply(String messageId, String replyContent) {
        LambdaQueryWrapper<WhatsappRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(WhatsappRecord::getMessageId, messageId);
        WhatsappRecord record = whatsappRecordMapper.selectOne(wrapper);
        
        if (record != null) {
            record.setStatus("Replied");
            record.setRepliedAt(LocalDateTime.now());
            record.setReplyContent(replyContent);
            whatsappRecordMapper.updateById(record);
            
            Company company = companyMapper.selectById(record.getCompanyId());
            if (company != null && "Contacted".equals(company.getStatus())) {
                company.setStatus("Replied");
                companyMapper.updateById(company);
            }
            
            log.info("WhatsApp replied for message: {}", messageId);
        }
    }
}
