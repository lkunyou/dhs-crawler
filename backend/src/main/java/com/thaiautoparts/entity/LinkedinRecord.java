package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_linkedin_record")
public class LinkedinRecord {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("company_id")
    private Long companyId;
    
    @TableField("contact_id")
    private Long contactId;
    
    @TableField("linkedin_profile_url")
    private String linkedinProfileUrl;
    
    @TableField("linkedin_id")
    private String linkedinId;
    
    @TableField("action_type")
    private String actionType;
    
    private String status;
    
    @TableField("message_content")
    private String messageContent;
    
    @TableField("response_content")
    private String responseContent;
    
    @TableField("scheduled_at")
    private LocalDateTime scheduledAt;
    
    @TableField("executed_at")
    private LocalDateTime executedAt;
    
    @TableField("error_message")
    private String errorMessage;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}
