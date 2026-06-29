package com.thaiautoparts.dto;

import lombok.Data;
import java.util.List;
import java.util.Map;

@Data
public class AiAgentWorkflowDTO {
    private Long id;
    private String name;
    private String description;
    private String agentType;
    private List<WorkflowStep> steps;
    private List<WorkflowEdge> edges;
    private Map<String, Object> variables;
    private Integer timeout;
    private Boolean enabled;
    
    @Data
    public static class WorkflowEdge {
        private String id;
        private String sourceNodeId;
        private String targetNodeId;
        private String type;
        private String sourceAnchorId;
        private String targetAnchorId;
        private List<Map<String, Object>> pointsList;
    }
    
    @Data
    public static class WorkflowStep {
        private String id;
        private Integer order;
        private String name;
        private String type; // agent, mcp, delay, condition, loop, knowledge, knowledgeWrite, subflow, aggregate, script, reply, http, sql, java, classifier, extractor, end
        private String nodeType; // llm, classifier, extractor, knowledge, knowledgeWrite, condition, loop, subflow, aggregate, script, reply, tool, http, sql, java, end
        private Double x; // 画布X坐标
        private Double y; // 画布Y坐标
        private String config; // JSON配置
        private String nextStep; // 下一步
        private String condition; // 条件表达式
        
        // 通用字段
        private String inputVars;
        private String outputVars;
        
        // LLM / Classifier
        private String model;
        private String prompt;
        
        // Extractor
        private String extractFields;
        
        // Knowledge
        private String knowledgeId;
        
        // Tool / HTTP / Java / Subflow / Knowledge
        private String toolName;
        
        // HTTP
        private String url;
        private String method;
        private String headers;
        private String body;
        
        // SQL
        private String sql;
        
        // Java
        private String javaClass;
        
        // Script
        private String scriptCode;
        
        // Reply
        private String replyContent;
        
        // Loop
        private String loopCondition;
        private Integer maxIterations;
        
        // Subflow
        private String subflowId;
        
        // Aggregate
        private String aggregateRule;
    }
}
