package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("ai_agent_workflow_exec")
public class AiAgentWorkflowExec {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String workflowId;
    
    private String status; // pending, running, completed, failed
    
    private String input; // JSON格式的输入参数
    
    private String output; // JSON格式的输出结果
    
    private String errorMessage;
    
    private Integer currentStep;
    
    private LocalDateTime startedAt;
    
    private LocalDateTime completedAt;
    
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
