package com.thaiautoparts.service;

import com.thaiautoparts.entity.InboundEmail;
import java.util.List;

public interface EmailReceiverService {
    void fetchEmails();
    List<InboundEmail> getInbox();
    List<InboundEmail> getUnreadEmails();
    InboundEmail getEmailById(Long id);
    void markAsRead(Long id);
    void markAsStarred(Long id, boolean starred);
    void deleteEmail(Long id);
    Integer getUnreadCount();
}