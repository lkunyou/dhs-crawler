package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_email_record")
public class EmailRecord {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("campaign_id")
    private Long campaignId;
    
    @TableField("company_id")
    private Long companyId;
    
    @TableField("contact_id")
    private Long contactId;
    
    @TableField("template_id")
    private Long templateId;
    
    @TableField("in_reply_to_email_id")
    private Long inReplyToEmailId;
    
    @TableField("recipient_email")
    private String recipientEmail;
    
    @TableField(exist = false)
    private String recipientName;
    
    @TableField(exist = false)
    private String companyName;
    
    private String subject;
    private String content;
    private String status;
    
    @TableField("sent_at")
    private LocalDateTime sentAt;
    
    @TableField("opened_at")
    private LocalDateTime openedAt;
    
    @TableField("replied_at")
    private LocalDateTime repliedAt;
    
    @TableField("reply_content")
    private String replyContent;
    
    @TableField("error_message")
    private String errorMessage;
    
    @TableField("tracking_id")
    private String trackingId;
    
    @TableField("message_id")
    private String messageId;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}
