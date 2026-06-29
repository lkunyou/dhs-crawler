package com.thaiautoparts.dto;

import lombok.Data;
import java.time.LocalDateTime;
import java.util.Map;

@Data
public class AiAgentWorkflowExecDTO {
    private Long id;
    private String workflowId;
    private String workflowName;
    private String status;
    private Map<String, Object> input;
    private Map<String, Object> output;
    private String errorMessage;
    private Integer currentStep;
    private LocalDateTime startedAt;
    private LocalDateTime completedAt;
    private LocalDateTime createdAt;
}
