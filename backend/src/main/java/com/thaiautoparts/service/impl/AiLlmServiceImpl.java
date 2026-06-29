package com.thaiautoparts.service.impl;

import com.thaiautoparts.dto.ChatRequest;
import com.thaiautoparts.dto.ChatResponse;
import com.thaiautoparts.entity.AiModelConfig;
import com.thaiautoparts.repository.AiModelConfigMapper;
import com.thaiautoparts.service.AiLlmService;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;
import java.util.*;

/**
 * AI LLM 服务实现
 * 直接通过 HTTP 调用各种国产模型 API（DeepSeek、Kimi、GLM、Doubao、Qwen、Minimax）
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AiLlmServiceImpl implements AiLlmService {

    private final AiModelConfigMapper modelConfigMapper;
    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public ChatResponse chat(ChatRequest request) {
        String modelName = request.getModel();
        AiModelConfig modelConfig;

        if (modelName != null && !modelName.isEmpty()) {
            modelConfig = modelConfigMapper.selectOne(
                    new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<AiModelConfig>()
                            .eq(AiModelConfig::getModelName, modelName)
                            .eq(AiModelConfig::getEnabled, true)
            );
        } else {
            modelConfig = modelConfigMapper.selectOne(
                    new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<AiModelConfig>()
                            .eq(AiModelConfig::getEnabled, true)
                            .orderByAsc(AiModelConfig::getSortOrder)
                            .last("LIMIT 1")
            );
        }

        if (modelConfig == null) {
            return buildErrorResponse("No enabled AI model found. Please configure a model in AI Model Settings.");
        }

        try {
            String response = callModelApi(modelConfig, request.getMessage());
            
            ChatResponse chatResponse = new ChatResponse();
            chatResponse.setContent(response);
            chatResponse.setConversationId(request.getConversationId());
            chatResponse.setModel(modelConfig.getModelName());
            chatResponse.setFinishReason("stop");
            return chatResponse;
        } catch (Exception e) {
            log.error("Error calling AI model: {}", e.getMessage(), e);
            return buildErrorResponse("AI service error: " + e.getMessage());
        }
    }

    @Override
    public ChatResponse chatWithDefaultModel(String message) {
        ChatRequest request = new ChatRequest();
        request.setMessage(message);
        return chat(request);
    }

    /**
     * 调用模型 API
     */
    private String callModelApi(AiModelConfig config, String message) throws Exception {
        String provider = config.getProvider();
        String baseUrl = config.getBaseUrl();
        String apiKey = config.getApiKey();
        String modelName = config.getModelName();

        if (baseUrl == null || baseUrl.isEmpty()) {
            throw new RuntimeException("Base URL is required for AI model");
        }

        // 构建请求体
        ObjectNode requestBody = objectMapper.createObjectNode();
        requestBody.put("model", modelName);
        
        ArrayNode messages = requestBody.putArray("messages");
        ObjectNode userMsg = messages.addObject();
        userMsg.put("role", "user");
        userMsg.put("content", message);

        // 设置请求头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Authorization", "Bearer " + apiKey);

        // 根据不同 Provider 调整请求格式
        adjustRequestForProvider(provider, requestBody, baseUrl);

        HttpEntity<String> entity = new HttpEntity<>(objectMapper.writeValueAsString(requestBody), headers);

        // 调用 API
        String url = baseUrl + getApiPath(provider);
        ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, entity, String.class);

        // 解析响应
        return parseResponse(provider, response.getBody());
    }

    /**
     * 根据 Provider 调整请求
     */
    private void adjustRequestForProvider(String provider, ObjectNode requestBody, String baseUrl) {
        switch (provider) {
            case "DeepSeek":
                // DeepSeek 使用标准 OpenAI 格式
                break;
            case "Kimi":
                // Kimi (Moonshot) 使用标准格式
                break;
            case "GLM":
                // 智谱 GLM 可能需要 stream: false
                requestBody.put("stream", false);
                break;
            case "Doubao":
                // 豆包使用标准格式
                break;
            case "Qwen":
                // 通义千问使用标准格式
                break;
            case "Minimax":
                // MiniMax 使用标准格式
                break;
            default:
                // 默认设置
                requestBody.put("stream", false);
                break;
        }
    }

    /**
     * 获取 API 路径
     */
    private String getApiPath(String provider) {
        switch (provider) {
            case "DeepSeek":
                return "/v1/chat/completions";
            case "Kimi":
                return "/v1/chat/completions";
            case "GLM":
                return "/api/paulin/v1/chat/completions";
            case "Doubao":
                return "/api/v1/chat/completions";
            case "Qwen":
                return "/v1/chat/completions";
            case "Minimax":
                return "/v1/text/chatcompletion_v2";
            default:
                return "/v1/chat/completions";
        }
    }

    /**
     * 解析 API 响应
     */
    private String parseResponse(String provider, String responseBody) throws Exception {
        JsonNode root = objectMapper.readTree(responseBody);
        
        // 尝试多种响应格式
        // 格式1: choices[0].message.content (OpenAI 兼容格式)
        if (root.has("choices") && root.get("choices").isArray()) {
            JsonNode choice = root.get("choices").get(0);
            if (choice.has("message") && choice.get("message").has("content")) {
                return choice.get("message").get("content").asText();
            }
            if (choice.has("text")) {
                return choice.get("text").asText();
            }
        }
        
        // 格式2: text (某些模型使用)
        if (root.has("text")) {
            return root.get("text").asText();
        }

        // 格式3: result (某些模型使用)
        if (root.has("result")) {
            return root.get("result").asText();
        }

        // 格式4: Gemini 格式
        if (root.has("candidates") && root.get("candidates").isArray()) {
            JsonNode candidate = root.get("candidates").get(0);
            if (candidate.has("content") && candidate.get("content").has("parts")) {
                return candidate.get("content").get("parts").get(0).get("text").asText();
            }
        }

        throw new RuntimeException("Unable to parse response: " + responseBody);
    }

    /**
     * 构建错误响应
     */
    private ChatResponse buildErrorResponse(String errorMessage) {
        ChatResponse response = new ChatResponse();
        response.setContent("抱歉，发生了错误：" + errorMessage);
        response.setFinishReason("error");
        return response;
    }

    @Override
    public List<String> getModelsByProvider(String provider) {
        List<AiModelConfig> models = modelConfigMapper.selectList(
                new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<AiModelConfig>()
                        .eq(AiModelConfig::getProvider, provider)
                        .eq(AiModelConfig::getEnabled, true)
                        .orderByAsc(AiModelConfig::getSortOrder)
        );
        return models.stream()
                .map(AiModelConfig::getModelName)
                .toList();
    }

    @Override
    public List<String> getSupportedProviders() {
        return Arrays.asList("OpenAI", "DeepSeek", "Kimi", "GLM", "Doubao", "Qwen", "Minimax");
    }
}
