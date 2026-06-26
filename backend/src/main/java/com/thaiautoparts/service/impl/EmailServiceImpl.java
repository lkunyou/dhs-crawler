package com.thaiautoparts.service.impl;

import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.ContactPerson;
import com.thaiautoparts.entity.EmailRecord;
import com.thaiautoparts.entity.EmailTemplate;
import com.thaiautoparts.entity.FollowUpRecord;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.ContactPersonMapper;
import com.thaiautoparts.repository.EmailRecordMapper;
import com.thaiautoparts.repository.EmailTemplateMapper;
import com.thaiautoparts.repository.FollowUpRecordMapper;
import com.thaiautoparts.service.EmailService;
import jakarta.mail.*;
import jakarta.mail.internet.MimeMessage;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class EmailServiceImpl implements EmailService {

    private final EmailRecordMapper emailRecordMapper;
    private final EmailTemplateMapper emailTemplateMapper;
    private final CompanyMapper companyMapper;
    private final ContactPersonMapper contactPersonMapper;
    private final FollowUpRecordMapper followUpRecordMapper;

    @Value("${spring.mail.host-smtp}")
    private String mailHostSmtp;

    @Value("${spring.mail.port-smtp:465}")
    private int mailPortSmtp;

    @Value("${spring.mail.username}")
    private String mailUsername;

    @Value("${spring.mail.password}")
    private String mailPassword;

    private Session createSmtpSession() {
        Properties props = new Properties();
        props.setProperty("mail.transport.protocol", "smtp");
        props.setProperty("mail.smtp.host", mailHostSmtp);
        props.setProperty("mail.smtp.port", String.valueOf(mailPortSmtp));
        props.setProperty("mail.smtp.auth", "true");
        props.setProperty("mail.smtp.ssl.enable", "true");
        props.setProperty("mail.smtp.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
        props.setProperty("mail.smtp.socketFactory.fallback", "false");
        props.setProperty("mail.smtp.connectiontimeout", "5000");
        props.setProperty("mail.smtp.timeout", "5000");
        
        return Session.getInstance(props, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(mailUsername, mailPassword);
            }
        });
    }

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

        Transport transport = null;
        try {
            Session session = createSmtpSession();
            MimeMessage message = new MimeMessage(session);
            message.setFrom(new jakarta.mail.internet.InternetAddress(mailUsername));
            message.setRecipient(Message.RecipientType.TO, new jakarta.mail.internet.InternetAddress(recipientEmail));
            message.setSubject(template.getSubject(), "UTF-8");
            message.setContent(content, "text/html; charset=UTF-8");
            message.setHeader("X-Tracking-ID", trackingId);
            
            transport = session.getTransport();
            transport.connect();
            transport.sendMessage(message, message.getAllRecipients());
            
            record.setStatus("Sent");
            record.setSentAt(LocalDateTime.now());
            record.setMessageId(message.getMessageID());
            emailRecordMapper.updateById(record);
            
            // 插入跟进记录
            FollowUpRecord followUp = new FollowUpRecord();
            followUp.setCompanyId(companyId);
            followUp.setContactId(contactId);
            followUp.setFollowUpType("Email");
            followUp.setDirection("Outbound");
            followUp.setSummary("发送邮件: " + template.getSubject());
            followUp.setDetail(content);
            followUp.setOutcome("Sent");
            followUpRecordMapper.insert(followUp);
            
            log.info("Email sent to {} for company {}", recipientEmail, companyId);
        } catch (Exception e) {
            record.setStatus("Failed");
            record.setErrorMessage(e.getMessage());
            emailRecordMapper.updateById(record);
            
            // 插入跟进记录
            FollowUpRecord followUp = new FollowUpRecord();
            followUp.setCompanyId(companyId);
            followUp.setContactId(contactId);
            followUp.setFollowUpType("Email");
            followUp.setDirection("Outbound");
            followUp.setSummary("发送邮件失败: " + template.getSubject());
            followUp.setDetail(content);
            followUp.setOutcome("Failed");
            followUpRecordMapper.insert(followUp);
            
            log.error("Failed to send email to {}: {}", recipientEmail, e.getMessage());
        } finally {
            if (transport != null) {
                try {
                    transport.close();
                } catch (Exception e) {
                    log.error("Failed to close transport: {}", e.getMessage());
                }
            }
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
    public List<EmailRecord> getAllEmailRecords() {
        LambdaQueryWrapper<EmailRecord> wrapper = new LambdaQueryWrapper<>();
        wrapper.orderByDesc(EmailRecord::getCreatedAt);
        return emailRecordMapper.selectList(wrapper);
    }

    @Override
    public PageResult<EmailRecord> getAllEmailRecords(int page, int size, String email, String username, String startDate, String endDate) {
        LambdaQueryWrapper<EmailRecord> wrapper = new LambdaQueryWrapper<>();
        
        if (StrUtil.isNotBlank(email)) {
            wrapper.like(EmailRecord::getRecipientEmail, email);
        }
        
        if (StrUtil.isNotBlank(username)) {
            wrapper.like(EmailRecord::getSubject, username);
        }
        
        if (StrUtil.isNotBlank(startDate)) {
            LocalDateTime startDateTime = LocalDate.parse(startDate, DateTimeFormatter.ofPattern("yyyy-MM-dd")).atStartOfDay();
            wrapper.ge(EmailRecord::getCreatedAt, startDateTime);
        }
        
        if (StrUtil.isNotBlank(endDate)) {
            LocalDateTime endDateTime = LocalDate.parse(endDate, DateTimeFormatter.ofPattern("yyyy-MM-dd")).atTime(23, 59, 59);
            wrapper.le(EmailRecord::getCreatedAt, endDateTime);
        }
        
        wrapper.orderByDesc(EmailRecord::getCreatedAt);
        
        IPage<EmailRecord> pageResult = new Page<>(page, size);
        IPage<EmailRecord> result = emailRecordMapper.selectPage(pageResult, wrapper);
        
        List<EmailRecord> records = result.getRecords();
        for (EmailRecord record : records) {
            if (record.getCompanyId() != null) {
                Company company = companyMapper.selectById(record.getCompanyId());
                if (company != null) {
                    record.setCompanyName(company.getCompanyName());
                }
            }
            if (record.getContactId() != null) {
                ContactPerson contact = contactPersonMapper.selectById(record.getContactId());
                if (contact != null) {
                    record.setRecipientName(contact.getFullName());
                }
            }
        }
        
        return new PageResult<>(result.getTotal(), (int) result.getCurrent(), (int) result.getSize(), records);
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