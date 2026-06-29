package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("ai_agent_task")
public class AiAgentTask {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String taskId;
    
    private String agentType;
    
    private String input;
    
    private String status;
    
    private String result;
    
    private String errorMessage;
    
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
