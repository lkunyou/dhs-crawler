package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("p_quotation_item")
public class QuotationItem {
    @TableId(type = IdType.AUTO)
    private Long id;

    @TableField("quotation_id")
    private Long quotationId;

    @TableField("product_id")
    private Long productId;

    @TableField("product_name")
    private String productName;

    @TableField("product_model")
    private String productModel;

    private Integer quantity;

    @TableField("unit_price")
    private BigDecimal unitPrice;

    @TableField("line_total")
    private BigDecimal lineTotal;

    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;

    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
