package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("ai_message")
public class AiMessage {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private Long conversationId;
    
    private String role;
    
    private String content;
    
    private String model;
    
    private String agentType;
    
    private String mcpTool;
    
    private String mcpResult;
    
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}
