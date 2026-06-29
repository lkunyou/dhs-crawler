package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class ChatResponse {
    private String content;
    private Long conversationId;
    private String messageId;
    private String model;
    private String finishReason;
}
