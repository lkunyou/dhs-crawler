package com.thaiautoparts.service.impl;

import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.ContactPerson;
import com.thaiautoparts.entity.EmailRecord;
import com.thaiautoparts.entity.EmailTemplate;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.ContactPersonMapper;
import com.thaiautoparts.repository.EmailRecordMapper;
import com.thaiautoparts.repository.EmailTemplateMapper;
import com.thaiautoparts.service.EmailService;
import jakarta.mail.MessagingException;
import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class EmailServiceImpl implements EmailService {

    private final JavaMailSender mailSender;
    private final EmailRecordMapper emailRecordMapper;
    private final EmailTemplateMapper emailTemplateMapper;
    private final CompanyMapper companyMapper;
    private final ContactPersonMapper contactPersonMapper;

    @Override
    @Async
    public void sendEmail(Long companyId, Long contactId, Long templateId) {
        Company company = companyMapper.selectById(companyId);
        if (company == null) {
            log.error("Company not found: {}", companyId);
            return;
        }

        ContactPerson contact = contactId != null ? contactPersonMapper.selectById(contactId) : null;
        EmailTemplate template = emailTemplateMapper.selectById(templateId);
        if (template == null) {
            log.error("Email template not found: {}", templateId);
            return;
        }

        String recipientEmail = contact != null && StrUtil.isNotBlank(contact.getEmail()) 
                ? contact.getEmail() : company.getEmail();
        
        if (StrUtil.isBlank(recipientEmail)) {
            log.error("No email address for company: {}", companyId);
            return;
        }

        String trackingId = UUID.randomUUID().toString();
        String content = template.getContent()
                .replace("[Name]", contact != null ? contact.getFullName() : "Sir/Madam")
                .replace("[Your Company]", "Your Company Name")
                .replace("[Your Name]", "Your Name")
                .replace("[Your Title]", "Sales Manager")
                .replace("[Number]", "+86-xxx-xxxx-xxxx");

        EmailRecord record = new EmailRecord();
        record.setCampaignId(null);
        record.setCompanyId(companyId);
        record.setContactId(contactId);
        record.setTemplateId(templateId);
        record.setRecipientEmail(recipientEmail);
        record.setSubject(template.getSubject());
        record.setContent(content);
        record.setStatus("Pending");
        record.setTrackingId(trackingId);
        emailRecordMapper.insert(record);

        try {
            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");
            helper.setFrom("your-email@gmail.com");
            helper.setTo(recipientEmail);
            helper.setSubject(template.getSubject());
            helper.setText(content, true);
            
            message.setHeader("X-Tracking-ID", trackingId);
            
            mailSender.send(message);
            
            record.setStatus("Sent");
            record.setSentAt(LocalDateTime.now());
            record.setMessageId(message.getMessageID());
            emailRecordMapper.updateById(record);
            
            log.info("Email sent to {} for company {}", recipientEmail, companyId);
        } catch (MessagingException e) {
            record.setStatus("Failed");
            record.setErrorMessage(e.getMessage());
            emailRecordMapper.updateById(record);
            log.error("Failed to send email to {}: {}", recipientEmail, e.getMessage());
        }
    }

    @Override
    @Async
    public void sendBatchEmail(List<Long> companyIds, Long templateId) {
        log.info("Starting batch email send for {} companies", companyIds.size());
        for (Long companyId : companyIds) {
            try {
                sendEmail(companyId, null, templateId);
                Thread.sleep(1000);
            } catch (Exception e) {
                log.error("Failed to send email to company {}: {}", companyId, e.getMessage());
            }
        }
        log.info("Batch email send completed");
    }

    @Override
    public List<EmailRecord> getEmailRecords(Long companyId) {
        LambdaQueryWrapper<EmailRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(EmailRecord::getCompanyId, companyId);
        wrapper.orderByDesc(EmailRecord::getCreatedAt);
        return emailRecordMapper.selectList(wrapper);
    }

    @Override
    public Map<String, Object> getEmailStats() {
        Map<String, Object> stats = new HashMap<>();
        
        LambdaQueryWrapper<EmailRecord> wrapper = new LambdaQueryWrapper<>();
        long total = emailRecordMapper.selectCount(wrapper);
        
        wrapper.eq(EmailRecord::getStatus, "Sent");
        long sent = emailRecordMapper.selectCount(wrapper);
        
        wrapper.eq(EmailRecord::getStatus, "Opened");
        long opened = emailRecordMapper.selectCount(wrapper);
        
        wrapper.eq(EmailRecord::getStatus, "Replied");
        long replied = emailRecordMapper.selectCount(wrapper);
        
        stats.put("total", total);
        stats.put("sent", sent);
        stats.put("opened", opened);
        stats.put("replied", replied);
        stats.put("openRate", sent > 0 ? String.format("%.2f", (double) opened / sent * 100) : "0.00");
        stats.put("replyRate", sent > 0 ? String.format("%.2f", (double) replied / sent * 100) : "0.00");
        
        return stats;
    }

    @Override
    @Transactional
    public void handleEmailOpened(String trackingId) {
        LambdaQueryWrapper<EmailRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(EmailRecord::getTrackingId, trackingId);
        EmailRecord record = emailRecordMapper.selectOne(wrapper);
        
        if (record != null && ("Sent".equals(record.getStatus()) || "Delivered".equals(record.getStatus()))) {
            record.setStatus("Opened");
            record.setOpenedAt(LocalDateTime.now());
            emailRecordMapper.updateById(record);
            log.info("Email opened: {}", trackingId);
        }
    }

    @Override
    @Transactional
    public void handleEmailReplied(String trackingId, String replyContent) {
        LambdaQueryWrapper<EmailRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(EmailRecord::getTrackingId, trackingId);
        EmailRecord record = emailRecordMapper.selectOne(wrapper);
        
        if (record != null) {
            record.setStatus("Replied");
            record.setRepliedAt(LocalDateTime.now());
            record.setReplyContent(replyContent);
            emailRecordMapper.updateById(record);
            
            Company company = companyMapper.selectById(record.getCompanyId());
            if (company != null && "Contacted".equals(company.getStatus())) {
                company.setStatus("Replied");
                companyMapper.updateById(company);
            }
            
            log.info("Email replied: {}", trackingId);
        }
    }
}
