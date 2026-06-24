package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("p_follow_up_record")
public class FollowUpRecord {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("company_id")
    private Long companyId;
    
    @TableField("contact_id")
    private Long contactId;
    
    @TableField("follow_up_type")
    private String followUpType;
    
    private String direction;
    private String summary;
    private String detail;
    
    @TableField("next_action")
    private String nextAction;
    
    @TableField("next_action_date")
    private LocalDate nextActionDate;
    
    private String outcome;
    private String sentiment;
    
    @TableField(value = "attachments", typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String attachments;
    
    @TableField("created_by")
    private Long createdBy;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}
