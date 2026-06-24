package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDate;

@Data
@TableName("p_daily_stats")
public class DailyStats {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("stat_date")
    private LocalDate statDate;
    
    @TableField("new_leads")
    private Integer newLeads;
    
    @TableField(value = "leads_by_source", typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String leadsBySource;
    
    @TableField(value = "leads_by_grade", typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String leadsByGrade;
    
    @TableField("emails_sent")
    private Integer emailsSent;
    
    @TableField("emails_opened")
    private Integer emailsOpened;
    
    @TableField("emails_replied")
    private Integer emailsReplied;
    
    @TableField("whatsapp_sent")
    private Integer whatsappSent;
    
    @TableField("whatsapp_replied")
    private Integer whatsappReplied;
    
    @TableField("linkedin_actions")
    private Integer linkedinActions;
    
    @TableField("new_replies")
    private Integer newReplies;
    
    @TableField("new_quotations")
    private Integer newQuotations;
    
    @TableField("new_samples")
    private Integer newSamples;
    
    @TableField("deals_won")
    private Integer dealsWon;
    
    @TableField("deals_lost")
    private Integer dealsLost;
    
    @TableField("email_open_rate")
    private Double emailOpenRate;
    
    @TableField("email_reply_rate")
    private Double emailReplyRate;
    
    @TableField("whatsapp_reply_rate")
    private Double whatsappReplyRate;
    
    @TableField("overall_conversion_rate")
    private Double overallConversionRate;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private java.time.LocalDateTime createdAt;
    
    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private java.time.LocalDateTime updatedAt;
}
