package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
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
    
    @TableField("main_products")
    private String mainProducts;
    
    @TableField("main_market")
    private String mainMarket;
    
    @TableField("import_ability")
    private Integer importAbility;
    
    @TableField("purchase_scale")
    private Integer purchaseScale;
    
    @TableField("china_supplier_acceptance")
    private Integer chinaSupplierAcceptance;
    
    @TableField("oem_aftermarket_match")
    private Integer oemAftermarketMatch;
    
    @TableField("export_ability")
    private Integer exportAbility;
    
    @TableField("customization_match")
    private Integer customizationMatch;
    
    @TableField("quality_requirement")
    private String qualityRequirement;
    
    @TableField("price_sensitivity")
    private String priceSensitivity;
    
    @TableField("delivery_requirement")
    private String deliveryRequirement;
    
    @TableField("accept_china_factory")
    private String acceptChinaFactory;
    
    @TableField("customization_ability")
    private String customizationAbility;
    
    @TableField("after_sales_requirement")
    private String afterSalesRequirement;
    
    @TableField("supply_chain_pain_points")
    private String supplyChainPainPoints;
    
    @TableField("recommended_products")
    private String recommendedProducts;
    
    @TableField("recommended_channels")
    private String recommendedChannels;
    
    @TableField("first_email_strategy")
    private String firstEmailStrategy;
    
    @TableField("follow_up_immediately")
    private String followUpImmediately;
    
    @TableField("added_to_crm")
    private String addedToCrm;
    
    @TableField("manual_follow_up")
    private String manualFollowUp;
    
    @TableField("remarketing")
    private String remarketing;
    
    @TableField("email_subject")
    private String emailSubject;
    
    @TableField("development_email")
    private String developmentEmail;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
    
    @TableField("last_contacted_at")
    private LocalDateTime lastContactedAt;
    
    @TableField("core_contact")
    private String coreContact;
    
    @TableField("annual_revenue_usd")
    private BigDecimal annualRevenueUsd;
    
    @TableField("purchase_potential")
    private String purchasePotential;
    
    @TableField("development_priority")
    private String developmentPriority;
}
