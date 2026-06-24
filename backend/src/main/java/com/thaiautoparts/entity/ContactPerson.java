package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_contact_person")
public class ContactPerson {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("company_id")
    private Long companyId;
    
    @TableField("first_name")
    private String firstName;
    
    @TableField("last_name")
    private String lastName;
    
    @TableField("full_name")
    private String fullName;
    
    @TableField("name_th")
    private String nameTh;
    
    @TableField("job_title")
    private String jobTitle;
    
    private String department;
    
    @TableField("is_decision_maker")
    private Boolean isDecisionMaker;
    
    @TableField("seniority_level")
    private String seniorityLevel;
    
    private String email;
    
    @TableField("email_verified")
    private Boolean emailVerified;
    
    private String phone;
    private String whatsapp;
    
    @TableField("linkedin_url")
    private String linkedinUrl;
    
    @TableField("last_contacted_at")
    private LocalDateTime lastContactedAt;
    
    @TableField("contact_count")
    private Integer contactCount;
    
    @TableField("reply_count")
    private Integer replyCount;
    
    private String notes;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
