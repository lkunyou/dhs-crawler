package com.thaiautoparts.service;

import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.entity.EmailRecord;
import java.util.List;
import java.util.Map;

public interface EmailService {
    void sendEmail(Long companyId, Long contactId, Long templateId);
    void sendBatchEmail(List<Long> companyIds, Long templateId);
    void sendCustomEmail(String toEmail, String subject, String content, boolean isHtml, Long companyId, Long templateId, Long inReplyToEmailId);
    List<EmailRecord> getEmailRecords(Long companyId);
    List<EmailRecord> getAllEmailRecords();
    PageResult<EmailRecord> getAllEmailRecords(int page, int size, String email, String username, String startDate, String endDate);
    Map<String, Object> getEmailStats();
    void handleEmailOpened(String trackingId);
    void handleEmailReplied(String trackingId, String replyContent);
    List<EmailRecord> getRepliesByEmailId(Long emailId);
}
