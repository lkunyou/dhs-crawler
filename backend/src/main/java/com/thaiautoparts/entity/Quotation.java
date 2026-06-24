package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("p_quotation")
public class Quotation {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    @TableField("company_id")
    private Long companyId;
    
    @TableField("contact_id")
    private Long contactId;
    
    @TableField("quotation_no")
    private String quotationNo;
    
    @TableField("product_name")
    private String productName;
    
    @TableField("product_description")
    private String productDescription;
    
    private Integer quantity;
    
    @TableField("unit_price")
    private BigDecimal unitPrice;
    
    @TableField("total_amount")
    private BigDecimal totalAmount;
    
    private String currency;
    
    @TableField("valid_until")
    private LocalDate validUntil;
    
    private String terms;
    private String notes;
    private String status;
    
    @TableField("sent_at")
    private LocalDateTime sentAt;
    
    @TableField("viewed_at")
    private LocalDateTime viewedAt;
    
    @TableField("accepted_at")
    private LocalDateTime acceptedAt;
    
    @TableField(value = "attachments", typeHandler = com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler.class)
    private String attachments;
    
    @TableField("created_by")
    private Long createdBy;
    
    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
