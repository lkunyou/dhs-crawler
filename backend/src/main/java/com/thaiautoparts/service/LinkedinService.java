package com.thaiautoparts.service;

import com.thaiautoparts.entity.LinkedinRecord;
import java.util.List;
import java.util.Map;

public interface LinkedinService {
    void addContact(Long companyId, Long contactId, String profileUrl, String message);
    void sendMessage(Long companyId, Long contactId, String profileUrl, String content);
    void viewProfile(Long companyId, Long contactId, String profileUrl);
    List<LinkedinRecord> getRecords(Long companyId);
    Map<String, Object> getLinkedinStats();
    void handleConnectionAccepted(Long recordId);
    void handleMessageResponse(Long recordId, String responseContent);
}
