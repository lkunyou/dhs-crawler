package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("ai_agent")
public class AiAgent {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String agentType;
    
    private String name;
    
    private String description;
    
    private String prompt;
    
    private String config;
    
    private Boolean enabled;
    
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
