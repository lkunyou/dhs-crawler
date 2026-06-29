package com.thaiautoparts.service.impl;

import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.config.TwilioConfig;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.FollowUpRecord;
import com.thaiautoparts.entity.WhatsappRecord;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.FollowUpRecordMapper;
import com.thaiautoparts.repository.WhatsappRecordMapper;
import com.thaiautoparts.service.SystemConfigService;
import com.thaiautoparts.service.WhatsappService;
import com.twilio.rest.api.v2010.account.Message;
import com.twilio.type.PhoneNumber;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.net.URI;
import java.net.URISyntaxException;
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
    private final TwilioConfig twilioConfig;
    
    @Value("${app.whatsapp.api-url:https://api.whatsapp.com}")
    private String whatsappApiUrlYml;
    
    @Value("${app.whatsapp.api-token:}")
    private String whatsappApiTokenYml;

    private String getWhatsappConfig(String key, String defaultValue) {
        return systemConfigService.getValue(key, defaultValue);
    }
    
    private String formatPhoneNumber(String phoneNumber) {
        if (StrUtil.isBlank(phoneNumber)) {
            return null;
        }
        String cleaned = phoneNumber;//phoneNumber.replaceAll("[^0-9]", "");
        if (cleaned.startsWith("+")) {
            return cleaned;
        }
        if (cleaned.startsWith("0")) {
           // return "+66" + cleaned.substring(1);
        }
        if (cleaned.startsWith("66")) {
           // return "+" + cleaned;
        }
      //  return "+66" + cleaned;
        return cleaned;
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
            String formattedPhone = formatPhoneNumber(phoneNumber);
            if (formattedPhone == null) {
                throw new IllegalArgumentException("Invalid phone number: " + phoneNumber);
            }
            
            String messageId;
            if (twilioConfig.isConfigured()) {
                try {
                    Message message = Message.creator(
                            new PhoneNumber("whatsapp:" + formattedPhone),
                            new PhoneNumber("whatsapp:" + twilioConfig.getWhatsappNumber()),
                            content
                    ).create();
                    messageId = message.getSid();
                    log.info("Twilio WhatsApp message sent, SID: {}", messageId);
                } catch (com.twilio.exception.ApiException e) {
                    log.error("Twilio API error: {} - {}", e.getCode(), e.getMessage());
                    if (e.getCode() == 20003) {
                        log.error("Twilio authentication failed - please check your Account SID and Auth Token");
                    } else if (e.getCode() == 63007) {
                        log.error("Twilio WhatsApp channel not found - please check your WhatsApp number: {}", twilioConfig.getWhatsappNumber());
                        log.error("Ensure the number is configured in Twilio console with WhatsApp capability");
                    }
                    throw e;
                }
            } else {
                messageId = "WA_" + System.currentTimeMillis();
                log.info("Twilio not configured, using mock mode, messageId: {}", messageId);
            }
            
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
            String formattedPhone = formatPhoneNumber(phoneNumber);
            if (formattedPhone == null) {
                throw new IllegalArgumentException("Invalid phone number: " + phoneNumber);
            }
            
            String messageId;
            if (twilioConfig.isConfigured()) {
                try {
                    URI mediaUri = new URI(imageUrl);
                    Message message = Message.creator(
                            new PhoneNumber("whatsapp:" + formattedPhone),
                            new PhoneNumber("whatsapp:" + twilioConfig.getWhatsappNumber()),
                            caption
                    ).setMediaUrl(List.of(mediaUri)).create();
                    messageId = message.getSid();
                    log.info("Twilio WhatsApp image sent, SID: {}", messageId);
                } catch (URISyntaxException e) {
                    throw new IllegalArgumentException("Invalid image URL: " + imageUrl, e);
                }
            } else {
                messageId = "WA_" + System.currentTimeMillis();
                log.info("Twilio not configured, using mock mode, messageId: {}", messageId);
            }
            
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
    public List<WhatsappRecord> getAllMessageRecords() {
        LambdaQueryWrapper<WhatsappRecord> wrapper = new LambdaQueryWrapper<>();
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
