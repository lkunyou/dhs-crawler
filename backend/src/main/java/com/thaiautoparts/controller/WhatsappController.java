package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.WhatsappRecord;
import com.thaiautoparts.service.WhatsappService;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/whatsapp")
@RequiredArgsConstructor
public class WhatsappController {

    private final WhatsappService whatsappService;

    @PostMapping("/send-text")
    public Result<Void> sendText(@RequestBody SendTextRequest request) {
        whatsappService.sendTextMessage(
            request.getCompanyId(), 
            request.getContactId(), 
            request.getPhoneNumber(), 
            request.getContent()
        );
        return Result.success();
    }

    @PostMapping("/send-image")
    public Result<Void> sendImage(@RequestBody SendImageRequest request) {
        whatsappService.sendImageMessage(
            request.getCompanyId(),
            request.getContactId(),
            request.getPhoneNumber(),
            request.getImageUrl(),
            request.getCaption()
        );
        return Result.success();
    }

    @PostMapping("/send-batch")
    public Result<Void> sendBatch(@RequestBody SendBatchRequest request) {
        whatsappService.sendBatchMessages(request.getCompanyIds(), request.getContent());
        return Result.success();
    }

    @GetMapping("/records/{companyId}")
    public Result<List<WhatsappRecord>> getRecords(@PathVariable Long companyId) {
        return Result.success(whatsappService.getMessageRecords(companyId));
    }

    @GetMapping("/stats")
    public Result<Map<String, Object>> getStats() {
        return Result.success(whatsappService.getWhatsappStats());
    }

    @PostMapping("/webhook/delivery")
    public Result<Void> handleDelivery(@RequestBody WebhookRequest request) {
        whatsappService.handleDelivery(request.getMessageId());
        return Result.success();
    }

    @PostMapping("/webhook/read")
    public Result<Void> handleRead(@RequestBody WebhookRequest request) {
        whatsappService.handleRead(request.getMessageId());
        return Result.success();
    }

    @PostMapping("/webhook/reply")
    public Result<Void> handleReply(@RequestBody ReplyRequest request) {
        whatsappService.handleReply(request.getMessageId(), request.getContent());
        return Result.success();
    }

    @Data
    static class SendTextRequest {
        private Long companyId;
        private Long contactId;
        private String phoneNumber;
        private String content;
    }

    @Data
    static class SendImageRequest {
        private Long companyId;
        private Long contactId;
        private String phoneNumber;
        private String imageUrl;
        private String caption;
    }

    @Data
    static class SendBatchRequest {
        private List<Long> companyIds;
        private String content;
    }

    @Data
    static class WebhookRequest {
        private String messageId;
    }

    @Data
    static class ReplyRequest {
        private String messageId;
        private String content;
    }
}
