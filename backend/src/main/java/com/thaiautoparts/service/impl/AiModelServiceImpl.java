package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.thaiautoparts.dto.AiModelConfigDTO;
import com.thaiautoparts.entity.AiModelConfig;
import com.thaiautoparts.repository.AiModelConfigMapper;
import com.thaiautoparts.service.AiModelService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.*;

@Slf4j
@Service
@RequiredArgsConstructor
public class AiModelServiceImpl implements AiModelService {

    private final AiModelConfigMapper modelConfigMapper;
    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public List<AiModelConfigDTO> getModels() {
        return modelConfigMapper.selectList(new LambdaQueryWrapper<AiModelConfig>()
                .orderByAsc(AiModelConfig::getSortOrder))
            .stream()
            .map(this::convertToDTO)
            .collect(java.util.stream.Collectors.toList());
    }

    @Override
    public List<AiModelConfigDTO> getEnabledModels() {
        return modelConfigMapper.selectList(new LambdaQueryWrapper<AiModelConfig>()
                .eq(AiModelConfig::getEnabled, true)
                .orderByAsc(AiModelConfig::getSortOrder))
            .stream()
            .map(this::convertToDTO)
            .collect(java.util.stream.Collectors.toList());
    }

    @Override
    public AiModelConfigDTO getModel(Long id) {
        AiModelConfig model = modelConfigMapper.selectById(id);
        return model != null ? convertToDTO(model) : null;
    }

    @Override
    public AiModelConfigDTO getModelByProvider(String provider) {
        AiModelConfig model = modelConfigMapper.selectOne(
            new LambdaQueryWrapper<AiModelConfig>()
                .eq(AiModelConfig::getProvider, provider)
                .eq(AiModelConfig::getEnabled, true)
        );
        return model != null ? convertToDTO(model) : null;
    }

    @Override
    @Transactional
    public AiModelConfigDTO createModel(AiModelConfigDTO dto) {
        AiModelConfig model = new AiModelConfig();
        model.setProvider(dto.getProvider());
        model.setModelName(dto.getModelName());
        model.setApiEndpoint(dto.getApiEndpoint());
        model.setApiKey(dto.getApiKey());
        model.setBaseUrl(dto.getBaseUrl());
        model.setEnabled(dto.getEnabled() != null ? dto.getEnabled() : true);
        model.setSortOrder(dto.getSortOrder() != null ? dto.getSortOrder() : 0);
        model.setDescription(dto.getDescription());
        model.setCreatedAt(LocalDateTime.now());
        model.setUpdatedAt(LocalDateTime.now());
        modelConfigMapper.insert(model);
        return convertToDTO(model);
    }

    @Override
    @Transactional
    public AiModelConfigDTO updateModel(Long id, AiModelConfigDTO dto) {
        AiModelConfig model = modelConfigMapper.selectById(id);
        if (model == null) {
            throw new RuntimeException("Model not found");
        }
        if (dto.getProvider() != null) model.setProvider(dto.getProvider());
        if (dto.getModelName() != null) model.setModelName(dto.getModelName());
        if (dto.getApiEndpoint() != null) model.setApiEndpoint(dto.getApiEndpoint());
        if (dto.getApiKey() != null) model.setApiKey(dto.getApiKey());
        if (dto.getBaseUrl() != null) model.setBaseUrl(dto.getBaseUrl());
        if (dto.getEnabled() != null) model.setEnabled(dto.getEnabled());
        if (dto.getSortOrder() != null) model.setSortOrder(dto.getSortOrder());
        if (dto.getDescription() != null) model.setDescription(dto.getDescription());
        model.setUpdatedAt(LocalDateTime.now());
        modelConfigMapper.updateById(model);
        return convertToDTO(model);
    }

    @Override
    @Transactional
    public void deleteModel(Long id) {
        modelConfigMapper.deleteById(id);
    }

    @Override
    @Transactional
    public void toggleModel(Long id, Boolean enabled) {
        AiModelConfig model = modelConfigMapper.selectById(id);
        if (model != null) {
            model.setEnabled(enabled);
            model.setUpdatedAt(LocalDateTime.now());
            modelConfigMapper.updateById(model);
        }
    }

    @Override
    public String chat(String provider, String message, String systemPrompt) {
        List<ChatMessage> history = new ArrayList<>();
        if (systemPrompt != null && !systemPrompt.isEmpty()) {
            ChatMessage systemMsg = new ChatMessage();
            systemMsg.setRole("system");
            systemMsg.setContent(systemPrompt);
            history.add(systemMsg);
        }
        ChatMessage userMsg = new ChatMessage();
        userMsg.setRole("user");
        userMsg.setContent(message);
        history.add(userMsg);
        
        return chatWithHistory(provider, history, systemPrompt);
    }

    @Override
    public String chatWithHistory(String provider, List<ChatMessage> history, String systemPrompt) {
        AiModelConfigDTO modelConfig = getModelByProvider(provider);
        if (modelConfig == null) {
            throw new RuntimeException("Model provider not found or disabled: " + provider);
        }
        
        try {
            String endpoint = modelConfig.getBaseUrl() + modelConfig.getApiEndpoint();
            
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("model", modelConfig.getModelName());
            
            List<Map<String, String>> messages = new ArrayList<>();
            for (ChatMessage msg : history) {
                Map<String, String> msgMap = new HashMap<>();
                msgMap.put("role", msg.getRole());
                msgMap.put("content", msg.getContent());
                messages.add(msgMap);
            }
            requestBody.put("messages", messages);
            
            // 根据不同提供商设置参数
            setProviderSpecificParams(provider, requestBody);
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", "Bearer " + modelConfig.getApiKey());
            
            // 设置提供商特定的 headers
            setProviderHeaders(provider, headers);
            
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);
            
            ResponseEntity<String> response = restTemplate.exchange(
                endpoint,
                HttpMethod.POST,
                entity,
                String.class
            );
            
            return parseResponse(provider, response.getBody());
            
        } catch (Exception e) {
            log.error("AI chat failed for provider: {}", provider, e);
            throw new RuntimeException("AI chat failed: " + e.getMessage());
        }
    }
    
    private void setProviderSpecificParams(String provider, Map<String, Object> requestBody) {
        switch (provider.toLowerCase()) {
            case "deepseek":
                requestBody.put("max_tokens", 2048);
                requestBody.put("temperature", 0.7);
                break;
            case "kimi":
                requestBody.put("max_tokens", 2048);
                requestBody.put("temperature", 0.7);
                break;
            case "glm":
                requestBody.put("max_tokens", 2048);
                requestBody.put("temperature", 0.7);
                break;
            case "doubao":
                requestBody.put("max_tokens", 2048);
                requestBody.put("temperature", 0.7);
                break;
            case "qwen":
                requestBody.put("max_tokens", 2048);
                requestBody.put("temperature", 0.7);
                break;
            case "minimax":
                requestBody.put("max_tokens", 2048);
                requestBody.put("temperature", 0.7);
                break;
            default:
                requestBody.put("max_tokens", 2048);
                requestBody.put("temperature", 0.7);
        }
    }
    
    private void setProviderHeaders(String provider, HttpHeaders headers) {
        switch (provider.toLowerCase()) {
            case "kimi":
                headers.set("Content-Type", "application/json");
                break;
            case "doubao":
                headers.set("Content-Type", "application/json");
                break;
            case "minimax":
                headers.set("Content-Type", "application/json");
                break;
        }
    }
    
    private String parseResponse(String provider, String responseBody) {
        try {
            Map<String, Object> response = objectMapper.readValue(responseBody, Map.class);
            
            // 通用 OpenAI 格式
            if (response.containsKey("choices")) {
                List<Map<String, Object>> choices = (List<Map<String, Object>>) response.get("choices");
                if (!choices.isEmpty()) {
                    Map<String, Object> choice = choices.get(0);
                    if (choice.containsKey("message")) {
                        Map<String, String> message = (Map<String, String>) choice.get("message");
                        return message.get("content");
                    }
                }
            }
            
            // 智谱 GLM 格式
            if (response.containsKey("choices")) {
                List<Map<String, Object>> choices = (List<Map<String, Object>>) response.get("choices");
                if (!choices.isEmpty()) {
                    Map<String, Object> choice = choices.get(0);
                    if (choice.containsKey("delta")) {
                        Map<String, String> delta = (Map<String, String>) choice.get("delta");
                        return delta.get("content");
                    }
                }
            }
            
            // MiniMax 格式
            if (response.containsKey("choices")) {
                List<Map<String, Object>> choices = (List<Map<String, Object>>) response.get("choices");
                if (!choices.isEmpty()) {
                    Map<String, Object> choice = choices.get(0);
                    if (choice.containsKey("messages")) {
                        List<Map<String, String>> messages = (List<Map<String, String>>) choice.get("messages");
                        for (Map<String, String> msg : messages) {
                            if ("assistant".equals(msg.get("role"))) {
                                return msg.get("text");
                            }
                        }
                    }
                }
            }
            
            // 豆包 Doubao 格式
            if (response.containsKey("choices")) {
                List<Map<String, Object>> choices = (List<Map<String, Object>>) response.get("choices");
                if (!choices.isEmpty()) {
                    Map<String, Object> choice = choices.get(0);
                    if (choice.containsKey("message")) {
                        Map<String, String> message = (Map<String, String>) choice.get("message");
                        return message.get("content");
                    }
                }
            }
            
            // 通用的错误处理
            if (response.containsKey("error")) {
                Object error = response.get("error");
                if (error instanceof Map) {
                    return "Error: " + ((Map) error).get("message");
                }
                return "Error: " + error.toString();
            }
            
            return responseBody;
            
        } catch (Exception e) {
            log.error("Failed to parse AI response", e);
            return responseBody;
        }
    }

    private AiModelConfigDTO convertToDTO(AiModelConfig model) {
        AiModelConfigDTO dto = new AiModelConfigDTO();
        dto.setId(model.getId());
        dto.setProvider(model.getProvider());
        dto.setModelName(model.getModelName());
        dto.setApiEndpoint(model.getApiEndpoint());
        dto.setApiKey(model.getApiKey());
        dto.setBaseUrl(model.getBaseUrl());
        dto.setEnabled(model.getEnabled());
        dto.setSortOrder(model.getSortOrder());
        dto.setDescription(model.getDescription());
        return dto;
    }
}
