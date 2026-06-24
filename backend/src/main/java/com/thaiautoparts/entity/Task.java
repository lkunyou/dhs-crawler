package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_task")
public class Task {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("company_id")
    private Long companyId;
    
    @TableField("contact_id")
    private Long contactId;
    
    @TableField("assigned_to")
    private Long assignedTo;
    
    @TableField("task_type")
    private String taskType;
    
    private String title;
    private String description;
    private String priority;
    private String status;
    
    @TableField("due_date")
    private LocalDateTime dueDate;
    
    @TableField("completed_at")
    private LocalDateTime completedAt;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
