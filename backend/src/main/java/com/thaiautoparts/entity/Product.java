package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@TableName("p_product")
public class Product {
    @TableId(type = IdType.AUTO)
    private Long id;

    @TableField("product_name")
    private String productName;

    @TableField("product_code")
    private String productCode;

    private String category;

    private String brand;

    private String specification;

    @TableField("unit_price")
    private BigDecimal unitPrice;

    private Integer stock;

    private String description;

    private String status;

    private String model;

    private String dimensions;

    @TableField("pkg_length")
    private Integer pkgLength;

    @TableField("pkg_width")
    private Integer pkgWidth;

    @TableField("pkg_height")
    private Integer pkgHeight;

    @TableField("qty_per_pkg")
    private Integer qtyPerPkg;

    @TableField("car_model")
    private String carModel;

    @TableField("production_date")
    private LocalDate productionDate;

    private BigDecimal weight;

    @TableField("image_url")
    private String imageUrl;

    @TableField(value = "created_at", fill = FieldFill.INSERT)
    private LocalDateTime createdAt;

    @TableField(value = "updated_at", fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}