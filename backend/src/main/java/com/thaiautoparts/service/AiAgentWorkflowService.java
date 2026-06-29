package com.thaiautoparts.service;

import com.thaiautoparts.dto.AiAgentWorkflowDTO;
import com.thaiautoparts.dto.AiAgentWorkflowExecDTO;
import java.util.List;
import java.util.Map;

public interface AiAgentWorkflowService {
    // 工作流管理
    List<AiAgentWorkflowDTO> getWorkflows();
    List<AiAgentWorkflowDTO> getEnabledWorkflows();
    AiAgentWorkflowDTO getWorkflow(Long id);
    AiAgentWorkflowDTO getWorkflowByAgentType(String agentType);
    AiAgentWorkflowDTO createWorkflow(AiAgentWorkflowDTO dto);
    AiAgentWorkflowDTO updateWorkflow(Long id, AiAgentWorkflowDTO dto);
    void deleteWorkflow(Long id);
    void toggleWorkflow(Long id, Boolean enabled);
    
    // 执行管理
    List<AiAgentWorkflowExecDTO> getExecutions(Long workflowId);
    AiAgentWorkflowExecDTO getExecution(Long id);
    AiAgentWorkflowExecDTO executeWorkflow(Long workflowId, Map<String, Object> input);
    void stopExecution(Long id);
}
