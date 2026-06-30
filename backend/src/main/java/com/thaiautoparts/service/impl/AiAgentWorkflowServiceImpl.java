package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.thaiautoparts.dto.AiAgentWorkflowDTO;
import com.thaiautoparts.dto.AiAgentWorkflowExecDTO;
import com.thaiautoparts.dto.AiAgentWorkflowDebugDTO;
import com.thaiautoparts.dto.ChatRequest;
import com.thaiautoparts.dto.ChatResponse;
import com.thaiautoparts.entity.AiAgentWorkflow;
import com.thaiautoparts.entity.AiAgentWorkflowExec;
import com.thaiautoparts.entity.AiMcpTool;
import com.thaiautoparts.repository.AiAgentWorkflowExecMapper;
import com.thaiautoparts.repository.AiAgentWorkflowMapper;
import com.thaiautoparts.repository.AiMcpToolMapper;
import com.thaiautoparts.dto.RagSearchResult;
import com.thaiautoparts.service.AiAgentWorkflowService;
import com.thaiautoparts.service.AiLlmService;
import com.thaiautoparts.service.AiRagService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.time.LocalDateTime;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class AiAgentWorkflowServiceImpl implements AiAgentWorkflowService {

    private final AiAgentWorkflowMapper workflowMapper;
    private final AiAgentWorkflowExecMapper execMapper;
    private final AiMcpToolMapper mcpToolMapper;
    private final AiLlmService aiLlmService;
    private final AiRagService aiRagService;
    private final DataSource dataSource;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final RestTemplate restTemplate = new RestTemplate();

    // 条件表达式中的变量引用模式: {{varName}}
    private static final Pattern VAR_PATTERN = Pattern.compile("\\{\\{(\\w+(?:\\.\\w+)*)\\}\\}");

    @Override
    public List<AiAgentWorkflowDTO> getWorkflows() {
        return workflowMapper.selectList(new LambdaQueryWrapper<AiAgentWorkflow>()
                .orderByDesc(AiAgentWorkflow::getCreatedAt))
            .stream()
            .map(this::convertToDTO)
            .collect(Collectors.toList());
    }

    @Override
    public List<AiAgentWorkflowDTO> getEnabledWorkflows() {
        return workflowMapper.selectList(new LambdaQueryWrapper<AiAgentWorkflow>()
                .eq(AiAgentWorkflow::getEnabled, true)
                .orderByDesc(AiAgentWorkflow::getCreatedAt))
            .stream()
            .map(this::convertToDTO)
            .collect(Collectors.toList());
    }

    @Override
    public AiAgentWorkflowDTO getWorkflow(Long id) {
        AiAgentWorkflow workflow = workflowMapper.selectById(id);
        return workflow != null ? convertToDTO(workflow) : null;
    }

    @Override
    public AiAgentWorkflowDTO getWorkflowByAgentType(String agentType) {
        AiAgentWorkflow workflow = workflowMapper.selectOne(
            new LambdaQueryWrapper<AiAgentWorkflow>()
                .eq(AiAgentWorkflow::getAgentType, agentType)
                .eq(AiAgentWorkflow::getEnabled, true)
        );
        return workflow != null ? convertToDTO(workflow) : null;
    }

    @Override
    @Transactional
    public AiAgentWorkflowDTO createWorkflow(AiAgentWorkflowDTO dto) {
        AiAgentWorkflow workflow = new AiAgentWorkflow();
        workflow.setName(dto.getName());
        workflow.setDescription(dto.getDescription());
        workflow.setAgentType(dto.getAgentType());
        workflow.setSteps(convertStepsToJson(dto.getSteps()));
        workflow.setEdges(convertEdgesToJson(dto.getEdges()));
        workflow.setVariables(convertVariablesToJson(dto.getVariables()));
        workflow.setTimeout(dto.getTimeout() != null ? dto.getTimeout() : 300);
        workflow.setEnabled(dto.getEnabled() != null ? dto.getEnabled() : true);
        workflow.setCreatedAt(LocalDateTime.now());
        workflow.setUpdatedAt(LocalDateTime.now());
        workflowMapper.insert(workflow);
        return convertToDTO(workflow);
    }

    @Override
    @Transactional
    public AiAgentWorkflowDTO updateWorkflow(Long id, AiAgentWorkflowDTO dto) {
        AiAgentWorkflow workflow = workflowMapper.selectById(id);
        if (workflow == null) throw new RuntimeException("Workflow not found");
        if (dto.getName() != null) workflow.setName(dto.getName());
        if (dto.getDescription() != null) workflow.setDescription(dto.getDescription());
        if (dto.getAgentType() != null) workflow.setAgentType(dto.getAgentType());
        if (dto.getSteps() != null) workflow.setSteps(convertStepsToJson(dto.getSteps()));
        if (dto.getEdges() != null) workflow.setEdges(convertEdgesToJson(dto.getEdges()));
        if (dto.getVariables() != null) workflow.setVariables(convertVariablesToJson(dto.getVariables()));
        if (dto.getTimeout() != null) workflow.setTimeout(dto.getTimeout());
        if (dto.getEnabled() != null) workflow.setEnabled(dto.getEnabled());
        workflow.setUpdatedAt(LocalDateTime.now());
        workflowMapper.updateById(workflow);
        return convertToDTO(workflow);
    }

    @Override
    @Transactional
    public void deleteWorkflow(Long id) {
        workflowMapper.deleteById(id);
    }

    @Override
    @Transactional
    public void toggleWorkflow(Long id, Boolean enabled) {
        AiAgentWorkflow workflow = workflowMapper.selectById(id);
        if (workflow != null) {
            workflow.setEnabled(enabled);
            workflow.setUpdatedAt(LocalDateTime.now());
            workflowMapper.updateById(workflow);
        }
    }

    @Override
    public List<AiAgentWorkflowExecDTO> getExecutions(Long workflowId) {
        LambdaQueryWrapper<AiAgentWorkflowExec> wrapper = new LambdaQueryWrapper<>();
        if (workflowId != null) wrapper.eq(AiAgentWorkflowExec::getWorkflowId, workflowId.toString());
        wrapper.orderByDesc(AiAgentWorkflowExec::getCreatedAt);
        List<AiAgentWorkflowExec> execs = execMapper.selectList(wrapper);
        List<AiAgentWorkflowExecDTO> result = new ArrayList<>();
        for (AiAgentWorkflowExec exec : execs) {
            AiAgentWorkflow workflow = workflowMapper.selectById(exec.getWorkflowId());
            AiAgentWorkflowExecDTO dto = convertExecToDTO(exec);
            if (workflow != null) dto.setWorkflowName(workflow.getName());
            result.add(dto);
        }
        return result;
    }

    @Override
    public AiAgentWorkflowExecDTO getExecution(Long id) {
        AiAgentWorkflowExec exec = execMapper.selectById(id);
        if (exec == null) return null;
        AiAgentWorkflow workflow = workflowMapper.selectById(exec.getWorkflowId());
        AiAgentWorkflowExecDTO dto = convertExecToDTO(exec);
        if (workflow != null) dto.setWorkflowName(workflow.getName());
        return dto;
    }

    @Override
    @Transactional
    public AiAgentWorkflowExecDTO executeWorkflow(Long workflowId, Map<String, Object> input) {
        AiAgentWorkflow workflow = workflowMapper.selectById(workflowId);
        if (workflow == null) throw new RuntimeException("Workflow not found");

        AiAgentWorkflowExec exec = new AiAgentWorkflowExec();
        exec.setWorkflowId(workflowId.toString());
        exec.setStatus("pending");
        exec.setInput(convertVariablesToJson(input));
        exec.setCurrentStep(0);
        exec.setCreatedAt(LocalDateTime.now());
        exec.setStartedAt(LocalDateTime.now());
        execMapper.insert(exec);

        final Long execId = exec.getId();
        Thread executor = new Thread(() -> executeWorkflowAsync(execId, workflow));
        executor.start();

        return convertExecToDTO(exec);
    }

    private void executeWorkflowAsync(Long execId, AiAgentWorkflow workflow) {
        try {
            execMapper.updateStatusById(execId, "running");

            Map<String, Object> context = new HashMap<>();
            context.put("input", convertJsonToVariables(workflow.getVariables()));

            List<AiAgentWorkflowDTO.WorkflowStep> steps = convertJsonToSteps(workflow.getSteps());
            Map<String, Object> outputs = new HashMap<>();

            int maxSteps = steps.size() * 100; // 防止无限循环
            int stepCount = 0;

            for (int i = 0; i < steps.size() && stepCount < maxSteps; i++) {
                AiAgentWorkflowDTO.WorkflowStep step = steps.get(i);
                execMapper.updateCurrentStepById(execId, i + 1);
                stepCount++;

                try {
                    Object result = executeStep(step, context);
                    context.put("step_" + step.getOrder(), result);
                    if (step.getName() != null) outputs.put(step.getName(), result);

                    // 条件分支：根据结果跳转到不同步骤
                    if ("condition".equals(step.getType()) && result instanceof Map) {
                        @SuppressWarnings("unchecked")
                        Map<String, Object> condResult = (Map<String, Object>) result;
                        String branch = (String) condResult.get("branch");
                        if (branch != null) {
                            int jumpIdx = findStepByName(steps, branch);
                            if (jumpIdx >= 0) {
                                i = jumpIdx - 1; // -1 because loop will increment
                                continue;
                            }
                        }
                    }

                    // 循环节点
                    if ("loop".equals(step.getType()) && result instanceof Map) {
                        @SuppressWarnings("unchecked")
                        Map<String, Object> loopResult = (Map<String, Object>) result;
                        Boolean shouldContinue = (Boolean) loopResult.get("continue");
                        if (Boolean.TRUE.equals(shouldContinue)) {
                            int loopStart = findStepByName(steps, step.getName() + "_body");
                            if (loopStart >= 0) {
                                i = loopStart - 1;
                                continue;
                            }
                        }
                    }

                } catch (Exception e) {
                    log.error("Step {} failed: {}", step.getName(), e.getMessage(), e);
                    execMapper.updateErrorById(execId, e.getMessage());
                    execMapper.updateStatusById(execId, "failed");
                    return;
                }
            }

            execMapper.updateOutputById(execId, objectMapper.writeValueAsString(outputs));
            execMapper.updateStatusById(execId, "completed");

        } catch (Exception e) {
            log.error("Workflow execution failed", e);
            execMapper.updateErrorById(execId, e.getMessage());
            execMapper.updateStatusById(execId, "failed");
        }
    }

    @Override
    public AiAgentWorkflowDebugDTO debugWorkflow(Long workflowId, Map<String, Object> input) {
        AiAgentWorkflow workflow = workflowMapper.selectById(workflowId);
        if (workflow == null) throw new RuntimeException("Workflow not found");

        AiAgentWorkflowDebugDTO debugResult = new AiAgentWorkflowDebugDTO();
        debugResult.setStatus("running");
        debugResult.setStepResults(new ArrayList<>());

        try {
            Map<String, Object> context = new HashMap<>();
            context.put("input", input != null ? input : convertJsonToVariables(workflow.getVariables()));

            List<AiAgentWorkflowDTO.WorkflowStep> steps = convertJsonToSteps(workflow.getSteps());
            debugResult.setTotalSteps(steps.size());

            for (int i = 0; i < steps.size(); i++) {
                AiAgentWorkflowDTO.WorkflowStep step = steps.get(i);
                AiAgentWorkflowDebugDTO.StepResult stepResult = new AiAgentWorkflowDebugDTO.StepResult();
                stepResult.setIndex(i);
                stepResult.setStepId(step.getId());
                stepResult.setStepName(step.getName());
                stepResult.setStepType(step.getType());
                stepResult.setExecutedAt(LocalDateTime.now());

                long startTime = System.currentTimeMillis();
                try {
                    // 记录输入
                    Map<String, Object> stepInput = new HashMap<>();
                    if (step.getInputVars() != null && !step.getInputVars().isEmpty()) {
                        String[] vars = step.getInputVars().split("\\n");
                        for (String var : vars) {
                            var = var.trim();
                            if (!var.isEmpty()) {
                                stepInput.put(var, resolveVariablePath(var, context));
                            }
                        }
                    }
                    stepResult.setInput(stepInput);

                    // 执行步骤
                    Object result = executeStep(step, context);
                    stepResult.setOutput(result);
                    stepResult.setStatus("success");

                    // 更新上下文
                    context.put("step_" + (i + 1), result);
                    if (step.getName() != null) context.put(step.getName(), result);

                    // 条件分支处理
                    if ("condition".equals(step.getType()) && result instanceof Map) {
                        @SuppressWarnings("unchecked")
                        Map<String, Object> condResult = (Map<String, Object>) result;
                        String branch = (String) condResult.get("branch");
                        if (branch != null) {
                            int jumpIdx = findStepByName(steps, branch);
                            if (jumpIdx >= 0) {
                                i = jumpIdx - 1;
                                continue;
                            }
                        }
                    }

                    // 循环节点处理
                    if ("loop".equals(step.getType()) && result instanceof Map) {
                        @SuppressWarnings("unchecked")
                        Map<String, Object> loopResult = (Map<String, Object>) result;
                        Boolean shouldContinue = (Boolean) loopResult.get("continue");
                        if (Boolean.TRUE.equals(shouldContinue)) {
                            int loopStart = findStepByName(steps, step.getName() + "_body");
                            if (loopStart >= 0) {
                                i = loopStart - 1;
                                continue;
                            }
                        }
                    }

                } catch (Exception e) {
                    stepResult.setStatus("failed");
                    stepResult.setErrorMessage(e.getMessage());
                    debugResult.setErrorMessage(e.getMessage());
                    debugResult.setStatus("failed");
                    debugResult.getStepResults().add(stepResult);
                    break;
                }
                long endTime = System.currentTimeMillis();
                stepResult.setExecutionTimeMs(endTime - startTime);
                debugResult.getStepResults().add(stepResult);
                debugResult.setCurrentStepIndex(i);
                debugResult.setCurrentStepId(step.getId());
                debugResult.setCurrentStepName(step.getName());
            }

            if ("running".equals(debugResult.getStatus())) {
                debugResult.setStatus("completed");
            }

        } catch (Exception e) {
            log.error("Debug workflow failed", e);
            debugResult.setStatus("failed");
            debugResult.setErrorMessage(e.getMessage());
        }

        return debugResult;
    }

    /**
     * 根据步骤名称查找索引
     */
    private int findStepByName(List<AiAgentWorkflowDTO.WorkflowStep> steps, String name) {
        for (int i = 0; i < steps.size(); i++) {
            if (name.equals(steps.get(i).getName())) return i;
        }
        return -1;
    }

    /**
     * 替换字符串中的变量引用 {{varName}} 为实际值
     */
    private String resolveVariables(String template, Map<String, Object> context) {
        if (template == null) return null;
        Matcher matcher = VAR_PATTERN.matcher(template);
        StringBuffer sb = new StringBuffer();
        while (matcher.find()) {
            String varPath = matcher.group(1);
            Object value = resolveVariablePath(varPath, context);
            matcher.appendReplacement(sb, Matcher.quoteReplacement(String.valueOf(value != null ? value : "")));
        }
        matcher.appendTail(sb);
        return sb.toString();
    }

    /**
     * 解析变量路径，支持点号访问: input.name, step_1.result
     */
    @SuppressWarnings("unchecked")
    private Object resolveVariablePath(String path, Map<String, Object> context) {
        String[] parts = path.split("\\.");
        Object current = context.get(parts[0]);
        for (int i = 1; i < parts.length && current != null; i++) {
            if (current instanceof Map) {
                current = ((Map<String, Object>) current).get(parts[i]);
            } else {
                return null;
            }
        }
        return current;
    }

    // ==================== 步骤执行分发 ====================

    private Object executeStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        switch (step.getType()) {
            case "agent":
            case "llm":
                return executeAgentStep(step, context);
            case "classifier":
                return executeClassifierStep(step, context);
            case "extractor":
                return executeExtractorStep(step, context);
            case "mcp":
            case "tool":
                return executeMcpStep(step, context);
            case "http":
                return executeHttpStep(step, context);
            case "sql":
                return executeSqlStep(step, context);
            case "java":
                return executeJavaStep(step, context);
            case "knowledge":
                return executeKnowledgeStep(step, context);
            case "knowledgeWrite":
                return executeKnowledgeWriteStep(step, context);
            case "condition":
                return executeConditionStep(step, context);
            case "loop":
                return executeLoopStep(step, context);
            case "subflow":
                return executeSubflowStep(step, context);
            case "aggregate":
                return executeAggregateStep(step, context);
            case "script":
                return executeScriptStep(step, context);
            case "reply":
                return executeReplyStep(step, context);
            case "delay":
                return executeDelayStep(step);
            case "end":
                return "Workflow ended";
            default:
                return "Step executed: " + step.getName();
        }
    }

    // ==================== LLM / Agent 步骤 ====================

    private Object executeAgentStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing LLM step: {}, model: {}", step.getName(), step.getModel());

        // 解析提示词中的变量
        String prompt = resolveVariables(step.getPrompt(), context);
        if (prompt == null || prompt.isEmpty()) {
            prompt = "请根据输入进行处理";
        }

        ChatRequest request = new ChatRequest();
        request.setMessage(prompt);
        if (step.getModel() != null && !step.getModel().isEmpty()) {
            request.setModel(step.getModel());
        }

        try {
            ChatResponse response = aiLlmService.chat(request);
            Map<String, Object> result = new HashMap<>();
            result.put("type", "agent");
            result.put("name", step.getName());
            result.put("content", response.getContent());
            result.put("model", response.getModel());
            log.info("LLM step '{}' completed, response length: {}", step.getName(),
                response.getContent() != null ? response.getContent().length() : 0);
            return result;
        } catch (Exception e) {
            log.error("LLM step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "agent", "name", step.getName(), "error", e.getMessage());
        }
    }

    // ==================== 分类器步骤 ====================

    private Object executeClassifierStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Classifier step: {}", step.getName());

        String prompt = resolveVariables(step.getPrompt(), context);
        if (prompt == null || prompt.isEmpty()) {
            prompt = "请对以下输入进行分类，返回分类结果";
        }
        prompt += "\n\n请以JSON格式返回分类结果，格式为: {\"category\": \"分类名称\", \"confidence\": 0.95}";

        ChatRequest request = new ChatRequest();
        request.setMessage(prompt);
        if (step.getModel() != null) request.setModel(step.getModel());

        try {
            ChatResponse response = aiLlmService.chat(request);
            String content = response.getContent();
            // 尝试解析JSON结果
            Map<String, Object> result = new HashMap<>();
            result.put("type", "classifier");
            result.put("name", step.getName());
            result.put("rawResponse", content);

            // 尝试从响应中提取JSON
            int jsonStart = content.indexOf('{');
            int jsonEnd = content.lastIndexOf('}');
            if (jsonStart >= 0 && jsonEnd > jsonStart) {
                String jsonStr = content.substring(jsonStart, jsonEnd + 1);
                Map<String, Object> parsed = objectMapper.readValue(jsonStr,
                    new TypeReference<Map<String, Object>>() {});
                result.putAll(parsed);
            }
            return result;
        } catch (Exception e) {
            log.error("Classifier step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "classifier", "name", step.getName(), "error", e.getMessage());
        }
    }

    // ==================== 变量提取器步骤 ====================

    private Object executeExtractorStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Extractor step: {}", step.getName());

        String prompt = resolveVariables(step.getPrompt(), context);
        if (prompt == null || prompt.isEmpty()) {
            prompt = "请从以下输入中提取关键信息";
        }
        prompt += "\n\n请以JSON格式返回提取结果";

        ChatRequest request = new ChatRequest();
        request.setMessage(prompt);
        if (step.getModel() != null) request.setModel(step.getModel());

        try {
            ChatResponse response = aiLlmService.chat(request);
            String content = response.getContent();

            Map<String, Object> result = new HashMap<>();
            result.put("type", "extractor");
            result.put("name", step.getName());

            // 尝试解析JSON
            int jsonStart = content.indexOf('{');
            int jsonEnd = content.lastIndexOf('}');
            if (jsonStart >= 0 && jsonEnd > jsonStart) {
                String jsonStr = content.substring(jsonStart, jsonEnd + 1);
                Map<String, Object> extracted = objectMapper.readValue(jsonStr,
                    new TypeReference<Map<String, Object>>() {});
                result.put("extracted", extracted);
                // 将提取的变量放入上下文
                result.putAll(extracted);
            } else {
                result.put("extracted", content);
            }
            return result;
        } catch (Exception e) {
            log.error("Extractor step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "extractor", "name", step.getName(), "error", e.getMessage());
        }
    }

    // ==================== MCP / 工具调用步骤 ====================

    private Object executeMcpStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing MCP/Tool step: {}, tool: {}", step.getName(), step.getToolName());

        String toolName = resolveVariables(step.getToolName(), context);
        if (toolName == null || toolName.isEmpty()) {
            return Map.of("type", "mcp", "name", step.getName(), "error", "Tool name is empty");
        }

        // 查找 MCP 工具配置（按 name 字段匹配）
        AiMcpTool mcpTool = mcpToolMapper.selectOne(
            new LambdaQueryWrapper<AiMcpTool>()
                .eq(AiMcpTool::getName, toolName)
                .eq(AiMcpTool::getEnabled, true)
                .last("LIMIT 1")
        );

        if (mcpTool == null) {
            log.warn("MCP tool '{}' not found or disabled", toolName);
            return Map.of("type", "mcp", "name", step.getName(), "tool", toolName,
                "error", "Tool not found: " + toolName);
        }

        try {
            // 构建请求体
            ObjectNode requestBody = objectMapper.createObjectNode();
            requestBody.put("tool", toolName);

            // 解析输入变量
            Map<String, Object> params = new HashMap<>();
            if (step.getInputVars() != null && !step.getInputVars().isEmpty()) {
                for (String varName : step.getInputVars().split("[,\\n]")) {
                    varName = varName.trim();
                    if (!varName.isEmpty()) {
                        Object value = context.get(varName);
                        if (value == null) value = resolveVariablePath(varName, context);
                        if (value != null) params.put(varName, value);
                    }
                }
            }
            requestBody.set("params", objectMapper.valueToTree(params));

            // 发送 HTTP 请求到 MCP 工具 endpoint
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            String url = mcpTool.getEndpoint();
            if (url == null || url.isEmpty()) {
                url = "http://localhost:8080/api/mcp/execute";
            }

            HttpEntity<String> entity = new HttpEntity<>(
                objectMapper.writeValueAsString(requestBody), headers);
            ResponseEntity<String> response = restTemplate.exchange(
                url, HttpMethod.POST, entity, String.class);

            Map<String, Object> result = objectMapper.readValue(response.getBody(),
                new TypeReference<Map<String, Object>>() {});
            result.put("type", "mcp");
            result.put("name", step.getName());
            result.put("tool", toolName);
            log.info("MCP step '{}' completed via tool '{}'", step.getName(), toolName);
            return result;

        } catch (Exception e) {
            log.error("MCP step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "mcp", "name", step.getName(), "tool", toolName,
                "error", e.getMessage());
        }
    }

    // ==================== HTTP 请求步骤 ====================

    private Object executeHttpStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing HTTP step: {}, url: {}", step.getName(), step.getUrl());

        // 前端将 URL 存储在 toolName 中
        String url = resolveVariables(step.getUrl() != null ? step.getUrl() : step.getToolName(), context);
        if (url == null || url.isEmpty()) {
            return Map.of("type", "http", "name", step.getName(), "error", "URL is empty");
        }

        String method = step.getMethod() != null ? step.getMethod().toUpperCase() : "GET";

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            // 解析自定义 headers
            if (step.getHeaders() != null && !step.getHeaders().isEmpty()) {
                String resolvedHeaders = resolveVariables(step.getHeaders(), context);
                Map<String, String> headerMap = objectMapper.readValue(resolvedHeaders,
                    new TypeReference<Map<String, String>>() {});
                headerMap.forEach(headers::set);
            }

            HttpEntity<String> entity;
            if ("POST".equals(method) || "PUT".equals(method) || "PATCH".equals(method)) {
                String body = resolveVariables(step.getBody(), context);
                entity = new HttpEntity<>(body, headers);
            } else {
                entity = new HttpEntity<>(headers);
            }

            ResponseEntity<String> response = restTemplate.exchange(
                url, HttpMethod.valueOf(method), entity, String.class);

            Map<String, Object> result = new HashMap<>();
            result.put("type", "http");
            result.put("name", step.getName());
            result.put("statusCode", response.getStatusCode().value());

            // 尝试解析响应为JSON
            try {
                Object responseBody = objectMapper.readValue(response.getBody(), Object.class);
                result.put("body", responseBody);
            } catch (Exception e) {
                result.put("body", response.getBody());
            }

            log.info("HTTP step '{}' completed, status: {}", step.getName(), response.getStatusCode());
            return result;

        } catch (Exception e) {
            log.error("HTTP step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "http", "name", step.getName(), "url", url,
                "error", e.getMessage());
        }
    }

    // ==================== SQL 自定义步骤 ====================

    private Object executeSqlStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing SQL step: {}", step.getName());

        String sql = resolveVariables(step.getScriptCode(), context);
        if (sql == null || sql.isEmpty()) {
            return Map.of("type", "sql", "name", step.getName(), "error", "SQL is empty");
        }

        try (Connection conn = dataSource.getConnection();
             Statement stmt = conn.createStatement()) {

            boolean hasResultSet = stmt.execute(sql);

            Map<String, Object> result = new HashMap<>();
            result.put("type", "sql");
            result.put("name", step.getName());

            if (hasResultSet) {
                ResultSet rs = stmt.getResultSet();
                List<Map<String, Object>> rows = new ArrayList<>();
                int colCount = rs.getMetaData().getColumnCount();
                while (rs.next()) {
                    Map<String, Object> row = new LinkedHashMap<>();
                    for (int i = 1; i <= colCount; i++) {
                        row.put(rs.getMetaData().getColumnLabel(i), rs.getObject(i));
                    }
                    rows.add(row);
                }
                result.put("rows", rows);
                result.put("rowCount", rows.size());
                log.info("SQL step '{}' returned {} rows", step.getName(), rows.size());
            } else {
                int updateCount = stmt.getUpdateCount();
                result.put("affectedRows", updateCount);
                log.info("SQL step '{}' affected {} rows", step.getName(), updateCount);
            }

            return result;

        } catch (Exception e) {
            log.error("SQL step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "sql", "name", step.getName(), "error", e.getMessage());
        }
    }

    // ==================== Java 增强步骤 ====================

    private Object executeJavaStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Java step: {}, class: {}", step.getName(), step.getJavaClass());

        String javaClass = resolveVariables(step.getJavaClass(), context);
        if (javaClass == null || javaClass.isEmpty()) {
            return Map.of("type", "java", "name", step.getName(), "error", "Java class name is empty");
        }

        try {
            Class<?> clazz = Class.forName(javaClass);
            Object instance = clazz.getDeclaredConstructor().newInstance();

            // 查找 execute 方法，参数为 Map
            java.lang.reflect.Method method = clazz.getMethod("execute", Map.class);
            Object result = method.invoke(instance, context);

            Map<String, Object> wrapper = new HashMap<>();
            wrapper.put("type", "java");
            wrapper.put("name", step.getName());
            wrapper.put("javaClass", javaClass);
            wrapper.put("result", result);
            log.info("Java step '{}' completed via class '{}'", step.getName(), javaClass);
            return wrapper;

        } catch (ClassNotFoundException e) {
            log.error("Java class '{}' not found", javaClass);
            return Map.of("type", "java", "name", step.getName(), "javaClass", javaClass,
                "error", "Class not found: " + javaClass);
        } catch (Exception e) {
            log.error("Java step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "java", "name", step.getName(), "javaClass", javaClass,
                "error", e.getMessage());
        }
    }

    // ==================== 知识库检索步骤 ====================

    private Object executeKnowledgeStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Knowledge step: {}, knowledgeId: {}", step.getName(), step.getKnowledgeId());

        String knowledgeId = resolveVariables(step.getKnowledgeId(), context);

        // 从上下文中获取查询内容
        String query = "";
        Object inputObj = context.get("input");
        if (inputObj instanceof Map) {
            @SuppressWarnings("unchecked")
            Map<String, Object> inputMap = (Map<String, Object>) inputObj;
            query = String.valueOf(inputMap.getOrDefault("message",
                inputMap.getOrDefault("query", inputMap.toString())));
        }

        try {
            // 调用 RAG 搜索（知识库检索暂不支持按 knowledgeId 过滤，使用全局搜索）
            List<RagSearchResult> results = aiRagService.search(query, 5);

            Map<String, Object> result = new HashMap<>();
            result.put("type", "knowledge");
            result.put("name", step.getName());
            result.put("knowledgeId", knowledgeId);
            result.put("query", query);
            result.put("resultCount", results.size());

            // 将检索结果拼接为文本，供后续 LLM 步骤使用
            StringBuilder contextText = new StringBuilder();
            for (RagSearchResult doc : results) {
                if (doc.getContent() != null) {
                    contextText.append(doc.getContent()).append("\n");
                }
            }
            result.put("context", contextText.toString());

            log.info("Knowledge step '{}' found {} results", step.getName(), results.size());
            return result;

        } catch (Exception e) {
            log.error("Knowledge step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "knowledge", "name", step.getName(),
                "knowledgeId", knowledgeId, "error", e.getMessage());
        }
    }

    // ==================== 知识库写入步骤 ====================

    private Object executeKnowledgeWriteStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing KnowledgeWrite step: {}", step.getName());

        String knowledgeId = resolveVariables(step.getKnowledgeId(), context);

        // 从上下文中获取要写入的内容
        Object contentObj = context.get("input");
        String content = contentObj != null ? contentObj.toString() : "";

        // 尝试从前面步骤的结果中获取内容
        for (Map.Entry<String, Object> entry : context.entrySet()) {
            if (entry.getValue() instanceof Map) {
                @SuppressWarnings("unchecked")
                Map<String, Object> stepResult = (Map<String, Object>) entry.getValue();
                if (stepResult.containsKey("content")) {
                    content = String.valueOf(stepResult.get("content"));
                    break;
                }
            }
        }

        try {
            aiRagService.addDocument(content, "workflow", step.getName());

            Map<String, Object> result = new HashMap<>();
            result.put("type", "knowledgeWrite");
            result.put("name", step.getName());
            result.put("knowledgeId", knowledgeId);
            result.put("written", true);
            log.info("KnowledgeWrite step '{}' completed", step.getName());
            return result;

        } catch (Exception e) {
            log.error("KnowledgeWrite step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "knowledgeWrite", "name", step.getName(),
                "knowledgeId", knowledgeId, "error", e.getMessage());
        }
    }

    // ==================== 条件分支步骤 ====================

    private Object executeConditionStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Condition step: {}, condition: {}", step.getName(), step.getCondition());

        String condition = resolveVariables(step.getCondition(), context);
        if (condition == null || condition.isEmpty()) {
            return Map.of("type", "condition", "name", step.getName(), "branch", "else", "result", false);
        }

        boolean result = evaluateCondition(condition, context);

        Map<String, Object> resultMap = new HashMap<>();
        resultMap.put("type", "condition");
        resultMap.put("name", step.getName());
        resultMap.put("condition", step.getCondition());
        resultMap.put("resolvedCondition", condition);
        resultMap.put("result", result);
        resultMap.put("branch", result ? "true" : "else");

        log.info("Condition step '{}' evaluated to: {}", step.getName(), result);
        return resultMap;
    }

    /**
     * 简单的条件表达式评估
     * 支持: ==, !=, >, <, >=, <=, contains, exists, empty, true, false
     */
    private boolean evaluateCondition(String expression, Map<String, Object> context) {
        expression = expression.trim();

        // 布尔常量
        if ("true".equalsIgnoreCase(expression)) return true;
        if ("false".equalsIgnoreCase(expression)) return false;

        // exists 检查
        if (expression.startsWith("exists ")) {
            String varName = expression.substring(7).trim();
            return resolveVariablePath(varName, context) != null;
        }

        // empty 检查
        if (expression.startsWith("empty ")) {
            String varName = expression.substring(6).trim();
            Object val = resolveVariablePath(varName, context);
            return val == null || (val instanceof String && ((String) val).isEmpty())
                || (val instanceof Collection && ((Collection<?>) val).isEmpty());
        }

        // 比较操作
        String[] operators = {"==", "!=", ">=", "<=", ">", "<", "contains"};
        for (String op : operators) {
            int idx = expression.indexOf(op);
            if (idx > 0) {
                String leftExpr = expression.substring(0, idx).trim();
                String rightExpr = expression.substring(idx + op.length()).trim();

                Object leftVal = resolveVariablePath(leftExpr, context);
                if (leftVal == null) leftVal = leftExpr;

                Object rightVal = resolveVariablePath(rightExpr, context);
                if (rightVal == null) rightVal = rightExpr;

                return compareValues(leftVal, rightVal, op);
            }
        }

        // 直接变量值判断
        Object val = resolveVariablePath(expression, context);
        if (val instanceof Boolean) return (Boolean) val;
        if (val instanceof Number) return ((Number) val).doubleValue() != 0;
        if (val instanceof String) return !((String) val).isEmpty() && !"false".equalsIgnoreCase((String) val);
        return val != null;
    }

    @SuppressWarnings("unchecked")
    private boolean compareValues(Object left, Object right, String operator) {
        // contains 操作
        if ("contains".equals(operator)) {
            if (left instanceof String && right instanceof String) {
                return ((String) left).contains((String) right);
            }
            if (left instanceof Collection) {
                return ((Collection<Object>) left).contains(right);
            }
            return false;
        }

        // 数值比较
        if (left instanceof Number && right instanceof Number) {
            double l = ((Number) left).doubleValue();
            double r = ((Number) right).doubleValue();
            return switch (operator) {
                case "==" -> l == r;
                case "!=" -> l != r;
                case ">" -> l > r;
                case "<" -> l < r;
                case ">=" -> l >= r;
                case "<=" -> l <= r;
                default -> false;
            };
        }

        // 字符串比较
        String l = String.valueOf(left);
        String r = String.valueOf(right);
        return switch (operator) {
            case "==" -> l.equals(r);
            case "!=" -> !l.equals(r);
            case ">" -> l.compareTo(r) > 0;
            case "<" -> l.compareTo(r) < 0;
            case ">=" -> l.compareTo(r) >= 0;
            case "<=" -> l.compareTo(r) <= 0;
            default -> false;
        };
    }

    // ==================== 循环步骤 ====================

    private Object executeLoopStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Loop step: {}, condition: {}", step.getName(), step.getLoopCondition());

        String condition = resolveVariables(step.getLoopCondition(), context);
        int maxIterations = step.getMaxIterations() != null ? step.getMaxIterations() : 100;

        // 获取当前循环计数
        String counterKey = step.getName() + "_count";
        int currentCount = context.containsKey(counterKey)
            ? ((Number) context.get(counterKey)).intValue() : 0;

        boolean shouldContinue = false;
        if (currentCount < maxIterations) {
            shouldContinue = condition == null || condition.isEmpty()
                || evaluateCondition(condition, context);
        }

        if (shouldContinue) {
            context.put(counterKey, currentCount + 1);
        }

        Map<String, Object> result = new HashMap<>();
        result.put("type", "loop");
        result.put("name", step.getName());
        result.put("iteration", currentCount + 1);
        result.put("continue", shouldContinue);
        result.put("maxIterations", maxIterations);

        log.info("Loop step '{}' iteration {}/{}", step.getName(), currentCount + 1, maxIterations);
        return result;
    }

    // ==================== 子流程步骤 ====================

    private Object executeSubflowStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Subflow step: {}, subflowId: {}", step.getName(), step.getSubflowId());

        String subflowId = resolveVariables(step.getSubflowId(), context);
        if (subflowId == null || subflowId.isEmpty()) {
            return Map.of("type", "subflow", "name", step.getName(), "error", "Subflow ID is empty");
        }

        try {
            // 查找子流程
            AiAgentWorkflow subflow;
            try {
                Long id = Long.parseLong(subflowId);
                subflow = workflowMapper.selectById(id);
            } catch (NumberFormatException e) {
                subflow = workflowMapper.selectOne(
                    new LambdaQueryWrapper<AiAgentWorkflow>()
                        .eq(AiAgentWorkflow::getName, subflowId)
                        .eq(AiAgentWorkflow::getEnabled, true)
                        .last("LIMIT 1")
                );
            }

            if (subflow == null) {
                return Map.of("type", "subflow", "name", step.getName(),
                    "subflowId", subflowId, "error", "Subflow not found");
            }

            // 执行子流程（同步）
            List<AiAgentWorkflowDTO.WorkflowStep> subSteps = convertJsonToSteps(subflow.getSteps());
            Map<String, Object> subContext = new HashMap<>(context);
            Map<String, Object> subOutputs = new HashMap<>();

            for (AiAgentWorkflowDTO.WorkflowStep subStep : subSteps) {
                Object result = executeStep(subStep, subContext);
                subContext.put("step_" + subStep.getOrder(), result);
                if (subStep.getName() != null) subOutputs.put(subStep.getName(), result);
            }

            Map<String, Object> result = new HashMap<>();
            result.put("type", "subflow");
            result.put("name", step.getName());
            result.put("subflowId", subflowId);
            result.put("subflowName", subflow.getName());
            result.put("outputs", subOutputs);

            log.info("Subflow step '{}' completed, subflow: {}", step.getName(), subflow.getName());
            return result;

        } catch (Exception e) {
            log.error("Subflow step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "subflow", "name", step.getName(),
                "subflowId", subflowId, "error", e.getMessage());
        }
    }

    // ==================== 变量聚合步骤 ====================

    private Object executeAggregateStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Aggregate step: {}", step.getName());

        Map<String, Object> aggregated = new HashMap<>();
        aggregated.put("type", "aggregate");
        aggregated.put("name", step.getName());

        // 解析聚合规则
        String rule = step.getAggregateRule();
        if (rule != null && !rule.isEmpty()) {
            rule = resolveVariables(rule, context);
            try {
                Map<String, String> rules = objectMapper.readValue(rule,
                    new TypeReference<Map<String, String>>() {});
                for (Map.Entry<String, String> entry : rules.entrySet()) {
                    String targetKey = entry.getKey();
                    String sourcePath = entry.getValue();
                    Object value = resolveVariablePath(sourcePath, context);
                    aggregated.put(targetKey, value);
                }
            } catch (Exception e) {
                log.warn("Failed to parse aggregate rule: {}", rule);
            }
        } else {
            // 默认聚合：收集所有 step_ 开头的变量
            for (Map.Entry<String, Object> entry : context.entrySet()) {
                if (entry.getKey().startsWith("step_")) {
                    aggregated.put(entry.getKey(), entry.getValue());
                }
            }
        }

        log.info("Aggregate step '{}' completed with {} fields", step.getName(), aggregated.size() - 2);
        return aggregated;
    }

    // ==================== 脚本执行步骤 ====================

    private Object executeScriptStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Script step: {}", step.getName());

        String script = resolveVariables(step.getScriptCode(), context);
        if (script == null || script.isEmpty()) {
            return Map.of("type", "script", "name", step.getName(), "error", "Script is empty");
        }

        try {
            // 使用 Nashorn JavaScript 引擎执行脚本
            javax.script.ScriptEngineManager manager = new javax.script.ScriptEngineManager();
            javax.script.ScriptEngine engine = manager.getEngineByName("js");

            if (engine == null) {
                // 回退：尝试 groovy
                engine = manager.getEngineByName("groovy");
            }

            if (engine == null) {
                return Map.of("type", "script", "name", step.getName(),
                    "error", "No script engine available (js/groovy)");
            }

            // 将上下文变量绑定到脚本引擎
            for (Map.Entry<String, Object> entry : context.entrySet()) {
                engine.put(entry.getKey(), entry.getValue());
            }

            Object result = engine.eval(script);

            Map<String, Object> wrapper = new HashMap<>();
            wrapper.put("type", "script");
            wrapper.put("name", step.getName());
            wrapper.put("result", result);
            log.info("Script step '{}' completed", step.getName());
            return wrapper;

        } catch (Exception e) {
            log.error("Script step '{}' failed: {}", step.getName(), e.getMessage());
            return Map.of("type", "script", "name", step.getName(), "error", e.getMessage());
        }
    }

    // ==================== 直接回复步骤 ====================

    private Object executeReplyStep(AiAgentWorkflowDTO.WorkflowStep step, Map<String, Object> context) {
        log.info("Executing Reply step: {}", step.getName());

        String content = resolveVariables(step.getReplyContent(), context);
        if (content == null || content.isEmpty()) {
            content = resolveVariables(step.getPrompt(), context);
        }

        Map<String, Object> result = new HashMap<>();
        result.put("type", "reply");
        result.put("name", step.getName());
        result.put("content", content != null ? content : "");
        log.info("Reply step '{}' completed", step.getName());
        return result;
    }

    // ==================== 延时步骤 ====================

    private Object executeDelayStep(AiAgentWorkflowDTO.WorkflowStep step) {
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return Map.of("type", "delay", "name", step.getName(), "delayMs", 1000);
    }

    // ==================== 停止执行 ====================

    @Override
    @Transactional
    public void stopExecution(Long id) {
        AiAgentWorkflowExec exec = execMapper.selectById(id);
        if (exec != null && "running".equals(exec.getStatus())) {
            exec.setStatus("stopped");
            exec.setCompletedAt(LocalDateTime.now());
            execMapper.updateById(exec);
        }
    }

    // ==================== 转换方法 ====================

    private AiAgentWorkflowDTO convertToDTO(AiAgentWorkflow workflow) {
        AiAgentWorkflowDTO dto = new AiAgentWorkflowDTO();
        dto.setId(workflow.getId());
        dto.setName(workflow.getName());
        dto.setDescription(workflow.getDescription());
        dto.setAgentType(workflow.getAgentType());
        dto.setSteps(convertJsonToSteps(workflow.getSteps()));
        dto.setEdges(convertJsonToEdges(workflow.getEdges()));
        dto.setVariables(convertJsonToVariables(workflow.getVariables()));
        dto.setTimeout(workflow.getTimeout());
        dto.setEnabled(workflow.getEnabled());
        return dto;
    }

    private AiAgentWorkflowExecDTO convertExecToDTO(AiAgentWorkflowExec exec) {
        AiAgentWorkflowExecDTO dto = new AiAgentWorkflowExecDTO();
        dto.setId(exec.getId());
        dto.setWorkflowId(exec.getWorkflowId());
        dto.setStatus(exec.getStatus());
        dto.setInput(convertJsonToVariables(exec.getInput()));
        dto.setOutput(convertJsonToVariables(exec.getOutput()));
        dto.setErrorMessage(exec.getErrorMessage());
        dto.setCurrentStep(exec.getCurrentStep());
        dto.setStartedAt(exec.getStartedAt());
        dto.setCompletedAt(exec.getCompletedAt());
        dto.setCreatedAt(exec.getCreatedAt());
        return dto;
    }

    private String convertStepsToJson(List<AiAgentWorkflowDTO.WorkflowStep> steps) {
        if (steps == null || steps.isEmpty()) return "[]";
        try {
            return objectMapper.writeValueAsString(steps);
        } catch (Exception e) {
            return "[]";
        }
    }

    private List<AiAgentWorkflowDTO.WorkflowStep> convertJsonToSteps(String json) {
        if (json == null || json.isEmpty()) return new ArrayList<>();
        try {
            return objectMapper.readValue(json, new TypeReference<List<AiAgentWorkflowDTO.WorkflowStep>>() {});
        } catch (Exception e) {
            return new ArrayList<>();
        }
    }

    private String convertEdgesToJson(List<AiAgentWorkflowDTO.WorkflowEdge> edges) {
        if (edges == null || edges.isEmpty()) return "[]";
        try {
            return objectMapper.writeValueAsString(edges);
        } catch (Exception e) {
            return "[]";
        }
    }

    private List<AiAgentWorkflowDTO.WorkflowEdge> convertJsonToEdges(String json) {
        if (json == null || json.isEmpty()) return new ArrayList<>();
        try {
            return objectMapper.readValue(json, new TypeReference<List<AiAgentWorkflowDTO.WorkflowEdge>>() {});
        } catch (Exception e) {
            return new ArrayList<>();
        }
    }

    private String convertVariablesToJson(Map<String, Object> variables) {
        if (variables == null || variables.isEmpty()) return "{}";
        try {
            return objectMapper.writeValueAsString(variables);
        } catch (Exception e) {
            return "{}";
        }
    }

    private Map<String, Object> convertJsonToVariables(String json) {
        if (json == null || json.isEmpty()) return new HashMap<>();
        try {
            return objectMapper.readValue(json, new TypeReference<Map<String, Object>>() {});
        } catch (Exception e) {
            return new HashMap<>();
        }
    }
}
