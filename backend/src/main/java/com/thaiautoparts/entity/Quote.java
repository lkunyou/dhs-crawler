package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("p_quote")
public class Quote {
    @TableId(type = IdType.AUTO)
    private Long id;

    @TableField("quote_no")
    private String quoteNo;

    @TableField("company_id")
    private Long companyId;

    @TableField(exist = false)
    private String companyName;

    @TableField("product_name")
    private String productName;

    @TableField("product_model")
    private String productModel;

    private Integer quantity;

    @TableField("unit_price")
    private BigDecimal unitPrice;

    @TableField("total_amount")
    private BigDecimal totalAmount;

    @TableField("valid_date")
    private LocalDate validDate;

    private String remark;

    private String status;

    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;

    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}