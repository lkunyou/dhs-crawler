package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.EmailRecord;
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

    @GetMapping("/stats")
    public Result<Map<String, Object>> getStats() {
        return Result.success(emailService.getEmailStats());
    }

    @GetMapping("/track/open")
    public Result<Void> trackOpen(@RequestParam String trackingId) {
        emailService.handleEmailOpened(trackingId);
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
}
