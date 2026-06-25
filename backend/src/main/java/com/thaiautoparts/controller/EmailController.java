package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.EmailRecord;
import com.thaiautoparts.entity.InboundEmail;
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

    @GetMapping("/records/{companyId}")
    public Result<List<EmailRecord>> getRecords(@PathVariable Long companyId) {
        return Result.success(emailService.getEmailRecords(companyId));
    }

    @GetMapping("/records")
    public Result<List<EmailRecord>> getAllRecords() {
        return Result.success(emailService.getAllEmailRecords());
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
}