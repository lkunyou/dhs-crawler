package com.thaiautoparts.controller;

import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.EmailRecord;
import com.thaiautoparts.entity.EmailTemplate;
import com.thaiautoparts.entity.InboundEmail;
import com.thaiautoparts.repository.EmailTemplateMapper;
import com.thaiautoparts.service.EmailReceiverService;
import com.thaiautoparts.service.EmailService;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/email")
@RequiredArgsConstructor
public class EmailController {

    private final EmailService emailService;
    private final EmailReceiverService emailReceiverService;
    private final EmailTemplateMapper emailTemplateMapper;

    @PostMapping("/send")
    public Result<Void> sendEmail(@RequestBody SendEmailRequest request) {
        emailService.sendEmail(request.getCompanyId(), request.getContactId(), request.getTemplateId());
        return Result.success();
    }

    @PostMapping("/send-batch")
    public Result<Void> sendBatchEmail(@RequestBody SendBatchEmailRequest request) {
        emailService.sendBatchEmail(request.getCompanyIds(), request.getTemplateId());
        return Result.success();
    }

    @PostMapping("/send-custom")
    public Result<Void> sendCustomEmail(@RequestBody SendCustomEmailRequest request) {
        emailService.sendCustomEmail(
            request.getToEmail(),
            request.getSubject(),
            request.getContent(),
            request.isHtml(),
            request.getCompanyId(),
            request.getTemplateId(),
            request.getInReplyToEmailId()
        );
        return Result.success();
    }

    @GetMapping("/replies/{emailId}")
    public Result<List<EmailRecord>> getRepliesByEmailId(@PathVariable Long emailId) {
        return Result.success(emailService.getRepliesByEmailId(emailId));
    }

    @GetMapping("/records/{companyId}")
    public Result<List<EmailRecord>> getRecords(@PathVariable Long companyId) {
        return Result.success(emailService.getEmailRecords(companyId));
    }

    @GetMapping("/records")
    public Result<PageResult<EmailRecord>> getAllRecords(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String email,
            @RequestParam(required = false) String username,
            @RequestParam(required = false) String startDate,
            @RequestParam(required = false) String endDate) {
        return Result.success(emailService.getAllEmailRecords(page, size, email, username, startDate, endDate));
    }

    @GetMapping("/stats")
    public Result<Map<String, Object>> getStats() {
        return Result.success(emailService.getEmailStats());
    }

    @GetMapping("/track/open")
    public Result<Void> trackOpen(@RequestParam String trackingId) {
        emailService.handleEmailOpened(trackingId);
        return Result.success();
    }

    @GetMapping("/inbox")
    public Result<List<InboundEmail>> getInbox() {
        return Result.success(emailReceiverService.getInbox());
    }

    @GetMapping("/inbox/latest")
    public Result<List<InboundEmail>> getLatestEmails(@RequestParam(defaultValue = "20") int limit) {
        return Result.success(emailReceiverService.getInboxWithLimit(limit));
    }

    @GetMapping("/inbox/unread")
    public Result<List<InboundEmail>> getUnreadEmails() {
        return Result.success(emailReceiverService.getUnreadEmails());
    }

    @GetMapping("/inbox/count")
    public Result<Integer> getUnreadCount() {
        return Result.success(emailReceiverService.getUnreadCount());
    }

    @GetMapping("/inbox/{id}")
    public Result<InboundEmail> getEmailById(@PathVariable Long id) {
        InboundEmail email = emailReceiverService.getEmailById(id);
        if (email != null) {
            emailReceiverService.markAsRead(id);
            return Result.success(email);
        }
        return Result.error("邮件不存在");
    }

    @PostMapping("/inbox/{id}/read")
    public Result<Void> markAsRead(@PathVariable Long id) {
        emailReceiverService.markAsRead(id);
        return Result.success();
    }

    @PostMapping("/inbox/{id}/star")
    public Result<Void> markAsStarred(@PathVariable Long id, @RequestParam boolean starred) {
        emailReceiverService.markAsStarred(id, starred);
        return Result.success();
    }

    @PostMapping("/inbox/{id}/priority")
    public Result<Void> setPriority(@PathVariable Long id, @RequestParam String priority) {
        emailReceiverService.setPriority(id, priority);
        return Result.success();
    }

    @PostMapping("/inbox/{id}/replied")
    public Result<Void> markAsReplied(@PathVariable Long id) {
        emailReceiverService.markAsReplied(id);
        return Result.success();
    }

    @DeleteMapping("/inbox/{id}")
    public Result<Void> deleteEmail(@PathVariable Long id) {
        emailReceiverService.deleteEmail(id);
        return Result.success();
    }

    @PostMapping("/inbox/fetch")
    public Result<String> fetchEmails() {
        emailReceiverService.fetchEmails();
        return Result.success("邮件获取任务已启动");
    }

    @GetMapping("/templates")
    public Result<List<EmailTemplate>> getTemplates() {
        return Result.success(emailTemplateMapper.selectList(null));
    }

    @GetMapping("/templates/{id}")
    public Result<EmailTemplate> getTemplateById(@PathVariable Long id) {
        EmailTemplate template = emailTemplateMapper.selectById(id);
        if (template != null) {
            return Result.success(template);
        }
        return Result.error("模板不存在");
    }

    @PostMapping("/templates")
    public Result<EmailTemplate> createTemplate(@RequestBody EmailTemplate template) {
        emailTemplateMapper.insert(template);
        return Result.success(template);
    }

    @PutMapping("/templates/{id}")
    public Result<EmailTemplate> updateTemplate(@PathVariable Long id, @RequestBody EmailTemplate template) {
        template.setId(id);
        emailTemplateMapper.updateById(template);
        return Result.success(template);
    }

    @DeleteMapping("/templates/{id}")
    public Result<Void> deleteTemplate(@PathVariable Long id) {
        emailTemplateMapper.deleteById(id);
        return Result.success();
    }

    @Data
    static class SendEmailRequest {
        private Long companyId;
        private Long contactId;
        private Long templateId;
    }

    @Data
    static class SendBatchEmailRequest {
        private List<Long> companyIds;
        private Long templateId;
    }

    @Data
    static class SendCustomEmailRequest {
        private String toEmail;
        private String subject;
        private String content;
        private boolean html;
        private Long companyId;
        private Long templateId;
        private Long inReplyToEmailId;
    }
}