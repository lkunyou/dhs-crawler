package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_crawler_result")
public class CrawlerResult {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long taskId;
    private String sourceType;
    private String companyName;
    private String companyNameTh;
    private String companyNameEn;
    private String website;
    private String address;
    private String city;
    private String province;
    private String phone;
    private String whatsapp;
    private String email;
    private String companyType;
    private String businessDescription;
    private String productCategories;
    private String employeeCount;
    private String sourceUrl;
    private String searchKeyword;
    private String rawData;
    private String status;
    private Long syncedCompanyId;
    private Long duplicateOf;
    private String rejectionReason;
    private Integer leadScore;
    private String leadGrade;
    private Boolean isAutoPartsCore;
    private Boolean isImporterDistributor;
    private LocalDateTime createdAt;
    private LocalDateTime confirmedAt;
    private LocalDateTime syncedAt;
    private LocalDateTime updatedAt;
}
