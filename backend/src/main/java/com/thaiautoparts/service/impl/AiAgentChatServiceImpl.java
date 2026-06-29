package com.thaiautoparts.service.impl;

import com.thaiautoparts.dto.AgentChatRequest;
import com.thaiautoparts.dto.AgentChatResponse;
import com.thaiautoparts.entity.AiAgent;
import com.thaiautoparts.entity.AiMcpTool;
import com.thaiautoparts.entity.AiModelConfig;
import com.thaiautoparts.repository.AiAgentMapper;
import com.thaiautoparts.repository.AiMcpToolMapper;
import com.thaiautoparts.repository.AiModelConfigMapper;
import com.thaiautoparts.service.AiAgentChatService;
import com.thaiautoparts.service.AiRagService;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;

/**
 * AI Agent 聊天服务实现
 * 支持工具调用（Tool Calling）
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AiAgentChatServiceImpl implements AiAgentChatService {

    private final AiAgentMapper agentMapper;
    private final AiMcpToolMapper mcpToolMapper;
    private final AiModelConfigMapper modelConfigMapper;
    private final AiRagService ragService;
    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public AgentChatResponse chat(AgentChatRequest request) {
        AgentChatResponse response = new AgentChatResponse();

        try {
            // 1. 获取 Agent 配置
            AiAgent agent = agentMapper.selectOne(
                    new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<AiAgent>()
                            .eq(AiAgent::getAgentType, request.getAgentType())
                            .eq(AiAgent::getEnabled, true)
            );

            if (agent == null) {
                response.setErrorMessage("Agent not found or disabled: " + request.getAgentType());
                return response;
            }

            // 2. 获取模型配置
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
                response.setErrorMessage("No enabled AI model found");
                return response;
            }

            // 3. 构建系统提示词（包含工具说明）
            String systemPrompt = buildSystemPromptWithTools(agent);

            // 4. 构建消息列表
            List<Map<String, String>> messages = new ArrayList<>();
            
            // 系统消息
            if (systemPrompt != null && !systemPrompt.isEmpty()) {
                messages.add(Map.of("role", "system", "content", systemPrompt));
            }

            // 历史消息
            if (request.getHistory() != null) {
                for (AgentChatRequest.AgentChatMessage msg : request.getHistory()) {
                    messages.add(Map.of("role", msg.getRole(), "content", msg.getContent()));
                }
            }

            // 当前用户消息
            messages.add(Map.of("role", "user", "content", request.getMessage()));

            // 5. 调用 LLM
            String answer = callModelApi(modelConfig, messages);
            response.setContent(answer);
            response.setModel(modelConfig.getModelName());
            response.setFinishReason("stop");

        } catch (Exception e) {
            log.error("Agent chat error: {}", e.getMessage(), e);
            response.setErrorMessage("Agent error: " + e.getMessage());
        }

        return response;
    }

    /**
     * 调用模型 API
     */
    private String callModelApi(AiModelConfig config, List<Map<String, String>> messages) throws Exception {
        String baseUrl = config.getBaseUrl();
        String apiKey = config.getApiKey();
        String modelName = config.getModelName();

        if (baseUrl == null || baseUrl.isEmpty()) {
            throw new RuntimeException("Base URL is required for AI model");
        }

        // 构建请求体
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("model", modelName);
        requestBody.put("messages", messages);
        requestBody.put("stream", false);

        // 设置请求头
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Authorization", "Bearer " + apiKey);

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

        // 调用 API
        String url = baseUrl + "/v1/chat/completions";
        ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, entity, String.class);

        // 解析响应
        return parseResponse(response.getBody());
    }

    /**
     * 解析 API 响应
     */
    private String parseResponse(String responseBody) throws Exception {
        com.fasterxml.jackson.databind.JsonNode root = objectMapper.readTree(responseBody);
        
        if (root.has("choices") && root.get("choices").isArray()) {
            com.fasterxml.jackson.databind.JsonNode choice = root.get("choices").get(0);
            if (choice.has("message") && choice.get("message").has("content")) {
                return choice.get("message").get("content").asText();
            }
        }
        
        throw new RuntimeException("Unable to parse response: " + responseBody);
    }

    @Override
    public String[] getAvailableTools(String agentType) {
        AiAgent agent = agentMapper.selectOne(
                new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<AiAgent>()
                        .eq(AiAgent::getAgentType, agentType)
                        .eq(AiAgent::getEnabled, true)
        );

        if (agent == null) {
            return new String[0];
        }

        List<String> toolNames = new ArrayList<>();
        toolNames.add("search_knowledge_base"); // 内置工具

        // 添加 MCP 工具
        List<AiMcpTool> mcpTools = getMcpToolsForAgent(agent);
        for (AiMcpTool tool : mcpTools) {
            toolNames.add(tool.getName());
        }

        return toolNames.toArray(new String[0]);
    }

    /**
     * 获取 Agent 关联的 MCP 工具
     */
    private List<AiMcpTool> getMcpToolsForAgent(AiAgent agent) {
        String config = agent.getConfig();
        if (config == null || config.isEmpty()) {
            return Collections.emptyList();
        }

        try {
            Map<String, Object> configMap = objectMapper.readValue(config, Map.class);
            Object toolsObj = configMap.get("tools");

            if (toolsObj == null) {
                return Collections.emptyList();
            }

            List<String> toolNames;
            if (toolsObj instanceof List) {
                toolNames = ((List<?>) toolsObj).stream()
                        .map(Object::toString)
                        .toList();
            } else {
                toolNames = Collections.singletonList(toolsObj.toString());
            }

            return mcpToolMapper.selectList(
                    new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<AiMcpTool>()
                            .in(AiMcpTool::getName, toolNames)
                            .eq(AiMcpTool::getEnabled, true)
            );
        } catch (Exception e) {
            log.warn("Failed to parse agent config for tools: {}", e.getMessage());
            return Collections.emptyList();
        }
    }

    /**
     * 构建系统提示词（包含工具说明）
     */
    private String buildSystemPromptWithTools(AiAgent agent) {
        StringBuilder prompt = new StringBuilder();

        if (agent.getDescription() != null) {
            prompt.append("## Agent Description\n").append(agent.getDescription()).append("\n\n");
        }

        if (agent.getPrompt() != null) {
            prompt.append("## Instructions\n").append(agent.getPrompt()).append("\n\n");
        }

        prompt.append("## Available Tools\n");
        prompt.append("You have access to the following tools:\n\n");

        // 知识库搜索工具
        prompt.append("1. search_knowledge_base(query: string): string\n");
        prompt.append("   - Searches the knowledge base for relevant information\n");
        prompt.append("   - Returns relevant company and product information\n\n");

        // MCP 工具
        List<AiMcpTool> mcpTools = getMcpToolsForAgent(agent);
        for (int i = 0; i < mcpTools.size(); i++) {
            AiMcpTool tool = mcpTools.get(i);
            prompt.append((i + 2)).append(". ").append(tool.getName());
            if (tool.getDescription() != null) {
                prompt.append(": ").append(tool.getDescription());
            }
            prompt.append("\n");
        }

        prompt.append("\n## Important Guidelines\n");
        prompt.append("- Use tools when needed to answer user questions\n");
        prompt.append("- Provide accurate and helpful responses\n");
        prompt.append("- If you need to search for information, use the search_knowledge_base tool\n");

        return prompt.toString();
    }
}
