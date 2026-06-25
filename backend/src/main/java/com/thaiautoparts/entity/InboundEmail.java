package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_inbound_email")
public class InboundEmail {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("company_id")
    private Long companyId;
    
    @TableField("contact_id")
    private Long contactId;
    
    @TableField("from_email")
    private String fromEmail;
    
    @TableField("from_name")
    private String fromName;
    
    @TableField("to_email")
    private String toEmail;
    
    private String subject;
    private String content;
    
    @TableField("message_id")
    private String messageId;
    
    @TableField("in_reply_to")
    private String inReplyTo;
    
    @TableField("is_read")
    private Boolean isRead;
    
    @TableField("is_starred")
    private Boolean isStarred;
    
    @TableField("attachments")
    private String attachments;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}