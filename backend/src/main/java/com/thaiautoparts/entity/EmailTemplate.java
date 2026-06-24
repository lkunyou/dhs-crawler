package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_email_template")
public class EmailTemplate {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("template_name")
    private String templateName;
    
    private String subject;
    private String content;
    private String language;
    private String category;
    
    @TableField("day_sequence")
    private Integer daySequence;
    
    @TableField("is_active")
    private Boolean isActive;
    
    @TableField("open_rate")
    private Double openRate;
    
    @TableField("reply_rate")
    private Double replyRate;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
