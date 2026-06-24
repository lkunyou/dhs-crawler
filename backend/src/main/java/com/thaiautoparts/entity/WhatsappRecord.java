package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_whatsapp_record")
public class WhatsappRecord {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("company_id")
    private Long companyId;
    
    @TableField("contact_id")
    private Long contactId;
    
    @TableField("phone_number")
    private String phoneNumber;
    
    @TableField("message_type")
    private String messageType;
    
    private String content;
    
    @TableField("media_url")
    private String mediaUrl;
    
    private String direction;
    private String status;
    
    @TableField("sent_at")
    private LocalDateTime sentAt;
    
    @TableField("delivered_at")
    private LocalDateTime deliveredAt;
    
    @TableField("read_at")
    private LocalDateTime readAt;
    
    @TableField("replied_at")
    private LocalDateTime repliedAt;
    
    @TableField("reply_content")
    private String replyContent;
    
    @TableField("error_message")
    private String errorMessage;
    
    @TableField("message_id")
    private String messageId;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
}
