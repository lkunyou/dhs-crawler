package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("ai_agent_workflow")
public class AiAgentWorkflow {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String name;
    
    private String description;
    
    private String agentType;
    
    private String steps; // JSON格式的步骤定义
    
    private String edges; // JSON格式的连线定义
    
    private String variables; // JSON格式的变量定义
    
    private Integer timeout; // 超时时间（秒）
    
    private Boolean enabled;
    
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
