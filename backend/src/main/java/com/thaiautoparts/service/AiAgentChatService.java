package com.thaiautoparts.service;

import com.thaiautoparts.dto.AgentChatRequest;
import com.thaiautoparts.dto.AgentChatResponse;

/**
 * AI Agent 聊天服务接口 - 基于 LangChain4j Agent
 * 支持工具调用（Tool Calling）
 */
public interface AiAgentChatService {

    /**
     * 使用 Agent 进行对话（支持工具调用）
     */
    AgentChatResponse chat(AgentChatRequest request);

    /**
     * 获取 Agent 支持的工具列表
     */
    String[] getAvailableTools(String agentType);
}
