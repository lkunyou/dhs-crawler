package com.thaiautoparts.controller;

import com.thaiautoparts.dto.AiAgentWorkflowDTO;
import com.thaiautoparts.dto.AiAgentWorkflowExecDTO;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.AiAgentWorkflowService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/ai/workflow")
@RequiredArgsConstructor
public class AiAgentWorkflowController {

    private final AiAgentWorkflowService workflowService;

    @GetMapping
    public Result<List<AiAgentWorkflowDTO>> getWorkflows() {
        return Result.success(workflowService.getWorkflows());
    }

    @GetMapping("/enabled")
    public Result<List<AiAgentWorkflowDTO>> getEnabledWorkflows() {
        return Result.success(workflowService.getEnabledWorkflows());
    }

    @GetMapping("/{id}")
    public Result<AiAgentWorkflowDTO> getWorkflow(@PathVariable Long id) {
        return Result.success(workflowService.getWorkflow(id));
    }

    @GetMapping("/agent/{agentType}")
    public Result<AiAgentWorkflowDTO> getWorkflowByAgentType(@PathVariable String agentType) {
        return Result.success(workflowService.getWorkflowByAgentType(agentType));
    }

    @PostMapping
    public Result<AiAgentWorkflowDTO> createWorkflow(@RequestBody AiAgentWorkflowDTO dto) {
        return Result.success(workflowService.createWorkflow(dto));
    }

    @PutMapping("/{id}")
    public Result<AiAgentWorkflowDTO> updateWorkflow(@PathVariable Long id, @RequestBody AiAgentWorkflowDTO dto) {
        return Result.success(workflowService.updateWorkflow(id, dto));
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteWorkflow(@PathVariable Long id) {
        workflowService.deleteWorkflow(id);
        return Result.success();
    }

    @PostMapping("/{id}/toggle")
    public Result<Void> toggleWorkflow(@PathVariable Long id, @RequestParam Boolean enabled) {
        workflowService.toggleWorkflow(id, enabled);
        return Result.success();
    }

    @GetMapping("/{id}/executions")
    public Result<List<AiAgentWorkflowExecDTO>> getExecutions(@PathVariable Long id) {
        return Result.success(workflowService.getExecutions(id));
    }

    @GetMapping("/executions")
    public Result<List<AiAgentWorkflowExecDTO>> getAllExecutions() {
        return Result.success(workflowService.getExecutions(null));
    }

    @GetMapping("/execution/{execId}")
    public Result<AiAgentWorkflowExecDTO> getExecution(@PathVariable Long execId) {
        return Result.success(workflowService.getExecution(execId));
    }

    @PostMapping("/{id}/execute")
    public Result<AiAgentWorkflowExecDTO> executeWorkflow(@PathVariable Long id, @RequestBody Map<String, Object> input) {
        return Result.success(workflowService.executeWorkflow(id, input));
    }

    @PostMapping("/execution/{execId}/stop")
    public Result<Void> stopExecution(@PathVariable Long execId) {
        workflowService.stopExecution(execId);
        return Result.success();
    }
}
