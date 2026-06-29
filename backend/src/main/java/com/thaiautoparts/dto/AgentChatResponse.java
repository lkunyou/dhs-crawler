package com.thaiautoparts.dto;

import lombok.Data;
import java.util.List;

/**
 * Agent 聊天响应
 */
@Data
public class AgentChatResponse {
    private String content;              // AI 回复内容
    private String model;               // 使用的模型
    private String finishReason;         // 结束原因
    private List<ToolCall> toolCalls;    // 调用的工具列表
    private String errorMessage;         // 错误信息

    @Data
    public static class ToolCall {
        private String toolName;
        private String arguments;
        private String result;
    }
}
