package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.LinkedinRecord;
import com.thaiautoparts.service.LinkedinService;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/linkedin")
@RequiredArgsConstructor
public class LinkedinController {

    private final LinkedinService linkedinService;

    @PostMapping("/add-contact")
    public Result<Void> addContact(@RequestBody AddContactRequest request) {
        linkedinService.addContact(
            request.getCompanyId(),
            request.getContactId(),
            request.getProfileUrl(),
            request.getMessage()
        );
        return Result.success();
    }

    @PostMapping("/send-message")
    public Result<Void> sendMessage(@RequestBody SendMessageRequest request) {
        linkedinService.sendMessage(
            request.getCompanyId(),
            request.getContactId(),
            request.getProfileUrl(),
            request.getContent()
        );
        return Result.success();
    }

    @PostMapping("/view-profile")
    public Result<Void> viewProfile(@RequestBody ViewProfileRequest request) {
        linkedinService.viewProfile(
            request.getCompanyId(),
            request.getContactId(),
            request.getProfileUrl()
        );
        return Result.success();
    }

    @GetMapping("/records/{companyId}")
    public Result<List<LinkedinRecord>> getRecords(@PathVariable Long companyId) {
        return Result.success(linkedinService.getRecords(companyId));
    }

    @GetMapping("/stats")
    public Result<Map<String, Object>> getStats() {
        return Result.success(linkedinService.getLinkedinStats());
    }

    @PostMapping("/webhook/connection-accepted")
    public Result<Void> handleConnectionAccepted(@RequestBody WebhookRequest request) {
        linkedinService.handleConnectionAccepted(request.getRecordId());
        return Result.success();
    }

    @PostMapping("/webhook/message-response")
    public Result<Void> handleMessageResponse(@RequestBody MessageResponseRequest request) {
        linkedinService.handleMessageResponse(request.getRecordId(), request.getContent());
        return Result.success();
    }

    @Data
    static class AddContactRequest {
        private Long companyId;
        private Long contactId;
        private String profileUrl;
        private String message;
    }

    @Data
    static class SendMessageRequest {
        private Long companyId;
        private Long contactId;
        private String profileUrl;
        private String content;
    }

    @Data
    static class ViewProfileRequest {
        private Long companyId;
        private Long contactId;
        private String profileUrl;
    }

    @Data
    static class WebhookRequest {
        private Long recordId;
    }

    @Data
    static class MessageResponseRequest {
        private Long recordId;
        private String content;
    }
}
