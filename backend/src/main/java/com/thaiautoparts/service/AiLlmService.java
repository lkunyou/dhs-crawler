package com.thaiautoparts.service;

import com.thaiautoparts.dto.ChatRequest;
import com.thaiautoparts.dto.ChatResponse;

import java.util.List;

/**
 * AI LLM 服务接口 - 基于 LangChain4j
 */
public interface AiLlmService {

    /**
     * 使用指定模型进行对话
     */
    ChatResponse chat(ChatRequest request);

    /**
     * 使用默认模型进行对话
     */
    ChatResponse chatWithDefaultModel(String message);

    /**
     * 根据 Provider 获取可用模型
     */
    List<String> getModelsByProvider(String provider);

    /**
     * 获取支持的 Provider 列表
     */
    List<String> getSupportedProviders();
}
