package com.thaiautoparts.dto;

import lombok.Data;
import java.util.List;

@Data
public class ChatRequest {
    private Long conversationId;
    private String message;
    private String model;
    private String agentType;
    private List<Message> history;
    
    @Data
    public static class Message {
        private String role;
        private String content;
    }
}
