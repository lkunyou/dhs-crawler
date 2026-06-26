package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_crawler_task")
public class CrawlerTask {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("task_name")
    private String taskName;
    
    @TableField("source_type")
    private String sourceType;
    
    @TableField(value = "keywords", typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String keywords;
    
    @TableField("target_country")
    private String targetCountry;
    
    @TableField("target_city")
    private String targetCity;
    
    @TableField(value = "filters", typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String filters;
    
    private String status;
    private Integer progress;
    
    @TableField("total_found")
    private Integer totalFound;
    
    @TableField("new_companies")
    private Integer newCompanies;
    
    @TableField("duplicates")
    private Integer duplicates;
    
    private Integer errors;
    
    @TableField("started_at")
    private LocalDateTime startedAt;
    
    @TableField("completed_at")
    private LocalDateTime completedAt;
    
    @TableField("error_message")
    private String errorMessage;
    
    @TableField("log_content")
    private String logContent;
    
    @TableField("created_by")
    private Long createdBy;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
