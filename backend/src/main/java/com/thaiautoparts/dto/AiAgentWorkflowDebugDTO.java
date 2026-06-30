package com.thaiautoparts.dto;

import lombok.Data;
import java.time.LocalDateTime;
import java.util.Map;

/**
 * 工作流调试结果DTO
 */
@Data
public class AiAgentWorkflowDebugDTO {

    private String status; // running, completed, failed
    private String errorMessage;
    private int totalSteps;
    private int currentStepIndex;
    private String currentStepId;
    private String currentStepName;
    private java.util.List<StepResult> stepResults;

    @Data
    public static class StepResult {
        private int index;
        private String stepId;
        private String stepName;
        private String stepType;
        private String status; // success, failed, skipped
        private Object input;
        private Object output;
        private String errorMessage;
        private long executionTimeMs;
        private LocalDateTime executedAt;
    }
}
