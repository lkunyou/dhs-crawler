package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_company")
public class Company {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String companyName;
    private String companyNameTh;
    private String companyNameEn;
    private String country;
    
    @TableField("company_type")
    private String companyType;
    
    private String website;
    private String address;
    private String city;
    private String province;
    private String phone;
    private String whatsapp;
    private String email;
    
    private Integer leadScore;
    
    @TableField("lead_grade")
    private String leadGrade;
    
    @TableField(value = "score_details", typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String scoreDetails;
    
    @TableField("is_auto_parts_core")
    private Boolean isAutoPartsCore;
    
    @TableField("is_importer_distributor")
    private Boolean isImporterDistributor;
    
    @TableField("has_oem_cooperation")
    private Boolean hasOemCooperation;
    
    @TableField("employee_count")
    private String employeeCount;
    
    @TableField("website_completeness")
    private Integer websiteCompleteness;
    
    private String source;
    
    @TableField("source_url")
    private String sourceUrl;
    
    @TableField(value = "raw_data", typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String rawData;
    
    private String status;
    
    @TableField("is_duplicate")
    private Boolean isDuplicate;
    
    @TableField("duplicate_of")
    private Long duplicateOf;
    
    @TableField("assigned_to")
    private Long assignedTo;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
    
    @TableField("last_contacted_at")
    private LocalDateTime lastContactedAt;
}
