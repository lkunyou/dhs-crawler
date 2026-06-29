package com.thaiautoparts.dto;

import lombok.Data;
import java.util.List;
import java.util.Map;

/**
 * Agent 聊天请求
 */
@Data
public class AgentChatRequest {
    private String agentType;           // Agent 类型
    private String message;             // 用户消息
    private String model;               // 使用的模型
    private List<AgentChatMessage> history;  // 历史消息
    private Map<String, Object> context;     // 额外上下文

    @Data
    public static class AgentChatMessage {
        private String role;
        private String content;
    }
}
