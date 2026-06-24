package com.thaiautoparts.service;

import com.thaiautoparts.entity.WhatsappRecord;
import java.util.List;
import java.util.Map;

public interface WhatsappService {
    void sendTextMessage(Long companyId, Long contactId, String phoneNumber, String content);
    void sendImageMessage(Long companyId, Long contactId, String phoneNumber, String imageUrl, String caption);
    void sendBatchMessages(List<Long> companyIds, String templateContent);
    List<WhatsappRecord> getMessageRecords(Long companyId);
    Map<String, Object> getWhatsappStats();
    void handleDelivery(String messageId);
    void handleRead(String messageId);
    void handleReply(String messageId, String replyContent);
}
